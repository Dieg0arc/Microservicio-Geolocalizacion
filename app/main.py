from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine
from . import models, schemas, crud
from .deps import get_db_session

# Crear tablas (solo para desarrollo; en producción usar migraciones)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=f"{settings.API_NAME} - Geolocation Service",
    version=settings.API_VERSION,
)


# --------- Healthcheck ---------

@app.get("/health")
def health():
    return {"status": "ok", "service": "geolocation", "env": settings.ENV}


# --------- Crear y listar parqueaderos ---------

@app.post(
    "/parkings/",
    response_model=schemas.Parking,
    status_code=status.HTTP_201_CREATED,
)
def create_parking(
    parking_in: schemas.ParkingCreate,
    db: Session = Depends(get_db_session),
):
    return crud.create_parking(db, parking_in)


@app.get(
    "/parkings/",
    response_model=List[schemas.Parking],
)
def list_parkings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db_session),
):
    return crud.list_parkings(db, skip=skip, limit=limit)


# --------- Búsqueda cercana (radar) ---------
# OJO: esto va ANTES de /parkings/{parking_id}

@app.get("/parkings/nearby")
def get_nearby(
    latitude: float,
    longitude: float,
    radius_meters: int = 1000,
    only_available: bool = True,
    db: Session = Depends(get_db_session),
):
    """
    Ejemplo:
    GET /parkings/nearby?latitude=4.5343&longitude=-75.6732&radius_meters=1200
    """
    results = crud.get_nearby_parkings(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_meters=radius_meters,
        only_available=only_available,
    )
    return {"count": len(results), "results": results}


# --------- Operaciones por ID ---------

@app.get(
    "/parkings/{parking_id}",
    response_model=schemas.Parking,
)
def get_parking(
    parking_id: int,
    db: Session = Depends(get_db_session),
):
    parking = crud.get_parking(db, parking_id)
    if not parking:
        raise HTTPException(status_code=404, detail="Parqueadero no encontrado")
    return parking


@app.patch(
    "/parkings/{parking_id}",
    response_model=schemas.Parking,
)
def update_parking(
    parking_id: int,
    parking_in: schemas.ParkingUpdate,
    db: Session = Depends(get_db_session),
):
    parking = crud.update_parking(db, parking_id, parking_in)
    if not parking:
        raise HTTPException(status_code=404, detail="Parqueadero no encontrado")
    return parking


@app.patch(
    "/parkings/{parking_id}/availability",
    response_model=schemas.Parking,
)
def update_availability(
    parking_id: int,
    availability: schemas.ParkingAvailabilityUpdate,
    db: Session = Depends(get_db_session),
):
    parking = crud.update_parking_availability(db, parking_id, availability.occupied)
    if not parking:
        raise HTTPException(status_code=404, detail="Parqueadero no encontrado")
    return parking
