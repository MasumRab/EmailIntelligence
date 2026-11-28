import argparse
import asyncio
import subprocess
from argparse import Namespace
from typing import Any, Dict

from .interface import Command


class IdentifyCommand(Command):
    """
    Command to identify and categorize local branches.
    """

    @property
    def name(self) -> str:
        return "identify-branches"

    @property
    def description(self) -> str:
        return "List local branches and categorize them as feature, maintenance, or hotfix"

    def add_arguments(self, parser: Any) -> None:
        """
        Add command-specific arguments.
        """
        parser.add_argument(
            "--json",
            action="store_true",
            help="Output in JSON format",
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """
        Get required dependencies for this command.
        """
        return {}

    @staticmethod
    def _categorise(branch_name: str) -> str:
        """Map a branch name to its category."""
        if branch_name.startswith("hotfix"):
            return "hotfix"
        if branch_name.startswith(("maint", "fix")):
            return "maintenance"
        if branch_name.startswith("feature"):
            return "feature"
        if branch_name in ("main", "master"):
            return "primary"
        return "feature"

    async def execute(self, args: Namespace) -> int:
        """
        Execute the command.
        """
        try:
            proc = await asyncio.create_subprocess_exec(
                "git", "branch", "--list",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(
                    proc.returncode, "git branch --list", stderr=stderr
                )
            branches = []
            for line in stdout.decode().strip().split("\n"):
                branch_name = line.replace("*", "").strip()
                if not branch_name:
                    continue
                branches.append({
                    "name": branch_name,
                    "category": self._categorise(branch_name),
                })

            if getattr(args, "json", False):
                import json
                print(json.dumps(branches, indent=2))
            else:
                for b in branches:
                    print(f"{b['name']} [{b['category']}]")

            return 0
        except subprocess.CalledProcessError as e:
            print(f"Error listing branches: {e}")
            return 1
