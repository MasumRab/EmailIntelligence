"""
Git module for EmailIntelligence CLI
"""

# Exports without importing from core to avoid circular imports
# The actual classes are defined in their respective modules

__all__ = [
    "WorktreeManager",
    "GitConflictDetector",
    "RepositoryOperations",
    "GitHistory",
    "Commit",
    "CommitClassifier",
]
