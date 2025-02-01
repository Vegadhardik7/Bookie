from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import BookModel, BookCreateModel, UpdateBookModel
from src.db.models import BookModel
from src.books.service import BookService
from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker

# Initialize FastAPI Router for books
book_router = APIRouter()

# BookService instance for handling book-related operations
book_service = BookService()

# Dependencies for authentication and role-based access control
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(['admin', 'user']))

# ----------------- List all the books -----------------
@book_router.get("/", response_model=List[BookModel], dependencies=[role_checker])
async def getAllBooks(
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    """
    Retrieve all books from the database.

    Args:
        session (AsyncSession): Database session for querying.
        token_details: User details retrieved from the access token.

    Returns:
        List[BookModel]: List of all books.
    """
    print(f"User details: {token_details}")
    return await book_service.get_all_books(session)

# ----------------- List all the books added by a specific user -----------------
@book_router.get("/user/{user_uid}", response_model=List[BookModel], dependencies=[role_checker])
async def get_user_book_submissions(
    user_uid : str,
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    """
    Retrieve all books from the database created by a perticular user.

    Args:
        session (AsyncSession): Database session for querying.
        user_id: UID of the user who has inserted data of the books.
        token_details: User details retrieved from the access token.

    Returns:
        List[BookModel]: List of all books added by that perticular user.
    """
    print(f"User details: {token_details}")
    return await book_service.get_user_books(user_uid, session)

# ----------------- List the book data by ID -----------------
@book_router.get("/{book_uid}", status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def getBook(
    book_uid: str, 
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
) -> dict:
    """
    Retrieve details of a specific book by its unique ID.

    Args:
        book_uid (str): Unique identifier of the book.
        session (AsyncSession): Database session for querying.
        token_details: User details retrieved from the access token.

    Returns:
        dict: Success message and book data if found.

    Raises:
        HTTPException: If the book with the given ID is not found.
    """
    print(f"User details: {token_details}")
    book = await book_service.get_book(book_uid, session)
    if book is not None:
        return {"message": "Book data retrieved successfully", "data": book}
    else:
        raise HTTPException(status_code=404, detail=f"Book with ID '{book_uid}' not found")

# ----------------- Insert Book data -----------------
@book_router.post("/createBook", status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def createBook(
    newbook: BookCreateModel, 
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
) -> dict:
    """
    Create a new book in the database.

    Args:
        newbook (BookCreateModel): Data for creating a new book.
        session (AsyncSession): Database session for querying.
        token_details: User details retrieved from the access token.

    Returns:
        dict: Success message and details of the newly created book.
    """
    user = token_details.get("user")
    if user is None:
        raise HTTPException(status_code=400, detail="User details not found in token")
    user_uid = user['user_uid']
    new_book = await book_service.create_book(newbook, user_uid, session)
    return {"message": "Book created successfully", "data": new_book}

# ----------------- Update Books based on User ID -----------------
@book_router.put("/updatebook/{book_uid}", status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def updateBook(
    book_uid: str, 
    book: UpdateBookModel, 
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
) -> dict:
    """
    Update details of an existing book by its unique ID.

    Args:
        book_uid (str): Unique identifier of the book to update.
        book (UpdateBookModel): Updated book data.
        session (AsyncSession): Database session for querying.
        token_details: User details retrieved from the access token.

    Returns:
        dict: Success message and updated book data.

    Raises:
        HTTPException: If the book with the given ID is not found.
    """
    print(f"User details: {token_details}")
    updated_book = await book_service.update_book(book_uid, book, session)
    if updated_book is not None:
        return {"message": "Book updated successfully", "data": updated_book}
    else:
        raise HTTPException(status_code=404, detail=f"Book with ID '{book_uid}' not found") 

# ----------------- Delete a book based on ID -----------------
@book_router.delete("/delete/{book_uid}", status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def deleteBook(
    book_uid: str, 
    session: AsyncSession = Depends(get_session), 
    token_details: dict = Depends(access_token_bearer)
):
    """
    Delete a book from the database by its unique ID.

    Args:
        book_uid (str): Unique identifier of the book to delete.
        session (AsyncSession): Database session for querying.
        token_details: User details retrieved from the access token.

    Returns:
        JSONResponse: Success message if the book is deleted.

    Raises:
        HTTPException: If the book with the given ID is not found.
    """
    print(f"User details: {token_details}")
    book_to_delete = await book_service.delete_book(book_uid, session)
    print(f"Book to delete: {book_to_delete}")
    if book_to_delete is not None:
        return JSONResponse(status_code=200, content={"message": "Book deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail=f"Book with ID '{book_uid}' not found")
