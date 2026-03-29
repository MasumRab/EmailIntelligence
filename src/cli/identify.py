"""
Module for the `identify-rebased-branches` CLI command.

TODO: Refactor this module to integrate its functionality into `src/cli/main.py`
and consolidate its core rebase detection logic.

To adhere to SOLID principles, specifically the Single Responsibility Principle (SRP)
and Open/Closed Principle (OCP), the following steps are required:

1.  **Consolidate Core Logic:** The core rebase detection logic, currently within
    `RebaseDetector`, should be integrated into or reused by the `AnalysisService`
    in `src/services/analysis_service.py`. This ensures a single, well-defined
    service for analysis and detection.
2.  **CLI Command Integration:** Refactor `identify_rebased_branches_command` and
    `add_identify_parser` to become part of `src/cli/main.py`'s sub-command structure,
    centralizing CLI entry points and argument parsing.
3.  **Dependency Inversion:** Ensure `identify_rebased_branches_command` depends on
    abstractions (e.g., an `AnalysisService` interface) rather than concrete
    implementations, allowing for easier testing and swapping of detection backends.
4.  **Modularity:** If `RebaseDetector` provides distinct functionality not fully
    covered by `AnalysisService`, refactor it as a separate, reusable component
    that `AnalysisService` or `src/cli/main.py` can compose.
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