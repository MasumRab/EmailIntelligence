"""
Git Worktree Module

This module provides worktree management functionality using gtr (git worktree runner).
Reference: https://github.com/coderabbitai/git-worktree-runner
"""

import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class WorktreeManager:
    """
    Manages git worktrees for the repository using gtr CLI.

    Provides integration with gtr for:
    - Listing worktrees
    - Creating worktrees
    - Removing worktrees
    - Running commands in worktrees
    - Opening worktrees in editors/AI tools
    """

    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path.cwd()
        self._gtr_available = self._check_gtr()

    def _check_gtr(self) -> bool:
        """Check if gtr is available in PATH."""
        result = subprocess.run(["which", "git-gtr"], capture_output=True, text=True)
        return result.returncode == 0

    def _run_gtr(self, args: List[str]) -> Tuple[str, str, int]:
        """Run a gtr command and return (stdout, stderr, returncode)."""
        if not self._gtr_available:
            return ("gtr not found in PATH", "", 1)

        result = subprocess.run(
            ["git", "gtr"] + args,
            capture_output=True,
            text=True,
            cwd=str(self.repo_path),
        )
        return result.stdout, result.stderr, result.returncode

    def list_worktrees(self) -> List[Dict[str, Any]]:
        """
        List all worktrees in the repository.

        Returns:
            List of worktree dictionaries with keys:
            - path: str - worktree path
            - branch: str - branch name
            - status: str - worktree status
        """
        stdout, _, code = self._run_gtr(["list", "--porcelain"])

        if code != 0:
            return self._list_worktrees_fallback()

        worktrees = []
        for line in stdout.strip().split("\n"):
            if line:
                parts = line.split("\t")
                if len(parts) >= 2:
                    worktrees.append(
                        {
                            "path": parts[0],
                            "branch": parts[1],
                            "status": "ok" if len(parts) < 3 else parts[2],
                        }
                    )
                elif len(parts) == 1:
                    worktrees.append(
                        {"path": parts[0], "branch": "unknown", "status": "ok"}
                    )

        return worktrees

    def _list_worktrees_fallback(self) -> List[Dict[str, Any]]:
        """Fallback using native git worktree list."""
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=str(self.repo_path),
        )

        if result.returncode != 0:
            return []

        worktrees = []
        current = {}
        for line in result.stdout.strip().split("\n"):
            if line.startswith("worktree "):
                if current:
                    worktrees.append(current)
                current = {"path": line.replace("worktree ", ""), "status": "ok"}
            elif line.startswith("HEAD "):
                current["branch"] = line.replace("HEAD ", "").strip()
            elif line.startswith("branch "):
                current["branch"] = line.replace("branch ", "").strip()

        if current:
            worktrees.append(current)

        return worktrees

    def create_worktree(
        self,
        branch: str,
        name: Optional[str] = None,
        from_ref: Optional[str] = None,
        no_copy: bool = False,
        no_fetch: bool = False,
        no_hooks: bool = False,
    ) -> Dict[str, Any]:
        """
        Create a new worktree.

        Args:
            branch: Branch name to create worktree from
            name: Optional custom name for worktree directory
            from_ref: Create from specific ref instead of current branch
            no_copy: Skip copying config files
            no_fetch: Skip git fetch
            no_hooks: Skip post-create hooks

        Returns:
            Dict with keys:
            - success: bool
            - worktree_path: str (if successful)
            - error: str (if failed)
        """
        args = ["new", branch]

        if name:
            args.extend(["--name", name])
        if from_ref:
            args.extend(["--from", from_ref])
        if no_copy:
            args.append("--no-copy")
        if no_fetch:
            args.append("--no-fetch")
        if no_hooks:
            args.append("--no-hooks")

        stdout, stderr, code = self._run_gtr(args)

        if code == 0:
            path = (
                stdout.strip()
                if stdout.strip()
                else str(self.repo_path.parent / branch)
            )
            return {"success": True, "worktree_path": path, "branch": branch}
        else:
            return {
                "success": False,
                "error": stderr or stdout or "Failed to create worktree",
                "branch": branch,
            }

    def remove_worktree(
        self, branch: str, delete_branch: bool = False, force: bool = False
    ) -> Dict[str, Any]:
        """
        Remove a worktree.

        Args:
            branch: Branch name (or worktree name) to remove
            delete_branch: Also delete the branch
            force: Force removal even with uncommitted changes

        Returns:
            Dict with keys:
            - success: bool
            - error: str (if failed)
        """
        args = ["rm", branch]

        if delete_branch:
            args.append("--delete-branch")
        if force:
            args.append("--force")

        stdout, stderr, code = self._run_gtr(args)

        if code == 0:
            return {"success": True, "branch": branch}
        else:
            return {
                "success": False,
                "error": stderr or stdout or "Failed to remove worktree",
                "branch": branch,
            }

    def run_in_worktree(
        self, worktree: str, command: List[str]
    ) -> Tuple[str, str, int]:
        """
        Run a command in a specific worktree.

        Args:
            worktree: Branch name or worktree identifier
            command: Command and arguments to run

        Returns:
            Tuple of (stdout, stderr, returncode)
        """
        return self._run_gtr(["run", worktree] + command)

    def open_in_editor(
        self, worktree: str, editor: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Open a worktree in the configured editor.

        Args:
            worktree: Branch name or worktree identifier
            editor: Optional editor override

        Returns:
            Dict with success status
        """
        args = ["editor", worktree]
        if editor:
            args.extend(["--editor", editor])

        stdout, stderr, code = self._run_gtr(args)

        return {"success": code == 0, "error": stderr if code != 0 else None}

    def open_in_ai(
        self,
        worktree: str,
        ai_tool: Optional[str] = None,
        extra_args: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Open a worktree with an AI tool.

        Args:
            worktree: Branch name or worktree identifier
            ai_tool: Optional AI tool override (aider, claude, codex, etc.)
            extra_args: Additional arguments to pass to AI tool

        Returns:
            Dict with success status
        """
        args = ["ai", worktree]
        if ai_tool:
            args.extend(["--ai", ai_tool])
        if extra_args:
            args.append("--")
            args.extend(extra_args)

        stdout, stderr, code = self._run_gtr(args)

        return {"success": code == 0, "error": stderr if code != 0 else None}

    def get_worktree_path(self, worktree: str) -> Optional[str]:
        """
        Get the filesystem path for a worktree.

        Args:
            worktree: Branch name or worktree identifier

        Returns:
            Path string or None if not found
        """
        stdout, _, code = self._run_gtr(["go", worktree])

        if code == 0 and stdout.strip():
            return stdout.strip()
        return None

    def copy_to_worktree(
        self,
        target: str,
        patterns: List[str],
        dry_run: bool = False,
        all_worktrees: bool = False,
    ) -> Dict[str, Any]:
        """
        Copy files from main repo to worktree(s).

        Args:
            target: Target worktree branch name
            patterns: File patterns to copy
            dry_run: Preview without copying
            all_worktrees: Copy to all worktrees

        Returns:
            Dict with success status and details
        """
        args = ["copy", target]

        if dry_run:
            args.append("--dry-run")
        if all_worktrees:
            args.append("--all")

        args.append("--")
        args.extend(patterns)

        stdout, stderr, code = self._run_gtr(args)

        return {
            "success": code == 0,
            "output": stdout,
            "error": stderr if code != 0 else None,
        }

    def clean_worktrees(
        self,
        merged: bool = False,
        dry_run: bool = False,
        yes: bool = False,
        force: bool = False,
    ) -> Dict[str, Any]:
        """
        Clean up worktrees.

        Args:
            merged: Remove worktrees with merged branches
            dry_run: Preview without removing
            yes: Skip confirmation prompts
            force: Force removal even with changes

        Returns:
            Dict with success status and details
        """
        args = ["clean"]

        if merged:
            args.append("--merged")
        if dry_run:
            args.append("--dry-run")
        if yes:
            args.append("--yes")
        if force:
            args.append("--force")

        stdout, stderr, code = self._run_gtr(args)

        return {
            "success": code == 0,
            "output": stdout,
            "error": stderr if code != 0 else None,
        }

    def is_available(self) -> bool:
        """Check if gtr is available."""
        return self._gtr_available

    def get_status(self) -> Dict[str, Any]:
        """Get worktree manager status."""
        return {
            "gtr_available": self._gtr_available,
            "repo_path": str(self.repo_path),
            "worktrees": self.list_worktrees(),
        }
