#!/usr/bin/env python3
"""
Test Stages Module for EmailIntelligence

This module provides functions for testing different stages of the application,
including unit tests, integration tests, and end-to-end tests.
"""

import os
import sys
import subprocess
import logging
import time
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

# Import environment manager
from deployment.env_manager import env_manager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("test-stages")

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

class TestStages:
    """Manages testing for different stages of the application."""
    
    def __init__(self, root_dir: Path = ROOT_DIR):
        """Initialize the test stages manager."""
        self.root_dir = root_dir
        self.env_manager = env_manager
    
    def run_unit_tests(self, coverage: bool = False, verbose: bool = False) -> bool:
        """Run unit tests."""
        logger.info("Running unit tests...")
        
        # Ensure test dependencies are installed
        if not self.env_manager.setup_environment_for_stage("test"):
            return False
        
        # Build command
        python = self.env_manager.get_python_executable()
        cmd = [python, "-m", "pytest", "tests/"]
        
        if coverage:
            cmd.extend(["--cov=server", "--cov-report=term", "--cov-report=html"])
        
        if verbose:
            cmd.append("-v")
        
        # Run tests
        try:
            subprocess.check_call(cmd)
            logger.info("Unit tests completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Unit tests failed with exit code {e.returncode}")
            return False
    
    def run_integration_tests(self, coverage: bool = False, verbose: bool = False) -> bool:
        """Run integration tests."""
        logger.info("Running integration tests...")
        
        # Ensure test dependencies are installed
        if not self.env_manager.setup_environment_for_stage("test"):
            return False
        
        # Build command
        python = self.env_manager.get_python_executable()
        cmd = [python, "-m", "pytest", "tests/integration/"]
        
        if coverage:
            cmd.extend(["--cov=server", "--cov-report=term", "--cov-report=html"])
        
        if verbose:
            cmd.append("-v")
        
        # Run tests
        try:
            subprocess.check_call(cmd)
            logger.info("Integration tests completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Integration tests failed with exit code {e.returncode}")
            return False
    
    def run_e2e_tests(self, headless: bool = True, verbose: bool = False) -> bool:
        """Run end-to-end tests."""
        logger.info("Running end-to-end tests...")
        
        # Ensure test dependencies are installed
        if not self.env_manager.setup_environment_for_stage("test"):
            return False
        
        # Check if Playwright is installed
        python = self.env_manager.get_python_executable()
        try:
            subprocess.check_call([python, "-c", "import playwright"])
        except subprocess.CalledProcessError:
            logger.info("Playwright not found, installing...")
            try:
                subprocess.check_call([python, "-m", "pip", "install", "playwright"])
                subprocess.check_call([python, "-m", "playwright", "install"])
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install Playwright: {e}")
                return False
        
        # Build command
        cmd = [python, "-m", "pytest", "tests/e2e/"]
        
        if headless:
            cmd.append("--headless")
        
        if verbose:
            cmd.append("-v")
        
        # Run tests
        try:
            subprocess.check_call(cmd)
            logger.info("End-to-end tests completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"End-to-end tests failed with exit code {e.returncode}")
            return False
    
    def run_api_tests(self, verbose: bool = False) -> bool:
        """Run API tests."""
        logger.info("Running API tests...")
        
        # Ensure test dependencies are installed
        if not self.env_manager.setup_environment_for_stage("test"):
            return False
        
        # Build command
        python = self.env_manager.get_python_executable()
        cmd = [python, "-m", "pytest", "tests/api/"]
        
        if verbose:
            cmd.append("-v")
        
        # Run tests
        try:
            subprocess.check_call(cmd)
            logger.info("API tests completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"API tests failed with exit code {e.returncode}")
            return False
    
    def run_performance_tests(self, duration: int = 60, users: int = 10, verbose: bool = False) -> bool:
        """Run performance tests."""
        logger.info(f"Running performance tests with {users} users for {duration} seconds...")
        
        # Ensure test dependencies are installed
        if not self.env_manager.setup_environment_for_stage("test"):
            return False
        
        # Check if Locust is installed
        python = self.env_manager.get_python_executable()
        try:
            subprocess.check_call([python, "-c", "import locust"])
        except subprocess.CalledProcessError:
            logger.info("Locust not found, installing...")
            try:
                subprocess.check_call([python, "-m", "pip", "install", "locust"])
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install Locust: {e}")
                return False
        
        # Build command
        cmd = [
            python, "-m", "locust",
            "-f", "tests/performance/locustfile.py",
            "--headless",
            "-u", str(users),
            "-r", "1",
            "-t", f"{duration}s",
            "--host", "http://localhost:8000"
        ]
        
        if verbose:
            cmd.append("--verbose")
        
        # Run tests
        try:
            subprocess.check_call(cmd)
            logger.info("Performance tests completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Performance tests failed with exit code {e.returncode}")
            return False
    
    def run_security_tests(self, target: str = "http://localhost:8000", verbose: bool = False) -> bool:
        """Run security tests."""
        logger.info(f"Running security tests against {target}...")
        
        # Ensure test dependencies are installed
        if not self.env_manager.setup_environment_for_stage("test"):
            return False
        
        # Check if OWASP ZAP is installed
        python = self.env_manager.get_python_executable()
        try:
            subprocess.check_call([python, "-c", "import zapv2"])
        except subprocess.CalledProcessError:
            logger.info("OWASP ZAP Python API not found, installing...")
            try:
                subprocess.check_call([python, "-m", "pip", "install", "python-owasp-zap-v2.4"])
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install OWASP ZAP Python API: {e}")
                return False
        
        # Build command for custom security test script
        cmd = [
            python,
            str(self.root_dir / "tests" / "security" / "run_security_tests.py"),
            "--target", target
        ]
        
        if verbose:
            cmd.append("--verbose")
        
        # Run tests
        try:
            subprocess.check_call(cmd)
            logger.info("Security tests completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Security tests failed with exit code {e.returncode}")
            return False
    
    def run_all_tests(self, coverage: bool = False, verbose: bool = False) -> bool:
        """Run all tests."""
        logger.info("Running all tests...")
        
        # Run unit tests
        if not self.run_unit_tests(coverage, verbose):
            logger.warning("Unit tests failed")
        
        # Run integration tests
        if not self.run_integration_tests(coverage, verbose):
            logger.warning("Integration tests failed")
        
        # Run API tests
        if not self.run_api_tests(verbose):
            logger.warning("API tests failed")
        
        # Run end-to-end tests
        if not self.run_e2e_tests(True, verbose):
            logger.warning("End-to-end tests failed")
        
        logger.info("All tests completed")
        return True
    
    def run_tests_for_stage(self, stage: str, coverage: bool = False, verbose: bool = False) -> bool:
        """Run tests for a specific stage."""
        if stage == "dev":
            return self.run_unit_tests(coverage, verbose)
        elif stage == "test":
            return self.run_all_tests(coverage, verbose)
        elif stage == "staging":
            return self.run_integration_tests(coverage, verbose) and self.run_api_tests(verbose)
        elif stage == "prod":
            return self.run_e2e_tests(True, verbose)
        else:
            logger.error(f"Unknown stage: {stage}")
            return False

# Create a singleton instance
test_stages = TestStages()

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test Stages for EmailIntelligence")
    
    # Test type arguments
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--api", action="store_true", help="Run API tests")
    parser.add_argument("--e2e", action="store_true", help="Run end-to-end tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    # Test configuration
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--stage", choices=["dev", "test", "staging", "prod"], help="Run tests for a specific stage")
    
    # Performance test configuration
    parser.add_argument("--duration", type=int, default=60, help="Duration of performance tests in seconds")
    parser.add_argument("--users", type=int, default=10, help="Number of users for performance tests")
    
    # Security test configuration
    parser.add_argument("--target", type=str, default="http://localhost:8000", help="Target URL for security tests")
    
    return parser.parse_args()

def main() -> int:
    """Main entry point."""
    # Parse arguments
    args = parse_arguments()
    
    # Determine which tests to run
    if args.stage:
        return 0 if test_stages.run_tests_for_stage(args.stage, args.coverage, args.verbose) else 1
    
    if args.all:
        return 0 if test_stages.run_all_tests(args.coverage, args.verbose) else 1
    
    # Run specific tests
    success = True
    
    if args.unit:
        success = test_stages.run_unit_tests(args.coverage, args.verbose) and success
    
    if args.integration:
        success = test_stages.run_integration_tests(args.coverage, args.verbose) and success
    
    if args.api:
        success = test_stages.run_api_tests(args.verbose) and success
    
    if args.e2e:
        success = test_stages.run_e2e_tests(True, args.verbose) and success
    
    if args.performance:
        success = test_stages.run_performance_tests(args.duration, args.users, args.verbose) and success
    
    if args.security:
        success = test_stages.run_security_tests(args.target, args.verbose) and success
    
    # If no specific tests were requested, run unit tests by default
    if not (args.unit or args.integration or args.api or args.e2e or args.performance or args.security or args.all or args.stage):
        success = test_stages.run_unit_tests(args.coverage, args.verbose)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())