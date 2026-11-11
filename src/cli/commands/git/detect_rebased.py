"""
Detect Rebased Command Module

Implements the detect-rebased command for identifying rebased branches.
"""

from argparse import Namespace
from typing import Any, Dict

from ..interface import Command


class DetectRebasedCommand(Command):
    """
    Command for detecting branches that have been rebased.

    This command wraps the RebaseDetector service to identify local branches
    that may have been rebased and require verification.
    """

    def __init__(self):
        self._git_wrapper = None

    @property
    def name(self) -> str:
        return "detect-rebased"

    @property
    def description(self) -> str:
        return "Detect branches that have been rebased"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        parser.add_argument(
            "--since",
            type=str,
            help="Only show branches rebased since a certain date (e.g., '2 weeks ago')",
        )
        parser.add_argument("--json", action="store_true", help="Output in JSON format")
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
        """Execute the detect-rebased command."""
        try:
            from src.lib.git_wrapper import GitWrapper
            from src.services.rebase_detector import RebaseDetector

            git_wrapper = self._git_wrapper or GitWrapper()
            detector = RebaseDetector(git_wrapper)

            rebased_branches = detector.identify_rebased_branches()

            if args.json:
                import json

                print(
                    json.dumps(
                        {
                            "rebased_branches": rebased_branches,
                            "count": len(rebased_branches),
                        },
                        indent=2,
                    )
                )
            else:
                print(f"\n=== Detected Rebased Branches ===")
                if rebased_branches:
                    for branch in rebased_branches:
                        print(f"  - {branch}")
                    print(f"\nTotal: {len(rebased_branches)} branches")
                else:
                    print("No rebased branches detected.")
                print("=" * 42)

            return 0

        except ImportError as e:
            print(f"Error: Required module not available: {e}")
            print("Install gitpython: pip install gitpython")
            return 1
        except Exception as e:
            print(f"Error during detection: {e}")
            return 1
