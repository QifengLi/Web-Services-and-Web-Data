import argparse
from datetime import date, timedelta

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.city import City
from app.services.importer import import_open_meteo_data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import climate records from Open-Meteo archive API.")
    parser.add_argument("--city-id", type=int, required=True, help="City ID stored in local database.")
    parser.add_argument(
        "--start-date",
        type=lambda x: date.fromisoformat(x),
        default=date.today() - timedelta(days=30),
        help="Start date in YYYY-MM-DD format.",
    )
    parser.add_argument(
        "--end-date",
        type=lambda x: date.fromisoformat(x),
        default=date.today() - timedelta(days=1),
        help="End date in YYYY-MM-DD format.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.start_date > args.end_date:
        raise ValueError("start-date must not be later than end-date.")

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        city = db.get(City, args.city_id)
        if not city:
            raise ValueError(f"City with id={args.city_id} does not exist.")
        inserted = import_open_meteo_data(db=db, city=city, start_date=args.start_date, end_date=args.end_date)
    print(f"Open-Meteo import complete. Inserted records: {inserted}")


if __name__ == "__main__":
    main()

