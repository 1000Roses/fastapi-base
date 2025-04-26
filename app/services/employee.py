from fastapi import Request, status
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.schemas.base import BaseResponse
from app.core.logging import log_service_call, get_request_id
from loguru import logger

class EmployeeService:
    def __init__(self, repository: EmployeeRepository, request_id: str):
        self.repository = repository
        self.request_id = request_id
        self.logger = logger.bind(request_id=request_id)

    @log_service_call("EmployeeService")
    async def get_employee(self, employee_id: int, request_id: str) -> BaseResponse[EmployeeResponse]:
        employee = await self.repository.get_by_id(request_id=request_id, employee_id=employee_id)
        if not employee:
            return BaseResponse.error(
                status=status.HTTP_404_NOT_FOUND,
                msg="Employee not found"
            )
        return BaseResponse.success(
            detail=EmployeeResponse.model_validate(employee),
            msg="Employee retrieved successfully"
        )

    @log_service_call("EmployeeService")
    async def get_employees(self, request: Request, skip: int = 0, limit: int = 100) -> BaseResponse[list[EmployeeResponse]]:
        try:
            employees = await self.repository.get_all(self.request_id, skip=skip, limit=limit)
            return BaseResponse.success(
                detail=[EmployeeResponse.model_validate(emp) for emp in employees],
                msg="Employees retrieved successfully"
            )
        except Exception as e:
            self.logger.error(f"Failed to retrieve employees: {str(e)}")
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to retrieve employees",
                detail=str(e)
            )

    @log_service_call("EmployeeService")
    async def create_employee(self, employee: EmployeeCreate, request: Request) -> BaseResponse[EmployeeResponse]:
        try:
            self.logger.info(f"Creating new employee: {employee.name}")
            created_employee = await self.repository.create(employee, self.request_id)
            self.logger.info(f"Successfully created employee with ID: {created_employee.id}")
            return BaseResponse.success(
                detail=EmployeeResponse.model_validate(created_employee),
                msg="Employee created successfully"
            )
        except Exception as e:
            self.logger.error(f"Failed to create employee: {str(e)}")
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to create employee",
                detail=str(e)
            )

    @log_service_call("EmployeeService")
    async def update_employee(self, employee_id: int, employee_update: EmployeeUpdate, request: Request) -> BaseResponse[EmployeeResponse]:
        try:
            self.logger.info(f"Updating employee with ID: {employee_id}")
            updated_employee = await self.repository.update(employee_id, employee_update, self.request_id)
            if not updated_employee:
                self.logger.warning(f"Employee not found with ID: {employee_id}")
                return BaseResponse.error(
                    status=status.HTTP_404_NOT_FOUND,
                    msg="Employee not found"
                )
            self.logger.info(f"Successfully updated employee with ID: {employee_id}")
            return BaseResponse.success(
                detail=EmployeeResponse.model_validate(updated_employee),
                msg="Employee updated successfully"
            )
        except Exception as e:
            self.logger.error(f"Failed to update employee with ID {employee_id}: {str(e)}")
            return BaseResponse.error(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                msg="Failed to update employee",
                detail=str(e)
            ) 