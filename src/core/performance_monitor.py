def log_performance(operation=None):
    def decorator(func):
        return func
    if callable(operation):
        return decorator(operation)
    return decorator
