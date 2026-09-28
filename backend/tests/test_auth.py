from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    username = "jenkins_test_user"
    password = "test123"
    r = client.post("/auth/register", json={"username": username, "password": password})
    assert r.status_code in (200, 400)
    r = client.post("/auth/login", json={"username": username, "password": password})
    assert r.status_code == 200
    assert "access_token" in r.json()
