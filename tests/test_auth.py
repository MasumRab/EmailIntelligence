"""
Tests for authentication functionality
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.security import HTTPAuthorizationCredentials
from src.core.auth import get_current_active_user, verify_token
from src.main import create_app

@pytest.fixture(scope="module")
def client():
    """Create a test client fixture to avoid repeated app initialization."""
    app = create_app()
    with TestClient(app) as c:
        yield c

def test_auth_token_endpoint(client):
    """Test the token endpoint for authentication"""
    # Test with valid credentials
    response = client.post("/token", data={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Test with invalid credentials
    response = client.post("/token", data={"username": "invalid", "password": "invalid"})
    assert response.status_code == 401


def test_protected_endpoint_requires_auth(client):
    """Test that protected endpoints require authentication"""
    # Try to access a protected endpoint without authentication
    response = client.get("/api/emails")
    assert response.status_code == 401  # Unauthorized

        # Should work with valid token (after proper setup)
        # This test would require a valid token which is complex to set up in this context