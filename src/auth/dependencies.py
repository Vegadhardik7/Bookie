"""
This file is important because it defines custom dependencies for token validation and user authentication.
It includes custom classes for validating access and refresh tokens, as well as dependencies for fetching the
currently authenticated user and checking user roles. These dependencies are used to protect routes and ensure
that only authorized users can access certain endpoints.
"""

from src.errors import (  # Import custom error classes for handling various authentication and authorization errors.
    InvalidToken, 
    RevokedToken, 
    AccessTokenRequired, 
    RefreshTokenRequired, 
    InsufficientPermission,
    UserNotFound,
)
from src.db.models import User  # Import the User model from the database models.
from typing import List, Any  # Import typing utilities for type annotations.
from .service import UserService  # Import the UserService class for user-related business logic.
from src.db.main import get_session  # Import the get_session function for database session management.
from fastapi import Request, Depends  # Import FastAPI utilities for handling requests and dependencies.
from fastapi.security import HTTPBearer  # Import the HTTPBearer class for handling HTTP Bearer authentication.
from src.db.redis import token_in_blocklist  # Import the token_in_blocklist function for checking if a token is in the blocklist.
from src.auth.utils import decode_access_token  # Import the decode_access_token function for decoding JWT tokens.
from sqlmodel.ext.asyncio.session import AsyncSession  # Import the AsyncSession class for asynchronous database sessions.
from fastapi.security.http import HTTPAuthorizationCredentials  # Import the HTTPAuthorizationCredentials class for handling HTTP authorization credentials.

user_service = UserService()  # Create an instance of the UserService class for user-related business logic.

# Custom TokenBearer class to validate tokens
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        """
        Initialize the TokenBearer class, inheriting from FastAPI's HTTPBearer.
        :param auto_error: Whether to automatically raise an exception if authentication fails.
        """
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        """
        Override the __call__ method to extract and validate the token from the request.
        :param request: The incoming HTTP request.
        :return: Decoded token data if valid.
        :raises HTTPException: If the token is missing, invalid, or expired.
        """
        # Call the parent class's __call__ method to extract credentials
        credentials = await super().__call__(request)
        
        if credentials is None:
            raise InvalidToken()
        
        token = credentials.credentials  # Extract the token

        if token is None:
            raise AccessTokenRequired()

        # Check if the token is valid
        if not self.token_valid(token):
            raise InvalidToken()
        
        # Decode the token to get token data
        token_data = decode_access_token(token)

        # Check if the token is in the blocklist (revoked or blacklisted)
        if await token_in_blocklist(token_data["jti"]):
            raise RevokedToken()

        # Verify token-specific data (to be implemented by child classes)
        self.verify_token_data(token_data)

        return token_data  # type: ignore # Return the validated token data

    def token_valid(self, token: str) -> bool:
        """
        Check if the token is valid by decoding it.
        :param token: The token string.
        :return: True if the token is valid, otherwise False.
        """
        token_data = decode_access_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        """
        Verify the token data. Must be implemented in child classes.
        :param token_data: Decoded token data.
        :raises NotImplementedError: If the method is not overridden in child classes.
        """
        raise NotImplementedError("Please override this method in child class")

# Custom class for validating access tokens
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        """
        Verify the token data to ensure it's an access token.
        :param token_data: Decoded token data.
        :raises AccessTokenRequired: If the token is not an access token.
        """
        if token_data and token_data["refresh"]:
            raise AccessTokenRequired()
        
# Custom class for validating refresh tokens
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        """
        Verify the token data to ensure it's a refresh token.
        :param token_data: Decoded token data.
        :raises RefreshTokenRequired: If the token is not a refresh token.
        """
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequired()

# Dependency to fetch the currently authenticated user
async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), 
                           session: AsyncSession = Depends(get_session)):
    """
    Dependency to fetch the currently authenticated user from the database.
    :param token_details: Decoded token data from the access token.
    :param session: Database session (AsyncSession).
    :return: The user object corresponding to the token's email.
    :raises UserNotFound: If the user does not exist in the database.
    """
    # Extract user email from the token details
    user_email = token_details['user']['email']
    
    # Fetch the user object from the database
    user = await user_service.get_user_by_email(user_email, session)
    
    if not user:
        raise UserNotFound()
    
    # Return the user object
    return user

# Check the role of the user
class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise InsufficientPermission()
