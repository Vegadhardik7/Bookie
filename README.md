# Project Folder & File Structure

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

### Bearer Token Autorization:

![image](https://github.com/user-attachments/assets/ad46ce0e-709a-4f07-8545-0159b2f195fc)
