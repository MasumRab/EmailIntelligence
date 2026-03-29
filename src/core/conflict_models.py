"""
Conflict Models

Defines data models for conflict representation and analysis.
"""
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


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

class AnalysisResult:
    """Result of conflict analysis"""
    def __init__(self, conflicts: List[Conflict], risk_level: RiskLevel, recommendations: List[str]):
        self.conflicts = conflicts
        self.risk_level = risk_level
        self.recommendations = recommendations


class ResolutionStrategy:
    """Strategy for resolving conflicts"""
    def __init__(self, strategy_type: str, steps: List[Dict[str, Any]]):
        self.strategy_type = strategy_type
        self.steps = steps


class ValidationResult:
    """Result of validation"""
    def __init__(self, is_valid: bool, errors: List[str], warnings: List[str]):
        self.is_valid = is_valid
        self.errors = errors
        self.warnings = warnings


class ResolutionPlan:
    """Plan for resolving conflicts"""
    def __init__(self, conflicts: List[Conflict], strategy: ResolutionStrategy):
        self.conflicts = conflicts
        self.strategy = strategy


class ValidationStatus(Enum):
    """Status of validation"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    PENDING = "pending"
