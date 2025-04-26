import redis.asyncio as redis
from app.core.config import settings


async def get_redis_client() -> redis.Redis:
    """
    Get Redis client instance.
    """
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=False
    ) 