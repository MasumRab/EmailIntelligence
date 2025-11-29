"""
Git-based conflict detection for EmailIntelligence CLI

This module implements the IConflictDetector interface using native git commands
to identify conflicts between branches without checking them out.
"""

import re
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..core.interfaces import IConflictDetector
from ..core.models import (
    Conflict, 
    ConflictBlock, 
    ConflictTypeExtended, 
    RiskLevel
)
from ..core.exceptions import ConflictDetectionError
from ..utils.logger import get_logger
from .repository import RepositoryOperations

logger = get_logger(__name__)


class GitConflictDetector(IConflictDetector):
    """
    Detects conflicts using git merge-tree operations.
    """
    
    def __init__(self, repo_path: Path = None):
        self.repo = RepositoryOperations(repo_path)
        
    async def detect_conflicts(self, pr_id: str, target_branch: str) -> List[Conflict]:
        """
        Detect conflicts for a PR.
        Assumes PR branch name convention or lookup.
        """
        # TODO: Implement PR ID to branch name lookup
        # For now, assume pr_id is the branch name or we can derive it
        source_branch = f"feature/{pr_id}" if not pr_id.startswith("feature/") else pr_id
        return await self.detect_conflicts_between_branches(source_branch, target_branch)

    async def detect_conflicts_between_branches(
        self, 
        source_branch: str, 
        target_branch: str
    ) -> List[Conflict]:
        """
        Detect conflicts between two branches using git merge-tree.
        """
        logger.info("Detecting conflicts", source=source_branch, target=target_branch)
        
        try:
            # Check git version for capability
            version = await self.repo.get_git_version()
            if version < (2, 38, 0):
                logger.warning("Git version < 2.38.0, falling back to basic check")
                return await self._detect_legacy(source_branch, target_branch)
            
            # Use modern merge-tree
            output = await self.repo.run_git(
                ["merge-tree", "--write-tree", "--name-only", target_branch, source_branch],
                check=False  # merge-tree returns non-zero on conflicts
            )
            
            # Parse output
            # Format:
            # <OID>
            # <Conflicting File 1>
            # <Conflicting File 2>
            # ...
            
            lines = output.splitlines()
            if not lines:
                return []
                
            # First line is OID (tree hash)
            tree_oid = lines[0]
            conflicting_files = lines[1:]
            
            conflicts = []
            for file_path in conflicting_files:
                file_path = file_path.strip()
                if not file_path or file_path.startswith("CONFLICT") or file_path.startswith("Auto-merging"):
                    continue
                    
                conflict = await self._analyze_file_conflict(
                    file_path, 
                    source_branch, 
                    target_branch,
                    tree_oid
                )
                conflicts.append(conflict)
                
            return conflicts
            
        except Exception as e:
            logger.error("Conflict detection failed", error=str(e))
            raise ConflictDetectionError(f"Failed to detect conflicts: {str(e)}") from e

    async def _analyze_file_conflict(
        self, 
        file_path: str, 
        source_branch: str, 
        target_branch: str,
        tree_oid: str
    ) -> Conflict:
        """
        Analyze a specific file conflict to extract details and blocks.
        """
        # Get content from both branches
        try:
            source_content = await self.repo.get_file_content(file_path, source_branch)
            target_content = await self.repo.get_file_content(file_path, target_branch)
            
            # TODO: Get base content for 3-way analysis
            # base_sha = await self.repo.get_merge_base(source_branch, target_branch)
            # base_content = await self.repo.get_file_content(file_path, base_sha)
            
            # Get merged content with markers from the tree
            merged_content = await self.repo.get_file_content(file_path, tree_oid)
            blocks = self._parse_conflict_blocks(merged_content, file_path)
            
            # Create conflict object
            return Conflict(
                id=f"conflict-{Path(file_path).name}-{hash(file_path)}",
                type=ConflictTypeExtended.MERGE_CONFLICT,
                severity=RiskLevel.HIGH,
                description=f"Merge conflict in {file_path}",
                file_paths=[file_path],
                details={
                    "source_branch": source_branch,
                    "target_branch": target_branch,
                    "file_type": Path(file_path).suffix
                },
                blocks=blocks
            )
            
        except Exception as e:
            logger.error("Failed to analyze file conflict", file=file_path, error=str(e))
            # Return generic conflict if analysis fails
            return Conflict(
                id=f"conflict-{Path(file_path).name}",
                type=ConflictTypeExtended.MERGE_CONFLICT,
                severity=RiskLevel.HIGH,
                description=f"Merge conflict in {file_path} (analysis failed)",
                file_paths=[file_path]
            )

    async def _detect_legacy(self, source: str, target: str) -> List[Conflict]:
        """Legacy detection for older git versions."""
        # Fallback: Try merge --no-commit --no-ff
        # This is riskier as it modifies the worktree, so we should avoid it if possible
        # Or use `git merge-tree <base> <branch1> <branch2>` (old syntax)
        
        base = await self.repo.get_merge_base(source, target)
        output = await self.repo.run_git(["merge-tree", base, target, source])
        
        # Parse old merge-tree output (complex)
        # For now, just detect if output contains "changed in both"
        
        conflicts = []
        if "changed in both" in output:
            # Very basic parsing
            for line in output.splitlines():
                if "changed in both" in line:
                    # Format: changed in both <file>
                    file_path = line.split("changed in both")[-1].strip()
                    conflicts.append(Conflict(
                        id=f"legacy-{hash(file_path)}",
                        type=ConflictTypeExtended.MERGE_CONFLICT,
                        severity=RiskLevel.HIGH,
                        description=f"Merge conflict in {file_path}",
                        file_paths=[file_path]
                    ))
                    
        return conflicts

    def _parse_conflict_blocks(self, content: str, file_path: str) -> List[ConflictBlock]:
        """Parse conflict blocks from content with markers."""
        blocks = []
        lines = content.splitlines()
        
        current_lines = []
        incoming_lines = []
        start_line = 0
        
        # Simple state machine
        # STATES: NORMAL, IN_CURRENT, IN_INCOMING
        state = "NORMAL"
        
        for i, line in enumerate(lines):
            line_num = i + 1
            
            if line.startswith("<<<<<<<"):
                state = "IN_CURRENT"
                start_line = line_num
                current_lines = []
                incoming_lines = []
            elif line.startswith("======="):
                if state == "IN_CURRENT":
                    state = "IN_INCOMING"
            elif line.startswith(">>>>>>>"):
                if state == "IN_INCOMING":
                    state = "NORMAL"
                    # Create block
                    blocks.append(ConflictBlock(
                        file_path=file_path,
                        start_line=start_line,
                        end_line=line_num,
                        current_content="\n".join(current_lines),
                        incoming_content="\n".join(incoming_lines),
                        conflict_marker_type="git"
                    ))
            else:
                if state == "IN_CURRENT":
                    current_lines.append(line)
                elif state == "IN_INCOMING":
                    incoming_lines.append(line)
                    
        return blocks
