"""In this we are going to write all our logic regarding CRUD operations"""

from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, UpdateBookModel
from sqlmodel import select, desc
from uuid import UUID
from .models import BookModel
from fastapi import HTTPException


class BookService:
    async def get_all_books(self, session:AsyncSession):
        # select * from books order by created_at desc;
        statement = select(BookModel).order_by(desc(BookModel.created_at)) 
        result = await session.exec(statement)
        return result.all()
    
    async def get_user_books(self, user_uid:str, session:AsyncSession):
        # select * from books order by created_at desc;
        statement = select(BookModel).where(BookModel.user_uid == user_uid).order_by(desc(BookModel.created_at)) 
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid: str, session:AsyncSession):
        # select * from books where uid = book_uid;
        statement = select(BookModel).where(BookModel.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()

        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel,user_uid:str,session:AsyncSession):
        # insert into books values (book_data);
        book_data_dict = book_data.model_dump()
        newbook = BookModel(**book_data_dict)
        newbook.user_uid = UUID(user_uid)
        session.add(newbook)
        await session.commit()
        return newbook
    
    async def update_book(self, book_uid:str, update_data: UpdateBookModel,session:AsyncSession):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()

            for key, value in update_data_dict.items():
                if value is not None:
                    setattr(book_to_update, key, value) 

            await session.commit()
            await session.refresh(book_to_update)
            return book_to_update
        else:
            raise HTTPException(status_code=404, detail=f"Book with ID '{book_uid}' not found")
            
    async def delete_book(self, book_uid:str, session:AsyncSession):
        # delete from books where uid = book_uid;
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return book_to_delete  # Return the deleted book
        else:
            return None