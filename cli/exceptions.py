"""
EmailIntelligence CLI - Custom Exception Hierarchy

This module contains all custom exceptions used by the EmailIntelligence CLI.
Each exception follows a hierarchical structure for granular error handling.
"""

from typing import Optional


# ============================================================================
# CUSTOM EXCEPTION HIERARCHY
# ============================================================================


class EmailIntelligenceError(Exception):
    """Base exception class for all EmailIntelligence errors"""
    pass


class GitOperationError(EmailIntelligenceError):
    """Raised when git operations fail"""
    pass


class MergeTreeError(GitOperationError):
    """Raised when git merge-tree command fails"""
    pass


class BranchNotFoundError(GitOperationError):
    """Raised when specified branch doesn't exist locally or remotely"""
    pass


class WorktreeUnavailableError(GitOperationError):
    """Raised when git worktree operations fail or worktree not supported"""
    pass


class ConflictDetectionError(EmailIntelligenceError):
    """Raised when conflict detection fails"""
    pass


class WorkspaceCreationError(EmailIntelligenceError):
    """Raised when workspace creation fails"""
    pass


class ResolutionNotReadyError(EmailIntelligenceError):
    """Raised when attempting operations on incomplete resolutions"""
    pass


class PushOperationError(EmailIntelligenceError):
    """Raised when push operations fail"""
    pass


class BranchEnumerationError(EmailIntelligenceError):
    """Raised when branch enumeration fails"""
    pass


class ScanExecutionError(EmailIntelligenceError):
    """Raised when all-branches scanning fails"""
    pass


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'EmailIntelligenceError',
    'GitOperationError',
    'MergeTreeError',
    'BranchNotFoundError',
    'WorktreeUnavailableError',
    'ConflictDetectionError',
    'WorkspaceCreationError',
    'ResolutionNotReadyError',
    'PushOperationError',
    'BranchEnumerationError',
    'ScanExecutionError',
]
