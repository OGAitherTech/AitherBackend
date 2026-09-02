from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_foundation():
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    assert response.json()["authenticated"] is False


def test_logout():
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
