"""Tests for core exceptions module."""

import pytest  # noqa: F401
from src.core.exceptions import (
    BaseAppException,
    DatabaseError,
    AIAnalysisError,
    GmailServiceError,
)


class TestBaseAppException:
    """Test the BaseAppException class."""

    def test_base_exception_creation(self):
        """Test creating a base exception with status and detail."""
        exc = BaseAppException(status_code=400, detail="Test error")
        assert exc.status_code == 400
        assert exc.detail == "Test error"
        assert str(exc) == "Test error"

    def test_base_exception_with_custom_message(self):
        """Test base exception with custom message."""
        exc = BaseAppException(status_code=500, detail="Server error")
        assert exc.args[0] == "Server error"

    def test_base_exception_inheritance(self):
        """Test that BaseAppException inherits from Exception."""
        exc = BaseAppException(status_code=404, detail="Not found")
        assert isinstance(exc, Exception)


class TestDatabaseError:
    """Test the DatabaseError class."""

    def test_database_error_default(self):
        """Test database error with default message."""
        exc = DatabaseError()
        assert exc.status_code == 503
        assert exc.detail == "A database error occurred."

    def test_database_error_custom_message(self):
        """Test database error with custom message."""
        exc = DatabaseError(detail="Connection failed")
        assert exc.status_code == 503
        assert exc.detail == "Connection failed"
        assert str(exc) == "Connection failed"

    def test_database_error_inheritance(self):
        """Test DatabaseError inherits from BaseAppException."""
        exc = DatabaseError()
        assert isinstance(exc, BaseAppException)
        assert isinstance(exc, Exception)


class TestAIAnalysisError:
    """Test the AIAnalysisError class."""

    def test_ai_analysis_error_default(self):
        """Test AI analysis error with default message."""
        exc = AIAnalysisError()
        assert exc.status_code == 500
        assert exc.detail == "An error occurred during AI analysis."

    def test_ai_analysis_error_custom_message(self):
        """Test AI analysis error with custom message."""
        exc = AIAnalysisError(detail="Model not found")
        assert exc.status_code == 500
        assert exc.detail == "Model not found"

    def test_ai_analysis_error_inheritance(self):
        """Test AIAnalysisError inherits from BaseAppException."""
        exc = AIAnalysisError()
        assert isinstance(exc, BaseAppException)
        assert isinstance(exc, Exception)


class TestGmailServiceError:
    """Test the GmailServiceError class."""

    def test_gmail_service_error_default(self):
        """Test Gmail service error with default values."""
        exc = GmailServiceError()
        assert exc.status_code == 502
        assert exc.detail == "An error occurred with the Gmail service."

    def test_gmail_service_error_custom_detail(self):
        """Test Gmail service error with custom detail."""
        exc = GmailServiceError(detail="Authentication failed")
        assert exc.status_code == 502
        assert exc.detail == "Authentication failed"

    def test_gmail_service_error_custom_status(self):
        """Test Gmail service error with custom status code."""
        exc = GmailServiceError(status_code=429, detail="Rate limited")
        assert exc.status_code == 429
        assert exc.detail == "Rate limited"

    def test_gmail_service_error_custom_both(self):
        """Test Gmail service error with custom detail and status."""
        exc = GmailServiceError(detail="Timeout", status_code=504)
        assert exc.status_code == 504
        assert exc.detail == "Timeout"

    def test_gmail_service_error_inheritance(self):
        """Test GmailServiceError inherits from BaseAppException."""
        exc = GmailServiceError()
        assert isinstance(exc, BaseAppException)
        assert isinstance(exc, Exception)