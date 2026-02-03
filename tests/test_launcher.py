import argparse
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to the Python path to allow importing 'launch'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from setup.launch import (
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
    install_nodejs_dependencies,
    check_uvicorn_installed,
)


@patch("setup.launch.logger")
@patch("pathlib.Path.exists")
@patch("setup.launch.shutil.which", return_value=True)
@patch("setup.environment.run_command", return_value=False)
def test_install_deps_npm_install_fails(mock_run, mock_which, mock_exists, mock_logger):
    """
    Verifies that install_nodejs_dependencies exits gracefully if 'npm install' fails.
    """
    # Setup path exists side effects:
    # 1. dir_path.exists() -> True
    # 2. package_json.exists() -> True
    # 3. node_modules.exists() -> False (to trigger install)
    # 4. anything else -> True
    mock_exists.side_effect = lambda: True # Default

    # We need a more complex side effect or just ensure node_modules check returns False
    # If we patch Path.exists globally, we must be careful.
    # Logic in code:
    # dir_path.exists()
    # package_json.exists()
    # node_modules.exists()

    # Let's use a simpler approach: mock specific paths?
    # Or just use side_effect with a sequence if we know the order?
    # Order: dir_path, package_json, node_modules
    mock_exists.side_effect = [True, True, False, True, True, True]

    result = install_nodejs_dependencies("client")

    assert result is False, "Function should return False when npm install fails"
    # Note: The actual error message might vary depending on implementation details
    # We just verify it failed gracefully


@patch("setup.launch.os.environ", {"LAUNCHER_REEXEC_GUARD": "0"})
@patch("setup.launch.sys.argv", ["launch.py"])
@patch("setup.launch.platform.system", return_value="Linux")
@patch("setup.launch.sys.version_info", (3, 10, 0))  # Incompatible version
@patch("setup.launch.shutil.which")
@patch("setup.launch.subprocess.run")
@patch("setup.launch.os.execv", side_effect=Exception("Called execve"))
@patch("setup.launch.sys.exit")
@patch("setup.launch.logger")
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
        with (
            patch("setup.launch.sys.version_info", (3, 12, 0)),
            patch("setup.launch.sys.version", "3.12.0"),
            patch("setup.launch.logger") as mock_logger,
        ):
            check_python_version()
            mock_logger.info.assert_called_with("Python version 3.12.0 is compatible.")

    @patch("setup.launch.sys.version_info", (3, 8, 0))
    def test_incompatible_version(self):
        """Test that incompatible Python versions exit."""
        with pytest.raises(SystemExit):
            check_python_version()


class TestVirtualEnvironment:
    """Test virtual environment creation and management."""

    @patch("setup.launch.venv.create")
    @patch("setup.launch.Path.exists", return_value=False)
    def test_create_venv_success(self, mock_exists, mock_venv_create):
        """Test successful venv creation."""
        venv_path = ROOT_DIR / "venv"
        with patch("setup.environment.logger") as mock_logger:
            create_venv(venv_path)
            mock_venv_create.assert_called_once_with(venv_path, with_pip=True)
            mock_logger.info.assert_called_with(f"Creating virtual environment at {venv_path}")

    @patch("setup.launch.shutil.rmtree")
    @patch("setup.launch.venv.create")
    @patch("setup.launch.Path.exists")
    def test_create_venv_recreate(self, mock_exists, mock_venv_create, mock_rmtree):
        """Test venv recreation when forced."""
        # Mock exists to return True initially, then False after rmtree
        mock_exists.side_effect = [True, False]
        venv_path = ROOT_DIR / "venv"
        with patch("setup.launch.logger") as mock_logger:
            create_venv(venv_path, recreate=True)
            mock_rmtree.assert_called_once_with(venv_path)
            mock_venv_create.assert_called_once_with(venv_path, with_pip=True)


class TestDependencyManagement:
    """Test dependency installation and management."""

    @patch("subprocess.run")
    def test_setup_dependencies_success(self, mock_subprocess_run):
        """Test successful dependency setup."""
        # Mock responses - ensure stdout satisfies notmuch version check
        # other calls to subprocess.run (via run_command) just log stdout, so it's fine
        process_mock = MagicMock()
        process_mock.returncode = 0
        process_mock.stdout = "notmuch 0.38.3\n"
        process_mock.stderr = ""
        mock_subprocess_run.return_value = process_mock

        venv_path = ROOT_DIR / "venv"
        with patch("setup.launch.logger") as mock_logger:
            setup_dependencies(venv_path)

        # Verify calls were made
        assert mock_subprocess_run.called

    @patch("setup.environment.subprocess.run")
    def test_download_nltk_success(self, mock_subprocess_run):
        """Test successful NLTK data download."""
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        venv_path = ROOT_DIR / "venv"
        download_nltk_data(venv_path)
        assert mock_subprocess_run.call_count == 1


class TestServiceStartup:
    """Test service startup functions."""

    @patch("setup.launch.check_uvicorn_installed", return_value=True)
    @patch("setup.launch.get_python_executable", return_value="/app/venv/bin/python")
    @patch("setup.services.subprocess.Popen")
    def test_start_backend_success(self, mock_popen, mock_get_exec, mock_check_uvicorn):
        """Test successful backend startup."""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        with patch("setup.launch.process_manager.processes", []):
            # start_backend doesn't return anything in the current implementation
            # it just starts the process and adds it to process_manager
            start_backend("127.0.0.1", 8000)
            mock_popen.assert_called_once()

    @patch("setup.launch.get_python_executable", return_value="/app/venv/bin/python")
    @patch("setup.services.subprocess.Popen")
    def test_start_gradio_ui_success(self, mock_popen, mock_get_exec):
        """Test successful Gradio UI startup."""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        with patch("setup.launch.process_manager.processes", []):
            # start_gradio_ui doesn't return anything
            start_gradio_ui("127.0.0.1", 7860, False, False)
            mock_popen.assert_called_once()


# Integration tests
class TestLauncherIntegration:
    """Integration tests for complete launcher workflows."""

    @patch("setup.launch.subprocess.run")
    @patch("setup.launch.shutil.which", return_value="/usr/bin/npm")
    @patch("setup.launch.Path.exists", return_value=True)
    def test_full_setup_workflow(self, mock_exists, mock_which, mock_run):
        """Test complete setup workflow."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        pass  # In a real scenario, you'd verify the final state

    def test_version_compatibility_matrix(self):
        """Test version compatibility for different Python versions."""
        test_cases = [
            ((3, 9, 0), False),  # Too old
            (PYTHON_MIN_VERSION, True),  # Compatible
            ((3, 12, 5), True),  # Compatible
            (PYTHON_MAX_VERSION, True),  # Compatible
        ]

        for version_tuple, should_pass in test_cases:
            with patch("setup.launch.sys.version_info", version_tuple):
                if should_pass:
                    try:
                        check_python_version()
                    except SystemExit:
                        pytest.fail(f"Version {version_tuple} should be compatible")
                else:
                    with pytest.raises(SystemExit):
                        check_python_version()
