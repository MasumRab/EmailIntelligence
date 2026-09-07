import sys
from unittest.mock import MagicMock
import pytest

# Mock settings
mock_settings = MagicMock()
mock_settings.rate_limit_window = 60
mock_settings.rate_limit_requests = 5
mock_settings.rate_limit_max_clients = 3

sys.modules['src.config.settings'] = MagicMock()
sys.modules['src.config.settings'].settings = mock_settings

from src.utils.rate_limit import RateLimiter  # noqa: E402

@pytest.mark.asyncio
async def test_lru_eviction():
    limiter = RateLimiter()
    limiter.max_clients = 3 # Override for test

    # Add 3 clients
    await limiter.check_rate_limit("1.1.1.1")
    await limiter.check_rate_limit("2.2.2.2")
    await limiter.check_rate_limit("3.3.3.3")

    assert len(limiter.requests) == 3
    assert list(limiter.requests.keys()) == ["1.1.1.1", "2.2.2.2", "3.3.3.3"]

    # Access 1.1.1.1 to move it to the end
    await limiter.check_rate_limit("1.1.1.1")
    assert list(limiter.requests.keys()) == ["2.2.2.2", "3.3.3.3", "1.1.1.1"]

    # Add 4th client, which should evict the least recently used (2.2.2.2)
    await limiter.check_rate_limit("4.4.4.4")
    assert len(limiter.requests) == 3
    assert "2.2.2.2" not in limiter.requests
    assert list(limiter.requests.keys()) == ["3.3.3.3", "1.1.1.1", "4.4.4.4"]

    print("LRU Eviction Test Passed")

@pytest.mark.asyncio
async def test_rate_limiting():
    limiter = RateLimiter()
    limiter.max_requests = 2

    # Client should be allowed 2 requests
    assert await limiter.check_rate_limit("1.1.1.1") is True
    assert await limiter.check_rate_limit("1.1.1.1") is True

    # 3rd request should fail
    assert await limiter.check_rate_limit("1.1.1.1") is False

    print("Rate Limiting Test Passed")


@pytest.mark.asyncio
async def test_all():
    await test_lru_eviction()
    await test_rate_limiting()
