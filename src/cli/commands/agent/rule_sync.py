"""
Rule Sync Command Module

Synchronizes repository-anchored rules from .agent/rules/ to active 
agent environments (e.g. .clinerules, .cursor/rules).
"""

import shutil
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict

from ..interface import Command


class RuleSyncCommand(Command):
    """
    Command for publishing repository-managed rules to AI agent environments.
    
    Ensures that the 'Source of Truth' in .agent/rules/ is correctly 
    mirrored to active agent configuration folders.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "rule-sync"

    @property
    def description(self) -> str:
        return "Publish repository rules from .agent/rules to active agent environments"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--target-dir", 
            help="Specific directory to publish rules to (e.g. .clinerules)"
        )
        parser.add_argument(
            "--verify", 
            action="store_true", 
            help="Verify consistency without making changes"
        )
        parser.add_argument(
            "--force", 
            action="store_true", 
            help="Overwrite existing files in target folders"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the rule synchronization."""
        source_dir = Path(".agent/rules")
        
        if not source_dir.exists():
            print(f"Error: Source rules directory '{source_dir}' not found.")
            return 1

        print(f"📜 Synchronizing Source of Truth rules from '{source_dir}'...")

        # Default targets if none specified
        target_dirs = [Path(".clinerules"), Path(".cursor/rules")]
        if args.target_dir:
            target_dirs = [Path(args.target_dir)]

        try:
            for dest_dir in target_dirs:
                print(f"\n--- Syncing target: {dest_dir} ---")
                
                if not args.verify:
                    dest_dir.mkdir(parents=True, exist_ok=True)

                for rule_file in source_dir.glob("*.md"):
                    # We maintain original names to minimize environment-specific hacks
                    dest_path = dest_dir / rule_file.name

                    if args.verify:
                        if not dest_path.exists():
                            print(f"  [MISSING] {rule_file.name}")
                        else:
                            print(f"  [OK] {rule_file.name}")
                        continue

                    if dest_path.exists() and not args.force:
                        print(f"  - Skipping {rule_file.name} (exists). Use --force to overwrite.")
                        continue

                    # Copy with metadata preservation
                    shutil.copy2(rule_file, dest_path)
                    print(f"  - Published {rule_file.name}")

            return 0
        except Exception as e:
            print(f"Error during rule sync: {e}")
            return 1
