# ClimatePulse API Documentation

## Project Summary
ClimatePulse is a data-driven web API for storing and analyzing city-level climate records.
The API is implemented using FastAPI + SQLAlchemy + SQLite and supports full CRUD operations.

## Base URL
- Local: `http://127.0.0.1:8000`
- API prefix: `/api/v1`

## Authentication
- Write endpoints are protected using header `X-API-Key`.
- Configure key in `.env` as `API_KEY`.
- Example header: `X-API-Key: cw1-local-api-key`

## Endpoints
### Meta
- `GET /` Service welcome payload
- `GET /health` Health check

### City CRUD
- `POST /api/v1/cities` Create city (auth required)
- `GET /api/v1/cities` List cities
- `GET /api/v1/cities/{city_id}` Get city by id
- `PUT /api/v1/cities/{city_id}` Update city (auth required)
- `DELETE /api/v1/cities/{city_id}` Delete city (auth required)

### Climate Record CRUD
- `POST /api/v1/climate-records` Create record (auth required)
- `GET /api/v1/climate-records` List records with optional filters
- `GET /api/v1/climate-records/{record_id}` Get record by id
- `PUT /api/v1/climate-records/{record_id}` Update record (auth required)
- `DELETE /api/v1/climate-records/{record_id}` Delete record (auth required)

### Analytics
- `GET /api/v1/analytics/cities/{city_id}/temperature-trend?days=30`
- `GET /api/v1/analytics/global/summary?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD`
- `GET /api/v1/analytics/cities/{city_id}/anomalies?threshold_c=3&days=90`

### External Data Import
- `POST /api/v1/import/open-meteo` Import climate history from Open-Meteo (auth required)

## Example Request and Response
### Create City
Request:
`POST /api/v1/cities`
```json
{
  "name": "Leeds",
  "country": "United Kingdom",
  "latitude": 53.8008,
  "longitude": -1.5491
}
```

Response (201):
```json
{
  "id": 1,
  "name": "Leeds",
  "country": "United Kingdom",
  "latitude": 53.8008,
  "longitude": -1.5491,
  "created_at": "2026-04-19T12:00:00"
}
```

## Error Codes
- `400 Bad Request`: invalid range or malformed payload
- `401 Unauthorized`: missing or invalid API key
- `404 Not Found`: resource does not exist
- `409 Conflict`: duplicate data or unique constraint conflict
- `422 Unprocessable Entity`: request validation error
- `500 Internal Server Error`: unexpected server failure

## OpenAPI
- Interactive docs: `/docs`
- ReDoc: `/redoc`
- Exported schema: `docs/openapi.json`
