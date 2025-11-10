"""Context and verification-related models."""

from enum import Enum
from typing import Any, Optional, List, Dict
from pydantic import Field

from src.models.base import BaseModel


class ContextType(str, Enum):
    """Type of context to verify."""

    ENVIRONMENT_VARIABLES = "environment_variables"
    DEPENDENCY_VERSIONS = "dependency_versions"
    CONFIGURATION_FILES = "configuration_files"
    INFRASTRUCTURE_STATE = "infrastructure_state"
    GIT_STATE = "git_state"
    BRANCH_STATE = "branch_state"
    PERMISSIONS = "permissions"


class ContextVerification(BaseModel):
    """Model for context verification."""

    context_type: ContextType = Field(..., description="Type of context being verified")
    status: str = Field(..., description="Verification status (passed/failed)")
    checks: List[str] = Field(default_factory=list, description="List of checks performed")
    passed_checks: int = Field(default=0, description="Number of passed checks")
    failed_checks: int = Field(default=0, description="Number of failed checks")
    errors: List[str] = Field(default_factory=list, description="Detailed errors")
    warnings: List[str] = Field(default_factory=list, description="Warnings")
    details: Dict[str, Any] = Field(default_factory=dict, description="Detailed results")
    correlation_id: str = Field(..., description="Correlation ID for tracing")


class EnvironmentVariable(BaseModel):
    """Single environment variable check."""

    name: str = Field(..., description="Variable name")
    required: bool = Field(default=True, description="Whether variable is required")
    expected_type: Optional[str] = Field(default=None, description="Expected value type")
    validation_rule: Optional[str] = Field(default=None, description="Regex or validation rule")
    value: Optional[str] = Field(default=None, description="Current value")
    status: str = Field(default="unchecked", description="Check status")


class DependencyVersion(BaseModel):
    """Package dependency version check."""

    package_name: str = Field(..., description="Package name")
    current_version: Optional[str] = Field(default=None, description="Currently installed version")
    required_version: str = Field(..., description="Required version constraint")
    status: str = Field(default="unchecked", description="Check status")
    compatible: bool = Field(default=False, description="Compatibility status")


class ConfigurationFile(BaseModel):
    """Configuration file check."""

    file_path: str = Field(..., description="Path to configuration file")
    exists: bool = Field(default=False, description="Whether file exists")
    valid: bool = Field(default=False, description="Whether file is valid")
    format: str = Field(..., description="File format (yaml, json, etc.)")
    validation_errors: List[str] = Field(default_factory=list, description="Validation errors")
    required: bool = Field(default=True, description="Whether file is required")


class InfrastructureState(BaseModel):
    """Infrastructure state check."""

    component: str = Field(..., description="Infrastructure component name")
    status: str = Field(..., description="Component status (running/stopped/error)")
    health_check: bool = Field(default=False, description="Health check result")
    details: Dict[str, Any] = Field(default_factory=dict, description="Component-specific details")
    last_checked: Optional[str] = Field(default=None, description="Last health check timestamp")
