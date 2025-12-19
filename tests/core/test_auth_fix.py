
import pytest
from src.core.auth import verify_password, hash_password

def test_verify_password_with_argon2_import_fix():
    """
    Test that verifying a wrong password returns False instead of raising NameError.
    This validates the fix for the missing 'import argon2' statement.
    """
    pwd = "password"
    hashed = hash_password(pwd)

    # Should return True for correct password
    assert verify_password(pwd, hashed) is True

    # Should return False for incorrect password, NOT raise NameError
    # Prior to the fix, this would raise NameError: name 'argon2' is not defined
    assert verify_password("wrong", hashed) is False
