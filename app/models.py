from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from .database import Base

class ParkingLot(Base):
    __tablename__ = "parking_lots"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    address = Column(String(255), nullable=False)
    zone = Column(String(100), nullable=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    capacity = Column(Integer, nullable=False, default=0)
    occupied = Column(Integer, nullable=False, default=0)

    price_per_hour = Column(Float, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
