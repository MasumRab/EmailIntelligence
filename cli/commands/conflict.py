"""
Conflict Commands Module
"""
from typing import Any, Dict, List, Optional
from pathlib import Path

class ConflictCommands:
    """Conflict detection and resolution commands"""
    
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
    
    def detect_conflicts_with_merge_tree(
        self,
        base: str,
        branch_a: str,
        branch_b: str
    ):
        """Detect actual merge conflicts using git merge-tree."""
        self.cli._info(f"🔍 Running merge-tree analysis: {branch_a} vs {branch_b}")
        
        # Validate branches exist
        try:
            self._validate_branch_exists(branch_a)
            self._validate_branch_exists(branch_b)
        except BranchNotFoundError as e:
            raise BranchNotFoundError(f"Branch validation failed: {e}")
        
        # Get merge base for context
        merge_base = self._get_merge_base(branch_a, branch_b)
        self._info(f"✓ Merge base: {merge_base[:8]}...")
        
        # Execute merge-tree to detect conflicts
        try:
            result = subprocess.run(
                ["git", "merge-tree", "--name-only", base, branch_a, branch_b],
                cwd=self.cli.repo_root,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise MergeTreeError(f"git merge-tree failed: {e.stderr}")
        
        # Parse output into ConflictFile objects
        conflicts = self._parse_merge_tree_output(result.stdout, branch_a, branch_b)
        
        self._info(f"✅ Conflict detection complete: {len(conflicts)} conflicts found")
        
        return ConflictReport(
            source_branch=branch_a,
            target_branch=branch_b,
            base_branch=base,
            conflicts=conflicts,
            merge_base_commit=merge_base
        )
    
    def _parse_merge_tree_output(
        self,
        output: str,
        source_branch: str,
        target_branch: str
    ):
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

class ConflictCommands:
    """Conflict detection and resolution commands"""
    
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
