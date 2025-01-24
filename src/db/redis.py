# import aioredis
from redis import asyncio as aioredis
from src.config import Config

JTI_EXPIRY_SECONDS = 3600

# setup redis client object
redis_token_blocklist = aioredis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)

# add our token to the blocklist
async def add_jti_to_blocklist(jti: str) -> None:
    async with aioredis.from_url(f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}") as redis:
        await redis.set(name=jti, value="", ex=JTI_EXPIRY_SECONDS)


# check token exists in our blocklist
async def token_in_blocklist(jti: str) -> bool:
    async with aioredis.from_url(f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}") as redis:
        return await redis.exists(jti) > 0