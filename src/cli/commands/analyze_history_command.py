"""
Analyze History Command Module

Implements the analyze-history command for git history analysis.
"""

from argparse import Namespace
from typing import Any, Dict

from .interface import Command


class AnalyzeHistoryCommand(Command):
    """
    Command for analyzing git commit history and patterns.

    This command retrieves commits from git log, classifies them by type
    and risk level, and generates analysis reports.
    """

    @property
    def name(self) -> str:
        return "analyze-history"

    @property
    def description(self) -> str:
        return "Analyze git commit history and patterns"

    def add_arguments(self, parser: Any) -> None:
        """
        Add command-specific arguments.

        Args:
            parser: ArgumentParser subparser for this command
        """
        parser.add_argument(
            "--branch", default="HEAD", help="Branch to analyze (default: HEAD)"
        )
        parser.add_argument("--output", help="Output file for report")

    def get_dependencies(self) -> Dict[str, Any]:
        """
        Get required dependencies for this command.

        Returns:
            Dict mapping dependency names to types
        """
        return {
            "history": "GitHistory",
            "classifier": "CommitClassifier",
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """
        Set command dependencies.

        Args:
            dependencies: Dict of dependency instances
        """
        self._history = dependencies.get("history")
        self._classifier = dependencies.get("classifier")

    async def execute(self, args: Namespace) -> int:
        """
        Execute the analyze-history command.

        Args:
            args: Parsed command-line arguments

        Returns:
            int: Exit code (0 for success, 1 for error)
        """
        try:
            branch = args.branch or "HEAD"
            print(f"Analyzing history for branch: {branch}...")

            # Get commits from git history
            commits = await self._history.get_commits(branch, limit=500)

            if not commits:
                print("No commits found.")
                return 0

            # Analyze commits using classifier
            stats = self._classifier.analyze_history(commits)

            # Build report
            report_lines = [
                f"Analysis Report for {branch}",
                f"Total Commits: {stats.get('total', 0)}",
                "",
                "By Category:",
            ]

            # Add category breakdown
            by_category = stats.get("by_category", {})
            for cat, count in by_category.items():
                report_lines.append(f"  - {cat}: {count}")

            report_lines.extend(["", "By Risk:"])

            # Add risk breakdown
            by_risk = stats.get("by_risk", {})
            for risk, count in by_risk.items():
                report_lines.append(f"  - {risk}: {count}")

            report = "\n".join(report_lines)

            # Print report
            print(f"\n{report}")

            # Write to output file if specified
            if args.output:
                try:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(report)
                    print(f"\nReport saved to {args.output}")
                except Exception as e:
                    print(f"Error writing to output file: {e}")
                    return 1

            return 0

        except Exception as e:
            print(f"Error during history analysis: {e}")
            return 1
