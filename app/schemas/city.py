from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CityCreate(BaseModel): 
    city: str
    country_id: int

class CityResponse(BaseModel):
    city_id: int
    city: str
    country_id: int
    last_update: datetime  

    class Config:
        from_attributes = True  #chuẩn Pydantic v2


