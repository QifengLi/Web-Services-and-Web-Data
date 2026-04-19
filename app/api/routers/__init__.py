from app.api.routers.analytics import router as analytics_router
from app.api.routers.cities import router as cities_router
from app.api.routers.climate_records import router as climate_records_router
from app.api.routers.import_data import router as import_router

__all__ = ["cities_router", "climate_records_router", "analytics_router", "import_router"]

