import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_shorten_url():
    payload = {"target_url": "https://example.com/long-page-path"}
    response = client.post("/shorten", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert data["target_url"] == "https://example.com/long-page-path"


def test_redirect_and_analytics():
    payload = {"target_url": "https://python.org"}
    create_res = client.post("/shorten", json=payload)
    short_code = create_res.json()["short_code"]

    redirect_res = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers["location"] == "https://python.org/"

    analytics_res = client.get(f"/analytics/{short_code}")
    assert analytics_res.status_code == 200
    assert analytics_res.json()["click_count"] == 1


def test_not_found():
    response = client.get("/nonexistent123")
    assert response.status_code == 404