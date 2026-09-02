from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_status_api():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {
        "status": "operational",
        "service": "AitherBackend",
    }
