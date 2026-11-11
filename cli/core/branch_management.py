"""
Branch Management Module
"""
from typing import Any, Dict, List, Optional
from pathlib import Path

class BranchManager:
    """Branch operations and management"""
    
    def __init__(self, cli_base):
        self.cli = cli_base
        self.logger = getattr(cli_base, 'logger', None)
    
    def _info(self, message: str) -> None:
        if self.logger:
            self.logger.info(message)
    
    def _warn(self, message: str) -> None:
        if self.logger:
            self.logger.warning(f"⚠️  {message}")
    
    def _error(self, message: str) -> None:
        if self.logger:
            self.logger.error(f"❌ {message}")
    
    def _success(self, message: str) -> None:
        if self.logger:
            self.logger.info(f"✅ {message}")
    
    def _get_merge_base(self, branch_a: str, branch_b: str) -> str:
        """Get the merge base commit between two branches."""
        try:
            result = subprocess.run(
                ["git", "merge-base", branch_a, branch_b],
                cwd=self.cli.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise GitOperationError(f"Failed to find merge base: {e.stderr}")
    
    def _validate_branch_exists(self, branch: str) -> None:
        """Validate that a branch exists locally or remotely."""
        # Try local branch first
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=self.cli.repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.returncode == 0:
            return
        
        # Try remote branches
        result = subprocess.run(
            ["git", "branch", "-r", "--format=%(refname:short)"],
            cwd=self.cli.repo_root,
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.split('\n'):
            branch = line.strip().replace('origin/', '')
            if branch == branch:
                return
        
        raise BranchNotFoundError(f"Branch '{branch}' not found locally or on remote origin")
    
    def _validate_branches_exist(self, branches: List[str]) -> None:
        """Validate that all specified branches exist."""
        for branch in branches:
            self._validate_branch_exists(branch)
    
    def _matches_pattern(self, branch: str, pattern: str) -> bool:
        """Check if branch name matches exclusion pattern."""
        import fnmatch
        return fnmatch.fnmatch(branch, pattern)
    
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
                cwd=self.cli.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
            local_branches = [b.strip() for b in result.stdout.split('\n') if b.strip()]
            
            # Get remote branches if requested
            if include_remotes:
                result = subprocess.run(
                    ["git", "branch", "-r", "--format=%(refname:short)"],
                    cwd=self.cli.repo_root,
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
            from cli.exceptions import BranchEnumerationError
            raise BranchEnumerationError(f"Failed to enumerate branches: {e.stderr}")
    
    def _scan_branch_pair(
        self,
        source: str,
        target: str,
        use_semantic: bool = False
    ):
        """Scan a single branch pair for conflicts."""
        start_time = time.time()
        
        try:
            # Run conflict detection
            report = self.cli.detect_conflicts_with_merge_tree(target, source, target)
            duration_ms = (time.time() - start_time) * 1000
            
            # If semantic analysis is enabled, enhance the conflict detection
            if use_semantic and report.conflicts:
                self._enhance_with_semantic_analysis(report, target)
            
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
            )

class BranchManager:
    """Branch operations and management"""
    
    def __init__(self, cli_base):
        self.cli = cli_base
        self.logger = getattr(cli_base, 'logger', None)
    
    def _info(self, message: str) -> None:
        if self.logger:
            self.logger.info(message)
    
    def _warn(self, message: str) -> None:
        if self.logger:
            self.logger.warning(f"⚠️  {message}")
    
    def _error(self, message: str) -> None:
        if self.logger:
            self.logger.error(f"❌ {message}")
    
    def _success(self, message: str) -> None:
        if self.logger:
            self.logger.info(f"✅ {message}")
