"""Tests for the Onkyo API."""

import pytest
from main import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    with app.app.test_client() as client:
        yield client


def test_index(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Onkyo API"
    assert "documentation" in data


def test_health(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
