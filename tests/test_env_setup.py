"""
Test to verify environment setup is working correctly.
"""
import os


def test_secret_key_is_set():
    """Test that SECRET_KEY environment variable is set."""
    secret_key = os.environ.get("SECRET_KEY")
    assert secret_key is not None, "SECRET_KEY environment variable must be set"
    assert len(secret_key) >= 32, "SECRET_KEY should be at least 32 characters for security"


def test_data_dir_is_set():
    """Test that DATA_DIR environment variable is set."""
    data_dir = os.environ.get("DATA_DIR")
    assert data_dir is not None, "DATA_DIR environment variable should be set"


def test_debug_is_set():
    """Test that DEBUG environment variable is set."""
    debug = os.environ.get("DEBUG")
    assert debug is not None, "DEBUG environment variable should be set"


def test_test_data_directory_exists():
    """Test that test_data directory is created."""
    test_data_dir = os.path.join(os.path.dirname(__file__), "..", "test_data")
    assert os.path.exists(test_data_dir), "test_data directory should be created"
    assert os.path.isdir(test_data_dir), "test_data should be a directory"
