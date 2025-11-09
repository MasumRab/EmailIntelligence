# Data Models: Agent Context Control

**Date**: 2025-11-10 | **Spec**: specs/001-agent-context-control/spec.md | **Research**: specs/001-agent-context-control/research.md

## Overview

This document defines the data models and schemas for the Agent Context Control system. All models follow Python type hints and Pydantic validation patterns for runtime type checking and data validation.

## Core Data Models

### ContextProfile

The primary data model representing an agent's context configuration for a specific branch/environment.

```python
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    CI = "ci"

class ContextProfile(BaseModel):
    """Agent context profile for branch-based configuration."""

    context_id: str = Field(..., description="Unique identifier for this context")
    branch: str = Field(..., description="Git branch name this context applies to")
    environment: Environment = Field(..., description="Deployment environment")

    agent_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Agent-specific configuration parameters"
    )

    api_keys: Dict[str, str] = Field(
        default_factory=dict,
        description="Environment-specific API keys (should be encrypted)"
    )

    feature_flags: Dict[str, bool] = Field(
        default_factory=dict,
        description="Feature toggles for this context"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for context management"
    )

    created_at: Optional[str] = Field(None, description="ISO 8601 creation timestamp")
    updated_at: Optional[str] = Field(None, description="ISO 8601 last update timestamp")

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        json_encoders = {
            # Custom JSON encoders if needed
        }

    @validator('context_id')
    def validate_context_id(cls, v):
        """Validate context ID format."""
        if not v or not isinstance(v, str):
            raise ValueError("context_id must be a non-empty string")
        if len(v) > 100:
            raise ValueError("context_id must be 100 characters or less")
        # Allow alphanumeric, hyphens, and underscores
        import re
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError("context_id must contain only alphanumeric characters, hyphens, and underscores")
        return v

    @validator('branch')
    def validate_branch(cls, v):
        """Validate branch name format."""
        if not v or not isinstance(v, str):
            raise ValueError("branch must be a non-empty string")
        if len(v) > 255:
            raise ValueError("branch must be 255 characters or less")
        # Git branch name validation (simplified)
        forbidden_chars = [' ', '..', '~', '^', ':', '\\', '*', '?', '[', ']']
        if any(char in v for char in forbidden_chars):
            raise ValueError(f"branch contains forbidden characters: {forbidden_chars}")
        return v
```

### BranchDetectionResult

Result of branch detection operations.

```python
class BranchDetectionResult(BaseModel):
    """Result of branch detection operation."""

    branch_name: Optional[str] = Field(None, description="Detected branch name")
    commit_hash: Optional[str] = Field(None, description="Current commit hash (full SHA)")
    is_detached: bool = Field(..., description="Whether HEAD is in detached state")
    context_id: str = Field(..., description="Resolved context identifier")
    detection_method: str = Field(..., description="Method used for detection")

    detection_timestamp: str = Field(..., description="ISO 8601 timestamp of detection")
    repository_path: str = Field(..., description="Path to the repository")

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
```

### ContextValidationResult

Result of context validation operations.

```python
class ValidationError(BaseModel):
    """Individual validation error."""
    field: str = Field(..., description="Field that failed validation")
    error_type: str = Field(..., description="Type of validation error")
    message: str = Field(..., description="Human-readable error message")
    value: Any = Field(None, description="Invalid value that caused the error")

class ContextValidationResult(BaseModel):
    """Result of context validation operation."""

    is_valid: bool = Field(..., description="Whether the context is valid")
    errors: List[ValidationError] = Field(default_factory=list, description="List of validation errors")
    warnings: List[str] = Field(default_factory=list, description="Non-blocking validation warnings")

    validated_at: str = Field(..., description="ISO 8601 timestamp of validation")
    schema_version: str = Field(..., description="Schema version used for validation")

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
```

### AgentContext

Runtime context object provided to agents.

```python
class AgentContext(BaseModel):
    """Runtime context provided to agents."""

    context_id: str = Field(..., description="Context identifier")
    environment: Environment = Field(..., description="Current environment")

    # Agent configuration
    max_concurrent_tasks: int = Field(default=5, ge=1, description="Maximum concurrent tasks")
    timeout_seconds: int = Field(default=300, ge=1, description="Default timeout in seconds")
    memory_limit_mb: int = Field(default=1024, ge=1, description="Memory limit in MB")

    # Feature flags
    feature_flags: Dict[str, bool] = Field(default_factory=dict, description="Active feature flags")

    # Environment variables (filtered and sanitized)
    env_vars: Dict[str, str] = Field(default_factory=dict, description="Allowed environment variables")

    # Metadata
    branch_info: Dict[str, Any] = Field(default_factory=dict, description="Branch detection information")
    created_at: str = Field(..., description="Context creation timestamp")

    class Config:
        """Pydantic configuration."""
        validate_assignment = True

    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature flag is enabled."""
        return self.feature_flags.get(feature, False)

    def get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get an environment variable value."""
        return self.env_vars.get(key, default)
```

## Storage Models

### ContextFile

Represents a context profile stored on disk.

```python
from pathlib import Path

class ContextFile(BaseModel):
    """Context profile file on disk."""

    file_path: Path = Field(..., description="Absolute path to context file")
    profile: ContextProfile = Field(..., description="Loaded context profile")
    file_hash: str = Field(..., description="SHA256 hash of file contents")
    last_modified: str = Field(..., description="ISO 8601 last modified timestamp")

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True  # Allow Path objects

    @classmethod
    def from_file(cls, file_path: Path) -> 'ContextFile':
        """Load context file from disk."""
        import hashlib
        import json
        from datetime import datetime

        if not file_path.exists():
            raise FileNotFoundError(f"Context file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Calculate hash
        file_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

        # Parse JSON
        data = json.loads(content)

        # Create profile
        profile = ContextProfile(**data)

        # Get modification time
        stat = file_path.stat()
        last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()

        return cls(
            file_path=file_path,
            profile=profile,
            file_hash=file_hash,
            last_modified=last_modified
        )
```

## Configuration Models

### ContextControlConfig

Main configuration for the context control system.

```python
class ContextControlConfig(BaseModel):
    """Main configuration for context control system."""

    # Storage configuration
    context_dir: Path = Field(
        default=Path(".agent-context"),
        description="Directory for context profile storage"
    )

    # Security configuration
    encryption_enabled: bool = Field(
        default=True,
        description="Whether to encrypt sensitive data in context files"
    )

    encryption_key: Optional[str] = Field(
        None,
        description="Encryption key for sensitive data (required if encryption_enabled)"
    )

    # Performance configuration
    cache_enabled: bool = Field(
        default=True,
        description="Whether to cache context profiles in memory"
    )

    cache_ttl_seconds: int = Field(
        default=300,
        ge=0,
        description="Cache time-to-live in seconds"
    )

    # Validation configuration
    strict_validation: bool = Field(
        default=True,
        description="Whether to enforce strict schema validation"
    )

    schema_version: str = Field(
        default="1.0.0",
        description="Expected schema version for context profiles"
    )

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True  # Allow Path objects

    @validator('encryption_key')
    def validate_encryption_key(cls, v, values):
        """Validate encryption key when encryption is enabled."""
        if values.get('encryption_enabled', True) and not v:
            raise ValueError("encryption_key is required when encryption_enabled is True")
        if v and len(v) < 32:
            raise ValueError("encryption_key must be at least 32 characters for security")
        return v
```

## Error Models

### ContextControlError

Base exception class for context control operations.

```python
class ContextControlError(Exception):
    """Base exception for context control operations."""

    def __init__(self, message: str, error_code: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}

class BranchDetectionError(ContextControlError):
    """Error during branch detection."""
    pass

class ContextValidationError(ContextControlError):
    """Error during context validation."""
    pass

class ContextIsolationError(ContextControlError):
    """Error during context isolation."""
    pass

class ConfigurationError(ContextControlError):
    """Error in system configuration."""
    pass
```

## Schema Definitions

### JSON Schema for ContextProfile

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ContextProfile",
  "type": "object",
  "properties": {
    "context_id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 100,
      "pattern": "^[a-zA-Z0-9_-]+$",
      "description": "Unique identifier for this context"
    },
    "branch": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "not": {
        "pattern": "[ ..~^:\\\\*\\?\\[\\]]"
      },
      "description": "Git branch name this context applies to"
    },
    "environment": {
      "type": "string",
      "enum": ["development", "staging", "production", "ci"],
      "description": "Deployment environment"
    },
    "agent_config": {
      "type": "object",
      "description": "Agent-specific configuration parameters",
      "additionalProperties": true
    },
    "api_keys": {
      "type": "object",
      "description": "Environment-specific API keys",
      "additionalProperties": {
        "type": "string"
      }
    },
    "feature_flags": {
      "type": "object",
      "description": "Feature toggles for this context",
      "additionalProperties": {
        "type": "boolean"
      }
    },
    "metadata": {
      "type": "object",
      "description": "Additional metadata",
      "additionalProperties": true
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 creation timestamp"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 last update timestamp"
    }
  },
  "required": ["context_id", "branch", "environment"]
}
```

## Data Flow Diagrams

### Context Resolution Flow

```
Branch Detection → Context ID Resolution → Profile Loading → Validation → Agent Context Creation
       ↓              ↓                        ↓            ↓              ↓
    GitPython     Environment         File System    Schema      Runtime Object
   Operations     Variables           Access       Validation     Creation
```

### Context Storage Flow

```
Agent Context → Validation → Serialization → Encryption → File Storage → Hash Calculation
       ↓            ↓            ↓            ↓            ↓            ↓
  Runtime Data   Schema Check   JSON Format   AES-256      .json File   Integrity Check
```

## Migration & Versioning

### Schema Versioning

- **v1.0.0**: Initial schema with basic context profile structure
- **v1.1.0**: Added metadata field for extensibility
- **v1.2.0**: Added encryption support for sensitive data

### Migration Strategy

```python
def migrate_context_profile(data: dict, from_version: str, to_version: str) -> dict:
    """Migrate context profile data between schema versions."""

    migrations = {
        ("1.0.0", "1.1.0"): lambda d: {**d, "metadata": d.get("metadata", {})},
        ("1.1.0", "1.2.0"): lambda d: {**d, "encrypted": False}
    }

    key = (from_version, to_version)
    if key in migrations:
        return migrations[key](data)

    raise ValueError(f"No migration path from {from_version} to {to_version}")
```

## Performance Considerations

### Memory Usage

- **ContextProfile**: ~1-5KB per profile (depending on configuration size)
- **AgentContext**: ~2-10KB per active context
- **Caching**: LRU cache with configurable TTL to balance memory vs performance

### Serialization Performance

- **JSON**: Fast serialization/deserialization for most use cases
- **YAML**: Human-readable format for configuration files
- **Binary**: Consider msgpack for high-performance scenarios

### Validation Performance

- **Pydantic**: Fast validation with compiled schemas
- **JSON Schema**: Additional validation layer for complex rules
- **Caching**: Cache validation results for repeated operations