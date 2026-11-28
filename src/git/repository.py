"""
Git repository operations for EmailIntelligence CLI

This module provides a wrapper around common git operations,
handling command execution, error checking, and output parsing.
"""

import asyncio
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

from ..core.exceptions import GitOperationError
from ..utils.logger import get_logger


logger = get_logger(__name__)


class RepositoryOperations:
    """
    Provides a wrapper around git operations for the EmailIntelligence CLI.
    """
    
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path.cwd()
        if not self.repo_path.exists():
            raise ValueError(f"Repository path does not exist: {self.repo_path}")
    
    async def run_command(self, cmd: List[str], cwd: Optional[Path] = None) -> Tuple[str, str, int]:
        """
        Run a git command asynchronously.
        
        Args:
            cmd: Command to run as a list of strings
            cwd: Working directory (defaults to repo_path)
            
        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        working_dir = cwd or self.repo_path
        
        logger.info(f"Running command: {' '.join(cmd)} in {working_dir}")
        
        try:
            # Use subprocess for the git command
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            logger.debug(f"Command completed with return code: {result.returncode}")
            
            return result.stdout, result.stderr, result.returncode
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out: {' '.join(cmd)}"
            logger.error(error_msg)
            raise GitOperationError(error_msg)
        except Exception as e:
            error_msg = f"Error running command: {str(e)}"
            logger.error(error_msg)
            raise GitOperationError(error_msg)
    
    def run_command_sync(self, cmd: List[str], cwd: Optional[Path] = None) -> Tuple[str, str, int]:
        """
        Run a git command synchronously.
        
        Args:
            cmd: Command to run as a list of strings
            cwd: Working directory (defaults to repo_path)
            
        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        working_dir = cwd or self.repo_path
        
        logger.info(f"Running command: {' '.join(cmd)} in {working_dir}")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            logger.debug(f"Command completed with return code: {result.returncode}")
            
            return result.stdout, result.stderr, result.returncode
            
        except subprocess.TimeoutExpired:
            error_msg = f"Command timed out: {' '.join(cmd)}"
            logger.error(error_msg)
            raise GitOperationError(error_msg)
        except Exception as e:
            error_msg = f"Error running command: {str(e)}"
            logger.error(error_msg)
            raise GitOperationError(error_msg)
    
    async def get_current_branch(self) -> str:
        """Get the current git branch."""
        stdout, stderr, code = await self.run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        
        if code != 0:
            raise GitOperationError(f"Failed to get current branch: {stderr}")
        
        return stdout.strip()
    
    def get_current_branch_sync(self) -> str:
        """Get the current git branch synchronously."""
        stdout, stderr, code = self.run_command_sync(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        
        if code != 0:
            raise GitOperationError(f"Failed to get current branch: {stderr}")
        
        return stdout.strip()
    
    async def get_branches(self) -> List[str]:
        """Get a list of all branches."""
        stdout, stderr, code = await self.run_command(["git", "branch", "-a"])
        
        if code != 0:
            raise GitOperationError(f"Failed to get branches: {stderr}")
        
        branches = []
        for line in stdout.strip().split('\n'):
            # Remove leading whitespace and asterisk
            branch = line.strip().replace('*', '').strip()
            if branch:
                branches.append(branch)
        
        return branches
    
    async def get_uncommitted_changes(self) -> List[str]:
        """Get a list of uncommitted changes."""
        stdout, stderr, code = await self.run_command(["git", "status", "--porcelain"])
        
        if code != 0:
            raise GitOperationError(f"Failed to get uncommitted changes: {stderr}")
        
        changes = []
        for line in stdout.strip().split('\n'):
            if line.strip():
                changes.append(line.strip())
        
        return changes
    
    async def get_diff(self, ref1: str, ref2: str = "") -> str:
        """Get the diff between two references."""
        cmd = ["git", "diff"]
        if ref2:
            cmd.extend([ref1, ref2])
        else:
            cmd.append(ref1)
        
        stdout, stderr, code = await self.run_command(cmd)
        
        if code != 0:
            raise GitOperationError(f"Failed to get diff: {stderr}")
        
        return stdout
    
    async def checkout_branch(self, branch_name: str) -> bool:
        """Checkout a branch."""
        stdout, stderr, code = await self.run_command(["git", "checkout", branch_name])
        
        if code != 0:
            logger.error(f"Failed to checkout branch {branch_name}: {stderr}")
            return False
        
        logger.info(f"Successfully checked out branch: {branch_name}")
        return True
    
    async def merge_branch(self, branch_name: str, strategy: str = "") -> Dict[str, Any]:
        """Merge a branch into the current branch."""
        cmd = ["git", "merge"]
        if strategy:
            cmd.extend(["--strategy", strategy])
        cmd.append(branch_name)
        
        stdout, stderr, code = await self.run_command(cmd)
        
        result = {
            "success": code == 0,
            "stdout": stdout,
            "stderr": stderr,
            "return_code": code,
            "has_conflicts": "conflict" in stderr.lower() or code != 0
        }
        
        if result["success"]:
            logger.info(f"Successfully merged branch: {branch_name}")
        else:
            logger.warning(f"Merge failed for branch {branch_name}: {stderr}")
        
        return result
    
    async def get_commit_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get commit history."""
        cmd = ["git", "log", f"--max-count={limit}", "--pretty=format:%H|%s|%an|%ad", "--date=iso"]
        
        stdout, stderr, code = await self.run_command(cmd)
        
        if code != 0:
            raise GitOperationError(f"Failed to get commit history: {stderr}")
        
        commits = []
        for line in stdout.strip().split('\n'):
            if '|' in line:
                parts = line.split('|', 3)  # Split into 4 parts max
                if len(parts) == 4:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1],
                        "author": parts[2],
                        "date": parts[3]
                    })
        
        return commits
    
    async def has_uncommitted_changes(self) -> bool:
        """Check if there are uncommitted changes."""
        changes = await self.get_uncommitted_changes()
        return len(changes) > 0
    
    async def get_file_at_revision(self, file_path: str, revision: str) -> str:
        """Get the content of a file at a specific revision."""
        cmd = ["git", "show", f"{revision}:{file_path}"]
        
        stdout, stderr, code = await self.run_command(cmd)
        
        if code != 0:
            raise GitOperationError(f"Failed to get file {file_path} at revision {revision}: {stderr}")
        
        return stdout