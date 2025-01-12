from fastapi import APIRouter, Depends, status
from src.auth.service import UserService
from src.db.main import get_session
from fastapi.exceptions import HTTPException
from src.auth.schemas import UserCreateModel, UserModel
from sqlmodel.ext.asyncio.session import AsyncSession
import logging

auth_router = APIRouter()
user_Service = UserService()

@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession=Depends(get_session)):
    try:
        email = user_data.email
        usr_exists = await user_Service.user_exists(email, session=session)

        if usr_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists")
        
        new_user = await user_Service.create_user(user_data, session=session)

        # Convert new_user to a dictionary or a Pydantic model that matches UserModel
        user_dict = {
            "username": new_user.username,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "password": new_user.password,  # Ensure password is hashed
        }

        return user_dict
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@auth_router.get("/users", response_model=list[UserModel])
async def get_all_users(session: AsyncSession=Depends(get_session)):
    try:
        users = await user_Service.get_all_user(session=session)
        return users
    except Exception as e:
        logging.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")