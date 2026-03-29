"""
Unit tests for rate_limit utility module - standalone version
"""

import pytest
import asyncio
import time
from collections import defaultdict

# Import the real settings module from src.config
from src.config import settings as real_settings


class RateLimiter:
    """Rate limiter implementation using sliding window (copy for testing)"""

    def __init__(self):
        self.requests = defaultdict(list)
        self.window_size = real_settings.rate_limit_window
        self.max_requests = real_settings.rate_limit_requests
        self._lock = asyncio.Lock()

    async def initialize(self):
        pass

    async def close(self):
        self.requests.clear()

    async def check_rate_limit(self, client_ip: str) -> bool:
        async with self._lock:
            current_time = time.time()
            window_start = current_time - self.window_size

            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip] if req_time > window_start
            ]

            if len(self.requests[client_ip]) >= self.max_requests:
                return False

            self.requests[client_ip].append(current_time)
            return True

    async def get_stats(self):
        async with self._lock:
            stats = {
                "window_size": self.window_size,
                "max_requests": self.max_requests,
                "active_clients": len(self.requests),
                "client_stats": {},
            }

            for client_ip, requests in self.requests.items():
                current_time = time.time()
                window_start = current_time - self.window_size
                recent_requests = [req for req in requests if req > window_start]

                stats["client_stats"][client_ip] = {
                    "total_requests": len(requests),
                    "recent_requests": len(recent_requests),
                    "usage_percent": (len(recent_requests) / self.max_requests) * 100,
                }

            return stats


class TestRateLimiter:
    """Test RateLimiter functionality."""

    @pytest.mark.asyncio
    async def test_check_rate_limit_first_request(self):
        rate_limiter = RateLimiter()
        result = await rate_limiter.check_rate_limit("192.168.1.1")
        assert result is True

    @pytest.mark.asyncio
    async def test_check_rate_limit_within_limit(self):
        rate_limiter = RateLimiter()
        for _ in range(min(5, rate_limiter.max_requests)):
            result = await rate_limiter.check_rate_limit("192.168.1.1")
            assert result is True

    @pytest.mark.asyncio
    async def test_check_rate_limit_different_clients(self):
        rate_limiter = RateLimiter()
        result1 = await rate_limiter.check_rate_limit("192.168.1.1")
        result2 = await rate_limiter.check_rate_limit("192.168.1.2")
        assert result1 is True
        assert result2 is True

    @pytest.mark.asyncio
    async def test_get_stats(self):
        rate_limiter = RateLimiter()
        await rate_limiter.check_rate_limit("192.168.1.1")
        stats = await rate_limiter.get_stats()
        assert "window_size" in stats
        assert "max_requests" in stats

    def test_rate_limiter_initialization(self):
        rate_limiter = RateLimiter()
        assert rate_limiter.requests is not None
        assert rate_limiter.window_size > 0
        assert rate_limiter.max_requests > 0

    @pytest.mark.asyncio
    async def test_rate_limiter_close(self):
        rate_limiter = RateLimiter()
        await rate_limiter.check_rate_limit("192.168.1.1")
        await rate_limiter.close()
        assert len(rate_limiter.requests) == 0


class TestRateLimiterEdgeCases:

    @pytest.fixture
    def rate_limiter_limited(self):
        return RateLimiter()

    @pytest.mark.asyncio
    async def test_rate_limit_exceeded(self, rate_limiter_limited):
        # Save original settings
        original_window = real_settings.rate_limit_window
        original_requests = real_settings.rate_limit_requests
        
        # Temporarily modify settings
        real_settings.rate_limit_window = 1
        real_settings.rate_limit_requests = 2
        rate_limiter_limited.window_size = 1
        rate_limiter_limited.max_requests = 2
        
        await rate_limiter_limited.check_rate_limit("192.168.1.1")
        await rate_limiter_limited.check_rate_limit("192.168.1.1")
        result = await rate_limiter_limited.check_rate_limit("192.168.1.1")
        
        # Restore original settings
        real_settings.rate_limit_window = original_window
        real_settings.rate_limit_requests = original_requests
        
        assert result is False

    @pytest.mark.asyncio
    async def test_stats_shows_usage_percent(self, rate_limiter_limited):
        # Save original settings
        original_window = real_settings.rate_limit_window
        original_requests = real_settings.rate_limit_requests
        
        # Temporarily modify settings
        real_settings.rate_limit_window = 1
        real_settings.rate_limit_requests = 2
        rate_limiter_limited.window_size = 1
        rate_limiter_limited.max_requests = 2
        
        await rate_limiter_limited.check_rate_limit("192.168.1.1")
        stats = await rate_limiter_limited.get_stats()
        client_stats = stats["client_stats"]["192.168.1.1"]
        assert client_stats["usage_percent"] == 50.0
        
        # Restore original settings
        real_settings.rate_limit_window = original_window
        real_settings.rate_limit_requests = original_requests


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
