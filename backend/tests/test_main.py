from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "python_info" in response.text or "process_" in response.text

def test_get_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json() == []