"""
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
        self,
        detail: str = "An error occurred with the Gmail service.",
        status_code: int = 502,
    ):
        super().__init__(status_code=status_code, detail=detail)


class EmailNotFoundException(BaseAppException):
    """Exception raised when an email cannot be found.

    Compatible with the call signature used by
    ``src/backend/python_backend/routes/v1/email_routes.py``
    (``email_id`` and ``message_id`` keyword arguments).
    """

    def __init__(
        self,
        email_id: int | None = None,
        message_id: str | None = None,
    ):
        if email_id is not None:
            detail = f"Email with ID {email_id} not found"
        elif message_id is not None:
            detail = f"Email with message ID {message_id} not found"
        else:
            detail = "Email not found"
        super().__init__(status_code=404, detail=detail)


class GitOperationError(BaseAppException):
    """Exception for a failed git operation.

    Takes a single message rather than the ``(status_code, detail)`` pair
    because the callers in :mod:`src.git` construct it as
    ``GitOperationError(f"...")``.
    """

    def __init__(self, detail: str = "A git operation failed."):
        super().__init__(status_code=500, detail=detail)


class ConflictDetectionError(BaseAppException):
    """Exception for a failure while detecting merge conflicts.

    Takes a single message for the same reason as
    :class:`GitOperationError`: :mod:`src.git.conflict_detector` constructs it
    as ``ConflictDetectionError(f"...")``.
    """

    def __init__(self, detail: str = "Conflict detection failed."):
        super().__init__(status_code=500, detail=detail)
