"""
Core data models for EmailIntelligence CLI

This module defines the data structures used throughout the system.
It re-exports existing types from src.resolution.types and adds new core models.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Re-export existing types
from ..resolution.types import (
    ConflictTypeExtended,
    RiskLevel,
    ExecutionStatus,
    ValidationStatus,
    CodeChange,
    ResolutionStep,
    ResolutionStrategy,
    ValidationResult,
    QualityMetrics,
    ResolutionPlan,
    MergeConflict,
    DependencyConflict,
    ArchitectureViolation,
    SemanticConflict,
    ResourceConflict,
)

__all__ = [
    # Re-exported types
    "ConflictTypeExtended",
    "RiskLevel",
    "ExecutionStatus",
    "ValidationStatus",
    "CodeChange",
    "ResolutionStep",
    "ResolutionStrategy",
    "ValidationResult",
    "QualityMetrics",
    "ResolutionPlan",
    "MergeConflict",
    "DependencyConflict",
    "ArchitectureViolation",
    "SemanticConflict",
    "ResourceConflict",
    # New types
    "ConflictBlock",
    "Conflict",
    "AnalysisResult",
]


class ConflictBlock(BaseModel):
    """
    Represents a specific block of conflicting code within a file.
    """
    file_path: str = Field(..., description="Path to the file containing the conflict")
    start_line: int = Field(..., description="Starting line number of the conflict block")
    end_line: int = Field(..., description="Ending line number of the conflict block")
    current_content: str = Field(..., description="Content in the current branch (ours)")
    incoming_content: str = Field(..., description="Content in the incoming branch (theirs)")
    base_content: Optional[str] = Field(None, description="Content in the base branch (ancestor)")
    conflict_marker_type: str = Field("git", description="Type of conflict marker (git, diff3, etc.)")


class Conflict(BaseModel):
    """
    Generic wrapper for any type of conflict.
    
    This model provides a unified interface for handling different conflict types
    (merge, dependency, semantic, etc.) in the core system.
    """
    id: str = Field(..., description="Unique conflict identifier")
    type: ConflictTypeExtended = Field(..., description="Type of conflict")
    severity: RiskLevel = Field(RiskLevel.MEDIUM, description="Severity/Risk level")
    description: str = Field(..., description="Human-readable description")
    file_paths: List[str] = Field(..., description="Files involved in the conflict")
    
    # Context
    pr_id: Optional[str] = Field(None, description="Pull Request ID")
    commit_sha: Optional[str] = Field(None, description="Commit SHA where conflict occurred")
    
    # Detailed data (polymorphic storage)
    details: Dict[str, Any] = Field(default_factory=dict, description="Type-specific conflict details")
    blocks: List[ConflictBlock] = Field(default_factory=list, description="Specific conflict blocks if applicable")
    
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    status: str = Field("OPEN", description="Current status (OPEN, RESOLVED, IGNORED)")


class AnalysisResult(BaseModel):
    """
    Result of a comprehensive conflict analysis.
    """
    conflict_id: str = Field(..., description="ID of the analyzed conflict")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")
    
    # Analysis metrics
    complexity_score: float = Field(..., description="Calculated complexity score (0-100)")
    risk_level: RiskLevel = Field(..., description="Assessed risk level")
    estimated_resolution_time_minutes: int = Field(..., description="Estimated time to resolve")
    
    # Classification
    is_auto_resolvable: bool = Field(..., description="Whether conflict can be auto-resolved")
    recommended_strategy_type: str = Field(..., description="Recommended resolution strategy type")
    
    # Detailed findings
    root_cause: str = Field(..., description="Identified root cause of the conflict")
    impact_analysis: Dict[str, Any] = Field(default_factory=dict, description="Impact on other components")
    constitutional_violations: List[str] = Field(default_factory=list, description="Violated constitutional rules")
    
    # AI insights
    ai_analysis: Optional[str] = Field(None, description="Free-text AI analysis summary")
    confidence_score: float = Field(..., description="Confidence in the analysis (0.0-1.0)")
