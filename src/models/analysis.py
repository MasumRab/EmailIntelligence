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
