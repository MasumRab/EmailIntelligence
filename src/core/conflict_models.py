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


@dataclass
class AnalysisResult:
    """Result of constitutional analysis"""
    compliance_score: float
    violations: List[str]
    recommendations: List[str]
    details: Dict[str, Any]


@dataclass
class ResolutionStrategy:
    """Strategy for resolving conflicts"""
    strategy_type: str
    steps: List[Dict[str, Any]]
    estimated_time: int
    risk_assessment: Dict[str, Any]


@dataclass
class ValidationResult:
    """Result of validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    details: Dict[str, Any]


@dataclass
class ResolutionPlan:
    """Plan for resolving conflicts"""
    conflicts: List[Conflict]
    strategy: ResolutionStrategy
    validation_result: ValidationResult
    execution_context: Dict[str, Any]