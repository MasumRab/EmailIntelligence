"""
Git repository operations for EmailIntelligence CLI

This module provides a wrapper around common git operations,
handling command execution, error checking, and output parsing.
"""

import asyncio
from pathlib import Path
from typing import List, Tuple

from ..core.config import settings
from ..core.exceptions import GitOperationError
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RepositoryOperations:
    """
    Wrapper for git repository operations.
    """

    def __init__(self, repo_path: Path = None):
        self.repo_path = repo_path or Path.cwd()

    async def run_git(self, args: List[str], cwd: Path = None, check: bool = True) -> str:
        """
        Run a git command asynchronously.

        Args:
            args: List of command arguments
            cwd: Working directory (defaults to repo_path)
            check: Whether to raise exception on non-zero return code

        Returns:
            Command stdout output

        Raises:
            GitOperationError: If command fails and check is True
        """
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

            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=settings.git_timeout_seconds
            )

            output = stdout.decode().strip()
            error_msg = stderr.decode().strip()

            if check and process.returncode != 0:
                logger.error("Git command failed", command=cmd_str, error=error_msg)
                raise GitOperationError(f"Git command failed: {error_msg}")

            return output

        except asyncio.TimeoutError:
            logger.error(
                "Git command timed out",
                command=cmd_str,
                timeout=settings.git_timeout_seconds,
            )
            try:
                process.terminate()
                await asyncio.wait_for(process.wait(), timeout=1.0)
            except Exception:
                try:
                    process.kill()
                except Exception:
                    pass
            raise GitOperationError(f"Git command timed out: {cmd_str}")
        except Exception as e:
            if isinstance(e, GitOperationError):
                raise
            logger.error("Git execution error", command=cmd_str, error=str(e))
            raise GitOperationError(f"Git execution error: {str(e)}") from e

    async def get_current_branch(self) -> str:
        """Get the name of the current branch."""
        return await self.run_git(["rev-parse", "--abbrev-ref", "HEAD"])

    async def get_commit_sha(self, ref: str = "HEAD") -> str:
        """Get the full SHA for a reference."""
        return await self.run_git(["rev-parse", ref])

    async def fetch_all(self) -> None:
        """Fetch all remotes."""
        await self.run_git(["fetch", "--all"])

    async def checkout(self, branch: str) -> None:
        """Checkout a branch."""
        await self.run_git(["checkout", branch])

    async def get_merge_base(self, branch1: str, branch2: str) -> str:
        """Find the common ancestor of two branches."""
        return await self.run_git(["merge-base", branch1, branch2])

    async def get_changed_files(self, base: str, head: str) -> List[str]:
        """Get list of changed files between two references."""
        output = await self.run_git(["diff", "--name-only", base, head])
        return [f for f in output.splitlines() if f]

    async def get_file_content(self, path: str, ref: str = "HEAD") -> str:
        """Get content of a file at a specific reference."""
        return await self.run_git(["show", f"{ref}:{path}"])

    async def get_git_version(self) -> Tuple[int, int, int]:
        """Get git version as a tuple."""
        import re

        output = await self.run_git(["version"])
        # Format: "git version 2.39.1.windows.1" or "git version 2.39.1-rc1"

        # Extract all numeric groups
        numbers = re.findall(r"\d+", output)

        if not numbers:
            raise ValueError(f"Could not parse git version from output: {output}")

        # Take first 3 numbers, pad with 0 if needed
        parts = [int(n) for n in numbers[:3]]
        while len(parts) < 3:
            parts.append(0)

        return tuple(parts)
