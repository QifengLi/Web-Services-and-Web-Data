from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ClimatePulse API"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./climatepulse.db"
    api_key: str = "cw1-local-api-key"

    default_seed_city: str = "Leeds"
    default_seed_country: str = "United Kingdom"

    model_config = SettingsConfigDict(
        env_prefix="CW1_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
