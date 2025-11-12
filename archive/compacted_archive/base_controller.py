"""
Base AI Controller - Minimal common patterns
"""

import asyncio
import time
import structlog
from abc import ABC, abstractmethod

logger = structlog.get_logger()


class CircuitBreaker:
    def __init__(self, threshold=5, timeout=300):
        self.threshold = threshold
        self.timeout = timeout
        self.count = 0
        self.state = 'closed'
        self.last = None
    
    async def success(self):
        self.count = 0
        self.state = 'closed'
    
    async def failure(self):
        self.count += 1
        if self.count >= self.threshold:
            self.state = 'open'
    
    async def can_attempt(self):
        if self.state == 'closed':
            return True
        if self.state == 'open' and self.last:
            if time.time() - self.last > self.timeout:
                self.state = 'half-open'
            else:
                return False
        return True


class RateLimiter:
    def __init__(self, rpm=3):
        self.rpm = rpm
        self.tokens = rpm
        self.refill = time.time()
    
    async def wait(self):
        while self.tokens <= 0:
            if time.time() - self.refill >= 60:
                self.tokens = self.rpm
                self.refill = time.time()
            else:
                await asyncio.sleep(1)
        self.tokens -= 1
        return True


class BaseAIController(ABC):
    def __init__(self, rpm=3, threshold=5):
        self.rate_limiter = RateLimiter(rpm)
        self.circuit_breaker = CircuitBreaker(threshold)
        self.initialized = False
    
    async def analyze(self, context):
        if not await self.circuit_breaker.can_attempt():
            return self._fallback(context, "Circuit open")
        if not await self.rate_limiter.wait():
            return self._fallback(context, "Rate limit")
        
        try:
            result = await self._perform(context)
            await self.circuit_breaker.success()
            return result
        except Exception as e:
            await self.circuit_breaker.failure()
            return self._fallback(context, str(e))
    
    @abstractmethod
    async def _perform(self, context):
        pass
    
    def _fallback(self, context, error):
        return {"error": error, "fallback": True, "context": context}