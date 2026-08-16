"""Base exception classes for Agent Context Control library."""


class ContextControlError(Exception):
    """Base exception for all context control operations."""

    def __init__(self, message: str, context_id: str | None = None) -> None:
        super().__init__(message)
        self.context_id = context_id


class ContextNotFoundError(ContextControlError):
    """Raised when a requested context cannot be found."""

    pass


class ContextValidationError(ContextControlError):
    """Raised when context validation fails."""

    pass


class ContextIsolationError(ContextControlError):
    """Raised when context isolation mechanisms fail."""

    pass


class ConfigurationError(ContextControlError):
    """Raised when configuration is invalid or missing."""

    pass


class EnvironmentDetectionError(ContextControlError):
    """Raised when environment detection fails."""

    pass


class StorageError(ContextControlError):
    """Raised when context storage operations fail."""

    pass
