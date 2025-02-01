from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import AsyncGenerator
from src.config import Config
from sqlmodel import SQLModel

engine = create_async_engine(url=Config.DATABASE_URL, echo=True, future=True) # echo is use for logging

# This function is going to help us to connect our database
async def init_db()->None:
    async with engine.begin() as conn:
        from src.db.models import BookModel
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = async_sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session