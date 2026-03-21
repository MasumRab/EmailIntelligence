"""
Rule Sync Command Module

Synchronizes repository-anchored rules from agent/rules/ to IDE-specific 
hidden directories like .cursor/rules/ or .cline/.
"""

import os
import shutil
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List

from ..interface import Command


class RuleSyncCommand(Command):
    """
    Command for publishing repository-managed rules to AI agent environments.
    
    Ensures that the 'Source of Truth' in agent/rules/ is correctly 
    mirrored to .cursor/rules/, .cline/, and other IDE hidden folders.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "rule-sync"

    @property
    def description(self) -> str:
        return "Publish repository rules to IDE-specific agent folders"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--target", 
            choices=["cursor", "cline", "all"],
            default="all",
            help="Target IDE/Agent environment"
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
        source_dir = Path("agent/rules")
        
        if not source_dir.exists():
            print(f"Error: Source rules directory '{source_dir}' not found.")
            return 1

        print(f"📜 Synchronizing Source of Truth rules from '{source_dir}'...")

        targets = {
            "cursor": Path(".cursor/rules"),
            "cline": Path(".clinerules")
        }

        try:
            selected = targets.keys() if args.target == "all" else [args.target]
            
            for key in selected:
                dest_dir = targets[key]
                print(f"\n--- Syncing target: {key} ({dest_dir}) ---")
                
                if not args.verify:
                    dest_dir.mkdir(parents=True, exist_ok=True)

                for rule_file in source_dir.glob("*.md"):
                    # For Cursor, we rename .md to .mdc
                    dest_name = rule_file.name if key != "cursor" else rule_file.stem + ".mdc"
                    dest_path = dest_dir / dest_name

                    if args.verify:
                        if not dest_path.exists():
                            print(f"  [MISSING] {dest_name}")
                        else:
                            print(f"  [OK] {dest_name}")
                        continue

                    if dest_path.exists() and not args.force:
                        print(f"  - Skipping {dest_name} (exists). Use --force to overwrite.")
                        continue

                    # Copy with metadata preservation
                    shutil.copy2(rule_file, dest_path)
                    print(f"  - Published {rule_file.name} -> {dest_name}")

            return 0
        except Exception as e:
            print(f"Error during rule sync: {e}")
            return 1
