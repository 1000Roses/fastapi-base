from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.core.logging import log_service_call


class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @log_service_call("EmployeeRepository")
    async def get_by_id(self, request_id: str, employee_id: int)  -> Employee | None:
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
    async def create(self, request_id:str, employee: EmployeeCreate) -> Employee:
        db_employee = Employee(
            name=employee.name,
            department=employee.department,
            role=employee.role,
            type_of_working=employee.type_of_working,
            hometown=employee.hometown,
            age=employee.age
        )
        self.db.add(db_employee)
        await self.db.commit()
        await self.db.refresh(db_employee)
        return db_employee

    @log_service_call("EmployeeRepository")
    async def update(self, request_id: str, employee_update: EmployeeUpdate) -> Employee:
        # First check if employee exists
        db_employee = await self.get_by_id(request_id, employee_update.id)
        if not db_employee:
            raise Exception(f"Không tồn tại employee_id {employee_update.id}")

        # Convert Pydantic model to dict, excluding unset values
        update_data = employee_update.model_dump(exclude_unset=True)
        
        # Remove id from update data since it's used in where clause
        employee_id = update_data.pop('id', None)
        
        # Create update statement
        stmt = (
            update(Employee)
            .where(Employee.id == employee_id)
            .values(update_data)
        )
        
        # Execute the update
        await self.db.execute(stmt)
        await self.db.commit()
        
        # Refresh and return the updated employee with all fields
        await self.db.refresh(db_employee)
        return db_employee
        
        