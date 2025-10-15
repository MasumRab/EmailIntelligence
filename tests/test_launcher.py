"""
Tests for the EmailIntelligence launcher (launch.py).

This module contains comprehensive tests for the launcher functionality,
including environment setup, dependency management, and service startup.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

<<<<<<< HEAD
from launch import (
    PYTHON_MAX_VERSION,
    PYTHON_MIN_VERSION,
    ROOT_DIR,
    check_python_version,
    create_venv,
    download_nltk_data,
    install_uv,
    main,
    process_manager,
    setup_dependencies,
    start_backend,
    start_client,
    start_gradio_ui,
    start_server_ts,
    install_nodejs_dependencies,
)


class TestPythonVersionCheck:
    """Test Python version compatibility checking."""

    @patch("launch.sys.version_info", (3, 12, 0))
    @patch("launch.sys.version", "3.12.0")
    def test_compatible_version(self, mock_version, mock_version_info):
        """Test that compatible Python versions pass."""
        with patch("launch.logger") as mock_logger:
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
            mock_logger.info.assert_called_with(f"Creating virtual environment at {venv_path}")

    @patch("launch.Path.exists", return_value=True)
    def test_create_venv_already_exists(self, mock_exists):
        """Test when venv already exists."""
        venv_path = ROOT_DIR / "venv"
        with patch("launch.logger") as mock_logger:
            create_venv(venv_path)
            mock_logger.info.assert_called_with(
                f"Virtual environment already exists at {venv_path}"
            )

    @patch("launch.shutil.rmtree")
    @patch("launch.venv.create")
    @patch("launch.Path.exists")
    def test_create_venv_recreate(self, mock_exists, mock_venv_create, mock_rmtree):
        """Test venv recreation when forced."""
        # Mock exists to return True initially, then False after rmtree
        mock_exists.side_effect = [True, False]
        venv_path = ROOT_DIR / "venv"
        with patch("launch.logger") as mock_logger:
            create_venv(venv_path, recreate=True)
            mock_rmtree.assert_called_once_with(venv_path)
            mock_venv_create.assert_called_once_with(venv_path, with_pip=True)


class TestDependencyManagement:
    """Test dependency installation and management."""

    @patch("launch.subprocess.run")
    @patch("launch.Path.exists", return_value=True)
    def test_install_uv_success(self, mock_exists, mock_run):
        """Test successful uv installation."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        venv_path = ROOT_DIR / "venv"
        with patch("launch.logger") as mock_logger:
            install_uv(venv_path)
            mock_run.assert_called_once()
            mock_logger.info.assert_any_call("Installing uv package manager...")

    @patch("launch.subprocess.run")
    @patch("launch.Path.exists", return_value=True)
    def test_setup_dependencies_success(self, mock_exists, mock_run):
        """Test successful dependency setup."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        venv_path = ROOT_DIR / "venv"
        with patch("launch.logger") as mock_logger:
            setup_dependencies(venv_path)
            mock_logger.info.assert_any_call("Installing project dependencies with uv...")

    @patch("launch.subprocess.run")
    @patch("launch.Path.exists", return_value=True)
    def test_download_nltk_success(self, mock_exists, mock_run):
        """Test successful NLTK data download."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        venv_path = ROOT_DIR / "venv"
        with patch("launch.logger") as mock_logger:
            download_nltk_data(venv_path)
            mock_logger.info.assert_called_with("NLTK data downloaded successfully.")


class TestServiceStartup:
    """Test service startup functions."""

    @patch("launch.subprocess.Popen")
    @patch("launch.check_uvicorn_installed", return_value=True)
    def test_start_backend_success(self, mock_check_uvicorn, mock_popen):
        """Test successful backend startup."""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        venv_path = ROOT_DIR / "venv"
        with patch.object(process_manager, "add_process") as mock_add_process:
            result = start_backend(venv_path, "127.0.0.1", 8000)
            assert result == mock_process
            mock_add_process.assert_called_once_with(mock_process)

    @patch("launch.subprocess.Popen")
    @patch("launch.Path.exists", return_value=True)
    def test_start_gradio_ui_success(self, mock_exists, mock_popen):
        """Test successful Gradio UI startup."""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        venv_path = ROOT_DIR / "venv"
        with patch.object(process_manager, "add_process") as mock_add_process:
            result = start_gradio_ui(venv_path, "127.0.0.1")
            assert result == mock_process
            mock_add_process.assert_called_once_with(mock_process)

    @patch("launch.subprocess.Popen")
    @patch("launch.install_nodejs_dependencies", return_value=True)
    def test_start_client_install_deps(self, mock_install_deps, mock_popen):
        """Test client startup with dependency installation."""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        with patch.object(process_manager, "add_process") as mock_add_process:
            result = start_client()
            assert result == mock_process
            mock_add_process.assert_called_once_with(mock_process)
            mock_install_deps.assert_called_once_with("client")

    @patch("launch.subprocess.Popen")
    @patch("launch.subprocess.run")
    @patch("launch.shutil.which", return_value="/usr/bin/npm")
    @patch("launch.Path.exists", side_effect=[True, False])
    def test_start_server_ts_install_deps(self, mock_exists, mock_which, mock_run, mock_popen):
        """Test TypeScript server startup with dependency installation."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        with patch.object(process_manager, "add_process") as mock_add_process:
            result = start_server_ts()
            assert result == mock_process
            mock_add_process.assert_called_once_with(mock_process)
            mock_run.assert_called_once_with(
                ["npm", "install"],
                cwd=ROOT_DIR / "server",
                capture_output=True,
                text=True,
                shell=isinstance(sys.platform, str) and sys.platform == "win32",
            )
=======
from launch import ROOT_DIR, main, start_gradio_ui, install_nodejs_dependencies
>>>>>>> main


# Test case 1: node executable is not found
@patch("launch.ROOT_DIR", Path("/app"))
@patch("pathlib.Path.exists", return_value=True)
@patch("shutil.which", return_value=None)  # This will now correctly trigger the node check first
@patch("launch.logger")
def test_install_deps_node_not_found(mock_logger, mock_which, mock_exists):
    """
    Verifies that install_nodejs_dependencies exits gracefully if node is not installed.
    """
    result = install_nodejs_dependencies("client")

    assert result is False, "Function should return False when node is not found"
    # Correctly assert the first error that should be logged
    mock_logger.error.assert_called_with("Node.js is not installed. Please install it to continue.")


# Test case 2: npm install fails
@patch("launch.ROOT_DIR", Path("/app"))
@patch("pathlib.Path.exists", return_value=True)
<<<<<<< HEAD
@patch("shutil.which", side_effect=["/fake/path/to/node", "/fake/path/to/npm"])  # Mock both node and npm
=======
@patch(
    "shutil.which", side_effect=["/fake/path/to/node", "/fake/path/to/npm"]
)  # Mock both node and npm
>>>>>>> main
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


<<<<<<< HEAD
class TestMainFunction:
    """Test the main launcher function and argument parsing."""
=======
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
>>>>>>> main

    @patch("launch.check_python_version")
    @patch("argparse.ArgumentParser.parse_args")
    @patch("launch.install_uv")
    @patch("launch._handle_setup_mode")
    def test_main_setup_mode(self, mock_handle_setup, mock_install_uv, mock_parse, mock_check_version):
        """Test main function in setup mode."""
        # Mock setup arguments
        mock_args = MagicMock()
        mock_args.setup = True
        mock_args.update_deps = False
        mock_args.no_venv = False
        mock_args.force_recreate_venv = False
        mock_args.no_download_nltk = False
        mock_args.env_file = None
        mock_args.use_poetry = False
        mock_parse.return_value = mock_args

<<<<<<< HEAD
        with patch("launch.create_venv") as mock_create_venv:
            with patch("launch.setup_dependencies") as mock_setup_deps:
                with patch("launch.download_nltk_data") as mock_download_nltk:
                    with patch("launch.logger") as mock_logger:
                        main()
                        mock_handle_setup.assert_called_once()

    @patch("launch.check_python_version")
    @patch("argparse.ArgumentParser.parse_args")
    @patch("launch.Path.exists", return_value=True)
    @patch("launch.shutil.rmtree")
    @patch("launch.validate_environment", return_value=True)
    @patch("launch._handle_setup_mode")
    def test_main_launch_mode(
        self, mock_handle_setup, mock_validate_env, mock_rmtree, mock_exists, mock_parse, mock_check_version
    ):
        """Test main function in launch mode."""
        # Mock launch arguments
        mock_args = MagicMock()
        mock_args.setup = False
        mock_args.update_deps = False
        mock_args.no_venv = False
        mock_args.no_backend = False
        mock_args.no_ui = False
        mock_args.no_client = False
        mock_args.host = "127.0.0.1"
        mock_args.port = 8000
        mock_args.gradio_port = None
        mock_args.debug = False
        mock_args.share = False
        mock_args.listen = False
        mock_args.env_file = None
        mock_parse.return_value = mock_args

        with patch("launch.start_backend") as mock_start_backend:
            with patch("launch.start_gradio_ui") as mock_start_ui:
                with patch("launch.start_client") as mock_start_client:
                    with patch("launch.start_server_ts") as mock_start_server:
                        with patch("launch.time.sleep"):
                            with patch("launch.wait_for_processes"):
                                main()
                                mock_start_backend.assert_called_once()
                                mock_start_ui.assert_called_once()
                                mock_start_client.assert_called_once()
                                mock_start_server.assert_called_once()


class TestErrorHandling:
    """Test error handling scenarios."""

    @patch("launch.subprocess.run")
    def test_run_command_failure(self, mock_run):
        """Test command execution failure handling."""
        from launch import run_command

        mock_run.side_effect = subprocess.CalledProcessError(
            1, "failing command", "error output", "error details"
        )

        result = run_command(["failing", "command"], "Test command")
        assert result is False

    @patch("launch.shutil.which", return_value=None)
    def test_node_not_found(self, mock_which):
        """Test handling when Node.js is not installed."""
        from launch import check_node_npm_installed

        result = check_node_npm_installed()
        assert result is False

    @patch("launch.shutil.which")
    def test_npm_not_found(self, mock_which):
        """Test handling when npm is not installed."""

        # Mock shutil.which to return node but not npm
        def which_side_effect(cmd):
            if cmd == "node":
                return "/usr/bin/node"
            elif cmd == "npm":
                return None
            return None

        mock_which.side_effect = which_side_effect
        from launch import check_node_npm_installed

        result = check_node_npm_installed()
        assert result is False


# Integration tests
class TestLauncherIntegration:
    """Integration tests for complete launcher workflows."""

    @patch("launch.subprocess.run")
    @patch("launch.shutil.which", return_value="/usr/bin/npm")
    @patch("launch.Path.exists", return_value=True)
    def test_full_setup_workflow(self, mock_exists, mock_which, mock_run):
        """Test complete setup workflow."""
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        # This would test the complete setup process
        # In a real scenario, you'd set up actual temp directories
        # and verify the final state
        pass

    def test_version_compatibility_matrix(self):
        """Test version compatibility for different Python versions."""
        test_cases = [
            ((3, 10, 0), False),  # Too old
            ((3, 11, 0), True),  # Compatible
            ((3, 12, 0), True),  # Compatible
            ((3, 13, 0), False),  # Too new
        ]

        for version_tuple, should_pass in test_cases:
            with patch("launch.sys.version_info", version_tuple):
                if should_pass:
                    # Should not raise SystemExit
                    try:
                        check_python_version()
                    except SystemExit:
                        pytest.fail(f"Version {version_tuple} should be compatible")
                else:
                    # Should raise SystemExit
                    with pytest.raises(SystemExit):
                        check_python_version()
=======
    # Assert
    mock_execve.assert_called_once()
    # Correctly unpack the two arguments for os.execv
    exec_path, exec_args = mock_execve.call_args[0]
    assert exec_path == "/usr/bin/python-good"

    # When the mocked execve raises an exception, the except block should log it
    # and then exit with status 1.
    assert mock_logger.error.call_count > 0
    mock_exit.assert_called_once_with(1)
>>>>>>> main
