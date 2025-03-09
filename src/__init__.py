from fastapi import FastAPI  # Import FastAPI for creating the application instance.
from src.books.routes import book_router  # Import the book router for book-related routes.
from src.reviews.routes import review_router  # Import the review router for review-related routes.
from src.auth.routers import auth_router  # Import the auth router for authentication-related routes.
from contextlib import asynccontextmanager  # Import asynccontextmanager for managing the application's lifespan.

"""
Created lifespan event, which helps to initialize the database connection when the 
application starts and close the connection when the application stops.
"""

@asynccontextmanager
async def life_span(app: FastAPI):
    """
    Lifespan event to initialize the database connection when the application starts
    and close the connection when the application stops.
    """
    print("Starting the application...")
    try:
        from src.db.main import init_db  # Import the init_db function for initializing the database.
        await init_db()  # Initialize the database (await the coroutine function).
        yield  # Yield control back to the application.
    finally:
        print("Stopped the application")

version = "v1"  # Define the API version.

# Create the FastAPI application instance with version, title, and description.
app = FastAPI(version=version, title="MyBookie", description="REST API for a book review app service")

# Include the book router with a prefix and tag.
app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
# Include the auth router with a prefix and tag.
app.include_router(auth_router, prefix=f"/api/{version}/auths", tags=['auth'])
# Include the review router with a prefix and tag.
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])