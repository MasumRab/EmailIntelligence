"""
Git worktree management for EmailIntelligence CLI

This module handles the creation, management, and cleanup of git worktrees
to allow isolated analysis of Pull Requests without affecting the main working directory.
"""

import asyncio
import shutil
from pathlib import Path
from typing import List, Dict
from contextlib import asynccontextmanager

from ..core.config import settings
from ..core.exceptions import GitOperationError
from ..utils.logger import get_logger

logger = get_logger(__name__)


class WorktreeManager:
    """
    Manages git worktrees for isolated PR analysis.
    """

    def __init__(self, repo_path: Path = None):
        self.repo_path = repo_path or Path.cwd()
        self.worktree_base = Path(settings.git_worktree_base)

    async def _run_git(self, args: List[str], cwd: Path = None) -> str:
        """Run a git command asynchronously."""
        cwd = cwd or self.repo_path
        cmd_str = f"git {' '.join(args)}"

        try:
            process = await asyncio.create_subprocess_exec(
                "git",
                *args,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=settings.git_timeout_seconds
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                logger.error(
                    "Git command timed out",
                    command=cmd_str,
                    timeout=settings.git_timeout_seconds,
                )
                raise GitOperationError(f"Git command timed out: {cmd_str}")

            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                logger.error("Git command failed", command=cmd_str, error=error_msg)
                raise GitOperationError(f"Git command failed: {error_msg}")

            return stdout.decode().strip()
        except Exception as e:
            if isinstance(e, GitOperationError):
                raise
            logger.error("Git execution error", command=cmd_str, error=str(e))
            raise GitOperationError(f"Git execution error: {str(e)}") from e

    async def ensure_worktree_base(self) -> None:
        """Ensure the worktree base directory exists."""
        if not self.worktree_base.exists():
            self.worktree_base.mkdir(parents=True, exist_ok=True)
            # Add to .gitignore if not present
            gitignore = self.repo_path / ".gitignore"
            if gitignore.exists():
                content = gitignore.read_text(encoding="utf-8")
                worktree_entry = f"{settings.git_worktree_base}/"
                if not any(line.strip() == worktree_entry for line in content.splitlines()):
                    with gitignore.open("a", encoding="utf-8") as f:
                        f.write(f"\n{worktree_entry}\n")

    async def create_worktree(self, branch: str, pr_id: str) -> Path:
        """
        Create a worktree for a specific branch/PR.

        Args:
            branch: The branch to checkout
            pr_id: The PR ID (used for directory naming)

        Returns:
            Path to the created worktree
        """
        await self.ensure_worktree_base()

        worktree_path = settings.get_worktree_path(pr_id)

        # Check if worktree already exists
        if worktree_path.exists():
            logger.info("Worktree already exists, cleaning up", path=str(worktree_path))
            await self.remove_worktree(pr_id)

        logger.info("Creating worktree", branch=branch, path=str(worktree_path))

        try:
            # Create worktree
            await self._run_git(
                [
                    "worktree",
                    "add",
                    "-f",  # Force if branch is already checked out elsewhere
                    str(worktree_path),
                    branch,
                ]
            )
            return worktree_path
        except Exception as e:
            logger.error("Failed to create worktree", branch=branch, error=str(e))
            # Cleanup if partial creation happened
            if worktree_path.exists():
                await self.remove_worktree(pr_id)
            raise GitOperationError(f"Failed to create worktree for {branch}: {str(e)}") from e

    async def remove_worktree(self, pr_id: str) -> None:
        """
        Remove a worktree.

        Args:
            pr_id: The PR ID associated with the worktree
        """
        worktree_path = settings.get_worktree_path(pr_id)

        if not worktree_path.exists():
            return

        logger.info("Removing worktree", path=str(worktree_path))

        try:
            if worktree_path.exists():
                shutil.rmtree(worktree_path)
            # Prune worktrees to clean up git metadata
            await self._run_git(["worktree", "prune"])
        except Exception as cleanup_error:
            logger.error(
                "Failed to cleanup worktree directory",
                path=str(worktree_path),
                error=str(cleanup_error),
            )
            raise GitOperationError(
                f"Failed to remove worktree: {str(cleanup_error)}"
            ) from cleanup_error

    async def list_worktrees(self) -> List[Dict[str, str]]:
        """List all active worktrees."""
        output = await self._run_git(["worktree", "list", "--porcelain"])
        worktrees = []
        current_worktree = {}

        for line in output.splitlines():
            if not line:
                if current_worktree:
                    worktrees.append(current_worktree)
                    current_worktree = {}
                continue

            key, _, value = line.partition(" ")
            current_worktree[key] = value

        if current_worktree:
            worktrees.append(current_worktree)

        return worktrees

    @asynccontextmanager
    async def worktree_context(self, branch: str, pr_id: str):
        """
        Async context manager for temporary worktree usage.
        Automatically cleans up the worktree after use.
        """
        path = await self.create_worktree(branch, pr_id)
        try:
            yield path
        finally:
            await self.remove_worktree(pr_id)
