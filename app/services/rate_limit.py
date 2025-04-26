from typing import Dict, Optional
from datetime import datetime, timedelta
from fastapi import Request, status
from app.schemas.base import BaseResponse
from app.core.logging import log_service_call, get_request_id
from app.repositories.rate_limit import RateLimitRepository


class RateLimitService:
    def __init__(self, repository: RateLimitRepository):
        self.repository = repository
        self.rate_limits: Dict[str, Dict[str, int]] = {}  # customer_id -> {endpoint -> count}

    @log_service_call("RateLimitService")
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
            
            # Get rate limit record
            rate_limit = await self.repository.get_rate_limit(
                customer_id=customer_id,
                endpoint=endpoint,
                request_id=request_id
            )

            if not rate_limit:
                # First request, create new rate limit record
                await self.repository.create_rate_limit(
                    customer_id=customer_id,
                    endpoint=endpoint,
                    request_count=1,
                    window_start=current_time,
                    request_id=request_id
                )
                return BaseResponse.success(
                    detail=True,
                    msg="Rate limit check passed"
                )

            # Check if window has expired
            if current_time - rate_limit.window_start > timedelta(seconds=time_window_seconds):
                # Reset window
                await self.repository.update_rate_limit(
                    customer_id=customer_id,
                    endpoint=endpoint,
                    request_count=1,
                    window_start=current_time,
                    request_id=request_id
                )
                return BaseResponse.success(
                    detail=True,
                    msg="Rate limit check passed"
                )

            # Check if limit exceeded
            if rate_limit.request_count >= max_requests:
                return BaseResponse.error(
                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                    msg=f"Rate limit exceeded. Maximum {max_requests} requests per {time_window_seconds} seconds",
                    detail=False
                )

            # Increment request count
            await self.repository.update_rate_limit(
                customer_id=customer_id,
                endpoint=endpoint,
                request_count=rate_limit.request_count + 1,
                window_start=rate_limit.window_start,
                request_id=request_id
            )

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