# from src.books.book_data import books
from fastapi import APIRouter, status, Depends
from src.books.schemas import BookModel, BookCreateModel, UpdateBookModel
from src.books.models import BookModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.books.models import BookModel
from src.books.service import BookService
from src.db.main import get_session
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

book_router = APIRouter()
book_service = BookService()

# ----------------- List all the books ----------------- 
@book_router.get("/", response_model=List[BookModel])
async def getAllBooks(session: AsyncSession = Depends(get_session)):
    return await book_service.get_all_books(session)

# ----------------- List the book data by id ----------------- 
@book_router.get("/{book_uid}", status_code=status.HTTP_200_OK)
async def getBook(book_uid: str,session: AsyncSession = Depends(get_session))->dict:
    book = await book_service.get_book(book_uid,session)
    if book is not None:
        return {"message": "Book data retrieved successfully", "data": book}
    else:
        raise HTTPException(status_code=404, detail=f"User with ID '{book_uid}' not found")

# ----------------- Insert Book data ----------------- 
@book_router.post("/createBook", status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def createBook(newbook: BookCreateModel, session: AsyncSession = Depends(get_session))-> dict:
    new_book = await book_service.create_book(newbook,session)
    
    return {"message": "Book created successfully", "data": new_book}

# ----------------- Update Books based on User ID ----------------- 
@book_router.put("/updatebook/{book_uid}", status_code=status.HTTP_200_OK)
async def updateBook(book_uid: str, book: UpdateBookModel, session: AsyncSession = Depends(get_session)) -> dict:
    updated_book = await book_service.update_book(book_uid, book, session)
    
    if updated_book is not None:
        return {"message": "Book updated successfully", "data": updated_book}
    else:
        # If user is not found, raise a 404 error
        raise HTTPException(status_code=404, detail=f"User with ID '{book_uid}' not found") 

# ----------------- delete a user based on id ----------------- 
@book_router.delete("/delete/{book_uid}", status_code=status.HTTP_200_OK)
async def deleteBook(book_uid: str, session: AsyncSession = Depends(get_session)):

    book_to_delete = await book_service.delete_book(book_uid,session)
    print(f"Book to delete: {book_to_delete}")
    if book_to_delete is not None:
        return JSONResponse(status_code=200, content={"message": "Book deleted successfully"})
    else:
        # If no user is found with the given ID, raise a 404 error
        raise HTTPException(status_code=404, detail=f"User with ID '{book_uid}' not found")