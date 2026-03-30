import asyncio
from src.core.caching import CacheConfig, MemoryCacheBackend

async def test_cache():
    config = CacheConfig(max_memory_items=3)
    cache = MemoryCacheBackend(config)

    await cache.set("a", 1)
    await cache.set("b", 2)
    await cache.set("c", 3)
    print("after 3 inserts:", cache._cache.keys())

    await cache.get("a") # access 'a', moves to end
    print("after access 'a':", cache._cache.keys())

    await cache.set("d", 4) # should evict 'b'
    print("after insert 'd':", cache._cache.keys())

    assert await cache.get("a") == 1
    assert await cache.get("b") is None
    assert await cache.get("c") == 3
    assert await cache.get("d") == 4
    print("Test passed!")

asyncio.run(test_cache())
