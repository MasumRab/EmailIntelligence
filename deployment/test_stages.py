"""
Test stages for the EmailIntelligence application.
"""
import subprocess
import sys
from pathlib import Path

# Assuming the script is at /app/deployment/test_stages.py
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
    # Fallback to system python if venv not found, though it should exist
    # when run via launch.py
    return sys.executable


def _run_pytest(test_path: str, coverage: bool, debug: bool) -> bool:
    """Helper function to run pytest."""
    python_exe = get_python_executable()
    cmd = [python_exe, "-m", "pytest", test_path]
    if coverage:
        # Adjusting cov path to be more specific if needed
        cmd.extend(["--cov=backend", "--cov-report=term-missing"])
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
    """Container for test stage functions."""
    def run_unit_tests(self, coverage: bool, debug: bool) -> bool:
        """Runs unit tests."""
        print("\n--- Running Unit Tests ---")
        # Assuming all tests under backend/ are unit/integration for now
        # and can be run together.
        success = _run_pytest("backend/", coverage, debug)
        print(f"--- Unit Test Result: {'SUCCESS' if success else 'FAILURE'} ---")
        return success

    def run_integration_tests(self, coverage: bool, debug: bool) -> bool:
        """Runs integration tests."""
        print("\n--- Running Integration Tests ---")
        # Currently, no separate integration tests. We can add a marker later.
        print("No separate integration tests configured. Skipping.")
        return True

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

    def run_security_tests(self, api_url: str, debug: bool) -> bool:
        """Runs security tests."""
        print("\n--- Running Security Tests ---")
        print("No security tests configured. Skipping.")
        return True

# This is the object the launcher will import and use.
test_stages = TestStages()
import logging

logger = logging.getLogger(__name__)

class TestStages:
    """A class to encapsulate test stage runners."""
    def run_unit_tests(self, coverage: bool, debug: bool) -> bool:
        """Placeholder for running unit tests."""
        logger.info("Placeholder: Running unit tests...")
        return True

    def run_integration_tests(self, coverage: bool, debug: bool) -> bool:
        """Placeholder for running integration tests."""
        logger.info("Placeholder: Running integration tests...")
        return True

    def run_e2e_tests(self, headless: bool, debug: bool) -> bool:
        """Placeholder for running end-to-end tests."""
        logger.info("Placeholder: Running end-to-end tests...")
        return True

    def run_performance_tests(self, duration: int, users: int, debug: bool) -> bool:
        """Placeholder for running performance tests."""
        logger.info("Placeholder: Running performance tests...")
        return True

    def run_security_tests(self, target_url: str, debug: bool) -> bool:
        """Placeholder for running security tests."""
        logger.info("Placeholder: Running security tests...")
        return True

# The launch script expects to import this specific object.
test_stages = TestStages()