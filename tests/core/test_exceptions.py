"""
Tests for src/core/exceptions.py
"""

import pytest
from src.core.exceptions import (
    BaseAppException,
    DatabaseError,
    AIAnalysisError,
    GmailServiceError,
)


class TestBaseAppException:
    """Tests for BaseAppException."""

    def test_base_exception_initialization(self):
        """Test BaseAppException initialization with status code and detail."""
        exc = BaseAppException(status_code=400, detail="Bad request")
        
        assert exc.status_code == 400
        assert exc.detail == "Bad request"
        assert str(exc) == "Bad request"

    def test_base_exception_status_code_type(self):
        """Test status_code is an integer."""
        exc = BaseAppException(status_code=404, detail="Not found")
        assert isinstance(exc.status_code, int)

    def test_base_exception_detail_type(self):
        """Test detail is a string."""
        exc = BaseAppException(status_code=500, detail="Internal error")
        assert isinstance(exc.detail, str)


class TestDatabaseError:
    """Tests for DatabaseError."""

    def test_database_error_default_values(self):
        """Test DatabaseError has correct default values."""
        exc = DatabaseError()
        
        assert exc.status_code == 503
        assert exc.detail == "A database error occurred."

    def test_database_error_custom_message(self):
        """Test DatabaseError with custom message."""
        exc = DatabaseError(detail="Connection failed")
        
        assert exc.status_code == 503
        assert exc.detail == "Connection failed"

    def test_database_error_is_base_app_exception(self):
        """Test DatabaseError inherits from BaseAppException."""
        exc = DatabaseError()
        assert isinstance(exc, BaseAppException)


class TestAIAnalysisError:
    """Tests for AIAnalysisError."""

    def test_ai_analysis_error_default_values(self):
        """Test AIAnalysisError has correct default values."""
        exc = AIAnalysisError()
        
        assert exc.status_code == 500
        assert exc.detail == "An error occurred during AI analysis."

    def test_ai_analysis_error_custom_message(self):
        """Test AIAnalysisError with custom message."""
        exc = AIAnalysisError(detail="Model inference failed")
        
        assert exc.status_code == 500
        assert exc.detail == "Model inference failed"

    def test_ai_analysis_error_is_base_app_exception(self):
        """Test AIAnalysisError inherits from BaseAppException."""
        exc = AIAnalysisError()
        assert isinstance(exc, BaseAppException)


class TestGmailServiceError:
    """Tests for GmailServiceError."""

    def test_gmail_service_error_default_values(self):
        """Test GmailServiceError has correct default values."""
        exc = GmailServiceError()
        
        assert exc.status_code == 502
        assert exc.detail == "An error occurred with the Gmail service."

    def test_gmail_service_error_custom_message(self):
        """Test GmailServiceError with custom message."""
        exc = GmailServiceError(detail="Authentication failed")
        
        assert exc.status_code == 502
        assert exc.detail == "Authentication failed"

    def test_gmail_service_error_custom_status_code(self):
        """Test GmailServiceError with custom status code."""
        exc = GmailServiceError(status_code=401, detail="Unauthorized")
        
        assert exc.status_code == 401
        assert exc.detail == "Unauthorized"

    def test_gmail_service_error_is_base_app_exception(self):
        """Test GmailServiceError inherits from BaseAppException."""
        exc = GmailServiceError()
        assert isinstance(exc, BaseAppException)