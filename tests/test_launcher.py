import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to the Python path to allow importing 'launch'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from setup.launch import ROOT_DIR
from setup.validation import check_python_version


@patch("setup.launch.os.environ", {"LAUNCHER_REEXEC_GUARD": "0"}, create=True)
@patch("setup.launch.sys.argv", ["launch.py"], create=True)
@patch("setup.launch.platform.system", return_value="Linux", create=True)
@patch("setup.launch.sys.version_info", (3, 10, 0), create=True)  # Incompatible version
@patch("setup.launch.shutil.which", create=True)
@patch("setup.launch.subprocess.run", create=True)
@patch("setup.launch.os.execv", side_effect=Exception("Called execve"), create=True)
@patch("setup.launch.sys.exit", create=True)
@patch("setup.launch.logging.getLogger", create=True)
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
        with patch("setup.validation.platform.python_version", return_value="3.12.0"), \
             patch("setup.validation.sys.version_info", (3, 12, 0)), \
             patch("setup.validation.logger"):
            check_python_version()

    @patch("setup.validation.sys.version_info", (3, 8, 0))
    def test_incompatible_version(self):
        """Test that incompatible Python versions exit."""
        with pytest.raises(SystemExit):
            check_python_version()


class TestVirtualEnvironment:
    """Test virtual environment creation and management."""

    @patch("setup.launch.venv.create", create=True)
    @patch("setup.launch.Path.exists", return_value=False, create=True)
    def test_create_venv_success(self, mock_exists, mock_venv_create):
        """Test successful venv creation."""
        venv_path = ROOT_DIR / "venv"
        from setup.launch import create_venv
        with patch("setup.launch.logger", create=True):
            create_venv(venv_path)
            mock_venv_create.assert_called()


    @patch("setup.launch.shutil.rmtree", create=True)
    @patch("setup.launch.venv.create", create=True)
    @patch("setup.launch.Path.exists", create=True)
    def test_create_venv_recreate(self, mock_exists, mock_venv_create, mock_rmtree):
        """Test venv recreation when forced."""
        # Mock exists to return True initially, then False after rmtree
        mock_exists.side_effect = [True, False]
        venv_path = ROOT_DIR / "venv"
        from setup.launch import create_venv
        with patch("setup.launch.logger", create=True):
            create_venv(venv_path, recreate=True)
            mock_rmtree.assert_called_once_with(venv_path)
            mock_venv_create.assert_called()


class TestDependencyManagement:
    """Test dependency installation and management."""


    @patch("setup.launch.subprocess.run")
    @patch("setup.launch.get_python_executable", return_value="python", create=True)
    def test_setup_dependencies_success(self, mock_get_py, mock_subprocess_run):
        """Test successful dependency setup."""
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="notmuch 0.38.3", stderr="")
        venv_path = ROOT_DIR / "venv"
        from setup.launch import setup_dependencies
        setup_dependencies(venv_path)
        mock_subprocess_run.assert_called()


    @patch("launch.subprocess.run")
    @patch("setup.launch.get_python_executable", return_value="python", create=True)
    def test_download_nltk_success(self, mock_get_py, mock_subprocess_run):
        """Test successful NLTK data download."""
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        venv_path = ROOT_DIR / "venv"
        from setup.launch import download_nltk_data
        download_nltk_data(venv_path)
        assert mock_subprocess_run.call_count == 2


class TestServiceStartup:
    """Test service startup functions."""

    @patch("setup.launch.subprocess.Popen")
    @patch("setup.launch.get_python_executable", return_value="python", create=True)
    def test_start_backend_success(self, mock_get_py, mock_popen):
        """Test successful backend startup."""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        from setup.launch import start_backend
        with patch("setup.launch.process_manager.add_process", create=True) as mock_add_process:
            start_backend(host="127.0.0.1", port=8000)
            mock_popen.assert_called_once()
            mock_add_process.assert_called()

    @patch("setup.launch.subprocess.Popen")
    @patch("setup.launch.get_python_executable", return_value="python", create=True)
    def test_start_gradio_ui_success(self, mock_get_py, mock_popen):
        """Test successful Gradio UI startup."""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process

        from setup.launch import start_gradio_ui
        with patch("setup.launch.process_manager.add_process", create=True) as mock_add_process:
            start_gradio_ui(host="127.0.0.1", port=7860, share=False, debug=False)
            mock_popen.assert_called_once()
            mock_add_process.assert_called()




# Integration tests
class TestLauncherIntegration:
    """Integration tests for complete launcher workflows."""

    @patch("setup.launch.subprocess.run")
    @patch("setup.launch.shutil.which", return_value="/usr/bin/npm")
    @patch("setup.launch.Path.exists", return_value=True)
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

        from setup.validation import check_python_version
        for version_tuple, should_pass in test_cases:
            with patch("setup.validation.sys.version_info", version_tuple):
                with patch("setup.validation.PYTHON_MIN_VERSION", (3, 11)):
                    with patch("setup.validation.PYTHON_MAX_VERSION", (3, 13)):
                        if should_pass:
                            try:
                                check_python_version()
                            except SystemExit:
                                pytest.fail(f"Version {version_tuple} should be compatible")
                        else:
                            with pytest.raises(SystemExit):
                                check_python_version()
