from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class MarkerBase(BaseModel):
    lugar: str
    email: EmailStr


class MarkerCreate(MarkerBase):
    imagen: Optional[str] = None


class Marker(MarkerBase):
    id: str = Field(...)
    lat: float
    lon: float
    imagen: Optional[str] = None

    class Config:
        populate_by_name = True


class Visit(BaseModel):
    timestamp: datetime
    visitor_email: EmailStr
    token: str

    class Config:
        orm_mode = True
