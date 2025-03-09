"""
This file defines the SQLAlchemy models for the database.
It includes models for User, Book, and Review, which represent the corresponding tables in the database.
These models are used to interact with the database and perform CRUD operations.
"""

import uuid  # Import the uuid module for handling UUIDs.
from typing import List, Optional  # Import typing utilities for type annotations.
from datetime import datetime, date  # Import datetime and date for handling date and time.
import sqlalchemy.dialects.postgresql as pg  # Import PostgreSQL dialects for SQLAlchemy.
from sqlmodel import SQLModel, Field, Column, Relationship  # Import SQLModel, Field, Column, and Relationship from sqlmodel.

# Create User
class User(SQLModel, table=True):
    __tablename__: str = "user"
    
    uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID, 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
            )
        )  # User's unique identifier (UUID).
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  # Timestamp of when the user was created.
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  # Timestamp of when the user was last updated.
    username: str  # Username of the user.
    email: str  # Email of the user.
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))  # Role of the user (default is "user").
    password: str  # Password of the user.
    first_name: str  # First name of the user.
    last_name: str  # Last name of the user.
    is_verified: bool = Field(default=False)  # Whether the user's email is verified.
    books: List["BookModel"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})  # List of books associated with the user.
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})  # List of reviews associated with the user.

    """ String representation of the User object """
    def __repr__(self):
        return f"<User {self.username}>"

# Create Book
class BookModel(SQLModel, table=True):
    __tablename__: str = "book"

    uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID, 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
            )
        )  # Book's unique identifier (UUID).
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  # Timestamp of when the book was created.
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  # Timestamp of when the book was last updated.
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})  # List of reviews associated with the book.
    title: Optional[str] = None  # Title of the book.
    author: Optional[str] = None  # Author of the book.
    publisher: Optional[str] = None  # Publisher of the book.
    page_count: Optional[int] = None  # Number of pages in the book.
    language: Optional[str] = "English"  # Language of the book (default is English).
    published_date: Optional[date] = None  # Date when the book was published.
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user.uid")  # UID of the user who created the book.
    user: Optional[User] = Relationship(back_populates="books")  # Relationship to the user who created the book.

    def __repr__(self):
        return f"BookModel({self.title}, {self.author}, {self.publisher}, {self.page_count}, {self.language}, {self.published_date})"

# Create Review
class Review(SQLModel, table=True):
    __tablename__: str = "reviews"

    uid: uuid.UUID = Field(
        sa_column = Column(
            pg.UUID, 
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4
            )
        )  # Review's unique identifier (UUID).
    rating: int = Field(lt=5)  # Rating of the book (less than 5).
    review_text: str  # Text of the review.
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  # Timestamp of when the review was created.
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))  # Timestamp of when the review was last updated.
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user.uid")  # UID of the user who created the review.
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="book.uid")  # UID of the book being reviewed.
    user: Optional[User] = Relationship(back_populates="reviews")  # Relationship to the user who created the review.
    book: Optional[BookModel] = Relationship(back_populates="reviews")  # Relationship to the book being reviewed.

    """ String representation of the Review object """
    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"