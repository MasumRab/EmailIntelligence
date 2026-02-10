import sys
import unittest
from unittest.mock import MagicMock, patch, PropertyMock
import pytest

from setup.launch import PYTHON_MAX_VERSION, PYTHON_MIN_VERSION, check_python_version, main

class TestLauncher(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()

    @patch('sys.version_info')
    def test_python_version_check_valid(self, mock_version_info):
        """Test checking valid Python versions."""
        # Configure mock to behave like a named tuple/object with attributes AND indexable
        type(mock_version_info).major = PropertyMock(return_value=PYTHON_MIN_VERSION[0])
        type(mock_version_info).minor = PropertyMock(return_value=PYTHON_MIN_VERSION[1])
        type(mock_version_info).micro = PropertyMock(return_value=0)

        self.assertTrue(check_python_version())

        # Test maximum supported version
        type(mock_version_info).major = PropertyMock(return_value=PYTHON_MAX_VERSION[0])
        type(mock_version_info).minor = PropertyMock(return_value=PYTHON_MAX_VERSION[1])
        self.assertTrue(check_python_version())

    @patch('sys.version_info')
    def test_python_version_check_invalid_low(self, mock_version_info):
        """Test checking python version below minimum."""
        type(mock_version_info).major = PropertyMock(return_value=PYTHON_MIN_VERSION[0])
        type(mock_version_info).minor = PropertyMock(return_value=PYTHON_MIN_VERSION[1] - 1)
        type(mock_version_info).micro = PropertyMock(return_value=0)

        self.assertFalse(check_python_version())

    @patch('sys.version_info')
    def test_python_version_check_invalid_high(self, mock_version_info):
        """Test checking python version above maximum."""
        type(mock_version_info).major = PropertyMock(return_value=PYTHON_MAX_VERSION[0])
        type(mock_version_info).minor = PropertyMock(return_value=PYTHON_MAX_VERSION[1] + 1)
        type(mock_version_info).micro = PropertyMock(return_value=0)

        self.assertFalse(check_python_version())

    @patch('setup.launch.check_python_version')
    @patch('setup.launch.setup_logging')
    @patch('setup.launch.check_environment')
    @patch('setup.launch.install_dependencies')
    @patch('setup.launch.start_services')
    def test_main_success(self, mock_start, mock_install, mock_check_env, mock_setup_log, mock_check_py):
        """Test successful main execution."""
        mock_check_py.return_value = True
        mock_check_env.return_value = True

        with patch('sys.argv', ['launch.py']):
            main()

        mock_setup_log.assert_called_once()
        mock_check_env.assert_called_once()
        mock_install.assert_called_once()
        mock_start.assert_called_once()

    @patch('setup.launch.check_python_version')
    @patch('sys.exit')
    def test_main_invalid_python(self, mock_exit, mock_check_py):
        """Test main execution with invalid python version."""
        mock_check_py.return_value = False

        with patch('sys.argv', ['launch.py']):
            main()

        mock_exit.assert_called_once_with(1)

    @patch('setup.launch.check_python_version')
    @patch('setup.launch.setup_logging')
    @patch('setup.launch.check_environment')
    @patch('sys.exit')
    def test_main_env_check_failure(self, mock_exit, mock_check_env, mock_setup_log, mock_check_py):
        """Test main execution with environment check failure."""
        mock_check_py.return_value = True
        mock_check_env.return_value = False

        with patch('sys.argv', ['launch.py']):
            main()

        mock_exit.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
