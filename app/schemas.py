from pydantic import BaseModel, Field, conint, confloat
from typing import Optional

# --------- Base ---------

class ParkingBase(BaseModel):
    name: str = Field(..., max_length=150)
    address: str = Field(..., max_length=255)
    zone: Optional[str] = Field(default=None, max_length=100)

    latitude: float
    longitude: float

    capacity: conint(ge=0) = 0
    occupied: conint(ge=0) = 0

    price_per_hour: Optional[confloat(ge=0)] = None
    is_active: bool = True


class ParkingCreate(ParkingBase):
    pass


class ParkingUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    zone: Optional[str] = None
    capacity: Optional[conint(ge=0)] = None
    occupied: Optional[conint(ge=0)] = None
    price_per_hour: Optional[confloat(ge=0)] = None
    is_active: Optional[bool] = None


class ParkingAvailabilityUpdate(BaseModel):
    occupied: conint(ge=0)


class Parking(ParkingBase):
    id: int

    class Config:
        from_attributes = True  # equivalente a orm_mode=True en Pydantic 2
