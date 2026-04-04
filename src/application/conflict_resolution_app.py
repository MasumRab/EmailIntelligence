"""
Main application logic for EmailIntelligence conflict resolution
Separated from CLI to follow Single Responsibility Principle
"""
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.config import ConfigurationManager
from src.core.security import SecurityValidator
from src.core.git_operations import GitOperations


class ConflictResolutionApp:
    """Main application class for conflict resolution logic"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.worktrees_dir = self.repo_root / ".git" / "worktrees"
        self.resolution_branches_dir = self.repo_root / "resolution-workspace"
        self.constitutions_dir = self.repo_root / ".emailintelligence" / "constitutions"
        self.strategies_dir = self.repo_root / ".emailintelligence" / "strategies"

        # Initialize modular components
        self.config_manager = ConfigurationManager(self.repo_root)
        self.security_validator = SecurityValidator(self.repo_root)
        self.git_operations = GitOperations(self.repo_root)

        # Create necessary directories
        self._ensure_directories()

        # Load configuration from config manager
        self.config = self.config_manager.config

    def _ensure_directories(self):
        """Create necessary directories for the tool"""
        directories = [
            self.worktrees_dir,
            self.resolution_branches_dir,
            self.constitutions_dir,
            self.strategies_dir
        ]

        for directory in directories:
            # Validate directory path to prevent directory traversal
            if not self.security_validator.is_safe_path(directory):
                raise ValueError(f"Unsafe directory path detected: {directory}")
            directory.mkdir(parents=True, exist_ok=True)

    def setup_resolution(
        self, pr_number: int, source_branch: str, target_branch: str,
        constitution_files: List[str] = None, spec_files: List[str] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Setup resolution workspace for a specific PR

        Args:
            pr_number: Pull request number
            source_branch: Source branch with conflicts
            target_branch: Target branch for merging
            constitution_files: List of constitution YAML files
            spec_files: List of specification files
            dry_run: Preview setup without creating worktrees
        """
        # Validate inputs to prevent injection attacks
        if not self.security_validator.is_valid_pr_number(pr_number):
            raise ValueError(f"Invalid PR number: {pr_number}")
        
        if not self.security_validator.is_valid_git_reference(source_branch):
            raise ValueError(f"Invalid source branch name: {source_branch}")
        
        if not self.security_validator.is_valid_git_reference(target_branch):
            raise ValueError(f"Invalid target branch name: {target_branch}")

        resolution_branch = f"pr-{pr_number}-resolution"
        worktree_a_path = self.worktrees_dir / f"pr-{pr_number}-branch-a"
        worktree_b_path = self.worktrees_dir / f"pr-{pr_number}-branch-b"

        # Validate paths to prevent directory traversal
        if not self.security_validator.is_safe_path(worktree_a_path) or not self.security_validator.is_safe_path(worktree_b_path):
            raise ValueError("Unsafe worktree paths detected")

        if dry_run:
            return self._dry_run_setup(
                pr_number, source_branch, target_branch,
                resolution_branch, worktree_a_path, worktree_b_path
            )

        try:
            # Step 1: Create resolution branch
            if not self.git_operations.create_branch(resolution_branch):
                raise RuntimeError(f"Failed to create resolution branch: {resolution_branch}")

            # Step 2: Create worktrees
            # Create worktree for source branch
            if not self.git_operations.create_worktree(worktree_a_path, source_branch):
                raise RuntimeError(f"Failed to create worktree for source branch: {source_branch}")

            # Create worktree for target branch
            if not self.git_operations.create_worktree(worktree_b_path, target_branch):
                raise RuntimeError(f"Failed to create worktree for target branch: {target_branch}")

            # Step 3: Load constitutions and specifications
            constitutions = constitution_files or self.config.get(
                'constitutional_framework', {}
            ).get('default_constitutions', [])
            specifications = spec_files or []

            # Step 4: Create resolution metadata
            resolution_metadata = {
                'pr_number': pr_number,
                'source_branch': source_branch,
                'target_branch': target_branch,
                'resolution_branch': resolution_branch,
                'worktree_a_path': str(worktree_a_path),
                'worktree_b_path': str(worktree_b_path),
                'constitution_files': constitution_files or [],
                'spec_files': spec_files or [],
                'created_at': datetime.now().isoformat(),
                'status': 'ready_for_analysis'
            }

            metadata_file = self.resolution_branches_dir / f"pr-{pr_number}-metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(resolution_metadata, f, indent=2)

            # Step 5: Generate setup summary
            setup_summary = {
                'success': True,
                'message': 'Resolution workspace ready!',
                'next_steps': [
                    f"1. eai analyze-constitutional --pr {pr_number}",
                    f"2. eai develop-spec-kit-strategy --pr {pr_number}",
                    f"3. eai align-content --pr {pr_number}"
                ],
                'metadata_file': str(metadata_file)
            }

            return setup_summary

        except Exception as e:
            raise RuntimeError(f"Failed to setup resolution workspace: {e}")

    def _dry_run_setup(
        self, pr_number: int, source_branch: str, target_branch: str,
        resolution_branch: str, worktree_a_path: Path, worktree_b_path: Path
    ) -> Dict[str, Any]:
        """Preview setup without actually creating worktrees"""
        return {
            'dry_run': True,
            'would_create_branch': resolution_branch,
            'would_create_worktrees': [str(worktree_a_path), str(worktree_b_path)],
            'message': 'Dry run completed - no changes made'
        }