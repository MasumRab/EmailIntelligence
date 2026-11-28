"""
Stash Resolve Command Module

Implements systematic resolution of Git stashes by applying them to their original branches.
Ported from orchestration-tools:scripts/handle_stashes.sh.
"""

import re
import subprocess
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..interface import Command


class StashResolveCommand(Command):
    """
    Command for identifying and applying stashes to their corresponding branches.
    
    Parses stash messages to determine the original branch and automates
    the checkout-apply-pop cycle for systematic stash cleanup.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "stash-resolve"

    @property
    def description(self) -> str:
        return "Systematically apply stashes to their corresponding branches"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--dry-run", 
            action="store_true", 
            help="Show what would be done without applying stashes"
        )
        parser.add_argument(
            "--all", 
            action="store_true", 
            help="Process all stashes in the stack"
        )
        parser.add_argument(
            "--index", 
            type=int, 
            help="Process only a specific stash index (e.g. 0 for stash@{0})"
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
        """Execute the stash resolve command."""
        print("🔍 Scanning Git stash stack...")
        
        try:
            stashes = self._get_stashes()
            if not stashes:
                print("No stashes found.")
                return 0

            if args.index is not None:
                if args.index >= len(stashes):
                    print(f"Error: Stash index {args.index} out of range (max {len(stashes)-1})")
                    return 1
                target_stashes = [stashes[args.index]]
            elif args.all:
                target_stashes = stashes
            else:
                # Default to top stash if nothing specified
                target_stashes = [stashes[0]]

            print(f"Found {len(stashes)} stashes. Processing {len(target_stashes)} target(s)...")

            for stash in target_stashes:
                idx, msg = stash
                branch = self._extract_branch(msg)
                print(f"\n📦 stash@{{{idx}}}: {msg}")
                print(f"   -> Identified target branch: {branch}")

                if args.dry_run:
                    print("   [DRY RUN] Would attempt to apply to branch")
                    continue

                # Execute resolution
                success = await self._apply_stash_to_branch(idx, branch)
                if not success:
                    print(f"   ❌ Failed to process stash@{{{idx}}}")
                else:
                    print(f"   ✅ Successfully processed stash@{{{idx}}}")

            return 0
        except Exception as e:
            print(f"Error during stash resolution: {e}")
            return 1

    def _get_stashes(self) -> List[Tuple[int, str]]:
        """Retrieve list of stashes from git."""
        result = subprocess.run(
            ["git", "stash", "list"],
            capture_output=True, text=True, check=True
        )
        stashes = []
        for line in result.stdout.strip().split("\n"):
            if not line: continue
            match = re.match(r'stash@\{(\d+)\}: (.*)', line)
            if match:
                stashes.append((int(match.group(1)), match.group(2)))
        return stashes

    def _extract_branch(self, message: str) -> str:
        """Extract branch name from stash message."""
        # Pattern: WIP on [branch]: ... or On [branch]: ...
        match = re.search(r'(?:WIP on|On) ([^:\s]+):', message)
        if match:
            return match.group(1)
        return "unknown"

    async def _apply_stash_to_branch(self, index: int, branch: str) -> bool:
        """Checkout branch and apply stash."""
        if branch == "unknown":
            print("   ⚠️  Warning: Could not determine branch. Staying on current.")
        else:
            # Check if branch exists locally
            exists = subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
                check=False
            ).returncode == 0
            
            if not exists:
                print(f"   ⚠️  Branch '{branch}' does not exist locally.")
                return False

            print(f"   🔄 Switching to branch: {branch}")
            subprocess.run(["git", "checkout", branch], check=True, capture_output=True)

        print(f"   🩹 Applying stash@{{{index}}}...")
        result = subprocess.run(
            ["git", "stash", "apply", f"stash@{{{index}}}"],
            capture_output=True, text=True, check=False
        )
        
        return result.returncode == 0
