"""Smoke tests for the Flask application."""


def test_home_route_returns_service_payload(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["service"] == "Government Job Finder"
    assert response.get_json()["status"] == "ok"


def test_health_route_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
