"""
This file is reponsible to read our env variables
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
from pydantic import ValidationError

# Load environment variables from .env file
load_dotenv()
print("Loaded DATABASE_URL from dotenv:", os.getenv("DATABASE_URL"))
print(os.environ.get('DATABASE_URL'))

class Settings(BaseSettings):
    DATABASE_URL: str 
    JWT_SECRET: str 
    JWT_ALGORITHM: str 
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

try:
    Config = Settings() # type: ignore
except ValidationError as e:
    print(f"Error loading settings: {e}") 
    exit(1) 

print(Config.DATABASE_URL)