from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user import UserService
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, Token, TokenData
from app.core.security import get_current_user
from app.core.logging import log_service_call
from app.core.rate_limit import rate_limit


router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@log_service_call("UserAPI")
async def create_user(
    user: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository(db))
    return await service.create_user(user, request)


@router.get("/me", response_model=UserResponse)
@log_service_call("UserAPI")
@rate_limit("/me")
async def read_users_me(
    request: Request,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository(db))
    return await service.get_user_by_username(current_user.username, request)


@router.put("/me", response_model=UserResponse)
@log_service_call("UserAPI")
@rate_limit("/me")
async def update_user_me(
    user_update: UserUpdate,
    request: Request,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository(db))
    return await service.update_user_by_username(current_user.username, user_update, request)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
@log_service_call("UserAPI")
@rate_limit("/me")
async def delete_user_me(
    request: Request,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(UserRepository(db))
    return await service.delete_user_by_username(current_user.username, request)


# Apply custom rate limit (50 requests per 30 seconds)
@router.get("/endpoint2")
@rate_limit("/endpoint2", max_requests=50, time_window_seconds=30)
async def endpoint2(request: Request):
    return {"message": "Hello World"}

# Apply custom rate limit with different customer ID header
@router.get("/endpoint3")
@rate_limit("/endpoint3", max_requests=200, time_window_seconds=60, customer_id_header="X-API-Key")
async def endpoint3(request: Request):
    return {"message": "Hello World"} 