from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.logging import log_service_call


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @log_service_call("TaskRepository")
    async def get_by_id(self, task_id: int, request_id: str) -> Task:
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    @log_service_call("TaskRepository")
    async def get_by_title(self, title: str, request_id: str) -> Task:
        result = await self.db.execute(select(Task).where(Task.title == title))
        return result.scalar_one_or_none()

    @log_service_call("TaskRepository")
    async def create(self, task: TaskCreate, request_id: str) -> Task:
        db_task = Task(
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            due_date=task.due_date
        )
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    @log_service_call("TaskRepository")
    async def update(self, task_id: int, task_update: TaskUpdate, request_id: str) -> Task:
        db_task = await self.get_by_id(task_id, request_id)
        if not db_task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    @log_service_call("TaskRepository")
    async def delete(self, task_id: int, request_id: str) -> bool:
        db_task = await self.get_by_id(task_id, request_id)
        if not db_task:
            return False

        await self.db.delete(db_task)
        await self.db.commit()
        return True

    @log_service_call("TaskRepository")
    async def get_all(self, request_id: str, skip: int = 0, limit: int = 100) -> list[Task]:
        result = await self.db.execute(
            select(Task)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all() 