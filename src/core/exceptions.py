"""
Custom exceptions for the Email Intelligence Platform.
"""

from typing import Optional


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
        self,
        detail: str = "An error occurred with the Gmail service.",
        status_code: int = 502,
    ):
        super().__init__(status_code=status_code, detail=detail)


class EmailNotFoundException(BaseAppException):
    """Exception raised when an email is not found."""

    def __init__(self, email_id: Optional[str] = None, message: Optional[str] = None):
        self.email_id = email_id
        if message:
            detail = message
        elif email_id:
            detail = f"Email not found: {email_id}"
        else:
            detail = "Email not found"
        super().__init__(status_code=404, detail=detail)
