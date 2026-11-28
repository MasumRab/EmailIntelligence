"""
EmailIntelligence CLI - Conflict Detection

This module contains conflict detection functionality including branch scanning
and merge-tree based conflict detection.
"""

import concurrent.futures
import fnmatch
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from cli.exceptions import (
    BranchEnumerationError,
    BranchNotFoundError,
    MergeTreeError,
    ScanExecutionError,
)
from cli.models import (
    BranchPairResult,
    ConflictFile,
    ConflictMatrix,
    ConflictReport,
    ConflictSeverity,
    ConflictType,
)


# ============================================================================
# CONFLICT DETECTION FUNCTIONS
# ============================================================================


class ConflictDetector:
    """
    Handles conflict detection operations including scanning all branch pairs.
    
    This class provides functionality to detect merge conflicts using git merge-tree
    and scan multiple branches systematically.
    """
    
    def __init__(self, repo_root: Path):
        """Initialize the conflict detector.
        
        Args:
            repo_root: Path to the git repository root
        """
        self.repo_root = repo_root
    
    def _matches_pattern(self, branch: str, pattern: str) -> bool:
        """Check if branch name matches exclusion pattern.
        
        Supports fnmatch-style wildcards:
        - * matches everything
        - ? matches any single character
        - [seq] matches any character in seq
        """
        return fnmatch.fnmatch(branch, pattern)
    
    def _get_merge_base(self, branch_a: str, branch_b: str) -> str:
        """Get the merge base commit between two branches."""
        try:
            result = subprocess.run(
                ["git", "merge-base", branch_a, branch_b],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise MergeTreeError(f"Failed to find merge base: {e.stderr}")
    
    def _validate_branch_exists(self, branch: str) -> None:
        """Validate that a branch exists locally or remotely."""
        # Try local branch first
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return
        
        # Try remote branches
        result = subprocess.run(
            ["git", "ls-remote", "--heads", "origin", branch],
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            return
        
        raise BranchNotFoundError(f"Branch '{branch}' not found locally or on remote origin")
    
    def _parse_merge_tree_output(
        self,
        output: str,
        source_branch: str,
        target_branch: str
    ) -> List[ConflictFile]:
        """Parse git merge-tree output into structured ConflictFile objects."""
        conflicts = []
        
        for line in output.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Parse conflict type and file path
            if line.startswith('changed in both:'):
                file_path = line.split(':', 1)[1].strip()
                conflicts.append(ConflictFile(
                    file_path=file_path,
                    conflict_type=ConflictType.CHANGED_IN_BOTH,
                    severity=ConflictSeverity.HIGH
                ))
                
            elif line.startswith('added in both:'):
                file_path = line.split(':', 1)[1].strip()
                conflicts.append(ConflictFile(
                    file_path=file_path,
                    conflict_type=ConflictType.ADDED_IN_BOTH,
                    severity=ConflictSeverity.HIGH
                ))
                
            elif line.startswith('removed in '):
                file_path = line.split(':', 1)[1].strip()
                if 'removed in source' in line:
                    conflict_type = ConflictType.REMOVED_IN_SOURCE
                else:
                    conflict_type = ConflictType.REMOVED_IN_TARGET
                
                conflicts.append(ConflictFile(
                    file_path=file_path,
                    conflict_type=conflict_type,
                    severity=ConflictSeverity.MEDIUM
                ))
        
        return conflicts
    
    def detect_conflicts_with_merge_tree(
        self,
        base: str,
        branch_a: str,
        branch_b: str
    ) -> ConflictReport:
        """Detect actual merge conflicts using git merge-tree."""
        # Validate branches exist
        try:
            self._validate_branch_exists(branch_a)
            self._validate_branch_exists(branch_b)
        except BranchNotFoundError as e:
            raise BranchNotFoundError(f"Branch validation failed: {e}")
        
        # Get merge base for context
        merge_base = self._get_merge_base(branch_a, branch_b)
        
        # Execute merge-tree to detect conflicts
        try:
            result = subprocess.run(
                ["git", "merge-tree", "--name-only", base, branch_a, branch_b],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise MergeTreeError(f"git merge-tree failed: {e.stderr}")
        
        # Parse output into ConflictFile objects
        conflicts = self._parse_merge_tree_output(result.stdout, branch_a, branch_b)
        
        return ConflictReport(
            source_branch=branch_a,
            target_branch=branch_b,
            base_branch=base,
            conflicts=conflicts,
            merge_base_commit=merge_base
        )
    
    def _enumerate_branches(
        self,
        include_remotes: bool = True,
        exclude_patterns: Optional[List[str]] = None
    ) -> List[str]:
        """Enumerate all local and remote branches with filtering."""
        exclude_patterns = exclude_patterns or ['HEAD', 'main', 'develop']
        
        try:
            # Get local branches
            result = subprocess.run(
                ["git", "branch", "--format=%(refname:short)"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            local_branches = [b.strip() for b in result.stdout.split('\n') if b.strip()]
            
            # Get remote branches if requested
            if include_remotes:
                result = subprocess.run(
                    ["git", "branch", "-r", "--format=%(refname:short)"],
                    cwd=self.repo_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                remote_branches = [
                    b.strip().replace('origin/', '')
                    for b in result.stdout.split('\n')
                    if b.strip() and 'origin/HEAD' not in b
                ]
                local_branches = list(set(local_branches + remote_branches))
            
            # Apply exclusions
            if exclude_patterns:
                local_branches = [
                    b for b in local_branches
                    if not any(self._matches_pattern(b, p) for p in exclude_patterns)
                ]
            
            return sorted(list(set(local_branches)))
            
        except subprocess.CalledProcessError as e:
            raise BranchEnumerationError(f"Failed to enumerate branches: {e.stderr}")
    
    def _scan_branch_pair(self, source: str, target: str) -> BranchPairResult:
        """Scan a single branch pair for conflicts."""
        start_time = time.time()
        
        try:
            # Run conflict detection
            report = self.detect_conflicts_with_merge_tree(target, source, target)
            duration_ms = (time.time() - start_time) * 1000
            
            # Determine overall severity
            severity = "low"
            if any(c.severity == ConflictSeverity.HIGH for c in report.conflicts):
                severity = "high"
            elif any(c.severity == ConflictSeverity.MEDIUM for c in report.conflicts):
                severity = "medium"
            
            return BranchPairResult(
                source=source,
                target=target,
                conflict_count=len(report.conflicts),
                conflict_files=[c.file_path for c in report.conflicts],
                severity=severity,
                scan_duration_ms=duration_ms
            )
            
        except (MergeTreeError, BranchNotFoundError) as e:
            return BranchPairResult(
                source=source,
                target=target,
                conflict_count=0,
                conflict_files=[],
                severity="error",
                scan_duration_ms=(time.time() - start_time) * 1000
            )
    
    def scan_all_branches(
        self,
        include_remotes: bool = True,
        target_branches: Optional[List[str]] = None,
        concurrency: int = 4,
        exclude_patterns: Optional[List[str]] = None,
        progress_callback: Optional[callable] = None
    ) -> ConflictMatrix:
        """Scan conflicts across all branch pairs systematically."""
        target_branches = target_branches or ['main']
        exclude_patterns = exclude_patterns or ['main', 'develop', 'HEAD']
        
        try:
            # Enumerate all branches
            all_branches = self._enumerate_branches(include_remotes, exclude_patterns)
            
            # Generate branch pairs (source → target combinations)
            pairs = []
            for source in all_branches:
                for target in target_branches:
                    if source != target:
                        pairs.append((source, target))
            
            # Perform parallel conflict analysis
            results = []
            start_time = time.time()
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = {
                    executor.submit(self._scan_branch_pair, src, tgt): (src, tgt)
                    for src, tgt in pairs
                }
                
                completed = 0
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        results.append(result)
                        completed += 1
                        
                        if progress_callback and completed % 10 == 0:
                            progress_callback(completed, len(pairs))
                        
                    except Exception as e:
                        pass  # Error already handled in _scan_branch_pair
            
            scan_duration_s = time.time() - start_time
            
            # Build conflict matrix result
            conflict_matrix = ConflictMatrix(
                scanned_at=datetime.now().isoformat(),
                branches=all_branches,
                target_branches=target_branches,
                total_pairs=len(pairs),
                pairs_with_conflicts=sum(1 for r in results if r.has_conflicts),
                results=results
            )
            
            # Save analysis results
            analysis_file = self.repo_root / '.emailintelligence' / 'branch_conflict_analysis.json'
            analysis_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(analysis_file, 'w') as f:
                json.dump({
                    'scanned_at': conflict_matrix.scanned_at,
                    'summary': {
                        'total_branches': conflict_matrix.total_pairs,
                        'pairs_with_conflicts': conflict_matrix.pairs_with_conflicts,
                        'conflict_rate': f"{conflict_matrix.conflict_rate:.1f}%",
                        'total_conflicts': conflict_matrix.total_conflicts,
                        'scan_duration_seconds': scan_duration_s
                    },
                    'results': [r.__dict__ for r in results]
                }, f, indent=2)
            
            return conflict_matrix
            
        except BranchEnumerationError as e:
            raise ScanExecutionError(f"Failed to enumerate branches: {e}")
        except Exception as e:
            raise ScanExecutionError(f"All-branches scanning failed: {e}")
    
    def display_scan_summary(self, matrix: ConflictMatrix, duration_s: float) -> None:
        """Display formatted scan summary"""
        print("\n" + "="*80)
        print("ALL-BRANCHES CONFLICT SCAN SUMMARY")
        print("="*80)
        print(f"Scanned at: {matrix.scanned_at}")
        print(f"\nBranches analyzed: {len(matrix.branches)}")
        print(f"Target branches: {', '.join(matrix.target_branches)}")
        print(f"Total pairs: {matrix.total_pairs}")
        print(f"\nPairs with conflicts: {matrix.pairs_with_conflicts}")
        print(f"Conflict rate: {matrix.conflict_rate:.1f}%")
        print(f"Total conflicts found: {matrix.total_conflicts}")
        print(f"Scan duration: {duration_s:.2f}s ({matrix.total_pairs/duration_s:.1f} pairs/sec)")
        print(f"\nHigh severity pairs: {len(matrix.high_conflict_pairs)}")
        for pair in matrix.high_conflict_pairs[:5]:
            print(f"  • {pair.source}→{pair.target}: {pair.conflict_count} conflicts")
        if len(matrix.high_conflict_pairs) > 5:
            print(f"  ... and {len(matrix.high_conflict_pairs)-5} more")
        print("="*80 + "\n")


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'ConflictDetector',
]
