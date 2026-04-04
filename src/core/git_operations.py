"""
Git operations module for EmailIntelligence CLI
Separated from main CLI to follow Single Responsibility Principle
"""
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import json
from datetime import datetime


class GitOperations:
    """Handles git operations and worktree management"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    def check_git_repository(self):
        """Verify we're in a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def create_branch(self, branch_name: str) -> bool:
        """Create a new git branch"""
        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def create_worktree(self, worktree_path: Path, branch_name: str) -> bool:
        """Create a git worktree"""
        try:
            subprocess.run(
                ["git", "worktree", "add", str(worktree_path.resolve()), branch_name],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def get_changed_files(self, branch1: str, branch2: str) -> List[str]:
        """Get list of changed files between two branches"""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", branch1, branch2],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            return [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
        except subprocess.CalledProcessError:
            return []

    def get_commit_history(self, branch: str, limit: int = 10) -> List[Dict[str, str]]:
        """Get commit history for a branch"""
        try:
            result = subprocess.run(
                ["git", "log", f"--max-count={limit}", "--pretty=format:{\"hash\":\"%H\",\"author\":\"%an\",\"date\":\"%ad\",\"message\":\"%s\"}"],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        commit = json.loads(line)
                        commits.append(commit)
                    except json.JSONDecodeError:
                        continue
            return commits
        except subprocess.CalledProcessError:
            return []

    def checkout_branch(self, branch_name: str) -> bool:
        """Checkout a git branch"""
        try:
            subprocess.run(
                ["git", "checkout", branch_name],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def merge_branch(self, source_branch: str, target_branch: str) -> bool:
        """Merge one branch into another"""
        try:
            # Checkout target branch first
            if not self.checkout_branch(target_branch):
                return False
            
            # Perform merge
            subprocess.run(
                ["git", "merge", source_branch],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def cleanup_worktree(self, worktree_path: Path) -> bool:
        """Remove a git worktree"""
        try:
            subprocess.run(
                ["git", "worktree", "remove", str(worktree_path.resolve())],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            # Also remove the directory if it still exists
            if worktree_path.exists():
                import shutil
                shutil.rmtree(worktree_path)
            return True
        except subprocess.CalledProcessError:
            return False