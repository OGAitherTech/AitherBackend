from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_public_config():
    response = client.get("/api/config")
    assert response.status_code == 200
    body = response.json()
    assert body["app_name"] == "AitherBackend"
    assert body["app_version"] == "1.0.0"
