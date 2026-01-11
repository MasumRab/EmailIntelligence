"""
Tests for password hashing functionality
"""

import pytest

from src.core.auth import hash_password, verify_password


def test_hash_password():
    """Test that password hashing works correctly"""
    password = "test_password"
    hashed = hash_password(password)
    assert hashed is not None
    assert "$" in hashed  # Should contain salt


def test_verify_password():
    """Test that password verification works correctly"""
    password = "test_password"
    hashed = hash_password(password)

    # Should verify correctly
    assert verify_password(password, hashed) is True

    # Should not verify with wrong password
    assert verify_password("wrong_password", hashed) is False


def test_verify_password_invalid_format():
    """Test that password verification handles invalid formats gracefully"""
    # Should handle invalid format gracefully
    assert verify_password("password", "invalid_format") is False
    assert verify_password("password", "") is False
