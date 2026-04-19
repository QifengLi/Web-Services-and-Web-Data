from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.analytics import (
    CityAnomalyResponse,
    CityTemperatureTrendResponse,
    GlobalClimateSummaryResponse,
)
from app.services.analytics import city_anomalies, city_temperature_trend, global_summary

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/cities/{city_id}/temperature-trend", response_model=CityTemperatureTrendResponse)
def get_city_temperature_trend(
    city_id: int,
    days: int = Query(default=30, ge=1, le=3650),
    db: Session = Depends(get_db),
) -> CityTemperatureTrendResponse:
    try:
        return city_temperature_trend(db, city_id=city_id, days=days)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/global/summary", response_model=GlobalClimateSummaryResponse)
def get_global_summary(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    db: Session = Depends(get_db),
) -> GlobalClimateSummaryResponse:
    return global_summary(db, start_date=start_date, end_date=end_date)


@router.get("/cities/{city_id}/anomalies", response_model=CityAnomalyResponse)
def get_city_anomalies(
    city_id: int,
    threshold_c: float = Query(default=3.0, ge=0.1, le=20.0),
    days: int = Query(default=90, ge=1, le=3650),
    db: Session = Depends(get_db),
) -> CityAnomalyResponse:
    try:
        return city_anomalies(db, city_id=city_id, threshold_c=threshold_c, days=days)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

