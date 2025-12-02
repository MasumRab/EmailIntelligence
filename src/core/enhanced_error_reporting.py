import logging
from enum import Enum

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    UNCATEGORIZED = "uncategorized"
    DATABASE = "database"
    API = "api"
    AI_MODEL = "ai_model"

def log_error(e: Exception, message: str = "An error occurred", severity: ErrorSeverity = ErrorSeverity.MEDIUM, category: ErrorCategory = ErrorCategory.UNCATEGORIZED):
    logger.error(f"[{severity.value.upper()}/{category.value.upper()}] {message}: {e}", exc_info=True)

def create_error_context(error: Exception, message: str, severity: ErrorSeverity, category: ErrorCategory):
    return {"error": str(error), "message": message, "severity": severity.value, "category": category.value}

class EnhancedErrorReporting:
    pass
