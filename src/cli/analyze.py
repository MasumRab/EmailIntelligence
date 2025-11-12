"""
Module for the `analyze` CLI command.

TODO: Refactor this module to integrate its functionality into `src/cli/main.py`
and consolidate its core analysis logic.

To adhere to SOLID principles, specifically the Single Responsibility Principle (SRP)
and Open/Closed Principle (OCP), the following steps are required:

1.  **Consolidate Core Logic:** The core analysis logic, currently within
    `RebaseAnalyzer`, should be integrated into or reused by the `AnalysisService`
    in `src/services/analysis_service.py`. This ensures a single, well-defined
    service for analysis.
2.  **CLI Command Integration:** Refactor `analyze_command` and `add_analyze_parser`
    to become part of `src/cli/main.py`'s sub-command structure, centralizing
    CLI entry points and argument parsing.
3.  **Dependency Inversion:** Ensure `analyze_command` depends on abstractions
    (e.g., an `AnalysisService` interface) rather than concrete implementations,
    allowing for easier testing and swapping of analysis backends.
4.  **Modularity:** If `RebaseAnalyzer` provides distinct functionality not fully
    covered by `AnalysisService`, refactor it as a separate, reusable component
    that `AnalysisService` or `src/cli/main.py` can compose.
"""
from ..services.rebase_analyzer import RebaseAnalyzer
from ..lib.git_wrapper import GitWrapper
from .progress import progress_bar

def analyze_command(args):
    """
    Handles the analyze command.
    """
    try:
        progress_bar(5, "analysis")
        git_wrapper = GitWrapper()
        rebase_analyzer = RebaseAnalyzer(git_wrapper)
        intentions = rebase_analyzer.analyze(args.branch_name)
        print("Analysis complete:")
        for intention in intentions:
            print(f"- {intention.description}")
    except Exception as e:
        print(f"An error occurred during analysis: {e}")

def add_analyze_parser(subparsers):
    """
    Adds the parser for the analyze command.
    """
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a rebased branch."
    )
    analyze_parser.add_argument(
        "branch_name",
        help="The name of the rebased branch to analyze."
    )
    analyze_parser.set_defaults(func=analyze_command)