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




### Bearer Token Autorization:

![image](https://github.com/user-attachments/assets/ad46ce0e-709a-4f07-8545-0159b2f195fc)
