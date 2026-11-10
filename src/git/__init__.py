"""Git module for EmailIntelligence CLI.

Re-exports the public surface so ``from src.git import WorktreeManager`` works.
The implementations live in the sibling modules; nothing here imports
``src.core``, which is what keeps this package free of the analysis tree's
circular import.
"""

from .conflict_detector import GitConflictDetector
from .history import Commit, CommitClassifier, GitHistory
from .repository import RepositoryOperations
from .worktree import WorktreeManager

__all__ = [
    "WorktreeManager",
    "GitConflictDetector",
    "RepositoryOperations",
    "GitHistory",
    "Commit",
    "CommitClassifier",
]
