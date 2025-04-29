from fastapi import APIRouter
from app.api.v1.endpoints import users, auth, employees, city  

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(employees.router, prefix="/employees", tags=["users"])
api_router.include_router(city.router, prefix="/cities", tags=["cities"])  
api_router.include_router(city.router, prefix="/cities/create", tags=["cities"])  