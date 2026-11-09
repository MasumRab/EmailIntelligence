"""
PR Extract Command Module

Implements isolation of orchestration-specific changes from a feature branch.
Ported from feat-v2.0-pr:scripts/extract-orchestration-changes.sh.
"""

import subprocess
from argparse import Namespace
from typing import Any, Dict, List

from ..interface import Command


class OrchExtractCommand(Command):
    """
    Command for extracting orchestration-managed file changes into a dedicated branch.
    
    Identifies changes to setup, deployment, and configuration files,
    allowing them to be reviewed and merged separately to orchestration-tools.
    """

    ORCH_PATTERNS = [
        "setup/", "deployment/", "scripts/shell/", "scripts/sh/",
        "pyproject.toml", "requirements.txt", "uv.lock",
        "tsconfig.json", ".gitignore", ".gitattributes",
        "conductor/", ".taskmaster/"
    ]

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "orch-extract"

    @property
    def description(self) -> str:
        return "Isolate and extract orchestration/config changes into a dedicated branch"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument("source", help="Source branch to extract from")
        parser.add_argument("--base", default="main", help="Base branch for comparison")
        parser.add_argument("--target", help="Custom name for the new branch")
        parser.add_argument("--dry-run", action="store_true", help="Show files that would be extracted")

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the PR extraction command."""
        source = args.source
        base = args.base
        
        print(f"🔍 Analyzing changes in '{source}' relative to '{base}'...")

        try:
            # 1. Get changed files
            changed_files = self._get_changed_files(base, source)
            if not changed_files:
                print("No changes found between branches.")
                return 0

            # 2. Filter for orchestration files
            orch_files = [f for f in changed_files if any(p in f for p in self.ORCH_PATTERNS)]
            
            if not orch_files:
                print("No orchestration-related changes detected.")
                return 0

            print(f"Found {len(orch_files)} orchestration-managed files:")
            for f in orch_files:
                print(f"  - {f}")

            if args.dry_run:
                print("\n[DRY RUN] Skipping branch creation.")
                return 0

            # 3. Create extraction branch
            target_branch = args.target or f"orch-extract-{source.replace('/', '-')}"
            print(f"\n🚀 Creating extraction branch: {target_branch}")
            
            self._create_extraction_branch(base, source, target_branch, orch_files)
            
            print(f"✅ Successfully extracted changes to {target_branch}")
            return 0

        except Exception as e:
            print(f"Error during PR extraction: {e}")
            return 1

    def _get_changed_files(self, base: str, source: str) -> List[str]:
        """Get list of files changed between refs."""
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...{source}"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split("\n")

    def _create_extraction_branch(self, base: str, source: str, target: str, files: List[str]) -> None:
        """Create a new branch and cherry-pick specific file changes."""
        # Checkout new branch from base
        subprocess.run(["git", "checkout", "-b", target, base], check=True, capture_output=True)
        
        # Checkout files from source branch
        for file_path in files:
            subprocess.run(["git", "checkout", source, "--", file_path], check=True, capture_output=True)
        
        # Commit the changes
        subprocess.run(["git", "add"] + files, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"chore: extract orchestration changes from {source}"],
            check=True, capture_output=True
        )
