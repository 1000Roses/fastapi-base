from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from app.services.rate_limit import RateLimitService
from app.repositories.rate_limit import RateLimitRepository
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.rate_limit import rate_limit


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        max_requests: int = 100,
        time_window_seconds: int = 60
    ):
        super().__init__(app)
        self.max_requests = max_requests
        self.time_window_seconds = time_window_seconds

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip rate limiting for certain paths
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        # Get customer_id from request (you might need to adjust this based on your auth system)
        customer_id = request.headers.get("X-Customer-ID")
        if not customer_id:
            return Response(
                content="Customer ID is required",
                status_code=400
            )

        # Get database session
        db: AsyncSession = next(get_db())
        
        # Initialize services
        rate_limit_repo = RateLimitRepository(db)
        rate_limit_service = RateLimitService(rate_limit_repo)

        # Check rate limit
        rate_limit_response = await rate_limit_service.check_rate_limit(
            customer_id=customer_id,
            endpoint=request.url.path,
            max_requests=self.max_requests,
            time_window_seconds=self.time_window_seconds,
            request=request
        )

        if not rate_limit_response.detail:
            return Response(
                content=rate_limit_response.msg,
                status_code=rate_limit_response.status
            )

        # If rate limit check passes, proceed with the request
        response = await call_next(request)
        return response 