from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_models():
    response = client.get("/api/ai/models")
    assert response.status_code == 200
    assert response.json()["models"] == []


def test_chat_foundation():
    response = client.post("/api/ai/chat", json={"message": "Hello"})
    assert response.status_code == 200
    assert response.json()["success"] is False
