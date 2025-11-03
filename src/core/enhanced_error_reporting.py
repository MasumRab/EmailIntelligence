"""
Enhanced Error Reporting for Email Intelligence Platform

This module provides enhanced error reporting capabilities with structured logging,
error context information, and error analytics to help diagnose issues more effectively.
"""

import asyncio
import json
import logging
import sys
import traceback
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union

# Configure logger for this module
logger = logging.getLogger(__name__)

ERROR_LOG_FILE = "error_log.jsonl"


class ErrorSeverity(Enum):
    """Error severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Categories of errors."""
    VALIDATION = "validation"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    SECURITY = "security"
    DATA = "data"
    NETWORK = "network"
    UNKNOWN = "unknown"


class ErrorContext:
    """Context information for errors."""
    
    def __init__(self):
        self.user_id: Optional[str] = None
        self.session_id: Optional[str] = None
        self.request_id: Optional[str] = None
        self.component: Optional[str] = None
        self.operation: Optional[str] = None
        self.additional_context: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return {
            "user_id": self.user_id,
            "session_id": self.session_id,
            "request_id": self.request_id,
            "component": self.component,
            "operation": self.operation,
            "additional_context": self.additional_context
        }


class EnhancedErrorReporter:
    """Enhanced error reporting system with structured logging and analytics."""
    
    def __init__(self):
        self.error_log_file = ERROR_LOG_FILE
        self._ensure_log_file_exists()
        
        # Error statistics
        self.error_counts: Dict[str, int] = {}
        self.error_categories: Dict[str, int] = {}
        self.error_components: Dict[str, int] = {}
    
    def _ensure_log_file_exists(self):
        """Ensure the error log file exists."""
        try:
            with open(self.error_log_file, "a"):
                pass
        except Exception as e:
            logger.warning(f"Failed to create error log file: {e}")
    
    def log_error(
        self,
        error: Union[Exception, str],
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        context: Optional[ErrorContext] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log an error with structured information.
        
        Args:
            error: The error or error message to log
            severity: The severity level of the error
            category: The category of the error
            context: Context information about the error
            details: Additional details about the error
        
        Returns:
            A unique error ID
        """
        error_id = f"err_{datetime.now(timezone.utc).timestamp():.0f}_{id(error)}"
        
        # Create error entry
        error_entry = {
            "error_id": error_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "severity": severity.value,
            "category": category.value,
            "message": str(error) if not isinstance(error, str) else error,
            "type": type(error).__name__ if not isinstance(error, str) else "StringError",
            "context": context.to_dict() if context else {},
            "details": details or {}
        }
        
        # Add traceback if it's an exception
        if isinstance(error, Exception):
            error_entry["traceback"] = traceback.format_exception(type(error), error, error.__traceback__)
        
        # Log to file
        try:
            with open(self.error_log_file, "a") as f:
                f.write(json.dumps(error_entry) + "\n")
        except Exception as e:
            logger.warning(f"Failed to write error to log: {e}")
        
        # Update statistics
        self._update_error_stats(error_entry)
        
        # Log to standard logger
        logger.log(
            getattr(logging, severity.value.upper(), logging.ERROR),
            f"Error {error_id}: {error_entry['message']}",
            extra={"error_id": error_id}
        )
        
        return error_id
    
    def _update_error_stats(self, error_entry: Dict[str, Any]) -> None:
        """Update error statistics."""
        # Update error type counts
        error_type = error_entry.get("type", "Unknown")
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Update error category counts
        category = error_entry.get("category", "unknown")
        self.error_categories[category] = self.error_categories.get(category, 0) + 1
        
        # Update component counts
        component = error_entry.get("context", {}).get("component", "unknown")
        self.error_components[component] = self.error_components.get(component, 0) + 1
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get current error statistics."""
        return {
            "error_counts": self.error_counts,
            "error_categories": self.error_categories,
            "error_components": self.error_components
        }
    
    def get_recent_errors(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent errors from the log."""
        errors = []
        
        try:
            with open(self.error_log_file, "r") as f:
                lines = f.readlines()
                # Get last 'limit' errors
                lines = lines[-limit:]
                
                for line in lines:
                    try:
                        error_data = json.loads(line.strip())
                        errors.append(error_data)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            logger.warning(f"Failed to read error log: {e}")
        
        return errors
    
    def get_errors_by_category(self, category: ErrorCategory) -> List[Dict[str, Any]]:
        """Get errors by category."""
        all_errors = self.get_recent_errors()
        return [error for error in all_errors if error.get("category") == category.value]
    
    def get_errors_by_severity(self, severity: ErrorSeverity) -> List[Dict[str, Any]]:
        """Get errors by severity."""
        all_errors = self.get_recent_errors()
        return [error for error in all_errors if error.get("severity") == severity.value]


# Global enhanced error reporter instance
enhanced_error_reporter = EnhancedErrorReporter()


def log_error(
    error: Union[Exception, str],
    severity: ErrorSeverity = ErrorSeverity.ERROR,
    category: ErrorCategory = ErrorCategory.UNKNOWN,
    context: Optional[ErrorContext] = None,
    details: Optional[Dict[str, Any]] = None
) -> str:
    """
    Log an error with structured information.
    
    Args:
        error: The error or error message to log
        severity: The severity level of the error
        category: The category of the error
        context: Context information about the error
        details: Additional details about the error
    
    Returns:
        A unique error ID
    """
    return enhanced_error_reporter.log_error(error, severity, category, context, details)


def create_error_context(
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    request_id: Optional[str] = None,
    component: Optional[str] = None,
    operation: Optional[str] = None,
    additional_context: Optional[Dict[str, Any]] = None
) -> ErrorContext:
    """Create an error context object."""
    context = ErrorContext()
    context.user_id = user_id
    context.session_id = session_id
    context.request_id = request_id
    context.component = component
    context.operation = operation
    context.additional_context = additional_context or {}
    return context


def get_error_statistics() -> Dict[str, Any]:
    """Get current error statistics."""
    return enhanced_error_reporter.get_error_stats()


def get_recent_errors(limit: int = 100) -> List[Dict[str, Any]]:
    """Get recent errors from the log."""
    return enhanced_error_reporter.get_recent_errors()


def get_errors_by_category(category: ErrorCategory) -> List[Dict[str, Any]]:
    """Get errors by category."""
    return enhanced_error_reporter.get_errors_by_category(category)


def get_errors_by_severity(severity: ErrorSeverity) -> List[Dict[str, Any]]:
    """Get errors by severity."""
    return enhanced_error_reporter.get_errors_by_severity(severity)
# Alias for backward compatibility
ErrorReporter = EnhancedErrorReporter
