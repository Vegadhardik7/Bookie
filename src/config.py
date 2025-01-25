"""
This file is responsible for loading and managing environment variables using Pydantic and dotenv.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
from pydantic import ValidationError

# Load environment variables from the .env file into the environment
load_dotenv()
print("Loaded DATABASE_URL from dotenv:", os.getenv("DATABASE_URL"))
print(os.environ.get('DATABASE_URL'))

class Settings(BaseSettings):
    """
    This class defines the configuration settings for the application.
    It uses Pydantic to validate and load environment variables.
    """

    DATABASE_URL: str  # The database connection URL (required).
    JWT_SECRET: str  # The secret key for JWT token generation (required).
    JWT_ALGORITHM: str  # The algorithm used for JWT (e.g., "HS256") (required).
    REDIS_HOST: str = "localhost"  # Redis server hostname (optional, defaults to "localhost").
    REDIS_PORT: int = 6379  # Redis server port (optional, defaults to 6379).

    # Pydantic-specific configuration
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")  
    # `env_file` specifies the file to load variables from.
    # `extra="ignore"` ensures unexpected fields in the environment are ignored.

# Try to load the settings and handle validation errors
try:
    Config = Settings()  # type: ignore # Create an instance of the Settings class to load variables.
except ValidationError as e:
    # Handle cases where required environment variables are missing or invalid
    print(f"Error loading settings: {e}")
    exit(1)  # Exit the application if configuration fails.

# Debug prints to confirm the settings are loaded correctly
print(Config.DATABASE_URL)