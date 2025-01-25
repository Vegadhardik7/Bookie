"""
This file handles Redis client setup and operations for managing token blocklists and roles.
"""

# Import aioredis for asynchronous Redis operations
from redis import asyncio as aioredis
from src.config import Config  # Import the configuration settings

# Token expiry time in seconds for the blocklist (1 hour)
JTI_EXPIRY_SECONDS = 3600

# Initialize a Redis client for the token blocklist
redis_token_blocklist = aioredis.StrictRedis(
    host=Config.REDIS_HOST,  # Redis server host (from config)
    port=Config.REDIS_PORT,  # Redis server port (from config)
    db=0  # Use database 0
)

async def add_jti_to_blocklist(jti: str) -> None:
    """
    Adds a JWT ID (JTI) to the Redis blocklist.
    
    Args:
        jti (str): The unique identifier of the JWT token to block.

    This function sets the JTI as a key in Redis with a blank value and 
    an expiration time defined by `JTI_EXPIRY_SECONDS`.
    """
    async with aioredis.from_url(f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}") as redis:
        await redis.set(name=jti, value="", ex=JTI_EXPIRY_SECONDS)

async def token_in_blocklist(jti: str) -> bool:
    """
    Checks if a given JTI exists in the Redis blocklist.
    
    Args:
        jti (str): The unique identifier of the JWT token to check.

    Returns:
        bool: True if the JTI is in the blocklist, False otherwise.
    """
    async with aioredis.from_url(f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}") as redis:
        return await redis.exists(jti) > 0

# Role-Based Access Definitions

"""
1. Admin Role:
    - Responsibilities:
        * Add new users
        * Change user roles
        * Perform CRUD operations on user accounts
        * Submit new books
        * Perform CRUD operations on books and reviews
        * Revoke user access

2. User Role:
    - Responsibilities:
        * CRUD operations on their own book submissions
        * CRUD operations on their own reviews
        * Manage their own account details
"""

