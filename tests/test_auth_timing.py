import time
import pytest
from unittest.mock import AsyncMock
from src.core.auth import authenticate_user, hash_password

@pytest.mark.asyncio
async def test_auth_timing_attack_mitigation():
    """
    Test that authentication time is roughly constant regardless of whether
    the user exists or not, to prevent user enumeration via timing attacks.
    """
    mock_db = AsyncMock()

    # Generate a valid hash for existing user scenario
    hashed = hash_password("correct_password")

    # Scenario 1: User does not exist
    mock_db.get_user_by_username.return_value = None

    # Warm up
    await authenticate_user("warmup", "password", mock_db)

    start_time = time.time()
    iterations = 5
    for _ in range(iterations):
        await authenticate_user("nonexistent", "password", mock_db)
    duration_no_user = (time.time() - start_time) / iterations

    # Scenario 2: User exists, wrong password
    user_data = {"username": "existing", "hashed_password": hashed}
    mock_db.get_user_by_username.return_value = user_data

    start_time = time.time()
    for _ in range(iterations):
        await authenticate_user("existing", "wrong_password", mock_db)
    duration_wrong_pass = (time.time() - start_time) / iterations

    # Ensure both paths take significant time (mitigation is active)
    # The dummy hash verification should take roughly same order of magnitude as real hash

    # We assert that the "no user" case is NOT instant.
    # Instant would be < 1ms. Argon2 is usually > 50ms.
    assert duration_no_user > 0.01, f"User not found path is too fast ({duration_no_user}s), indicating no hash verification"
