"""
EmailIntelligence CLI - Data Models

This module contains all dataclasses and enumerations used by the EmailIntelligence CLI.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


# ============================================================================
# ENUMERATIONS
# ============================================================================


class ConflictType(Enum):
    """Types of merge conflicts detected by git merge-tree"""
    CHANGED_IN_BOTH = "changed_in_both"      # Both branches modified same file
    ADDED_IN_BOTH = "added_in_both"          # Both branches added same file
    REMOVED_IN_SOURCE = "removed_in_source"  # Removed in source branch
    REMOVED_IN_TARGET = "removed_in_target"  # Removed in target branch
    MODIFIED_DELETED = "modified_deleted"    # Modified in one, deleted in other


class ConflictSeverity(Enum):
    """Severity assessment for conflicts"""
    HIGH = "high"      # Both branches modified same areas - high risk
    MEDIUM = "medium"  # One branch deleted/modified - moderate risk
    LOW = "low"        # Minor conflicts - low risk


# ============================================================================
# DATA STRUCTURES
# ============================================================================


@dataclass
class ConflictRegion:
    """Represents a specific conflict region within a file"""
    start_line: int
    end_line: int
    content_ours: str                    # Content from source branch
    content_theirs: str                  # Content from target branch
    content_base: Optional[str] = None   # Content from merge base
    
    @property
    def region_size(self) -> int:
        """Number of lines in this conflict region"""
        return self.end_line - self.start_line + 1


@dataclass
class ConflictFile:
    """Structured conflict information for a single file"""
    file_path: str
    conflict_type: ConflictType
    conflict_regions: List[ConflictRegion] = field(default_factory=list)
    resolution_status: str = "unresolved"  # unresolved|resolved_ours|resolved_theirs|resolved_manual
    severity: ConflictSeverity = ConflictSeverity.MEDIUM
    lines_affected: int = 0               # Total lines affected by conflicts
    
    @property
    def is_resolved(self) -> bool:
        """Check if this file has been resolved"""
        return self.resolution_status != "unresolved"
    
    @property
    def total_conflict_lines(self) -> int:
        """Total lines involved in all conflict regions"""
        return sum(r.region_size for r in self.conflict_regions)


@dataclass
class ConflictReport:
    """Complete conflict detection result"""
    source_branch: str
    target_branch: str
    base_branch: str
    conflicts: List[ConflictFile]
    merge_base_commit: str
    detection_method: str = "git merge-tree"
    detected_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    @property
    def total_conflicts(self) -> int:
        """Total number of conflicted files"""
        return len(self.conflicts)
    
    @property
    def files_requiring_resolution(self) -> List[str]:
        """List of files that still need resolution"""
        return [c.file_path for c in self.conflicts if c.resolution_status == "unresolved"]
    
    @property
    def severity_summary(self) -> Dict[str, int]:
        """Count of conflicts by severity level"""
        summary = {"high": 0, "medium": 0, "low": 0}
        for c in self.conflicts:
            summary[c.severity.value] += 1
        return summary
    
    @property
    def unresolved_count(self) -> int:
        """Number of files still requiring resolution"""
        return len(self.files_requiring_resolution)


@dataclass
class BranchPairResult:
    """Result for a single branch pair scan"""
    source: str                          # Source branch name
    target: str                          # Target branch name
    conflict_count: int                  # Number of conflicted files
    conflict_files: List[str]            # List of files with conflicts
    severity: str                        # Overall severity: low|medium|high|error
    scan_duration_ms: float              # Time to scan this pair
    
    @property
    def has_conflicts(self) -> bool:
        """Check if conflicts exist"""
        return self.conflict_count > 0


@dataclass
class ConflictMatrix:
    """Complete conflict matrix for all branch pairs"""
    scanned_at: str
    branches: List[str]                  # All branches scanned
    target_branches: List[str]           # Target branches used
    total_pairs: int                     # Total pairs analyzed
    pairs_with_conflicts: int            # Pairs that have conflicts
    results: List[BranchPairResult]      # Individual pair results
    
    @property
    def conflict_rate(self) -> float:
        """Percentage of pairs with conflicts"""
        return (self.pairs_with_conflicts / self.total_pairs * 100) if self.total_pairs > 0 else 0.0
    
    @property
    def total_conflicts(self) -> int:
        """Total conflicts across all pairs"""
        return sum(r.conflict_count for r in self.results)
    
    @property
    def high_conflict_pairs(self) -> List[BranchPairResult]:
        """Pairs with high severity conflicts"""
        return [r for r in self.results if r.severity == "high"]


@dataclass
class SemanticConflictAnalysis:
    """Advanced semantic conflict analysis using multiple matching techniques"""
    file_path: str
    semantic_similarity: float  # 0.0 to 1.0
    fuzzy_match_score: float    # 0.0 to 1.0
    structural_similarity: float  # 0.0 to 1.0
    conflict_regions: List[ConflictRegion]
    resolution_suggestions: List[str] = field(default_factory=list)

    @property
    def combined_score(self) -> float:
        """Calculate combined similarity score from all techniques"""
        return (self.semantic_similarity + self.fuzzy_match_score + 
                self.structural_similarity) / 3.0

    @property
    def has_high_confidence(self) -> bool:
        """Check if analysis has high confidence (all scores > 0.7)"""
        return (self.semantic_similarity > 0.7 and 
                self.fuzzy_match_score > 0.7 and 
                self.structural_similarity > 0.7)


@dataclass
class WorkspaceInfo:
    """Information about a git worktree workspace"""
    name: str
    path: str
    branch: str
    commit_hash: str
    created_at: str
    status: str = "active"  # active|error|cleanup_pending


class GitWorkspaceManager:
    """Fallback workspace manager for git worktree operations"""
    def __init__(self, repo_root: str, worktrees_dir: str = None):
        self.repo_root = repo_root
        self.worktrees_dir = worktrees_dir or f"{repo_root}/.git/worktrees"
    
    def create_workspace(self, name: str, branch: str) -> str:
        """Create a new worktree workspace"""
        import subprocess
        import os
        
        workspace_path = f"{self.worktrees_dir}/{name}"
        
        # Create worktree
        result = subprocess.run(
            ["git", "worktree", "add", workspace_path, branch],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise Exception(f"Failed to create worktree: {result.stderr}")
        
        return workspace_path
    
    def list_workspaces(self) -> List[WorkspaceInfo]:
        """List all active workspaces"""
        import subprocess
        import json
        
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        workspaces = []
        if result.returncode == 0:
            current_info = {}
            for line in result.stdout.strip().split('\n'):
                if line.startswith('worktree '):
                    if current_info:
                        workspaces.append(WorkspaceInfo(**current_info))
                    current_info = {'path': line.split(' ', 1)[1]}
                elif line.startswith('branch '):
                    current_info['branch'] = line.split(' ', 1)[1]
                elif line.startswith('HEAD '):
                    current_info['commit_hash'] = line.split(' ', 1)[1]
                    current_info['created_at'] = datetime.now().isoformat()
                    current_info['name'] = os.path.basename(current_info['path'])
        
        if current_info:
            workspaces.append(WorkspaceInfo(**current_info))
        
        return workspaces
    
    def remove_workspace(self, name: str, force: bool = False) -> bool:
        """Remove a worktree workspace"""
        import subprocess
        
        cmd = ["git", "worktree", "remove", name]
        if force:
            cmd.append("--force")
        
        result = subprocess.run(
            cmd,
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        return result.returncode == 0


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    # Enums
    'ConflictType',
    'ConflictSeverity',
    # Dataclasses
    'ConflictRegion',
    'ConflictFile',
    'ConflictReport',
    'BranchPairResult',
    'ConflictMatrix',
    'SemanticConflictAnalysis',
]
