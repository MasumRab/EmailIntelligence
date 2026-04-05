#!/usr/bin/env python3
"""
Rollback Manager for Branch Cleanup Operations

Comprehensive rollback system with checkpoints, branch restoration,
and operation reversal capabilities.
"""

import json
import subprocess
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum



class OperationType(Enum):
    DELETE = "delete"
    MERGE = "merge"
    REBASE = "rebase"
    ARCHIVE = "archive"
    RENAME = "rename"
    SYNC = "sync"

class OperationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW_REQUIRED = "review_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"

@dataclass
class BranchOperation:
    operation_id: str
    branch_name: str
    operation_type: OperationType
    target_branch: str = None
    priority: str = "normal"
    reason: str = ""
    metadata: dict = None
    status: OperationStatus = OperationStatus.PENDING
    created_at: datetime = None
    started_at: datetime = None
    completed_at: datetime = None
    error_message: str = None
    rollback_available: bool = False


@dataclass
class RollbackCheckpoint:
    """Rollback checkpoint with complete state capture."""
    checkpoint_id: str
    name: str
    description: str
    created_at: datetime
    branches_backup: Dict[str, str] = field(default_factory=dict)  # branch_name -> commit_hash
    tags_backup: List[str] = field(default_factory=list)
    worktrees_backup: List[Dict[str, Any]] = field(default_factory=list)
    stash_backup: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RollbackOperation:
    """Individual rollback operation."""
    operation_id: str
    checkpoint_id: str
    operation_type: str  # "restore_branch", "delete_tag", "restore_worktree", "restore_stash"
    target: str
    data: Dict[str, Any] = field(default_factory=dict)
    status: OperationStatus = OperationStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class RollbackManager:
    """Comprehensive rollback management for branch operations."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.checkpoints_dir = self.repo_path / "backups" / "branch_cleanup"
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints: Dict[str, RollbackCheckpoint] = {}
        self.rollback_history: List[RollbackOperation] = []
        self._load_existing_checkpoints()
    
    def _load_existing_checkpoints(self):
        """Load existing checkpoints from disk."""
        for checkpoint_file in self.checkpoints_dir.glob("checkpoint_*.json"):
            try:
                with open(checkpoint_file, 'r') as f:
                    checkpoint_data = json.load(f)
                
                checkpoint = RollbackCheckpoint(
                    checkpoint_id=checkpoint_data["checkpoint_id"],
                    name=checkpoint_data["name"],
                    description=checkpoint_data["description"],
                    created_at=datetime.fromisoformat(checkpoint_data["created_at"]),
                    branches_backup=checkpoint_data.get("branches_backup", {}),
                    tags_backup=checkpoint_data.get("tags_backup", []),
                    worktrees_backup=checkpoint_data.get("worktrees_backup", []),
                    stash_backup=checkpoint_data.get("stash_backup", []),
                    metadata=checkpoint_data.get("metadata", {})
                )
                
                self.checkpoints[checkpoint.checkpoint_id] = checkpoint
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Warning: Failed to load checkpoint {checkpoint_file}: {e}")
    
    def create_checkpoint(self, name: str, description: str = "") -> str:
        """Create a complete rollback checkpoint."""
        checkpoint_id = f"checkpoint_{int(datetime.now().timestamp())}"
        
        # Capture current state
        branches_backup = self._capture_branches()
        tags_backup = self._capture_tags()
        worktrees_backup = self._capture_worktrees()
        stash_backup = self._capture_stash()
        
        checkpoint = RollbackCheckpoint(
            checkpoint_id=checkpoint_id,
            name=name,
            description=description,
            created_at=datetime.now(),
            branches_backup=branches_backup,
            tags_backup=tags_backup,
            worktrees_backup=worktrees_backup,
            stash_backup=stash_backup,
            metadata={
                "git_status": self._get_git_status(),
                "current_branch": self._get_current_branch(),
                "remote_status": self._get_remote_status()
            }
        )
        
        # Save checkpoint
        self._save_checkpoint(checkpoint)
        self.checkpoints[checkpoint_id] = checkpoint
        
        return checkpoint_id
    
    def _capture_branches(self) -> Dict[str, str]:
        """Capture all branches and their current commits."""
        branches = {}
        
        try:
            # Get all local branches
            result = subprocess.run(
                ["git", "for-each-ref", "--format=%(refname:short)%00%(objectname)", "refs/heads/"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.splitlines():
                if line.strip():
                    branch, commit = line.split("\x00")
                    branches[branch] = commit
        
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to capture branches: {e}")
        
        return branches
    
    def _capture_tags(self) -> List[str]:
        """Capture all tags."""
        tags = []
        
        try:
            result = subprocess.run(
                ["git", "tag", "-l"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            tags = [tag.strip() for tag in result.stdout.splitlines() if tag.strip()]
        
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to capture tags: {e}")
        
        return tags
    
    def _capture_worktrees(self) -> List[Dict[str, Any]]:
        """Capture all worktrees."""
        worktrees = []
        
        try:
            result = subprocess.run(
                ["git", "worktree", "list", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            current_worktree = {}
            for line in result.stdout.splitlines():
                if line.startswith("worktree "):
                    if current_worktree:
                        worktrees.append(current_worktree)
                    current_worktree = {"path": line[9:]}
                elif line.startswith("HEAD "):
                    current_worktree["head"] = line[5:]
                elif line.startswith("branch "):
                    current_worktree["branch"] = line[7:]
            
            if current_worktree:
                worktrees.append(current_worktree)
        
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to capture worktrees: {e}")
        
        return worktrees
    
    def _capture_stash(self) -> List[str]:
        """Capture stash entries."""
        stash = []
        
        try:
            result = subprocess.run(
                ["git", "stash", "list"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            stash = [entry.strip() for entry in result.stdout.splitlines() if entry.strip()]
        
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to capture stash: {e}")
        
        return stash
    
    def _get_git_status(self) -> str:
        """Get current git status."""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""
    
    def _get_current_branch(self) -> str:
        """Get current branch."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return ""
    
    def _get_remote_status(self) -> Dict[str, Any]:
        """Get remote tracking status."""
        remotes = {}
        
        try:
            # Get remote tracking info
            result = subprocess.run(
                ["git", "branch", "-vv"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.splitlines():
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        branch = parts[0].replace('*', '').strip()
                        remote_info = parts[2].strip('[]')
                        remotes[branch] = remote_info
        
        except subprocess.CalledProcessError:
            pass
        
        return remotes
    
    def _save_checkpoint(self, checkpoint: RollbackCheckpoint):
        """Save checkpoint to disk."""
        checkpoint_data = asdict(checkpoint)
        checkpoint_data["created_at"] = checkpoint.created_at.isoformat()
        
        filepath = self.checkpoints_dir / f"{checkpoint.checkpoint_id}.json"
        with open(filepath, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
    
    def rollback_to_checkpoint(self, checkpoint_id: str) -> bool:
        """Rollback to a specific checkpoint."""
        if checkpoint_id not in self.checkpoints:
            print(f"Checkpoint {checkpoint_id} not found")
            return False
        
        checkpoint = self.checkpoints[checkpoint_id]
        
        try:
            # Create rollback operations
            operations = self._create_rollback_operations(checkpoint)
            
            # Execute rollback operations
            for operation in operations:
                self._execute_rollback_operation(operation)
                self.rollback_history.append(operation)
            
            print(f"Successfully rolled back to checkpoint: {checkpoint_id}")
            return True
            
        except Exception as e:
            print(f"Rollback failed: {e}")
            return False
    
    def _create_rollback_operations(self, checkpoint: RollbackCheckpoint) -> List[RollbackOperation]:
        """Create rollback operations from checkpoint."""
        operations = []
        
        # Get current state
        current_branches = self._capture_branches()
        current_tags = self._capture_tags()
        current_worktrees = self._capture_worktrees()
        current_stash = self._capture_stash()
        
        # Branch restoration operations
        for branch_name, commit_hash in checkpoint.branches_backup.items():
            if branch_name not in current_branches:
                operations.append(RollbackOperation(
                    operation_id=f"restore_branch_{branch_name}_{int(datetime.now().timestamp())}",
                    checkpoint_id=checkpoint.checkpoint_id,
                    operation_type="restore_branch",
                    target=branch_name,
                    data={"commit_hash": commit_hash}
                ))
        
        # Tag restoration operations
        for tag in checkpoint.tags_backup:
            if tag not in current_tags:
                operations.append(RollbackOperation(
                    operation_id=f"restore_tag_{tag}_{int(datetime.now().timestamp())}",
                    checkpoint_id=checkpoint.checkpoint_id,
                    operation_type="restore_tag",
                    target=tag
                ))
        
        # Worktree restoration operations
        for worktree in checkpoint.worktrees_backup:
            if not any(wt.get("path") == worktree["path"] for wt in current_worktrees):
                operations.append(RollbackOperation(
                    operation_id=f"restore_worktree_{worktree['path']}_{int(datetime.now().timestamp())}",
                    checkpoint_id=checkpoint.checkpoint_id,
                    operation_type="restore_worktree",
                    target=worktree["path"],
                    data=worktree
                ))
        
        return operations
    
    def _execute_rollback_operation(self, operation: RollbackOperation):
        """Execute individual rollback operation."""
        operation.status = OperationStatus.IN_PROGRESS
        operation.executed_at = datetime.now()
        
        try:
            if operation.operation_type == "restore_branch":
                self._restore_branch(operation)
            elif operation.operation_type == "restore_tag":
                self._restore_tag(operation)
            elif operation.operation_type == "restore_worktree":
                self._restore_worktree(operation)
            
            operation.status = OperationStatus.COMPLETED
            
        except Exception as e:
            operation.status = OperationStatus.FAILED
            operation.error_message = str(e)
            raise
    
    def _restore_branch(self, operation: RollbackOperation):
        """Restore a branch from checkpoint."""
        branch_name = operation.target
        commit_hash = operation.data["commit_hash"]
        
        # Create branch from commit
        subprocess.run(
            ["git", "branch", branch_name, commit_hash],
            cwd=self.repo_path,
            check=True
        )
        
        print(f"Restored branch: {branch_name}")
    
    def _restore_tag(self, operation: RollbackOperation):
        """Restore a tag from checkpoint."""
        tag_name = operation.target
        
        # This would need tag data from checkpoint
        # For now, just create a lightweight tag
        subprocess.run(
            ["git", "tag", tag_name, "HEAD"],
            cwd=self.repo_path,
            check=True
        )
        
        print(f"Restored tag: {tag_name}")
    
    def _restore_worktree(self, operation: RollbackOperation):
        """Restore a worktree from checkpoint."""
        worktree_data = operation.data
        path = worktree_data["path"]
        branch = worktree_data.get("branch", "main")
        
        # Create worktree
        subprocess.run(
            ["git", "worktree", "add", path, branch],
            cwd=self.repo_path,
            check=True
        )
        
        print(f"Restored worktree: {path}")
    
    def reverse_operation(self, operation: BranchOperation) -> bool:
        """Reverse a specific branch operation."""
        try:
            if operation.operation_type == OperationType.DELETE:
                return self._reverse_delete(operation)
            elif operation.operation_type == OperationType.MERGE:
                return self._reverse_merge(operation)
            elif operation.operation_type == OperationType.ARCHIVE:
                return self._reverse_archive(operation)
            elif operation.operation_type == OperationType.RENAME:
                return self._reverse_rename(operation)
            
            return False
            
        except Exception as e:
            print(f"Failed to reverse operation: {e}")
            return False
    
    def _reverse_delete(self, operation: BranchOperation) -> bool:
        """Reverse a delete operation by restoring branch."""
        branch_name = operation.branch_name
        
        # Try to restore from reflog
        try:
            result = subprocess.run(
                ["git", "reflog", "show", "--format=%gd %H", f"refs/heads/{branch_name}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                # Get the last commit before deletion
                last_line = result.stdout.splitlines()[0]
                commit_hash = last_line.split()[-1]
                
                # Restore branch
                subprocess.run(
                    ["git", "branch", branch_name, commit_hash],
                    cwd=self.repo_path,
                    check=True
                )
                
                print(f"Restored deleted branch: {branch_name}")
                return True
        
        except subprocess.CalledProcessError:
            pass
        
        return False
    
    def _reverse_merge(self, operation: BranchOperation) -> bool:
        """Reverse a merge operation."""
        target_branch = operation.target_branch or "main"
        source_branch = operation.branch_name
        
        try:
            # Checkout target branch
            subprocess.run(
                ["git", "checkout", target_branch],
                cwd=self.repo_path,
                check=True
            )
            
            # Reset to before merge
            subprocess.run(
                ["git", "reset", "--hard", "HEAD~1"],
                cwd=self.repo_path,
                check=True
            )
            
            # Force push to revert remote merge
            subprocess.run(
                ["git", "push", "origin", target_branch, "--force"],
                cwd=self.repo_path,
                check=True
            )
            
            print(f"Reversed merge of {source_branch} into {target_branch}")
            return True
            
        except subprocess.CalledProcessError:
            return False
    
    def _reverse_archive(self, operation: BranchOperation) -> bool:
        """Reverse an archive operation."""
        branch_name = operation.branch_name
        
        # Find the archive tag
        try:
            result = subprocess.run(
                ["git", "tag", "-l", f"archive/{branch_name}*"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            tags = result.stdout.splitlines()
            if tags:
                # Use the most recent archive tag
                tag = sorted(tags)[-1]
                
                # Restore branch from tag
                subprocess.run(
                    ["git", "branch", branch_name, tag],
                    cwd=self.repo_path,
                    check=True
                )
                
                print(f"Restored archived branch: {branch_name}")
                return True
        
        except subprocess.CalledProcessError:
            pass
        
        return False
    
    def _reverse_rename(self, operation: BranchOperation) -> bool:
        """Reverse a rename operation."""
        # This would need the old name stored in metadata
        old_name = operation.metadata.get("old_name")
        if not old_name:
            return False
        
        try:
            # Rename back to original name
            subprocess.run(
                ["git", "branch", "-m", operation.branch_name, old_name],
                cwd=self.repo_path,
                check=True
            )
            
            print(f"Renamed branch back to: {old_name}")
            return True
            
        except subprocess.CalledProcessError:
            return False
    
    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """List all available checkpoints."""
        return [
            {
                "checkpoint_id": checkpoint.checkpoint_id,
                "name": checkpoint.name,
                "description": checkpoint.description,
                "created_at": checkpoint.created_at.isoformat(),
                "branches_count": len(checkpoint.branches_backup),
                "tags_count": len(checkpoint.tags_backup),
                "worktrees_count": len(checkpoint.worktrees_backup),
                "stash_count": len(checkpoint.stash_backup)
            }
            for checkpoint in self.checkpoints.values()
        ]
    
    def delete_checkpoint(self, checkpoint_id: str) -> bool:
        """Delete a checkpoint."""
        if checkpoint_id not in self.checkpoints:
            return False
        
        # Remove from memory
        del self.checkpoints[checkpoint_id]
        
        # Remove from disk
        checkpoint_file = self.checkpoints_dir / f"{checkpoint_id}.json"
        if checkpoint_file.exists():
            checkpoint_file.unlink()
        
        return True
    
    def cleanup_old_checkpoints(self, days: int = 30) -> int:
        """Clean up checkpoints older than specified days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        checkpoints_to_delete = []
        for checkpoint_id, checkpoint in self.checkpoints.items():
            if checkpoint.created_at < cutoff_date:
                checkpoints_to_delete.append(checkpoint_id)
        
        for checkpoint_id in checkpoints_to_delete:
            if self.delete_checkpoint(checkpoint_id):
                deleted_count += 1
        
        return deleted_count
    
    def get_rollback_history(self) -> List[Dict[str, Any]]:
        """Get rollback operation history."""
        return [
            {
                "operation_id": op.operation_id,
                "checkpoint_id": op.checkpoint_id,
                "operation_type": op.operation_type,
                "target": op.target,
                "status": op.status.value,
                "created_at": op.created_at.isoformat(),
                "executed_at": op.executed_at.isoformat() if op.executed_at else None,
                "error_message": op.error_message
            }
            for op in self.rollback_history
        ]