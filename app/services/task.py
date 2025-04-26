from typing import Optional
from fastapi import Request, status
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.schemas.base import BaseResponse
from app.core.logging import log_service_call, get_request_id


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    @log_service_call("TaskService")
    async def create_task(self, task: TaskCreate, request: Request) -> BaseResponse[TaskResponse]:
        try:
            request_id = get_request_id(request)
            if await self.repository.get_by_title(task.title, request_id):
                return BaseResponse.error(
                    status=status.HTTP_400_BAD_REQUEST,
                    msg="Task with this title already exists"
                )

            created_task = await self.repository.create(task, request_id)
            return BaseResponse.success(
                detail=TaskResponse.model_validate(created_task),
                msg="Task created successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to create task",
                detail=str(e)
            )

    @log_service_call("TaskService")
    async def get_task(self, task_id: int, request: Request) -> BaseResponse[TaskResponse]:
        try:
            request_id = get_request_id(request)
            task = await self.repository.get_by_id(task_id, request_id)
            if not task:
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="Task not found"
                )

            return BaseResponse.success(
                detail=TaskResponse.model_validate(task),
                msg="Task retrieved successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to retrieve task",
                detail=str(e)
            )

    @log_service_call("TaskService")
    async def update_task(self, task_id: int, task_update: TaskUpdate, request: Request) -> BaseResponse[TaskResponse]:
        try:
            request_id = get_request_id(request)
            task = await self.repository.get_by_id(task_id, request_id)
            if not task:
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="Task not found"
                )

            if task_update.title and task_update.title != task.title:
                if await self.repository.get_by_title(task_update.title, request_id):
                    return BaseResponse.error(
                        status=status.HTTP_400_BAD_REQUEST,
                        msg="Task with this title already exists"
                    )

            updated_task = await self.repository.update(task_id, task_update, request_id)
            return BaseResponse.success(
                detail=TaskResponse.model_validate(updated_task),
                msg="Task updated successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to update task",
                detail=str(e)
            )

    @log_service_call("TaskService")
    async def delete_task(self, task_id: int, request: Request) -> BaseResponse[None]:
        try:
            request_id = get_request_id(request)
            task = await self.repository.get_by_id(task_id, request_id)
            if not task:
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="Task not found"
                )

            await self.repository.delete(task_id, request_id)
            return BaseResponse.success(
                msg="Task deleted successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to delete task",
                detail=str(e)
            )

    @log_service_call("TaskService")
    async def get_tasks(self, request: Request, skip: int = 0, limit: int = 100) -> BaseResponse[list[TaskResponse]]:
        try:
            request_id = get_request_id(request)
            tasks = await self.repository.get_all(request_id, skip=skip, limit=limit)
            return BaseResponse.success(
                detail=[TaskResponse.model_validate(task) for task in tasks],
                msg="Tasks retrieved successfully"
            )
        except Exception as e:
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to retrieve tasks",
                detail=str(e)
            ) 