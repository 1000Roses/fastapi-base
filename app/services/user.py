from datetime import timedelta
from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash, verify_password, create_access_token
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse, Token
from app.schemas.base import BaseResponse
from app.core.logging import log_service_call, get_request_id
import uuid


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        # self.logger = logging.getLogger(__name__)

    @log_service_call("UserService")
    async def create_user(self, user: UserCreate, request_id: str) -> BaseResponse[UserResponse]:
        try:
            print("request_id 123: ", request_id)
            if await self.repository.get_by_username(user.username, request_id):
                return BaseResponse.error(
                    status=status.HTTP_400_BAD_REQUEST,
                    msg="Username already registered"
                )

            if await self.repository.get_by_email(user.email, request_id):
                return BaseResponse.error(
                    status=status.HTTP_400_BAD_REQUEST,
                    msg="Email already registered"
                )

            hashed_password = get_password_hash(user.password)
            await self.repository.create(user, hashed_password, request_id)
            return BaseResponse.success(
                detail=UserResponse.model_validate(user),
                msg="User created successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to create user",
                detail=str(e)
            )

    @log_service_call("UserService")
    async def authenticate_user(self, username: str, password: str, request: Request) -> BaseResponse[UserResponse]:
        try:
            request_id = get_request_id(request)
            user = await self.repository.get_by_username(username, request_id)
            if not user:
                return BaseResponse.error(
                    status=status.HTTP_401_UNAUTHORIZED,
                    msg="Invalid username or password"
                )

            if not verify_password(password, user.hashed_password):
                return BaseResponse.error(
                    status=status.HTTP_401_UNAUTHORIZED,
                    msg="Invalid username or password"
                )

            return BaseResponse.success(
                detail=UserResponse.model_validate(user),
                msg="Authentication successful"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Authentication failed",
                detail=str(e)
            )

    @log_service_call("UserService")
    async def get_user(self, user_id: int, request: Request) -> BaseResponse[UserResponse]:
        try:
            request_id = get_request_id(request)
            user = await self.repository.get_by_id(user_id, request_id)
            if not user:
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="User not found"
                )

            return BaseResponse.success(
                detail=UserResponse.model_validate(user),
                msg="User retrieved successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to retrieve user",
                detail=str(e)
            )

    @log_service_call("UserService")
    async def update_user(self, user_id: int, user_update: UserUpdate, request: Request) -> BaseResponse[UserResponse]:
        try:
            request_id = get_request_id(request)
            user = await self.repository.get_by_id(user_id, request_id)
            if not user:
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="User not found"
                )

            if user_update.username and user_update.username != user.username:
                if await self.repository.get_by_username(user_update.username, request_id):
                    return BaseResponse.error(
                        status=status.HTTP_400_BAD_REQUEST,
                        msg="Username already taken"
                    )

            if user_update.email and user_update.email != user.email:
                if await self.repository.get_by_email(user_update.email, request_id):
                    return BaseResponse.error(
                        status=status.HTTP_400_BAD_REQUEST,
                        msg="Email already registered"
                    )

            if user_update.password:
                user_update.password = get_password_hash(user_update.password)

            updated_user = await self.repository.update(user_id, user_update, request_id)
            return BaseResponse.success(
                detail=UserResponse.model_validate(updated_user),
                msg="User updated successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to update user",
                detail=str(e)
            )

    @log_service_call("UserService")
    async def delete_user(self, user_id: int, request: Request) -> BaseResponse[None]:
        try:
            request_id = get_request_id(request)
            user = await self.repository.get_by_id(user_id, request_id)
            if not user:
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="User not found"
                )

            await self.repository.delete(user_id, request_id)
            return BaseResponse.success(
                msg="User deleted successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to delete user",
                detail=str(e)
            )

    @log_service_call("UserService")
    async def create_access_token(self, username: str, request: Request) -> BaseResponse[Token]:
        try:
            request_id = get_request_id(request)
            access_token = create_access_token(data={"sub": username})
            return BaseResponse.success(
                detail=Token(access_token=access_token, token_type="bearer"),
                msg="Token created successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to create token",
                detail=str(e)
            )

    @log_service_call("UserService")
    async def update_user_by_username(self, username: str, user_update: UserUpdate, request: Request) -> BaseResponse[UserResponse]:
        try:
            request_id = get_request_id(request)
            user = await self.repository.get_by_username(username, request_id)
            if not user:
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="User not found"
                )

            if user_update.username and user_update.username != user.username:
                if await self.repository.get_by_username(user_update.username, request_id):
                    return BaseResponse.error(
                        status=status.HTTP_400_BAD_REQUEST,
                        msg="Username already taken"
                    )

            if user_update.email and user_update.email != user.email:
                if await self.repository.get_by_email(user_update.email, request_id):
                    return BaseResponse.error(
                        status=status.HTTP_400_BAD_REQUEST,
                        msg="Email already registered"
                    )

            if user_update.password:
                user_update.password = get_password_hash(user_update.password)

            updated_user = await self.repository.update(user.id, user_update, request_id)
            return BaseResponse.success(
                detail=UserResponse.model_validate(updated_user),
                msg="User updated successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to update user",
                detail=str(e)
            )

    @log_service_call("UserService")
    async def delete_user_by_username(self, username: str, request: Request) -> BaseResponse[None]:
        try:
            request_id = get_request_id(request)
            user = await self.repository.get_by_username(username, request_id)
            if not user:
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="User not found"
                )

            await self.repository.delete(user.id, request_id)
            return BaseResponse.success(
                msg="User deleted successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to delete user",
                detail=str(e)
            )

    @log_service_call("UserService")
    async def get_user_by_username(self, username: str, request: Request) -> BaseResponse[UserResponse]:
        try:
            request_id = get_request_id(request)
            user = await self.repository.get_by_username(username, request_id)
            if not user:
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="User not found"
                )

            return BaseResponse.success(
                detail=UserResponse.model_validate(user),
                msg="User retrieved successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to retrieve user",
                detail=str(e)
            )

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id  # Store in request state 
