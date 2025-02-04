import logging  # Log the formation
from fastapi import status  # Importing status codes from FastAPI for use in HTTP responses.
from src.db.models import Review  # Importing the Review model from the database models.
from src.auth.service import UserService  # Importing the UserService class from the authentication service.
from src.books.service import BookService  # Importing the BookService class from the book service.
from fastapi.exceptions import HTTPException  # Importing HTTPException from FastAPI to handle exceptions.
from src.reviews.schemas import ReviewCreateModel  # Importing the ReviewCreateModel schema for review creation data.
from sqlmodel.ext.asyncio.session import AsyncSession  # Importing AsyncSession for asynchronous database sessions.

# Initialize services
book_service = BookService()  # Creating an instance of the BookService class to interact with book-related operations.
user_service = UserService()  # Creating an instance of the UserService class to interact with user-related operations.

# Service class for handling reviews
class ReviewService:
    # Asynchronous method to add a review to a book
    async def add_review_to_book(self, 
                                 user_email: str,  # The email of the user adding the review.
                                 book_uid: str,  # The unique identifier of the book being reviewed.
                                 review_data: ReviewCreateModel,  # The data for the new review, using the ReviewCreateModel schema.
                                 session: AsyncSession):  # The asynchronous database session for database operations.
        try:
            logging.info("#### Starting transaction... ####")
            # async with session.begin():  # Start a transaction block
            logging.info("Transaction started.")
            book = await book_service.get_book(book_uid, session)  # Fetch the book using the book UID and database session.
            user = await user_service.get_user_by_email(user_email, session)  # Fetch the user using the email and database session.

            # Check if book exists
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book Not Found!"  # Corrected the detail message
                )
            
            # Check if user exists
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User Not Found!"  # Corrected the detail message
                )

            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)  # Create a new Review object using the review data.

            new_review.user = user  # Associate the user with the new review.
            new_review.book = book  # Associate the book with the new review.

            session.add(new_review)  # Add the new review to the database session.
            await session.commit()
            await session.refresh(new_review)
            logging.info("New review added to session.")

            logging.info("#### Transaction committed. ####")
            return new_review  # Return the newly created review.
        except Exception as e:  # Handle any exceptions that occur during the process.
            logging.error(f"#### Transaction failed: {e} ####")
            await session.rollback()  # Rollback the transaction in case of error
            logging.exception(f"---------------- LOGGING ---------------- \n {e} \n ----------------")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Oops! Something went wrong...")  # Raise an HTTPException if an error occurs, with a 500 status code and error message.

