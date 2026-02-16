"""
Test stages for the EmailIntelligence application.

This module provides test execution stages that can be run via the launch.py script.
It assumes that the Python virtual environment is already set up and activated externally.
The launch.py script handles environment setup before calling these test stages.
"""

import logging
import subprocess
import sys
from pathlib import Path

# Import utils for python executable detection
try:
    from setup.utils import get_python_executable
except ImportError:
    def get_python_executable():
        return sys.executable

logger = logging.getLogger(__name__)

# Global paths
ROOT_DIR = Path(__file__).resolve().parent.parent


def _run_pytest(test_path: str, coverage: bool, debug: bool) -> bool:
    """Helper function to run pytest."""
    python_exe = get_python_executable()
    cmd = [python_exe, "-m", "pytest"] + test_path.split()

    if coverage:
        cmd.extend(["--cov=src", "--cov-report=term-missing"])
    if debug:
        cmd.append("-vv")

    print(f"Running command: {' '.join(cmd)}")
    try:
        # Run from the project's root directory to ensure all modules are found
        result = subprocess.run(cmd, check=True, cwd=ROOT_DIR, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:\n", result.stderr)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Pytest execution failed with return code {e.returncode}")
        print("Stdout:\n", e.stdout)
        print("Stderr:\n", e.stderr)
        return False
    except FileNotFoundError:
        print(f"Error: Python executable not found at {python_exe}")
        return False


class TestStages:
    """A class to encapsulate test stage runners."""

    def run_unit_tests(self, coverage: bool, debug: bool) -> bool:
        """Runs unit tests."""
        print("\n--- Running Unit Tests ---")
        # Run unit tests in tests directory
        success = _run_pytest("tests/", coverage, debug)
        print(f"--- Unit Test Result: {'SUCCESS' if success else 'FAILURE'} ---")
        return success

    def run_integration_tests(self, coverage: bool, debug: bool) -> bool:
        """Runs integration tests."""
        print("\n--- Running Integration Tests ---")
        # Run integration tests with marker
        success = _run_pytest("tests/ -m integration", coverage, debug)
        print(f"--- Integration Test Result: {'SUCCESS' if success else 'FAILURE'} ---")
        return success

    def run_e2e_tests(self, headless: bool, debug: bool) -> bool:
        """Runs end-to-end tests."""
        print("\n--- Running E2E Tests ---")
        print("No E2E tests configured. Skipping.")
        return True

    def run_performance_tests(self, duration: int, users: int, debug: bool) -> bool:
        """Runs performance tests."""
        print("\n--- Running Performance Tests ---")
        print("No performance tests configured. Skipping.")
        return True

    def run_security_tests(self, target_url: str, debug: bool) -> bool:
        """Runs security tests."""
        print("\n--- Running Security Tests ---")
        print("No security tests configured. Skipping.")
        return True

# Global instance
test_stages = TestStages()


def handle_test_stage(args):
    """Handles the test stage execution."""
    logger.info("Starting test stage...")
    results = []

    # Check if any specific test type is selected
    specific_tests = any([
        getattr(args, 'unit', False),
        getattr(args, 'integration', False),
        getattr(args, 'e2e', False),
        getattr(args, 'performance', False),
        getattr(args, 'security', False)
    ])

    if getattr(args, 'unit', False):
        results.append(test_stages.run_unit_tests(getattr(args, 'coverage', False), getattr(args, 'debug', False)))
    if getattr(args, 'integration', False):
        results.append(test_stages.run_integration_tests(getattr(args, 'coverage', False), getattr(args, 'debug', False)))
    if getattr(args, 'e2e', False):
        results.append(test_stages.run_e2e_tests(headless=not getattr(args, 'debug', False), debug=getattr(args, 'debug', False)))
    if getattr(args, 'performance', False):
        results.append(test_stages.run_performance_tests(duration=300, users=10, debug=getattr(args, 'debug', False)))
    if getattr(args, 'security', False):
        results.append(
            test_stages.run_security_tests(
                target_url=f"http://{getattr(args, 'host', 'localhost')}:{getattr(args, 'port', 8000)}",
                debug=getattr(args, 'debug', False)
            )
        )

    # If no specific test type is selected, run defaults (unit + integration)
    if not specific_tests:
        logger.info("No specific test type selected, running unit and integration tests.")
        results.append(test_stages.run_unit_tests(getattr(args, 'coverage', False), getattr(args, 'debug', False)))
        results.append(test_stages.run_integration_tests(getattr(args, 'coverage', False), getattr(args, 'debug', False)))

    if all(results):
        logger.info("All tests passed successfully.")
        return 0
    else:
        logger.error("Some tests failed.")
        return 1
