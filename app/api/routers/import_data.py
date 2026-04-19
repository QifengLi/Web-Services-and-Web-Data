from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import require_api_key
from app.models.city import City
from app.services.importer import import_open_meteo_data

router = APIRouter(prefix="/import", tags=["import"])


class OpenMeteoImportRequest(BaseModel):
    city_id: int = Field(gt=0)
    start_date: date = Field(default_factory=lambda: date.today() - timedelta(days=30))
    end_date: date = Field(default_factory=lambda: date.today() - timedelta(days=1))


class ImportResponse(BaseModel):
    city_id: int
    inserted_records: int
    source: str


@router.post(
    "/open-meteo",
    response_model=ImportResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_api_key)],
)
def import_from_open_meteo(payload: OpenMeteoImportRequest, db: Session = Depends(get_db)) -> ImportResponse:
    city = db.get(City, payload.city_id)
    if not city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
    if payload.start_date > payload.end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="start_date must be <= end_date.")

    inserted = import_open_meteo_data(db=db, city=city, start_date=payload.start_date, end_date=payload.end_date)
    return ImportResponse(city_id=city.id, inserted_records=inserted, source="open-meteo")

