"""
Validation utilities for EmailIntelligence launcher.
"""

import logging
import platform
import sys
from pathlib import Path

# Import project configuration
from setup.project_config import get_project_config

logger = logging.getLogger("launcher")

# Constants
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 13)

# Get root directory
ROOT_DIR = get_project_config().root_dir


def check_python_version():
    """Check if the current Python version is compatible."""
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.error(
            f"Python version {platform.python_version()} is not compatible. "
            f"Please use Python version {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} "
            f"to {PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}."
        )
        sys.exit(1)
    logger.info(f"Python version {platform.python_version()} is compatible.")


def check_for_merge_conflicts() -> bool:
    """Check for unresolved merge conflict markers in critical files."""
    conflict_markers = ["<<<<<<< ", "======= ", ">>>>>>> "]

    # Get critical files from project configuration
    config = get_project_config()
    # Try to use config, fallback to list if method missing
    try:
        critical_files = config.get_critical_files()
    except AttributeError:
        # Fallback list if config doesn't support it yet
        critical_files = [
            "src/main.py",
            "setup/launch.py",
            "pyproject.toml",
            "README.md",
        ]

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
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        issues.append(
            f"Python version {current_version} is not compatible. Required: {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}-{PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}"
        )

    # Check key directories
    required_dirs = ["src", "tests"] # Updated for new structure
    for dir_name in required_dirs:
        if not (ROOT_DIR / dir_name).exists():
            issues.append(f"Required directory '{dir_name}' is missing.")

    # Check key files
    required_files = ["pyproject.toml", "README.md"]
    for file_name in required_files:
        if not (ROOT_DIR / file_name).exists():
            issues.append(f"Required file '{file_name}' is missing.")

    if issues:
        for issue in issues:
            logger.error(issue)
        return False

    logger.info("All required components are present.")
    return True


def validate_environment() -> bool:
    """Run comprehensive environment validation."""
    logger.info("Running environment validation...")

    if not check_for_merge_conflicts():
        return False

    if not check_required_components():
        return False

    logger.info("Environment validation passed.")
    return True


def validate_port(port: int) -> int:
    """Validate and return a valid port number."""
    if not isinstance(port, int) or port < 1 or port > 65535:
        raise ValueError(f"Invalid port number: {port}. Must be between 1 and 65535.")
    return port


def validate_host(host: str) -> str:
    """Validate and return a valid host address."""
    if not host or not isinstance(host, str):
        raise ValueError(f"Invalid host: {host}")
    return host


def check_critical_files() -> bool:
    """Check for critical files that must exist in the orchestration-tools branch."""
    # Critical files that are essential for orchestration
    critical_files = [
        "setup/launch.py",
        "setup/pyproject.toml",
        "launch.py",
    ]

    missing_files = []

    for file_path in critical_files:
        full_path = ROOT_DIR / file_path
        if not full_path.exists():
            missing_files.append(file_path)

    if missing_files:
        logger.error("Missing critical files:")
        for file_path in missing_files:
            logger.error(f"  - {file_path}")
        return False

    logger.info("All critical files are present.")
    return True


def validate_orchestration_environment() -> bool:
    """Run comprehensive validation for the orchestration-tools branch."""
    logger.info("Running orchestration environment validation...")

    # Check for merge conflicts first
    if not check_for_merge_conflicts():
        return False

    # Check critical files
    if not check_critical_files():
        return False

    logger.info("Orchestration environment validation passed.")
    return True
