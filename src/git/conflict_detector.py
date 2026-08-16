"""
Git-based conflict detection for EmailIntelligence CLI

This module implements the IConflictDetector interface using native git commands
to identify conflicts between branches without checking them out.
"""

from typing import List, Optional, Dict
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
    Detects conflicts using git merge-tree operations and file parsing.
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
        """
        if pr_id.isdigit():
            return f"pr-{pr_id}"
        else:
            return pr_id

    def _detect_conflicts_with_merge_tree(self, source_branch: str, target_branch: str) -> List[Conflict]:
        """
        Use git merge-tree to detect conflicts between branches.
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
                return []
            elif return_code == 1:
                conflicts = self._parse_merge_tree_output(stdout, source_branch, target_branch)
                return conflicts
            else:
                raise ConflictDetectionError(f"Git merge-tree failed: {stderr}")
                
        except Exception as e:
            raise ConflictDetectionError(f"Git operation failed: {str(e)}")

    def _parse_merge_tree_output(self, output: str, source_branch: str, target_branch: str) -> List[Conflict]:
        """
        Parse the output from git merge-tree to extract conflicts.
        """
        conflicts = []
        
        for line in output.split('\n'):
            if 'conflict' in line.lower() or 'both modified' in line.lower():
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
        conflicts = []
        
        # Look for files with conflict markers
        for file_path in self._get_tracked_files():
            conflict_blocks = self._find_conflict_markers(file_path)
            if conflict_blocks:
                conflict = Conflict(
                    file_path=str(file_path.relative_to(self.repo_path)),
                    conflict_blocks=conflict_blocks,
                    conflict_type=ConflictTypeExtended.CONTENT,
                    severity=self._determine_severity(conflict_blocks),
                    description="File contains git conflict markers",
                    resolution_strategy="resolve_manually"
                )
                conflicts.append(conflict)
        
        # Also check for unmerged files from git's perspective
        try:
            cmd = ["git", "diff", "--name-only", "--diff-filter=U"]
            stdout, _, code = self.repo_ops.run_command_sync(cmd)
            
            if code == 0:
                unmerged_files = stdout.strip().split('\n')
                for f in unmerged_files:
                    if f and not any(c.file_path == f for c in conflicts):
                        conflict = Conflict(
                            file_path=f,
                            conflict_blocks=[],
                            conflict_type=ConflictTypeExtended.MERGE,
                            severity=RiskLevel.HIGH,
                            description="Unmerged file detected in index",
                            resolution_strategy="resolve_manually"
                        )
                        conflicts.append(conflict)
        except Exception:
            pass
            
        return conflicts

    def _get_tracked_files(self) -> List[Path]:
        """Get list of tracked files in the repository"""
        try:
            stdout, _, code = self.repo_ops.run_command_sync(["git", "ls-files"])
            if code == 0:
                return [self.repo_path / f for f in stdout.strip().split('\n') if f]
            else:
                return []
        except Exception:
            return []

    def _find_conflict_markers(self, file_path: Path) -> List[ConflictBlock]:
        """Find conflict markers in a file"""
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            return []
        
        conflict_blocks = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            if line.startswith("<<<<<<<"):
                start_line = i
                content_before = []
                content_after = []
                
                j = i + 1
                while j < len(lines):
                    if lines[j].startswith("======="):
                        break
                    if lines[j].startswith(">>>>>>>"):
                        break
                    content_before.append(lines[j])
                    j += 1
                else:
                    i = j
                    continue
                
                k = j + 1
                while k < len(lines):
                    if lines[k].startswith(">>>>>>>"):
                        break
                    content_after.append(lines[k])
                    k += 1
                else:
                    i = k
                    continue
                
                conflict_block = ConflictBlock(
                    start_line=start_line,
                    end_line=k,
                    conflict_type=ConflictTypeExtended.CONTENT,
                    content_before=content_before,
                    content_after=content_after,
                    content_common=[]
                )
                conflict_blocks.append(conflict_block)
                i = k + 1
            else:
                i += 1
        
        return conflict_blocks

    def _determine_severity(self, conflict_blocks: List[ConflictBlock]) -> RiskLevel:
        """Determine severity based on conflict characteristics"""
        if len(conflict_blocks) > 5:
            return RiskLevel.HIGH
        elif len(conflict_blocks) > 2:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
