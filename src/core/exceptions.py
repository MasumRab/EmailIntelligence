"""
Core exceptions for EmailIntelligence CLI

This module defines custom exceptions used throughout the system.
"""


class EmailIntelligenceException(Exception):
    """Base exception for all EmailIntelligence CLI exceptions."""
    pass


class ConflictDetectionError(EmailIntelligenceException):
    """Raised when conflict detection fails."""
    pass


class ConstitutionalAnalysisError(EmailIntelligenceException):
    """Raised when constitutional analysis fails."""
    pass


class ResolutionStrategyError(EmailIntelligenceException):
    """Raised when resolution strategy generation fails."""
    pass


class ValidationError(EmailIntelligenceException):
    """Raised when validation fails."""
    pass


class ConfigurationError(EmailIntelligenceException):
    """Raised when configuration is invalid."""
    pass


class GitOperationError(EmailIntelligenceException):
    """Raised when git operations fail."""
    pass


class ResourceNotFoundError(EmailIntelligenceException):
    """Raised when a required resource is not found."""
    pass


class PermissionError(EmailIntelligenceException):
    """Raised when an operation lacks required permissions."""
    pass

# Aliases for backward compatibility
EmailIntelligenceError = EmailIntelligenceException
AnalysisError = ConstitutionalAnalysisError
StrategyGenerationError = ResolutionStrategyError


class ResolutionError(EmailIntelligenceException):
    """Raised when conflict resolution fails."""
    pass


class DatabaseError(EmailIntelligenceException):
    """Raised when database operations fail."""
    pass


class StorageError(EmailIntelligenceException):
    """Raised when storage operations fail."""
    pass
