"""
<<<<<<< HEAD
Core exceptions for EmailIntelligence CLI

This module defines custom exceptions used throughout the system.
"""


class EmailIntelligenceException(Exception):
    """Base exception for all EmailIntelligence CLI exceptions."""
    pass


class ConflictDetectionError(EmailIntelligenceException):
    """Raised when conflict detection fails."""
    pass


class ConstitutionalAnalysisError(EmailIntelligenceException):
    """Raised when constitutional analysis fails."""
    pass


class ResolutionStrategyError(EmailIntelligenceException):
    """Raised when resolution strategy generation fails."""
    pass


class ValidationError(EmailIntelligenceException):
    """Raised when validation fails."""
    pass


class ConfigurationError(EmailIntelligenceException):
    """Raised when configuration is invalid."""
    pass


class GitOperationError(EmailIntelligenceException):
    """Raised when git operations fail."""
    pass


class ResourceNotFoundError(EmailIntelligenceException):
    """Raised when a required resource is not found."""
    pass


class PermissionError(EmailIntelligenceException):
    """Raised when an operation lacks required permissions."""
    pass
=======
Custom exceptions for the Email Intelligence Platform.
"""


class BaseAppException(Exception):
    """Base exception class for the application."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class DatabaseError(BaseAppException):
    """Exception for database related errors."""

    def __init__(self, detail: str = "A database error occurred."):
        super().__init__(status_code=503, detail=detail)


class AIAnalysisError(BaseAppException):
    """Exception for AI analysis related errors."""

    def __init__(self, detail: str = "An error occurred during AI analysis."):
        super().__init__(status_code=500, detail=detail)


class GmailServiceError(BaseAppException):
    """Exception for Gmail service related errors."""

    def __init__(
        self, detail: str = "An error occurred with the Gmail service.", status_code: int = 502
    ):
        super().__init__(status_code=status_code, detail=detail)
>>>>>>> origin/main
