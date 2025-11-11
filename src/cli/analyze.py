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
