"""
Custom exceptions for the Email Intelligence Platform.
Standardized error handling with consistent error codes and structures.
"""

from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel, Field


class APIError(BaseModel):
    """Standardized API Error response model.
    
    Provides consistent error response structure across all API endpoints.
    Includes request tracking for debugging and monitoring.
    """
    success: bool = Field(default=False, description="Indicates if the operation succeeded")
    message: str = Field(..., description="Human-readable error message")
    error_code: str = Field(..., description="Machine-readable error code for programmatic handling")
    details: Optional[str] = Field(None, description="Additional error details or context")
    request_id: Optional[str] = Field(None, description="Unique identifier for request tracking")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "Email with ID 123 not found",
                "error_code": "EMAIL_NOT_FOUND",
                "details": "The email may have been deleted or you may not have access",
                "request_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class BaseAppException(HTTPException):
    """Base application exception with standardized structure.
    
    Extends FastAPI's HTTPException to provide:
    - Consistent error response format via APIError model
    - Error codes for programmatic handling
    - Request tracking for debugging
    - Backward compatibility with existing code
    """
    
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str = "GENERAL_ERROR",
        details: Optional[str] = None,
        request_id: Optional[str] = None,
    ):
        """
        Initialize the exception.
        
        Args:
            status_code: HTTP status code for the error
            message: Human-readable error message
            error_code: Machine-readable error code (default: GENERAL_ERROR)
            details: Additional error details or context
            request_id: Unique identifier for request tracking
        """
        error_response = APIError(
            success=False,
            message=message,
            error_code=error_code,
            details=details,
            request_id=request_id
        )
        super().__init__(
            status_code=status_code,
            detail=error_response.model_dump()
        )
        
        # Store attributes for programmatic access
        self.error_code = error_code
        self.request_id = request_id


class EmailNotFoundException(BaseAppException):
    """Raised when an email is not found."""
    
    def __init__(
        self,
        email_id: int = None,
        message_id: str = None,
        request_id: Optional[str] = None
    ):
        """
        Initialize the exception.
        
        Args:
            email_id: Internal email ID
            message_id: Gmail message ID
            request_id: Request tracking ID
        """
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
    """Raised when a category is not found."""
    
    def __init__(self, category_id: int, request_id: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"Category with ID {category_id} not found",
            error_code="CATEGORY_NOT_FOUND",
            request_id=request_id
        )


class ValidationError(BaseAppException):
    """Raised when validation fails."""
    
    def __init__(
        self,
        message: str,
        details: Optional[str] = None,
        request_id: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_code="VALIDATION_ERROR",
            details=details,
            request_id=request_id
        )


class DatabaseError(BaseAppException):
    """Raised when a database operation fails."""
    
    def __init__(
        self,
        message: str = "A database error occurred.",
        details: Optional[str] = None,
        request_id: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_code="DATABASE_ERROR",
            details=details,
            request_id=request_id
        )


class UnauthorizedException(BaseAppException):
    """Raised when authentication/authorization fails."""
    
    def __init__(
        self,
        message: str = "Unauthorized access",
        request_id: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code="UNAUTHORIZED",
            request_id=request_id
        )


class ForbiddenException(BaseAppException):
    """Raised when access is forbidden."""
    
    def __init__(
        self,
        message: str = "Access forbidden",
        request_id: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error_code="FORBIDDEN",
            request_id=request_id
        )


class AIAnalysisError(BaseAppException):
    """Raised when AI analysis fails."""
    
    def __init__(
        self,
        detail: str = "An error occurred during AI analysis.",
        request_id: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=detail,
            error_code="AI_ANALYSIS_ERROR",
            request_id=request_id
        )


class GmailServiceError(BaseAppException):
    """Raised when Gmail service operations fail."""
    
    def __init__(
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