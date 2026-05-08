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

logger = logging.getLogger(__name__)

# Assuming the script is at /app/setup/test_stages.py
# ROOT_DIR will be /app
ROOT_DIR = Path(__file__).resolve().parent.parent


def get_python_executable() -> str:
    """Get the Python executable path from the venv."""
    venv_path = ROOT_DIR / "venv"
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"

    if python_exe.exists():
        return str(python_exe)
    # Fallback to system python if venv not found
    return sys.executable


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
        # Run unit tests in tests/core and tests/modules
        success = _run_pytest("tests/core tests/modules", coverage, debug)
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

# The launch script expects to import this specific object.
test_stages = TestStages()


def handle_test_stage(args):
    """Handle test stage execution based on provided arguments."""
    if getattr(args, "unit", False):
        test_stages.run_unit_tests(getattr(args, "coverage", False), getattr(args, "debug", False))
    
    if getattr(args, "integration", False):
        test_stages.run_integration_tests(getattr(args, "coverage", False), getattr(args, "debug", False))
        
    if getattr(args, "e2e", False):
        test_stages.run_e2e_tests(True, getattr(args, "debug", False))
        
    if getattr(args, "performance", False):
        test_stages.run_performance_tests(60, 10, getattr(args, "debug", False))
        
    if getattr(args, "security", False):
        test_stages.run_security_tests("http://localhost:8000", getattr(args, "debug", False))

    if args.stage == "test" and not any([args.unit, args.integration, args.e2e, args.performance, args.security]):
        # Default to running unit and integration tests if in test stage and no specific test type selected
        test_stages.run_unit_tests(getattr(args, "coverage", False), getattr(args, "debug", False))
        test_stages.run_integration_tests(getattr(args, "coverage", False), getattr(args, "debug", False))
