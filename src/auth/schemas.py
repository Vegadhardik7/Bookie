import uuid
import datetime
from sqlmodel import Field
from pydantic import BaseModel

class UserCreateModel(BaseModel):
    username: str = Field(max_length=50)
    email: str = Field(max_length=80)
    password: str = Field(min_length=6)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password: str = Field(exclude=True)  # Exclude password from response
    created_at : datetime.datetime
    updated_at : datetime.datetime
    class Config:
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy models