from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_notifications():
    response = client.get("/api/notifications")
    assert response.status_code == 200
    assert response.json()["notifications"] == []
