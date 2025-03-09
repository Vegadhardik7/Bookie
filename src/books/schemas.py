"""
This file defines the Pydantic models (schemas) for the book-related data.
These models are used for request validation and response formatting in the book endpoints.
They ensure that the data being sent and received adheres to the expected structure and types.
"""

import uuid  # Import the uuid module for handling UUIDs.
from src.reviews.schemas import ReviewModel  # Import the ReviewModel from the reviews module.
from typing import Optional, List  # Import typing utilities for type annotations.
from datetime import datetime, date  # Import datetime and date for handling date and time.
from pydantic import BaseModel  # Import BaseModel from pydantic for creating Pydantic models.

# Create Book
class BookModel(BaseModel):
    """
    Pydantic model for representing a book.
    """
    uid: Optional[uuid.UUID] = None  # Book's unique identifier (UUID).
    title: Optional[str] = None  # Title of the book.
    author: Optional[str] = None  # Author of the book.
    publisher: Optional[str] = None  # Publisher of the book.
    page_count: Optional[int] = None  # Number of pages in the book.
    language: Optional[str] = "English"  # Language of the book (default is English).
    created_at: Optional[datetime] = None  # Timestamp of when the book was created.
    updated_at: Optional[datetime] = None  # Timestamp of when the book was last updated.
    published_date: Optional[date] = None  # Date when the book was published.

class BookDetailModel(BookModel):
    """
    Pydantic model for representing detailed information about a book, including reviews.
    Inherits from BookModel.
    """
    reviews: List[ReviewModel]  # List of reviews associated with the book.

class BookCreateModel(BaseModel):
    """
    Pydantic model for creating a new book.
    """
    title: Optional[str] = None  # Title of the book.
    author: Optional[str] = None  # Author of the book.
    publisher: Optional[str] = None  # Publisher of the book.
    page_count: Optional[int] = None  # Number of pages in the book.
    language: Optional[str] = "English"  # Language of the book (default is English).
    created_at: Optional[datetime] = None  # Timestamp of when the book was created.
    updated_at: Optional[datetime] = None  # Timestamp of when the book was last updated.
    published_date: Optional[date] = None  # Date when the book was published.

class UpdateBookModel(BaseModel):
    """
    Pydantic model for updating an existing book.
    """
    title: Optional[str] = None  # Title of the book.
    author: Optional[str] = None  # Author of the book.
    publisher: Optional[str] = None  # Publisher of the book.
    page_count: Optional[int] = None  # Number of pages in the book.
    language: Optional[str] = "English"  # Language of the book (default is English).
    published_date: Optional[date] = None  # Date when the book was published.

class BOOKS:
    """
    Class representing a book with attributes for title, author, publisher, published date, page count, and language.
    """
    def __init__(self, title: Optional[str], author: Optional[str], publisher: Optional[str], 
                 published_date: Optional[date], page_count: Optional[int], language: Optional[str]):
        self.id = str(uuid.uuid4())  # Generate a unique identifier for the book.
        self.title = title  # Title of the book.
        self.author = author  # Author of the book.
        self.publisher = publisher  # Publisher of the book.
        self.published_date = published_date  # Date when the book was published.
        self.page_count = page_count  # Number of pages in the book.
        self.language = language  # Language of the book.