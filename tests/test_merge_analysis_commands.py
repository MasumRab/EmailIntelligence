"""The merge-analysis scripts must actually run git.

Both `scripts/intelligent_merge_analyzer.py` and `scripts/path_change_detector.py`
wrapped process execution as

    def run_command(cmd: str) -> str:
        result = subprocess.run(cmd, shell=False, capture_output=True, text=True)

With `shell=False`, a string is taken as the *program name*, so every call
raised `FileNotFoundError: 'git diff ...'` instead of running git.

The analyzer's failure was silent rather than loud: `get_changed_lines` catches
the exception and returns an empty set, so `analyze_overlap` computed a 0%
overlap for every file and recommended "LOW OVERLAP - Safe to auto-merge" no
matter what the two ranges actually touched.
"""

import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load(relative_path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def analyzer():
    return _load("scripts/intelligent_merge_analyzer.py", "intelligent_merge_analyzer")


@pytest.fixture(scope="module")
def detector_module():
    return _load("scripts/path_change_detector.py", "path_change_detector")


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A two-commit repository whose second commit changes line 2 of a.txt."""

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True
        )

    git("init", "-q", "-b", "main")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "Test")
    (tmp_path / "a.txt").write_text("one\ntwo\nthree\n")
    git("add", "a.txt")
    git("commit", "-q", "-m", "first")
    (tmp_path / "a.txt").write_text("one\nTWO CHANGED\nthree\n")
    git("commit", "-q", "-am", "second")

    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_get_changed_lines_reports_real_line_numbers(analyzer, repo):
    """`git diff` must actually run, so the changed line must show up."""
    lines = analyzer.get_changed_lines("a.txt", "HEAD~1..HEAD")

    # The pre-fix code swallowed FileNotFoundError and returned set().
    assert lines, "get_changed_lines returned nothing — git was never invoked"
    assert 2 in lines


def test_analyze_overlap_detects_overlap_when_ranges_collide(analyzer, repo):
    """Two identical ranges overlap completely; they must not read as 'safe'."""
    result = analyzer.analyze_overlap("a.txt", "HEAD~1..HEAD", "HEAD~1..HEAD")

    assert result.total_changed_lines > 0
    assert "LOW OVERLAP" not in result.recommendation


def test_scan_branches_lists_files_per_branch(detector_module, repo):
    """`git ls-tree` must actually run for both branches."""
    subprocess.run(
        ["git", "checkout", "-q", "-b", "other"], cwd=repo, check=True, capture_output=True
    )
    (repo / "b.txt").write_text("x\n")
    subprocess.run(["git", "add", "b.txt"], cwd=repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "add b"], cwd=repo, check=True, capture_output=True
    )
    subprocess.run(
        ["git", "checkout", "-q", "main"], cwd=repo, check=True, capture_output=True
    )

    detector = detector_module.PathChangeDetector("main", "other")
    detector.scan_branches()

    assert "a.txt" in detector.local_files
    assert "b.txt" in detector.remote_files
    assert "b.txt" not in detector.local_files
