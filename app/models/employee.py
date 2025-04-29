from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500), nullable=False)
    department = Column(String(500), nullable=False)
    role = Column(String(100), nullable=False)
    type_of_working = Column(String(100), nullable=False)
    hometown = Column(String(500), nullable=False)
    age = Column(Integer, nullable=False)
    active = Column(Integer, nullable=False, default=1)
    t_create = Column(DateTime(timezone=True), server_default=func.now())
