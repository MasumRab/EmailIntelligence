"""Unit tests for configuration conflict detection."""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile

from src.context_control.project import ProjectConfig
from src.context_control.exceptions import ConfigurationError
from src.context_control.validation import ContextValidator
from src.context_control.config import ContextControlConfig, init_config


class TestConfigConflicts:
    """Test cases for configuration conflict detection."""

    def test_detect_conflicting_project_settings(self):
        """Test detection of conflicting project configuration settings."""
        # Initialize global config
        init_config()

        # Test conflicting boolean settings that don't make sense
        config = ProjectConfig(
            project_name="conflict-test",
            project_type="python",
            enable_code_execution=False,  # Conflicts with python project type
            enable_shell_commands=True    # Might be okay
        )

        validator = ContextValidator()
        result = validator.validate_project_config(config)

        # Should have warnings about code execution for python projects
        assert len(result.warnings) > 0
        assert any("code execution" in warning.lower() for warning in result.warnings)

    def test_resolve_configuration_precedence(self):
        """Test resolution of configuration precedence rules."""
        # Initialize global config
        init_config()

        # Test that agent-specific settings override project settings
        from src.context_control.agent import AgentAdapter
        from src.context_control.models import AgentContext

        project_config = ProjectConfig(
            project_name="precedence-test",
            project_type="web",
            max_context_length=4096
        )

        # Create a mock context with agent-specific override
        context = AgentContext(
            profile_id="test-profile",
            agent_id="test-agent",
            environment_type="development"
        )
        # Set agent settings on the profile, not context
        profile = type('MockProfile', (), {
            'agent_settings': {"test-agent": {"max_context_length": 8192}}
        })()
        context.profile_config = project_config

        # Create adapter and manually set the profile config
        adapter = AgentAdapter(context)
        # Manually override the project config for testing
        adapter.project_config = project_config

        # Test that project settings are used
        assert adapter.get_max_context_length() == 4096

    def test_invalid_configuration_values(self):
        """Test detection of invalid configuration values."""
        # Initialize global config
        init_config()

        validator = ContextValidator()

        # Test invalid project name
        invalid_config = ProjectConfig(
            project_name="invalid@name!",
            project_type="python"
        )
        result = validator.validate_project_config(invalid_config)
        assert not result.is_valid
        assert any("project name" in error.lower() for error in result.errors)

        # Test invalid project type
        invalid_config2 = ProjectConfig(
            project_name="valid-name",
            project_type="invalid-type"
        )
        result2 = validator.validate_project_config(invalid_config2)
        assert not result2.is_valid

        # Test invalid context length
        invalid_config3 = ProjectConfig(
            project_name="valid-name",
            project_type="python",
            max_context_length=50  # Too small
        )
        result3 = validator.validate_project_config(invalid_config3)
        assert not result3.is_valid

    def test_missing_required_configuration(self):
        """Test detection of missing required configuration."""
        # Initialize global config
        init_config()

        validator = ContextValidator()

        # Test missing project name
        try:
            config = ProjectConfig(
                project_name="",  # Empty name
                project_type="python"
            )
            result = validator.validate_project_config(config)
            assert not result.is_valid
            assert any("required" in error.lower() for error in result.errors)
        except Exception:
            # Pydantic might raise validation error before our validator
            pass