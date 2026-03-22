"""
Tests for AnalyzeCommand
"""

import pytest
from argparse import Namespace
from pathlib import Path
from unittest.mock import Mock, AsyncMock

from src.cli.commands.analyze_command import AnalyzeCommand


class TestAnalyzeCommand:
    """Test suite for AnalyzeCommand."""

    def test_name_property(self):
        """Test command name is 'analyze'."""
        cmd = AnalyzeCommand()
        assert cmd.name == "analyze"

    def test_description_property(self):
        """Test description contains conflicts."""
        cmd = AnalyzeCommand()
        assert "conflicts" in cmd.description.lower()

    def test_add_arguments_with_repo_path(self):
        """Test argument parsing with repo_path."""
        cmd = AnalyzeCommand()
        parser = self._create_parser()
        cmd.add_arguments(parser)

        args = parser.parse_args(["/tmp/repo"])
        assert args.repo_path == "/tmp/repo"

    def test_add_arguments_with_all_options(self):
        """Test argument parsing with all options."""
        cmd = AnalyzeCommand()
        parser = self._create_parser()
        cmd.add_arguments(parser)

        args = parser.parse_args(
            [
                "/tmp/repo",
                "--pr",
                "123",
                "--base-branch",
                "develop",
                "--head-branch",
                "feature/test",
            ]
        )
        assert args.repo_path == "/tmp/repo"
        assert args.pr_id == "123"
        assert args.base_branch == "develop"
        assert args.head_branch == "feature/test"

    def test_add_arguments_defaults(self):
        """Test default values for optional arguments."""
        cmd = AnalyzeCommand()
        parser = self._create_parser()
        cmd.add_arguments(parser)

        args = parser.parse_args(["/tmp/repo"])
        assert args.base_branch == "main"  # Default
        assert args.pr_id is None
        assert args.head_branch is None

    def test_get_dependencies_returns_dict(self):
        """Test dependencies are returned as dict."""
        cmd = AnalyzeCommand()
        deps = cmd.get_dependencies()
        assert isinstance(deps, dict)
        assert "conflict_detector" in deps
        assert "analyzer" in deps
        assert "strategy_generator" in deps
        assert "repository_ops" in deps

    def test_set_dependencies_stores_values(self):
        """Test dependencies are stored correctly."""
        cmd = AnalyzeCommand()
        mock_deps = {
            "conflict_detector": Mock(),
            "analyzer": Mock(),
            "strategy_generator": Mock(),
            "repository_ops": Mock(),
        }
        cmd.set_dependencies(mock_deps)

        assert cmd._detector == mock_deps["conflict_detector"]
        assert cmd._analyzer == mock_deps["analyzer"]
        assert cmd._strategy_gen == mock_deps["strategy_generator"]
        assert cmd._repo_ops == mock_deps["repository_ops"]

    @pytest.mark.asyncio
    async def test_execute_repo_not_exists(self):
        """Test error when repo path doesn't exist."""
        cmd = AnalyzeCommand()
        cmd.set_dependencies(
            {
                "conflict_detector": Mock(),
                "analyzer": Mock(),
                "strategy_generator": Mock(),
                "repository_ops": Mock(),
            }
        )

        args = Namespace(
            repo_path="/nonexistent/path",
            pr_id=None,
            base_branch="main",
            head_branch=None,
        )
        result = await cmd.execute(args)
        assert result == 1

    @pytest.mark.asyncio
    async def test_execute_no_conflicts(self):
        """Test when no conflicts are detected."""
        cmd = AnalyzeCommand()

        mock_detector = Mock()
        mock_detector.detect_conflicts_between_branches = AsyncMock(return_value=[])

        # Create a mock repository operations class
        mock_repo_class = Mock()
        mock_repo_instance = Mock()
        mock_repo_instance.run_command = AsyncMock(return_value=("main\n", "", 0))
        mock_repo_class.return_value = mock_repo_instance

        # Mock all dependencies
        cmd.set_dependencies(
            {
                "conflict_detector": mock_detector,
                "analyzer": Mock(),
                "strategy_generator": Mock(),
                "repository_ops": mock_repo_class,
            }
        )

        # Create a temporary directory for testing
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            args = Namespace(
                repo_path=temp_dir,
                pr_id=None,
                base_branch="main",
                head_branch="feature",
            )
            result = await cmd.execute(args)
            assert result == 0

            # Verify the method was called
            mock_detector.detect_conflicts_between_branches.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_with_conflicts(self):
        """Test when conflicts are detected and analyzed."""
        cmd = AnalyzeCommand()

        # Create mock conflict
        mock_conflict = Mock()
        mock_conflict.id = "conflict-test-123"
        mock_conflict.file_path = "test.py"
        mock_conflict.severity = Mock(value="HIGH")

        mock_detector = Mock()
        mock_detector.detect_conflicts_between_branches = AsyncMock(
            return_value=[mock_conflict]
        )

        # Create mock analyzer result
        mock_analysis = Mock()
        mock_analysis.compliance_score = 0.85

        mock_analyzer = Mock()
        mock_analyzer.analyze_constitutional_compliance = AsyncMock(
            return_value=mock_analysis
        )

        # Create mock strategy
        mock_strategy = Mock()
        mock_strategy.strategy_type = "standard_resolution"
        mock_strategy.steps = [{"description": "Step 1"}]

        mock_strategy_gen = Mock()
        mock_strategy_gen.generate_resolution_strategy = AsyncMock(
            return_value=mock_strategy
        )

        # Create mock repo ops
        mock_repo = Mock()
        mock_repo.run_command = AsyncMock(return_value=("feature\n", "", 0))

        # Create a mock repository operations class
        mock_repo_class = Mock()
        mock_repo_instance = Mock()
        mock_repo_instance.run_command = AsyncMock(return_value=("feature\n", "", 0))
        mock_repo_class.return_value = mock_repo_instance

        cmd.set_dependencies(
            {
                "conflict_detector": mock_detector,
                "analyzer": mock_analyzer,
                "strategy_generator": mock_strategy_gen,
                "repository_ops": mock_repo_class,
            }
        )

        # Create a temporary directory for testing
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            args = Namespace(
                repo_path=temp_dir,
                pr_id=None,
                base_branch="main",
                head_branch="feature",
            )
            result = await cmd.execute(args)
            assert result == 0

        # Verify interactions
        mock_detector.detect_conflicts_between_branches.assert_called_once()
        mock_analyzer.analyze_constitutional_compliance.assert_called()
        mock_strategy_gen.generate_resolution_strategy.assert_called()

    @pytest.mark.asyncio
    async def test_execute_exception_handling(self):
        """Test exception handling during execution."""
        cmd = AnalyzeCommand()
        cmd.set_dependencies(
            {
                "conflict_detector": Mock(),
                "analyzer": Mock(),
                "strategy_generator": Mock(),
                "repository_ops": Mock(),
            }
        )

        # Make repo_ops raise an exception
        cmd._repo_ops = Mock()
        cmd._repo_ops.run_command = AsyncMock(side_effect=Exception("Git error"))

        args = Namespace(
            repo_path="/tmp/repo", pr_id=None, base_branch="main", head_branch="feature"
        )
        result = await cmd.execute(args)
        assert result == 1

    def _create_parser(self):
        """Helper to create a parser for testing."""
        import argparse

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(required=True)
        cmd_parser = subparsers.add_parser("analyze")
        return cmd_parser
