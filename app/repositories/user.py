from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.logging import log_service_call


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @log_service_call("UserRepository")
    async def get_by_id(self, user_id: int, request_id: str) -> User:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @log_service_call("UserRepository")
    async def get_by_username(self, username: str, request_id: str) -> User:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @log_service_call("UserRepository")
    async def get_by_email(self, email: str, request_id: str) -> User:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @log_service_call("UserRepository")
    async def create(self, user: UserCreate, hashed_password: str, request_id: str) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    @log_service_call("UserRepository")
    async def update(self, user_id: int, user_update: UserUpdate, request_id: str) -> User:
        db_user = await self.get_by_id(user_id, request_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    @log_service_call("UserRepository")
    async def delete(self, user_id: int, request_id: str) -> bool:
        db_user = await self.get_by_id(user_id, request_id)
        if not db_user:
            return False

        await self.db.delete(db_user)
        await self.db.commit()
        return True 