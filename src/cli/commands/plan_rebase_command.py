"""
Plan Rebase Command Module

Implements the plan-rebase command for generating rebase plans.
"""

from argparse import Namespace
from typing import Any, Dict

from .interface import Command


class PlanRebaseCommand(Command):
    """
    Command for generating optimal rebase plans for branches.

    This command analyzes commit history and generates a structured
    rebase plan that organizes commits by priority and risk.
    """

    @property
    def name(self) -> str:
        return "plan-rebase"

    @property
    def description(self) -> str:
        return "Generate optimal rebase plan for a branch"

    def add_arguments(self, parser: Any) -> None:
        """
        Add command-specific arguments.

        Args:
            parser: ArgumentParser subparser for this command
        """
        parser.add_argument(
            "--branch", default="HEAD", help="Branch to plan rebase for (default: HEAD)"
        )
        parser.add_argument(
            "--output", required=True, help="Output file for rebase plan"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """
        Get required dependencies for this command.

        Returns:
            Dict mapping dependency names to types
        """
        return {
            "history": "GitHistory",
            "classifier": "CommitClassifier",
            "planner": "RebasePlanner",
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """
        Set command dependencies.

        Args:
            dependencies: Dict of dependency instances
        """
        self._history = dependencies.get("history")
        self._classifier = dependencies.get("classifier")
        self._planner = dependencies.get("planner")

    async def execute(self, args: Namespace) -> int:
        """
        Execute the plan-rebase command.

        Args:
            args: Parsed command-line arguments

        Returns:
            int: Exit code (0 for success, 1 for error)
        """
        try:
            branch = args.branch or "HEAD"
            output_file = args.output

            print(f"Planning rebase for branch: {branch}...")

            # Get commits from git history
            commits = await self._history.get_commits(branch, limit=500)

            if not commits:
                print("No commits found.")
                return 0

            # Classify each commit
            for commit in commits:
                self._classifier.classify(commit)

            # Generate rebase plan
            plan = self._planner.generate_plan(commits)

            # Write plan to output file
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(plan)
            except Exception as e:
                print(f"Error writing to output file: {e}")
                return 1

            print(f"Rebase plan saved to {output_file}")
            print(f"Plan contains {len(commits)} commits organized into phases")

            return 0

        except Exception as e:
            print(f"Error during rebase planning: {e}")
            return 1
