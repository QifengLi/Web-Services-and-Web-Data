from datetime import date, timedelta

from tests.conftest import API_KEY


def test_health_endpoint(client) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_city_crud_requires_api_key(client) -> None:
    payload = {
        "name": "Leeds",
        "country": "United Kingdom",
        "latitude": 53.8008,
        "longitude": -1.5491,
    }

    unauthorized = client.post("/api/v1/cities", json=payload)
    assert unauthorized.status_code == 401

    created = client.post("/api/v1/cities", json=payload, headers={"X-API-Key": API_KEY})
    assert created.status_code == 201
    city_id = created.json()["id"]

    listed = client.get("/api/v1/cities")
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.put(
        f"/api/v1/cities/{city_id}",
        json={"name": "Leeds City"},
        headers={"X-API-Key": API_KEY},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Leeds City"

    deleted = client.delete(f"/api/v1/cities/{city_id}", headers={"X-API-Key": API_KEY})
    assert deleted.status_code == 204


def test_climate_record_crud_and_analytics(client) -> None:
    city = client.post(
        "/api/v1/cities",
        json={
            "name": "Manchester",
            "country": "United Kingdom",
            "latitude": 53.4808,
            "longitude": -2.2426,
        },
        headers={"X-API-Key": API_KEY},
    )
    assert city.status_code == 201
    city_id = city.json()["id"]

    today = date.today()
    records_payload = [
        {
            "city_id": city_id,
            "record_date": (today - timedelta(days=2)).isoformat(),
            "temp_avg_c": 11.0,
            "temp_min_c": 8.0,
            "temp_max_c": 14.0,
            "precipitation_mm": 1.2,
            "wind_speed_max_mps": 5.1,
            "source": "manual",
            "notes": "Test day 1",
        },
        {
            "city_id": city_id,
            "record_date": (today - timedelta(days=1)).isoformat(),
            "temp_avg_c": 17.0,
            "temp_min_c": 14.0,
            "temp_max_c": 20.0,
            "precipitation_mm": 0.0,
            "wind_speed_max_mps": 3.4,
            "source": "manual",
            "notes": "Test day 2",
        },
    ]

    for payload in records_payload:
        created = client.post("/api/v1/climate-records", json=payload, headers={"X-API-Key": API_KEY})
        assert created.status_code == 201

    listed = client.get(f"/api/v1/climate-records?city_id={city_id}")
    assert listed.status_code == 200
    assert len(listed.json()) == 2
    record_id = listed.json()[0]["id"]

    updated = client.put(
        f"/api/v1/climate-records/{record_id}",
        json={"notes": "Updated by test"},
        headers={"X-API-Key": API_KEY},
    )
    assert updated.status_code == 200
    assert updated.json()["notes"] == "Updated by test"

    trend = client.get(f"/api/v1/analytics/cities/{city_id}/temperature-trend?days=10")
    assert trend.status_code == 200
    assert trend.json()["records_count"] == 2

    summary = client.get("/api/v1/analytics/global/summary")
    assert summary.status_code == 200
    assert summary.json()["records_count"] >= 2

    anomalies = client.get(f"/api/v1/analytics/cities/{city_id}/anomalies?threshold_c=2&days=10")
    assert anomalies.status_code == 200
    assert anomalies.json()["anomalies_found"] >= 0

