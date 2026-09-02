from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_current_user():
    response = client.get("/api/users/me")
    assert response.status_code == 200
    assert response.json()["authenticated"] is False
