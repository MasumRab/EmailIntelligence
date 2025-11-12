"""
Caching Framework for Email Intelligence Platform

Implements distributed caching with Redis support for multi-instance deployments,
along with cache warming, invalidation, and monitoring capabilities.
"""

import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set

try:
    import redis.asyncio as redis

    REDIS_AVAILABLE = True
except ImportError:
    redis = None
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)


class CacheBackend(Enum):
    """Supported cache backends"""

    MEMORY = "memory"
    REDIS = "redis"


class CacheStrategy(Enum):
    """Cache invalidation strategies"""

    LRU = "lru"
    TTL = "ttl"
    TAGS = "tags"


@dataclass
class CacheConfig:
    """Configuration for cache backends"""

    backend: CacheBackend = CacheBackend.MEMORY
    redis_url: Optional[str] = None
    redis_db: int = 0
    max_memory_items: int = 10000
    default_ttl: int = 3600  # 1 hour
    enable_monitoring: bool = True


@dataclass
class CacheStats:
    """Cache performance statistics"""

    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    evictions: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class CacheBackendInterface(ABC):
    """Abstract interface for cache backends"""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL"""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        pass

    @abstractmethod
    async def clear(self) -> bool:
        """Clear all cache entries"""
        pass

    @abstractmethod
    async def get_stats(self) -> CacheStats:
        """Get cache statistics"""
        pass


class MemoryCacheBackend(CacheBackendInterface):
    """In-memory cache backend using LRU strategy"""

    def __init__(self, config: CacheConfig):
        self.config = config
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_order: List[str] = []
        self._stats = CacheStats()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from memory cache"""
        if key in self._cache:
            entry = self._cache[key]
            # Check TTL
            if entry.get("expires_at") and time.time() > entry["expires_at"]:
                await self.delete(key)
                self._stats.misses += 1
                return None

            # Update access order for LRU
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)

            self._stats.hits += 1
            return entry["value"]
        else:
            self._stats.misses += 1
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in memory cache"""
        expires_at = time.time() + ttl if ttl else None

        self._cache[key] = {
            "value": value,
            "expires_at": expires_at,
            "created_at": time.time(),
        }

        # Update access order
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)

        # Enforce max items limit (LRU eviction)
        while len(self._cache) > self.config.max_memory_items:
            oldest_key = self._access_order.pop(0)
            if oldest_key in self._cache:
                del self._cache[oldest_key]
                self._stats.evictions += 1

        self._stats.sets += 1
        return True

    async def delete(self, key: str) -> bool:
        """Delete value from memory cache"""
        if key in self._cache:
            del self._cache[key]
            if key in self._access_order:
                self._access_order.remove(key)
            self._stats.deletes += 1
            return True
        return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in memory cache"""
        if key in self._cache:
            entry = self._cache[key]
            if entry.get("expires_at") and time.time() > entry["expires_at"]:
                await self.delete(key)
                return False
            return True
        return False

    async def clear(self) -> bool:
        """Clear all memory cache entries"""
        self._cache.clear()
        self._access_order.clear()
        return True

    async def get_stats(self) -> CacheStats:
        """Get memory cache statistics"""
        return self._stats


class RedisCacheBackend(CacheBackendInterface):
    """Redis-based distributed cache backend"""

    def __init__(self, config: CacheConfig):
        if not REDIS_AVAILABLE:
            raise ImportError(
                "Redis is not available. Install redis-py to use Redis caching."
            )

        self.config = config
        self._redis: Optional[redis.Redis] = None
        self._stats = CacheStats()

    async def _ensure_connection(self):
        """Ensure Redis connection is established"""
        if self._redis is None:
            self._redis = redis.Redis.from_url(
                self.config.redis_url or "redis://localhost:6379",
                db=self.config.redis_db,
                decode_responses=True,
            )

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache"""
        await self._ensure_connection()
        try:
            value = await self._redis.get(key)
            if value is not None:
                self._stats.hits += 1
                return json.loads(value)
            else:
                self._stats.misses += 1
                return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            self._stats.misses += 1
            return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in Redis cache"""
        await self._ensure_connection()
        try:
            json_value = json.dumps(value)
            ttl_value = ttl or self.config.default_ttl
            result = await self._redis.setex(key, ttl_value, json_value)
            self._stats.sets += 1
            return bool(result)
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete value from Redis cache"""
        await self._ensure_connection()
        try:
            result = await self._redis.delete(key)
            self._stats.deletes += 1
            return bool(result)
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis cache"""
        await self._ensure_connection()
        try:
            return bool(await self._redis.exists(key))
        except Exception as e:
            logger.error(f"Redis exists error: {e}")
            return False

    async def clear(self) -> bool:
        """Clear all Redis cache entries"""
        await self._ensure_connection()
        try:
            await self._redis.flushdb()
            return True
        except Exception as e:
            logger.error(f"Redis clear error: {e}")
            return False

    async def get_stats(self) -> CacheStats:
        """Get Redis cache statistics"""
        # Redis doesn't provide hit/miss stats directly, so we track our own
        return self._stats


class CacheManager:
    """
    Unified cache manager supporting multiple backends and strategies
    """

    def __init__(self, config: CacheConfig):
        self.config = config
        self.backend: CacheBackendInterface = self._create_backend()
        self._tags: Dict[str, Set[str]] = {}  # tag -> set of keys
        self._warming_tasks: Set[str] = set()

    def _create_backend(self) -> CacheBackendInterface:
        """Create the appropriate cache backend"""
        if self.config.backend == CacheBackend.REDIS:
            return RedisCacheBackend(self.config)
        else:
            return MemoryCacheBackend(self.config)

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        return await self.backend.get(key)

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """Set value in cache with optional tags"""
        success = await self.backend.set(key, value, ttl)

        if success and tags:
            for tag in tags:
                if tag not in self._tags:
                    self._tags[tag] = set()
                self._tags[tag].add(key)

        return success

    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        success = await self.backend.delete(key)

        if success:
            # Remove from tag sets
            for tag_keys in self._tags.values():
                tag_keys.discard(key)

        return success

    async def invalidate_tags(self, tags: List[str]) -> int:
        """Invalidate all keys with given tags"""
        keys_to_delete = set()
        for tag in tags:
            if tag in self._tags:
                keys_to_delete.update(self._tags[tag])

        deleted_count = 0
        for key in keys_to_delete:
            if await self.delete(key):
                deleted_count += 1

        return deleted_count

    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return await self.backend.exists(key)

    async def clear(self) -> bool:
        """Clear all cache entries"""
        self._tags.clear()
        return await self.backend.clear()

    async def get_stats(self) -> CacheStats:
        """Get cache statistics"""
        return await self.backend.get_stats()

    async def warm_cache(self, warming_func, key_prefix: str = "warm"):
        """
        Warm cache with background task

        Args:
            warming_func: Async function that returns dict of key->value pairs to cache
            key_prefix: Prefix for warming task identification
        """
        task_id = f"{key_prefix}_{time.time()}"
        if task_id in self._warming_tasks:
            return  # Already warming

        self._warming_tasks.add(task_id)

        try:
            # Run warming in background
            asyncio.create_task(self._do_warming(warming_func, task_id))
        except Exception as e:
            logger.error(f"Failed to start cache warming: {e}")
            self._warming_tasks.discard(task_id)

    async def _do_warming(self, warming_func, task_id: str):
        """Execute cache warming"""
        try:
            data = await warming_func()
            for key, value in data.items():
                await self.set(key, value)
            logger.info(f"Cache warming completed for {len(data)} items")
        except Exception as e:
            logger.error(f"Cache warming failed: {e}")
        finally:
            self._warming_tasks.discard(task_id)


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        # Default to memory cache
        config = CacheConfig()
        _cache_manager = CacheManager(config)
    return _cache_manager


def init_cache_manager(config: CacheConfig) -> CacheManager:
    """Initialize the global cache manager with configuration"""
    global _cache_manager
    _cache_manager = CacheManager(config)
    return _cache_manager
