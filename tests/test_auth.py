from fastapi.testclient import TestClient

from app.db import init_db
from app.main import app

init_db()
client = TestClient(app)


def test_login_unknown_user():
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


def test_logout():
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
