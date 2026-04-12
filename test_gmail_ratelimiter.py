import asyncio
import time
from collections import deque
from src.backend.python_nlp.gmail_integration import RateLimiter, RateLimitConfig

async def test_gmail_ratelimiter():
    config = RateLimitConfig(queries_per_second=10, queries_per_100_seconds=250)
    limiter = RateLimiter(config)

    print("Testing gmail ratelimiter...")
    for i in range(10000):
        # We simulate the passing of time, since the limiter relies on `time.time()`
        limiter.request_times.append(time.time() - 200) # This makes it keep adding items

    print(f"Items in request_times: {len(limiter.request_times)}")

    # We call acquire. It should clear items older than 100 seconds.
    await limiter.acquire()

    print(f"Items in request_times after acquire: {len(limiter.request_times)}")

if __name__ == "__main__":
    asyncio.run(test_gmail_ratelimiter())
