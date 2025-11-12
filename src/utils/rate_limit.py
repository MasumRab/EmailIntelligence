"""
Rate limiting utility for API endpoints
"""

import time
import structlog
from typing import Dict, Any
from collections import defaultdict
from ..config.settings import settings

logger = structlog.get_logger()


class RateLimiter:
    """Rate limiter implementation using sliding window"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.window_size = settings.rate_limit_window
        self.max_requests = settings.rate_limit_requests
    
    async def initialize(self):
        """Initialize rate limiter"""
        logger.info("Rate limiter initialized", 
                   window_size=self.window_size,
                   max_requests=self.max_requests)
    
    async def close(self):
        """Clean up rate limiter"""
        self.requests.clear()
        logger.info("Rate limiter closed")
    
    async def check_rate_limit(self, client_ip: str) -> bool:
        """Check if client IP is within rate limit"""
        current_time = time.time()
        window_start = current_time - self.window_size
        
        # Remove old requests outside the window
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > window_start
        ]
        
        # Check if within limit
        if len(self.requests[client_ip]) >= self.max_requests:
            logger.warning("Rate limit exceeded", client_ip=client_ip)
            return False
        
        # Add current request
        self.requests[client_ip].append(current_time)
        return True
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get rate limiting statistics"""
        stats = {
            "window_size": self.window_size,
            "max_requests": self.max_requests,
            "active_clients": len(self.requests),
            "client_stats": {}
        }
        
        for client_ip, requests in self.requests.items():
            current_time = time.time()
            window_start = current_time - self.window_size
            recent_requests = [req for req in requests if req > window_start]
            
            stats["client_stats"][client_ip] = {
                "total_requests": len(requests),
                "recent_requests": len(recent_requests),
                "usage_percent": (len(recent_requests) / self.max_requests) * 100
            }
        
        return stats


# Global rate limiter instance
rate_limiter = RateLimiter()