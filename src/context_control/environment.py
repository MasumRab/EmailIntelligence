"""Environment detection functionality for Agent Context Control."""

from pathlib import Path
from typing import Optional

import git

from .exceptions import EnvironmentDetectionError
from .logging import get_context_logger

logger = get_context_logger()


class GitRepository:
    """Encapsulates Git repository operations for environment detection."""
    
    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize Git repository wrapper.
        
        Args:
            repo_path: Path to the Git repository. Defaults to current directory.
            
        Raises:
            EnvironmentDetectionError: If repository initialization fails
        """
        try:
            repo_path = repo_path or Path(".")
            self._repo = git.Repo(repo_path, search_parent_directories=True)
            self._path = Path(self._repo.working_dir)
            logger.debug(f"Initialized Git repository at {self._path}")
        except git.InvalidGitRepositoryError:
            raise EnvironmentDetectionError("Not a valid Git repository", context_id=None)
        except git.GitCommandError as e:
            raise EnvironmentDetectionError(f"Git command failed: {e}", context_id=None)
        except Exception as e:
            raise EnvironmentDetectionError(
                f"Unexpected error during repository initialization: {e}", context_id=None
            )
    
    @property
    def path(self) -> Path:
        """Get the repository root path."""
        return self._path
    
    @property
    def is_detached(self) -> bool:
        """Check if HEAD is in detached state."""
        return self._repo.head.is_detached
    
    @property
    def active_branch_name(self) -> Optional[str]:
        """Get the current branch name, or None if detached."""
        if self.is_detached:
            return None
        return self._repo.active_branch.name
    
    @property
    def commit_hash(self) -> str:
        """Get the current commit hash (abbreviated to 8 characters)."""
        return self._repo.head.commit.hexsha[:8]
    
    def get_branch_info(self) -> str:
        """Get branch information for environment detection.
        
        Returns:
            Branch name or commit reference (e.g., 'main', 'feature/xyz', 'abc123...')
        """
        if self.is_detached:
            commit_hash = self.commit_hash
            logger.warning(f"HEAD is detached, using commit hash: {commit_hash}")
            return f"detached-{commit_hash}"
        
        branch_name = self.active_branch_name
        logger.debug(f"Detected branch: {branch_name}")
        return branch_name


def _get_git_repository(repo_path: Optional[Path] = None) -> Optional[GitRepository]:
    """Get Git repository wrapper, or None if not in a Git repository.
    
    Args:
        repo_path: Path to the Git repository. Defaults to current directory.
        
    Returns:
        GitRepository instance or None if not in a Git repository
    """
    try:
        return GitRepository(repo_path)
    except EnvironmentDetectionError:
        return None


def detect_branch(repo_path: Optional[Path] = None) -> str:
    """Detect the current Git branch or commit reference.

    Args:
        repo_path: Path to the Git repository. Defaults to current directory.

    Returns:
        Branch name or commit reference (e.g., 'main', 'feature/xyz', 'abc123...')

    Raises:
        EnvironmentDetectionError: If branch detection fails
    """
    repo = _get_git_repository(repo_path)
    if repo is None:
        raise EnvironmentDetectionError("Not in a Git repository", context_id=None)
    
    return repo.get_branch_info()


def get_current_branch(repo_path: Optional[Path] = None) -> Optional[str]:
    """Get the current branch name, or None if not on a branch.

    Args:
        repo_path: Path to the Git repository. Defaults to current directory.

    Returns:
        Branch name if on a branch, None if detached HEAD or error
    """
    repo = _get_git_repository(repo_path)
    if repo is None:
        return None
    
    try:
        return repo.active_branch_name
    except Exception:
        return None


def is_detached_head(repo_path: Optional[Path] = None) -> bool:
    """Check if HEAD is in detached state.

    Args:
        repo_path: Path to the Git repository. Defaults to current directory.

    Returns:
        True if HEAD is detached, False otherwise
    """
    repo = _get_git_repository(repo_path)
    if repo is None:
        return False
    
    try:
        return repo.is_detached
    except Exception:
        return False


def get_repository_root(repo_path: Optional[Path] = None) -> Optional[Path]:
    """Get the root path of the Git repository.

    Args:
        repo_path: Path to check for Git repository. Defaults to current directory.

    Returns:
        Path to repository root, or None if not a Git repository
    """
    repo = _get_git_repository(repo_path)
    if repo is None:
        return None
    
    try:
        return repo.path
    except Exception:
        return None


def is_git_repository(repo_path: Optional[Path] = None) -> bool:
    """Check if the given path is within a Git repository.

    Args:
        repo_path: Path to check. Defaults to current directory.

    Returns:
        True if path is in a Git repository, False otherwise
    """
    return _get_git_repository(repo_path) is not None
