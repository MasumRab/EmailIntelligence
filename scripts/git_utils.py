#!/usr/bin/env python3
"""
Git Utilities Module

Provides a shared GitHelper class for common git operations across the project.
Centralizes git command execution with proper error handling and logging.
"""

import logging
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple


class GitHelper:
    """
    Shared git operations helper class.
    
    Provides a centralized interface for git operations used across
    atomic_commit_manager.py, docs_branch_versioning.py, and script_sync.py.
    """
    
    def __init__(self, cwd: Optional[Path] = None, logger: Optional[logging.Logger] = None):
        """
        Initialize GitHelper.
        
        Args:
            cwd: Working directory for git operations. Defaults to current directory.
            logger: Optional logger instance for operation logging.
        """
        self.cwd = cwd or Path.cwd()
        self.logger = logger or logging.getLogger("GitHelper")
    
    def run(self, args: List[str], check: bool = True, capture_output: bool = True,
            text: bool = True, timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        """
        Execute a git command with proper error handling.
        
        Args:
            args: Git command arguments (e.g., ["status", "--porcelain"])
            check: Raise CalledProcessError if command returns non-zero
            capture_output: Capture stdout/stderr
            text: Return output as text (str) instead of bytes
            timeout: Optional command timeout in seconds
            
        Returns:
            CompletedProcess instance with command result
            
        Raises:
            subprocess.CalledProcessError: If check=True and command fails
        """
        cmd = ["git"] + args
        self.logger.debug(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            cwd=self.cwd,
            check=check,
            capture_output=capture_output,
            text=text,
            timeout=timeout
        )
        
        return result
    
    def get_current_branch(self) -> str:
        """Get the current git branch name."""
        try:
            result = self.run(["branch", "--show-current"])
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            self.logger.warning("Failed to get current branch")
            return ""
    
    def get_branch_name_from_ref(self) -> str:
        """Get branch name using rev-parse (alternative method)."""
        try:
            result = self.run(["rev-parse", "--abbrev-ref", "HEAD"])
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""
    
    def get_all_branches(self) -> List[str]:
        """Get all local branch names."""
        try:
            result = self.run(["branch"])
            branches = [line.strip().lstrip('*+ ') for line in result.stdout.split('\n') if line.strip()]
            return branches
        except subprocess.CalledProcessError:
            return []
    
    def get_all_branches_verbose(self) -> List[Tuple[str, bool]]:
        """
        Get all local branches with their current status.
        
        Returns:
            List of (branch_name, is_current) tuples
        """
        try:
            result = self.run(["branch", "-v"])
            branches = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    is_current = line.startswith('*')
                    name = parts[1] if is_current else parts[0]
                    branches.append((name, is_current))
            return branches
        except subprocess.CalledProcessError:
            return []
    
    def add(self, paths: List[Path]) -> bool:
        """
        Add files to git staging.
        
        Args:
            paths: List of file/directory paths to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            path_strs = [str(self.cwd / p) for p in paths]
            self.run(["add"] + path_strs)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to add files: {e}")
            return False
    
    def commit(self, message: str, allow_empty: bool = False) -> Optional[str]:
        """
        Create a git commit.
        
        Args:
            message: Commit message
            allow_empty: Allow empty commits
            
        Returns:
            Commit hash if successful, None otherwise
        """
        try:
            args = ["commit", "-m", message]
            if allow_empty:
                args.append("--allow-empty")
            self.run(args)
            
            # Get commit hash
            hash_result = self.run(["rev-parse", "HEAD"])
            return hash_result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to commit: {e}")
            return None
    
    def get_commit_hash(self, ref: str = "HEAD") -> Optional[str]:
        """
        Get commit hash for a reference.
        
        Args:
            ref: Git reference (default: HEAD)
            
        Returns:
            Full commit hash or None if not found
        """
        try:
            result = self.run(["rev-parse", ref])
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None
    
    def get_status(self, porcelain: bool = True) -> str:
        """
        Get git status.
        
        Args:
            porcelain: Use porcelain output format
            
        Returns:
            Status output string
        """
        args = ["status"]
        if porcelain:
            args.append("--porcelain")
        
        try:
            result = self.run(args)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""
    
    def is_dirty(self) -> bool:
        """Check if there are uncommitted changes."""
        return bool(self.get_status())
    
    def has_staged_changes(self) -> bool:
        """Check if there are staged changes."""
        try:
            result = self.run(["diff", "--cached", "--name-only"])
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False
    
    def get_staged_files(self, directory_prefix: Optional[str] = None) -> List[str]:
        """
        Get list of staged files.
        
        Args:
            directory_prefix: Filter to files starting with this prefix
            
        Returns:
            List of staged file paths
        """
        try:
            result = self.run(["diff", "--cached", "--name-only"])
            files = result.stdout.strip().split('\n')
            if directory_prefix:
                files = [f for f in files if f.startswith(directory_prefix)]
            return [f for f in files if f]
        except subprocess.CalledProcessError:
            return []
    
    def get_staged_docs(self, docs_dir: str = "docs/") -> List[str]:
        """
        Get list of staged documentation files (.md files in docs/).
        
        Args:
            docs_dir: Documentation directory prefix
            
        Returns:
            List of staged .md file paths
        """
        return self.get_staged_files(docs_dir)
    
    def checkout(self, branch: str, paths: Optional[List[str]] = None) -> bool:
        """
        Checkout a branch or specific paths.
        
        Args:
            branch: Branch name to checkout
            paths: Optional specific paths to checkout
            
        Returns:
            True if successful, False otherwise
        """
        try:
            args = ["checkout", branch]
            if paths:
                args.extend(["--"] + paths)
            self.run(args)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def is_branch_checked_out_in_worktree(self, branch: str) -> bool:
        """
        Check if a branch is currently checked out in a git worktree.
        
        Args:
            branch: Branch name to check
            
        Returns:
            True if branch is checked out in a worktree, False otherwise
        """
        try:
            result = self.run(["worktree", "list"])
            for line in result.stdout.split('\n'):
                if f'[{branch}]' in line:
                    return True
            return False
        except subprocess.CalledProcessError:
            return False
    
    def get_worktree_list(self) -> List[str]:
        """
        Get list of worktree paths.
        
        Returns:
            List of worktree directory paths
        """
        try:
            result = self.run(["worktree", "list", "--porcelain"])
            paths = []
            for line in result.stdout.split('\n'):
                if line.startswith("path "):
                    paths.append(line[5:].strip())
            return paths
        except subprocess.CalledProcessError:
            return []
    
    def read_tree(self, source_tree: str, target_tree: str) -> bool:
        """
        Use git read-tree to merge trees (for script sync operations).
        
        Args:
            source_tree: Source tree reference (e.g., 'main:scripts')
            target_tree: Target tree reference (e.g., 'feature:scripts')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.run(["read-tree", "-m", "-u", source_tree, target_tree])
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"read-tree failed: {e}")
            return False
    
    def ls_tree(self, treeish: str, path: str = "") -> str:
        """
        List contents of a tree object.
        
        Args:
            treeish: Treeish reference (branch, commit, etc.)
            path: Optional subdirectory path
            
        Returns:
            ls-tree output
        """
        args = ["ls-tree", "-d" if not path else "-r", treeish]
        if path:
            args.append(path)
        
        try:
            result = self.run(args)
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""
    
    def tree_exists(self, treeish: str, path: str = "") -> bool:
        """
        Check if a tree path exists in a given treeish.
        
        Args:
            treeish: Treeish reference (branch, commit, etc.)
            path: Subdirectory path to check
            
        Returns:
            True if path exists, False otherwise
        """
        return bool(self.ls_tree(treeish, path))
    
    def reset_hard(self, ref: str) -> bool:
        """
        Reset working tree to a reference.
        
        Args:
            ref: Git reference to reset to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.run(["reset", "--hard", ref])
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Reset failed: {e}")
            return False
    
    def log(self, max_count: int = 10, format_str: Optional[str] = None) -> List[str]:
        """
        Get git log entries.
        
        Args:
            max_count: Maximum number of entries
            format_str: Custom format string
            
        Returns:
            List of log entries
        """
        args = ["log", f"-{max_count}", "--oneline"]
        if format_str:
            args.append(f"--format={format_str}")
        
        try:
            result = self.run(args)
            return result.stdout.strip().split('\n')
        except subprocess.CalledProcessError:
            return []
    
    def get_last_commit_message(self) -> str:
        """Get the message of the most recent commit."""
        try:
            result = self.run(["log", "-1", "--format=%s"])
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""


def create_git_helper(cwd: Optional[Path] = None, log_level: int = logging.INFO) -> GitHelper:
    """
    Factory function to create a GitHelper with default configuration.
    
    Args:
        cwd: Working directory for git operations
        log_level: Logging level for the helper's logger
        
    Returns:
        Configured GitHelper instance
    """
    logger = logging.getLogger("GitHelper")
    logger.setLevel(log_level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return GitHelper(cwd=cwd, logger=logger)


# Convenience functions for simple scripts
def get_current_branch(cwd: Optional[Path] = None) -> str:
    """Get current branch name (convenience function)."""
    helper = create_git_helper(cwd)
    return helper.get_current_branch()


def is_clean(cwd: Optional[Path] = None) -> bool:
    """Check if repository is clean (no uncommitted changes)."""
    helper = create_git_helper(cwd)
    return not helper.is_dirty()


def has_nothing_to_commit() -> bool:
    """Check if there is nothing to commit."""
    helper = create_git_helper()
    return not helper.has_staged_changes()