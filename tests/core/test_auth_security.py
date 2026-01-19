
import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.core.auth import (
    create_security_context_for_user,
    authenticate_user,
    verify_password,
    SecurityContext,
    Permission,
    SecurityLevel,
    DUMMY_HASH
)
import time
import argon2

def test_create_security_context_for_user():
    """Verify SecurityContext is created with correct fields."""
    username = "testuser"
    context = create_security_context_for_user(username)

    assert isinstance(context, SecurityContext)
    assert context.user_id == username
    assert context.permissions == [Permission.READ, Permission.WRITE]
    assert context.security_level == SecurityLevel.INTERNAL
    assert context.session_token is not None
    assert len(context.session_token) > 0
    # Check timestamps
    now = time.time()
    assert context.created_at <= now
    assert context.expires_at > now
    # Check default fields
    assert context.ip_address is None
    assert context.origin is None

@pytest.mark.asyncio
async def test_authenticate_user_timing_attack_mitigation():
    """Verify that verify_password is called even when user is not found."""

    mock_db = AsyncMock()
    mock_db.get_user_by_username.return_value = None

    with patch("src.core.auth.verify_password") as mock_verify:
        await authenticate_user("nonexistent_user", "password", mock_db)

        # Verify get_user_by_username was called
        mock_db.get_user_by_username.assert_called_with("nonexistent_user")

        # KEY ASSERTION: verify_password must be called with dummy hash
        # This confirms the timing attack mitigation
        mock_verify.assert_called_once_with("password", DUMMY_HASH)

@pytest.mark.asyncio
async def test_authenticate_user_success():
    """Verify successful authentication."""
    mock_db = AsyncMock()
    user_data = {"username": "valid_user", "hashed_password": "hashed_secret"}
    mock_db.get_user_by_username.return_value = user_data

    with patch("src.core.auth.verify_password", return_value=True) as mock_verify:
        result = await authenticate_user("valid_user", "password", mock_db)

        assert result == user_data
        mock_verify.assert_called_once_with("password", "hashed_secret")

def test_verify_password_handles_exceptions():
    """Verify that verify_password handles argon2 exceptions safely."""

    # Test VerifyMismatchError (safe failure)
    with patch("argon2.PasswordHasher.verify", side_effect=argon2.exceptions.VerifyMismatchError):
        assert verify_password("wrong", "hash") is False

    # Test InvalidHashError (safe failure)
    with patch("argon2.PasswordHasher.verify", side_effect=argon2.exceptions.InvalidHashError):
        assert verify_password("right", "bad_hash") is False

    # Test generic Exception (safe failure)
    with patch("argon2.PasswordHasher.verify", side_effect=Exception("Unexpected")):
        assert verify_password("right", "hash") is False
