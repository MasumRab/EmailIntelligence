import os
import json
import subprocess
import pytest
from pathlib import Path
from scripts.branch_ref_backup import snapshot, restore, BACKUP_FILE_DEFAULT

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}\nError: {result.stderr.strip()}")
    return result.stdout.strip()

@pytest.fixture
def temp_git_repo(tmp_path):
    """Creates a temporary git repository for testing."""
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        run_cmd("git init")
        run_cmd("git config user.email 'test@example.com'")
        run_cmd("git config user.name 'Test User'")
        run_cmd("git checkout -B main")

        # Create initial commit
        test_file = tmp_path / "test.txt"
        test_file.write_text("initial content")
        run_cmd("git add test.txt")
        run_cmd("git commit -m 'Initial commit'")

        yield tmp_path
    finally:
        os.chdir(original_cwd)

def test_snapshot_and_restore(temp_git_repo):
    # Get initial SHA
    initial_sha = run_cmd("git rev-parse HEAD")

    # Take a snapshot
    backup_file = str(temp_git_repo / BACKUP_FILE_DEFAULT)
    snapshot(backup_file)

    # Verify backup file contents
    assert os.path.exists(backup_file)
    with open(backup_file, "r") as f:
        data = json.load(f)

    assert data["branch"] == "main"
    assert data["sha"] == initial_sha
    assert "timestamp" in data

    # Make a new commit
    test_file = temp_git_repo / "test.txt"
    test_file.write_text("new content")
    run_cmd("git add test.txt")
    run_cmd("git commit -m 'Second commit'")

    # Verify we are on a new SHA
    new_sha = run_cmd("git rev-parse HEAD")
    assert new_sha != initial_sha
    assert test_file.read_text() == "new content"

    # Restore from snapshot
    restore(backup_file)

    # Verify we are back to initial state
    restored_sha = run_cmd("git rev-parse HEAD")
    assert restored_sha == initial_sha
    assert test_file.read_text() == "initial content"

def test_restore_invalid_data(tmp_path):
    backup_file = str(tmp_path / BACKUP_FILE_DEFAULT)
    with open(backup_file, "w") as f:
        json.dump({"branch": "-b", "sha": "1234", "timestamp": "2023-01-01T00:00:00"}, f)
    with pytest.raises(ValueError):
        restore(backup_file)
    with open(backup_file, "w") as f:
        json.dump({"branch": "../../etc", "sha": "1234", "timestamp": "2023-01-01T00:00:00"}, f)
    with pytest.raises(ValueError):
        restore(backup_file)
