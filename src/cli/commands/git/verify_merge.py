"""
Verify Merge Command Module

Implements the verify-merge command for verifying merged branches against IntentReports.
"""

from argparse import Namespace
from typing import Any, Dict

from ..interface import Command


class VerifyMergeCommand(Command):
    """
    Command for verifying a merged branch against an IntentReport.

    This command wraps the MergeVerifier service to ensure that the actual
    changes made in a rebased branch, once merged, reflect the original intentions.
    """

    def __init__(self):
        self._git_wrapper = None

    @property
    def name(self) -> str:
        return "verify-merge"

    @property
    def description(self) -> str:
        return "Verify a merged branch against an IntentReport"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "merged_branch", help="Name of the branch that was merged (e.g., 'main')"
        )
        parser.add_argument(
            "--report", type=str, help="Path to the IntentReport JSON file"
        )
        parser.add_argument(
            "--source-branch", type=str, help="The feature branch that was merged"
        )
        parser.add_argument(
            "--verbose", action="store_true", help="Enable verbose output"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Return required dependencies."""
        return {}

    def set_dependencies(self, deps: Dict[str, Any]) -> None:
        """Set dependencies for the command."""
        if "git_wrapper" in deps:
            self._git_wrapper = deps["git_wrapper"]

    async def execute(self, args: Namespace) -> int:
        """Execute the verify-merge command."""
        try:
            from src.lib.git_wrapper import GitWrapper
            from src.services.merge_verifier import MergeVerifier

            git_wrapper = self._git_wrapper or GitWrapper()
            verifier = MergeVerifier(git_wrapper)

            result = verifier.verify(args.merged_branch)

            print(f"\n=== Merge Verification Result ===")
            print(f"Branch: {args.merged_branch}")
            if args.source_branch:
                print(f"Source: {args.source_branch}")
            if args.report:
                print(f"Report: {args.report}")
            print(f"\nResult: {result}")
            print("=" * 40)

            return 0

        except ImportError as e:
            print(f"Error: Required module not available: {e}")
            print("Install gitpython: pip install gitpython")
            return 1
        except Exception as e:
            print(f"Error during verification: {e}")
            return 1
