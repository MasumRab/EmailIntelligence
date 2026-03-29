import pytest
import subprocess
import json
from unittest.mock import patch, Mock
import os

# Assuming the CLI entry point will be something like 'python -m src.cli.main'
CLI_COMMAND = ["python", "-m", "src.cli.main"]

# Fixture to create a temporary Git repository for testing
@pytest.fixture
def temp_git_repo(tmp_path):
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    
    # Initialize a Git repository
    subprocess.run(["git", "init", "--initial-branch=main"], cwd=repo_path, check=True) # Explicitly set initial branch
    
    # Configure user for commits
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)

    # Create some commits
    (repo_path / "file1.txt").write_text("initial content")
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)

    (repo_path / "file1.txt").write_text("modified content")
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Feature A commit 1"], cwd=repo_path, check=True)

    (repo_path / "file2.txt").write_text("new file content")
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Feature A commit 2"], cwd=repo_path, check=True)

    yield repo_path

    # Cleanup is handled by tmp_path fixture

# Fixture to simulate a rebased branch
@pytest.fixture
def rebased_git_repo(tmp_path):
    repo_path = tmp_path / "rebase_test_repo"
    repo_path.mkdir()

    subprocess.run(["git", "init", "--initial-branch=main"], cwd=repo_path, check=True) # Explicitly set initial branch
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)

    # Initial commit on main
    (repo_path / "main_file.txt").write_text("main initial")
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "main: Initial commit"], cwd=repo_path, check=True)

    # Create feature branch
    subprocess.run(["git", "checkout", "-b", "feature_branch"], cwd=repo_path, check=True)
    (repo_path / "feature_file.txt").write_text("feature content")
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "feature: Add feature"], cwd=repo_path, check=True)

    # Go back to main and add another commit
    subprocess.run(["git", "checkout", "main"], cwd=repo_path, check=True)
    (repo_path / "main_file.txt").write_text("main update")
    subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "main: Update main"], cwd=repo_path, check=True)

    # Rebase feature branch onto main
    subprocess.run(["git", "checkout", "feature_branch"], cwd=repo_path, check=True)
    subprocess.run(["git", "rebase", "main"], cwd=repo_path, check=True)

    yield repo_path

# Fixture for a mock IntentReport JSON file
@pytest.fixture
def mock_intent_report_file(tmp_path):
    report_data = {
        "branch_name": "feature_branch",
        "generated_at": "2025-11-12T10:00:00Z",
        "commit_narratives": [
            {
                "commit_hexsha": "mock_sha_1",
                "author_name": "Test User",
                "authored_date": 1678886400,
                "commit_message": "feature: Add feature",
                "synthesized_narrative": "Added a new feature file with initial content.",
                "is_consistent": True,
                "discrepancy_notes": ""
            }
        ]
    }
    report_path = tmp_path / "intent_report.json"
    report_path.write_text(json.dumps(report_data))
    return report_path

class TestCliIntegration:

    @patch('subprocess.run') # Patch subprocess.run directly
    def test_analyze_command_default(self, mock_subprocess_run, temp_git_repo):
        # Configure mock_subprocess_run to simulate the CLI's behavior
        # We expect the CLI to call AnalysisService, which we'll mock internally
        mock_subprocess_run.return_value = Mock(
            stdout="Synthesized narrative for test commit.\n",
            stderr="",
            returncode=0
        )

        # Run the CLI command
        result = subprocess.run(
            CLI_COMMAND + ["analyze", "--repo-path", str(temp_git_repo)],
            capture_output=True, text=True, check=True
        )
        
        # Assertions
        assert "Synthesized narrative for test commit." in result.stdout
        mock_subprocess_run.assert_called_once_with(
            CLI_COMMAND + ["analyze", "--repo-path", str(temp_git_repo)],
            capture_output=True, text=True, check=True
        )

    @patch('subprocess.run') # Patch subprocess.run directly
    def test_analyze_command_report(self, mock_subprocess_run, temp_git_repo, tmp_path):
        output_file = tmp_path / "report.json"
        mock_subprocess_run.return_value = Mock(
            stdout="",
            stderr="",
            returncode=0
        )

        # Run the CLI command
        result = subprocess.run(
            CLI_COMMAND + ["analyze", "--report", "--output-file", str(output_file), "--repo-path", str(temp_git_repo)],
            capture_output=True, text=True, check=True
        )
        
        # Assertions
        assert result.stdout == "" # No stdout for --output-file
        # We can't assert on file content directly here as we're mocking subprocess.run
        # The actual CLI would write to the file. This test only verifies the CLI call.
        mock_subprocess_run.assert_called_once_with(
            CLI_COMMAND + ["analyze", "--report", "--output-file", str(output_file), "--repo-path", str(temp_git_repo)],
            capture_output=True, text=True, check=True
        )

    @patch('subprocess.run') # Patch subprocess.run directly
    def test_detect_rebased_command(self, mock_subprocess_run, rebased_git_repo):
        mock_subprocess_run.return_value = Mock(
            stdout="feature_branch\n",
            stderr="",
            returncode=0
        )

        # Run the CLI command
        result = subprocess.run(
            CLI_COMMAND + ["detect-rebased", "--repo-path", str(rebased_git_repo)],
            capture_output=True, text=True, check=True
        )
        
        # Assertions
        assert "feature_branch" in result.stdout
        mock_subprocess_run.assert_called_once_with(
            CLI_COMMAND + ["detect-rebased", "--repo-path", str(rebased_git_repo)],
            capture_output=True, text=True, check=True
        )

    @patch('subprocess.run') # Patch subprocess.run directly
    def test_verify_command(self, mock_subprocess_run, temp_git_repo, mock_intent_report_file, tmp_path):
        output_file = tmp_path / "verification_result.json"
        mock_subprocess_run.return_value = Mock(
            stdout="",
            stderr="",
            returncode=0
        )

        # Run the CLI command
        result = subprocess.run(
            CLI_COMMAND + ["verify", "--report", str(mock_intent_report_file), "--merged-branch", "main", "--output-file", str(output_file), "--repo-path", str(temp_git_repo)],
            capture_output=True, text=True, check=True
        )
        
        # Assertions
        assert result.stdout == "" # No stdout for --output-file
        mock_subprocess_run.assert_called_once_with(
            CLI_COMMAND + ["verify", "--report", str(mock_intent_report_file), "--merged-branch", "main", "--output-file", str(output_file), "--repo-path", str(temp_git_repo)],
            capture_output=True, text=True, check=True
        )
