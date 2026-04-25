from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    client = TestClient(app)
    assert client.get('/health').status_code == 200
    assert client.get('/api/health').status_code == 200
