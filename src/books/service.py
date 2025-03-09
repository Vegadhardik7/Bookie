"""In this we are going to write all our logic regarding CRUD operations"""

from sqlmodel.ext.asyncio.session import AsyncSession  # Import the AsyncSession class for asynchronous database sessions.
from .schemas import BookCreateModel, UpdateBookModel  # Import the BookCreateModel and UpdateBookModel schemas for book creation and updates.
from sqlmodel import select, desc  # Import select for constructing SQL queries and desc for ordering results in descending order.
from uuid import UUID  # Import the UUID class for handling UUIDs.
from src.db.models import BookModel  # Import the BookModel from the database models.
from fastapi import HTTPException  # Import HTTPException for raising HTTP exceptions.

class BookService:
    async def get_all_books(self, session: AsyncSession):
        """
        Retrieve all books from the database, ordered by creation date in descending order.
        Args:
            session: Database session (injected via dependency).
        Returns:
            List of all books.
        """
        statement = select(BookModel).order_by(desc(BookModel.created_at))  # Construct a SQL query to select all books ordered by creation date.
        result = await session.exec(statement)  # Execute the query.
        return result.all()  # Return all books.

    async def get_user_books(self, user_uid: str, session: AsyncSession):
        """
        Retrieve all books from the database created by a specific user, ordered by creation date in descending order.
        Args:
            user_uid: UID of the user who created the books.
            session: Database session (injected via dependency).
        Returns:
            List of all books created by the specified user.
        """
        statement = select(BookModel).where(BookModel.user_uid == user_uid).order_by(desc(BookModel.created_at))  # Construct a SQL query to select books by user UID ordered by creation date.
        result = await session.exec(statement)  # Execute the query.
        return result.all()  # Return all books created by the specified user.

    async def get_book(self, book_uid: str, session: AsyncSession):
        """
        Retrieve a specific book by its unique ID.
        Args:
            book_uid: Unique identifier of the book.
            session: Database session (injected via dependency).
        Returns:
            The book object if found, otherwise None.
        """
        statement = select(BookModel).where(BookModel.uid == book_uid)  # Construct a SQL query to select a book by its UID.
        result = await session.exec(statement)  # Execute the query.
        book = result.first()  # Get the first result (if any).
        return book if book is not None else None  # Return the book object or None.

    async def create_book(self, book_data: BookCreateModel, user_uid: str, session: AsyncSession):
        """
        Create a new book in the database.
        Args:
            book_data: Data for creating a new book.
            user_uid: UID of the user creating the book.
            session: Database session (injected via dependency).
        Returns:
            The newly created book object.
        """
        book_data_dict = book_data.model_dump()  # Convert the book data to a dictionary.
        newbook = BookModel(**book_data_dict)  # Create a new BookModel object.
        newbook.user_uid = UUID(user_uid)  # Set the user UID for the new book.
        session.add(newbook)  # Add the new book to the session.
        await session.commit()  # Commit the transaction.
        return newbook  # Return the newly created book.

    async def update_book(self, book_uid: str, update_data: UpdateBookModel, session: AsyncSession):
        """
        Update details of an existing book by its unique ID.
        Args:
            book_uid: Unique identifier of the book to update.
            update_data: Updated book data.
            session: Database session (injected via dependency).
        Returns:
            The updated book object.
        Raises:
            HTTPException: If the book with the given ID is not found.
        """
        book_to_update = await self.get_book(book_uid, session)  # Retrieve the book to update.

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()  # Convert the update data to a dictionary.

            for key, value in update_data_dict.items():
                if value is not None:
                    setattr(book_to_update, key, value)  # Update the book's attributes with the new values.

            await session.commit()  # Commit the transaction.
            await session.refresh(book_to_update)  # Refresh the book instance to include the updated fields.
            return book_to_update  # Return the updated book.
        else:
            raise HTTPException(status_code=404, detail=f"Book with ID '{book_uid}' not found")  # Raise an HTTPException if the book is not found.

    async def delete_book(self, book_uid: str, session: AsyncSession):
        """
        Delete a book from the database by its unique ID.
        Args:
            book_uid: Unique identifier of the book to delete.
            session: Database session (injected via dependency).
        Returns:
            The deleted book object if found, otherwise None.
        """
        book_to_delete = await self.get_book(book_uid, session)  # Retrieve the book to delete.

        if book_to_delete is not None:
            await session.delete(book_to_delete)  # Delete the book from the session.
            await session.commit()  # Commit the transaction.
            return book_to_delete  # Return the deleted book.
        else:
            return None  # Return None if the book is not found.