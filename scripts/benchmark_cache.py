import asyncio
import time
import random
import sys
import os

# Add src to path
sys.path.append(os.getcwd())

from src.core.caching import MemoryCacheBackend, CacheConfig

async def benchmark_cache():
    # Setup
    n_items = 10000
    config = CacheConfig(max_memory_items=n_items)
    backend = MemoryCacheBackend(config)

    # Fill cache to limit
    print(f"Filling cache with {n_items} items...")
    start_time = time.time()
    for i in range(n_items):
        await backend.set(f"key_{i}", f"value_{i}")
    fill_time = time.time() - start_time
    print(f"Fill time: {fill_time:.4f}s")

    # Perform random access (get + set to trigger LRU update)
    n_ops = 5000
    print(f"Performing {n_ops} random operations (get/set) on full cache...")
    start_time = time.time()
    for _ in range(n_ops):
        key = f"key_{random.randint(0, n_items-1)}"
        # Get triggers move to end
        await backend.get(key)

        # Set new item triggers eviction since cache is full
        new_key = f"new_key_{random.randint(0, 1000000)}"
        await backend.set(new_key, "value")

    ops_time = time.time() - start_time
    print(f"Operations time: {ops_time:.4f}s")
    print(f"Avg time per op: {ops_time/n_ops*1000:.4f}ms")

if __name__ == "__main__":
    asyncio.run(benchmark_cache())
