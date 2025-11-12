"""
OpenAI client implementation with rate limiting and caching
"""

import asyncio
import time
import json
import structlog
from typing import Dict, List, Any, Optional
from datetime import datetime

from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion

from .interfaces import AIClient, RateLimiter, CircuitBreaker, CacheManager
from ..config.settings import settings

logger = structlog.get_logger()


class OpenAIClient(AIClient):
    """
    OpenAI client with rate limiting, caching, and circuit breaker
    """
    
    def __init__(self):
        self.client: Optional[AsyncOpenAI] = None
        self.rate_limiter = RateLimiter(rate_per_minute=settings.ai_rate_limit_rpm)
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=settings.ai_circuit_breaker_threshold,
            timeout=settings.ai_circuit_breaker_timeout
        )
        self.cache_manager = CacheManager(cache_ttl=settings.ai_cache_ttl)
        self.initialized = False
        self.request_count = 0
        self.error_count = 0
        self.last_request_time = None
    
    async def initialize(self) -> bool:
        """Initialize OpenAI client with API key validation"""
        try:
            if not settings.openai_api_key:
                logger.error("OpenAI API key not configured")
                return False
            
            # Initialize OpenAI client
            self.client = AsyncOpenAI(
                api_key=settings.openai_api_key,
                timeout=settings.openai_timeout
            )
            
            # Test connection with a simple request
            test_response = await self.chat_completion([
                {"role": "user", "content": "Hello"}
            ], max_tokens=10)
            
            if test_response and "choices" in test_response:
                self.initialized = True
                logger.info("OpenAI client initialized successfully", 
                           model=settings.openai_model)
                return True
            else:
                logger.error("OpenAI client test failed")
                return False
                
        except Exception as e:
            logger.error("Failed to initialize OpenAI client", error=str(e))
            return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Check OpenAI service health and client status"""
        try:
            if not self.initialized or not self.client:
                return {
                    "status": "not_initialized",
                    "healthy": False,
                    "error": "Client not initialized"
                }
            
            # Test with a simple request
            start_time = time.time()
            test_response = await self.chat_completion([
                {"role": "user", "content": "Status check"}
            ], max_tokens=5)
            response_time = time.time() - start_time
            
            healthy = test_response and "choices" in test_response
            
            return {
                "status": "healthy" if healthy else "unhealthy",
                "healthy": healthy,
                "response_time": response_time,
                "initialized": self.initialized,
                "request_count": self.request_count,
                "error_count": self.error_count,
                "circuit_breaker_state": self.circuit_breaker.state,
                "last_request": self.last_request_time.isoformat() if self.last_request_time else None
            }
            
        except Exception as e:
            logger.error("OpenAI health check failed", error=str(e))
            return {
                "status": "error",
                "healthy": False,
                "error": str(e),
                "initialized": self.initialized
            }
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send chat completion request with rate limiting and caching
        """
        if not self.initialized or not self.client:
            raise Exception("OpenAI client not initialized")
        
        # Apply circuit breaker check
        if not await self.circuit_breaker.can_attempt():
            logger.warning("Circuit breaker open, skipping request")
            raise Exception("Circuit breaker is open")
        
        # Generate cache key
        context = {
            "messages": messages,
            "model": model or settings.openai_model,
            "max_tokens": max_tokens or settings.openai_max_tokens,
            "temperature": temperature or settings.openai_temperature,
            **kwargs
        }
        
        prompt = json.dumps(messages)
        cached_response = self.cache_manager.get(prompt, context)
        
        if cached_response:
            logger.debug("Returning cached AI response", 
                        prompt_hash=hash(prompt))
            return cached_response
        
        # Apply rate limiting
        if not await self.rate_limiter.wait_for_token():
            logger.error("Rate limit exceeded")
            raise Exception("Rate limit exceeded")
        
        try:
            # Make request to OpenAI
            start_time = time.time()
            response = await self.client.chat.completions.create(
                model=model or settings.openai_model,
                messages=messages,
                max_tokens=max_tokens or settings.openai_max_tokens,
                temperature=temperature or settings.openai_temperature,
                timeout=settings.openai_timeout,
                **kwargs
            )
            
            response_time = time.time() - start_time
            self.request_count += 1
            self.last_request_time = datetime.utcnow()
            
            # Convert response to dict
            response_data = {
                "choices": [
                    {
                        "message": {
                            "role": choice.message.role,
                            "content": choice.message.content
                        },
                        "finish_reason": choice.finish_reason
                    }
                    for choice in response.choices
                ],
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                } if response.usage else None,
                "response_time": response_time,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Cache the response
            self.cache_manager.set(prompt, context, response_data)
            
            # Record success
            await self.circuit_breaker.record_success()
            
            logger.info("OpenAI request completed",
                       model=response.model,
                       tokens=response.usage.total_tokens if response.usage else 0,
                       response_time=response_time)
            
            return response_data
            
        except Exception as e:
            self.error_count += 1
            await self.circuit_breaker.record_failure()
            
            logger.error("OpenAI request failed",
                        error=str(e),
                        request_count=self.request_count,
                        error_count=self.error_count)
            
            # Re-raise with context
            raise Exception(f"OpenAI request failed: {str(e)}")
    
    async def generate_embedding(
        self, 
        text: str,
        model: str = "text-embedding-ada-002"
    ) -> List[float]:
        """
        Generate embeddings for text
        """
        if not self.initialized or not self.client:
            raise Exception("OpenAI client not initialized")
        
        try:
            response = await self.client.embeddings.create(
                model=model,
                input=text
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            logger.error("OpenAI embedding request failed", error=str(e))
            raise Exception(f"OpenAI embedding failed: {str(e)}")
    
    async def batch_completion(
        self,
        requests: List[Dict[str, Any]],
        max_concurrent: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Process multiple requests in parallel with rate limiting
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_request(request_data):
            async with semaphore:
                try:
                    return await self.chat_completion(**request_data)
                except Exception as e:
                    logger.error("Batch request failed", error=str(e))
                    return {"error": str(e)}
        
        # Process all requests
        tasks = [process_request(req) for req in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Log batch statistics
        successful = sum(1 for r in results if isinstance(r, dict) and "error" not in r)
        failed = len(results) - successful
        
        logger.info("Batch completion completed",
                   total=len(requests),
                   successful=successful,
                   failed=failed)
        
        return results
    
    async def close(self) -> None:
        """Close OpenAI client connection"""
        if self.client:
            await self.client.close()
            logger.info("OpenAI client closed")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get client statistics"""
        return {
            "initialized": self.initialized,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_count / max(self.request_count, 1),
            "circuit_breaker_state": self.circuit_breaker.state,
            "cache_size": len(self.cache_manager.cache),
            "last_request": self.last_request_time.isoformat() if self.last_request_time else None
        }


# Global OpenAI client instance
openai_client = OpenAIClient()


async def get_openai_client() -> OpenAIClient:
    """Get initialized OpenAI client"""
    if not openai_client.initialized:
        await openai_client.initialize()
    return openai_client