from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routers import auth_router
from contextlib import asynccontextmanager

"""
Created lifespan event, which helps to initialize the database connection when the 
application starts and close the connection when the application stops.
"""

@asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting the application...")
    try:
        from src.db.main import init_db
        await init_db() # this is a coroutine function so we need to await it
        yield
    finally:
        print("Stopped the application")


version = "v1"

app = FastAPI(version=version, title="MyBookie", description="REST API for a book review app service")

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auths", tags=['auth'])