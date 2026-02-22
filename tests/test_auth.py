"""
Tests for authentication functionality
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.security import HTTPAuthorizationCredentials
from src.core.auth import get_current_active_user, verify_token, hash_password
from src.backend.python_backend.main import app
from src.backend.python_backend.database import db_manager, get_db


async def override_get_db():
    return db_manager

app.dependency_overrides[get_db] = override_get_db

import asyncio

def test_auth_token_endpoint():
    """Test the token endpoint for authentication"""
    # Ensure DB is initialized so it doesn't overwrite our seed data
    asyncio.run(db_manager._ensure_initialized())

    # Seed user data
    hashed = hash_password("secret")
    user = {"username": "admin", "hashed_password": hashed, "id": 1, "role": "user"}
    # Clear existing users to avoid duplicates
    db_manager.users_data = [user]

    with TestClient(app) as client:
        # Test with valid credentials (using query params as per endpoint definition)
        response = client.post("/token", params={"username": "admin", "password": "secret"})
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
        
        # Test with invalid credentials
        response = client.post("/token", params={"username": "invalid", "password": "invalid"})
        assert response.status_code == 401


def test_protected_endpoint_requires_auth():
    """Test that protected endpoints require authentication"""
    with TestClient(app) as client:
        # Try to access a protected endpoint without authentication
        response = client.get("/api/emails")
        assert response.status_code == 403  # Forbidden (Not Authenticated)
        
        # Should work with valid token (after proper setup)
        # This test would require a valid token which is complex to set up in this context