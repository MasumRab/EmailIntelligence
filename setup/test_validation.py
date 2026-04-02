#!/usr/bin/env python3
"""
Unit tests for the validation module.

These tests cover the validation functions in setup/validation.py:
- check_python_version
- check_for_merge_conflicts
- check_required_components
- validate_environment
- validate_port
- validate_host
"""

import logging
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from setup import validation


class TestValidatePort:
    """Tests for validate_port function."""

    def test_validate_port_valid(self):
        """Test valid port numbers are accepted."""
        assert validation.validate_port(80) == 80
        assert validation.validate_port(443) == 443
        assert validation.validate_port(8080) == 8080
        assert validation.validate_port(65535) == 65535
        assert validation.validate_port(1) == 1

    def test_validate_port_invalid_low(self):
        """Test port numbers below 1 are rejected."""
        with pytest.raises(ValueError, match="Invalid port number: 0"):
            validation.validate_port(0)

        with pytest.raises(ValueError, match="Invalid port number: -1"):
            validation.validate_port(-1)

    def test_validate_port_invalid_high(self):
        """Test port numbers above 65535 are rejected."""
        with pytest.raises(ValueError, match="Invalid port number: 65536"):
            validation.validate_port(65536)

    def test_validate_port_invalid_type_string(self):
        """Test string port values are rejected."""
        with pytest.raises(ValueError, match="Invalid port number"):
            validation.validate_port("8080")

    def test_validate_port_invalid_type_none(self):
        """Test None port values are rejected."""
        with pytest.raises(ValueError, match="Invalid port number"):
            validation.validate_port(None)


class TestValidateHost:
    """Tests for validate_host function."""

    def test_validate_host_valid(self):
        """Test valid host addresses are accepted."""
        assert validation.validate_host("localhost") == "localhost"
        assert validation.validate_host("127.0.0.1") == "127.0.0.1"
        assert validation.validate_host("example.com") == "example.com"
        assert validation.validate_host("api.example.com") == "api.example.com"
        assert validation.validate_host("my-server.local") == "my-server.local"

    def test_validate_host_empty(self):
        """Test empty host strings are rejected."""
        with pytest.raises(ValueError, match="Invalid host"):
            validation.validate_host("")

    def test_validate_host_none(self):
        """Test None host values are rejected."""
        with pytest.raises(ValueError, match="Invalid host"):
            validation.validate_host(None)


class TestCheckPythonVersion:
    """Tests for check_python_version function."""

    @patch.object(validation, 'PYTHON_MIN_VERSION', (3, 11))
    @patch.object(validation, 'PYTHON_MAX_VERSION', (3, 12))
    @patch.object(validation.logger, 'info')
    def test_check_python_version_compatible(self, mock_info):
        """Test compatible Python versions pass."""
        # Mock sys.version_info to return a compatible version
        with patch.object(sys, 'version_info', (3, 11)):
            validation.check_python_version()
            mock_info.assert_called_once()

    @patch.object(validation, 'PYTHON_MIN_VERSION', (3, 11))
    @patch.object(validation, 'PYTHON_MAX_VERSION', (3, 12))
    @patch.object(validation.logger, 'error')
    def test_check_python_version_incompatible_low(self, mock_error):
        """Test Python versions below minimum are rejected."""
        with patch.object(sys, 'version_info', (3, 10)):
            with pytest.raises(SystemExit):
                validation.check_python_version()
            mock_error.assert_called_once()

    @patch.object(validation, 'PYTHON_MIN_VERSION', (3, 11))
    @patch.object(validation, 'PYTHON_MAX_VERSION', (3, 12))
    @patch.object(validation.logger, 'error')
    def test_check_python_version_incompatible_high(self, mock_error):
        """Test Python versions above maximum are rejected."""
        with patch.object(sys, 'version_info', (3, 13)):
            with pytest.raises(SystemExit):
                validation.check_python_version()
            mock_error.assert_called_once()


class TestCheckForMergeConflicts:
    """Tests for check_for_merge_conflicts function."""

    @patch('setup.validation.get_project_config')
    @patch('setup.validation.ROOT_DIR', Path('/workspace/project/EmailIntelligence'))
    def test_check_for_merge_conflicts_none_found(self, mock_config):
        """Test when no merge conflicts are found."""
        # Mock config that returns empty list of critical files
        mock_config_obj = MagicMock()
        mock_config_obj.get_critical_files.return_value = []
        mock_config.return_value = mock_config_obj

        result = validation.check_for_merge_conflicts()
        assert result is True

    @patch('setup.validation.get_project_config')
    @patch('setup.validation.ROOT_DIR', Path('/workspace/project/EmailIntelligence'))
    def test_check_for_merge_conflicts_found(self, mock_config):
        """Test when merge conflicts are detected."""
        # Create a temp file with conflict markers
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("<<<<<<< HEAD\nsome content\n=======\nother content\n>>>>>>> abc123\n")
            temp_path = f.name
        
        try:
            # Mock config to return our temp file as critical
            mock_config_obj = MagicMock()
            mock_config_obj.get_critical_files.return_value = [temp_path]
            mock_config.return_value = mock_config_obj

            result = validation.check_for_merge_conflicts()
            assert result is False
        finally:
            Path(temp_path).unlink()


class TestValidateEnvironment:
    """Tests for validate_environment function."""

    @patch.object(validation, 'check_python_version')
    @patch.object(validation, 'check_for_merge_conflicts')
    @patch.object(validation, 'check_required_components')
    def test_validate_environment_all_pass(self, mock_components, mock_conflicts, mock_python):
        """Test when all validations pass."""
        mock_python.return_value = True
        mock_conflicts.return_value = True
        mock_components.return_value = True

        result = validation.validate_environment()
        assert result is True

    @patch.object(validation, 'check_python_version')
    @patch.object(validation, 'check_for_merge_conflicts')
    @patch.object(validation, 'check_required_components')
    def test_validate_environment_fails_python(self, mock_components, mock_conflicts, mock_python):
        """Test when Python version check fails."""
        mock_python.return_value = False
        mock_conflicts.return_value = True
        mock_components.return_value = True

        result = validation.validate_environment()
        assert result is False

    @patch.object(validation, 'check_python_version')
    @patch.object(validation, 'check_for_merge_conflicts')
    @patch.object(validation, 'check_required_components')
    def test_validate_environment_fails_conflicts(self, mock_components, mock_conflicts, mock_python):
        """Test when merge conflict check fails."""
        mock_python.return_value = True
        mock_conflicts.return_value = False
        mock_components.return_value = True

        result = validation.validate_environment()
        assert result is False


# Run tests if executed directly
if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v"])