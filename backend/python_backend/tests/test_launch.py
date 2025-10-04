import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from launch import (
    check_python_version,
    create_venv,
    download_nltk_data,
    get_python_executable,
    install_requirements_from_file,
    is_venv_available,
    parse_arguments,
    prepare_environment,
    run_application,
)

# Define the root directory for testing purposes
TEST_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.fixture(autouse=True)
def mock_root_dir(monkeypatch):
    """Fixture to mock the ROOT_DIR constant in the launch script."""
    monkeypatch.setattr("launch.ROOT_DIR", TEST_ROOT)


@pytest.fixture
def mock_args(monkeypatch):
    """Fixture to create a mock argparse.Namespace object."""
    # We need to mock sys.argv because the real parser uses it.
    monkeypatch.setattr(sys, "argv", ["launch.py"])
    args = parse_arguments()
    args.no_download_nltk = True  # Default for most tests to avoid network calls
    return args


def test_check_python_version_supported():
    """Test that a supported Python version is correctly identified."""
    with patch("sys.version_info", (3, 11, 5)):
        assert check_python_version() is True


def test_check_python_version_too_low():
    """Test that a Python version that is too low is correctly identified."""
    with patch("sys.version_info", (3, 9, 0)):
        assert check_python_version() is False


def test_check_python_version_too_high():
    """Test that a Python version that is too high is correctly identified (with a warning)."""
    with patch("sys.version_info", (3, 13, 0)):
        assert check_python_version() is True


@patch("pathlib.Path.exists")
def test_is_venv_available_unix(mock_exists):
    """Test venv availability check on Unix-like systems."""
    if platform.system() != "Windows":
        with patch("os.name", "posix"):
            mock_exists.return_value = True
            assert is_venv_available() is True
            assert mock_exists.call_count == 2


@patch("pathlib.Path.exists")
def test_is_venv_available_windows(mock_exists):
    """Test venv availability check on Windows."""
    with patch("os.name", "nt"):
        mock_exists.return_value = True
        assert is_venv_available() is True
        assert mock_exists.call_count == 2


@patch("venv.create")
def test_create_venv_success(mock_venv_create):
    """Test successful creation of a virtual environment."""
    with patch("pathlib.Path.exists", return_value=False):
        assert create_venv() is True
        mock_venv_create.assert_called_once_with(TEST_ROOT / "venv", with_pip=True)


@patch("pathlib.Path.exists", return_value=True)
def test_create_venv_already_exists(mock_exists):
    """Test that create_venv does nothing if the venv already exists."""
    with patch("venv.create") as mock_venv_create:
        assert create_venv() is True
        mock_venv_create.assert_not_called()


@patch("subprocess.run")
def test_install_requirements_success(mock_subprocess_run):
    """Test successful installation of requirements."""
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="Success", stderr="", check_returncode=lambda: None
    )
    req_file = TEST_ROOT / "requirements-test-dummy.txt"
    req_file.touch()
    assert install_requirements_from_file("requirements-test-dummy.txt") is True
    req_file.unlink()


@patch("subprocess.run")
def test_install_requirements_failure(mock_subprocess_run):
    """Test failed installation of requirements."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "pip install")
    req_file = TEST_ROOT / "requirements-test-dummy.txt"
    req_file.touch()
    assert install_requirements_from_file("requirements-test-dummy.txt") is False
    req_file.unlink()


@patch("launch.check_python_version", return_value=True)
@patch("launch.is_venv_available", return_value=True)
@patch("launch.create_venv", return_value=True)
@patch("launch.install_dependencies", return_value=True)
@patch("launch.download_nltk_data", return_value=True)
@patch("shutil.rmtree")
@patch("subprocess.run")
@patch("pathlib.Path.exists", return_value=True)
def test_prepare_environment_existing_compatible_venv(
    mock_path_exists,
    mock_subprocess_run,
    mock_rmtree,
    mock_download_nltk,
    mock_install_reqs,
    mock_create_venv,
    mock_is_venv,
    mock_check_py,
    mock_args,
):
    """Test prepare_environment with an existing, compatible venv."""
    mock_subprocess_run.return_value = MagicMock(stdout="Python 3.11.5")
    mock_args.no_download_nltk = False
    assert prepare_environment(mock_args) is True
    mock_create_venv.assert_not_called()
    mock_install_reqs.assert_not_called()
    mock_download_nltk.assert_called_once()


@patch("launch.check_python_version", return_value=True)
@patch("launch.is_venv_available", return_value=False)
@patch("launch.create_venv", return_value=True)
@patch("launch._get_primary_requirements_file", return_value="requirements.txt")
@patch("launch.install_dependencies", return_value=True)
@patch("launch.download_nltk_data", return_value=True)
@patch("pathlib.Path.exists", return_value=True)
def test_prepare_environment_no_venv(
    mock_path_exists,
    mock_download_nltk,
    mock_install_reqs,
    mock_get_req_file,
    mock_create_venv,
    mock_is_venv,
    mock_check_py,
    mock_args,
):
    """Test prepare_environment when no venv exists."""
    mock_args.stage = "dev"
    mock_args.no_download_nltk = False

    assert prepare_environment(mock_args) is True

    mock_create_venv.assert_called_once()
    assert mock_install_reqs.call_count == 2
    mock_download_nltk.assert_called_once()


@patch("launch.start_backend")
@patch("launch.start_gradio_ui")
def test_run_application_dev_mode(mock_start_gradio, mock_start_backend, mock_args):
    """Test run_application in default development mode."""
    mock_backend_proc = MagicMock()
    mock_backend_proc.poll.return_value = None
    mock_start_backend.return_value = mock_backend_proc

    mock_gradio_proc = MagicMock()
    mock_gradio_proc.poll.return_value = None
    mock_start_gradio.return_value = mock_gradio_proc

    with patch("time.sleep", side_effect=KeyboardInterrupt):
        assert run_application(mock_args) == 0

    mock_start_backend.assert_called_once()
    mock_start_gradio.assert_called_once()


@patch("launch.start_backend")
def test_run_application_api_only(mock_start_backend, mock_args):
    """Test run_application in API-only mode."""
    mock_args.api_only = True
    mock_backend_proc = MagicMock()
    mock_backend_proc.wait.return_value = 0
    mock_start_backend.return_value = mock_backend_proc

    assert run_application(mock_args) == 0
    mock_start_backend.assert_called_once()


@patch("deployment.test_stages.test_stages")
def test_run_application_test_stage(mock_test_stages, mock_args):
    """Test run_application in test stage."""
    mock_args.stage = "test"
    mock_test_stages.run_unit_tests.return_value = True
    mock_test_stages.run_integration_tests.return_value = True

    assert run_application(mock_args) == 0
    mock_test_stages.run_unit_tests.assert_called_once()
    mock_test_stages.run_integration_tests.assert_called_once()