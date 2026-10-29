import pytest
from fastapi.testclient import TestClient

def get_app():
    from src.backend.python_backend.main import app
    return app

@pytest.fixture
def client():
    return TestClient(get_app())

def test_ai_analyze_requires_auth(client):
    """Regression test: verify /api/ai/analyze requires authentication."""
    response = client.post("/api/ai/analyze", json={
        "subject": "Test",
        "content": "Test content",
        "sender": "test@test.com"
    })
    
    assert response.status_code == 401
    
def test_performance_metrics_requires_auth(client):
    """Regression test: verify /api/performance requires authentication."""
    response = client.get("/api/performance")
    assert response.status_code == 401
