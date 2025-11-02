"""
It will be removed in a future release.

Custom exceptions for the Email Intelligence Platform
Provides consistent error handling across the application
"""

from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class APIError(BaseModel):
    """API Error response model"""

    success: bool = False
    message: str
    error_code: str
    details: Optional[str] = None


class AppException(HTTPException):
    """Base application exception"""

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = "GENERAL_ERROR",
        details: Optional[str] = None,
    ):
        error_response = APIError(
            success=False, message=message, error_code=error_code, details=details
        )
        super().__init__(status_code=status_code, detail=error_response.model_dump())


class EmailNotFoundException(AppException):
    """Raised when an email is not found"""

    def __init__(self, email_id: int = None, message_id: str = None):
        if email_id:
            message = f"Email with ID {email_id} not found"
            error_code = "EMAIL_NOT_FOUND"
        elif message_id:
            message = f"Email with message ID {message_id} not found"
            error_code = "EMAIL_NOT_FOUND"
        else:
            message = "Email not found"
            error_code = "EMAIL_NOT_FOUND"

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, message=message, error_code=error_code
        )


class CategoryNotFoundException(AppException):
    """Raised when a category is not found"""

    def __init__(self, category_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"Category with ID {category_id} not found",
            error_code="CATEGORY_NOT_FOUND",
        )


class ValidationError(AppException):
    """Raised when validation fails"""

    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_code="VALIDATION_ERROR",
            details=details,
        )


class DatabaseError(AppException):
    """Raised when a database operation fails"""

    def __init__(self, message: str, details: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_code="DATABASE_ERROR",
            details=details,
        )


class UnauthorizedException(AppException):
    """Raised when authentication/authorization fails"""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, message=message, error_code="UNAUTHORIZED"
        )


class ForbiddenException(AppException):
    """Raised when access is forbidden"""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, message=message, error_code="FORBIDDEN"
        )


class BaseAppException(Exception):
    """Base exception class for the application."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


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
