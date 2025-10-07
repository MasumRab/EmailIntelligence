import argparse
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to the Python path to allow importing 'launch'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

<<<<<<< HEAD
from launch import ROOT_DIR, main, install_nodejs_dependencies
=======
from launch import ROOT_DIR, main, start_gradio_ui
>>>>>>> origin/main

# Test case 1: node executable is not found
@patch("launch.ROOT_DIR", Path("/app"))
@patch("pathlib.Path.exists", return_value=True)
@patch("shutil.which", return_value=None) # This will now correctly trigger the node check first
@patch("launch.logger")
def test_install_deps_node_not_found(mock_logger, mock_which, mock_exists):
    """
<<<<<<< HEAD
    Verifies that install_nodejs_dependencies exits gracefully if node is not installed.
    """
    result = install_nodejs_dependencies("client")
=======
    Verifies that start_gradio_ui exits gracefully if npm is not installed.
    """
    # The function expects 'port' for VITE_API_URL, which was missing before
    args = argparse.Namespace(host="127.0.0.1", port=8000, gradio_port=7860, debug=False, share=False)
    result = start_gradio_ui(args, sys.executable)

    # This assertion is expected to fail with the buggy code
    assert result is None, "Function should return None when npm is not found"
    client_dir = ROOT_DIR / "client"
    expected_error = (
        f"The 'npm' command was not found in your system's PATH. "
        f"Please ensure Node.js and npm are correctly installed and that the npm installation directory is added to your PATH environment variable. "
        f"Attempted to find 'npm' for the client in: {client_dir}"
    )
    mock_logger.error.assert_called_with(expected_error)
>>>>>>> origin/main

    assert result is False, "Function should return False when node is not found"
    # Correctly assert the first error that should be logged
    mock_logger.error.assert_called_with("Node.js is not installed. Please install it to continue.")

# Test case 2: npm install fails
@patch("launch.ROOT_DIR", Path("/app"))
@patch("pathlib.Path.exists", return_value=True)
@patch("shutil.which", side_effect=["/fake/path/to/node", "/fake/path/to/npm"]) # Mock both node and npm
@patch(
    "subprocess.run",
    side_effect=subprocess.CalledProcessError(1, "npm install", "Error output", "Error details"),
)
@patch("launch.logger")
def test_install_deps_npm_install_fails(mock_logger, mock_run, mock_which, mock_exists):
    """
    Verifies that install_nodejs_dependencies exits gracefully if 'npm install' fails.
    """
    result = install_nodejs_dependencies("client")

    assert result is False, "Function should return False when npm install fails"
    mock_logger.error.assert_any_call("Failed: Installing Node.js dependencies for 'client/'")


@patch('launch.os.environ', {"LAUNCHER_REEXEC_GUARD": "0"})
@patch('launch.sys.argv', ['launch.py'])
@patch('launch.platform.system', return_value='Linux')
@patch('launch.sys.version_info', (3, 10, 0)) # Incompatible version
@patch('launch.shutil.which')
@patch('launch.subprocess.run')
@patch('launch.os.execv', side_effect=Exception("Called execve"))
@patch('launch.sys.exit')
@patch('launch.logger')
def test_python_interpreter_discovery_avoids_substring_match(
    mock_logger, mock_exit, mock_execve, mock_subprocess_run, mock_which, _mock_system
):
    """
<<<<<<< HEAD
    Tests that the launcher does not incorrectly match partial version strings.
    """
    # Arrange
    mock_which.side_effect = [
        '/usr/bin/python-tricky',
        '/usr/bin/python-good',
        None,
    ]
    mock_subprocess_run.side_effect = [
        MagicMock(stdout="Python 3.1.11", stderr="", returncode=0), # Should be rejected
        MagicMock(stdout="Python 3.12.5", stderr="", returncode=0), # Should be accepted
    ]

    # Act
    try:
        main()
    except Exception as e:
        assert "Called execve" in str(e)

    # Assert
    mock_execve.assert_called_once()
    # Correctly unpack the two arguments for os.execv
    exec_path, exec_args = mock_execve.call_args[0]
    assert exec_path == '/usr/bin/python-good'
    assert exec_args[0] == '/usr/bin/python-good'
=======
    Verifies that start_gradio_ui exits gracefully if 'npm install' fails.
    """
    # The function expects 'port' for VITE_API_URL, which was missing before
    args = argparse.Namespace(host="127.0.0.1", port=8000, gradio_port=7860, debug=False, share=False)
    result = start_gradio_ui(args, sys.executable)

    # This assertion is expected to fail with the buggy code
    assert result is None, "Function should return None when npm install fails"
    client_dir = ROOT_DIR / "client"
    mock_logger.error.assert_any_call(
        f"Failed to install frontend dependencies in {client_dir}."
    )

@patch('launch.os.environ', {"LAUNCHER_REEXEC_GUARD": "0"})
@patch('launch.sys.argv', ['launch.py'])
@patch('launch.platform.system', return_value='Linux')
@patch('launch.sys.version_info', (3, 10, 0)) # Incompatible version
@patch('launch.shutil.which')
@patch('launch.subprocess.run')
@patch('launch.os.execve', side_effect=Exception("Called execve"))
@patch('launch.sys.exit')
@patch('launch.logger')
def test_python_interpreter_discovery_avoids_substring_match(
    mock_logger, mock_exit, mock_execve, mock_subprocess_run, mock_which, _mock_system
):
    """
    Tests that the launcher does not incorrectly match partial version strings (e.g., 3.111 vs 3.11).
    This test should fail with the old string-based comparison and pass with the new tuple-based one.
    """
    # Arrange
    mock_which.side_effect = [
        '/usr/bin/python-tricky',   # for python3.12
        '/usr/bin/python-good',     # for python3.11
        None,                       # for python3
    ]
    # The first interpreter found returns a version that could be a problem for string matching
    # The second one is fine.
    mock_subprocess_run.side_effect = [
        MagicMock(stdout="Python 3.111.0", stderr="", returncode=0), # Should be rejected
        MagicMock(stdout="Python 3.11.5", stderr="", returncode=0), # Should be accepted
    ]

    # Act
    main()

    # Assert
    # It should have tried to execute the second, valid interpreter
    mock_execve.assert_called_once()
    exec_path, _, _ = mock_execve.call_args[0]
    assert exec_path == '/usr/bin/python-good'

    # When the mocked execve raises an exception, the except block should log it
    # and then exit with status 1.
    assert mock_logger.error.call_count > 0
    mock_exit.assert_called_once_with(1)
>>>>>>> origin/main
