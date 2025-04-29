# app/models/city.py

from sqlalchemy import Column, Integer, String, SmallInteger, TIMESTAMP, func
from app.db.base import Base

class City(Base):
    __tablename__ = "city"

    city_id = Column(SmallInteger, primary_key=True, autoincrement=True, index=True)
    city = Column(String(50), nullable=False)
    country_id = Column(SmallInteger, nullable=False)
    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
