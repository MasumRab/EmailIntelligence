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
            op_name = operation if operation else func.__name__
            logger.info(f"Performance: {op_name} took {end_time - start_time:.4f} seconds.")
            return result
        return wrapper
    if callable(operation):
        return decorator(operation)
    return decorator
