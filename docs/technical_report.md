# Technical Report - ClimatePulse API

## 1. Project Overview
This coursework project implements a climate statistics API with SQL-backed CRUD operations and analytical endpoints.
The solution satisfies the minimum technical requirements from the brief and extends them with:
- API key authentication for write operations
- Automated test suite
- Open-Meteo data import integration
- Delivery automation for documentation and presentation assets

## 2. Problem Scope and Requirements Mapping
The API provides:
- At least one data model with full CRUD linked to a SQL database
- More than four HTTP endpoints
- JSON responses and standard status/error codes
- Local runnable deployment via FastAPI/Uvicorn

Implemented models:
- `City`
- `ClimateRecord`

## 3. Architecture and Stack Justification
- Language: Python 3.11
- Framework: FastAPI (strong validation, built-in OpenAPI)
- ORM: SQLAlchemy 2.0 (clear model mapping and query capabilities)
- Database: SQLite (lightweight SQL database suitable for coursework demos)
- Test tooling: pytest + FastAPI TestClient

This stack was selected to maximize readability, quick iteration, and clean API documentation generation.

## 4. Data Sources and Integration
- Primary external data source: Open-Meteo archive API (`https://archive-api.open-meteo.com`)
- Local reproducible seed dataset: `data/sample_climate_records.csv`

The project includes:
- `scripts/seed_data.py` for deterministic local setup
- `scripts/import_open_meteo_cli.py` for fetching real historical data

## 5. API Design and Error Handling
The API follows REST conventions:
- Resource-oriented routing (`/cities`, `/climate-records`)
- Proper status codes (`201`, `204`, `401`, `404`, `409`, `422`)
- Validation through Pydantic schemas
- Consistent JSON response payloads

Authentication:
- Header-based API key (`X-API-Key`) required on write endpoints

## 6. Testing Strategy
Tests cover:
- Health endpoint
- City CRUD and auth checks
- Climate record CRUD
- Analytics endpoints (trend, summary, anomalies)

The tests use an isolated temporary SQLite database for repeatability.

## 7. Challenges and Lessons Learned
Challenges:
- Maintaining data consistency between city and climate record entities
- Designing analytical endpoints that remain simple but meaningful
- Producing all deliverables (code, docs PDF, report PDF, PPTX) in one coherent workflow

Lessons learned:
- Strong schema validation reduces runtime bugs early
- Modular services improve maintainability and testing
- Automating deliverable generation reduces submission risk

## 8. Limitations and Future Work
Current limitations:
- SQLite may not be ideal for high concurrency production workloads
- Authentication is API-key based instead of role-based user auth
- Analytics are descriptive, not predictive

Future improvements:
- Add PostgreSQL support and migrations
- Add JWT-based authentication and user accounts
- Add caching and pagination metadata
- Add anomaly detection models using time-series methods

## 9. GenAI Declaration and Reflection
GenAI tools were used for:
- Planning project structure
- Drafting documentation content
- Refining endpoint and test coverage ideas
- Improving wording and report organization

All generated outputs were manually reviewed, edited, and validated with runnable tests.
No AI content was accepted without developer verification.

## 10. Supplementary GenAI Conversation Logs
An excerpt log is included at:
- `docs/genai_conversation_log_excerpt.md`

Date generated: 2026-04-19
