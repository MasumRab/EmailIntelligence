"""Goal and consistency tracking models."""

from typing import List, Optional, Dict, Any
from pydantic import Field

from src.models.base import BaseModel


class Goal(BaseModel):
    """Model representing a project goal."""

    name: str = Field(..., description="Goal name")
    description: str = Field(..., description="Goal description")
    status: str = Field(default="pending", description="Goal status")
    priority: str = Field(default="medium", description="Goal priority (high/medium/low)")
    related_tasks: List[str] = Field(default_factory=list, description="IDs of related tasks")
    success_criteria: List[str] = Field(default_factory=list, description="Success criteria")
    owner: Optional[str] = Field(default=None, description="Goal owner")
    target_date: Optional[str] = Field(default=None, description="Target completion date")


class Task(BaseModel):
    """Model representing a task."""

    name: str = Field(..., description="Task name")
    description: str = Field(..., description="Task description")
    status: str = Field(default="pending", description="Task status")
    priority: str = Field(default="medium", description="Task priority")
    goal_id: Optional[str] = Field(default=None, description="Associated goal ID")
    dependencies: List[str] = Field(default_factory=list, description="Task dependencies")
    owner: Optional[str] = Field(default=None, description="Task owner")
    estimated_effort: Optional[int] = Field(default=None, description="Estimated effort hours")
    actual_effort: Optional[int] = Field(default=None, description="Actual effort hours")


class GoalTaskAlignment(BaseModel):
    """Model for goal-task alignment check."""

    goal_id: str = Field(..., description="Goal ID")
    aligned_tasks: List[str] = Field(default_factory=list, description="Aligned task IDs")
    unaligned_tasks: List[str] = Field(default_factory=list, description="Unaligned task IDs")
    alignment_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Alignment score (0-1)"
    )
    issues: List[str] = Field(default_factory=list, description="Alignment issues")


class ConsistencyCheckResult(BaseModel):
    """Result of a consistency check."""

    check_type: str = Field(..., description="Type of consistency check")
    status: str = Field(..., description="Check status (passed/failed)")
    issues: List[str] = Field(default_factory=list, description="Issues found")
    details: Dict[str, Any] = Field(default_factory=dict, description="Check details")
