"""
Custom exceptions for the Email Intelligence Platform.
<<<<<<< HEAD
Standardized error handling with consistent error codes and structures.
"""

from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel


class APIError(BaseModel):
    """Standardized API Error response model"""

    success: bool = False
    message: str
    error_code: str
    details: Optional[str] = None
    request_id: Optional[str] = None  # To track specific requests


class BaseAppException(HTTPException):
    """Base application exception with standardized structure"""

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = "GENERAL_ERROR",
        details: Optional[str] = None,
        request_id: Optional[str] = None,
    ):
        error_response = APIError(
            success=False, 
            message=message, 
            error_code=error_code, 
            details=details,
            request_id=request_id
        )
        super().__init__(status_code=status_code, detail=error_response.model_dump())


class EmailNotFoundException(BaseAppException):
    """Raised when an email is not found"""

    def __init__(self, email_id: int = None, message_id: str = None, request_id: Optional[str] = None):
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
            status_code=status.HTTP_404_NOT_FOUND, 
            message=message, 
            error_code=error_code,
            request_id=request_id
        )


class CategoryNotFoundException(BaseAppException):
    """Raised when a category is not found"""

    def __init__(self, category_id: int, request_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"Category with ID {category_id} not found",
            error_code="CATEGORY_NOT_FOUND",
            request_id=request_id
        )


class ValidationError(BaseAppException):
    """Raised when validation fails"""

    def __init__(self, message: str, details: Optional[str] = None, request_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_code="VALIDATION_ERROR",
            details=details,
            request_id=request_id
        )


class DatabaseError(BaseAppException):
    """Raised when a database operation fails"""

    def __init__(self, message: str, details: Optional[str] = None, request_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_code="DATABASE_ERROR",
            details=details,
            request_id=request_id
        )


class UnauthorizedException(BaseAppException):
    """Raised when authentication/authorization fails"""

    def __init__(self, message: str = "Unauthorized access", request_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            message=message, 
            error_code="UNAUTHORIZED",
            request_id=request_id
        )


class ForbiddenException(BaseAppException):
    """Raised when access is forbidden"""

    def __init__(self, message: str = "Access forbidden", request_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, 
            message=message, 
            error_code="FORBIDDEN",
            request_id=request_id
        )
=======
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
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2


class AIAnalysisError(BaseAppException):
    """Exception for AI analysis related errors."""

<<<<<<< HEAD
    def __init__(self, detail: str = "An error occurred during AI analysis.", request_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=detail,
            error_code="AI_ANALYSIS_ERROR",
            request_id=request_id
        )
=======
    def __init__(self, detail: str = "An error occurred during AI analysis."):
        super().__init__(status_code=500, detail=detail)
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2


class GmailServiceError(BaseAppException):
    """Exception for Gmail service related errors."""

    def __init__(
<<<<<<< HEAD
        self, 
        detail: str = "An error occurred with the Gmail service.", 
        status_code: int = status.HTTP_502_BAD_GATEWAY,
        request_id: Optional[str] = None
    ):
        super().__init__(
            status_code=status_code,
            message=detail,
            error_code="GMAIL_SERVICE_ERROR",
            request_id=request_id
        )


class WorkflowExecutionError(BaseAppException):
    """Exception for workflow execution related errors."""

    def __init__(self, detail: str = "An error occurred during workflow execution.", request_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=detail,
            error_code="WORKFLOW_EXECUTION_ERROR",
            request_id=request_id
        )


class ModelLoadError(BaseAppException):
    """Exception for model loading related errors."""

    def __init__(self, detail: str = "An error occurred while loading the model.", request_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=detail,
            error_code="MODEL_LOAD_ERROR",
            request_id=request_id
        )
=======
        self, detail: str = "An error occurred with the Gmail service.", status_code: int = 502
    ):
        super().__init__(status_code=status_code, detail=detail)
>>>>>>> 73a8d1727b5a9766467abd3d090470711b0fdcb2
