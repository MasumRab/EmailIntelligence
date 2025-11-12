"""
TODO: Refactor and integrate this module's functionality into `src/cli/main.py`.

This module provides an `identify-rebased-branches` command that uses `RebaseDetector`.
To adhere to SOLID principles, specifically the Single Responsibility Principle (SRP)
and Open/Closed Principle (OCP), consider the following:

1.  **Extract Core Logic:** The core rebase detection logic within `RebaseDetector` should be
    reused or integrated into the `AnalysisService` in `src/services/analysis_service.py`.
    This ensures that rebase detection logic resides in a single, well-defined service.
2.  **CLI Command Integration:** The `identify_rebased_branches_command` and `add_identify_parser`
    functions should be refactored to become part of the `src/cli/main.py`'s sub-command structure.
    This centralizes CLI entry points and argument parsing.
3.  **Dependency Inversion:** Ensure that the `identify_rebased_branches_command` depends on
    abstractions (e.g., an `AnalysisService` interface) rather than concrete implementations,
    allowing for easier testing and swapping of detection backends.
4.  **Modularity:** If `RebaseDetector` offers distinct functionality not covered by
    `AnalysisService`, refactor it as a separate, reusable component that `AnalysisService`
    or `src/cli/main.py` can compose.
"""
from ..services.rebase_detector import RebaseDetector
from ..lib.git_wrapper import GitWrapper

def identify_rebased_branches_command(args):
    """
    Handles the identify-rebased-branches command.
    """
    try:
        git_wrapper = GitWrapper()
        rebase_detector = RebaseDetector(git_wrapper)
        rebased_branches = rebase_detector.identify_rebased_branches()
        print("Rebased branches:")
        for branch in rebased_branches:
            print(f"- {branch}")
    except Exception as e:
        print(f"An error occurred during branch identification: {e}")

def add_identify_parser(subparsers):
    """
    Adds the parser for the identify-rebased-branches command.
    """
    identify_parser = subparsers.add_parser(
        "identify-rebased-branches",
        help="Identify branches that have recently undergone a rebase operation."
    )
    identify_parser.set_defaults(func=identify_rebased_branches_command)