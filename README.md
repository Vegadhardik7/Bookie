# Bookie Detailed Notes

## Project Folder & File Structure

```
Bookie/
├── migrations/                  # Directory for database migration files
│   └── env.py                   # Configuration for Alembic migrations
├── src/                         # Source code directory
│   ├── auth/                    # Directory for authentication-related code
│   │   ├── dependencies.py      # Custom dependencies for authentication
│   │   ├── routers.py           # Authentication-related routes
│   │   ├── schemas.py           # Pydantic models for authentication
│   │   ├── service.py           # Business logic for authentication
│   │   └── utils.py             # Utility functions for authentication
│   ├── books/                   # Directory for book-related code
│   │   ├── routes.py            # Book-related routes
│   │   ├── schemas.py           # Pydantic models for books
│   │   └── service.py           # Business logic for books
│   ├── reviews/                 # Directory for review-related code
│   │   ├── routes.py            # Review-related routes
│   │   ├── schemas.py           # Pydantic models for reviews
│   │   └── service.py           # Business logic for reviews
│   ├── db/                      # Directory for database-related code
│   │   ├── main.py              # Database connection and session management
│   │   ├── models.py            # SQLAlchemy models for the database
│   │   └── redis.py             # Redis client setup and operations
│   ├── errors.py                # Custom error classes for the application
│   └── __init__.py              # FastAPI application setup and router inclusion
└── README.md                    # Project documentation file
```

## Routes and API's

### 1. FastAPI Application Initialization (__init__.py)
**File:** __init__.py

**Description:** Sets up the FastAPI application, includes routers for books, reviews, and authentication, and manages the application's lifespan.
```
FastAPI Application Initialization
|
|-- /api/v1/books (Book Routes)
|-- /api/v1/reviews (Review Routes)
|-- /api/v1/auths (Auth Routes)
```

### 2. Book Routes (books/routes.py)
**File:** routes.py

**Description:** Defines endpoints for book-related operations.
```
Book Routes
|
|-- GET /api/v1/books/ (List all books)
|   |-- Triggers: `getAllBooks`
|   |-- Functionality: Retrieves all books from the database.
|
|-- GET /api/v1/books/user/{user_uid} (List books by user)
|   |-- Triggers: `get_user_book_submissions`
|   |-- Functionality: Retrieves all books created by a specific user.
|
|-- GET /api/v1/books/{book_uid} (Get book by ID)
|   |-- Triggers: `getBook`
|   |-- Functionality: Retrieves details of a specific book by its unique ID.
|
|-- POST /api/v1/books/createBook (Create a new book)
|   |-- Triggers: `createBook`
|   |-- Functionality: Creates a new book in the database.
|
|-- PATCH /api/v1/books/updatebook/{book_uid} (Update book by ID)
|   |-- Triggers: `updateBook`
|   |-- Functionality: Updates details of an existing book by its unique ID.
|
|-- DELETE /api/v1/books/delete/{book_uid} (Delete book by ID)
|   |-- Triggers: `deleteBook`
|   |-- Functionality: Deletes a book from the database by its unique ID.
```

### 3. Review Routes (reviews/routes.py)
**File:** routes.py

**Description:** Defines endpoints for review-related operations.
```
Review Routes
|
|-- POST /api/v1/reviews/book/{book_uid} (Add review to book)
|   |-- Triggers: `add_review_to_books`
|   |-- Functionality: Adds a review to a book.
```

### 4. Auth Routes (auth/routers.py)
**File:** routers.py

**Description:** Defines endpoints for authentication-related operations.
```
Auth Routes
|
|-- POST /api/v1/auths/signup (User signup)
|   |-- Triggers: `create_user_account`
|   |-- Functionality: Creates a new user account.
|
|-- POST /api/v1/auths/login (User login)
|   |-- Triggers: `login_user`
|   |-- Functionality: Authenticates the user and provides access and refresh tokens.
|
|-- GET /api/v1/auths/refresh_token (Refresh token)
|   |-- Triggers: `get_new_access_token`
|   |-- Functionality: Generates a new access token using a valid refresh token.
|
|-- GET /api/v1/auths/me (Get current user)
|   |-- Triggers: `get_me`
|   |-- Functionality: Retrieves details of the currently authenticated user.
|
|-- GET /api/v1/auths/logout (User logout)
|   |-- Triggers: `revoke_token`
|   |-- Functionality: Revokes the user's access token by adding it to the blocklist.
```

### -> Book Routes

### GET /api/v1/books/
- **Triggers:** getAllBooks
- **Functionality:** Retrieves all books from the database.
- **Flow:**
  - Calls `getAllBooks` function in `books/routes.py`.
  - Uses `BookService` to fetch all books from the database.

### GET /api/v1/books/user/{user_uid}
- **Triggers:** get_user_book_submissions
- **Functionality:** Retrieves all books created by a specific user.
- **Flow:**
  - Calls `get_user_book_submissions` function in `books/routes.py`.
  - Uses `BookService` to fetch books by user UID.

### GET /api/v1/books/{book_uid}
- **Triggers:** getBook
- **Functionality:** Retrieves details of a specific book by its unique ID.
- **Flow:**
  - Calls `getBook` function in `books/routes.py`.
  - Uses `BookService` to fetch book details by book UID.

### POST /api/v1/books/createBook
- **Triggers:** createBook
- **Functionality:** Creates a new book in the database.
- **Flow:**
  - Calls `createBook` function in `books/routes.py`.
  - Uses `BookService` to create a new book with provided data.

### PATCH /api/v1/books/updatebook/{book_uid}
- **Triggers:** updateBook
- **Functionality:** Updates details of an existing book by its unique ID.
- **Flow:**
  - Calls `updateBook` function in `books/routes.py`.
  - Uses `BookService` to update book details by book UID.

### DELETE /api/v1/books/delete/{book_uid}
- **Triggers:** deleteBook
- **Functionality:** Deletes a book from the database by its unique ID.
- **Flow:**
  - Calls `deleteBook` function in `books/routes.py`.
  - Uses `BookService` to delete book by book UID.

### -> Review Routes

### POST /api/v1/reviews/book/{book_uid}
- **Triggers:** add_review_to_books
- **Functionality:** Adds a review to a book.
- **Flow:**
  - Calls `add_review_to_books` function in `reviews/routes.py`.
  - Uses `ReviewService` to add a review to the specified book.

### -> Auth Routes

### POST /api/v1/auths/signup
- **Triggers:** create_user_account
- **Functionality:** Creates a new user account.
- **Flow:**
  - Calls `create_user_account` function in `auth/routers.py`.
  - Uses `UserService` to create a new user with provided data.

### POST /api/v1/auths/login
- **Triggers:** login_user
- **Functionality:** Authenticates the user and provides access and refresh tokens.
- **Flow:**
  - Calls `login_user` function in `auth/routers.py`.
  - Uses `UserService` to authenticate the user and generate tokens.

### GET /api/v1/auths/refresh_token
- **Triggers:** get_new_access_token
- **Functionality:** Generates a new access token using a valid refresh token.
- **Flow:**
  - Calls `get_new_access_token` function in `auth/routers.py`.
  - Uses `create_access_token` utility to generate a new access token.

### GET /api/v1/auths/me
- **Triggers:** get_me
- **Functionality:** Retrieves details of the currently authenticated user.
- **Flow:**
  - Calls `get_me` function in `auth/routers.py`.
  - Uses `get_current_user` dependency to fetch current user details.

### GET /api/v1/auths/logout
- **Triggers:** revoke_token
- **Functionality:** Revokes the user's access token by adding it to the blocklist.
- **Flow:**
  - Calls `revoke_token` function in `auth/routers.py`.
  - Uses `add_jti_to_blocklist` utility to revoke the token.

## Starting Point

## FastAPI Application Initialization (__init__.py)
**File:** __init__.py  

**Description:** This is where the FastAPI application is created and configured. It includes routers for different parts of the application (books, reviews, and authentication) and manages the application's lifespan.  

**Key Points:**
- Understand how the FastAPI application is initialized.
- Learn how routers are included in the application.
- Familiarize yourself with the lifespan event for initializing and closing the database connection.

## Flow Progression

### Routers and Endpoints

#### Books Router (books/routes.py)
**File:** routes.py  

**Description:** Defines endpoints for book-related operations.  

**Key Points:**
- Study each endpoint and its corresponding function.
- Understand how each endpoint interacts with the `BookService` to perform CRUD operations on books.

#### Reviews Router (reviews/routes.py)
**File:** routes.py  

**Description:** Defines endpoints for review-related operations.  

**Key Points:**
- Study the endpoint for adding reviews to books.
- Understand how the endpoint interacts with the `ReviewService` to add reviews.

#### Auth Router (auth/routers.py)
**File:** routers.py  

**Description:** Defines endpoints for authentication-related operations.  

**Key Points:**
- Study each endpoint and its corresponding function.
- Understand how each endpoint interacts with the `UserService` to handle user authentication and management.

### Service Classes

#### Book Service (books/service.py)
**File:** service.py  

**Description:** Contains the business logic for book-related operations.  

**Key Points:**
- Study the methods in the `BookService` class.
- Understand how each method interacts with the database to perform CRUD operations on books.

#### Review Service (reviews/service.py)
**File:** service.py  

**Description:** Contains the business logic for review-related operations.  

**Key Points:**
- Study the method for adding reviews to books.
- Understand how the method interacts with the database to add reviews.

#### Auth Service (auth/service.py)
**File:** service.py  

**Description:** Contains the business logic for authentication-related operations.  

**Key Points:**
- Study the methods in the `UserService` class.
- Understand how each method interacts with the database to handle user authentication and management.

### Schemas

#### Book Schemas (books/schemas.py)
**File:** schemas.py  

**Description:** Defines Pydantic models for book-related data.  

**Key Points:**
- Study the Pydantic models and their fields.
- Understand how these models are used for request validation and response formatting.

#### Review Schemas (reviews/schemas.py)
**File:** schemas.py  

**Description:** Defines Pydantic models for review-related data.  

**Key Points:**
- Study the Pydantic models and their fields.
- Understand how these models are used for request validation and response formatting.

#### Auth Schemas (auth/schemas.py)
**File:** schemas.py  

**Description:** Defines Pydantic models for authentication-related data.  

**Key Points:**
- Study the Pydantic models and their fields.
- Understand how these models are used for request validation and response formatting.

### Database Models and Configuration

#### Database Models (db/models.py)
**File:** models.py  

**Description:** Defines SQLAlchemy models for the database.  

**Key Points:**
- Study the models for User, Book, and Review.
- Understand how these models represent the database tables and their relationships.

#### Database Configuration (db/main.py)
**File:** main.py  

**Description:** Manages the database connection and session.  

**Key Points:**
- Understand how the database engine and session are configured.
- Learn how the database is initialized.

#### Redis Configuration (db/redis.py)
**File:** redis.py  

**Description:** Handles Redis client setup and operations for managing token blocklists and roles.  

**Key Points:**
- Study the functions for adding and checking tokens in the blocklist.
- Understand how Redis is used for token management.

### Custom Errors

#### Custom Errors (errors.py)
**File:** errors.py  

**Description:** Defines custom error classes for the application.  

**Key Points:**
- Study the custom error classes.
- Understand how these errors are used to handle specific error cases.

## Study Flow
1. Start with `__init__.py`: Understand how the FastAPI application is initialized and how routers are included.
2. Move to Routers: Study the routes in `books/routes.py`, `reviews/routes.py`, and `auth/routers.py`. Understand the endpoints and their functionalities.
3. Explore Service Classes: Dive into the service classes in `books/service.py`, `reviews/service.py`, and `auth/service.py`. Understand the business logic for each operation.
4. Review Schemas: Study the Pydantic models in `books/schemas.py`, `reviews/schemas.py`, and `auth/schemas.py`. Understand how data validation and formatting are handled.
5. Examine Database Models and Configuration: Look into `db/models.py`, `db/main.py`, and `db/redis.py`. Understand how the database and Redis are configured and managed.
6. Understand Custom Errors: Review `errors.py` to understand how custom errors are defined and used.

# ERD Diagram Representation (ASCII)
```
+-----------------+     +-----------------+     +-----------------+
|     Users      |     |     Books       |     |    Reviews      |
+-----------------+     +-----------------+     +-----------------+
| user_uid (PK)  |<---+| book_uid (PK)   |     | review_uid (PK) |
| username       |     | title           |     | book_uid (FK)   |
| email          |     | author          |     | user_uid (FK)   |
| password_hash  |     | user_uid (FK)   |     | rating          |
| created_at     |     | created_at      |     | review_text     |
+-----------------+     +-----------------+     | created_at      |
                                                +-----------------+
```
## Users (users)
- **user_uid** (Primary Key, UUID)
- **username** (Unique)
- **email** (Unique)
- **password_hash**
- **created_at**
- **updated_at**

### Relationships:
- One user can create multiple books (1:N with books).
- One user can write multiple reviews (1:N with reviews).

## Books (books)
- **book_uid** (Primary Key, UUID)
- **title**
- **author**
- **description**
- **user_uid** (Foreign Key → users.user_uid) (creator of the book)
- **created_at**
- **updated_at**

### Relationships:
- One book can have multiple reviews (1:N with reviews).
- Each book is submitted by one user (N:1 with users).

## Reviews (reviews)
- **review_uid** (Primary Key, UUID)
- **book_uid** (Foreign Key → books.book_uid)
- **user_uid** (Foreign Key → users.user_uid)
- **rating** (Integer)
- **review_text**
- **created_at**
- **updated_at**

### Relationships:
- Each review is written by one user (N:1 with users).
- Each review is for one book (N:1 with books).

## Auth Tokens (Optional, if stored in DB) (tokens)
- **token_id** (Primary Key)
- **user_uid** (Foreign Key → users.user_uid)
- **refresh_token**
- **expires_at**


### Bearer Token Autorization:

![image](https://github.com/user-attachments/assets/ad46ce0e-709a-4f07-8545-0159b2f195fc)
