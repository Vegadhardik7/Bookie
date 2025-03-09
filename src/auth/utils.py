"""
This file defines utility functions for the authentication module.
It includes functions for password hashing and verification, as well as functions for creating and decoding JWT tokens.
These utilities are used throughout the authentication module to handle common tasks related to security and token management.
"""

import jwt  # Import the jwt module for handling JSON Web Tokens.
import uuid  # Import the uuid module for generating unique identifiers.
import logging  # Import the logging module for logging errors and information.
from src.config import Config  # Import the Config class for accessing configuration settings.
from datetime import datetime, timedelta  # Import datetime and timedelta for handling date and time operations.
from typing import Optional  # Import Optional for optional type annotations.
from passlib.context import CryptContext  # Import CryptContext for password hashing.

password_context = CryptContext(schemes=["bcrypt"])  # Define the password hashing context using bcrypt.
ACCESS_TOKEN_EXPIRE_MINUTES = 3600  # Define the expiration time for access tokens in minutes.

def generated_pswd_hash(password: str) -> str:
    """
    Hash the given password using bcrypt.
    Args:
        password: The plain text password to hash.
    Returns:
        The hashed password.
    """
    hash = password_context.hash(password)  # Hash the password.
    return hash  # Return the hashed password.

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify that the plain text password matches the hashed password.
    Args:
        plain_password: The plain text password.
        hashed_password: The hashed password.
    Returns:
        True if the password matches the hash, otherwise False.
    """
    return password_context.verify(plain_password, hashed_password)  # Verify the password.

def create_access_token(user_data: dict, expiry: Optional[timedelta] = None, refresh: bool = False) -> str:
    """
    Create a new access token with the given user data and expiration time.
    Args:
        user_data: The user data to include in the token.
        expiry: The expiration time for the token (optional).
        refresh: Whether the token is a refresh token (default is False).
    Returns:
        The encoded JWT token.
    """
    payload = {}  # Initialize the payload dictionary.
    payload['user'] = user_data  # Add the user data to the payload.
    expiry_time = str(datetime.now() + (expiry if expiry else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)))  # Calculate the expiration time.
    payload['expire'] = expiry_time  # Add the expiration time to the payload.
    payload['jti'] = str(uuid.uuid4())  # Generate a unique identifier for the token.
    payload['refresh'] = refresh  # Add the refresh flag to the payload.
    encoded_jwt = jwt.encode(payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)  # Encode the JWT token.
    return encoded_jwt  # Return the encoded token.

def decode_access_token(token: str) -> dict:
    """
    Decode the given access token and return the token data.
    Args:
        token: The JWT token to decode.
    Returns:
        The decoded token data.
    """
    try:
        token_data = jwt.decode(jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])  # Decode the token.
        return token_data  # Return the token data.
    except jwt.PyJWTError as e:
        logging.error(f"Error decoding token: {e}")  # Log the error if decoding fails.
        return {}  # Return an empty dictionary if decoding fails.