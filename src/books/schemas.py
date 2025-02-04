import uuid
from src.reviews.schemas import ReviewModel
from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel

# Create Book
class BookModel(BaseModel):
    uid: Optional[uuid.UUID] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = "English"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_date: Optional[date] = None

class BookDetailModel(BookModel):
    reviews: List[ReviewModel]

class BookCreateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = "English"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_date: Optional[date] = None

class UpdateBookModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = "English"
    published_date: Optional[date] = None

class BOOKS:
    def __init__(self, title: Optional[str], author: Optional[str], publisher: Optional[str], 
                 published_date: Optional[date], page_count: Optional[int], language: Optional[str]):
        
        self.id = str(uuid.uuid4())
        self.title = title 
        self.author = author
        self.publisher = publisher
        self.published_date = published_date
        self.page_count = page_count
        self.language= language