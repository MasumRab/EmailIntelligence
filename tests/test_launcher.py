import argparse
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to the Python path to allow importing 'launch'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from launch import ROOT_DIR, start_gradio_ui


# Test case 1: npm executable is not found
@patch("launch.ROOT_DIR", Path("/app"))
@patch("pathlib.Path.exists", return_value=True)
@patch("shutil.which", return_value=None)
@patch("subprocess.check_call")  # Mock node version check
@patch("launch.logger")
def test_start_gradio_ui_npm_not_found(
    mock_logger, mock_check_call, mock_which, mock_exists
):
    """
    Verifies that start_gradio_ui exits gracefully if npm is not installed.
    """
    args = argparse.Namespace(host="127.0.0.1", port=8000, gradio_port=7860, debug=False, share=False)
    python_executable = sys.executable
    result = start_gradio_ui(args, python_executable)

    assert result is None, "Function should return None when npm is not found"
    client_dir = ROOT_DIR / "client"
    expected_error = (
        f"The 'npm' command was not found in your system's PATH. "
        f"Please ensure Node.js and npm are correctly installed and that the npm installation directory is added to your PATH environment variable. "
        f"Attempted to find 'npm' for the client in: {client_dir}"
    )
    mock_logger.error.assert_called_with(expected_error)


# Test case 2: npm install fails
@patch("launch.ROOT_DIR", Path("/app"))
@patch("pathlib.Path.exists", return_value=True)
@patch("shutil.which", return_value="/fake/path/to/npm")
@patch("subprocess.check_call")  # Mock node version check
@patch(
    "subprocess.run",
    return_value=MagicMock(
        returncode=1, stdout="Error output", stderr="Error details"
    ),
)
@patch("launch.logger")
def test_start_gradio_ui_npm_install_fails(
    mock_logger, mock_run, mock_check_call, mock_which, mock_exists
):
    """
    Verifies that start_gradio_ui exits gracefully if 'npm install' fails.
    """
    args = argparse.Namespace(host="127.0.0.1", port=8000, gradio_port=7860, debug=False, share=False)
    python_executable = sys.executable
    result = start_gradio_ui(args, python_executable)

    assert result is None, "Function should return None when npm install fails"
    client_dir = ROOT_DIR / "client"
    mock_logger.error.assert_any_call(
        f"Failed to install frontend dependencies in {client_dir}."
    )