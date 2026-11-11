"""
Conflict Resolution Module
"""
import asyncio
import hashlib
import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Optional imports for interface-based architecture (may not exist in all setups)
try:
    from core.conflict_models import Conflict, ConflictBlock, ConflictTypeExtended, RiskLevel
except ImportError:
    Conflict = ConflictBlock = ConflictTypeExtended = RiskLevel = None

try:
    from analysis.conflict_analyzer import ConflictAnalyzer
except ImportError:
    ConflictAnalyzer = None

try:
    from analysis.constitutional.analyzer import ConstitutionalAnalyzer
except ImportError:
    ConstitutionalAnalyzer = None

try:
    from resolution.auto_resolver import AutoResolver
except ImportError:
    AutoResolver = None

try:
    from resolution.semantic_merger import SemanticMerger
except ImportError:
    SemanticMerger = None

try:
    from strategy.generator import StrategyGenerator
except ImportError:
    StrategyGenerator = None

try:
    from strategy.risk_assessor import RiskAssessor
except ImportError:
    RiskAssessor = None

try:
    from validation.validator import Validator
except ImportError:
    Validator = None

try:
    import yaml
except ImportError:
    yaml = None

from cli.conflict import ConflictDetector
from cli.exceptions import (
    BranchNotFoundError,
    GitOperationError,
    MergeTreeError,
)
from cli.models import (
    BranchPairResult,
    ConflictFile,
    ConflictMatrix,
    ConflictReport,
    ConflictSeverity,
    ConflictType,
    SemanticConflictAnalysis,
    GitWorkspaceManager,
)
from cli.semantic import SemanticConflictDetector
from cli.workspace import RobustWorkspaceManager

logger = logging.getLogger(__name__)


class ConflictResolver:
    """Conflict detection and resolution"""

    def __init__(self, cli_base):
        self.cli = cli_base
        self.logger = getattr(cli_base, 'logger', None)
    
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
        self.cli._info(f"🔍 Running merge-tree analysis: {branch_a} vs {branch_b}")
        
        # Validate branches exist
        try:
            self._validate_branch_exists(branch_a)
            self._validate_branch_exists(branch_b)
        except BranchNotFoundError as e:
            raise BranchNotFoundError(f"Branch validation failed: {e}")
        
        # Get merge base for context
        merge_base = self._get_merge_base(branch_a, branch_b)
        self.cli._info(f"✓ Merge base: {merge_base[:8]}...")
        
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
        
        self.cli._info(f"✅ Conflict detection complete: {len(conflicts)} conflicts found")
        
        return ConflictReport(
            source_branch=branch_a,
            target_branch=branch_b,
            base_branch=base,
            conflicts=conflicts,
            merge_base_commit=merge_base
        )
    
    def _enhance_with_semantic_analysis(self, report: ConflictReport, base_branch: str) -> None:
        """Enhance conflict report with semantic analysis.
        
        Args:
            report: ConflictReport to enhance
            base_branch: Base branch name for worktree paths
        """
        semantic_detector = SemanticConflictDetector()
        
        for conflict in report.conflicts:
            file_path = conflict.file_path
            
            # Try to read both versions of the file
            try:
                worktree_path = self.cli.worktrees_dir / base_branch
                path_a = worktree_path / file_path
                path_b = worktree_path / file_path  # This would need actual paths
                
                # For now, we'll just add placeholder semantic data
                # In a full implementation, we would read the actual file contents
                conflict.severity = ConflictSeverity.MEDIUM  # Default
                
            except Exception as e:
                self.cli._warn(f"Could not perform semantic analysis for {file_path}: {e}")
    
    def _detect_conflicts(self, worktree_a_path: Path, worktree_b_path: Path) -> List[Dict[str, Any]]:
        """Detect conflicts between worktrees"""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=worktree_a_path,
                check=True,
                capture_output=True,
                text=True
            )

            conflicts = []
            for file_path in result.stdout.strip().split('\n'):
                if file_path and not file_path.startswith('.'):
                    conflict_info = {
                        'file': file_path,
                        'path_a': str(worktree_a_path / file_path),
                        'path_b': str(worktree_b_path / file_path),
                        'detected_at': datetime.now().isoformat()
                    }
                    conflicts.append(conflict_info)

            self.cli._info(f"🔍 Detected {len(conflicts)} potential conflicts")
            return conflicts

        except subprocess.CalledProcessError:
            return []
    
    def _detect_conflicts_interface_based(self, worktree_a_path: Path, worktree_b_path: Path) -> List[Dict[str, Any]]:
        """Detect conflicts between worktrees using the new interface-based detector"""
        try:
            detector = GitConflictDetector(self.cli.repo_root)
            conflicts = detector.detect_conflicts_in_repo()

            conflict_list = []
            for conflict in conflicts:
                conflict_info = {
                    'file': conflict.file_path,
                    'path_a': str(worktree_a_path / conflict.file_path),
                    'path_b': str(worktree_b_path / conflict.file_path),
                    'detected_at': datetime.now().isoformat(),
                    'conflict_type': conflict.conflict_type.value,
                    'severity': conflict.severity.value,
                    'description': conflict.description
                }
                conflict_list.append(conflict_info)

            self.cli._info(f"🔍 Detected {len(conflict_list)} potential conflicts using new detector")
            return conflict_list

        except Exception as e:
            self.cli._error(f"Error detecting conflicts: {str(e)}")
            return self._detect_conflicts(worktree_a_path, worktree_b_path)
    
    def detect_conflicts_with_semantic_analysis(
        self,
        base_branch: str,
        branch_a: str,
        branch_b: str,
        worktree_a_path: Path,
        worktree_b_path: Path
    ) -> List[Dict[str, Any]]:
        """Enhanced conflict detection with semantic analysis.
        
        Args:
            base_branch: The base branch for comparison
            branch_a: First branch to compare
            branch_b: Second branch to compare
            worktree_a_path: Path to first branch's worktree
            worktree_b_path: Path to second branch's worktree
            
        Returns:
            List of conflict dictionaries with semantic analysis
        """
        # First get traditional conflicts
        traditional_conflicts = self._detect_conflicts_interface_based(
            worktree_a_path, worktree_b_path
        )
        
        if not traditional_conflicts:
            return []
        
        # Initialize semantic detector
        semantic_detector = SemanticConflictDetector()
        
        enhanced_conflicts = []
        
        for conflict in traditional_conflicts:
            file_path = conflict.get('file', '')
            path_a = conflict.get('path_a', '')
            path_b = conflict.get('path_b', '')
            
            # Read file contents
            try:
                with open(path_a, 'r', encoding='utf-8', errors='ignore') as f:
                    content_a = f.read()
                with open(path_b, 'r', encoding='utf-8', errors='ignore') as f:
                    content_b = f.read()
            except Exception as e:
                self.cli._warn(f"Could not read files for semantic analysis: {e}")
                enhanced_conflicts.append(conflict)
                continue
            
            # Perform semantic analysis
            analysis = semantic_detector.detect_conflicts(
                file_path=file_path,
                content_a=content_a,
                content_b=content_b,
                conflict_regions=[]
            )
            
            # Determine enhanced severity
            traditional_severity = conflict.get('severity', 'medium')
            enhanced_severity = self._determine_enhanced_severity(
                traditional_severity, analysis
            )
            
            # Add semantic analysis to conflict info
            enhanced_conflict = {
                **conflict,
                'semantic_similarity': analysis.semantic_similarity,
                'fuzzy_match_score': analysis.fuzzy_match_score,
                'structural_similarity': analysis.structural_similarity,
                'combined_score': analysis.combined_score,
                'resolution_suggestions': analysis.resolution_suggestions,
                'severity': enhanced_severity,
                'detection_method': 'semantic_analysis'
            }
            enhanced_conflicts.append(enhanced_conflict)
        
        self.cli._info(
            f"🔍 Semantic analysis complete: {len(enhanced_conflicts)} conflicts analyzed"
        )
        return enhanced_conflicts
    
    def _determine_enhanced_severity(
        self,
        traditional_conflict: str,
        semantic_conflict: SemanticConflictAnalysis
    ) -> str:
        """Determine combined severity from traditional and semantic analysis.
        
        Args:
            traditional_conflict: Traditional severity level (high/medium/low)
            semantic_conflict: Semantic conflict analysis result
            
        Returns:
            Enhanced severity level
        """
        # Traditional severity weights
        severity_weights = {"high": 1.0, "medium": 0.5, "low": 0.2}
        trad_weight = severity_weights.get(traditional_conflict, 0.5)
        
        # Combined score from semantic analysis
        combined = semantic_conflict.combined_score
        
        # Calculate final score (weighted average)
        final_score = (combined * 0.6) + (trad_weight * 0.4)
        
        if final_score >= 0.7:
            return "high"
        elif final_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def _convert_metadata_to_conflicts(self, metadata_conflicts: List[Dict[str, Any]]) -> List[Conflict]:
        """Convert metadata conflict format to Conflict objects"""
        from core.conflict_models import Conflict, ConflictBlock, ConflictTypeExtended, RiskLevel

        conflicts = []
        for meta_conflict in metadata_conflicts:
            conflict = Conflict(
                file_path=meta_conflict.get('file', 'unknown'),
                conflict_blocks=[],
                conflict_type=ConflictTypeExtended.CONTENT,
                severity=RiskLevel.MEDIUM,
                description=meta_conflict.get('description', ''),
                resolution_strategy=meta_conflict.get('resolution_strategy', 'standard_merge'),
                estimated_resolution_time=meta_conflict.get('estimated_resolution_time', 30)
            )
            conflicts.append(conflict)

        return conflicts
    
    def _validate_branch_exists(self, branch: str) -> None:
        """Validate branch exists"""
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            cwd=self.cli.repo_root,
            capture_output=True
        )
        if result.returncode != 0:
            raise BranchNotFoundError(f"Branch '{branch}' does not exist")
    
    def _get_merge_base(self, branch_a: str, branch_b: str) -> str:
        """Get merge base commit"""
        result = subprocess.run(
            ["git", "merge-base", branch_a, branch_b],
            cwd=self.cli.repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
