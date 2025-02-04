import uuid
from typing import List, Optional
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column, Relationship

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
        )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    username: str
    email: str
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    password: str # = Field(exclude=True) # won't show password in response
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    books: List["BookModel"] = Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})
    reviews: List["Review"] = Relationship(back_populates="user",sa_relationship_kwargs={"lazy":"selectin"})


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
        )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    reviews: List["Review"] = Relationship(back_populates="book",sa_relationship_kwargs={"lazy":"selectin"}) 
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = "English"
    published_date: Optional[date] = None
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user.uid")
    user: Optional[User] = Relationship(back_populates="books")

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
        )
    
    rating: int = Field(lt=5)
    review_text: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="book.uid")
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[BookModel] = Relationship(back_populates="reviews")

    """ String representation of the Review object """
    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"