"""
This file defines the review-related routes for the FastAPI application.
It includes endpoints for adding reviews to books.
These routes use custom dependencies for token validation to ensure that only authorized users can access certain endpoints.
"""

from src.db.models import User  # Import the User model from the database models.
from src.db.main import get_session  # Import the get_session function for database session management.
from fastapi import APIRouter, Depends  # Import FastAPI utilities for routing and dependencies.
from src.reviews.schemas import ReviewCreateModel, ReviewModel  # Import Pydantic models for request and response validation.
from sqlmodel.ext.asyncio.session import AsyncSession  # Import the AsyncSession class for asynchronous database sessions.
from src.reviews.service import ReviewService  # Import the ReviewService class for review-related business logic.
from src.auth.dependencies import get_current_user  # Import custom dependency for getting the current authenticated user.

# Initialize FastAPI Router for reviews
review_router = APIRouter()

# ReviewService instance for handling review-related operations
review_service = ReviewService()

@review_router.post("/book/{book_uid}")
async def add_review_to_books(book_uid: str,
                              review_data: ReviewCreateModel, 
                              current_user: User = Depends(get_current_user), 
                              session: AsyncSession = Depends(get_session)):
    """
    Add a review to a book.

    Args:
        book_uid (str): Unique identifier of the book to add the review to.
        review_data (ReviewCreateModel): Data for creating the review.
        current_user (User): The current authenticated user (injected via dependency).
        session (AsyncSession): Database session for querying (injected via dependency).

    Returns:
        The newly created review.
    """
    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        review_data=review_data,
        book_uid=book_uid,
        session=session
    )

    return new_review  # Return the newly created review.