"""
AI service interfaces for provider abstraction
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime


class AIProvider(ABC):
    """Abstract interface for AI providers"""
    
    @abstractmethod
    async def analyze_conflict(
        self, 
        pr_data: Dict[str, Any], 
        conflict_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze conflicts using AI"""
        pass
    
    @abstractmethod
    async def generate_resolution_suggestions(
        self, 
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate resolution suggestions based on analysis"""
        pass
    
    @abstractmethod
    async def assess_complexity(
        self, 
        pr_data: Dict[str, Any]
    ) -> float:
        """Assess complexity of PR changes"""
        pass
    
    @abstractmethod
    async def validate_solution(
        self, 
        solution: str, 
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate proposed solution"""
        pass


class AIClient(ABC):
    """Abstract AI client interface"""
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize AI client"""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check AI service health"""
        pass
    
    @abstractmethod
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> Dict[str, Any]:
        """Send chat completion request"""
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close AI client connection"""
        pass


class CircuitBreaker:
    """Circuit breaker pattern for AI service resilience"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 300):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'closed'  # closed, open, half-open
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.record_failure()
        else:
            await self.record_success()
    
    async def record_success(self):
        """Record successful operation"""
        self.failure_count = 0
        self.state = 'closed'
    
    async def record_failure(self):
        """Record failed operation"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'open'
    
    async def can_attempt(self) -> bool:
        """Check if operation can be attempted"""
        if self.state == 'closed':
            return True
        elif self.state == 'open':
            # Check if timeout has passed
            if self.last_failure_time:
                time_since_failure = (datetime.utcnow() - self.last_failure_time).total_seconds()
                if time_since_failure >= self.timeout:
                    self.state = 'half-open'
                    return True
            return False
        elif self.state == 'half-open':
            return True
        
        return False


class RateLimiter:
    """Token bucket rate limiter for AI API calls"""
    
    def __init__(self, rate_per_minute: int = 3):
        self.rate_per_minute = rate_per_minute
        self.tokens = rate_per_minute
        self.last_refill = datetime.utcnow()
        self.lock = None  # Will be initialized in async context
    
    async def acquire(self) -> bool:
        """Acquire token for API call"""
        import asyncio
        if not self.lock:
            self.lock = asyncio.Lock()
        
        async with self.lock:
            now = datetime.utcnow()
            time_passed = (now - self.last_refill).total_seconds()
            
            # Refill tokens based on time passed
            if time_passed >= 60:
                self.tokens = self.rate_per_minute
                self.last_refill = now
            
            if self.tokens > 0:
                self.tokens -= 1
                return True
            
            return False
    
    async def wait_for_token(self) -> bool:
        """Wait for available token"""
        import asyncio
        
        max_wait = 60  # Maximum wait time in seconds
        wait_time = 0
        
        while not await self.acquire():
            await asyncio.sleep(1)
            wait_time += 1
            
            if wait_time >= max_wait:
                return False
        
        return True


class CacheManager:
    """AI response cache manager"""
    
    def __init__(self, cache_ttl: int = 3600):
        self.cache = {}
        self.cache_ttl = cache_ttl
    
    def _generate_key(self, prompt: str, context: Dict[str, Any]) -> str:
        """Generate cache key for request"""
        import hashlib
        content = f"{prompt}_{str(sorted(context.items()))}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, prompt: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached response"""
        key = self._generate_key(prompt, context)
        
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            
            # Check if cache is still valid
            if (datetime.utcnow() - timestamp).total_seconds() < self.cache_ttl:
                return cached_data
            else:
                # Remove expired cache
                del self.cache[key]
        
        return None
    
    def set(self, prompt: str, context: Dict[str, Any], response: Dict[str, Any]) -> None:
        """Cache AI response"""
        key = self._generate_key(prompt, context)
        self.cache[key] = (response, datetime.utcnow())
    
    def clear(self) -> None:
        """Clear all cached responses"""
        self.cache.clear()