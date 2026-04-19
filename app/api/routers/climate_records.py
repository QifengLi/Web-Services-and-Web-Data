from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import require_api_key
from app.models.city import City
from app.models.climate_record import ClimateRecord
from app.schemas.climate_record import ClimateRecordCreate, ClimateRecordRead, ClimateRecordUpdate

router = APIRouter(prefix="/climate-records", tags=["climate-records"])


@router.post(
    "",
    response_model=ClimateRecordRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
def create_climate_record(payload: ClimateRecordCreate, db: Session = Depends(get_db)) -> ClimateRecord:
    city = db.get(City, payload.city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")

    record = ClimateRecord(**payload.model_dump())
    db.add(record)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A record for this city and date already exists.",
        ) from exc
    db.refresh(record)
    return record


@router.get("", response_model=list[ClimateRecordRead])
def list_climate_records(
    db: Session = Depends(get_db),
    city_id: int | None = Query(default=None, gt=0),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
) -> list[ClimateRecord]:
    query = db.query(ClimateRecord)
    if city_id is not None:
        query = query.filter(ClimateRecord.city_id == city_id)
    if start_date is not None:
        query = query.filter(ClimateRecord.record_date >= start_date)
    if end_date is not None:
        query = query.filter(ClimateRecord.record_date <= end_date)
    return query.order_by(ClimateRecord.record_date.desc()).offset(skip).limit(limit).all()


@router.get("/{record_id}", response_model=ClimateRecordRead)
def get_climate_record(record_id: int, db: Session = Depends(get_db)) -> ClimateRecord:
    record = db.get(ClimateRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Climate record not found.")
    return record


@router.put("/{record_id}", response_model=ClimateRecordRead, dependencies=[Depends(require_api_key)])
def update_climate_record(record_id: int, payload: ClimateRecordUpdate, db: Session = Depends(get_db)) -> ClimateRecord:
    record = db.get(ClimateRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Climate record not found.")

    updates = payload.model_dump(exclude_unset=True)
    if "city_id" in updates and updates["city_id"] is not None:
        city = db.get(City, updates["city_id"])
        if not city:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")

    for field, value in updates.items():
        setattr(record, field, value)

    db.add(record)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Update violates unique constraints.",
        ) from exc
    db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_api_key)])
def delete_climate_record(record_id: int, db: Session = Depends(get_db)) -> None:
    record = db.get(ClimateRecord, record_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Climate record not found.")
    db.delete(record)
    db.commit()

