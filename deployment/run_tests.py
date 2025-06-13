#!/usr/bin/env python3
"""
Test Runner Script for EmailIntelligence

This script helps run tests for the EmailIntelligence project.
It supports unit tests, integration tests, and end-to-end tests.

Usage:
    python run_tests.py [--unit] [--integration] [--e2e] [--coverage] [--verbose]
"""

import argparse
import os
import subprocess
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("run-tests")

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

def run_command(command, cwd=None):
    """Run a shell command and log the output."""
    logger.info(f"Running command: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=False,  # Show output in real-time
            cwd=cwd or str(PROJECT_ROOT)
        )
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        return False

def run_unit_tests(coverage=False, verbose=False):
    """Run unit tests."""
    logger.info("Running unit tests...")
    
    command = f"{sys.executable} -m pytest tests/"
    
    if coverage:
        command += " --cov=server"
    
    if verbose:
        command += " -v"
    
    return run_command(command)

def run_integration_tests(coverage=False, verbose=False):
    """Run integration tests."""
    logger.info("Running integration tests...")
    
    command = f"{sys.executable} -m pytest tests/integration/"
    
    if coverage:
        command += " --cov=server"
    
    if verbose:
        command += " -v"
    
    return run_command(command)

def run_e2e_tests(verbose=False):
    """Run end-to-end tests."""
    logger.info("Running end-to-end tests...")
    
    command = "npx playwright test"
    
    if verbose:
        command += " --debug"
    
    return run_command(command)

def main():
    """Main entry point for the test runner script."""
    parser = argparse.ArgumentParser(description="Test Runner Script for EmailIntelligence")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    # If no test type is specified, run all tests
    run_all = not (args.unit or args.integration or args.e2e)
    
    # Set up environment variables
    os.environ["PYTHONPATH"] = str(PROJECT_ROOT)
    os.environ["NODE_ENV"] = "test"
    
    # Run tests
    success = True
    
    if args.unit or run_all:
        if not run_unit_tests(args.coverage, args.verbose):
            success = False
    
    if args.integration or run_all:
        if not run_integration_tests(args.coverage, args.verbose):
            success = False
    
    if args.e2e or run_all:
        if not run_e2e_tests(args.verbose):
            success = False
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()