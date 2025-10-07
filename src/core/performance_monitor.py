import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from functools import wraps

logger = logging.getLogger(__name__)

LOG_FILE = "performance_metrics_log.jsonl"

def log_performance(operation: str):
    """
    A decorator to log the performance of both sync and async functions.
    """
    def decorator(func):
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            duration = end_time - start_time

            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "operation": operation,
                "duration_seconds": duration,
            }

            try:
                with open(LOG_FILE, 'a') as f:
                    f.write(json.dumps(log_entry) + "\n")
            except IOError as e:
                logger.error(f"Failed to write performance log: {e}")

            return result

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            duration = end_time - start_time

            log_entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "operation": operation,
                "duration_seconds": duration,
            }

            try:
                with open(LOG_FILE, 'a') as f:
                    f.write(json.dumps(log_entry) + "\n")
            except IOError as e:
                logger.error(f"Failed to write performance log: {e}")

            return result

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    return decorator