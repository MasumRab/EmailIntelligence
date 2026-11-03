from src.core.auth import verify_password
import pytest

def test_verify_password_invalid_hash():
    # Attempt to trigger InvalidHashError
    assert verify_password("secret", "invalidhash") == False

def test_verify_password_mismatch():
    from argon2 import PasswordHasher
    ph = PasswordHasher()
    hashed = ph.hash("correct")
    assert verify_password("wrong", hashed) == False

