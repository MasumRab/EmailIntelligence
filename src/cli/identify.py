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
