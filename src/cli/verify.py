"""
TODO: Deprecate or integrate this module into `src/cli/main.py`.

This module appears to be an older or alternative implementation of a `verify` command.
The new unified CLI for `git-verifier` is located in `src/cli/main.py`.
Its functionality should either be migrated to `src/cli/main.py` or this module
(along with other modules in `src/cli/` like `analyze.py`, `ci.py`, `identify.py`,
`install.py`, `progress.py`) should be deprecated and removed.
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