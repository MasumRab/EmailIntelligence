import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the root directory to the Python path to allow for top-level imports
# This makes the test environment mimic the production environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

class TestLaunchScript(unittest.TestCase):

    @patch('launch.parse_arguments')
    def test_import_and_main_function_existence(self, mock_parse_args):
        """
        Test that the launch script can be imported without errors and that
        the main function and its helpers exist.
        """
        # Mock the argument parser to avoid issues with command-line arguments
        # during testing.
        mock_parse_args.return_value = MagicMock()

        try:
            import launch
            # We are not calling main() directly because it contains sys.exit() calls
            # and complex logic that is hard to test in a unit test.
            # Instead, we are verifying that the script is importable and has the
            # expected structure.
            self.assertIsNotNone(launch, "The launch module should not be None.")
            self.assertTrue(hasattr(launch, 'main'), "The launch module should have a 'main' function.")
            self.assertTrue(hasattr(launch, 'prepare_environment'), "The launch module should have a 'prepare_environment' function.")
            self.assertTrue(hasattr(launch, 'run_application'), "The launch module should have a 'run_application' function.")
        except ImportError as e:
            self.fail(f"Failed to import launch.py. This is a critical error. Details: {e}")

if __name__ == '__main__':
    unittest.main()