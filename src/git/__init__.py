"""
Git operations module for EmailIntelligence CLI

This module handles all git interactions, including worktree management,
conflict detection, and repository operations.
"""

from .worktree import WorktreeManager
from .conflict_detector import GitConflictDetector
from .merger import GitMerger
from .repository import RepositoryOperations

__all__ = [
    "WorktreeManager",
    "GitConflictDetector",
    "GitMerger",
    "RepositoryOperations",
]
