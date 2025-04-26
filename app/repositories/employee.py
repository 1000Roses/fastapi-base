from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.core.logging import log_service_call


class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @log_service_call("EmployeeRepository")
    async def get_by_id(self, request_id: str, employee_id: int)  -> Employee:
        result = await self.db.execute(select(Employee).where(Employee.id == employee_id))
        return result.scalar_one_or_none()

    @log_service_call("EmployeeRepository")
    async def get_all(self, request_id: str, skip: int = 0, limit: int = 100) -> list[Employee]:
        result = await self.db.execute(
            select(Employee)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @log_service_call("EmployeeRepository")
    async def create(self, employee: EmployeeCreate, request_id: str) -> Employee:
        db_employee = Employee(
            name=employee.name,
            department=employee.department,
            role=employee.role,
            type_of_working=employee.type_of_working,
            hometown=employee.hometown,
            age=employee.age,
            active=employee.active
        )
        self.db.add(db_employee)
        await self.db.commit()
        await self.db.refresh(db_employee)
        return db_employee

    @log_service_call("EmployeeRepository")
    async def update(self, employee_id: int, employee_update: EmployeeUpdate, request_id: str) -> Employee:
        db_employee = await self.get_by_id(employee_id, request_id)
        if not db_employee:
            return None

        update_data = employee_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_employee, key, value)

        await self.db.commit()
        await self.db.refresh(db_employee)
        return db_employee 