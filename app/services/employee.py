from fastapi import Request, status
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.models.employee import Employee
from app.schemas.base import BaseResponse
from app.core.logging import log_service_call, get_request_id
from app.core.global_define import *
from loguru import logger

class EmployeeService:
    def __init__(self, repository: EmployeeRepository, request_id: str):
        self.repository = repository
        self.request_id = request_id
        self.logger = logger.bind(request_id=request_id)

    @log_service_call("EmployeeService")
    async def get_employee(self, employee_id: int, request_id: str) -> BaseResponse[EmployeeResponse]:
        employee_db = await self.repository.get_by_id(request_id=request_id, employee_id=employee_id)
        if not employee_db:
            return SystemMessages.WRONG_PARAMS
        return BaseResponse.response(
            status=1,
            detail=EmployeeResponse.model_validate(employee_db),
            msg="Employee retrieved successfully"
        )

    @log_service_call("EmployeeService")
    async def get_employees(self, request_id: str, skip: int = 0, limit: int = 100) -> BaseResponse[list[EmployeeResponse]]:
        employees = await self.repository.get_all(request_id=self.request_id, skip=skip, limit=limit)
        return BaseResponse.response(
            status=1,
            detail=[EmployeeResponse.model_validate(emp) for emp in employees],
            msg="Employees retrieved successfully"
        )

    @log_service_call("EmployeeService")
    async def create_employee(self, request_id: str, employee: EmployeeCreate) -> BaseResponse[EmployeeResponse]:
        created_employee = await self.repository.create(request_id= self.request_id, employee=employee)
        if not isinstance(created_employee, Employee):
            return SystemMessages.DB_FAILED
        self.logger.info(f"Successfully created employee with ID: {created_employee.id}")
        return BaseResponse.response(
            status=1,
            detail=EmployeeResponse.model_validate(created_employee),
            msg="Employee created successfully"
        )

    @log_service_call("EmployeeService")
    async def update_employee(self, request_id: str, employee_update: EmployeeUpdate) -> BaseResponse[EmployeeResponse]:
        self.logger.info(f"Updating employee with ID: {employee_update.id}")
        updated_employee = await self.repository.update(request_id=self.request_id, employee_update=employee_update)
        if updated_employee is None:
            self.logger.warning(f"Employee not found with ID: {employee_update.id}")
            return SystemMessages.WRONG_PARAMS
        self.logger.info(f"Successfully updated employee with ID: {employee_update.id}")
        return BaseResponse.response(
            status=1,
            detail=EmployeeResponse.model_validate(updated_employee),
            msg="Employee updated successfully"
        )