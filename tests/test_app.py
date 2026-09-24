"""Tests for the Kube Traffic Lens Flask application."""
# pylint: disable=redefined-outer-name
import os
import pytest
from app import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_index_returns_200(client):
    """Verify home page is available."""
    response = client.get("/")

    assert response.status_code == 200


def test_health_endpoint(client):
    """Verify health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "UP"
    }


def test_ready_endpoint(client):
    """Verify readiness endpoint."""
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "READY",
        "acceptingTraffic": True
    }


def test_details_endpoint(client):
    """Verify application details endpoint."""
    response = client.get("/api/details")

    data = response.get_json()

    assert response.status_code == 200
    assert data["application"] == "kube-traffic-lens"
    assert data["version"] == os.getenv("APP_VERSION", "v1.0.0")
    assert data["environment"] == os.getenv("APP_ENVIRONMENT", "local")
    assert "pod" in data
    assert "hostname" in data
