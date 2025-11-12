"""
TODO: Refactor or deprecate this module.

This module defines `Commit` and `Intention` dataclasses. It appears to be an older
or alternative set of data models for analysis.

The new unified data models for the `git-verifier` feature are defined in
`src/models/unified_analysis.py` (`ActionNarrative`, `IntentReport`, `VerificationResult`).

Consider the following:
1.  **Consolidation:** If the concepts of `Commit` and `Intention` are still relevant,
    their definitions and usage should be consolidated with the models in
    `src/models/unified_analysis.py` to maintain a single source of truth for data structures.
2.  **Deprecation:** If these models are no longer used by any active part of the system,
    this module should be deprecated and eventually removed to reduce codebase clutter.
3.  **Refinement:** If `file_changes_summary` in `Commit` or `status` in `Intention`
    are to be used, they should be refined (e.g., `file_changes_summary` could be a
    list of structured change objects, `status` could be an Enum).
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Commit:
    """
    Represents a change in the repository history.
    """
    message: str
    author: str
    changes: List[str]
    timestamp: datetime
    parent_shas: List[str]
    file_changes_summary: str

@dataclass
class Intention:
    """
    The purpose or goal behind a specific change or set of changes.
    """
    description: str
    associated_commits: List[Commit]
    status: str  # "fulfilled", "partially_fulfilled", "unfulfilled"