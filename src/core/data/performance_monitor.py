import time
from functools import wraps

def log_performance(operation=None):
    """
    A decorator to log the performance of a function, with an optional operation name.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            op_name = operation or func.__name__
            print(f"Operation {op_name} took {end_time - start_time:.2f} seconds to execute.")
            return result
        return wrapper
    # This allows the decorator to be used with or without arguments
    if callable(operation):
        return decorator(operation)
    return decorator
