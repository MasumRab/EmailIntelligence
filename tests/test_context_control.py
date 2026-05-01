"""
Tests for context_control module - Context Control functionality
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from src.context_control.models import (
    ProjectConfig,
    ContextProfile,
    AgentContext,
    ContextValidationResult,
)
from src.context_control.exceptions import (
    ContextControlError,
    ContextNotFoundError,
    ContextValidationError,
    ContextIsolationError,
    ConfigurationError,
    EnvironmentDetectionError,
    StorageError,
)


class TestProjectConfig:
    """Tests for ProjectConfig model"""

    def test_project_config_valid_creation(self):
        """Test creating a valid ProjectConfig"""
        config = ProjectConfig(
            project_name="TestProject",
            project_type="web",
        )
        assert config.project_name == "TestProject"
        assert config.project_type == "web"
        assert config.max_context_length == 4096  # default
        assert config.enable_code_execution is False  # default

    def test_project_config_custom_settings(self):
        """Test ProjectConfig with custom settings"""
        config = ProjectConfig(
            project_name="CustomProject",
            project_type="api",
            enable_code_execution=True,
            enable_file_writing=True,
            preferred_models=["gpt-4", "claude-3"],
        )
        assert config.enable_code_execution is True
        assert config.enable_file_writing is True
        assert "gpt-4" in config.preferred_models

    def test_project_config_requires_name_and_type(self):
        """Test that project_name and project_type are required"""
        with pytest.raises(ValidationError):
            ProjectConfig(project_name="Test")

    def test_project_config_default_values(self):
        """Test default values"""
        config = ProjectConfig(
            project_name="Test",
            project_type="web",
        )
        assert config.max_context_length == 4096
        assert config.enable_code_execution is False
        assert config.enable_file_writing is False
        assert config.enable_shell_commands is False
        assert config.created_at is not None
        assert config.updated_at is not None


class TestContextProfile:
    """Tests for ContextProfile model"""

    def test_context_profile_valid_creation(self):
        """Test creating a valid ContextProfile"""
        profile = ContextProfile(
            id="test-profile-1",
            name="Test Profile",
            description="A test profile",
        )
        assert profile.id == "test-profile-1"
        assert profile.name == "Test Profile"
        assert profile.description == "A test profile"
        assert profile.version == "1.0.0"  # default

    def test_context_profile_with_project_config(self):
        """Test ContextProfile with ProjectConfig"""
        project_config = ProjectConfig(
            project_name="TestProject",
            project_type="web",
            enable_code_execution=True,
        )
        profile = ContextProfile(
            id="test-profile-2",
            name="Profile with Config",
            project_config=project_config,
        )
        assert profile.project_config is not None
        assert profile.project_config.enable_code_execution is True

    def test_context_profile_with_branch_patterns(self):
        """Test ContextProfile with branch patterns"""
        profile = ContextProfile(
            id="test-profile-3",
            name="Branch Profile",
            branch_patterns=["feature/*", "bugfix/*"],
        )
        assert "feature/*" in profile.branch_patterns
        assert "bugfix/*" in profile.branch_patterns


class TestAgentContext:
    """Tests for AgentContext model"""

    def test_agent_context_valid_creation(self):
        """Test creating a valid AgentContext"""
        context = AgentContext(
            profile_id="test-profile-1",
            agent_id="agent-123",
            environment_type="dev",
        )
        assert context.profile_id == "test-profile-1"
        assert context.agent_id == "agent-123"
        assert context.environment_type == "dev"
        assert context.is_active is True  # default

    def test_agent_context_with_files(self):
        """Test AgentContext with file restrictions"""
        context = AgentContext(
            profile_id="test-profile-1",
            agent_id="agent-456",
            environment_type="staging",
            accessible_files=["src/*.py", "tests/*.py"],
            restricted_files=["*.env", "secrets/*"],
        )
        assert len(context.accessible_files) == 2
        assert len(context.restricted_files) == 2

    def test_agent_context_with_project_config(self):
        """Test AgentContext with ProjectConfig"""
        project_config = ProjectConfig(
            project_name="TestProject",
            project_type="library",
        )
        context = AgentContext(
            profile_id="test-profile-1",
            agent_id="agent-789",
            environment_type="prod",
            profile_config=project_config,
        )
        assert context.profile_config is not None
        assert context.profile_config.project_name == "TestProject"


class TestContextValidationResult:
    """Tests for ContextValidationResult model"""

    def test_validation_result_valid(self):
        """Test valid validation result"""
        result = ContextValidationResult(
            is_valid=True,
            context_id="test-context-1",
        )
        assert result.is_valid is True
        assert result.context_id == "test-context-1"
        assert len(result.errors) == 0

    def test_validation_result_with_errors(self):
        """Test validation result with errors"""
        result = ContextValidationResult(
            is_valid=False,
            errors=["Invalid configuration", "Missing required field"],
            context_id="test-context-2",
        )
        assert result.is_valid is False
        assert len(result.errors) == 2

    def test_validation_result_with_warnings(self):
        """Test validation result with warnings"""
        result = ContextValidationResult(
            is_valid=True,
            warnings=["Configuration may need review"],
            context_id="test-context-3",
        )
        assert result.is_valid is True
        assert len(result.warnings) == 1


class TestContextControlExceptions:
    """Tests for context control exceptions"""

    def test_context_control_error(self):
        """Test ContextControlError"""
        error = ContextControlError("Test error", context_id="ctx-1")
        assert str(error) == "Test error"
        assert error.context_id == "ctx-1"

    def test_context_not_found_error(self):
        """Test ContextNotFoundError"""
        error = ContextNotFoundError("Context not found", context_id="ctx-missing")
        assert "Context not found" in str(error)
        assert error.context_id == "ctx-missing"

    def test_context_validation_error(self):
        """Test ContextValidationError"""
        error = ContextValidationError("Validation failed")
        assert "Validation failed" in str(error)

    def test_context_isolation_error(self):
        """Test ContextIsolationError"""
        error = ContextIsolationError("Isolation breach detected")
        assert "Isolation breach detected" in str(error)

    def test_configuration_error(self):
        """Test ConfigurationError"""
        error = ConfigurationError("Invalid config")
        assert "Invalid config" in str(error)

    def test_environment_detection_error(self):
        """Test EnvironmentDetectionError"""
        error = EnvironmentDetectionError("Cannot detect environment")
        assert "Cannot detect environment" in str(error)

    def test_storage_error(self):
        """Test StorageError"""
        error = StorageError("Storage operation failed")
        assert "Storage operation failed" in str(error)

    def test_exception_inheritance(self):
        """Test exception inheritance hierarchy"""
        error = ContextControlError("base error")
        assert isinstance(error, Exception)

        not_found = ContextNotFoundError("not found")
        assert isinstance(not_found, ContextControlError)

        validation = ContextValidationError("invalid")
        assert isinstance(validation, ContextControlError)

        isolation = ContextIsolationError("isolated")
        assert isinstance(isolation, ContextControlError)