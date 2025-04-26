from functools import wraps
from typing import Callable, Optional
from fastapi import Request, Response, status, Depends
from app.services.redis_rate_limit import RedisRateLimitService
from app.core.redis import get_redis_client
from app.core.logging import log_service_call


def rate_limit(
    endpoint: str,
    max_requests: int = 100,
    time_window_seconds: int = 60,
    customer_id_header: str = "X-Customer-ID"
):
    """
    Decorator for rate limiting API endpoints using Redis.
    
    Args:
        endpoint: The endpoint URL to rate limit
        max_requests: Maximum number of requests allowed in the time window
        time_window_seconds: Time window in seconds
        customer_id_header: Header name to get customer ID from
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get request object from args or kwargs
            request = next((arg for arg in args if isinstance(arg, Request)), None)
            if not request:
                request = kwargs.get("request")
            
            if not request:
                raise ValueError("Request object not found in function arguments")

            # Get customer_id from header
            customer_id = request.headers.get(customer_id_header)
            if not customer_id:
                return Response(
                    content="Customer ID is required",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Get Redis client
            redis_client = await get_redis_client()
            
            # Initialize rate limit service
            rate_limit_service = RedisRateLimitService(redis_client)

            # Check rate limit
            rate_limit_response = await rate_limit_service.check_rate_limit(
                customer_id=customer_id,
                endpoint=endpoint,
                max_requests=max_requests,
                time_window_seconds=time_window_seconds,
                request=request
            )

            if not rate_limit_response.detail:
                return Response(
                    content=rate_limit_response.msg,
                    status_code=rate_limit_response.status
                )

            # If rate limit check passes, proceed with the request
            return await func(*args, **kwargs)

        return wrapper
    return decorator


def rate_limit_dependency(endpoint: str, max_requests: int = 100, time_window_seconds: int = 60):
    return rate_limit(endpoint, max_requests, time_window_seconds)
