# ClimatePulse API (XJCO3011 Coursework 1)

ClimatePulse is an individual data-driven web API project for **Web Services and Web Data (XJCO3011)**.
It implements SQL-backed CRUD endpoints, analytics endpoints, authentication, tests, and all required coursework deliverables.

## Repository Deliverables

- Source code (FastAPI + SQLAlchemy + SQLite)
- `README.md` setup and usage guide
- API documentation PDF: `docs/api_documentation.pdf`
- Technical report PDF: `docs/technical_report.pdf`
- Presentation slides: `slides/coursework_presentation.pptx`
- GenAI declaration/supporting log excerpt: `docs/genai_conversation_log_excerpt.md`

## Project Structure

```text
app/
  api/routers/               # Endpoints
  core/                      # Settings and API-key auth
  db/                        # SQLAlchemy engine and base
  models/                    # City + ClimateRecord models
  schemas/                   # Pydantic request/response models
  services/                  # Analytics and Open-Meteo import
  main.py                    # FastAPI app entrypoint
data/
  sample_climate_records.csv # Local seed dataset
docs/
  api_documentation.pdf
  technical_report.pdf
slides/
  coursework_presentation.pptx
scripts/
  seed_data.py
  import_open_meteo_cli.py
  generate_deliverables.py
tests/
```

## Quick Start

### 1. Create virtual environment and install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
```

### 2. Configure environment

```powershell
Copy-Item .env.example .env
```

Optional: change `CW1_API_KEY` or `CW1_DATABASE_URL` in `.env`.

### 3. Seed data

```powershell
.\.venv\Scripts\python -m scripts.seed_data
```

### 4. Run API

```powershell
.\.venv\Scripts\uvicorn app.main:app --reload
```

Open:
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Authentication

Write operations require `X-API-Key`:

```text
X-API-Key: cw1-local-api-key
```

## Core Endpoints

### Meta
- `GET /`
- `GET /health`

### City CRUD
- `POST /api/v1/cities` (auth required)
- `GET /api/v1/cities`
- `GET /api/v1/cities/{city_id}`
- `PUT /api/v1/cities/{city_id}` (auth required)
- `DELETE /api/v1/cities/{city_id}` (auth required)

### Climate Record CRUD
- `POST /api/v1/climate-records` (auth required)
- `GET /api/v1/climate-records`
- `GET /api/v1/climate-records/{record_id}`
- `PUT /api/v1/climate-records/{record_id}` (auth required)
- `DELETE /api/v1/climate-records/{record_id}` (auth required)

### Analytics
- `GET /api/v1/analytics/cities/{city_id}/temperature-trend?days=30`
- `GET /api/v1/analytics/global/summary`
- `GET /api/v1/analytics/cities/{city_id}/anomalies?threshold_c=3&days=90`

### External Data Import
- `POST /api/v1/import/open-meteo` (auth required)

## Example cURL

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/cities" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: cw1-local-api-key" \
  -d "{\"name\":\"Leeds\",\"country\":\"United Kingdom\",\"latitude\":53.8008,\"longitude\":-1.5491}"
```

## Tests

```powershell
.\.venv\Scripts\python -m pytest -q
```

## Generate/Refresh Coursework Deliverables

```powershell
.\.venv\Scripts\python -m scripts.generate_deliverables
```

This script regenerates:
- API docs Markdown/PDF
- Technical report Markdown/PDF
- OpenAPI schema JSON
- Presentation PPTX

## Data Source References

- Open-Meteo Archive API: <https://archive-api.open-meteo.com/v1/archive>
- Sample seed file in this repository is coursework demonstration data for local testing.
