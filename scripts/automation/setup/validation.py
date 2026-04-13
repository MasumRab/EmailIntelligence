"""
Validation functions for the EmailIntelligence launch system.

This module handles validation of environment, components, and configuration.
"""

import logging
import platform
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from scripts.automation.setup.project_config import get_project_config

logger = logging.getLogger("launcher")

# Global paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Version requirements
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 13)


def check_python_version() -> bool:
    """Check if the current Python version is compatible."""
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.error(
            f"Python version {platform.python_version()} is not compatible. "
            f"Please use Python version {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} "
            f"to {PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}."
        )
        return False
    logger.info(f"Python version {platform.python_version()} is compatible.")
    return True


def check_for_merge_conflicts() -> bool:
    """Check for unresolved merge conflict markers in critical files."""
    conflict_markers = ["<<<<<<< ", "======= ", ">>>>>>> "]

    # Get critical files from project configuration
    config = get_project_config()
    critical_files = config.get_critical_files()

    # Add additional files that aren't automatically discovered
    additional_files = ["README.md", "requirements-dev.txt", "pyproject.toml", "package.json"]
    for f in additional_files:
        if f not in critical_files:
            critical_files.append(f)

    conflicts_found = False
    for file_path in critical_files:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    # Optimized to read line-by-line instead of loading entire file
                    for line_num, line in enumerate(f, 1):
                        for marker in conflict_markers:
                            if marker in line:
                                logger.error(
                                    f"Unresolved merge conflict detected in {file_path} at line {line_num} with marker: {marker.strip()}"
                                )
                                conflicts_found = True
            except Exception as e:
                logger.warning(f"Could not check {file_path} for conflicts: {e}")

    if conflicts_found:
        logger.error("Please resolve all merge conflicts before proceeding.")
        return False

    logger.info("No unresolved merge conflicts detected in critical files.")
    return True


def check_required_components() -> bool:
    """Check for required components and configurations."""
    issues = []

    # Check Python version
    if not check_python_version():
        issues.append(f"Python version is not compatible.")

    # Get project configuration and validate structure
    config = get_project_config()
    structure_issues = config.validate_structure()
    issues.extend(structure_issues)

    # Check key directories explicitly
    required_dirs = ["backend", "client", "shared", "tests"]
    for dir_name in required_dirs:
        if not (ROOT_DIR / dir_name).exists():
            issues.append(f"Required directory '{dir_name}' is missing.")

    # Check AI models directory
    models_dir = ROOT_DIR / "models"
    if not models_dir.exists():
        logger.warning("AI models directory not found. Creating it...")
        try:
            models_dir.mkdir(parents=True, exist_ok=True)
            logger.info("AI models directory created successfully.")
        except Exception as e:
            logger.error(f"Failed to create models directory: {e}")
            issues.append("Failed to create models directory")

    if issues:
        logger.error("Component validation failed:")
        for issue in issues:
            logger.error(f"  - {issue}")
        return False

    logger.info("All required components are present.")
    return True


def validate_environment() -> bool:
    """Run comprehensive environment validation."""
    logger.info("Running environment validation...")

    checks = [
        check_python_version,
        check_for_merge_conflicts,
        check_required_components,
    ]

    all_passed = True
    for check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            logger.error(f"Validation check {check_func.__name__} failed: {e}")
            all_passed = False

    if all_passed:
        logger.info("Environment validation passed.")
    else:
        logger.error("Environment validation failed.")

    return all_passed


def validate_port(port: int) -> bool:
    """Validate that a port number is valid and available."""
    if not isinstance(port, int) or not (1 <= port <= 65535):
        logger.error(f"Invalid port number: {port}. Port must be between 1 and 65535.")
        return False
    return True


def validate_host(host: str) -> bool:
    """Validate that a host string is valid."""
    if not host or not isinstance(host, str):
        logger.error(f"Invalid host: {host}")
        return False
    # Basic validation - could be enhanced with regex
    return True
