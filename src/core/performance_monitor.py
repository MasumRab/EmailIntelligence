import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_performance(operation=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            op = operation or func.__name__
            logger.info(f"Performance: {op} took {duration:.4f} seconds.")
            return result
        return wrapper
    return decorator
