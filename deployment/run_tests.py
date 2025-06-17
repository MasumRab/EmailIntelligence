#!/usr/bin/env python3
"""
Test Runner Script for EmailIntelligence

This script acts as a frontend to test_stages.py, forwarding all command-line
arguments to it. It is responsible for setting up the command execution
environment and invoking test_stages.py.

Usage:
    python run_tests.py [arguments_for_test_stages.py]
    Example: python run_tests.py --unit --coverage
"""

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("run-tests")

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


def run_command(
    command_list: List[str], cwd: Optional[str] = None, timeout: Optional[int] = None
) -> bool:
    """Run a command and log the output."""
    logger.info(f"Running command: {' '.join(command_list)}")
    try:
        result = subprocess.run(
            command_list,
            check=True,
            text=True,
            capture_output=True,  # Capture output to log it
            cwd=cwd or str(PROJECT_ROOT),
            timeout=timeout,
        )
        if result.stdout:
            logger.info(f"Command STDOUT:\n{result.stdout}")
        if (
            result.stderr
        ):  # Should be empty if check=True and no error, but log if present
            logger.warning(f"Command STDERR:\n{result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Command '{' '.join(e.cmd)}' failed with exit code {e.returncode}"
        )
        if e.stdout:
            logger.error(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            logger.error(f"STDERR:\n{e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        logger.error(f"Command timed out: {' '.join(command_list)}")
        return False
    except FileNotFoundError:
        logger.error(
            f"Command not found: {command_list[0]}. Please ensure it is installed and in PATH."
        )
        return False


def run_unit_tests(coverage=False, verbose=False, timeout_seconds=900):
    """Run unit tests."""
    logger.info("Running unit tests...")

    command = f"{sys.executable} -m pytest tests/"

    if coverage:
        command += " --cov=server"

    if verbose:
        command += " -v"

    return run_command(command, timeout=timeout_seconds)


def run_integration_tests(coverage=False, verbose=False, timeout_seconds=900):
    """Run integration tests."""
    logger.info("Running integration tests...")

    command = f"{sys.executable} -m pytest tests/"

    if coverage:
        command += " --cov=server"

    if verbose:
        command += " -v"

    return run_command(command, timeout=timeout_seconds)


def run_e2e_tests(verbose=False, timeout_seconds=1800):
    """Run end-to-end tests."""
    logger.info("Running end-to-end tests...")

    command = "npx playwright test"

    if verbose:
        command += " --debug"

    return run_command(command, timeout=timeout_seconds)


def main():
    """Main entry point for the test runner script."""

    # Construct the command list to call test_stages.py
    # It will be executed with the same Python interpreter as this script
    command_to_forward = [
        sys.executable,
        str(PROJECT_ROOT / "deployment" / "test_stages.py"),
    ]

    # Append all arguments passed to this script (run_tests.py)
    # These arguments will be interpreted by test_stages.py
    command_to_forward.extend(sys.argv[1:])

    logger.info(f"Forwarding command to test_stages.py: {' '.join(command_to_forward)}")

    success = run_command(command_to_forward)

    # Exit with appropriate status code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
