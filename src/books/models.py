from typing import Optional
from datetime import datetime, date
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column
import uuid

# Create Book
class BookModel(SQLModel, table=True):

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
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = "English"
    published_date: Optional[date] = None
    
    def __repr__(self):
        return f"BookModel({self.title}, {self.author}, {self.publisher}, {self.page_count}, {self.language}, {self.published_date})"