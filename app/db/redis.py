import json
from typing import Any, List, Optional, Union
import redis.asyncio as redis
from app.core.config import settings


class RedisClient:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
        )
        self.redis = redis.Redis(connection_pool=self.pool)

    async def get(self, key: str) -> Optional[str]:
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int = None) -> bool:
        return await self.redis.set(key, value, ex=expire)

    async def delete(self, key: str) -> bool:
        return bool(await self.redis.delete(key))

    async def get_json(self, key: str) -> Optional[dict]:
        data = await self.get(key)
        return json.loads(data) if data else None

    async def set_json(self, key: str, value: dict, expire: int = None) -> bool:
        return await self.set(key, json.dumps(value), expire)

    async def lpush(self, key: str, *values: Any) -> int:
        return await self.redis.lpush(key, *values)

    async def rpush(self, key: str, *values: Any) -> int:
        return await self.redis.rpush(key, *values)

    async def lrange(self, key: str, start: int = 0, end: int = -1) -> List[str]:
        return await self.redis.lrange(key, start, end)

    async def lpop(self, key: str) -> Optional[str]:
        return await self.redis.lpop(key)

    async def rpop(self, key: str) -> Optional[str]:
        return await self.redis.rpop(key)

    async def close(self):
        await self.redis.close()


redis_client = RedisClient() 