# app/api/v1/endpoints/city.py
from fastapi import APIRouter, Depends, Request
from app.services.city_service import CityService
from app.schemas.city import CityResponse
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.logging import log_service_call
from app.repositories.city import CityRepository,CityCreate
from app.schemas.base import BaseResponse

router = APIRouter()

@router.get("/", response_model=BaseResponse[List[CityResponse]])
@log_service_call("CityAPI")
async def list_cities(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    service = CityService(CityRepository(db))
    return await service.get_all_cities(request)

@router.post("/", response_model=BaseResponse[CityResponse])
@log_service_call("CityAPI")
async def create_city(
    request: Request,
    city_create: CityCreate,
    db: AsyncSession = Depends(get_db),
):
    service = CityService(CityRepository(db))
    return await service.create_city(request, city_create)