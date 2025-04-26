from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.rate_limit import RateLimit
from app.core.logging import log_service_call


class RateLimitRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @log_service_call("RateLimitRepository")
    async def get_rate_limit(self, customer_id: str, endpoint: str, request_id: str) -> RateLimit:
        result = await self.db.execute(
            select(RateLimit)
            .where(
                RateLimit.customer_id == customer_id,
                RateLimit.endpoint == endpoint
            )
        )
        return result.scalar_one_or_none()

    @log_service_call("RateLimitRepository")
    async def create_rate_limit(
        self,
        customer_id: str,
        endpoint: str,
        request_count: int,
        window_start: datetime,
        request_id: str
    ) -> RateLimit:
        rate_limit = RateLimit(
            customer_id=customer_id,
            endpoint=endpoint,
            request_count=request_count,
            window_start=window_start
        )
        self.db.add(rate_limit)
        await self.db.commit()
        await self.db.refresh(rate_limit)
        return rate_limit

    @log_service_call("RateLimitRepository")
    async def update_rate_limit(
        self,
        customer_id: str,
        endpoint: str,
        request_count: int,
        window_start: datetime,
        request_id: str
    ) -> RateLimit:
        rate_limit = await self.get_rate_limit(customer_id, endpoint, request_id)
        if not rate_limit:
            return None

        rate_limit.request_count = request_count
        rate_limit.window_start = window_start

        await self.db.commit()
        await self.db.refresh(rate_limit)
        return rate_limit 