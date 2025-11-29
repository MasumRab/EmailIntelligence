"""
Core types and models for the intelligent conflict resolution system
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from src.models.graph_entities import ConflictSeverity


class ConflictTypeExtended(str, Enum):
    """Extended conflict types for resolution engine"""

    MERGE_CONFLICT = "MERGE_CONFLICT"
    DEPENDENCY_CONFLICT = "DEPENDENCY_CONFLICT"
    ARCHITECTURE_VIOLATION = "ARCHITECTURE_VIOLATION"
    SEMANTIC_INCOMPATIBILITY = "SEMANTIC_INCOMPATIBILITY"
    RESOURCE_LOCK = "RESOURCE_LOCK"
    SEMANTIC_CONFLICT = "SEMANTIC_CONFLICT"
    LOGICAL_INCONSISTENCY = "LOGICAL_INCONSISTENCY"
    CONFIGURATION_CONFLICT = "CONFIGURATION_CONFLICT"
    TEST_FAILURE = "TEST_FAILURE"
    CODE_STYLE_VIOLATION = "CODE_STYLE_VIOLATION"
    SECURITY_VIOLATION = "SECURITY_VIOLATION"
    PERFORMANCE_ISSUE = "PERFORMANCE_ISSUE"


class RiskLevel(str, Enum):
    """Risk levels for resolution strategies"""

    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    CRITICAL = "CRITICAL"


class ExecutionStatus(str, Enum):
    """Resolution execution status"""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    VALIDATING = "VALIDATING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    REQUIRES_APPROVAL = "REQUIRES_APPROVAL"
    CANCELLED = "CANCELLED"


class ValidationStatus(str, Enum):
    """Validation result status"""

    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"
    PENDING = "PENDING"


class CodeChange(BaseModel):
    """Represents a code change for resolution"""

    file_path: str = Field(..., description="Path to the file to modify")
    operation: str = Field(..., description="Type of operation: add, modify, delete, replace")
    start_line: Optional[int] = Field(None, description="Starting line number")
    end_line: Optional[int] = Field(None, description="Ending line number")
    old_content: Optional[str] = Field(None, description="Original content to replace")
    new_content: str = Field(..., description="New content to add/replace")
    description: str = Field(..., description="Description of the change")
    confidence: float = Field(..., description="AI confidence in this change (0.0-1.0)")
    validation_required: bool = Field(True, description="Whether this change requires validation")
    rollback_data: Optional[str] = Field(None, description="Data needed for rollback")

    class Config:
        json_schema_extra = {
            "example": {
                "file_path": "src/api/main.py",
                "operation": "modify",
                "start_line": 45,
                "end_line": 67,
                "old_content": "def old_function():\n    return old_result",
                "new_content": "def new_function():\n    return new_result",
                "description": "Update function implementation to resolve conflict",
                "confidence": 0.95,
                "validation_required": True,
            }
        }


class ResolutionStep(BaseModel):
    """Individual step in a resolution plan"""

    id: str = Field(..., description="Unique step identifier")
    description: str = Field(..., description="Human-readable description")
    code_changes: List[CodeChange] = Field(default_factory=list, description="Code changes for this step")
    validation_steps: List[str] = Field(default_factory=list, description="Validation steps to perform")
    estimated_time: int = Field(0, description="Estimated time in seconds")
    risk_level: RiskLevel = Field(..., description="Risk level of this step")
    can_rollback: bool = Field(True, description="Whether this step can be rolled back")
    dependencies: List[str] = Field(default_factory=list, description="IDs of steps this depends on")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "step_1",
                "description": "Update import statements to resolve dependency conflict",
                "code_changes": [],
                "validation_steps": ["check_imports", "run_linting"],
                "estimated_time": 30,
                "risk_level": "LOW",
                "can_rollback": True,
                "dependencies": [],
            }
        }


class ResolutionStrategy(BaseModel):
    """AI-generated resolution strategy"""

    id: str = Field(..., description="Unique strategy identifier")
    name: str = Field(..., description="Strategy name")
    description: str = Field(..., description="Strategy description")
    approach: str = Field(..., description="High-level approach taken")
    steps: List[ResolutionStep] = Field(default_factory=list, description="Resolution steps")
    pros: List[str] = Field(default_factory=list, description="Advantages of this approach")
    cons: List[str] = Field(default_factory=list, description="Disadvantages of this approach")
    confidence: float = Field(..., description="AI confidence in strategy (0.0-1.0)")
    estimated_time: int = Field(..., description="Estimated resolution time in seconds")
    risk_level: RiskLevel = Field(..., description="Overall risk level")
    requires_approval: bool = Field(False, description="Whether this strategy requires human approval")
    success_criteria: List[str] = Field(default_factory=list, description="Criteria for successful resolution")
    rollback_strategy: Optional[str] = Field(None, description="How to roll back if needed")
    validation_approach: str = Field(..., description="How to validate the resolution")
    ai_generated: bool = Field(True, description="Whether this was AI-generated")
    model_used: str = Field(..., description="AI model used for generation")
    prompt_context: Dict[str, Any] = Field(default_factory=dict, description="Context used in AI prompt")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "strategy_1",
                "name": "Intelligent Merge Strategy",
                "description": "Use AI to intelligently merge conflicting changes",
                "approach": "AI-powered semantic merge with conflict resolution",
                "steps": [],
                "pros": ["High accuracy", "Preserves functionality", "Minimal manual intervention"],
                "cons": ["May require review", "Complex conflicts might need adjustments"],
                "confidence": 0.92,
                "estimated_time": 120,
                "risk_level": "MEDIUM",
                "requires_approval": True,
                "success_criteria": ["All tests pass", "No regressions", "Conflicts resolved"],
                "rollback_strategy": "Git revert operations",
                "validation_approach": "Automated testing + manual review",
                "ai_generated": True,
                "model_used": "gpt-4o",
            }
        }


class ValidationResult(BaseModel):
    """Result of validation checks"""

    status: ValidationStatus = Field(..., description="Validation result status")
    message: str = Field(..., description="Validation result message")
    details: Dict[str, Any] = Field(default_factory=dict, description="Detailed validation results")
    execution_time: float = Field(..., description="Time taken for validation in seconds")
    validator_version: str = Field(..., description="Version of validator used")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Validation timestamp")


class QualityMetrics(BaseModel):
    """Quality metrics for resolution strategy"""

    correctness: float = Field(..., description="Correctness score (0.0-1.0)")
    maintainability: float = Field(..., description="Maintainability score (0.0-1.0)")
    readability: float = Field(..., description="Readability score (0.0-1.0)")
    performance: float = Field(..., description="Performance impact score (0.0-1.0)")
    security: float = Field(..., description="Security score (0.0-1.0)")
    testability: float = Field(..., description="Testability score (0.0-1.0)")
    overall_score: float = Field(..., description="Overall quality score (0.0-1.0)")
    improvements: List[str] = Field(default_factory=list, description="Suggested improvements")
    issues: List[str] = Field(default_factory=list, description="Identified issues")


class ResolutionPlan(BaseModel):
    """Complete resolution plan for a conflict"""

    id: str = Field(..., description="Unique plan identifier")
    conflict_id: str = Field(..., description="ID of the conflict being resolved")
    conflict_type: ConflictTypeExtended = Field(..., description="Type of conflict")
    strategies: List[ResolutionStrategy] = Field(default_factory=list, description="Available resolution strategies")
    selected_strategy: Optional[str] = Field(None, description="ID of selected strategy")
    execution_status: ExecutionStatus = Field(ExecutionStatus.PENDING, description="Current execution status")
    progress: float = Field(0.0, description="Completion progress (0.0-1.0)")
    validation_results: List[ValidationResult] = Field(default_factory=list, description="Validation results")
    quality_metrics: Optional[QualityMetrics] = Field(None, description="Quality assessment")
    human_feedback: Optional[str] = Field(None, description="Human feedback on resolution")
    execution_log: List[Dict[str, Any]] = Field(default_factory=list, description="Execution log")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Plan creation time")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update time")
    timeout_seconds: int = Field(300, description="Timeout for resolution execution")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "plan_123",
                "conflict_id": "conflict_456",
                "conflict_type": "MERGE_CONFLICT",
                "strategies": [],
                "selected_strategy": "strategy_1",
                "execution_status": "IN_PROGRESS",
                "progress": 0.5,
                "validation_results": [],
                "quality_metrics": None,
                "execution_log": [],
                "timeout_seconds": 300,
            }
        }


# Conflict type definitions
class MergeConflict(BaseModel):
    """Merge conflict representation"""

    pr1_id: str = Field(..., description="First PR ID")
    pr2_id: str = Field(..., description="Second PR ID")
    file_path: str = Field(..., description="Conflicting file path")
    conflict_region: str = Field(..., description="Text region with conflicts")
    base_content: Optional[str] = Field(None, description="Base content before changes")
    content1: str = Field(..., description="First PR's content")
    content2: str = Field(..., description="Second PR's content")
    similarity_score: float = Field(..., description="Similarity between changes (0.0-1.0)")
    conflict_type: str = Field(..., description="Type of merge conflict")
    line_numbers: Dict[str, List[int]] = Field(..., description="Line numbers for each version")

    class Config:
        json_schema_extra = {
            "example": {
                "pr1_id": "pr_1",
                "pr2_id": "pr_2",
                "file_path": "src/main.py",
                "conflict_region": (
                    "<<<<<<< HEAD\\n"
                    "def new_function():\\n"
                    "    return 'version1'\\n"
                    "=======\\n"
                    "def new_function():\\n"
                    "    return 'version2'\\n"
                    ">>>>>>> feature-branch"
                ),
                "base_content": "def old_function():\n    return 'original'",
                "content1": "def new_function():\n    return 'version1'",
                "content2": "def new_function():\n    return 'version2'",
                "similarity_score": 0.8,
                "conflict_type": "content_modification",
                "line_numbers": {"pr1": [10, 15], "pr2": [10, 15], "base": [10, 15]},
            }
        }


class DependencyConflict(BaseModel):
    """Dependency conflict representation"""

    conflict_type: str = Field(..., description="Type of dependency conflict")
    affected_nodes: List[str] = Field(..., description="Affected dependency nodes")
    cycle_path: List[str] = Field(default_factory=list, description="Path in dependency cycle")
    version_conflicts: Dict[str, Any] = Field(default_factory=dict, description="Version conflict details")
    severity: ConflictSeverity = Field(..., description="Conflict severity")
    resolution_suggestions: List[str] = Field(default_factory=list, description="Suggested resolutions")

    class Config:
        json_schema_extra = {
            "example": {
                "conflict_type": "circular_dependency",
                "affected_nodes": ["module_a", "module_b", "module_c"],
                "cycle_path": ["module_a", "module_b", "module_c", "module_a"],
                "version_conflicts": {"package_x": {"pr1": "1.0.0", "pr2": "2.0.0"}},
                "severity": "HIGH",
                "resolution_suggestions": ["Refactor to break cycle", "Use dependency injection"],
            }
        }


class ArchitectureViolation(BaseModel):
    """Architecture violation representation"""

    violation_type: str = Field(..., description="Type of architecture violation")
    pattern_name: str = Field(..., description="Name of violated pattern")
    violating_prs: List[str] = Field(..., description="PRs that violate the pattern")
    description: str = Field(..., description="Description of the violation")
    affected_components: List[str] = Field(..., description="Affected system components")
    suggested_fix: Optional[str] = Field(None, description="Suggested architectural fix")
    severity: ConflictSeverity = Field(..., description="Violation severity")
    layer_violations: List[Dict[str, str]] = Field(default_factory=list, description="Specific layer violations")

    class Config:
        json_schema_extra = {
            "example": {
                "violation_type": "layer_violation",
                "pattern_name": "layered_architecture",
                "violating_prs": ["pr_123"],
                "description": "Presentation layer directly accessing database",
                "affected_components": ["UserInterface", "DatabaseAccess"],
                "suggested_fix": "Use service layer pattern",
                "severity": "CRITICAL",
                "layer_violations": [{"from": "UI", "to": "Database", "description": "Direct access"}],
            }
        }


class SemanticConflict(BaseModel):
    """Semantic conflict representation"""

    pr1_id: str = Field(..., description="First PR ID")
    pr2_id: str = Field(..., description="Second PR ID")
    conflict_area: str = Field(..., description="Area of semantic conflict")
    description: str = Field(..., description="Description of semantic incompatibility")
    confidence: float = Field(..., description="AI confidence in conflict detection")
    evidence: List[str] = Field(default_factory=list, description="Evidence for the conflict")
    resolution_suggestions: List[str] = Field(default_factory=list, description="Suggested resolutions")

    class Config:
        json_schema_extra = {
            "example": {
                "pr1_id": "pr_1",
                "pr2_id": "pr_2",
                "conflict_area": "function_logic",
                "description": "Functions implement opposite business logic",
                "confidence": 0.9,
                "evidence": ["pr1 returns success for condition A", "pr2 returns failure for condition A"],
                "resolution_suggestions": ["Refactor to use strategy pattern", "Combine logic with conditional"],
            }
        }


class ResourceConflict(BaseModel):
    """Resource conflict representation"""

    resource_type: str = Field(..., description="Type of resource")
    resource_id: str = Field(..., description="Resource identifier")
    conflicting_prs: List[str] = Field(..., description="PRs competing for resource")
    access_pattern: str = Field(..., description="How resources are being accessed")
    contention_level: str = Field(..., description="Level of resource contention")
    resolution_suggestions: List[str] = Field(default_factory=list, description="Suggested resolutions")

    class Config:
        json_schema_extra = {
            "example": {
                "resource_type": "database",
                "resource_id": "main_db",
                "conflicting_prs": ["pr_1", "pr_2", "pr_3"],
                "access_pattern": "concurrent_write",
                "contention_level": "HIGH",
                "resolution_suggestions": ["Use database transactions", "Implement queue-based access"],
            }
        }
