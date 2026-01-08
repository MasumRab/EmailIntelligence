"""
Tests for ValidateCommand
"""

import pytest
from argparse import Namespace
from unittest.mock import Mock, AsyncMock

from src.cli.commands.validate_command import ValidateCommand


class TestValidateCommand:
    """Test suite for ValidateCommand."""

    def test_name_property(self):
        """Test command name is 'validate'."""
        cmd = ValidateCommand()
        assert cmd.name == "validate"

    def test_description_property(self):
        """Test description contains validation."""
        cmd = ValidateCommand()
        assert "validation" in cmd.description.lower()

    def test_add_arguments_no_args(self):
        """Test that validate command doesn't add arguments."""
        cmd = ValidateCommand()
        parser = self._create_parser()

        # Count arguments before
        before_count = len(parser._actions)

        cmd.add_arguments(parser)

        # Count arguments after
        after_count = len(parser._actions)

        # Should be the same (no arguments added)
        assert before_count == after_count

    def test_get_dependencies_returns_dict(self):
        """Test dependencies are returned as dict."""
        cmd = ValidateCommand()
        deps = cmd.get_dependencies()
        assert isinstance(deps, dict)
        assert "validator" in deps

    def test_set_dependencies_stores_values(self):
        """Test dependencies are stored correctly."""
        cmd = ValidateCommand()
        mock_validator = Mock()
        cmd.set_dependencies({"validator": mock_validator})
        assert cmd._validator == mock_validator

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Test successful validation execution."""
        cmd = ValidateCommand()

        mock_validator = Mock()
        mock_result = Mock()
        mock_result.is_valid = True
        mock_result.details = {"test": "passed"}
        mock_validator.validate = AsyncMock(return_value=mock_result)

        cmd.set_dependencies({"validator": mock_validator})

        args = Namespace()
        result = await cmd.execute(args)

        assert result == 0
        mock_validator.validate.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_failure(self):
        """Test failed validation execution."""
        cmd = ValidateCommand()

        mock_validator = Mock()
        mock_result = Mock()
        mock_result.is_valid = False
        mock_validator.validate = AsyncMock(return_value=mock_result)

        cmd.set_dependencies({"validator": mock_validator})

        args = Namespace()
        result = await cmd.execute(args)

        assert result == 1

    @pytest.mark.asyncio
    async def test_execute_exception_handling(self):
        """Test exception handling during execution."""
        cmd = ValidateCommand()
        cmd.set_dependencies({"validator": Mock()})

        # Make validator raise an exception
        cmd._validator = Mock()
        cmd._validator.validate = AsyncMock(side_effect=Exception("Validation error"))

        args = Namespace()
        result = await cmd.execute(args)
        assert result == 1

    def _create_parser(self):
        """Helper to create a parser for testing."""
        import argparse

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(required=True)
        cmd_parser = subparsers.add_parser("validate")
        return cmd_parser
