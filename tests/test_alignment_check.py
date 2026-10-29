import subprocess
import os
import shutil
import tempfile
import pytest
import sys

def run_cmd(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)  # NOSONAR

@pytest.fixture
def repo():
    # Create a temporary directory for the git repo
    d = tempfile.mkdtemp()

    # Initialize a git repo
    run_cmd(["git", "init"], cwd=d)
    run_cmd(["git", "config", "user.email", "test@example.com"], cwd=d)
    run_cmd(["git", "config", "user.name", "Test User"], cwd=d)

    # Create initial commit on main
    with open(os.path.join(d, "file.txt"), "w") as f:
        f.write("initial\n")
    run_cmd(["git", "add", "file.txt"], cwd=d)
    run_cmd(["git", "commit", "-m", "initial commit"], cwd=d)
    run_cmd(["git", "branch", "-M", "main"], cwd=d)

    # Create feature branch
    run_cmd(["git", "checkout", "-b", "feature"], cwd=d)
    with open(os.path.join(d, "file.txt"), "a") as f:
        f.write("feature change\n")
    run_cmd(["git", "add", "file.txt"], cwd=d)
    run_cmd(["git", "commit", "-m", "feature change"], cwd=d)

    yield d

    shutil.rmtree(d)

def test_alignment_up_to_date(repo):
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "alignment", "check_alignment.py")

    # At this point feature is branched off main and main hasn't moved
    # So feature is up-to-date with main
    result = subprocess.run([sys.executable, script_path, "feature", "main"], cwd=repo, capture_output=True, text=True, check=True)  # NOSONAR
    assert "Status: UP-TO-DATE" in result.stdout

def test_alignment_out_of_date(repo):
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "alignment", "check_alignment.py")

    # Move back to main and add a commit
    run_cmd(["git", "checkout", "main"], cwd=repo)
    with open(os.path.join(repo, "file2.txt"), "w") as f:
        f.write("main change\n")
    run_cmd(["git", "add", "file2.txt"], cwd=repo)
    run_cmd(["git", "commit", "-m", "main change"], cwd=repo)

    # Now feature is out of date
    result = subprocess.run([sys.executable, script_path, "feature", "main"], cwd=repo, capture_output=True, text=True)  # NOSONAR
    assert result.returncode == 1
    assert "Status: OUT-OF-DATE" in result.stdout
