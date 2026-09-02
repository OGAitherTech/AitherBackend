from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "AitherBackend"


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_version():
    response = client.get("/api/version")
    assert response.status_code == 200
    assert response.json()["version"] == "2.1.0"
