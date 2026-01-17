import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.core.auth import authenticate_user

@pytest.mark.asyncio
async def test_authenticate_user_timing_attack_protection():
    """
    Test that authenticate_user performs password verification even if user is not found,
    to prevent timing attacks.
    """
    mock_db = MagicMock()
    mock_db.get_user_by_username = AsyncMock(return_value=None)

    # We patch verify_password to verify it is called
    with patch("src.core.auth.verify_password") as mock_verify:
        await authenticate_user("non_existent_user", "some_password", mock_db)

        # Verify that verify_password was called despite user not found
        # In the vulnerable code, this assertion will FAIL
        mock_verify.assert_called_once()
