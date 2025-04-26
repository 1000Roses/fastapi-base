from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base


class RateLimit(Base):
    __tablename__ = "rate_limits"
    __table_args__ = (
        UniqueConstraint('customer_id', 'endpoint', name='uix_customer_endpoint'),
    )

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), index=True, nullable=False)
    endpoint = Column(String(100), nullable=False)
    request_count = Column(Integer, default=0, nullable=False)
    window_start = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 