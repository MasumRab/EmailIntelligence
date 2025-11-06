
def log_error(e, severity, category, context, details):
    pass

def create_error_context(component, operation, additional_context):
    pass

class ErrorSeverity:
    WARNING = "warning"
    ERROR = "error"

class ErrorCategory:
    DATA = "data"
    VALIDATION = "validation"
