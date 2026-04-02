"""
Tests for exception classes.
"""

import pytest
from src.core.exceptions import (
    BaseAppException,
    DatabaseError,
    AIAnalysisError,
    GmailServiceError,
    EmailIntelligenceError,
    AuthenticationError,
    ValidationError,
    WorkflowError,
)


class TestBaseAppException:
    """Test the BaseAppException class."""

    def test_base_exception_creation(self):
        """Test BaseAppException creation."""
        exc = BaseAppException(status_code=400, detail="Test error")
        assert exc.status_code == 400
        assert exc.detail == "Test error"
        assert str(exc) == "Test error"

    def test_base_exception_with_custom_message(self):
        """Test BaseAppException with custom message."""
        exc = BaseAppException(status_code=500, detail="Custom message")
        assert exc.detail == "Custom message"


class TestDatabaseError:
    """Test the DatabaseError class."""

    def test_database_error_default(self):
        """Test DatabaseError with default message."""
        exc = DatabaseError()
        assert exc.status_code == 503
        assert exc.detail == "A database error occurred."

    def test_database_error_custom_message(self):
        """Test DatabaseError with custom message."""
        exc = DatabaseError(detail="Connection failed")
        assert exc.status_code == 503
        assert exc.detail == "Connection failed"


class TestAIAnalysisError:
    """Test the AIAnalysisError class."""

    def test_ai_analysis_error_default(self):
        """Test AIAnalysisError with default message."""
        exc = AIAnalysisError()
        assert exc.status_code == 500
        assert exc.detail == "An error occurred during AI analysis."

    def test_ai_analysis_error_custom_message(self):
        """Test AIAnalysisError with custom message."""
        exc = AIAnalysisError(detail="Model timeout")
        assert exc.status_code == 500
        assert exc.detail == "Model timeout"


class TestGmailServiceError:
    """Test the GmailServiceError class."""

    def test_gmail_error_default(self):
        """Test GmailServiceError with default message."""
        exc = GmailServiceError()
        assert exc.status_code == 502
        assert exc.detail == "An error occurred with the Gmail service."

    def test_gmail_error_custom_message(self):
        """Test GmailServiceError with custom message."""
        exc = GmailServiceError(detail="API rate limit exceeded")
        assert exc.status_code == 502
        assert exc.detail == "API rate limit exceeded"

    def test_gmail_error_custom_status_code(self):
        """Test GmailServiceError with custom status code."""
        exc = GmailServiceError(detail="Auth expired", status_code=401)
        assert exc.status_code == 401
        assert exc.detail == "Auth expired"


class TestAdditionalExceptions:
    """Test additional exception classes."""

    def test_email_intelligence_error(self):
        """Test EmailIntelligenceError creation."""
        exc = EmailIntelligenceError("Test error")
        assert exc.message == "Test error"
        assert str(exc) == "Test error"

    def test_authentication_error(self):
        """Test AuthenticationError creation."""
        exc = AuthenticationError("Invalid token")
        assert exc.message == "Invalid token"

    def test_validation_error(self):
        """Test ValidationError creation."""
        exc = ValidationError("Invalid input")
        assert exc.message == "Invalid input"

    def test_workflow_error(self):
        """Test WorkflowError creation."""
        exc = WorkflowError("Invalid workflow")
        assert exc.message == "Invalid workflow"