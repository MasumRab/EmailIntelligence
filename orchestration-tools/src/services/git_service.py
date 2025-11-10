"""Git service for repository operations."""

from typing import List, Optional, Dict, Any
from pathlib import Path
import subprocess

from src.logging import get_logger


logger = get_logger(__name__)


class GitService:
    """Service for Git operations."""

    def __init__(self, repo_path: str = "."):
        """Initialize Git service with repository path."""
        self.repo_path = Path(repo_path)
        self.logger = logger

    def get_current_branch(self) -> str:
        """Get the current branch name."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get current branch: {e}")
            raise

    def get_branches(self, remote: bool = False) -> List[str]:
        """Get list of branches."""
        try:
            cmd = ["git", "branch"]
            if remote:
                cmd.append("-r")
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            branches = [b.strip().replace("* ", "") for b in result.stdout.split("\n") if b.strip()]
            return branches
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get branches: {e}")
            raise

    def get_status(self) -> Dict[str, Any]:
        """Get repository status."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return {
                "clean": result.stdout == "",
                "changes": result.stdout.strip().split("\n") if result.stdout.strip() else [],
            }
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get repository status: {e}")
            raise

    def get_commit_hash(self, ref: str = "HEAD") -> str:
        """Get commit hash for a reference."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", ref],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get commit hash: {e}")
            raise

    def get_changed_files(self, from_ref: str = "origin/main", to_ref: str = "HEAD") -> List[str]:
        """Get list of changed files between two references."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{from_ref}...{to_ref}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            return [f for f in result.stdout.strip().split("\n") if f]
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get changed files: {e}")
            raise

    def get_commit_log(self, ref: str = "HEAD", max_count: int = 10) -> List[Dict[str, str]]:
        """Get commit log."""
        try:
            result = subprocess.run(
                [
                    "git",
                    "log",
                    f"--max-count={max_count}",
                    "--format=%H|%an|%ae|%ai|%s",
                    ref,
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            commits = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    parts = line.split("|")
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4],
                    })
            return commits
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get commit log: {e}")
            raise
