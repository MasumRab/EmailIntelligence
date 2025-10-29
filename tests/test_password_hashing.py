import pytest
from unittest.mock import patch, AsyncMock
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.core.auth import hash_password, verify_password


def test_hash_password():
    """Test that password hashing works correctly."""
    password = "testpassword"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert len(hashed) > 32  # Should be salt + hash


def test_verify_password():
    """Test that password verification works correctly."""
    password = "testpassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_hash_different_salts():
    """Test that hashing the same password twice produces different results."""
    password = "testpassword"
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)
    assert hashed1 != hashed2  # Different salts should produce different hashes