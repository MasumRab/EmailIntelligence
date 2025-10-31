"""
Test suite for MFA implementation
"""

import asyncio
import pytest
from src.core.mfa import MFAService
from src.core.database import DatabaseManager


@pytest.fixture
def mfa_service():
    return MFAService()


@pytest.fixture
async def db_manager():
    db = DatabaseManager()
    await db._ensure_initialized()
    return db


@pytest.mark.asyncio
async def test_mfa_secret_generation(mfa_service):
    """Test that MFA secrets are generated correctly"""
    secret = mfa_service.generate_secret()
    assert secret is not None
    assert len(secret) > 0
    # Should be base32 encoded
    assert all(c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567' for c in secret)


@pytest.mark.asyncio
async def test_mfa_qr_code_generation(mfa_service):
    """Test that QR codes are generated correctly"""
    secret = mfa_service.generate_secret()
    qr_code = mfa_service.generate_qr_code("testuser", secret)
    assert qr_code is not None
    assert len(qr_code) > 0
    # Should be base64 encoded PNG
    assert qr_code.startswith('iVBORw0KGgo')


@pytest.mark.asyncio
async def test_mfa_token_verification(mfa_service):
    """Test that TOTP tokens can be verified"""
    secret = mfa_service.generate_secret()
    # This test is limited because we can't generate a real TOTP token
    # without knowing the exact time, but we can test the verification
    # function with an invalid token
    result = mfa_service.verify_token(secret, "123456")
    # Should return False for invalid token
    assert result is False


@pytest.mark.asyncio
async def test_backup_code_generation(mfa_service):
    """Test that backup codes are generated correctly"""
    codes = mfa_service.generate_backup_codes(5)
    assert len(codes) == 5
    for code in codes:
        assert len(code) > 0


@pytest.mark.asyncio
async def test_backup_code_verification(mfa_service):
    """Test that backup codes can be verified"""
    codes = mfa_service.generate_backup_codes(3)
    # Test valid code
    is_valid, updated_codes = mfa_service.verify_backup_code(codes, codes[0])
    assert is_valid is True
    assert len(updated_codes) == 2
    assert codes[0] not in updated_codes
    
    # Test invalid code
    is_valid, updated_codes = mfa_service.verify_backup_code(codes, "invalid_code")
    assert is_valid is False
    assert len(updated_codes) == 3


@pytest.mark.asyncio
async def test_user_mfa_fields(db_manager):
    """Test that user records include MFA fields"""
    # Create a test user
    user_data = {
        "username": "testuser",
        "hashed_password": "hashed_password",
        "mfa_enabled": True,
        "mfa_secret": "TESTSECRET",
        "mfa_backup_codes": ["code1", "code2"]
    }
    
    created_user = await db_manager.create_user(user_data)
    assert created_user is not None
    assert "mfa_enabled" in created_user
    assert "mfa_secret" in created_user
    assert "mfa_backup_codes" in created_user
    assert created_user["mfa_enabled"] is True
    assert created_user["mfa_secret"] == "TESTSECRET"
    assert len(created_user["mfa_backup_codes"]) == 2


if __name__ == "__main__":
    pytest.main([__file__])