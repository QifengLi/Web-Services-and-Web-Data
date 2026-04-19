from datetime import date
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models.city import City
from app.models.climate_record import ClimateRecord

DATASET_PATH = Path("data/sample_climate_records.csv")


def upsert_city(db: Session, name: str, country: str, latitude: float, longitude: float) -> City:
    existing = db.query(City).filter(City.name == name, City.country == country).first()
    if existing:
        existing.latitude = latitude
        existing.longitude = longitude
        db.add(existing)
        return existing

    city = City(name=name, country=country, latitude=latitude, longitude=longitude)
    db.add(city)
    db.flush()
    return city


def seed() -> None:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    Base.metadata.create_all(bind=engine)
    df = pd.read_csv(DATASET_PATH)

    with SessionLocal() as db:
        for row in df.to_dict(orient="records"):
            city = upsert_city(
                db,
                name=str(row["city_name"]),
                country=str(row["country"]),
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
            )

            exists = (
                db.query(ClimateRecord)
                .filter(
                    ClimateRecord.city_id == city.id,
                    ClimateRecord.record_date == row["record_date"],
                )
                .first()
            )
            if exists:
                continue

            db.add(
                ClimateRecord(
                    city_id=city.id,
                    record_date=date.fromisoformat(str(row["record_date"])),
                    temp_avg_c=float(row["temp_avg_c"]),
                    temp_min_c=float(row["temp_min_c"]),
                    temp_max_c=float(row["temp_max_c"]),
                    precipitation_mm=float(row["precipitation_mm"]),
                    wind_speed_max_mps=float(row["wind_speed_max_mps"]),
                    source=str(row.get("source", "seed")),
                    notes=str(row.get("notes", "")),
                )
            )
        db.commit()

    print("Seed completed from data/sample_climate_records.csv")


if __name__ == "__main__":
    seed()
