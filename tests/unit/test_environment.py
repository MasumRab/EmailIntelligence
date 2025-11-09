"""Unit tests for environment detection functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import git

from src.context_control.environment import (
    detect_branch,
    get_current_branch,
    is_detached_head,
    get_repository_root,
    is_git_repository
)
from src.context_control.exceptions import EnvironmentDetectionError


class TestBranchDetection:
    """Test cases for Git branch detection."""

    def test_detect_branch_main_branch(self):
        """Test detection of main branch."""
        # Test with the actual repository
        branch = detect_branch()
        assert isinstance(branch, str)
        assert len(branch) > 0

    def test_detect_branch_no_git_repo(self):
        """Test behavior when not in a Git repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with pytest.raises(EnvironmentDetectionError, match="Not a valid Git repository"):
                detect_branch(temp_path)

    @patch('git.Repo')
    def test_detect_branch_detached_head(self, mock_repo_class):
        """Test detection of detached HEAD state."""
        # Mock detached HEAD scenario
        mock_repo = MagicMock()
        mock_repo.head.is_detached = True
        mock_repo.head.commit.hexsha = "abc123456789"
        mock_repo_class.return_value = mock_repo

        with patch('src.context_control.environment.git.Repo', mock_repo_class):
            branch = detect_branch()
            assert branch == "detached-abc12345"

    @patch('git.Repo')
    def test_get_current_branch_with_mock(self, mock_repo_class):
        """Test current branch retrieval with mocked Git repo."""
        # Mock normal branch scenario
        mock_repo = MagicMock()
        mock_repo.head.is_detached = False
        mock_repo.active_branch.name = "feature/test-branch"
        mock_repo_class.return_value = mock_repo

        with patch('src.context_control.environment.git.Repo', mock_repo_class):
            branch = get_current_branch()
            assert branch == "feature/test-branch"

    @patch('git.Repo')
    def test_get_current_branch_detached_head(self, mock_repo_class):
        """Test current branch returns None for detached HEAD."""
        mock_repo = MagicMock()
        mock_repo.head.is_detached = True
        mock_repo_class.return_value = mock_repo

        with patch('src.context_control.environment.git.Repo', mock_repo_class):
            branch = get_current_branch()
            assert branch is None

    @patch('git.Repo')
    def test_is_detached_head_true(self, mock_repo_class):
        """Test detached HEAD detection."""
        mock_repo = MagicMock()
        mock_repo.head.is_detached = True
        mock_repo_class.return_value = mock_repo

        with patch('src.context_control.environment.git.Repo', mock_repo_class):
            assert is_detached_head() is True

    @patch('git.Repo')
    def test_is_detached_head_false(self, mock_repo_class):
        """Test normal branch detection."""
        mock_repo = MagicMock()
        mock_repo.head.is_detached = False
        mock_repo_class.return_value = mock_repo

        with patch('src.context_control.environment.git.Repo', mock_repo_class):
            assert is_detached_head() is False

    def test_is_git_repository_true(self):
        """Test Git repository detection in current directory."""
        assert is_git_repository() is True

    def test_is_git_repository_false(self):
        """Test non-Git directory detection."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            assert is_git_repository(temp_path) is False

    def test_get_repository_root(self):
        """Test repository root detection."""
        root = get_repository_root()
        assert root is not None
        assert root.is_dir()
        assert (root / '.git').exists()