import os
import subprocess
import pytest
from unittest.mock import patch, MagicMock
import importlib.util
import sys

# Load intelligent_merger.py dynamically
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../scripts/intelligent_merger.py'))
spec = importlib.util.spec_from_file_location("intelligent_merger", script_path)
intelligent_merger = importlib.util.module_from_spec(spec)
sys.modules["intelligent_merger"] = intelligent_merger
spec.loader.exec_module(intelligent_merger)

def test_run_command_success():
    with patch('subprocess.run') as mock_run:
        mock_result = MagicMock()
        mock_result.stdout = "success output"
        mock_run.return_value = mock_result

        result = intelligent_merger.run_command(["git", "status"])

        mock_run.assert_called_once_with(["git", "status"], shell=False, capture_output=True, text=True, check=True)
        assert result == "success output"

def test_run_command_called_process_error():
    with patch('subprocess.run') as mock_run:
        mock_error = subprocess.CalledProcessError(1, ["git", "diff"])
        mock_error.stdout = "diff output"
        mock_run.side_effect = mock_error

        result = intelligent_merger.run_command(["git", "diff"])

        mock_run.assert_called_once_with(["git", "diff"], shell=False, capture_output=True, text=True, check=True)
        assert result == "diff output"