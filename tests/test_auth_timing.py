import pytest
import time
from src.core.auth import authenticate_user, hash_password


class DummyDB:
    def __init__(self, users=None):
        self.users = users or {}

    async def get_user_by_username(self, username):
        return self.users.get(username)


@pytest.mark.asyncio
async def test_auth_failure_no_nameerror():
    db = DummyDB(
        {"admin": {"username": "admin", "hashed_password": hash_password("secret")}}
    )
    # Should return None, not raise NameError
    result = await authenticate_user("admin", "wrong_password", db)
    assert result is None


@pytest.mark.asyncio
async def test_auth_timing():
    # Setup users
    hashed = hash_password("secret")
    db = DummyDB(
        {"existing_user": {"username": "existing_user", "hashed_password": hashed}}
    )

    # Test existing user with wrong password
    start_time = time.time()
    await authenticate_user("existing_user", "wrong_password", db)
    existing_user_time = time.time() - start_time

    # Test nonexistent user
    start_time = time.time()
    await authenticate_user("nonexistent_user", "wrong_password", db)
    nonexistent_user_time = time.time() - start_time

    # Times should be comparable. We'll check they are within 0.1s of each other.
    # Note: Timing tests can be flaky in CI, so we use a generous threshold,
    # but the key is that both paths actually execute the argon2 hash.
    difference = abs(existing_user_time - nonexistent_user_time)
    print(f"Existing user time: {existing_user_time:.4f}s")
    print(f"Nonexistent user time: {nonexistent_user_time:.4f}s")
    print(f"Difference: {difference:.4f}s")

    assert difference < 0.2, f"Timing difference too large: {difference:.4f}s"
    assert nonexistent_user_time > 0.05, "Nonexistent user path bypassed hashing"


def test_dummy_hash_verify():
    from src.core.auth import verify_password, DUMMY_HASH
    start_time = time.time()
    result = verify_password("x", DUMMY_HASH)
    duration = time.time() - start_time
    assert result is False
    assert duration > 0.05, "Dummy hash verification bypassed hashing"
