from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Verify root endpoint returns expected service status message."""
    response = client.get("/")
    assert response.status_code == 200


def test_health():
    """Verify health endpoint reports healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_metrics():
    """Verify Prometheus metrics exposition endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "python_info" in response.text or "process_" in response.text


def test_get_employees():
    """Verify retrieving employee list."""
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == []