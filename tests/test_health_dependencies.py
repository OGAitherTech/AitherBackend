from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dependency_health():
    response = client.get("/api/health/dependencies")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["database"] == "ready"
