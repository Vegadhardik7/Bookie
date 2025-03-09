"""
This file defines the Pydantic models (schemas) for the authentication-related data.
These models are used for request validation and response formatting in the authentication endpoints.
They ensure that the data being sent and received adheres to the expected structure and types.
"""

import uuid  # Import the uuid module for handling UUIDs.
import datetime  # Import the datetime module for handling date and time.
from typing import List, Optional  # Import typing utilities for type annotations.
from sqlmodel import Field  # Import Field from sqlmodel for defining model fields.
from pydantic import BaseModel  # Import BaseModel from pydantic for creating Pydantic models.
from src.reviews.schemas import ReviewModel  # Import the ReviewModel from the reviews module.
from src.books.schemas import BookModel  # Import the BookModel from the books module.

class UserCreateModel(BaseModel):
    """
    Pydantic model for creating a new user.
    """
    username: str = Field(max_length=50)  # Username with a maximum length of 50 characters.
    email: str = Field(max_length=80)  # Email with a maximum length of 80 characters.
    password: str = Field(min_length=6)  # Password with a minimum length of 6 characters.
    first_name: str = Field(max_length=50)  # First name with a maximum length of 50 characters.
    last_name: str = Field(max_length=50)  # Last name with a maximum length of 50 characters.

class UserModel(BaseModel):
    """
    Pydantic model for representing a user.
    """
    uid: uuid.UUID  # User's unique identifier (UUID).
    username: str  # Username.
    email: str  # Email.
    first_name: str  # First name.
    last_name: str  # Last name.
    is_verified: bool  # Whether the user's email is verified.
    password: str = Field(exclude=True)  # Exclude password from response.
    created_at: datetime.datetime  # Timestamp of when the user was created.
    updated_at: datetime.datetime  # Timestamp of when the user was last updated.

class UserBooksModel(UserModel):
    """
    Pydantic model for representing a user along with their books and reviews.
    Inherits from UserModel.
    """
    books: Optional[List[BookModel]] = None  # List of books associated with the user (optional).
    reviews: List[ReviewModel]  # List of reviews associated with the user.

class UserLoginModel(BaseModel):
    """
    Pydantic model for user login.
    """
    email: str  # User's email.
    password: str  # User's password.