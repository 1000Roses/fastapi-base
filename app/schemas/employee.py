from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=500)
    department: str = Field(..., min_length=2, max_length=500)
    role: str = Field(..., min_length=2, max_length=100)
    type_of_working: str = Field(..., min_length=2, max_length=100)
    hometown: str = Field(..., min_length=2, max_length=500)
    age: int = Field(..., gt=0, lt=150)
    active: int = Field(..., ge=0, le=1)


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=500)
    department: Optional[str] = Field(None, min_length=2, max_length=500)
    role: Optional[str] = Field(None, min_length=2, max_length=100)
    type_of_working: Optional[str] = Field(None, min_length=2, max_length=100)
    hometown: Optional[str] = Field(None, min_length=2, max_length=500)
    age: Optional[int] = Field(None, gt=0, lt=150)
    active: Optional[int] = Field(None, ge=0, le=1)


class EmployeeResponse(EmployeeBase):
    id: int
    t_create: datetime

    class Config:
        from_attributes = True 