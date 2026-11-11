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


def _run_by_ref(base_rc=0, merge_rc=0, conflict=False):
    import subprocess
    def fake(cmd, **kwargs):
        if "merge-base" in cmd:
            if base_rc != 0:
                raise subprocess.CalledProcessError(base_rc, cmd)
            return _Result(base_rc, stdout="base-sha")
        if "merge-tree" in cmd:
            if merge_rc != 0:
                raise subprocess.CalledProcessError(merge_rc, cmd)
            out = "<<<<<<< ours\nx\n=======\ny\n>>>>>>> theirs\n" if conflict else ""
            return _Result(merge_rc, stdout=out)
        raise AssertionError(f"unexpected command: {cmd}")

    return fake


def test_unknown_branch_is_error_not_conflicting():
    # merge-tree exits 1 both for a conflict and for a ref it cannot resolve;
    # a missing branch must not be reported as a fork that needs resolving.
    with patch("subprocess.run", side_effect=_run_by_ref(base_rc=1)):
        assert check_branch_status("no-such-branch") == "error"


def test_real_conflict_still_reported_as_conflicting():
    with patch("subprocess.run", side_effect=_run_by_ref(conflict=True)):
        assert check_branch_status("feature/x") == "conflicting"


def test_clean_merge_reported_as_clean():
    with patch("subprocess.run", side_effect=_run_by_ref()):
        assert check_branch_status("feature/x") == "clean"


def test_unsafe_ref_rejected_without_invoking_git():
    with patch("subprocess.run") as run:
        assert check_branch_status("--upload-pack=evil") == "error"
        run.assert_not_called()
