"""
API Rate Limiting for Email Intelligence Platform

Implements token bucket algorithm for API endpoint rate limiting with Redis backend support.
"""

import asyncio
<<<<<<< HEAD
import logging
import time
from dataclasses import dataclass
from typing import Dict, Tuple
=======
import time
import logging
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from collections import defaultdict
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)

logger = logging.getLogger(__name__)


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""

    requests_per_minute: int = 60
    burst_limit: int = 10
    window_seconds: int = 60


@dataclass
class RateLimitState:
    """Internal state for rate limiting."""

    tokens: float
    last_refill: float


class RateLimiter:
    """
    Token bucket rate limiter for API endpoints.

    Uses in-memory storage by default. Can be extended to use Redis for distributed rate limiting.
    """

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self._limits: Dict[str, RateLimitState] = {}
        self._lock = asyncio.Lock()

    async def is_allowed(self, key: str) -> Tuple[bool, Dict[str, int]]:
        """
        Check if request is allowed for the given key.

        Args:
            key: Unique identifier (e.g., "user:123" or "ip:192.168.1.1")

        Returns:
            Tuple of (allowed: bool, headers: dict with rate limit info)
        """
        async with self._lock:
            now = time.time()
            state = self._limits.get(key)

            if state is None:
                # First request for this key
<<<<<<< HEAD
                state = RateLimitState(tokens=self.config.burst_limit, last_refill=now)
=======
                state = RateLimitState(
                    tokens=self.config.burst_limit,
                    last_refill=now
                )
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
                self._limits[key] = state

            # Refill tokens based on time passed
            time_passed = now - state.last_refill
<<<<<<< HEAD
            refill_amount = time_passed * (
                self.config.requests_per_minute / self.config.window_seconds
            )
=======
            refill_amount = time_passed * (self.config.requests_per_minute / self.config.window_seconds)
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
            state.tokens = min(self.config.burst_limit, state.tokens + refill_amount)
            state.last_refill = now

            # Check if request is allowed
            if state.tokens >= 1:
                state.tokens -= 1
                allowed = True
            else:
                allowed = False

            # Calculate headers for response
            headers = {
                "X-RateLimit-Limit": self.config.requests_per_minute,
                "X-RateLimit-Remaining": max(0, int(state.tokens)),
<<<<<<< HEAD
                "X-RateLimit-Reset": int(now + self.config.window_seconds),
=======
                "X-RateLimit-Reset": int(now + self.config.window_seconds)
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
            }

            return allowed, headers

    async def get_remaining_tokens(self, key: str) -> int:
        """Get remaining tokens for a key."""
        state = self._limits.get(key)
        if state is None:
            return self.config.burst_limit

        # Calculate current tokens (refill if needed)
        now = time.time()
        time_passed = now - state.last_refill
<<<<<<< HEAD
        refill_amount = time_passed * (
            self.config.requests_per_minute / self.config.window_seconds
        )
=======
        refill_amount = time_passed * (self.config.requests_per_minute / self.config.window_seconds)
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
        current_tokens = min(self.config.burst_limit, state.tokens + refill_amount)

        return max(0, int(current_tokens))


class APIRateLimiter:
    """
    API-specific rate limiter with endpoint-based configurations.
    """

    def __init__(self):
        self._limiters: Dict[str, RateLimiter] = {}
        self._default_config = RateLimitConfig()

    def add_endpoint_limit(self, endpoint: str, config: RateLimitConfig):
        """Add rate limiting for a specific endpoint."""
        self._limiters[endpoint] = RateLimiter(config)

    def get_limiter(self, endpoint: str) -> RateLimiter:
        """Get rate limiter for an endpoint, creating default if needed."""
        if endpoint not in self._limiters:
            self._limiters[endpoint] = RateLimiter(self._default_config)
        return self._limiters[endpoint]

<<<<<<< HEAD
    async def check_rate_limit(
        self, endpoint: str, client_key: str
    ) -> Tuple[bool, Dict[str, int]]:
=======
    async def check_rate_limit(self, endpoint: str, client_key: str) -> Tuple[bool, Dict[str, int]]:
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
        """
        Check rate limit for an endpoint and client.

        Args:
            endpoint: API endpoint path
            client_key: Client identifier (user ID, IP, etc.)

        Returns:
            Tuple of (allowed: bool, rate_limit_headers: dict)
        """
        limiter = self.get_limiter(endpoint)
        return await limiter.is_allowed(client_key)


# Global API rate limiter instance
api_rate_limiter = APIRateLimiter()

# Pre-configure some common endpoints
<<<<<<< HEAD
api_rate_limiter.add_endpoint_limit(
    "/api/emails", RateLimitConfig(requests_per_minute=120, burst_limit=20)
)
api_rate_limiter.add_endpoint_limit(
    "/api/workflows", RateLimitConfig(requests_per_minute=30, burst_limit=5)
)
api_rate_limiter.add_endpoint_limit(
    "/api/models", RateLimitConfig(requests_per_minute=20, burst_limit=3)
)
=======
api_rate_limiter.add_endpoint_limit("/api/emails", RateLimitConfig(requests_per_minute=120, burst_limit=20))
api_rate_limiter.add_endpoint_limit("/api/workflows", RateLimitConfig(requests_per_minute=30, burst_limit=5))
api_rate_limiter.add_endpoint_limit("/api/models", RateLimitConfig(requests_per_minute=20, burst_limit=3))
>>>>>>> 73a8d172 (Complete security hardening and production readiness implementation)
