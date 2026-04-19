from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.city import City
from app.models.climate_record import ClimateRecord
from app.schemas.analytics import (
    CityAnomalyResponse,
    CityTemperatureTrendResponse,
    GlobalClimateSummaryResponse,
    TemperatureAnomaly,
    TemperatureTrendPoint,
)


def city_temperature_trend(db: Session, city_id: int, days: int) -> CityTemperatureTrendResponse:
    city = db.get(City, city_id)
    if not city:
        raise ValueError("City not found.")

    start_date = date.today() - timedelta(days=days)
    records = (
        db.query(ClimateRecord)
        .filter(
            ClimateRecord.city_id == city_id,
            ClimateRecord.record_date >= start_date,
            ClimateRecord.temp_avg_c.isnot(None),
        )
        .order_by(ClimateRecord.record_date.asc())
        .all()
    )

    values = [r.temp_avg_c for r in records if r.temp_avg_c is not None]
    trend = [
        TemperatureTrendPoint(record_date=r.record_date, temp_avg_c=float(r.temp_avg_c))
        for r in records
        if r.temp_avg_c is not None
    ]

    return CityTemperatureTrendResponse(
        city_id=city.id,
        city_name=city.name,
        days=days,
        records_count=len(values),
        avg_temp_c=(sum(values) / len(values)) if values else None,
        min_temp_c=min(values) if values else None,
        max_temp_c=max(values) if values else None,
        trend=trend,
    )


def global_summary(db: Session, start_date: date | None, end_date: date | None) -> GlobalClimateSummaryResponse:
    query = db.query(
        func.count(ClimateRecord.id),
        func.avg(ClimateRecord.temp_avg_c),
        func.min(ClimateRecord.temp_avg_c),
        func.max(ClimateRecord.temp_avg_c),
        func.sum(ClimateRecord.precipitation_mm),
        func.avg(ClimateRecord.wind_speed_max_mps),
    )

    if start_date:
        query = query.filter(ClimateRecord.record_date >= start_date)
    if end_date:
        query = query.filter(ClimateRecord.record_date <= end_date)

    row = query.one()

    return GlobalClimateSummaryResponse(
        records_count=int(row[0] or 0),
        avg_temp_c=float(row[1]) if row[1] is not None else None,
        min_temp_c=float(row[2]) if row[2] is not None else None,
        max_temp_c=float(row[3]) if row[3] is not None else None,
        total_precipitation_mm=float(row[4]) if row[4] is not None else None,
        average_wind_speed_mps=float(row[5]) if row[5] is not None else None,
    )


def city_anomalies(db: Session, city_id: int, threshold_c: float, days: int) -> CityAnomalyResponse:
    city = db.get(City, city_id)
    if not city:
        raise ValueError("City not found.")

    start_date = date.today() - timedelta(days=days)
    records = (
        db.query(ClimateRecord)
        .filter(
            ClimateRecord.city_id == city_id,
            ClimateRecord.record_date >= start_date,
            ClimateRecord.temp_avg_c.isnot(None),
        )
        .order_by(ClimateRecord.record_date.asc())
        .all()
    )
    values = [r.temp_avg_c for r in records if r.temp_avg_c is not None]
    if not values:
        return CityAnomalyResponse(
            city_id=city.id,
            city_name=city.name,
            threshold_c=threshold_c,
            anomalies_found=0,
            anomalies=[],
        )

    mean_temp = sum(values) / len(values)
    anomalies = []
    for record in records:
        if record.temp_avg_c is None:
            continue
        deviation = float(record.temp_avg_c - mean_temp)
        if abs(deviation) >= threshold_c:
            anomalies.append(
                TemperatureAnomaly(
                    record_id=record.id,
                    record_date=record.record_date,
                    temp_avg_c=float(record.temp_avg_c),
                    deviation_c=deviation,
                )
            )

    return CityAnomalyResponse(
        city_id=city.id,
        city_name=city.name,
        threshold_c=threshold_c,
        anomalies_found=len(anomalies),
        anomalies=anomalies,
    )

