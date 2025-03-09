"""
This file defines the Pydantic models (schemas) for the review-related data.
These models are used for request validation and response formatting in the review endpoints.
They ensure that the data being sent and received adheres to the expected structure and types.
"""

import uuid  # Import the uuid module for handling UUIDs.
from typing import Optional  # Import Optional for optional type annotations.
from datetime import datetime  # Import datetime for handling date and time.
from sqlmodel import Field  # Import Field from sqlmodel for defining model fields.
from pydantic import BaseModel  # Import BaseModel from pydantic for creating Pydantic models.

class ReviewModel(BaseModel):
    """
    Pydantic model for representing a review.
    """
    uid: uuid.UUID  # Review's unique identifier (UUID).
    review_text: str  # Text of the review.
    created_at: datetime  # Timestamp of when the review was created.
    updated_at: datetime  # Timestamp of when the review was last updated.
    rating: int = Field(lt=5)  # Rating of the book (less than 5).
    user_uid: Optional[uuid.UUID]  # UID of the user who created the review.
    book_uid: Optional[uuid.UUID]  # UID of the book being reviewed.

class ReviewCreateModel(BaseModel):
    """
    Pydantic model for creating a new review.
    """
    rating: int = Field(lt=5)  # Rating of the book (less than 5).
    review_text: str  # Text of the review.