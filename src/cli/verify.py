"""
Module for the `verify` CLI command.

TODO: Refactor this module to integrate its functionality into `src/cli/main.py`
and consolidate its core verification logic.

To adhere to SOLID principles, specifically the Single Responsibility Principle (SRP)
and Open/Closed Principle (OCP), the following steps are required:

1.  **Consolidate Core Logic:** The core verification logic, currently within
    `MergeVerifier`, should be integrated into or reused by the `AnalysisService`
    in `src/services/analysis_service.py`. This ensures a single, well-defined
    service for analysis and verification.
2.  **CLI Command Integration:** Refactor `verify_command` and `add_verify_parser`
    to become part of `src/cli/main.py`'s sub-command structure, centralizing
    CLI entry points and argument parsing.
3.  **Dependency Inversion:** Ensure `verify_command` depends on abstractions
    (e.g., an `AnalysisService` interface) rather than concrete implementations,
    allowing for easier testing and swapping of verification backends.
4.  **Modularity:** If `MergeVerifier` provides distinct functionality not fully
    covered by `AnalysisService`, refactor it as a separate, reusable component
    that `AnalysisService` or `src/cli/main.py` can compose.
"""
from ..services.merge_verifier import MergeVerifier
from ..lib.git_wrapper import GitWrapper
from .progress import progress_bar

def verify_command(args):
    """
    Handles the verify command.
    """
    try:
        progress_bar(3, "verification")
        git_wrapper = GitWrapper()
        merge_verifier = MergeVerifier(git_wrapper)
        report = merge_verifier.verify(args.merged_branch_name)
        print("Verification complete:")
        print(report)
    except Exception as e:
        print(f"An error occurred during verification: {e}")

def add_verify_parser(subparsers):
    """
    Adds the parser for the verify command.
    """
    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify that merged changes reflect original intentions."
    )
    verify_parser.add_argument(
        "merged_branch_name",
        help="The name of the branch where the rebased branch was merged."
    )
    verify_parser.set_defaults(func=verify_command)