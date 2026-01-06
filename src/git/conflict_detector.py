"""
Git-based conflict detection for EmailIntelligence CLI

This module implements the IConflictDetector interface using native git commands
to identify conflicts between branches without checking them out.
"""

from typing import List
from pathlib import Path
import re
import hashlib
import subprocess

from ..core.interfaces import IConflictDetector
from ..core.conflict_models import Conflict, ConflictBlock, ConflictTypeExtended, RiskLevel
from ..core.exceptions import ConflictDetectionError
from ..utils.logger import get_logger
from .repository import RepositoryOperations


logger = get_logger(__name__)


class GitConflictDetector(IConflictDetector):
    """
    Detects conflicts using git merge-tree operations.
    """

    def __init__(self, repo_path: Path = None):
        self.repo_path = repo_path or Path.cwd()
        self.repo_ops = RepositoryOperations(self.repo_path)

    def detect_conflicts(self, pr_id: str, target_branch: str) -> List[Conflict]:
        """
        Detect conflicts between a PR and a target branch using git merge-tree.
        
        Args:
            pr_id: The pull request ID (typically a branch name)
            target_branch: The target branch to compare against
            
        Returns:
            List of detected conflicts
        """
        try:
            # Get the source branch from PR ID
            source_branch = self._get_source_branch_from_pr(pr_id)
            
            # Use git merge-tree to detect conflicts without checking out
            conflicts = self._detect_conflicts_with_merge_tree(source_branch, target_branch)
            
            logger.info(f"Detected {len(conflicts)} conflicts between {source_branch} and {target_branch}")
            return conflicts
            
        except Exception as e:
            logger.error(f"Error detecting conflicts: {e}")
            raise ConflictDetectionError(f"Failed to detect conflicts: {str(e)}")

    def _get_source_branch_from_pr(self, pr_id: str) -> str:
        """
        Get the source branch name from a PR ID.
        
        Args:
            pr_id: The pull request ID (e.g., "123" or "feature/branch-name")
            
        Returns:
            Source branch name
        """
        # If pr_id looks like a number, try to get the branch from git
        if pr_id.isdigit():
            # This is likely a PR number, we'll assume the branch follows a convention
            # In a real implementation, this would fetch from GitHub API
            return f"pr-{pr_id}"
        else:
            # Assume it's already a branch name
            return pr_id

    def _detect_conflicts_with_merge_tree(self, source_branch: str, target_branch: str) -> List[Conflict]:
        """
        Use git merge-tree to detect conflicts between branches.
        
        Args:
            source_branch: Source branch name
            target_branch: Target branch name
            
        Returns:
            List of conflicts
        """
        try:
            # Run git merge-tree to detect conflicts
            cmd = [
                "git", "merge-tree",
                f"refs/heads/{target_branch}",
                f"refs/heads/{source_branch}"
            ]
            
            stdout, stderr, return_code = self.repo_ops.run_command_sync(cmd)
            
            if return_code == 0:
                # No conflicts
                return []
            elif return_code == 1:
                # Conflicts detected - this is expected
                conflicts = self._parse_merge_tree_output(stdout, source_branch, target_branch)
                return conflicts
            else:
                # Actual error
                raise ConflictDetectionError(f"Git merge-tree failed: {stderr}")
                
        except Exception as e:
            raise ConflictDetectionError(f"Git operation failed: {str(e)}")

    def _parse_merge_tree_output(self, output: str, source_branch: str, target_branch: str) -> List[Conflict]:
        """
        Parse the output from git merge-tree to extract conflicts.
        
        Args:
            output: Output from git merge-tree command
            source_branch: Source branch name
            target_branch: Target branch name
            
        Returns:
            List of Conflict objects
        """
        conflicts = []
        
        # Parse the merge-tree output to identify conflicted files
        # This is a simplified parser - a full implementation would be more robust
        for line in output.split('\n'):
            if 'conflict' in line.lower() or 'both modified' in line.lower():
                # Extract file path from the line
                # This is a simplified approach - real parsing would be more sophisticated
                import re
                match = re.search(r'[^/\\]+\.(py|js|ts|json|md|txt)', line)
                if match:
                    file_path = match.group(0)
                    conflict = Conflict(
                        file_path=file_path,
                        conflict_blocks=[],
                        conflict_type=ConflictTypeExtended.MERGE,
                        severity=RiskLevel.HIGH,
                        description=f"Conflict detected in merge between {source_branch} and {target_branch}",
                        resolution_strategy="merge"
                    )
                    conflicts.append(conflict)
        
        return conflicts

    def detect_conflicts_in_repo(self) -> List[Conflict]:
        """
        Detect conflicts in the current repository state (e.g., unmerged files).
        
        Returns:
            List of conflicts
        """
        try:
            # Check for files with conflict markers
            cmd = ["git", "diff", "--check"]
            stdout, stderr, return_code = self.repo_ops.run_command_sync(cmd)
            
            conflicts = []
            if stdout:
                # Parse diff output for conflicts
                conflicts.extend(self._parse_diff_output_for_conflicts(stdout))
            
            # Also check for unmerged files
            cmd = ["git", "diff", "--name-only", "--diff-filter=U"]
            stdout, stderr, return_code = self.repo_ops.run_command_sync(cmd)
            
            for file_path in stdout.strip().split('\n'):
                if file_path:
                    conflict = Conflict(
                        file_path=file_path,
                        conflict_blocks=[],
                        conflict_type=ConflictTypeExtended.MERGE,
                        severity=RiskLevel.HIGH,
                        description="Unmerged file detected",
                        resolution_strategy="resolve_manually"
                    )
                    conflicts.append(conflict)
            
            return conflicts
            
        except Exception as e:
            raise ConflictDetectionError(f"Failed to check for conflicts: {str(e)}")

    def _parse_diff_output_for_conflicts(self, diff_output: str) -> List[Conflict]:
        """
        Parse diff output to identify files with conflict markers.
        
        Args:
            diff_output: Output from git diff --check
            
        Returns:
            List of Conflict objects
        """
        conflicts = []
        
        for line in diff_output.split('\n'):
            if '<<<<<<<' in line or '=======' in line or '>>>>>>>':
                # Find the file path in the diff output
                # This is a simplified approach
                pass  # Implementation would be more detailed in a production system
        
        return conflicts

    def _get_tracked_files(self) -> List[Path]:
        """Get list of tracked files in the repository"""
        try:
            stdout, stderr, return_code = self.repo_ops.run_command_sync(["git", "ls-files"])
            if return_code == 0:
                return [self.repo_path / f for f in stdout.strip().split('\n') if f]
            else:
                return []
        except Exception:
            return []