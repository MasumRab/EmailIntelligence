import argparse
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to the Python path to allow importing 'launch'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

from setup.launch import main
from setup.utils import ROOT_DIR, process_manager
from setup.validation import check_python_version, PYTHON_MIN_VERSION, PYTHON_MAX_VERSION
from setup.environment import create_venv, setup_dependencies, download_nltk_data
from setup.services import start_backend, start_gradio_ui, install_nodejs_dependencies



class TestVirtualEnvironment:
    """Test virtual environment creation and management."""

    @patch("venv.create")
    @patch("pathlib.Path.exists", return_value=False)
    def test_create_venv_success(self, mock_exists, mock_venv_create):
        """Test successful venv creation."""
        venv_path = ROOT_DIR / "venv"
        with patch("logging.getLogger") as mock_logger:
            create_venv(venv_path)
            mock_venv_create.assert_called_once_with(venv_path, with_pip=True)

    @patch("shutil.rmtree")
    @patch("venv.create")
    @patch("pathlib.Path.exists")
    def test_create_venv_recreate(self, mock_exists, mock_venv_create, mock_rmtree):
        """Test venv recreation when forced."""
        # Mock exists to return True initially, then False after rmtree
        mock_exists.side_effect = [True, False]
        venv_path = ROOT_DIR / "venv"
        with patch("logging.getLogger") as mock_logger:
            create_venv(venv_path, recreate=True)
            mock_rmtree.assert_called_once_with(venv_path)
            mock_venv_create.assert_called_once_with(venv_path, with_pip=True)


class TestDependencyManagement:
    """Test dependency installation and management."""



class TestLauncherIntegration:
    """Integration tests for complete launcher workflows."""

    @patch("shutil.which", return_value="/usr/bin/npm")
    @patch("pathlib.Path.exists", return_value=True)
    def test_full_setup_workflow(self, mock_exists, mock_which):
        """Test complete setup workflow."""
        
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
            with patch("sys.version_info", version_tuple):
                if should_pass:
                    try:
                        check_python_version()
                    except SystemExit:
                        pytest.fail(f"Version {version_tuple} should be compatible")
                else:
                    with pytest.raises(SystemExit):
                        check_python_version()
