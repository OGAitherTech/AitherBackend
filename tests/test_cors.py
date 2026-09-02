from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_cors_allows_configured_local_origin():
    response = client.get(
        "/api/health",
        headers={"Origin": "http://localhost:3000"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
