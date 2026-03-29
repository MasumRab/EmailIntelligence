"""
Module for legacy analysis data models.

This module defines `Commit` and `Intention` dataclasses, which represent
an older or alternative set of data models for analysis within the system.
The new unified data models for the `git-verifier` feature are defined in
`src/models/unified_analysis.py` (`ActionNarrative`, `IntentReport`, `VerificationResult`).

TODO: Plan for migration and eventual removal of this module.
1.  **Assess Usage:** Identify all remaining dependencies on `src/models/analysis.py`,
    including `tests/unit/test_rebase_analyzer.py` and any other potential internal
    or external consumers.
2.  **Migration Strategy:** Develop a clear strategy to migrate existing code
    (especially tests) to use the unified models in `src/models/unified_analysis.py`.
    This might involve:
    *   Creating adapter functions or classes.
    *   Directly refactoring dependent code to use the new models.
3.  **Consolidation/Refinement:** If the concepts of `Commit` and `Intention` are
    still fundamentally relevant, ensure their essential attributes are represented
    or integrated into the unified models. Refine any necessary fields (e.g.,
    `file_changes_summary` could be a list of structured change objects, `status`
    could be an Enum).
4.  **Deprecation Path:** Once all dependencies are migrated, formally deprecate
    this module (e.g., by adding a `warnings.warn` in its usage points) and
    schedule its removal to reduce codebase clutter and maintain a single source
    of truth for data structures.
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