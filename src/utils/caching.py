"""
Redis-based caching layer for the PR Resolution Automation System
"""

import redis.asyncio as redis
import json
import structlog
import hashlib
from typing import Any, Optional, Dict
from ..config.settings import settings

logger = structlog.get_logger()


class CacheManager:
    """Redis cache manager with connection pooling and error handling"""

    def __init__(self):
        self._redis: Optional[redis.Redis] = None
        self._connected = False

    async def initialize(self):
        """Initialize Redis connection"""
        try:
            self._redis = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
                max_connections=20,
                socket_keepalive=True,
                socket_keepalive_options={},
            )

            # Test connection
            await self._redis.ping()
            self._connected = True
            logger.info("Redis cache initialized", redis_url=settings.redis_url)

        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            self._connected = False
            # Continue without cache - don't fail startup
            logger.warning("Continuing without cache")

    async def close(self):
        """Close Redis connection"""
        if self._redis and self._connected:
            await self._redis.close()
            logger.info("Redis connection closed")

    async def health_check(self) -> bool:
        """Check Redis health"""
        if not self._redis or not self._connected:
            return False

        try:
            await self._redis.ping()
            return True
        except Exception as e:
            logger.error("Redis health check failed", error=str(e))
            return False

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self._connected:
            return None

        try:
            value = await self._redis.get(key)
            if value is None:
                return None

            return json.loads(value)
        except Exception as e:
            logger.error("Cache get failed", key=key, error=str(e))
            return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL"""
        if not self._connected:
            return False

        try:
            serialized_value = json.dumps(value, default=str)
            await self._redis.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            logger.error("Cache set failed", key=key, error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        if not self._connected:
            return False

        try:
            result = await self._redis.delete(key)
            return result > 0
        except Exception as e:
            logger.error("Cache delete failed", key=key, error=str(e))
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self._connected:
            return False

        try:
            result = await self._redis.exists(key)
            return result > 0
        except Exception as e:
            logger.error("Cache exists check failed", key=key, error=str(e))
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        if not self._connected:
            return 0

        try:
            keys = await self._redis.keys(pattern)
            if keys:
                return await self._redis.delete(*keys)
            return 0
        except Exception as e:
            logger.error("Cache clear pattern failed", pattern=pattern, error=str(e))
            return 0

    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if not self._connected:
            return {"status": "disconnected"}

        try:
            info = await self._redis.info()
            return {
                "status": "connected",
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
            }
        except Exception as e:
            logger.error("Failed to get cache stats", error=str(e))
            return {"status": "error", "error": str(e)}


class FictionalityCacheManager:
    """
    Specialized cache manager for fictionality analysis

    Extends the base CacheManager with fictionality-specific caching patterns
    and content hashing for deduplication.
    """

    def __init__(self, base_manager: CacheManager):
        self.base_manager = base_manager
        self.analysis_cache_prefix = "fictionality:analysis:"
        self.content_cache_prefix = "fictionality:content:"
        self.strategy_cache_prefix = "fictionality:strategies:"

    async def hash_content(self, content: str, algorithm: str = "sha256") -> str:
        """
        Generate hash for content deduplication

        Args:
            content: Content to hash
            algorithm: Hash algorithm to use

        Returns:
            str: Content hash
        """
        hasher = hashlib.new(algorithm)
        hasher.update(content.encode("utf-8"))
        return hasher.hexdigest()[:16]  # Truncate for efficiency

    async def cache_fictionality_analysis(self, content: str, analysis: Dict[str, Any], ttl: int = 3600) -> str:
        """
        Cache fictionality analysis with content hash

        Args:
            content: Original content
            analysis: Analysis result
            ttl: Time to live in seconds

        Returns:
            str: Cache key
        """
        content_hash = await self.hash_content(content)
        cache_key = f"{self.analysis_cache_prefix}{content_hash}"

        await self.base_manager.set(cache_key, analysis, ttl=ttl)
        return cache_key

    async def get_fictionality_analysis(self, content: str) -> Optional[Dict[str, Any]]:
        """
        Get cached fictionality analysis by content

        Args:
            content: Content to lookup

        Returns:
            Optional[Dict[str, Any]]: Cached analysis or None
        """
        content_hash = await self.hash_content(content)
        cache_key = f"{self.analysis_cache_prefix}{content_hash}"
        return await self.base_manager.get(cache_key)

    async def cache_content_hash_mapping(self, content: str, hash_value: str) -> None:
        """
        Cache content to hash mapping

        Args:
            content: Original content
            hash_value: Generated hash
        """
        content_key = f"{self.content_cache_prefix}map:{hash_value}"
        await self.base_manager.set(
            content_key, {"content": content, "hash": hash_value}, ttl=86400  # 24 hours for content mappings
        )

    async def get_cached_content_by_hash(self, hash_value: str) -> Optional[str]:
        """
        Get cached content by hash

        Args:
            hash_value: Content hash

        Returns:
            Optional[str]: Cached content or None
        """
        content_key = f"{self.content_cache_prefix}map:{hash_value}"
        cached_data = await self.base_manager.get(content_key)
        return cached_data.get("content") if cached_data else None

    async def clear_fictionality_cache(self, pattern: str = "*") -> int:
        """
        Clear fictionality cache entries matching pattern

        Args:
            pattern: Cache key pattern

        Returns:
            int: Number of entries cleared
        """
        total_cleared = 0

        # Clear analysis cache
        analysis_pattern = f"{self.analysis_cache_prefix}{pattern}"
        total_cleared += await self.base_manager.clear_pattern(analysis_pattern)

        # Clear content cache
        content_pattern = f"{self.content_cache_prefix}{pattern}"
        total_cleared += await self.base_manager.clear_pattern(content_pattern)

        # Clear strategy cache
        strategy_pattern = f"{self.strategy_cache_prefix}{pattern}"
        total_cleared += await self.base_manager.clear_pattern(strategy_pattern)

        return total_cleared

    async def get_fictionality_cache_stats(self) -> Dict[str, Any]:
        """
        Get fictionality-specific cache statistics

        Returns:
            Dict[str, Any]: Fictionality cache statistics
        """
        try:
            # Get base Redis stats
            base_stats = await self.base_manager.get_stats()

            # Estimate fictionality cache size by counting keys
            analysis_keys = await self.base_manager._redis.keys(f"{self.analysis_cache_prefix}*")
            content_keys = await self.base_manager._redis.keys(f"{self.content_cache_prefix}*")
            strategy_keys = await self.base_manager._redis.keys(f"{self.strategy_cache_prefix}*")

            return {
                **base_stats,
                "fictionality_specific": {
                    "analysis_cache_size": len(analysis_keys),
                    "content_cache_size": len(content_keys),
                    "strategy_cache_size": len(strategy_keys),
                    "total_fictionality_entries": len(analysis_keys) + len(content_keys) + len(strategy_keys),
                },
            }
        except Exception as e:
            return {"error": str(e)}


# Global cache manager instance
cache_manager = CacheManager()

# Global fictionality cache manager instance
fictionality_cache_manager = FictionalityCacheManager(cache_manager)
