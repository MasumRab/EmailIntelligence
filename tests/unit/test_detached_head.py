"""Unit tests for detached HEAD edge cases."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.context_control.environment import detect_branch, is_detached_head
from src.context_control.exceptions import EnvironmentDetectionError


class TestDetachedHead:
    """Test cases for detached HEAD scenarios."""

    @patch('git.Repo')
    def test_detect_detached_head_commit_hash(self, mock_repo_class):
        """Test detection when HEAD points to a commit hash."""
        mock_repo = MagicMock()
        mock_repo.head.is_detached = True
        mock_repo.head.commit.hexsha = "abcdef1234567890"
        mock_repo_class.return_value = mock_repo

        with patch('src.context_control.environment.git.Repo', mock_repo_class):
            branch = detect_branch()
            assert branch == "detached-abcdef12"

    @patch('git.Repo')
    def test_detect_detached_head_tag(self, mock_repo_class):
        """Test detection when HEAD points to a tag."""
        # Note: GitPython doesn't distinguish between commit and tag for detached HEAD
        # The implementation treats all detached HEAD as commit hashes
        mock_repo = MagicMock()
        mock_repo.head.is_detached = True
        mock_repo.head.commit.hexsha = "v1.0.0"
        mock_repo_class.return_value = mock_repo

        with patch('src.context_control.environment.git.Repo', mock_repo_class):
            branch = detect_branch()
            assert branch == "detached-v1.0.0"

    @patch('git.Repo')
    def test_context_fallback_for_detached_head(self, mock_repo_class):
        """Test that detached HEAD returns a valid branch identifier."""
        mock_repo = MagicMock()
        mock_repo.head.is_detached = True
        mock_repo.head.commit.hexsha = "commit123"
        mock_repo_class.return_value = mock_repo

        with patch('src.context_control.environment.git.Repo', mock_repo_class):
            branch = detect_branch()
            assert branch.startswith("detached-")
            assert len(branch) > 9  # "detached-" + at least 1 char

    @patch('git.Repo')
    def test_is_detached_head_detection(self, mock_repo_class):
        """Test that detached HEAD is properly detected."""
        mock_repo = MagicMock()
        mock_repo.head.is_detached = True
        mock_repo_class.return_value = mock_repo

        with patch('src.context_control.environment.git.Repo', mock_repo_class):
            assert is_detached_head() is True