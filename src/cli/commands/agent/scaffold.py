"""
Agent Scaffold Command Module

Installs and updates repository-specific agent tools with explicit 
differentiation from global ecosystem/MCP prompts.
"""

import os
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict

from ..interface import Command


class AgentScaffoldCommand(Command):
    """
    Command for installing repository-specific agent tools.
    
    Creates symlinks from the repo's .agent/ directory to ~/.gemini/
    with a 'repo-' prefix to differentiate from global/MCP skills.
    """

    PROJECT_PREFIX = "repo-"

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "agent-scaffold"

    @property
    def description(self) -> str:
        return "Sync project-specific agent tools to ~/.gemini (with prefixing)"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument(
            "--force", 
            action="store_true", 
            help="Overwrite existing global links"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        return {"security_validator": "SecurityValidator"}

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        repo_agent_dir = Path(".agent")
        gemini_root = Path("~/.gemini").expanduser()
        
        if not repo_agent_dir.exists():
            print(f"Error: Repository agent directory '{repo_agent_dir}' not found.")
            return 1

        print(f"🚀 Scaffolding Project-Specific Agent Tools (Prefix: '{self.PROJECT_PREFIX}')...")

        subdirs = ["skills", "recipes", "personalities"]
        for subdir in subdirs:
            source_path = repo_agent_dir / subdir
            dest_path = gemini_root / subdir
            
            if not source_path.exists():
                continue
                
            print(f"\n--- Syncing {subdir} ---")
            dest_path.mkdir(parents=True, exist_ok=True)

            for item in source_path.glob("*"):
                # Apply project prefix to prevent collisions with global skills
                prefixed_name = f"{self.PROJECT_PREFIX}{item.name}"
                link_path = dest_path / prefixed_name

                if link_path.exists() or link_path.is_symlink():
                    if args.force:
                        link_path.unlink()
                    else:
                        print(f"  - Skipping {item.name} (exists as {prefixed_name})")
                        continue

                try:
                    os.symlink(item.absolute(), link_path)
                    print(f"  - Linked {item.name} -> {prefixed_name}")
                except Exception as e:
                    print(f"  - Error linking {item.name}: {e}")

        print("\n✅ Differentiation complete. Project tools are prefixed with 'repo-'.")
        return 0
