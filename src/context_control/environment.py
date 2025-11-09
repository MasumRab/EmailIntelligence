"""Environment detection functionality for Agent Context Control."""

from pathlib import Path
from typing import Optional
import git

from .exceptions import EnvironmentDetectionError
from .logging import get_context_logger


logger = get_context_logger()


def detect_branch(repo_path: Optional[Path] = None) -> str:
    """Detect the current Git branch or commit reference.

    Args:
        repo_path: Path to the Git repository. Defaults to current directory.

    Returns:
        Branch name or commit reference (e.g., 'main', 'feature/xyz', 'abc123...')

    Raises:
        EnvironmentDetectionError: If branch detection fails
    """
    try:
        repo_path = repo_path or Path(".")
        repo = git.Repo(repo_path, search_parent_directories=True)

        # Check if HEAD is detached
        if repo.head.is_detached:
            # Return abbreviated commit hash
            commit_hash = repo.head.commit.hexsha[:8]
            logger.warning(f"HEAD is detached, using commit hash: {commit_hash}")
            return f"detached-{commit_hash}"

        # Get current branch name
        branch_name = repo.active_branch.name
        logger.debug(f"Detected branch: {branch_name}")
        return branch_name

    except git.InvalidGitRepositoryError:
        raise EnvironmentDetectionError(
            "Not a valid Git repository",
            context_id=None
        )
    except git.GitCommandError as e:
        raise EnvironmentDetectionError(
            f"Git command failed: {e}",
            context_id=None
        )
    except Exception as e:
        raise EnvironmentDetectionError(
            f"Unexpected error during branch detection: {e}",
            context_id=None
        )


def get_current_branch(repo_path: Optional[Path] = None) -> Optional[str]:
    """Get the current branch name, or None if not on a branch.

    Args:
        repo_path: Path to the Git repository. Defaults to current directory.

    Returns:
        Branch name if on a branch, None if detached HEAD or error
    """
    try:
        repo_path = repo_path or Path(".")
        repo = git.Repo(repo_path, search_parent_directories=True)

        if repo.head.is_detached:
            return None

        return repo.active_branch.name

    except Exception:
        # Return None on any error to avoid breaking functionality
        return None


def is_detached_head(repo_path: Optional[Path] = None) -> bool:
    """Check if HEAD is in detached state.

    Args:
        repo_path: Path to the Git repository. Defaults to current directory.

    Returns:
        True if HEAD is detached, False otherwise
    """
    try:
        repo_path = repo_path or Path(".")
        repo = git.Repo(repo_path, search_parent_directories=True)
        return repo.head.is_detached
    except Exception:
        return False


def get_repository_root(repo_path: Optional[Path] = None) -> Optional[Path]:
    """Get the root path of the Git repository.

    Args:
        repo_path: Path to check for Git repository. Defaults to current directory.

    Returns:
        Path to repository root, or None if not a Git repository
    """
    try:
        repo_path = repo_path or Path(".")
        repo = git.Repo(repo_path, search_parent_directories=True)
        return Path(repo.working_dir)
    except git.InvalidGitRepositoryError:
        return None


def is_git_repository(repo_path: Optional[Path] = None) -> bool:
    """Check if the given path is within a Git repository.

    Args:
        repo_path: Path to check. Defaults to current directory.

    Returns:
        True if path is in a Git repository, False otherwise
    """
    try:
        repo_path = repo_path or Path(".")
        git.Repo(repo_path, search_parent_directories=True)
        return True
    except git.InvalidGitRepositoryError:
        return False