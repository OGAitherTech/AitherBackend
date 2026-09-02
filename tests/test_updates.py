from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_updates():
    response = client.get("/api/updates")
    assert response.status_code == 200
    assert response.json()["updates"] == []
