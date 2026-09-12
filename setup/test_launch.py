#!/usr/bin/env python3
"""
Lightweight Launch.py Testing Script

This script provides comprehensive testing of setup/launch.py functionality
without requiring full package downloads or heavy operations.

Tests:
- Import verification
- Argument parsing (command pattern vs legacy)
- Main function routing logic
- COMMAND_PATTERN_AVAILABLE detection
- Basic function availability

Usage:
    python setup/test_launch.py                    # Run all tests
    python setup/test_launch.py --quick           # Skip slow operations
    python setup/test_launch.py --verbose         # Detailed output
"""

import argparse
import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root and setup directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(Path(__file__).parent))

class LaunchPyTest(unittest.TestCase):
    """Test cases for launch.py functionality."""

    def setUp(self):
        """Set up test environment."""
        self.launch_module = None
        self.original_argv = sys.argv.copy()

    def tearDown(self):
        """Clean up after tests."""
        sys.argv = self.original_argv
        if 'setup.launch' in sys.modules:
            del sys.modules['setup.launch']

    def _import_launch_module(self):
        """Import launch module with error handling."""
        if self.launch_module is None:
            try:
                import setup.launch as launch
                self.launch_module = launch
            except ImportError as e:
                self.fail(f"Failed to import setup.launch: {e}")
        return self.launch_module

    def test_imports(self):
        """Test that all required imports work."""
        launch = self._import_launch_module()

        # Test that COMMAND_PATTERN_AVAILABLE is defined
        self.assertTrue(hasattr(launch, 'COMMAND_PATTERN_AVAILABLE'))
        self.assertIsInstance(launch.COMMAND_PATTERN_AVAILABLE, bool)

        # Test that main function exists
        self.assertTrue(hasattr(launch, 'main'))
        self.assertTrue(callable(launch.main))

        # Test that helper functions exist
        required_functions = [
            '_check_setup_warnings',
            '_execute_command',
            '_handle_legacy_args',
            '_add_common_args',
            '_add_legacy_args'
        ]

        for func_name in required_functions:
            self.assertTrue(hasattr(launch, func_name), f"Missing function: {func_name}")
            self.assertTrue(callable(getattr(launch, func_name)), f"{func_name} is not callable")

    def test_command_pattern_detection(self):
        """Test COMMAND_PATTERN_AVAILABLE detection logic."""
        launch = self._import_launch_module()

        # The variable should be set based on whether get_command_factory is available
        expected_value = launch.get_command_factory is not None
        self.assertEqual(launch.COMMAND_PATTERN_AVAILABLE, expected_value)

    @patch('setup.launch._check_setup_warnings')
    @patch('setup.launch._execute_command')
    def test_main_command_pattern_routing(self, mock_execute, mock_check):
        """Test main() routing to command pattern."""
        launch = self._import_launch_module()

        # Mock command pattern being available
        with patch.object(launch, 'COMMAND_PATTERN_AVAILABLE', True):
            with patch.object(launch, 'initialize_all_services'):
                # Test command routing
                test_args = ['setup', 'launch.py', 'test', '--unit']
                with patch('sys.argv', test_args):
                    result = launch.main()

                mock_execute.assert_called_once()
                args = mock_execute.call_args[0][1]
                self.assertEqual(args.command, 'test')
                self.assertTrue(args.unit)

    @patch('setup.launch._check_setup_warnings')
    @patch('setup.launch._handle_legacy_args')
    def test_main_legacy_routing(self, mock_handle, mock_check):
        """Test main() routing to legacy arguments."""
        launch = self._import_launch_module()

        # Mock command pattern being unavailable
        with patch.object(launch, 'COMMAND_PATTERN_AVAILABLE', False):
            # Test legacy routing
            test_args = ['setup', 'launch.py', '--setup', '--debug']
            with patch('sys.argv', test_args):
                result = launch.main()

            mock_handle.assert_called_once()
            args = mock_handle.call_args[0][0]
            self.assertTrue(args.setup)
            self.assertTrue(args.debug)

    def test_argument_parsing_command_pattern(self):
        """Test argument parsing for command pattern."""
        launch = self._import_launch_module()

        # Test setup command
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")
        setup_parser = subparsers.add_parser("setup", help="Set up the development environment")
        launch._add_common_args(setup_parser)

        args = parser.parse_args(['setup', '--debug'])
        self.assertEqual(args.command, 'setup')
        self.assertTrue(args.debug)

        # Test test command
        test_parser = subparsers.add_parser("test", help="Run tests")
        launch._add_common_args(test_parser)
        test_parser.add_argument("--unit", action="store_true", help="Run unit tests")

        args = parser.parse_args(['test', '--unit', '--debug'])
        self.assertEqual(args.command, 'test')
        self.assertTrue(args.unit)
        self.assertTrue(args.debug)

    def test_argument_parsing_legacy(self):
        """Test argument parsing for legacy mode."""
        launch = self._import_launch_module()

        # Test legacy parser setup
        parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher")
        parser.add_argument("--setup", action="store_true", help="Set up the environment (legacy)")
        parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
        launch._add_legacy_args(parser)

        # Test legacy arguments
        args = parser.parse_args(['--setup', '--debug', '--port', '8080'])
        self.assertTrue(args.setup)
        self.assertTrue(args.debug)
        self.assertEqual(args.port, 8080)

    @patch('setup.launch.logger')
    def test_check_setup_warnings(self, mock_logger):
        """Test setup warnings check."""
        launch = self._import_launch_module()

        # This should run without errors
        launch._check_setup_warnings()

        # Should log some information
        mock_logger.warning.assert_called()
        mock_logger.info.assert_called()

    def test_helper_functions_exist(self):
        """Test that all helper functions are properly defined."""
        launch = self._import_launch_module()

        # Test that key functions don't raise NameError
        try:
            # These should not raise NameError if properly imported
            launch.check_python_version
            launch.validate_environment
            launch.print_system_info
            launch.setup_wsl_environment
            launch.check_wsl_requirements
        except NameError as e:
            self.fail(f"NameError in helper functions: {e}")


class QuickTestRunner:
    """Quick test runner that skips heavy operations."""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.results = []

    def run_test(self, test_name, test_func):
        """Run a single test."""
        try:
            if self.verbose:
                print(f"Running {test_name}...")
            test_func()
            self.results.append((test_name, True, None))
            if self.verbose:
                print(f"✅ {test_name} - PASSED")
        except Exception as e:
            self.results.append((test_name, False, str(e)))
            if self.verbose:
                print(f"❌ {test_name} - FAILED: {e}")

    def run_quick_tests(self):
        """Run quick tests without heavy dependencies."""
        print("Running quick launch.py tests...")

        # Test 1: Import test
        def test_imports():
            try:
                import setup.launch as launch
                assert hasattr(launch, 'COMMAND_PATTERN_AVAILABLE')
                assert hasattr(launch, 'main')
                assert callable(launch.main)
            except Exception as e:
                raise AssertionError(f"Import test failed: {e}")

        # Test 2: Command pattern detection
        def test_command_pattern():
            import setup.launch as launch
            expected = launch.get_command_factory is not None
            assert launch.COMMAND_PATTERN_AVAILABLE == expected

        # Test 3: Argument parsing
        def test_arg_parsing():
            import setup.launch as launch
            parser = argparse.ArgumentParser()
            subparsers = parser.add_subparsers(dest="command")
            setup_parser = subparsers.add_parser("setup")
            launch._add_common_args(setup_parser)

            args = parser.parse_args(['setup', '--debug'])
            assert args.command == 'setup'
            assert args.debug == True

        # Test 4: Legacy argument parsing
        def test_legacy_args():
            import setup.launch as launch
            parser = argparse.ArgumentParser()
            launch._add_legacy_args(parser)

            args = parser.parse_args(['--setup', '--port', '9000'])
            assert args.setup == True
            assert args.port == 9000

        # Run tests
        self.run_test("Import Test", test_imports)
        self.run_test("Command Pattern Detection", test_command_pattern)
        self.run_test("Command Pattern Arguments", test_arg_parsing)
        self.run_test("Legacy Arguments", test_legacy_args)

        return self.summarize_results()

    def summarize_results(self):
        """Summarize test results."""
        passed = sum(1 for _, success, _ in self.results if success)
        total = len(self.results)

        print(f"\nTest Summary: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All quick tests passed!")
            return 0
        else:
            print("❌ Some tests failed:")
            for name, success, error in self.results:
                if not success:
                    print(f"  - {name}: {error}")
            return 1


def main():
    """Main test runner."""
    # Parse arguments manually to avoid conflicts with launch.py
    quick = '--quick' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    unittest_mode = '--unittest' in sys.argv

    class Args:
        def __init__(self):
            self.quick = quick
            self.verbose = verbose
            self.unittest = unittest_mode

    args = Args()

    if args.quick:
        # Run quick tests
        runner = QuickTestRunner(verbose=args.verbose)
        return runner.run_quick_tests()

    elif args.unittest:
        # Run full unittest
        if args.verbose:
            verbosity = 2
        else:
            verbosity = 1

        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(LaunchPyTest)
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)

        return 0 if result.wasSuccessful() else 1

    else:
        # Run both quick and unittest
        print("Running comprehensive launch.py tests...\n")

        # Quick tests first
        print("Phase 1: Quick Tests")
        print("-" * 30)
        runner = QuickTestRunner(verbose=args.verbose)
        quick_result = runner.run_quick_tests()

        print("\nPhase 2: Unit Tests")
        print("-" * 30)

        # Unit tests
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(LaunchPyTest)
        runner = unittest.TextTestRunner(verbosity=1)
        unit_result = runner.run(suite)

        overall_success = quick_result == 0 and unit_result.wasSuccessful()
        return 0 if overall_success else 1


if __name__ == "__main__":
    sys.exit(main())