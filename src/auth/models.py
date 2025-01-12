import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column


class User(SQLModel, table=True):
    # __tablename__: str = "users"
    
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
    password: str # = Field(exclude=True) # won't show password in response
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)

    """ String representation of the User object """
    def __repr__(self):
        return f"<User {self.username}>"
