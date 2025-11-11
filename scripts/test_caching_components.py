#!/usr/bin/env python3
"""
Simple test script for the enhanced caching components.
"""

import asyncio
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.enhanced_caching import EnhancedCachingManager, LRUCache, QueryResultCache

async def test_enhanced_caching_components():
    """Test the enhanced caching components directly."""
    print("Testing enhanced caching components...")

    # Test LRUCache
    print("Testing LRUCache...")
    lru_cache = LRUCache(capacity=3)

    # Add items
    lru_cache.put("key1", "value1")
    lru_cache.put("key2", "value2")
    lru_cache.put("key3", "value3")

    # Retrieve items
    assert lru_cache.get("key1") == "value1"
    assert lru_cache.get("key2") == "value2"
    assert lru_cache.get("key3") == "value3"

    # Add one more item to trigger eviction
    lru_cache.put("key4", "value4")

    # First item should be evicted
    assert lru_cache.get("key1") is None
    assert lru_cache.get("key4") == "value4"

    # Check stats
    stats = lru_cache.get_stats()
    assert stats["capacity"] == 3
    assert stats["size"] == 3
    print("LRUCache test passed")

    # Test QueryResultCache
    print("Testing QueryResultCache...")
    query_cache = QueryResultCache(ttl_seconds=1)  # 1 second TTL for testing

    # Add item
    query_cache.put("query1", "result1")

    # Retrieve item
    assert query_cache.get("query1") == "result1"

    # Wait for expiration
    await asyncio.sleep(1.1)

    # Item should be expired
    assert query_cache.get("query1") is None

    # Check stats
    stats = query_cache.get_stats()
    print("QueryResultCache test passed")

    # Test EnhancedCachingManager
    print("Testing EnhancedCachingManager...")
    caching_manager = EnhancedCachingManager()

    # Test email record caching
    email_record = {"id": 1, "subject": "Test Email", "content": "Test content"}
    caching_manager.put_email_record(1, email_record)

    # Retrieve from cache
    cached_record = caching_manager.get_email_record(1)
    assert cached_record == email_record

    # Test cache invalidation
    caching_manager.invalidate_email_record(1)
    assert caching_manager.get_email_record(1) is None

    # Test query result caching
    query_result = [{"id": 1, "subject": "Email 1"}, {"id": 2, "subject": "Email 2"}]
    caching_manager.put_query_result("search:test", query_result)

    # Retrieve from cache
    cached_result = caching_manager.get_query_result("search:test")
    assert cached_result == query_result

    # Test content caching
    content = {"content": "This is the full email content", "attachments": []}
    caching_manager.put_email_content(1, content)

    # Retrieve from cache
    cached_content = caching_manager.get_email_content(1)
    assert cached_content == content

    # Test cache statistics
    stats = caching_manager.get_cache_statistics()
    print(f"Cache statistics: {stats}")

    print("EnhancedCachingManager test passed")
    print("All enhanced caching components working correctly!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_caching_components())