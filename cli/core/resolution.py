"""
Resolution Module
"""
import hashlib
import json
import logging
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from cli.conflict import ConflictDetector
from cli.exceptions import (
    BranchNotFoundError,
    GitOperationError,
    MergeTreeError,
)
from cli.models import (
    BranchPairResult,
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


class ResolutionManager:
    """Resolution management and push operations"""

    def __init__(self, cli_base):
        self.cli = cli_base
        self.logger = getattr(cli_base, 'logger', None)
    
    def _conflict_to_template(self, conflict: Dict[str, Any], metadata: Dict[str, Any]) -> str:
        """Convert conflict data to specification template format"""
        template_lines = [
            f"Conflict Analysis Report",
            f"PR: {metadata.get('pr_number', 'Unknown')}",
            f"Source Branch: {metadata.get('source_branch', 'Unknown')}",
            f"Target Branch: {metadata.get('target_branch', 'Unknown')}",
            f"File: {conflict.get('file', 'Unknown')}",
            f"Conflict Type: {conflict.get('conflict_type', 'Unknown')}",
            "",
            "Conflict Details:",
        ]
        
        # Add conflict blocks if available
        conflict_blocks = conflict.get('conflicts', [])
        for i, block in enumerate(conflict_blocks):
            template_lines.extend([
                f"Block {i+1}:",
                f"  Start: {block.get('start_line', 'Unknown')}",
                f"  End: {block.get('end_line', 'Unknown')}",
                f"  Type: {block.get('conflict_type', 'Unknown')}",
                ""
            ])
        
        return "\n".join(template_lines)
    
    def setup_resolution(
        self, pr_number: int, source_branch: str, target_branch: str,
        constitution_files: List[str] = None, spec_files: List[str] = None,
        dry_run: bool = False, push_to_target: bool = False,
        no_resolution_branch: bool = False
    ) -> Dict[str, Any]:
        """Setup resolution workspace for a specific PR."""
        resolution_branch = f"pr-{pr_number}-resolution"
        worktree_a_path = self.cli.worktrees_dir / f"pr-{pr_number}-branch-a"
        worktree_b_path = self.cli.worktrees_dir / f"pr-{pr_number}-branch-b"

        self.cli._info(f"Setting up resolution workspace for PR #{pr_number}...")

        if dry_run:
            return self._dry_run_setup(
                pr_number, source_branch, target_branch,
                resolution_branch, worktree_a_path, worktree_b_path
            )

        try:
            # Step 1: Create resolution branch (unless skipped)
            if no_resolution_branch:
                self.cli._info(f"📁 Using source branch directly: {source_branch}")
                result = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    cwd=self.cli.repo_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                original_branch = result.stdout.strip()
            else:
                self.cli._info(f"📁 Creating resolution branch: {resolution_branch}")
                subprocess.run(
                    ["git", "checkout", "-b", resolution_branch],
                    cwd=self.cli.repo_root,
                    check=True
                )
                original_branch = None

            # Step 2: Create worktrees with fallback support
            self.cli._info("🔧 Creating worktrees:")
            self.cli._info(f"   ├─ worktree-a: {source_branch} (analysis branch)")
            self.cli._info(f"   └─ worktree-b: {target_branch} (target branch)")

            try:
                # Try using workspace manager with fallback
                worktree_a_path = self.cli.workspace_manager.create_workspace(
                    f"pr-{pr_number}-branch-a", source_branch
                )
                worktree_b_path = self.cli.workspace_manager.create_workspace(
                    f"pr-{pr_number}-branch-b", target_branch
                )
            except Exception as e:
                self.cli._warn(f"Workspace manager failed: {e}")
                # Fallback to direct worktree creation
                subprocess.run(
                    ["git", "worktree", "add", str(worktree_a_path), source_branch],
                    cwd=self.cli.repo_root,
                    check=True
                )

                subprocess.run(
                    ["git", "worktree", "add", str(worktree_b_path), target_branch],
                    cwd=self.cli.repo_root,
                    check=True
                )

            # Step 3: Load constitutions and specifications
            self.cli._info("📋 Loading constitutions and specifications:")
            constitutions = constitution_files or self.cli.config.get(
                'constitutional_framework', {}
            ).get('default_constitutions', [])
            specifications = spec_files or []

            for constitution in constitutions:
                self.cli._info(f"   ├─ Constitution: {constitution}")
            for spec in specifications:
                self.cli._info(f"   └─ Specification: {spec}")

            # Step 4: Detect conflicts
            conflicts = self._detect_conflicts_interface_based(worktree_a_path, worktree_b_path)

            # Step 5: Create resolution metadata
            resolution_metadata = {
                'pr_number': pr_number,
                'source_branch': source_branch,
                'target_branch': target_branch,
                'resolution_branch': resolution_branch if not no_resolution_branch else source_branch,
                'worktree_a_path': str(worktree_a_path),
                'worktree_b_path': str(worktree_b_path),
                'constitution_files': constitution_files or [],
                'spec_files': spec_files or [],
                'conflicts': conflicts,
                'created_at': datetime.now().isoformat(),
                'status': 'ready_for_analysis',
                'push_to_target': push_to_target,
                'no_resolution_branch': no_resolution_branch,
                'original_branch': original_branch
            }

            metadata_file = self.cli.resolution_branches_dir / f"pr-{pr_number}-metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(resolution_metadata, f, indent=2)

            # Step 6: Generate setup summary
            setup_summary = {
                'success': True,
                'message': 'Resolution workspace ready!',
                'next_steps': [
                    f"1. eai analyze-constitutional --pr {pr_number}",
                    f"2. eai develop-spec-kit-strategy --pr {pr_number}",
                    f"3. eai align-content --pr {pr_number}"
                ],
                'metadata_file': str(metadata_file),
                'push_to_target': push_to_target
            }

            if push_to_target:
                setup_summary['next_steps'].append(
                    f"4. eai push-resolution --pr {pr_number} --target {target_branch}"
                )
                setup_summary['message'] = 'Resolution workspace ready! Use push-resolution to complete.'
            else:
                setup_summary['next_steps'].append(
                    f"4. Create PR or use push-resolution --pr {pr_number}"
                )

            self.cli._success("Resolution workspace ready!")
            return setup_summary

        except subprocess.CalledProcessError as e:
            self.cli._error_exit(f"Failed to setup resolution workspace: {e}")
        except Exception as e:
            self.cli._error_exit(f"Unexpected error during setup: {e}")
    
    def _dry_run_setup(
        self, pr_number: int, source_branch: str, target_branch: str,
        resolution_branch: str, worktree_a_path: Path, worktree_b_path: Path
    ) -> Dict[str, Any]:
        """Preview setup without actually creating worktrees"""
        self.cli._info("🔍 Preview resolution setup (dry run):")
        self.cli._info(f"📁 Would create resolution branch: {resolution_branch}")
        self.cli._info("🔧 Would create worktrees:")
        self.cli._info(f"   ├─ worktree-a: {source_branch} → {worktree_a_path}")
        self.cli._info(f"   └─ worktree-b: {target_branch} → {worktree_b_path}")

        return {
            'dry_run': True,
            'would_create_branch': resolution_branch,
            'would_create_worktrees': [str(worktree_a_path), str(worktree_b_path)],
            'message': 'Dry run completed - no changes made'
        }
    
    def push_resolution_to_target(
        self, pr_number: int, target_branch: str = None,
        confirmed: bool = False, force: bool = False
    ) -> Dict[str, Any]:
        """Push resolved changes directly to target branch."""
        if target_branch is None:
            target_branch = "main"

        self.cli._info(f"Pushing resolution for PR #{pr_number} to {target_branch}...")

        metadata_file = self.cli.resolution_branches_dir / f"pr-{pr_number}-metadata.json"
        if not metadata_file.exists():
            self.cli._error(f"No resolution metadata found for PR #{pr_number}")
            return {"success": False, "error": "No resolution metadata found"}

        with open(metadata_file) as f:
            metadata = json.load(f)

        resolution_branch = metadata.get("resolution_branch", f"pr-{pr_number}-resolution")
        source_branch = metadata.get("source_branch")

        result = subprocess.run(
            ["git", "rev-parse", "--verify", resolution_branch],
            cwd=self.cli.repo_root, capture_output=True
        )
        if result.returncode != 0:
            self.cli._error(f"Resolution branch '{resolution_branch}' not found")
            return {"success": False, "error": "Resolution branch not found"}

        if not confirmed:
            response = input(
                f"⚠️  Push resolution branch '{resolution_branch}' to {target_branch}? "
                f"(y/n): "
            )
            if response.lower() != 'y':
                self.cli._info("Push cancelled.")
                return {"success": False, "cancelled": True}

        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=self.cli.repo_root,
            capture_output=True,
            text=True,
            check=True
        )
        original_branch = result.stdout.strip()

        try:
            subprocess.run(
                ["git", "checkout", target_branch],
                cwd=self.cli.repo_root, check=True
            )

            merge_msg = f"Merge PR #{pr_number} resolution from {resolution_branch}"
            subprocess.run(
                ["git", "merge", "--no-ff", "-m", merge_msg, resolution_branch],
                cwd=self.cli.repo_root, check=True
            )

            push_cmd = ["git", "push", self.cli.remote, target_branch]
            if force:
                push_cmd.append("--force-with-lease")

            subprocess.run(push_cmd, cwd=self.cli.repo_root, check=True)

            subprocess.run(
                ["git", "branch", "-d", resolution_branch],
                cwd=self.cli.repo_root, check=True
            )

            self.cli._success(f"Successfully pushed resolution to {target_branch}")

            return {
                "success": True,
                "pr_number": pr_number,
                "target_branch": target_branch,
                "resolution_branch": resolution_branch,
                "source_branch": source_branch,
                "pushed": True
            }

        except subprocess.CalledProcessError as e:
            self.cli._error(f"Failed to push resolution: {e}")
            self.cli._warn("Rolling back changes...")
            try:
                subprocess.run(
                    ["git", "merge", "--abort"],
                    cwd=self.cli.repo_root,
                    capture_output=True
                )
                subprocess.run(
                    ["git", "checkout", original_branch],
                    cwd=self.cli.repo_root,
                    check=True
                )
                self.cli._info(f"Rolled back to branch: {original_branch}")
            except Exception as rollback_error:
                self.cli._error(f"Rollback failed: {rollback_error}")
            return {"success": False, "error": str(e)}
    
    def setup_resolution_direct(
        self,
        pr_number: int,
        source_branch: str,
        target_branch: str,
        constitution_files: List[str] = None,
        spec_files: List[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """Setup resolution workspace for direct branch push (no new branch).
        
        This method sets up resolution without creating a new resolution branch.
        Changes will be pushed directly to the target branch.
        
        Args:
            pr_number: Pull request number
            source_branch: Source branch with changes
            target_branch: Target branch to push to
            constitution_files: Optional list of constitution files
            spec_files: Optional list of specification files
            dry_run: If True, preview setup without creating worktrees
        
        Returns:
            Dictionary with setup results
        """
        self.cli._info(f"Setting up direct resolution for PR #{pr_number}...")
        self.cli._info(f"  Source: {source_branch} -> Target: {target_branch}")
        
        return self.setup_resolution(
            pr_number=pr_number,
            source_branch=source_branch,
            target_branch=target_branch,
            constitution_files=constitution_files,
            spec_files=spec_files,
            dry_run=dry_run,
            push_to_target=True,
            no_resolution_branch=True
        )
    
    def push_resolution(
        self,
        pr_number: int,
        confirmed: bool = False,
        branches: str = None,
        force: bool = False
    ) -> Dict[str, Any]:
        """Push resolved changes directly to target branch with --force-with-lease.
        
        This is the direct push method that pushes resolution changes
        directly to the target branch without creating a PR.
        
        Args:
            pr_number: Pull request number
            confirmed: Skip confirmation prompt if True
            branches: Target branch name (optional, uses metadata)
            force: Use --force-with-lease for safer force push
        
        Returns:
            Dictionary with push results
        """
        return self.push_resolution_to_target(
            pr_number=pr_number,
            target_branch=branches,
            confirmed=confirmed,
            force=force
        )
    
    def collect_pr_recommendations(
        self,
        pr_number: int,
        include_conflicts: bool = True,
        include_strategy: bool = True,
        include_validation: bool = True
    ) -> Dict[str, Any]:
        """Collect all recommendations for a PR.
        
        Args:
            pr_number: Pull request number
            include_conflicts: Include conflict-related recommendations
            include_strategy: Include strategy recommendations
            include_validation: Include validation recommendations
        
        Returns:
            Dictionary containing all recommendations
        """
        metadata_file = self.cli.resolution_branches_dir / f"pr-{pr_number}-metadata.json"
        
        if not metadata_file.exists():
            self.cli._error(f"No resolution metadata found for PR #{pr_number}")
            return {"success": False, "error": "No resolution metadata found"}
        
        with open(metadata_file) as f:
            metadata = json.load(f)
        
        recommendations = {
            "pr_number": pr_number,
            "collected_at": datetime.now().isoformat(),
            "recommendations": []
        }
        
        # Collect conflict recommendations
        if include_conflicts:
            conflicts = metadata.get("conflicts", [])
            if conflicts:
                recommendations["recommendations"].extend([
                    {
                        "category": "conflicts",
                        "type": "file_specific",
                        "file": conflict.get("file"),
                        "message": f"Resolve conflicts in {conflict.get('file')}",
                        "priority": "high" if conflict.get("severity") == "high" else "medium"
                    }
                    for conflict in conflicts
                ])
        
        # Collect strategy recommendations
        if include_strategy:
            strategy = metadata.get("strategy", {})
            if strategy:
                phases = strategy.get("phases", [])
                for phase in phases:
                    recommendations["recommendations"].append({
                        "category": "strategy",
                        "type": "phase",
                        "phase": phase.get("phase"),
                        "message": f"Execute phase {phase.get('phase')}: {phase.get('name')}",
                        "priority": "medium"
                    })
        
        # Collect validation recommendations
        if include_validation:
            validation = metadata.get("validation_results")
            if validation:
                checks = validation.get("validation_checks", [])
                failed_checks = [c for c in checks if c.get("status") == "failed"]
                if failed_checks:
                    recommendations["recommendations"].extend([
                        {
                            "category": "validation",
                            "type": "failed_check",
                            "check": check.get("check"),
                            "message": f"Fix failed validation: {check.get('check')}",
                            "priority": "high"
                        }
                        for check in failed_checks
                    ])
        
        # Add overall status recommendation
        status = metadata.get("status", "unknown")
        status_messages = {
            "ready_for_analysis": "Run constitutional analysis to begin resolution",
            "constitution_analyzed": "Develop a resolution strategy",
            "strategy_developed": "Execute content alignment",
            "content_aligned": "Validate the resolution",
            "validated": "Push resolution to target branch or create PR",
        }
        
        if status in status_messages:
            recommendations["recommendations"].append({
                "category": "workflow",
                "type": "next_step",
                "message": status_messages[status],
                "priority": "high"
            })
        
        recommendations["total_recommendations"] = len(recommendations["recommendations"])
        
        return recommendations
    
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
