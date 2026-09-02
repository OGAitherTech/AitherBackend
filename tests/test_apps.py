from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_apps_list():
    response = client.get("/api/apps")
    assert response.status_code == 200
    assert response.json()["apps"] == []


def test_apps_registration_validation():
    response = client.post("/api/apps", json={"name": "Aither Notes"})
    assert response.status_code == 422
