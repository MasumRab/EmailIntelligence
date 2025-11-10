"""Branch and git-related models."""

from typing import List, Optional, Dict, Any
from pydantic import Field

from src.models.base import BaseModel


class Branch(BaseModel):
    """Model representing a Git branch."""

    name: str = Field(..., description="Branch name")
    remote: Optional[str] = Field(default=None, description="Remote name (e.g., origin)")
    commit_hash: str = Field(..., description="Latest commit hash")
    last_commit_date: Optional[str] = Field(default=None, description="Last commit date")
    is_local: bool = Field(default=True, description="Is local branch")
    is_remote: bool = Field(default=False, description="Is remote branch")
    upstream: Optional[str] = Field(default=None, description="Upstream branch")
    ahead: int = Field(default=0, description="Commits ahead of upstream")
    behind: int = Field(default=0, description="Commits behind upstream")


class BranchCompatibility(BaseModel):
    """Model for branch compatibility check."""

    source_branch: str = Field(..., description="Source branch name")
    target_branch: str = Field(..., description="Target branch name")
    compatible: bool = Field(..., description="Compatibility status")
    conflicts: List[str] = Field(default_factory=list, description="Conflicting files")
    issues: List[str] = Field(default_factory=list, description="Compatibility issues")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")


class BranchStatus(BaseModel):
    """Status information for a branch."""

    branch_name: str = Field(..., description="Branch name")
    exists: bool = Field(..., description="Whether branch exists")
    is_up_to_date: bool = Field(..., description="Whether up to date with remote")
    has_changes: bool = Field(..., description="Whether has uncommitted changes")
    changed_files: List[str] = Field(default_factory=list, description="Changed file paths")
    status_details: Dict[str, Any] = Field(default_factory=dict, description="Status details")
