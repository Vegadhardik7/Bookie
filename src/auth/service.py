"""
This file defines the business logic for user-related operations in the authentication module.
It includes functions for retrieving users, checking if a user exists, and creating new users.
These functions interact with the database to perform the necessary operations.
"""

import logging  # Import logging module for logging errors and information.
from src.db.models import User  # Import the User model from the database models.
from src.auth.schemas import UserCreateModel  # Import the UserCreateModel schema for user creation.
from src.auth.utils import generated_pswd_hash  # Import the generated_pswd_hash function for password hashing.
from sqlmodel.ext.asyncio.session import AsyncSession  # Import the AsyncSession class for asynchronous database sessions.
from sqlmodel import select  # Import select for constructing SQL queries.
from passlib.context import CryptContext  # Import CryptContext for password hashing.

logging.basicConfig(level=logging.INFO)  # Configure logging to display information level logs.

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
        statement = select(User)  # Construct a SQL query to select all users.
        result = await session.exec(statement)  # Execute the query.
        return result.all()  # Return all users.

    async def get_user_by_email(self, email: str, session: AsyncSession):
        """
        Retrieve a user by their email address.
        Args:
            email: Email of the user to search for.
            session: Database session (injected via dependency).
        Returns:
            The user object if found, otherwise None.
        """
        statement = select(User).where(User.email == email)  # Construct a SQL query to select a user by email.
        result = await session.exec(statement)  # Execute the query.
        usr = result.first()  # Get the first result (if any).
        return usr  # Return the user object or None.

    async def user_exists(self, email: str, session: AsyncSession):
        """
        Check if a user with the given email already exists.
        Args:
            email: Email of the user to check.
            session: Database session (injected via dependency).
        Returns:
            True if the user exists, False otherwise.
        """
        usr = await self.get_user_by_email(email, session)  # Retrieve the user by email.
        return usr is not None  # Return True if the user exists, otherwise False.

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
        usr_data_dict = user_data.model_dump()  # Convert the user data to a dictionary.
        new_user = User(**usr_data_dict)  # Create a new User object.
        new_user.password = generated_pswd_hash(user_data.password)  # Hash the user's password.
        new_user.role = "user"  # Set the user's role to "user".

        # Add the new user to the database
        session.add(new_user)  # Add the new user to the session.
        await session.commit()  # Commit the transaction.
        await session.refresh(new_user)  # Refresh the user instance to include the database-generated fields.
        logging.info(f"create_user: User created successfully: {new_user}")  # Log the successful creation of the user.

        return new_user  # Return the newly created user object.