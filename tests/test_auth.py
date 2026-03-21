"""
Tests for authentication functionality
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.security import HTTPAuthorizationCredentials
from src.core.auth import get_current_active_user, verify_token
from src.main import app


import asyncio
from src.backend.python_backend.database import db_manager
from src.core.auth import hash_password

def test_auth_token_endpoint():
    """Test the token endpoint for authentication"""
    # Seed the database with a test user
    # We need to run this async code synchronously
    async def seed_user():
        await db_manager._ensure_initialized()
        # Check if user exists to avoid duplicates if test runs multiple times
        existing = await db_manager.get_user_by_username("admin")
        if not existing:
            user_data = {
                "username": "admin",
                "hashed_password": hash_password("secret"),
                "role": "admin"
            }
            # Add directly to users_data to bypass check in create_user if any logic is different
            # But create_user uses get_user_by_username too.
            # Let's use internal list append for simplicity and to avoid circular dependency issues if any
            new_id = db_manager._generate_id(db_manager.users_data)
            user_record = user_data.copy()
            user_record["id"] = new_id
            db_manager.users_data.append(user_record)

    # Run the seeding
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(seed_user())
    finally:
        loop.close()

    with TestClient(app) as client:
        # Test with valid credentials (using query params as expected by endpoint)
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
        assert response.status_code == 401  # Unauthorized
        
        # Should work with valid token (after proper setup)
        # This test would require a valid token which is complex to set up in this context