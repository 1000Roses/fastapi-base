from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.sql_logging import setup_sql_logging, set_request_id
from fastapi import Request
from loguru import logger

SQLALCHEMY_DATABASE_URL = (
    f"mysql+aiomysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DATABASE}"
)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    echo=False,  # Disable SQLAlchemy's built-in logging
)

logger.info("Database engine initialized with pool_size={}, max_overflow={}", 
           settings.DB_POOL_SIZE, settings.DB_MAX_OVERFLOW)

# Setup SQL logging with request_id context
setup_sql_logging(engine)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db(request: Request = None):
    async with AsyncSessionLocal() as session:
        try:
            if request and hasattr(request.state, 'request_id'):
                set_request_id(request.state.request_id)
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 