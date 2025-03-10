"""
This file defines the authentication-related routes for the FastAPI application.
It includes endpoints for user signup, login, token refresh, fetching user details, and logout.
These routes use custom dependencies for token validation and user authentication to ensure that
only authorized users can access certain endpoints.
"""

import logging  # Import logging module for logging errors and information.
from src.db.models import User  # Import the User model from the database models.
from src.db.main import get_session  # Import the get_session function for database session management.
from datetime import datetime, timedelta  # Import datetime and timedelta for handling date and time operations.
from src.auth.service import UserService  # Import the UserService class for user-related business logic.
from src.db.redis import add_jti_to_blocklist  # Import the add_jti_to_blocklist function for adding tokens to the blocklist.
from fastapi.responses import JSONResponse  # Import JSONResponse for sending JSON responses.
from fastapi.exceptions import HTTPException  # Import HTTPException for raising HTTP exceptions.
from fastapi import APIRouter, Depends, status  # Import FastAPI utilities for routing, dependencies, and status codes.
from sqlmodel.ext.asyncio.session import AsyncSession  # Import the AsyncSession class for asynchronous database sessions.
from src.auth.utils import create_access_token, verify_password  # Import utility functions for token creation and password verification.
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel, UserBooksModel  # Import Pydantic models for request and response validation.
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker  # Import custom dependencies for token validation and user authentication.

# Initialize the router for authentication-related endpoints
auth_router = APIRouter()
user_Service = UserService()  # Create an instance of the UserService class for user-related business logic.
role_checker = RoleChecker(['admin', 'user'])  # Create an instance of the RoleChecker class to check user roles.

# Define the expiration time for the refresh token
REFRESH_TOKEN_EXPIRY = timedelta(days=2)

@auth_router.get("/users", response_model=list[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session), _ : bool= Depends(role_checker)):
    """
    Fetch all users from the database.
    Args:
        session: Database session (injected via dependency).
    Returns:
        List of users in the system.
    """
    try:
        users = await user_Service.get_all_user(session=session)
        return users
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    """
    Create a new user account.
    Args:
        user_data: Data for the new user (email, password, etc.).
        session: Database session (injected via dependency).
    Returns:
        Details of the newly created user.
    """
    try:
        email = user_data.email
        usr_exists = await user_Service.user_exists(email, session=session)

        if usr_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists")
        
        new_user = await user_Service.create_user(user_data, session=session)

        return new_user 
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@auth_router.post("/login", response_model=UserLoginModel)
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    """
    Authenticate the user and provide access and refresh tokens.
    Args:
        login_data: User's email and password.
        session: Database session (injected via dependency).
    Returns:
        Access token, refresh token, and user details.
    """
    email = login_data.email
    password = login_data.password

    user = await user_Service.get_user_by_email(email, session=session)

    if user is not None:
        password_valid = verify_password(password, user.password)

        if password_valid:
            access_token = create_access_token(user_data={"email": user.email, 
                                                          "user_uid": str(user.uid), 
                                                          "role":user.role})
            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}, 
                refresh=True, 
                expiry=REFRESH_TOKEN_EXPIRY
            )

            return JSONResponse(content={
                "message": "Login successful",
                "access token": access_token,
                "refresh token": refresh_token,
                "user": {"email": user.email, "uid": str(user.uid)}
            })
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    """
    Generate a new access token using a valid refresh token.
    Args:
        token_details: Details of the refresh token (injected via dependency).
    Returns:
        New access token.
    """
    expiry_time = token_details['expire']
    expire_time_formated = datetime.strptime(expiry_time, '%Y-%m-%d %H:%M:%S.%f')
    if expire_time_formated > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'], refresh=False)
        return JSONResponse(content={"message": "Access token refreshed successfully", "access token": new_access_token})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")

@auth_router.get("/me", response_model=UserBooksModel)
async def get_me(user: User = Depends(get_current_user), _ : bool= Depends(role_checker)):
    """
    Get details of the currently authenticated user.
    Args:
        user: User object (injected via dependency).
    Returns:
        User details.
    """
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    return user

@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    """
    Revoke the user's access token by adding it to the blocklist.
    Args:
        token_details: Access token details (injected via dependency).
    Returns:
        Success message for logout.
    """
    jti = token_details['jti']
    await add_jti_to_blocklist(jti=jti)
    return JSONResponse(content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK)