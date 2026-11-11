"""
EmailIntelligence CLI - Git Workspace Management

This module contains classes for managing git workspaces, including worktree
support with fallback to temporary directories when worktrees are unavailable.
"""

import shutil
import subprocess
import tempfile
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Optional

from cli.exceptions import (
    WorkspaceCreationError,
    WorktreeUnavailableError,
)


# ============================================================================
# WORKSPACE MANAGER WITH FALLBACK SUPPORT
# ============================================================================


class GitWorkspaceManager(ABC):
    """Abstract base for workspace management strategies"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
    
    @abstractmethod
    def create_workspace(self, name: str, branch: str) -> Path:
        """Create workspace for specified branch"""
        raise NotImplementedError
    
    @abstractmethod
    def cleanup_workspace(self, name: str) -> bool:
        """Clean up workspace"""
        raise NotImplementedError


class GitWorktreeManager(GitWorkspaceManager):
    """Primary worktree manager using git worktree"""
    
    def __init__(self, repo_root: Path):
        super().__init__(repo_root)
        self.fallback_mode = False
        self.fallback_reason = None
    
    def initialize(self) -> bool:
        """Initialize and verify worktree support"""
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_root,
                check=True,
                capture_output=True
            )
            return True
        except FileNotFoundError:
            self._enable_fallback("git_not_installed", "Git is not installed")
            return False
        except subprocess.CalledProcessError:
            self._enable_fallback("not_a_repo", "Not in a git repository")
            return False
        except PermissionError as e:
            self._enable_fallback("permission_denied", str(e))
            return False
    
    def _enable_fallback(self, reason: str, details: str) -> None:
        """Enable fallback mode"""
        self.fallback_mode = True
        self.fallback_reason = {
            'reason': reason,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
    
    def create_workspace(self, name: str, branch: str) -> Path:
        """Create workspace using git worktree"""
        workspace_path = self.repo_root / ".git" / "worktrees" / name
        workspace_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            subprocess.run(
                ["git", "worktree", "add", str(workspace_path), branch],
                cwd=self.repo_root,
                check=True,
                capture_output=True
            )
            return workspace_path
        except subprocess.CalledProcessError as e:
            raise WorkspaceCreationError(f"Failed to create worktree: {e.stderr}")
    
    def cleanup_workspace(self, name: str) -> bool:
        """Clean up git worktree"""
        try:
            workspace_path = self.repo_root / ".git" / "worktrees" / name
            if workspace_path.exists():
                subprocess.run(
                    ["git", "worktree", "remove", str(workspace_path)],
                    cwd=self.repo_root,
                    check=True,
                    capture_output=True
                )
                return True
            return False
        except subprocess.CalledProcessError:
            return False


class FallbackWorkspaceManager(GitWorkspaceManager):
    """Fallback workspace manager using temporary directories"""
    
    def create_workspace(self, name: str, branch: str) -> Path:
        """Create workspace in temporary directory"""
        workspace_path = Path(tempfile.mkdtemp(prefix=f"ei-{name}-"))
        
        try:
            # Use git archive with list-based subprocess to avoid shell injection
            archive_result = subprocess.run(
                ["git", "archive", branch],
                cwd=self.repo_root,
                capture_output=True,
                check=True
            )
            # Extract using tar with stdin (no shell=True)
            subprocess.run(
                ["tar", "-x", "-C", str(workspace_path)],
                input=archive_result.stdout,
                check=True
            )
        except subprocess.CalledProcessError:
            subprocess.run(
                ["git", "clone", "--no-checkout", str(self.repo_root), str(workspace_path)],
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "checkout", branch],
                cwd=workspace_path,
                check=True,
                capture_output=True
            )
        
        return workspace_path
    
    def cleanup_workspace(self, name: str) -> bool:
        """Clean up temporary directory"""
        try:
            for path in Path(tempfile.gettempdir()).glob(f"ei-{name}-*"):
                shutil.rmtree(path, ignore_errors=True)
            return True
        except Exception:
            return False


class RobustWorkspaceManager:
    """Manager with fallback strategy"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.managers = [
            GitWorktreeManager(repo_root),
            FallbackWorkspaceManager(repo_root)
        ]
        self.current_manager = self.managers[0]
    
    def create_workspace(self, name: str, branch: str) -> Path:
        """Create workspace with fallback if primary fails"""
        for i, manager in enumerate(self.managers):
            try:
                workspace = manager.create_workspace(name, branch)
                if i > 0:
                    print(f"⚠️  Primary manager failed, using fallback: {manager.__class__.__name__}")
                self.current_manager = manager
                return workspace
            except (WorkspaceCreationError, WorktreeUnavailableError) as e:
                if i == len(self.managers) - 1:
                    raise WorkspaceCreationError(f"All workspace managers failed: {e}")
                continue
    
    def cleanup_workspace(self, name: str) -> bool:
        """Clean up workspace using current manager"""
        try:
            return self.current_manager.cleanup_workspace(name)
        except Exception:
            return False


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'GitWorkspaceManager',
    'GitWorktreeManager',
    'FallbackWorkspaceManager',
    'RobustWorkspaceManager',
]
