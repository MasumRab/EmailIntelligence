"""Verification-related models."""

from enum import Enum
from typing import Any, Optional, List
from pydantic import Field

from src.models.base import BaseModel


class VerificationStatus(str, Enum):
    """Verification result status."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    IN_PROGRESS = "in_progress"
    ERROR = "error"


class VerificationResult(BaseModel):
    """Model for verification results."""

    name: str = Field(..., description="Name of the verification")
    status: VerificationStatus = Field(..., description="Verification status")
    scenario: str = Field(..., description="Test scenario name")
    duration: float = Field(default=0.0, description="Execution duration in seconds")
    message: Optional[str] = Field(default=None, description="Status message")
    errors: List[str] = Field(default_factory=list, description="List of errors if any")
    warnings: List[str] = Field(default_factory=list, description="List of warnings if any")
    details: dict[str, Any] = Field(default_factory=dict, description="Additional details")
    correlation_id: str = Field(..., description="Correlation ID for tracing")

    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class VerificationProfile(BaseModel):
    """Model for verification profiles configuration."""

    name: str = Field(..., description="Profile name")
    description: Optional[str] = Field(default=None, description="Profile description")
    scenarios: List[str] = Field(default_factory=list, description="List of test scenarios")
    context_checks: List[str] = Field(default_factory=list, description="Context verification checks")
    branch_checks: List[str] = Field(default_factory=list, description="Branch validation checks")
    consistency_checks: List[str] = Field(default_factory=list, description="Consistency checks")
    timeout: int = Field(default=3600, description="Timeout in seconds")
    parallel: bool = Field(default=True, description="Run verifications in parallel")
    enabled: bool = Field(default=True, description="Profile enabled status")
