"""
Agent Scaffold Command Module

Synchronizes repository-specific skills, recipes, and personalities 
with the global Gemini CLI configuration (~/.gemini).
"""

import os
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict

from ..interface import Command


class AgentScaffoldCommand(Command):
    """
    Command for installing and updating repository-specific agent tools.
    
    Creates symlinks from the repo's .agent/ directory to ~/.gemini/
    to ensure the agent has the correct skills and recipes for this project.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "agent-scaffold"

    @property
    def description(self) -> str:
        return "Sync project-specific agent skills and recipes to ~/.gemini"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--force", 
            action="store_true", 
            help="Overwrite existing symlinks or files"
        )
        parser.add_argument(
            "--dry-run", 
            action="store_true", 
            help="Show what would be linked without making changes"
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
        """Execute the agent-scaffold command."""
        repo_agent_dir = Path(".agent")
        gemini_root = Path("~/.gemini").expanduser()
        
        if not repo_agent_dir.exists():
            print(f"Error: Repository agent directory '{repo_agent_dir}' not found.")
            return 1

        print("🚀 Scaffolding Project-Specific Agent Tools...")

        # 1. Sync Skills
        self._sync_category(
            repo_agent_dir / "skills", 
            gemini_root / "skills", 
            args.force, 
            args.dry_run
        )

        # 2. Sync Recipes (Commands)
        self._sync_category(
            repo_agent_dir / "recipes", 
            gemini_root / "commands", 
            args.force, 
            args.dry_run
        )

        # 3. Sync Personalities
        self._sync_category(
            repo_agent_dir / "personalities", 
            gemini_root / "personalities", 
            args.force, 
            args.dry_run
        )
        
        print("\n✅ Scaffolding complete. Run 'gemini --memory show' to verify loaded context.")
        return 0

    def _sync_category(self, source_dir: Path, target_dir: Path, force: bool, dry_run: bool):
        """Sync a category of tools using symlinks."""
        if not source_dir.exists():
            return

        print(f"\n--- Syncing {source_dir.name} ---")
        
        for item in source_dir.iterdir():
            if item.is_dir() or item.suffix in [".md", ".toml"]:
                dest_path = target_dir / item.name
                
                if dry_run:
                    print(f"  [DRY RUN] Would link {item} -> {dest_path}")
                    continue

                try:
                    # Create target parent dir if it doesn't exist
                    target_dir.mkdir(parents=True, exist_ok=True)

                    if dest_path.exists() or dest_path.is_symlink():
                        if force:
                            if dest_path.is_dir() and not dest_path.is_symlink():
                                import shutil
                                shutil.rmtree(dest_path)
                            else:
                                dest_path.unlink()
                        else:
                            print(f"  - Skipping {item.name} (already exists). Use --force to update.")
                            continue

                    os.symlink(item.absolute(), dest_path)
                    print(f"  - Linked {item.name}")
                except Exception as e:
                    print(f"  - Error linking {item.name}: {e}")
