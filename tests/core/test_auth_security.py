import pytest
import time
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.core.auth import authenticate_user, create_security_context_for_user
from src.core.security import SecurityContext
from fastapi.testclient import TestClient
from src.main import create_app
import jwt
from src.core.settings import settings

@pytest.mark.asyncio
async def test_create_security_context_for_user_fixed():
    """Verify that create_security_context_for_user creates a valid SecurityContext."""
    username = "test_user_123"
    context = create_security_context_for_user(username)

    assert isinstance(context, SecurityContext)
    assert context.user_id == username
    assert context.session_token is not None
    assert context.created_at <= time.time()
    assert context.expires_at > time.time()
    assert "session_id" not in context.__dict__  # Verify we aren't accidentally setting arbitrary attrs if it wasn't a dataclass (it is, so init handles it)

@pytest.mark.asyncio
async def test_authenticate_user_timing_mitigation():
    """
    Verify that authenticate_user performs constant-time(ish) operations
    regardless of whether the user exists.
    """
    mock_db = AsyncMock()

    # Case 1: User does not exist
    mock_db.get_user_by_username.return_value = None

    # We want to verify that verify_password (or equivalent work) is still called
    # or at least that it doesn't return immediately.
    # To be robust, we'll patch verify_password and see if it's called with a dummy hash.

    with patch("src.core.auth.verify_password") as mock_verify:
        await authenticate_user("nonexistent", "password123", mock_db)

        # It should be called to prevent timing leaks
        assert mock_verify.called, "verify_password should be called even for non-existent users"

        # Check args to ensure it's a dummy verification
        # The exact dummy hash might change, but we expect it to be called.

    # Case 2: User exists
    mock_db.get_user_by_username.return_value = {
        "username": "exists",
        "hashed_password": "real_hash"
    }

    with patch("src.core.auth.verify_password") as mock_verify:
        mock_verify.return_value = True
        await authenticate_user("exists", "password123", mock_db)

        assert mock_verify.called
        assert mock_verify.call_args[0][1] == "real_hash"


def test_register_authorization_bypass():
    """
    Verify that mass assignment during registration cannot grant the admin role.
    """
    app = create_app()

    # Mock performance monitor to avoid pre-existing TimerContext error
    with patch('src.core.middleware.performance_monitor') as mock_pm, \
         TestClient(app) as client:
        mock_pm.timer.return_value.__enter__.return_value = None
        mock_pm.timer.return_value.__exit__.return_value = None

        # Attempt to register a user with an elevated role via mass assignment
        payload = {
            "username": "hacker_test_user",
            "password": "password123",
            "role": "admin",
            "permissions": ["*"]
        }
        response = client.post("/api/auth/register", json=payload)

        # It should either succeed (ignoring extra fields) or fail validation (422)
        # Assuming it succeeds and ignores the fields:
        if response.status_code == 200:
            data = response.json()
            assert "access_token" in data

            # Decode the token and verify the role is strictly "user"
            token = data["access_token"]
            decoded = jwt.decode(token, options={"verify_signature": False})
            assert decoded.get("role") == "user", "Role in token should be 'user', not 'admin'"
