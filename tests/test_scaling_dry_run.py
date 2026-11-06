import pytest
import os
import tempfile
import subprocess
from src.scaling.dry_run import RepoDryRunner

def test_dry_run_success():
    runner = RepoDryRunner(max_workers=2)
    # We use the current directory as a success case
    repos = ["."]
    result = runner.dry_run_all(repos, "echo hello")

    assert result["total_repositories"] == 1
    assert result["successful_runs"] == 1
    assert result["failed_runs"] == 0
    assert result["all_feasible"] is True
    assert len(result["results"]) == 1

    assert result["results"][0]["status"] == "success"
    assert result["results"][0]["feasible"] is True
    assert "hello" in result["results"][0]["output"]

def test_dry_run_with_failures():
    runner = RepoDryRunner(max_workers=2)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a repo dir but command fails
        repos = [temp_dir]
        result = runner.dry_run_all(repos, "ls non_existent_file")

        assert result["total_repositories"] == 1
        assert result["successful_runs"] == 0
        assert result["failed_runs"] == 1
        assert result["all_feasible"] is False

        assert result["results"][0]["status"] == "error"
        assert result["results"][0]["feasible"] is False
        assert result["results"][0]["error"] is not None

def test_dry_run_nonexistent_repo():
    runner = RepoDryRunner(max_workers=2)
    repos = ["/path/to/nonexistent/repo/that/definitely/does/not/exist"]
    result = runner.dry_run_all(repos, "echo hello")

    assert result["total_repositories"] == 1
    assert result["failed_runs"] == 1
    assert result["results"][0]["status"] == "error"
    assert result["results"][0]["feasible"] is False

def test_dry_run_timeout():
    runner = RepoDryRunner(max_workers=1, timeout=1)
    repos = ["."]
    # Sleep longer than the timeout
    result = runner.dry_run_all(repos, "sleep 2")

    assert result["total_repositories"] == 1
    assert result["failed_runs"] == 1
    assert result["results"][0]["status"] == "timeout"
    assert result["results"][0]["feasible"] is False
