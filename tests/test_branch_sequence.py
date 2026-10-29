import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.orchestration.branch_sequence import check_branch_status


class _Result:
    def __init__(self, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def _run_by_ref(ref_rc, merge_rc):
    """Fake subprocess.run keyed on the git subcommand being invoked."""

    def fake(cmd, **kwargs):
        if "rev-parse" in cmd:
            return _Result(ref_rc)
        if "merge-tree" in cmd:
            return _Result(merge_rc, stderr="CONFLICT (content): Merge conflict in a.py")
        raise AssertionError(f"unexpected command: {cmd}")

    return fake


def test_unknown_branch_is_error_not_conflicting():
    # merge-tree exits 1 both for a conflict and for a ref it cannot resolve;
    # a missing branch must not be reported as a fork that needs resolving.
    with patch("subprocess.run", side_effect=_run_by_ref(ref_rc=1, merge_rc=1)):
        assert check_branch_status("no-such-branch") == "error"


def test_real_conflict_still_reported_as_conflicting():
    with patch("subprocess.run", side_effect=_run_by_ref(ref_rc=0, merge_rc=1)):
        assert check_branch_status("feature/x") == "conflicting"


def test_clean_merge_reported_as_clean():
    with patch("subprocess.run", side_effect=_run_by_ref(ref_rc=0, merge_rc=0)):
        assert check_branch_status("feature/x") == "clean"


def test_unsafe_ref_rejected_without_invoking_git():
    with patch("subprocess.run") as run:
        assert check_branch_status("--upload-pack=evil") == "error"
        run.assert_not_called()
