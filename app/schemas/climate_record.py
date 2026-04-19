from datetime import date, datetime

from pydantic import BaseModel, Field


class ClimateRecordBase(BaseModel):
    city_id: int = Field(gt=0)
    record_date: date
    temp_avg_c: float | None = None
    temp_min_c: float | None = None
    temp_max_c: float | None = None
    precipitation_mm: float | None = None
    wind_speed_max_mps: float | None = None
    source: str = Field(default="manual", min_length=1, max_length=80)
    notes: str | None = Field(default=None, max_length=500)


class ClimateRecordCreate(ClimateRecordBase):
    pass


class ClimateRecordUpdate(BaseModel):
    city_id: int | None = Field(default=None, gt=0)
    record_date: date | None = None
    temp_avg_c: float | None = None
    temp_min_c: float | None = None
    temp_max_c: float | None = None
    precipitation_mm: float | None = None
    wind_speed_max_mps: float | None = None
    source: str | None = Field(default=None, min_length=1, max_length=80)
    notes: str | None = Field(default=None, max_length=500)


class ClimateRecordRead(ClimateRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

