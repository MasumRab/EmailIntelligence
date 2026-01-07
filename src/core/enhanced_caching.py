"""
Enhanced Caching for Database Manager

This module provides enhanced caching capabilities for the DatabaseManager,
including LRU cache for frequently accessed data and query result caching.
"""

import asyncio
import logging
import time
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class LRUCache:
    """LRU (Least Recently Used) Cache implementation for frequently accessed data."""

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache, marking it as recently used."""
        if key in self.cache:
            # Move to end to mark as recently used
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None

    def put(self, key: str, value: Any) -> None:
        """Put value in cache, evicting oldest if necessary."""
        if key in self.cache:
            # Update existing entry
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            # Remove least recently used item
            self.cache.popitem(last=False)

        self.cache[key] = value

    def invalidate(self, key: str) -> None:
        """Remove a specific key from cache."""
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "capacity": self.capacity,
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate
        }


class QueryResultCache:
    """Cache for query results with TTL (Time To Live) support."""

    def __init__(self, ttl_seconds: int = 300):  # 5 minutes default
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Tuple[Any, float]] = {}  # (value, timestamp)
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                self.hits += 1
                return value
            else:
                # Expired, remove it
                del self.cache[key]
        self.misses += 1
        return None

    def put(self, key: str, value: Any) -> None:
        """Put value in cache with current timestamp."""
        self.cache[key] = (value, time.time())

    def invalidate(self, key: str) -> None:
        """Remove a specific key from cache."""
        if key in self.cache:
            del self.cache[key]

    def clear_expired(self) -> None:
        """Remove all expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp >= self.ttl_seconds
        ]
        for key in expired_keys:
            del self.cache[key]

    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        self.clear_expired()  # Clean up expired entries
        return {
            "size": len(self.cache),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
            "ttl_seconds": self.ttl_seconds
        }


class EnhancedCachingManager:
    """Enhanced caching manager that integrates with DatabaseManager."""

    def __init__(self):
        # LRU cache for frequently accessed individual records
        self.email_record_cache = LRUCache(capacity=200)
        self.category_record_cache = LRUCache(capacity=50)

        # Query result cache for complex queries
        self.query_cache = QueryResultCache(ttl_seconds=300)  # 5 minutes

        # Cache for email content (heavy data)
        self.email_content_cache = LRUCache(capacity=100)

        # Generic cache for other components (like SmartFilterManager)
        self.generic_cache = LRUCache(capacity=500)

        # Statistics tracking
        self.cache_operations = {
            "email_record_get": 0,
            "email_record_put": 0,
            "category_record_get": 0,
            "category_record_put": 0,
            "query_result_get": 0,
            "query_result_put": 0,
            "content_get": 0,
            "content_put": 0,
            "generic_get": 0,
            "generic_put": 0,
            "generic_delete": 0
        }

    def get_email_record(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email record from cache."""
        self.cache_operations["email_record_get"] += 1
        return self.email_record_cache.get(f"email_{email_id}")

    def put_email_record(self, email_id: int, email_record: Dict[str, Any]) -> None:
        """Put email record in cache."""
        self.cache_operations["email_record_put"] += 1
        self.email_record_cache.put(f"email_{email_id}", email_record)

    def get_category_record(self, category_id: int) -> Optional[Dict[str, Any]]:
        """Get category record from cache."""
        self.cache_operations["category_record_get"] += 1
        return self.category_record_cache.get(f"category_{category_id}")

    def put_category_record(self, category_id: int, category_record: Dict[str, Any]) -> None:
        """Put category record in cache."""
        self.cache_operations["category_record_put"] += 1
        self.category_record_cache.put(f"category_{category_id}", category_record)

    def get_query_result(self, query_key: str) -> Optional[Any]:
        """Get query result from cache."""
        self.cache_operations["query_result_get"] += 1
        return self.query_cache.get(query_key)

    def put_query_result(self, query_key: str, result: Any) -> None:
        """Put query result in cache."""
        self.cache_operations["query_result_put"] += 1
        self.query_cache.put(query_key, result)

    def get_email_content(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email content from cache."""
        self.cache_operations["content_get"] += 1
        return self.email_content_cache.get(f"content_{email_id}")

    def put_email_content(self, email_id: int, content: Dict[str, Any]) -> None:
        """Put email content in cache."""
        self.cache_operations["content_put"] += 1
        self.email_content_cache.put(f"content_{email_id}", content)

    def invalidate_email_record(self, email_id: int) -> None:
        """Invalidate email record cache."""
        self.email_record_cache.invalidate(f"email_{email_id}")
        self.email_content_cache.invalidate(f"content_{email_id}")

    def invalidate_category_record(self, category_id: int) -> None:
        """Invalidate category record cache."""
        self.category_record_cache.invalidate(f"category_{category_id}")

    def invalidate_query_result(self, query_key: str) -> None:
        """Invalidate query result cache."""
        self.query_cache.invalidate(query_key)

    # --- Async Compatibility Methods for SmartFilterManager ---

    async def _ensure_initialized(self):
        """Ensure the caching manager is initialized (async compatibility)."""
        pass

    async def close(self):
        """Close the caching manager (async compatibility)."""
        self.clear_all_caches()

    async def get(self, key: str) -> Optional[Any]:
        """Generic async get for SmartFilterManager compatibility."""
        self.cache_operations["generic_get"] += 1
        return self.generic_cache.get(key)

    async def set(self, key: str, value: Any) -> None:
        """Generic async set for SmartFilterManager compatibility."""
        self.cache_operations["generic_put"] += 1
        self.generic_cache.put(key, value)

    async def delete(self, key: str) -> None:
        """Generic async delete for SmartFilterManager compatibility."""
        self.cache_operations["generic_delete"] += 1
        self.generic_cache.invalidate(key)

    # ---------------------------------------------------------

    def clear_all_caches(self) -> None:
        """Clear all caches."""
        self.email_record_cache.clear()
        self.category_record_cache.clear()
        self.query_cache.clear()
        self.email_content_cache.clear()
        self.generic_cache.clear()

        # Reset statistics
        for key in self.cache_operations:
            self.cache_operations[key] = 0

    def get_cache_statistics(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics."""
        return {
            "email_record_cache": self.email_record_cache.get_stats(),
            "category_record_cache": self.category_record_cache.get_stats(),
            "query_cache": self.query_cache.get_stats(),
            "email_content_cache": self.email_content_cache.get_stats(),
            "generic_cache": self.generic_cache.get_stats(),
            "operations": self.cache_operations.copy()
        }
