"""
Unit tests for the exceptions module.
"""

import pytest

# Import the exceptions module
from src.core.exceptions import (
    EmailIntelligenceError,
    AuthenticationError,
    ValidationError,
    WorkflowError,
    BaseAppException,
    DatabaseError,
    AIAnalysisError,
    GmailServiceError,
)


class TestEmailIntelligenceError:
    """Test the base EmailIntelligenceError exception."""

    def test_inherits_from_exception(self):
        """Test that EmailIntelligenceError inherits from Exception."""
        error = EmailIntelligenceError("test message")
        assert isinstance(error, Exception)

    def test_message_is_stored(self):
        """Test that message is stored correctly."""
        error = EmailIntelligenceError("custom error message")
        assert error.message == "custom error message"

    def test_str_representation(self):
        """Test string representation of error."""
        error = EmailIntelligenceError("test error")
        assert str(error) == "test error"

    def test_empty_message(self):
        """Test with empty message."""
        error = EmailIntelligenceError("")
        assert error.message == ""

    def test_default_init(self):
        """Test the constructor accepts message parameter."""
        error = EmailIntelligenceError("Test")
        assert error.message == "Test"


class TestAuthenticationError:
    """Test the AuthenticationError exception."""

    def test_inherits_from_base(self):
        """Test that AuthenticationError inherits from EmailIntelligenceError."""
        error = AuthenticationError()
        assert isinstance(error, EmailIntelligenceError)
        assert isinstance(error, Exception)

    def test_default_message(self):
        """Test default message for AuthenticationError."""
        error = AuthenticationError()
        assert error.message == "Authentication failed"

    def test_custom_message(self):
        """Test custom message for AuthenticationError."""
        error = AuthenticationError("Token expired")
        assert error.message == "Token expired"


class TestValidationError:
    """Test the ValidationError exception."""

    def test_inherits_from_base(self):
        """Test that ValidationError inherits from EmailIntelligenceError."""
        error = ValidationError()
        assert isinstance(error, EmailIntelligenceError)

    def test_default_message(self):
        """Test default message for ValidationError."""
        error = ValidationError()
        assert error.message == "Validation failed"

    def test_custom_message(self):
        """Test custom message for ValidationError."""
        error = ValidationError("Invalid email format")
        assert error.message == "Invalid email format"


class TestWorkflowError:
    """Test the WorkflowError exception."""

    def test_inherits_from_base(self):
        """Test that WorkflowError inherits from EmailIntelligenceError."""
        error = WorkflowError()
        assert isinstance(error, EmailIntelligenceError)

    def test_default_message(self):
        """Test default message for WorkflowError."""
        error = WorkflowError()
        assert error.message == "Workflow error occurred"

    def test_custom_message(self):
        """Test custom message for WorkflowError."""
        error = WorkflowError("Step 3 failed")
        assert error.message == "Step 3 failed"


class TestBaseAppException:
    """Test the BaseAppException class."""

    def test_inherits_from_exception(self):
        """Test that BaseAppException inherits from Exception."""
        error = BaseAppException(404, "Not found")
        assert isinstance(error, Exception)

    def test_status_code_is_stored(self):
        """Test that status_code is stored correctly."""
        error = BaseAppException(500, "Server error")
        assert error.status_code == 500

    def test_detail_is_stored(self):
        """Test that detail is stored correctly."""
        error = BaseAppException(404, "Resource not found")
        assert error.detail == "Resource not found"

    def test_str_is_detail(self):
        """Test that str() returns detail."""
        error = BaseAppException(404, "Not found")
        assert str(error) == "Not found"

    def test_custom_status_code(self):
        """Test with custom status code."""
        error = BaseAppException(403, "Forbidden")
        assert error.status_code == 403
        assert error.detail == "Forbidden"

    def test_various_status_codes(self):
        """Test various HTTP status codes."""
        test_cases = [
            (400, "Bad request"),
            (401, "Unauthorized"),
            (403, "Forbidden"),
            (404, "Not found"),
            (500, "Internal error"),
            (503, "Service unavailable"),
        ]
        for code, detail in test_cases:
            error = BaseAppException(code, detail)
            assert error.status_code == code
            assert error.detail == detail


class TestDatabaseError:
    """Test the DatabaseError exception."""

    def test_inherits_from_base(self):
        """Test that DatabaseError inherits from BaseAppException."""
        error = DatabaseError()
        assert isinstance(error, BaseAppException)
        assert isinstance(error, Exception)

    def test_default_status_code(self):
        """Test default status code for DatabaseError."""
        error = DatabaseError()
        assert error.status_code == 503

    def test_default_detail(self):
        """Test default detail for DatabaseError."""
        error = DatabaseError()
        assert error.detail == "A database error occurred."

    def test_custom_detail(self):
        """Test custom detail for DatabaseError."""
        error = DatabaseError("Connection timeout")
        assert error.status_code == 503
        assert error.detail == "Connection timeout"


class TestAIAnalysisError:
    """Test the AIAnalysisError exception."""

    def test_inherits_from_base(self):
        """Test that AIAnalysisError inherits from BaseAppException."""
        error = AIAnalysisError()
        assert isinstance(error, BaseAppException)

    def test_default_status_code(self):
        """Test default status code for AIAnalysisError."""
        error = AIAnalysisError()
        assert error.status_code == 500

    def test_default_detail(self):
        """Test default detail for AIAnalysisError."""
        error = AIAnalysisError()
        assert error.detail == "An error occurred during AI analysis."

    def test_custom_detail(self):
        """Test custom detail for AIAnalysisError."""
        error = AIAnalysisError("Model not responding")
        assert error.status_code == 500
        assert error.detail == "Model not responding"


class TestGmailServiceError:
    """Test the GmailServiceError exception."""

    def test_inherits_from_base(self):
        """Test that GmailServiceError inherits from BaseAppException."""
        error = GmailServiceError()
        assert isinstance(error, BaseAppException)

    def test_default_status_code(self):
        """Test default status code for GmailServiceError."""
        error = GmailServiceError()
        assert error.status_code == 502

    def test_default_detail(self):
        """Test default detail for GmailServiceError."""
        error = GmailServiceError()
        assert error.detail == "An error occurred with the Gmail service."

    def test_custom_status_code(self):
        """Test custom status code for GmailServiceError."""
        error = GmailServiceError(detail="Gmail API rate limited", status_code=429)
        assert error.status_code == 429
        assert error.detail == "Gmail API rate limited"

    def test_custom_detail_only(self):
        """Test with only custom detail."""
        error = GmailServiceError(detail="Authentication failed")
        assert error.status_code == 502
        assert error.detail == "Authentication failed"

    def test_multiple_custom_status_codes(self):
        """Test multiple custom status codes."""
        test_cases = [
            (500, "Internal server error"),
            (502, "Bad gateway"),
            (503, "Service unavailable"),
            (504, "Gateway timeout"),
            (429, "Rate limited"),
        ]
        for code, detail in test_cases:
            error = GmailServiceError(detail=detail, status_code=code)
            assert error.status_code == code
            assert error.detail == detail


class TestExceptionInheritance:
    """Test exception class inheritance hierarchy."""

    def test_email_intelligence_error_is_base(self):
        """Test EmailIntelligenceError is the base exception."""
        errors = [
            AuthenticationError(),
            ValidationError(),
            WorkflowError(),
        ]
        for error in errors:
            assert isinstance(error, EmailIntelligenceError)

    def test_base_app_exception_is_separate_hierarchy(self):
        """Test BaseAppException is a separate hierarchy."""
        app_errors = [
            DatabaseError(),
            AIAnalysisError(),
            GmailServiceError(),
        ]
        for error in app_errors:
            assert isinstance(error, BaseAppException)
            # Should NOT be EmailIntelligenceError
            assert not isinstance(error, EmailIntelligenceError)


class TestExceptionRaising:
    """Test that exceptions can be raised and caught properly."""

    def test_raise_and_catch_email_intelligence_error(self):
        """Test raising and catching EmailIntelligenceError."""
        with pytest.raises(EmailIntelligenceError):
            raise EmailIntelligenceError("test error")

    def test_raise_and_catch_authentication_error(self):
        """Test raising and catching AuthenticationError."""
        with pytest.raises(AuthenticationError):
            raise AuthenticationError("Invalid token")

    def test_raise_and_catch_validation_error(self):
        """Test raising and catching ValidationError."""
        with pytest.raises(ValidationError):
            raise ValidationError("Invalid input")

    def test_raise_and_catch_workflow_error(self):
        """Test raising and catching WorkflowError."""
        with pytest.raises(WorkflowError):
            raise WorkflowError("Workflow step failed")

    def test_raise_and_catch_base_app_exception(self):
        """Test raising and catching BaseAppException."""
        with pytest.raises(BaseAppException) as exc_info:
            raise BaseAppException(400, "Bad request")
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Bad request"

    def test_raise_and_catch_database_error(self):
        """Test raising and catching DatabaseError."""
        with pytest.raises(DatabaseError) as exc_info:
            raise DatabaseError("Query failed")
        assert exc_info.value.status_code == 503

    def test_raise_and_catch_gmail_service_error(self):
        """Test raising and catching GmailServiceError."""
        with pytest.raises(GmailServiceError) as exc_info:
            raise GmailServiceError(detail="API error", status_code=500)
        assert exc_info.value.status_code == 500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])