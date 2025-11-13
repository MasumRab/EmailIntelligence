"""
Graph model entities for PR Resolution Automation System
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class PRStatus(str, Enum):
    OPEN = "OPEN"
    IN_REVIEW = "IN_REVIEW"
    CONFLICT_DETECTED = "CONFLICT_DETECTED"
    RESOLVING = "RESOLVING"
    READY_TO_MERGE = "READY_TO_MERGE"
    MERGED = "MERGED"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"


class ConflictType(str, Enum):
    MERGE_CONFLICT = "MERGE_CONFLICT"
    DEPENDENCY_CONFLICT = "DEPENDENCY_CONFLICT"
    ARCHITECTURE_VIOLATION = "ARCHITECTURE_VIOLATION"
    TEST_FAILURE = "TEST_FAILURE"
    CODE_STYLE_VIOLATION = "CODE_STYLE_VIOLATION"
    SECURITY_VIOLATION = "SECURITY_VIOLATION"
    PERFORMANCE_ISSUE = "PERFORMANCE_ISSUE"


class ConflictSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class ResolutionStrategy(str, Enum):
    AUTOMATIC = "AUTOMATIC"
    SEMI_AUTOMATIC = "SEMI_AUTOMATIC"
    MANUAL = "MANUAL"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"
    BLOCKED = "BLOCKED"


class ResolutionMethod(str, Enum):
    AI_RESOLVED = "AI_RESOLVED"
    SUGGESTED_MERGE = "SUGGESTED_MERGE"
    REBASE_REQUIRED = "REBASE_REQUIRED"
    MANUAL_INTERVENTION = "MANUAL_INTERVENTION"
    ARCHITECTURE_REFACTOR = "ARCHITECTURE_REFACTOR"


class ChangeType(str, Enum):
    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"
    RENAMED = "RENAMED"


class IssueSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class IssueStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class Node(BaseModel):
    """Base model for all graph nodes"""

    id: str = Field(..., description="Unique identifier for the node")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class PullRequest(Node):
    """Pull Request model"""

    title: str = Field(..., description="PR title")
    description: Optional[str] = Field(None, description="PR description")
    source_branch: str = Field(..., description="Source branch name")
    target_branch: str = Field(..., description="Target branch name")
    status: PRStatus = Field(default=PRStatus.OPEN, description="PR status")
    complexity: float = Field(default=0.0, description="Complexity score (0.0-1.0)")
    estimated_resolution_time: int = Field(default=0, description="Estimated resolution time in minutes")
    author_id: str = Field(..., description="Author node ID")
    reviewer_ids: List[str] = Field(default_factory=list, description="Reviewer node IDs")
    file_ids: List[str] = Field(default_factory=list, description="File node IDs")
    commit_ids: List[str] = Field(default_factory=list, description="Commit node IDs")
    conflict_ids: List[str] = Field(default_factory=list, description="Conflict node IDs")


class Commit(Node):
    """Commit model"""

    sha: str = Field(..., description="Git commit SHA")
    message: str = Field(..., description="Commit message")
    author_id: str = Field(..., description="Author node ID")
    timestamp: datetime = Field(..., description="Commit timestamp")
    parent_id: Optional[str] = Field(None, description="Parent commit ID")
    child_ids: List[str] = Field(default_factory=list, description="Child commit IDs")
    file_change_ids: List[str] = Field(default_factory=list, description="File change IDs")
    conflict_ids: List[str] = Field(default_factory=list, description="Conflict IDs")


class File(Node):
    """File model"""

    path: str = Field(..., description="File path")
    content: Optional[str] = Field(None, description="File content")
    language: str = Field(..., description="Programming language")
    size: int = Field(..., description="File size in bytes")
    last_modified: datetime = Field(..., description="Last modification time")
    file_change_ids: List[str] = Field(default_factory=list, description="File change IDs")
    conflict_ids: List[str] = Field(default_factory=list, description="Conflict IDs")


class Developer(Node):
    """Developer model"""

    name: str = Field(..., description="Developer name")
    email: str = Field(..., description="Developer email")
    github_username: Optional[str] = Field(None, description="GitHub username")
    expertise: List[str] = Field(default_factory=list, description="Areas of expertise")
    commit_ids: List[str] = Field(default_factory=list, description="Commit IDs")
    assigned_pr_ids: List[str] = Field(default_factory=list, description="Assigned PR IDs")
    conflict_history_ids: List[str] = Field(default_factory=list, description="Conflict history IDs")


class Issue(Node):
    """Issue model"""

    title: str = Field(..., description="Issue title")
    description: Optional[str] = Field(None, description="Issue description")
    severity: IssueSeverity = Field(..., description="Issue severity")
    status: IssueStatus = Field(default=IssueStatus.OPEN, description="Issue status")
    related_pr_ids: List[str] = Field(default_factory=list, description="Related PR IDs")
    conflict_ids: List[str] = Field(default_factory=list, description="Conflict IDs")


class Conflict(Node):
    """Conflict model"""

    type: ConflictType = Field(..., description="Type of conflict")
    severity: ConflictSeverity = Field(..., description="Conflict severity")
    description: str = Field(..., description="Conflict description")
    detected_at: datetime = Field(default_factory=datetime.utcnow, description="Detection timestamp")
    affected_file_ids: List[str] = Field(default_factory=list, description="Affected file IDs")
    affected_commit_ids: List[str] = Field(default_factory=list, description="Affected commit IDs")
    resolution_id: Optional[str] = Field(None, description="Resolution ID")
    ai_analysis_id: Optional[str] = Field(None, description="AI analysis ID")


class FileChange(BaseModel):
    """File Change model (edge type)"""

    type: ChangeType = Field(..., description="Type of change")
    file_id: str = Field(..., description="File node ID")
    old_content: Optional[str] = Field(None, description="Old file content")
    new_content: Optional[str] = Field(None, description="New file content")
    diff: str = Field(..., description="Diff representation")
    line_number: Optional[int] = Field(None, description="Line number where change occurred")


class PRResolution(BaseModel):
    """PR Resolution model"""

    id: str = Field(..., description="Resolution ID")
    strategy: ResolutionStrategy = Field(..., description="Resolution strategy")
    description: str = Field(..., description="Resolution description")
    applied_at: datetime = Field(default_factory=datetime.utcnow, description="Application timestamp")
    applied_by_id: str = Field(..., description="Resolver node ID")
    success: bool = Field(..., description="Resolution success status")
    feedback: Optional[str] = Field(None, description="Resolution feedback")


class ConflictResolution(BaseModel):
    """Conflict Resolution model"""

    id: str = Field(..., description="Resolution ID")
    method: ResolutionMethod = Field(..., description="Resolution method")
    description: str = Field(..., description="Resolution description")
    applied_at: datetime = Field(default_factory=datetime.utcnow, description="Application timestamp")
    confidence: float = Field(..., description="Resolution confidence (0.0-1.0)")
    ai_generated: bool = Field(default=False, description="AI-generated resolution")


class AIAnalysis(BaseModel):
    """AI Analysis model"""

    id: str = Field(..., description="Analysis ID")
    conflict_type: str = Field(..., description="Analyzed conflict type")
    complexity: float = Field(..., description="Complexity score (0.0-1.0)")
    resolution_suggestions: List[str] = Field(default_factory=list, description="Resolution suggestions")
    estimated_time: int = Field(..., description="Estimated resolution time in minutes")
    confidence: float = Field(..., description="AI confidence (0.0-1.0)")
    model: str = Field(..., description="AI model used")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


# Input models for mutations
class CreatePRInput(BaseModel):
    """Input for creating a PR"""

    title: str = Field(..., description="PR title")
    description: Optional[str] = Field(None, description="PR description")
    source_branch: str = Field(..., description="Source branch")
    target_branch: str = Field(..., description="Target branch")
    author_id: str = Field(..., description="Author node ID")


class UpdatePRStatusInput(BaseModel):
    """Input for updating PR status"""

    pr_id: str = Field(..., description="PR node ID")
    status: PRStatus = Field(..., description="New status")


class ResolveConflictInput(BaseModel):
    """Input for resolving conflicts"""

    conflict_id: str = Field(..., description="Conflict node ID")
    method: ResolutionMethod = Field(..., description="Resolution method")
    description: str = Field(..., description="Resolution description")


# Response models
class ProcessResult(BaseModel):
    """Process result for PR processing"""

    success: bool = Field(..., description="Process success status")
    message: str = Field(..., description="Result message")
    processing_time: float = Field(..., description="Processing time in seconds")
    conflicts_detected: int = Field(default=0, description="Number of conflicts detected")


class EscalationResult(BaseModel):
    """Escalation result"""

    success: bool = Field(..., description="Escalation success status")
    escalated_to: str = Field(..., description="Escalation target")
    reason: str = Field(..., description="Escalation reason")


class TrendPoint(BaseModel):
    """Trend data point"""

    timestamp: datetime = Field(..., description="Data point timestamp")
    value: float = Field(..., description="Trend value")
    label: str = Field(..., description="Data point label")


class WorkloadAnalysis(BaseModel):
    """Developer workload analysis"""

    current_prs: int = Field(..., description="Current assigned PRs")
    average_resolution_time: float = Field(..., description="Average resolution time in hours")
    expertise_score: float = Field(..., description="Expertise score (0.0-1.0)")
    conflict_rate: float = Field(..., description="Conflict rate (0.0-1.0)")


class Pattern(BaseModel):
    """Pattern analysis"""

    pattern_type: str = Field(..., description="Pattern type")
    frequency: int = Field(..., description="Pattern frequency")
    description: str = Field(..., description="Pattern description")
    confidence: float = Field(..., description="Pattern confidence")


class SystemHealth(BaseModel):
    """System health status"""

    status: str = Field(..., description="Overall system status")
    services: dict = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")
    uptime: float = Field(..., description="System uptime in seconds")
