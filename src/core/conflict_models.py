"""
Conflict Models

Defines data models for conflict representation and analysis.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class ConflictTypeExtended(Enum):
    """Extended types of conflicts"""

    CONTENT = "content"
    MERGE = "merge"
    FILE_DELETE = "file_delete"
    PERMISSION = "permission"
    BINARY = "binary"
    SEMANTIC = "semantic"
    LOGICAL = "logical"
    ARCHITECTURAL = "architectural"


class RiskLevel(Enum):
    """Risk levels for conflicts"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ConflictBlock:
    """Represents a single conflict block in a file"""

    start_line: int
    end_line: int
    conflict_type: ConflictTypeExtended
    content_before: List[str]
    content_after: List[str]
    content_common: List[str]
    original_content: Optional[List[str]] = None


@dataclass
class Conflict:
    """Represents a git conflict"""

    file_path: str
    conflict_blocks: List[ConflictBlock]
    conflict_type: ConflictTypeExtended
    severity: RiskLevel
    description: str = ""
    resolution_strategy: str = ""
    affected_components: List[str] = None
    estimated_resolution_time: int = 0  # in minutes

    def __post_init__(self):
        if self.affected_components is None:
            self.affected_components = []
