"""
Tests for the enhanced exception system.
"""

import pytest
from fastapi import status
from src.core.exceptions import (
    APIError,
    BaseAppException,
    EmailNotFoundException,
    CategoryNotFoundException,
    ValidationError,
    DatabaseError,
    UnauthorizedException,
    ForbiddenException,
    AIAnalysisError,
    GmailServiceError
)


class TestAPIError:
    """Test APIError model."""
    
    def test_api_error_creation(self):
        """Test creating APIError with all fields."""
        error = APIError(
            success=False,
            message="Test error",
            error_code="TEST_ERROR",
            details="Test details",
            request_id="test-request-id"
        )
        assert error.success is False
        assert error.message == "Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.details == "Test details"
        assert error.request_id == "test-request-id"
    
    def test_api_error_defaults(self):
        """Test APIError with default values."""
        error = APIError(
            message="Test error",
            error_code="TEST_ERROR"
        )
        assert error.success is False
        assert error.details is None
        assert error.request_id is None


class TestBaseAppException:
    """Test BaseAppException."""
    
    def test_base_exception_creation(self):
        """Test creating BaseAppException."""
        exc = BaseAppException(
            status_code=500,
            message="Test error",
            error_code="TEST_ERROR",
            details="Test details",
            request_id="test-request-id"
        )
        assert exc.status_code == 500
        assert exc.error_code == "TEST_ERROR"
        assert exc.request_id == "test-request-id"
        assert "success" in exc.detail
        assert exc.detail["success"] is False
    
    def test_base_exception_defaults(self):
        """Test BaseAppException with defaults."""
        exc = BaseAppException(
            status_code=500,
            message="Test error"
        )
        assert exc.error_code == "GENERAL_ERROR"
        assert exc.request_id is None


class TestEmailNotFoundException:
    """Test EmailNotFoundException."""
    
    def test_with_email_id(self):
        """Test exception with email ID."""
        exc = EmailNotFoundException(email_id=123)
        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert exc.error_code == "EMAIL_NOT_FOUND"
        assert "123" in exc.detail["message"]
    
    def test_with_message_id(self):
        """Test exception with message ID."""
        exc = EmailNotFoundException(message_id="msg123")
        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert exc.error_code == "EMAIL_NOT_FOUND"
        assert "msg123" in exc.detail["message"]
    
    def test_without_ids(self):
        """Test exception without IDs."""
        exc = EmailNotFoundException()
        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert exc.error_code == "EMAIL_NOT_FOUND"


class TestCategoryNotFoundException:
    """Test CategoryNotFoundException."""
    
    def test_creation(self):
        """Test creating CategoryNotFoundException."""
        exc = CategoryNotFoundException(category_id=456)
        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert exc.error_code == "CATEGORY_NOT_FOUND"
        assert "456" in exc.detail["message"]


class TestValidationError:
    """Test ValidationError."""
    
    def test_creation(self):
        """Test creating ValidationError."""
        exc = ValidationError(
            message="Invalid input",
            details="Field 'email' is required"
        )
        assert exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert exc.error_code == "VALIDATION_ERROR"
        assert exc.detail["message"] == "Invalid input"
        assert exc.detail["details"] == "Field 'email' is required"


class TestDatabaseError:
    """Test DatabaseError."""
    
    def test_creation(self):
        """Test creating DatabaseError."""
        exc = DatabaseError(
            message="Connection failed",
            details="Unable to connect to database"
        )
        assert exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc.error_code == "DATABASE_ERROR"
        assert exc.detail["message"] == "Connection failed"


class TestUnauthorizedException:
    """Test UnauthorizedException."""
    
    def test_creation(self):
        """Test creating UnauthorizedException."""
        exc = UnauthorizedException(message="Invalid token")
        assert exc.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.error_code == "UNAUTHORIZED"
        assert exc.detail["message"] == "Invalid token"


class TestForbiddenException:
    """Test ForbiddenException."""
    
    def test_creation(self):
        """Test creating ForbiddenException."""
        exc = ForbiddenException(message="Admin access required")
        assert exc.status_code == status.HTTP_403_FORBIDDEN
        assert exc.error_code == "FORBIDDEN"
        assert exc.detail["message"] == "Admin access required"


class TestAIAnalysisError:
    """Test AIAnalysisError."""
    
    def test_creation(self):
        """Test creating AIAnalysisError."""
        exc = AIAnalysisError(detail="Model failed to load")
        assert exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert exc.error_code == "AI_ANALYSIS_ERROR"
        assert exc.detail["message"] == "Model failed to load"


class TestGmailServiceError:
    """Test GmailServiceError."""
    
    def test_creation(self):
        """Test creating GmailServiceError."""
        exc = GmailServiceError(detail="API quota exceeded")
        assert exc.status_code == status.HTTP_502_BAD_GATEWAY
        assert exc.error_code == "GMAIL_SERVICE_ERROR"
        assert exc.detail["message"] == "API quota exceeded"
    
    def test_with_custom_status_code(self):
        """Test GmailServiceError with custom status code."""
        exc = GmailServiceError(
            detail="Service unavailable",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )
        assert exc.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert exc.error_code == "GMAIL_SERVICE_ERROR"