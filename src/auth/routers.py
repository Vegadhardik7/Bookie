import logging
from src.db.main import get_session
from datetime import datetime, timedelta
from src.auth.service import UserService
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
from src.auth.dependencies import RefreshTokenBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.schemas import UserCreateModel, UserModel, UserLoginModel
from src.auth.utils import create_access_token, verify_password, generated_pswd_hash

auth_router = APIRouter()
user_Service = UserService()

REFRESH_TOKEN_EXPIRY = timedelta(days=2)

@auth_router.get("/users", response_model=list[UserModel])
async def get_all_users(session: AsyncSession=Depends(get_session)):
    try:
        users = await user_Service.get_all_user(session=session)
        return users
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession=Depends(get_session)):
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
async def login_user(login_data: UserLoginModel, session: AsyncSession=Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_Service.get_user_by_email(email, session=session)

    if user is not None:
        password_valid = verify_password(password, generated_pswd_hash(password))

        if password_valid:
            access_token = create_access_token(user_data={"email": user.email, 
                                                          "user_uid": str(user.uid)})
            
            refresh_token = create_access_token(user_data={"email": user.email, 
                                                           "user_uid": str(user.uid)}, 
                                                           refresh=True, expiry=REFRESH_TOKEN_EXPIRY)

            return JSONResponse(content={"message": "Login successful", 
                                         "access token": access_token, 
                                         "refresh token": refresh_token, 
                                         "user":{"email": user.email, "uid": str(user.uid)}})
        
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
# once we receive the refresh token, we can use it to generate a new access token
@auth_router.get("/refresh_token")
async def get_new_access_token(token_details:dict=Depends(RefreshTokenBearer())):
    expiry_time = token_details['expire']
    expire_time_formated = datetime.strptime(expiry_time, '%Y-%m-%d %H:%M:%S.%f')
    if expire_time_formated > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'], refresh=False)
        return JSONResponse(content={"message": "Access token refreshed successfully", "access token": new_access_token})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
