from typing import Optional
from datetime import datetime, timedelta
from fastapi import Request, status
import redis.asyncio as redis
from app.schemas.base import BaseResponse
from app.core.logging import log_service_call, get_request_id


class RedisRateLimitService:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    @log_service_call("RedisRateLimitService")
    async def check_rate_limit(
        self,
        customer_id: str,
        endpoint: str,
        max_requests: int,
        time_window_seconds: int,
        request: Request
    ) -> BaseResponse[bool]:
        try:
            request_id = get_request_id(request)
            current_time = datetime.utcnow()
            
            # Create a unique key for this customer and endpoint
            key = f"rate_limit:{customer_id}:{endpoint}"
            
            # Get current count and window start from Redis
            pipe = self.redis.pipeline()
            pipe.get(key)
            pipe.get(f"{key}:window_start")
            count, window_start_str = await pipe.execute()
            
            count = int(count) if count else 0
            window_start = datetime.fromisoformat(window_start_str.decode()) if window_start_str else current_time
            
            # Check if window has expired
            if current_time - window_start > timedelta(seconds=time_window_seconds):
                # Reset window
                pipe = self.redis.pipeline()
                pipe.set(key, 1)
                pipe.set(f"{key}:window_start", current_time.isoformat())
                pipe.expire(key, time_window_seconds)
                pipe.expire(f"{key}:window_start", time_window_seconds)
                await pipe.execute()
                return BaseResponse.success(
                    detail=True,
                    msg="Rate limit check passed"
                )

            # Check if limit exceeded
            if count >= max_requests:
                return BaseResponse.error(
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                    msg=f"Rate limit exceeded. Maximum {max_requests} requests per {time_window_seconds} seconds",
                    detail=False
                )

            # Increment count
            pipe = self.redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, time_window_seconds)
            pipe.expire(f"{key}:window_start", time_window_seconds)
            await pipe.execute()

            return BaseResponse.success(
                detail=True,
                msg="Rate limit check passed"
            )

        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to check rate limit",
                detail=str(e)
            ) 