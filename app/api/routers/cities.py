from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import require_api_key
from app.models.city import City
from app.schemas.city import CityCreate, CityRead, CityUpdate

router = APIRouter(prefix="/cities", tags=["cities"])


@router.post("", response_model=CityRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_api_key)])
def create_city(payload: CityCreate, db: Session = Depends(get_db)) -> City:
    city = City(**payload.model_dump())
    db.add(city)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="City could not be created.") from exc
    db.refresh(city)
    return city


@router.get("", response_model=list[CityRead])
def list_cities(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
) -> list[City]:
    return db.query(City).order_by(City.id.asc()).offset(skip).limit(limit).all()


@router.get("/{city_id}", response_model=CityRead)
def get_city(city_id: int, db: Session = Depends(get_db)) -> City:
    city = db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    return city


@router.put("/{city_id}", response_model=CityRead, dependencies=[Depends(require_api_key)])
def update_city(city_id: int, payload: CityUpdate, db: Session = Depends(get_db)) -> City:
    city = db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(city, field, value)
    db.add(city)
    db.commit()
    db.refresh(city)
    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_api_key)])
def delete_city(city_id: int, db: Session = Depends(get_db)) -> None:
    city = db.get(City, city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    db.delete(city)
    db.commit()

