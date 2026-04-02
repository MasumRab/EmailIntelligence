"""
Tests for rate limiting functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.core.rate_limiter import (
    RateLimiter,
    RateLimitConfig,
    RateLimitState,
    APIRateLimiter,
)


class TestRateLimiter:
    """Test the RateLimiter class."""

    def test_rate_limiter_creation(self):
        """Test RateLimiter instance creation."""
        limiter = RateLimiter()
        assert limiter is not None

    def test_rate_limiter_with_custom_config(self):
        """Test RateLimiter with custom configuration."""
        config = RateLimitConfig(
            max_requests=100,
            window_seconds=60,
        )
        limiter = RateLimiter(config)
        assert limiter.config.max_requests == 100
        assert limiter.config.window_seconds == 60

    @pytest.mark.asyncio
    async def test_check_rate_limit_allowed(self):
        """Test rate limit check when under limit."""
        limiter = RateLimiter()
        result = await limiter.check_rate_limit("user1")
        assert result is True

    @pytest.mark.asyncio
    async def test_check_rate_limit_exceeded(self):
        """Test rate limit check when over limit."""
        config = RateLimitConfig(max_requests=2, window_seconds=60)
        limiter = RateLimiter(config)
        
        # First two requests should be allowed
        result1 = await limiter.check_rate_limit("user1")
        result2 = await limiter.check_rate_limit("user1")
        
        # Third request should be blocked
        result3 = await limiter.check_rate_limit("user1")
        
        assert result1 is True
        assert result2 is True
        assert result3 is False

    @pytest.mark.asyncio
    async def test_reset_rate_limit(self):
        """Test rate limit reset."""
        limiter = RateLimiter()
        await limiter.check_rate_limit("user1")
        await limiter.reset("user1")
        
        # Should be allowed again after reset
        result = await limiter.check_rate_limit("user1")
        assert result is True


class TestAPIRateLimiter:
    """Test the APIRateLimiter class."""

    def test_api_limiter_creation(self):
        """Test APIRateLimiter instance creation."""
        limiter = APIRateLimiter()
        assert limiter is not None


class TestRateLimitConfig:
    """Test RateLimitConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = RateLimitConfig()
        assert config.max_requests == 100
        assert config.window_seconds == 60

    def test_custom_config(self):
        """Test custom configuration."""
        config = RateLimitConfig(
            max_requests=50,
            window_seconds=30,
        )
        assert config.max_requests == 50
        assert config.window_seconds == 30


class TestRateLimitState:
    """Test RateLimitState."""

    def test_rate_limit_state_creation(self):
        """Test RateLimitState creation."""
        state = RateLimitState(requests=0, window_start=0)
        assert state.requests == 0