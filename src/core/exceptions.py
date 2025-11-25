"""
Custom exceptions for EmailIntelligence CLI

This module defines a hierarchy of exceptions used throughout the EmailIntelligence
system for better error handling and debugging.
"""


class EmailIntelligenceError(Exception):
    """
    Base exception for all EmailIntelligence errors.
    
    All custom exceptions in the system should inherit from this class.
    """
    pass


class ConflictDetectionError(EmailIntelligenceError):
    """
    Raised when conflict detection fails.
    
    Examples:
        - Git merge-tree command fails
        - Unable to parse conflict markers
        - Invalid PR references
    """
    pass


class AnalysisError(EmailIntelligenceError):
    """
    Raised when code analysis fails.
    
    Examples:
        - AST parsing errors
        - Constitutional rule evaluation failures
        - Complexity calculation errors
    """
    pass


class StrategyGenerationError(EmailIntelligenceError):
    """
    Raised when strategy generation fails.
    
    Examples:
        - AI API failures
        - Invalid strategy parameters
        - Strategy validation failures
    """
    pass


class ResolutionError(EmailIntelligenceError):
    """
    Raised when conflict resolution fails.
    
    Examples:
        - Resolution execution errors
        - Merge operation failures
        - Validation failures after resolution
    """
    pass


class ValidationError(EmailIntelligenceError):
    """
    Raised when validation fails.
    
    Examples:
        - Test execution failures
        - Quality check failures
        - Security scan issues
    """
    pass


class DatabaseError(EmailIntelligenceError):
    """
    Raised when database operations fail.
    
    Examples:
        - Neo4j connection failures
        - Query execution errors
        - Transaction failures
    """
    pass


class GitOperationError(EmailIntelligenceError):
    """
    Raised when git operations fail.
    
    Examples:
        - Worktree creation failures
        - Branch checkout errors
        - Merge failures
        - Repository access issues
    """
    pass


class ConfigurationError(EmailIntelligenceError):
    """
    Raised when configuration is invalid or missing.
    
    Examples:
        - Missing required configuration
        - Invalid configuration values
        - Environment variable errors
    """
    pass


class StorageError(EmailIntelligenceError):
    """
    Raised when storage operations fail.
    
    Examples:
        - File I/O errors
        - Metadata save/load failures
        - Permission errors
    """
    pass


class InterfaceError(EmailIntelligenceError):
    """
    Raised when interface contract violations occur.
    
    Examples:
        - Missing required methods
        - Invalid return types
        - Protocol violations
    """
    pass
