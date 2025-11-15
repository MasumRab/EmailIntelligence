"""
Validation functions for the launch system.

This module handles validation of environment, components, and configuration.
"""

import logging
import sys
from pathlib import Path

from setup.project_config import get_project_config

logger = logging.getLogger(__name__)

# Global paths
ROOT_DIR = Path(__file__).resolve().parent.parent

# Version requirements
PYTHON_MIN_VERSION = (3, 11)
PYTHON_MAX_VERSION = (3, 12)


def check_python_version():
    """Check if Python version is compatible."""
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.error(
            f"Python version {current_version} is not compatible. "
            f"Required: {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}-"
            f"{PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}"
        )
        sys.exit(1)
    logger.info(f"Python version {current_version} is compatible.")


def check_for_merge_conflicts() -> bool:
    """Check for unresolved merge conflict markers in critical files."""
    conflict_markers = ["<<<<<<< ", "======= ", ">>>>>>> "]

    # Get critical files from project configuration
    config = get_project_config()
    critical_files = config.get_critical_files()

    # Add additional files that aren't automatically discovered
    additional_files = ["README.md", "requirements-dev.txt"]
    critical_files.extend(additional_files)

    conflicts_found = False
    for file_path in critical_files:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for marker in conflict_markers:
                        if marker in content:
                            logger.error(
                                f"Unresolved merge conflict detected in {file_path} with marker: {marker.strip()}"
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

    # Get project configuration and validate structure
    config = get_project_config()
    structure_issues = config.validate_structure()
    issues.extend(structure_issues)

    # Check AI models directory
    models_dir = ROOT_DIR / "models"
    if not models_dir.exists():
        logger.warning("AI models directory not found. Creating it...")
        try:
            models_dir.mkdir(parents=True, exist_ok=True)
            logger.info("AI models directory created successfully.")
        except Exception as e:
            issues.append(f"Could not create AI models directory: {e}")

    if issues:
        logger.error("Component validation failed:")
        for issue in issues:
            logger.error(f"  - {issue}")
        return False

    logger.info("All required components are present.")
    return True


def validate_environment() -> bool:
    """Validate the overall environment for running the application."""
    logger.info("Validating environment...")

    checks = [
        check_python_version,
        check_for_merge_conflicts,
        check_required_components,
        check_nltk_compatibility,
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


def validate_port(port: int) -> int:
    """Validate and return a valid port number."""
    if not isinstance(port, int) or port < 1 or port > 65535:
        raise ValueError(f"Invalid port number: {port}. Must be between 1 and 65535.")
    return port


def validate_host(host: str) -> str:
    """Validate and return a valid host address."""
    if not host or not isinstance(host, str):
        raise ValueError(f"Invalid host: {host}")
    # Basic validation - could be enhanced
    return host

def check_nltk_compatibility() -> bool:
    """Check NLTK version compatibility and presence of DownloadError."""
    try:
        import nltk
        from packaging.version import parse as parse_version

        # Check for the specific attribute that caused issues
        if not hasattr(nltk.downloader, 'DownloadError'):
            logger.error(
                "NLTK version is incompatible. 'nltk.downloader.DownloadError' is missing. "
                "Please ensure NLTK version 3.6.5 is installed."
            )
            return False

        # Optionally, check the version directly
        current_nltk_version = parse_version(nltk.__version__)
        required_nltk_version = parse_version("3.6.5")

        if current_nltk_version > required_nltk_version:
            logger.warning(
                f"NLTK version {current_nltk_version} is installed. "
                f"Version 3.6.5 is recommended to avoid potential issues with 'DownloadError'."
            )
            # We return True here because the attribute check passed, but a warning is issued.
            # The user can choose to ignore the warning if their setup works.
            return True

        logger.info(f"NLTK version {current_nltk_version} is compatible.")
        return True

    except ImportError:
        logger.warning("NLTK is not installed. Skipping NLTK compatibility check.")
        return True # NLTK not installed, so no compatibility issue yet
    except Exception as e:
        logger.error(f"An unexpected error occurred during NLTK compatibility check: {e}")
        return False
    # This is a simplified version restored from git history.
    # The original had a much longer list of files.
    critical_files = [
        "scripts/install-hooks.sh",
        "setup/launch.py",
        "setup/pyproject.toml",
        ".pylintrc",
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
        logger.error("Please restore these critical files for proper orchestration functionality.")
        return False

    logger.info("All critical files are present.")
    return True


def validate_orchestration_environment() -> bool:
    """Run comprehensive validation for the orchestration-tools branch."""
    logger.info("Running orchestration environment validation...")
    if not check_for_merge_conflicts():
        return False
    if not check_critical_files():
        return False
    logger.info("Orchestration environment validation passed.")
    return True
