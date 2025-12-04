"""
Git merge operations for EmailIntelligence CLI

This module handles merge execution, including fast-forward, squash,
and standard merges, with safety checks and error handling.
"""

from typing import Optional
from pathlib import Path

from ..core.exceptions import GitOperationError
from ..utils.logger import get_logger
from .repository import RepositoryOperations

logger = get_logger(__name__)


class GitMerger:
    """
    Handles git merge operations.
    """

    def __init__(self, repo_path: Path = None):
        self.repo = RepositoryOperations(repo_path)

    async def merge(
        self,
        source_branch: str,
        target_branch: str,
        strategy: str = "ort",
        squash: bool = False,
        message: Optional[str] = None,
    ) -> bool:
        """
        Merge source_branch into target_branch.

        Args:
            source_branch: Branch to merge from
            target_branch: Branch to merge into (must be checked out)
            strategy: Merge strategy (ort, recursive, etc.)
            squash: Whether to squash commits
            message: Optional commit message

        Returns:
            True if merge successful, False otherwise
        """
        # Verify we are on target branch
        current = await self.repo.get_current_branch()
        if current != target_branch:
            raise GitOperationError(f"Must be on {target_branch} to merge, currently on {current}")

        logger.info("Starting merge", source=source_branch, target=target_branch, squash=squash)

        cmd = ["merge", "--no-ff"]

        if squash:
            cmd.append("--squash")

        if strategy:
            cmd.extend(["-s", strategy])

        if message:
            cmd.extend(["-m", message])

        cmd.append(source_branch)

        try:
            await self.repo.run_git(cmd)
            logger.info("Merge successful")
            return True
        except GitOperationError as e:
            logger.warning("Merge failed", error=str(e))
            # Check if it's a conflict
            status = await self.repo.run_git(["status", "--porcelain"])
            if "UU" in status:  # Unmerged paths
                logger.info("Merge resulted in conflicts")
                return False
            raise

    async def abort_merge(self) -> None:
        """Abort the current merge."""
        try:
            await self.repo.run_git(["merge", "--abort"])
            logger.info("Merge aborted")
        except GitOperationError as e:
            logger.error("Failed to abort merge", error=str(e))
            raise

    async def continue_merge(self) -> None:
        """Continue merge after resolving conflicts."""
        try:
            # Check if all conflicts resolved
            status = await self.repo.run_git(["status", "--porcelain"])
            if "UU" in status:
                raise GitOperationError("Cannot continue merge: Unresolved conflicts remain")

            await self.repo.run_git(["merge", "--continue"])
            logger.info("Merge continued")
        except GitOperationError as e:
            logger.error("Failed to continue merge", error=str(e))
            raise
