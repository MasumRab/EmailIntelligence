"""Unit tests for project configuration loading functionality."""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import tempfile
import json

from src.context_control.project import ProjectConfig, load_project_config, ProjectConfigLoader
from src.context_control.models import ContextProfile
from src.context_control.exceptions import ConfigurationError
from src.context_control.config import ContextControlConfig


class TestProjectConfig:
    """Test cases for project configuration loading."""

    def test_load_project_config_from_file(self):
        """Test loading project configuration from a JSON file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a project config file
            config_data = {
                "project_name": "test-project",
                "project_type": "python",
                "max_context_length": 8192,
                "enable_code_execution": True
            }

            config_file = temp_path / ".context-control" / "project.json"
            config_file.parent.mkdir(parents=True)
            with open(config_file, 'w') as f:
                json.dump(config_data, f)

            # Initialize config
            app_config = ContextControlConfig()
            loader = ProjectConfigLoader(app_config)
            config = loader.load_project_config(temp_path)

            assert config is not None
            assert config.project_name == "test-project"
            assert config.project_type == "python"
            assert config.max_context_length == 8192
            assert config.enable_code_execution is True

    def test_load_project_config_from_directory(self):
        """Test loading project configuration from a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create config in project root
            config_data = {
                "project_name": "root-project",
                "project_type": "web"
            }

            config_file = temp_path / "project.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f)

            # Initialize config
            app_config = ContextControlConfig()
            loader = ProjectConfigLoader(app_config)
            config = loader.load_project_config(temp_path)

            assert config is not None
            assert config.project_name == "root-project"
            assert config.project_type == "web"

    def test_project_config_validation(self):
        """Test validation of project configuration."""
        from src.context_control.validation import ContextValidator
        from src.context_control.config import init_config

        init_config()

        validator = ContextValidator()

        # Valid config
        valid_config = ProjectConfig(
            project_name="valid-project",
            project_type="python"
        )
        result = validator.validate_project_config(valid_config)
        assert result.is_valid

        # Invalid config - empty name
        invalid_config = ProjectConfig(
            project_name="",  # Invalid: empty name
            project_type="python"
        )
        result = validator.validate_project_config(invalid_config)
        assert not result.is_valid

    def test_project_config_defaults(self):
        """Test default values for project configuration."""
        config = ProjectConfig(project_name="test", project_type="python")

        assert config.max_context_length == 4096
        assert config.enable_code_execution is False
        assert config.enable_file_writing is False
        assert config.enable_shell_commands is False
        assert len(config.preferred_models) > 0

    def test_project_config_merge(self):
        """Test merging of multiple configuration sources."""
        # Create a config with some defaults
        config = ProjectConfig(project_name="test", project_type="python")

        # Simulate merging additional settings
        additional = {"max_context_length": 8192, "enable_code_execution": True}
        merged = config.dict()
        merged.update(additional)

        # Create new config from merged data
        merged_config = ProjectConfig(**merged)

        assert merged_config.max_context_length == 8192
        assert merged_config.enable_code_execution is True
        assert merged_config.project_name == "test"  # Original value preserved

