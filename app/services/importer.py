from datetime import date

import requests
from sqlalchemy.orm import Session

from app.models.city import City
from app.models.climate_record import ClimateRecord

OPEN_METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def import_open_meteo_data(
    db: Session,
    city: City,
    start_date: date,
    end_date: date,
    source_label: str = "open-meteo",
) -> int:
    params = {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
        "timezone": "UTC",
    }
    response = requests.get(OPEN_METEO_ARCHIVE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    daily = payload.get("daily", {})
    dates = daily.get("time", [])
    temp_max = daily.get("temperature_2m_max", [])
    temp_min = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    wind = daily.get("wind_speed_10m_max", [])

    inserted = 0
    for idx, date_str in enumerate(dates):
        record_date = date.fromisoformat(date_str)
        existing = (
            db.query(ClimateRecord)
            .filter(ClimateRecord.city_id == city.id, ClimateRecord.record_date == record_date)
            .first()
        )
        if existing:
            continue

        tmax = temp_max[idx] if idx < len(temp_max) else None
        tmin = temp_min[idx] if idx < len(temp_min) else None
        tavg = (tmax + tmin) / 2 if tmax is not None and tmin is not None else None

        db.add(
            ClimateRecord(
                city_id=city.id,
                record_date=record_date,
                temp_avg_c=tavg,
                temp_min_c=tmin,
                temp_max_c=tmax,
                precipitation_mm=precip[idx] if idx < len(precip) else None,
                wind_speed_max_mps=wind[idx] if idx < len(wind) else None,
                source=source_label,
                notes="Imported from Open-Meteo archive API.",
            )
        )
        inserted += 1

    db.commit()
    return inserted

