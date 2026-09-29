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


def test_create_employee():
    """Verify employee registration endpoint."""
    payload = {"name": "Alice Smith", "department": "Engineering", "role": "DevOps Engineer"}
    response = client.post("/employees", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Employee created"
    assert data["employee"] == payload


def test_get_employee_by_id():
    """Verify retrieving employee by unique ID."""
    response = client.get("/employees/42")
    assert response.status_code == 200
    assert response.json() == {"id": 42}


def test_update_employee():
    """Verify updating employee record by ID."""
    payload = {"name": "Alice Smith", "role": "Lead DevOps Engineer"}
    response = client.put("/employees/42", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Employee updated"
    assert data["id"] == 42
    assert data["employee"] == payload


def test_delete_employee():
    """Verify removing employee record by ID."""
    response = client.delete("/employees/42")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Employee deleted"
    assert data["id"] == 42