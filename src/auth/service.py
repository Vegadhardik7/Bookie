import logging
from src.auth.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import generated_pswd_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from passlib.context import CryptContext

logging.basicConfig(level=logging.INFO)

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    async def get_all_user(self, session: AsyncSession):
        """
        Retrieve all users from the database.
        Args:
            session: Database session (injected via dependency).
        Returns:
            List of all users.
        """
        async with session.begin():
            statement = select(User)
            result = await session.exec(statement)
            return result.all()

    async def get_user_by_email(self, email: str, session: AsyncSession):
        """
        Retrieve a user by their email address.
        Args:
            email: Email of the user to search for.
            session: Database session (injected via dependency).
        Returns:
            The user object if found, otherwise None.
        """
        async with session.begin():
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            usr = result.first()
            return usr
    
    async def user_exists(self, email: str, session: AsyncSession):
        """
        Check if a user with the given email already exists.
        Args:
            email: Email of the user to check.
            session: Database session (injected via dependency).
        Returns:
            True if the user exists, False otherwise.
        """
        usr = await self.get_user_by_email(email, session)
        return usr is not None 

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        """
        Create a new user in the database.
        Args:
            user_data: Data for the new user (email, password, etc.).
            session: Database session (injected via dependency).
        Returns:
            The newly created user object.
        Raises:
            ValueError: If a user with the given email already exists.
        """
        # Check if the user already exists
        if await self.user_exists(user_data.email, session):  
            raise ValueError("User with this email already exists")

        # Prepare the user data for insertion
        usr_data_dict = user_data.model_dump()
        new_user = User(**usr_data_dict)
        new_user.password = generated_pswd_hash(user_data.password)  # Hash the user's password
        new_user.role = "user"

        # Add the new user to the database
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)  # Refresh the user instance to include the database-generated fields
        logging.info(f"create_user: User created successfully: {new_user}")

        return new_user
