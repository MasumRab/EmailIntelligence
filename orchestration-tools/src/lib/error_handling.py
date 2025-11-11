import logging
import uuid
from datetime import datetime
from typing import Optional
from fastapi import HTTPException


class OrchestrationError(Exception):
    """Base exception for orchestration tools"""
    def __init__(self, message: str, error_code: str = "ORCHESTRATION_ERROR", correlation_id: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.timestamp = datetime.now()
        super().__init__(self.message)


class AuthenticationError(OrchestrationError):
    """Exception for authentication failures"""
    def __init__(self, message: str, correlation_id: Optional[str] = None):
        super().__init__(message, "AUTHENTICATION_FAILED", correlation_id)


class AuthorizationError(OrchestrationError):
    """Exception for authorization failures"""
    def __init__(self, message: str, correlation_id: Optional[str] = None):
        super().__init__(message, "INSUFFICIENT_PERMISSIONS", correlation_id)


class ValidationError(OrchestrationError):
    """Exception for validation failures"""
    def __init__(self, message: str, correlation_id: Optional[str] = None):
        super().__init__(message, "INVALID_REQUEST", correlation_id)


class VerificationError(OrchestrationError):
    """Exception for verification failures"""
    def __init__(self, message: str, correlation_id: Optional[str] = None):
        super().__init__(message, "VERIFICATION_FAILED", correlation_id)


class OrchestrationLogger:
    """Structured logging for orchestration tools"""
    
    def __init__(self, name: str = "orchestration"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create console handler if not already present
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s - correlation_id: %(correlation_id)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def _log_with_correlation(self, level: str, message: str, correlation_id: str, **kwargs):
        """Log a message with correlation ID"""
        extra = {'correlation_id': correlation_id}
        extra.update(kwargs)
        
        getattr(self.logger, level)(message, extra=extra)
    
    def info(self, message: str, correlation_id: str, **kwargs):
        """Log an info message with correlation ID"""
        self._log_with_correlation('info', message, correlation_id, **kwargs)
    
    def error(self, message: str, correlation_id: str, **kwargs):
        """Log an error message with correlation ID"""
        self._log_with_correlation('error', message, correlation_id, **kwargs)
    
    def warning(self, message: str, correlation_id: str, **kwargs):
        """Log a warning message with correlation ID"""
        self._log_with_correlation('warning', message, correlation_id, **kwargs)
    
    def debug(self, message: str, correlation_id: str, **kwargs):
        """Log a debug message with correlation ID"""
        self._log_with_correlation('debug', message, correlation_id, **kwargs)


# Global logger instance
logger = OrchestrationLogger()


def handle_exception(exc: Exception, correlation_id: str = None) -> HTTPException:
    """Convert orchestration exceptions to HTTP exceptions"""
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
    
    if isinstance(exc, AuthenticationError):
        logger.error(f"Authentication failed: {exc.message}", correlation_id)
        return HTTPException(
            status_code=401,
            detail={
                "error": exc.message,
                "error_code": exc.error_code,
                "timestamp": exc.timestamp.isoformat(),
                "request_id": correlation_id
            }
        )
    
    elif isinstance(exc, AuthorizationError):
        logger.error(f"Authorization failed: {exc.message}", correlation_id)
        return HTTPException(
            status_code=403,
            detail={
                "error": exc.message,
                "error_code": exc.error_code,
                "timestamp": exc.timestamp.isoformat(),
                "request_id": correlation_id
            }
        )
    
    elif isinstance(exc, ValidationError):
        logger.error(f"Validation failed: {exc.message}", correlation_id)
        return HTTPException(
            status_code=400,
            detail={
                "error": exc.message,
                "error_code": exc.error_code,
                "timestamp": exc.timestamp.isoformat(),
                "request_id": correlation_id
            }
        )
    
    elif isinstance(exc, OrchestrationError):
        logger.error(f"Orchestration error: {exc.message}", correlation_id)
        return HTTPException(
            status_code=500,
            detail={
                "error": exc.message,
                "error_code": exc.error_code,
                "timestamp": exc.timestamp.isoformat(),
                "request_id": correlation_id
            }
        )
    
    else:
        logger.error(f"Unexpected error: {str(exc)}", correlation_id)
        return HTTPException(
            status_code=500,
            detail={
                "error": "An unexpected error occurred",
                "error_code": "INTERNAL_ERROR",
                "timestamp": datetime.now().isoformat(),
                "request_id": correlation_id
            }
        )