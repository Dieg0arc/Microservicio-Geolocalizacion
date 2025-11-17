from typing import List, Optional, Dict
from sqlalchemy.orm import Session

from . import models, schemas
from .utils.geo import haversine_distance_m


def create_parking(db: Session, parking_in: schemas.ParkingCreate) -> models.ParkingLot:
    data = parking_in.model_dump()
    db_parking = models.ParkingLot(**data)
    db.add(db_parking)
    db.commit()
    db.refresh(db_parking)
    return db_parking


def get_parking(db: Session, parking_id: int) -> Optional[models.ParkingLot]:
    return db.query(models.ParkingLot).filter(models.ParkingLot.id == parking_id).first()


def list_parkings(db: Session, skip: int = 0, limit: int = 100) -> List[models.ParkingLot]:
    return (
        db.query(models.ParkingLot)
        .filter(models.ParkingLot.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_parking(
    db: Session,
    parking_id: int,
    parking_in: schemas.ParkingUpdate,
) -> Optional[models.ParkingLot]:
    db_parking = get_parking(db, parking_id)
    if not db_parking:
        return None

    update_data = parking_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_parking, field, value)

    db.commit()
    db.refresh(db_parking)
    return db_parking


def update_parking_availability(
    db: Session,
    parking_id: int,
    occupied: int,
) -> Optional[models.ParkingLot]:
    db_parking = get_parking(db, parking_id)
    if not db_parking:
        return None

    if occupied > db_parking.capacity:
        occupied = db_parking.capacity

    db_parking.occupied = occupied

    db.commit()
    db.refresh(db_parking)
    return db_parking


def get_nearby_parkings(
    db: Session,
    latitude: float,
    longitude: float,
    radius_meters: int,
    only_available: bool = True,
) -> List[Dict]:
    """
    Versión simple: trae todos los activos y filtra en Python con Haversine.
    """
    query = db.query(models.ParkingLot).filter(models.ParkingLot.is_active == True)

    if only_available:
        query = query.filter(models.ParkingLot.occupied < models.ParkingLot.capacity)

    parkings = query.all()
    results: List[Dict] = []

    for p in parkings:
        distance = haversine_distance_m(latitude, longitude, p.latitude, p.longitude)
        if distance <= radius_meters:
            results.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "address": p.address,
                    "zone": p.zone,
                    "latitude": p.latitude,
                    "longitude": p.longitude,
                    "capacity": p.capacity,
                    "occupied": p.occupied,
                    "price_per_hour": p.price_per_hour,
                    "is_active": p.is_active,
                    "distance_m": round(distance, 2),
                }
            )

    results.sort(key=lambda x: x["distance_m"])
    return results
