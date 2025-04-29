# app/services/city_service.py
from fastapi import Request, HTTPException
from typing import List

from app.repositories.city import CityRepository
from app.schemas.city import CityResponse
from app.core.logging import log_service_call, get_request_id
from app.schemas.base import BaseResponse 
from app.schemas.city import CityCreate

class CityService:
    def __init__(self, repository: CityRepository):
        self.repository = repository

    @log_service_call("CityService")
    async def get_all_cities(self, request: Request) -> BaseResponse[List[CityResponse]]:
        try:
            request_id = get_request_id(request)  # Lấy request_id
            cities = await self.repository.get_all_cities(request_id)
            if not cities:
                raise HTTPException(
                    status_code=404,
                    detail="No cities found"
                )
            print(f"Fetched cities: {cities}")
            return BaseResponse.response(
                status=200,
                msg="Cities retrieved successfully",
                detail=[CityResponse.model_validate(city) for city in cities]
            )
        except Exception as e:
            print(f"Error in CityService: {str(e)}")
            return BaseResponse.response(
                status=500,
                msg=f"Failed to retrieve cities: {str(e)}"
            )
    @log_service_call("CityService")
    async def create_city(self, city_create: CityCreate, request: Request) -> BaseResponse[CityResponse]:
        try:
            new_city = await self.repository.create_city(city_create)

            if not new_city:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to create city"
                )

            return BaseResponse.response(
                status=201,
                msg="City created successfully",
                detail=CityResponse(**new_city)
            )

        except Exception as e:
            print(f"Error in CityService create_city: {str(e)}")
            return BaseResponse.response(
                status=500,
                msg=f"Failed to create city: {str(e)}"
            )