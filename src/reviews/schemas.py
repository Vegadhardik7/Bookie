import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import Field
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ReviewModel(BaseModel):
    uid: uuid.UUID
    review_text: str
    created_at: datetime 
    updated_at: datetime
    rating: int = Field(lt=5) 
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]


class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text: str