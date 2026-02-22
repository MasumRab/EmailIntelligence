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
def app_instance():
    """Create the app instance once per module."""
    return create_app()

@pytest.fixture(scope="module")
def client(app_instance):
    """Create a test client fixture to avoid repeated app initialization."""
    with TestClient(app_instance) as c:
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

def test_protected_endpoint_with_valid_token(client):
    """Test accessing a protected endpoint with a valid token."""
    # Get token first
    login_response = client.post("/token", data={"username": "admin", "password": "secret"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get("/api/emails", headers={"Authorization": f"Bearer {token}"})
    # Assuming /api/emails is implemented and returns 200 or 404 (if empty) but NOT 401
    assert response.status_code in (200, 404)