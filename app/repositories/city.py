# app/repositories/city.py
from app.models.city import City
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.logging import log_service_call
from typing import List
from app.schemas.city import CityCreate



class CityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @log_service_call("CityRepository")
    async def get_all_cities(self, request_id: str) -> List[City]:
        try:
            result = await self.db.execute(select(City))
            cities = result.scalars().all()
            
            print(f"Cities retrieved from DB: {cities}")
            
            return cities
        except Exception as e:
            print(f"Error in CityRepository: {str(e)}")  # Debug log lỗi
            raise Exception(f"Error fetching cities: {str(e)}")
        
    @log_service_call("CityRepository")        
    async def create_city(self, city_create: CityCreate) -> City:
        new_city = City(
            city=city_create.city,
            country_id=city_create.country_id,
        )
        self.db.add(new_city)
        await self.db.commit()
        await self.db.refresh(new_city)
        return new_city


