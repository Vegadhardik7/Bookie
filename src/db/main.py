"""
This file defines the database connection and session management for the FastAPI application.
It includes functions for initializing the database and providing asynchronous database sessions.
These functions ensure that the application can interact with the database efficiently and handle database operations asynchronously.
"""

from sqlmodel.ext.asyncio.session import AsyncSession  # Import the AsyncSession class for asynchronous database sessions.
from sqlalchemy.ext.asyncio import create_async_engine  # Import create_async_engine for creating an asynchronous database engine.
from sqlalchemy.ext.asyncio import async_sessionmaker  # Import async_sessionmaker for creating asynchronous session makers.
from typing import AsyncGenerator  # Import AsyncGenerator for type annotations.
from src.config import Config  # Import the Config class for accessing configuration settings.
from sqlmodel import SQLModel  # Import SQLModel for handling SQLAlchemy models.

# Create an asynchronous database engine using the database URL from the configuration
engine = create_async_engine(url=Config.DATABASE_URL, echo=True, future=True)  # echo is used for logging

# This function initializes the database by creating all tables defined in the models
async def init_db() -> None:
    async with engine.begin() as conn:  # Begin an asynchronous connection to the database
        from src.db.models import BookModel  # Import the BookModel from the database models
        await conn.run_sync(SQLModel.metadata.create_all)  # Create all tables defined in the models

# This function provides an asynchronous database session for handling database operations
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )  # Create an asynchronous session maker
    async with async_session() as session:  # Provide an asynchronous session
        yield session  # Yield the session for use in database operations