import argparse
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to the Python path to allow importing 'launch'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from launch import (
    PYTHON_MAX_VERSION,
    PYTHON_MIN_VERSION,
    ROOT_DIR,
    check_python_version,
    create_venv,
    download_nltk_data,
    main,
    process_manager,
    setup_dependencies,
    start_backend,
    start_gradio_ui,
)
@patch("launch.logger")
def test_install_deps_npm_install_fails(mock_logger, mock_run, mock_which, mock_exists):
    """
    Verifies that install_nodejs_dependencies exits gracefully if 'npm install' fails.
    """
    result = install_nodejs_dependencies("client")

    assert result is False, "Function should return False when npm install fails"
    mock_logger.error.assert_any_call("Failed: Installing Node.js dependencies for 'client/'")


@patch("launch.os.environ", {"LAUNCHER_REEXEC_GUARD": "0"})
@patch("launch.sys.argv", ["launch.py"])
@patch("launch.platform.system", return_value="Linux")
@patch("launch.sys.version_info", (3, 10, 0))  # Incompatible version
@patch("launch.shutil.which")
@patch("launch.subprocess.run")
@patch("launch.os.execv", side_effect=Exception("Called execve"))
@patch("launch.sys.exit")
@patch("launch.logger")
def test_python_interpreter_discovery_avoids_substring_match(
    mock_logger, mock_exit, mock_execve, mock_subprocess_run, mock_which, _mock_system
):
    """
    Tests that the launcher does not incorrectly match partial version strings.
    """
    # Arrange
    mock_which.side_effect = [
        "/usr/bin/python-tricky",
        "/usr/bin/python-good",
        None,
    ]
    mock_subprocess_run.side_effect = [
        MagicMock(stdout="Python 3.1.11", stderr="", returncode=0),  # Should be rejected
        MagicMock(stdout="Python 3.12.5", stderr="", returncode=0),  # Should be accepted
    ]

    def test_compatible_version(self):
        """Test that compatible Python versions pass."""
        with patch("launch.platform.python_version", return_value="3.12.0"), \
             patch("launch.sys.version_info", (3, 12, 0)), \
             patch("launch.logger") as mock_logger:
            check_python_version()
            mock_logger.info.assert_called_with("Python version 3.12.0 is compatible.")

    @patch("launch.sys.version_info", (3, 8, 0))
    def test_incompatible_version(self):
        """Test that incompatible Python versions exit."""
        with pytest.raises(SystemExit):
            check_python_version()


class TestVirtualEnvironment:
    """Test virtual environment creation and management."""

    @patch("launch.venv.create")
    @patch("launch.Path.exists", return_value=False)
    def test_create_venv_success(self, mock_exists, mock_venv_create):
        """Test successful venv creation."""
        venv_path = ROOT_DIR / "venv"
        with patch("launch.logger") as mock_logger:
            create_venv(venv_path)
            mock_venv_create.assert_called_once_with(venv_path, with_pip=True)
            mock_logger.info.assert_called_with("Creating virtual environment.")

    @patch("launch.shutil.rmtree")
    @patch("launch.venv.create")
    @patch("launch.Path.exists")
    def test_create_venv_recreate(self, mock_exists, mock_venv_create, mock_rmtree):
<<<<<<< HEAD
    """Test venv recreation when forced."""
    # Mock exists to return True initially, then False after rmtree
    mock_exists.side_effect = [True, False]
    venv_path = ROOT_DIR / "venv"
=======
        """Test venv recreation when forced."""
        # Mock exists to return True initially, then False after rmtree
        mock_exists.side_effect = [True, False]
        venv_path = ROOT_DIR / "venv"
>>>>>>> 9c4d9a4 (feat: WSL optimization and NVIDIA-free setup)
        with patch("launch.logger") as mock_logger:
            create_venv(venv_path, recreate=True)
            mock_rmtree.assert_called_once_with(venv_path)
            mock_venv_create.assert_called_once_with(venv_path, with_pip=True)


class TestDependencyManagement:
    """Test dependency installation and management."""


    @patch("launch.subprocess.run")
    def test_setup_dependencies_success(self, mock_subprocess_run):
<<<<<<< HEAD
    """Test successful dependency setup."""
    mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
    venv_path = ROOT_DIR / "venv"
=======
        """Test successful dependency setup."""
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        venv_path = ROOT_DIR / "venv"
>>>>>>> 9c4d9a4 (feat: WSL optimization and NVIDIA-free setup)
        setup_dependencies(venv_path)
        mock_subprocess_run.assert_called_once()


    @patch("launch.subprocess.run")
    def test_download_nltk_success(self, mock_subprocess_run):
<<<<<<< HEAD
    """Test successful NLTK data download."""
    mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
    venv_path = ROOT_DIR / "venv"
=======
        """Test successful NLTK data download."""
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        venv_path = ROOT_DIR / "venv"
>>>>>>> 9c4d9a4 (feat: WSL optimization and NVIDIA-free setup)
        download_nltk_data(venv_path)
        assert mock_subprocess_run.call_count == 2


class TestServiceStartup:
    """Test service startup functions."""

    @patch("launch.subprocess.Popen")
    def test_start_backend_success(self, mock_popen):
    """Test successful backend startup."""
    mock_process = MagicMock()
    mock_popen.return_value = mock_process

<<<<<<< HEAD
    venv_path = ROOT_DIR / "venv"
=======
        venv_path = ROOT_DIR / "venv"
>>>>>>> 9c4d9a4 (feat: WSL optimization and NVIDIA-free setup)
        with patch.object(process_manager, "add_process") as mock_add_process:
            start_backend(venv_path, "127.0.0.1", 8000)
            mock_popen.assert_called_once()
            mock_add_process.assert_called_once_with(mock_process)

    @patch("launch.subprocess.Popen")
    def test_start_gradio_ui_success(self, mock_popen):
    """Test successful Gradio UI startup."""
    mock_process = MagicMock()
    mock_popen.return_value = mock_process

<<<<<<< HEAD
    venv_path = ROOT_DIR / "venv"
=======
        venv_path = ROOT_DIR / "venv"
>>>>>>> 9c4d9a4 (feat: WSL optimization and NVIDIA-free setup)
        with patch.object(process_manager, "add_process") as mock_add_process:
            start_gradio_ui(venv_path, "127.0.0.1", 7860, False, False)
            mock_popen.assert_called_once()
            mock_add_process.assert_called_once_with(mock_process)




# Integration tests
class TestLauncherIntegration:
    """Integration tests for complete launcher workflows."""

    @patch("launch.subprocess.run")
    @patch("launch.shutil.which", return_value="/usr/bin/npm")
    @patch("launch.Path.exists", return_value=True)
    def test_full_setup_workflow(self, mock_exists, mock_which, mock_run):
        """Test complete setup workflow."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        pass # In a real scenario, you'd verify the final state

    def test_version_compatibility_matrix(self):
        """Test version compatibility for different Python versions."""
        test_cases = [
            ((3, 10, 0), False),
            ((3, 11, 0), True),
            ((3, 12, 0), True),
            ((3, 13, 0), True),
            ((3, 14, 0), False),
        ]

        for version_tuple, should_pass in test_cases:
            with patch("launch.sys.version_info", version_tuple):
                if should_pass:
                    try:
                        check_python_version()
                    except SystemExit:
                        pytest.fail(f"Version {version_tuple} should be compatible")
                else:
                    with pytest.raises(SystemExit):
                        check_python_version()
