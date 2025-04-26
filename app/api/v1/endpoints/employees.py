from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.employee import EmployeeService
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.core.logging import log_service_call
from typing import List


router = APIRouter()


@router.post("/get/{employee_id}")
@log_service_call("HandlerEmployeeAPI")
async def get_employee(
    employee_id: int,
    request: Request = None,
    db: AsyncSession = Depends(get_db)
):
    request_id = request.state.request_id
    service = EmployeeService(EmployeeRepository(db), request_id)
    return await service.get_employee(employee_id=employee_id, request_id=request_id)


@router.post("/get-all")
@log_service_call("EmployeeAPI")
async def get_employees(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    request_id = request.state.request_id
    service = EmployeeService(EmployeeRepository(db), request_id)
    return await service.get_employees(request, skip=skip, limit=limit)


@router.post("/create", response_model=EmployeeResponse)
@log_service_call("EmployeeAPI")
async def create_employee(
    employee: EmployeeCreate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    request_id = request.state.request_id
    service = EmployeeService(EmployeeRepository(db), request_id)
    return await service.create_employee(employee, request)


@router.post("/update/{employee_id}", response_model=EmployeeResponse)
@log_service_call("EmployeeAPI")
async def update_employee(
    employee_id: int,
    employee_update: EmployeeUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    request_id = request.state.request_id
    service = EmployeeService(EmployeeRepository(db), request_id)
    return await service.update_employee(employee_id, employee_update, request) 