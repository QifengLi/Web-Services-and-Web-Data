from datetime import date

from pydantic import BaseModel


class TemperatureTrendPoint(BaseModel):
    record_date: date
    temp_avg_c: float


class CityTemperatureTrendResponse(BaseModel):
    city_id: int
    city_name: str
    days: int
    records_count: int
    avg_temp_c: float | None
    min_temp_c: float | None
    max_temp_c: float | None
    trend: list[TemperatureTrendPoint]


class GlobalClimateSummaryResponse(BaseModel):
    records_count: int
    avg_temp_c: float | None
    min_temp_c: float | None
    max_temp_c: float | None
    total_precipitation_mm: float | None
    average_wind_speed_mps: float | None


class TemperatureAnomaly(BaseModel):
    record_id: int
    record_date: date
    temp_avg_c: float
    deviation_c: float


class CityAnomalyResponse(BaseModel):
    city_id: int
    city_name: str
    threshold_c: float
    anomalies_found: int
    anomalies: list[TemperatureAnomaly]

