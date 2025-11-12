"""
TODO: Deprecate or integrate this module into `src/cli/main.py`.

This module appears to be an older or alternative implementation of a rebase detection command.
The new unified CLI for `git-verifier` is located in `src/cli/main.py`.
Its functionality should either be migrated to `src/cli/main.py` or this module
(along with other modules in `src/cli/` like `analyze.py`, `ci.py`, `install.py`,
`progress.py`, `verify.py`) should be deprecated and removed.
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