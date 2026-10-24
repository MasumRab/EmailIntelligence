import argparse
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

    async def execute(self, args: Namespace) -> int:
        """
        Execute the command.
        """
        try:
            result = subprocess.run(
                ["git", "branch", "--list"],
                capture_output=True,
                text=True,
                check=True,
            )
            branches = []
            for line in result.stdout.strip().split("\n"):
                branch_name = line.replace("*", "").strip()
                if not branch_name:
                    continue
                category = "feature"
                if branch_name.startswith("hotfix"):
                    category = "hotfix"
                elif branch_name.startswith("maint") or branch_name.startswith("fix"):
                    category = "maintenance"
                elif branch_name.startswith("feature"):
                    category = "feature"
                elif branch_name == "main" or branch_name == "master":
                    category = "primary"
                else:
                    category = "feature" # Default based on issue context

                branches.append({
                    "name": branch_name,
                    "category": category
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
