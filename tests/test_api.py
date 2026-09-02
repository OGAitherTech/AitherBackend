from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"


def test_ai_models():
    response = client.get("/api/ai/models")
    assert response.status_code == 200
    assert response.json()["models"] == []


def test_ai_chat_requires_message():
    response = client.post("/api/ai/chat", json={})
    assert response.status_code == 422


def test_auth_login_requires_credentials():
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 422
