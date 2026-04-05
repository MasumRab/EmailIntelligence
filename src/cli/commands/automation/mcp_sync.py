"""
MCP Sync Command Module

Synchronizes Model Context Protocol (MCP) configurations across different IDEs and tools.
Consolidates templates from the central mcp/ directory.
"""

import shutil
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict

from ..interface import Command


class MCPSyncCommand(Command):
    """
    Command for unifying MCP configurations across Claude, Cline, Cursor, and Roo.
    
    Ensures all AI agents have access to the same modular CLI tools by 
    syncing templates from mcp/ to their respective hidden directories.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "mcp-sync"

    @property
    def description(self) -> str:
        return "Synchronize MCP configurations across agents and IDEs"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--target", 
            choices=["claude", "cline", "cursor", "all"],
            default="all",
            help="Target agent to sync"
        )
        parser.add_argument(
            "--dry-run", 
            action="store_true", 
            help="Show what would be synced without making changes"
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
        """Execute the MCP sync command."""
        mcp_root = Path("mcp")
        targets = {
            "claude": (".claude/mcp.json", "claude.mcp.json"),
            "cline": (".cline/mcp.json", "cline.mcp.json"),
            "cursor": (".cursor/mcp.json", "cursor.mcp.json")
        }

        print("🔄 Starting MCP Configuration Sync...")

        try:
            selected = targets.keys() if args.target == "all" else [args.target]
            
            for agent in selected:
                dest_rel, template_name = targets[agent]
                template_path = mcp_root / template_name
                dest_path = Path(dest_rel)

                if not template_path.exists():
                    print(f"  - Warning: Template {template_name} not found. Skipping {agent}.")
                    continue

                print(f"  - Syncing {agent} -> {dest_path}")
                
                if args.dry_run:
                    print(f"    [DRY RUN] Would copy {template_name} to {dest_rel}")
                    continue

                # Ensure destination directory exists
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(template_path, dest_path)
                print("    ✅ Success")

            print("\n🚀 MCP synchronization complete.")
            return 0

        except Exception as e:
            print(f"Error during MCP sync: {e}")
            return 1
