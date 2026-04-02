"""
Tests for security validator functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.core.security_validator import (
    NodeSecurityValidator,
    WorkflowSecurityValidator,
    SecurityLevel,
    ValidationResult,
)


class TestNodeSecurityValidator:
    """Test the NodeSecurityValidator class."""

    def test_validator_creation(self):
        """Test NodeSecurityValidator instance creation."""
        validator = NodeSecurityValidator()
        assert validator is not None

    def test_validate_with_default_level(self):
        """Test validation with default security level."""
        validator = NodeSecurityValidator()
        result = validator.validate_node("test_node", "safe")
        assert result is not None


class TestWorkflowSecurityValidator:
    """Test WorkflowSecurityValidator."""

    def test_validator_creation(self):
        """Test WorkflowSecurityValidator instance creation."""
        validator = WorkflowSecurityValidator()
        assert validator is not None

    def test_validate_workflow(self):
        """Test workflow validation."""
        validator = WorkflowSecurityValidator()
        result = validator.validate_workflow({"nodes": [], "connections": []})
        assert result is not None


class TestSecurityLevelEnum:
    """Test SecurityLevel enum."""

    def test_security_level_values(self):
        """Test SecurityLevel enum values."""
        assert SecurityLevel.PUBLIC.value == "public"
        assert SecurityLevel.INTERNAL.value == "internal"
        assert SecurityLevel.CONFIDENTIAL.value == "confidential"
        assert SecurityLevel.RESTRICTED.value == "restricted"


class TestValidationResult:
    """Test ValidationResult."""

    def test_validation_result_creation(self):
        """Test ValidationResult creation."""
        result = ValidationResult(valid=True, message="OK")
        assert result.valid is True
        assert result.message == "OK"

    def test_validation_result_with_errors(self):
        """Test ValidationResult with errors."""
        result = ValidationResult(valid=False, message="Error", errors=["error1"])
        assert result.valid is False
        assert "error1" in result.errors