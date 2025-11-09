"""Base data models for Agent Context Control library."""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ProjectConfig(BaseModel):
    """Project-specific configuration settings."""

    # Project identification
    project_name: str = Field(..., description="Name of the project")
    project_type: str = Field(..., description="Type of project (web, api, library, etc.)")

    # Agent behavior settings
    max_context_length: int = Field(
        default=4096,
        description="Maximum context length for agents"
    )
    enable_code_execution: bool = Field(
        default=False,
        description="Whether agents can execute code"
    )
    enable_file_writing: bool = Field(
        default=False,
        description="Whether agents can write files"
    )
    enable_shell_commands: bool = Field(
        default=False,
        description="Whether agents can run shell commands"
    )

    # Model preferences
    preferred_models: List[str] = Field(
        default_factory=lambda: ["gpt-4", "claude-3"],
        description="Preferred AI models for this project"
    )

    # Custom agent settings
    custom_settings: Dict[str, Any] = Field(
        default_factory=dict,
        description="Project-specific custom settings"
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ContextProfile(BaseModel):
    """Represents a context profile configuration."""

    id: str = Field(..., description="Unique identifier for the context profile")
    name: str = Field(..., description="Human-readable name for the profile")
    description: Optional[str] = Field(None, description="Optional description of the profile")

    # Environment mapping
    branch_patterns: List[str] = Field(
        default_factory=list,
        description="Git branch patterns that match this profile"
    )

    # Context content
    allowed_files: List[str] = Field(
        default_factory=list,
        description="File patterns that agents can access"
    )
    blocked_files: List[str] = Field(
        default_factory=list,
        description="File patterns that agents cannot access"
    )

    # Agent behavior configuration
    agent_settings: Dict[str, Any] = Field(
        default_factory=dict,
        description="Agent-specific configuration settings"
    )

    # Project configuration (User Story 2)
    project_config: Optional[ProjectConfig] = Field(
        default=None,
        description="Project-specific configuration settings"
    )

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(default="1.0.0", description="Profile version")

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentContext(BaseModel):
    """Represents the runtime context for an agent."""

    profile_id: str = Field(..., description="ID of the active context profile")
    agent_id: str = Field(..., description="Unique identifier for the agent")

    # Environment information
    branch_name: Optional[str] = Field(None, description="Current Git branch name")
    environment_type: str = Field(..., description="Type of environment (dev, staging, prod)")

    # Context boundaries
    accessible_files: List[str] = Field(
        default_factory=list,
        description="Files the agent can currently access"
    )
    restricted_files: List[str] = Field(
        default_factory=list,
        description="Files the agent cannot access"
    )

    # Project configuration (User Story 2)
    profile_config: Optional[ProjectConfig] = Field(
        default=None,
        description="Project-specific configuration settings"
    )

    # Agent settings (inherited from profile)
    agent_settings: Dict[str, Any] = Field(
        default_factory=dict,
        description="Agent-specific configuration settings"
    )

    # Runtime state
    is_active: bool = Field(default=True, description="Whether this context is currently active")
    activated_at: datetime = Field(default_factory=datetime.utcnow)
    last_validated: Optional[datetime] = Field(None)

    # Security tracking
    access_log: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Log of file access attempts"
    )

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ContextValidationResult(BaseModel):
    """Result of context validation operations."""

    is_valid: bool = Field(..., description="Whether the context is valid")
    errors: List[str] = Field(default_factory=list, description="Validation error messages")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")

    # Additional metadata
    validated_at: datetime = Field(default_factory=datetime.utcnow)
    context_id: Optional[str] = Field(None, description="ID of the validated context")