"""
Tests for authentication functionality
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.security import HTTPAuthorizationCredentials
from src.core.auth import get_current_active_user, verify_token
from src.main import create_app
from src.core.database import get_db, DatabaseManager

app = create_app()

async def override_get_db():
    db = DatabaseManager(db_path=":memory:")
    await db.initialize()
    return db

app.dependency_overrides[get_db] = override_get_db

def test_auth_token_endpoint():
    """Test the token endpoint for authentication"""
    with TestClient(app) as client:
        # Create a user first
        client.post("/api/auth/register", json={"username": "admin", "password": "secret"})

        # Test with valid credentials
        response = client.post("/api/auth/login", json={"username": "admin", "password": "secret"})
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
        
        # Test with invalid credentials
        response = client.post("/api/auth/login", json={"username": "invalid", "password": "invalid"})
        assert response.status_code == 401


def test_protected_endpoint_requires_auth():
    """Test that protected endpoints require authentication"""
    with TestClient(app) as client:
        # Try to access a protected endpoint without authentication
        response = client.get("/api/emails", headers={"Authorization": "Bearer invalid"})
        assert response.status_code == 401  # Unauthorized