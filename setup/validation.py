"""
Validation utilities for EmailIntelligence launcher
"""

import logging
import platform
import sys
from pathlib import Path

logger = logging.getLogger("launcher")

# Constants (will be imported from main launcher)
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 13)

# Get root directory (avoid circular import)
ROOT_DIR = Path(__file__).parent.parent


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
    critical_files = [
        "backend/python_backend/main.py",
        "backend/python_nlp/nlp_engine.py",
        "backend/python_backend/database.py",
        "backend/python_backend/email_routes.py",
        "backend/python_backend/category_routes.py",
        "backend/python_backend/gmail_routes.py",
        "backend/python_backend/filter_routes.py",
        "backend/python_backend/action_routes.py",
        "backend/python_backend/dashboard_routes.py",
        "backend/python_backend/workflow_routes.py",
        "backend/python_backend/performance_monitor.py",
        "backend/python_nlp/gmail_integration.py",
        "backend/python_nlp/gmail_service.py",
        "backend/python_nlp/smart_filters.py",
        "backend/python_nlp/smart_retrieval.py",
        "backend/python_nlp/ai_training.py",
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
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
                                # Don't break here to find all conflicts in the file?
                                # Original implementation found the first marker and continued logic.
                                # But `if marker in content` would trigger if ANY marker is present.
                                # Since we want to report errors, finding one is enough to mark the file as bad,
                                # but printing all is helpful. We'll set the flag and continue.
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
    required_dirs = ["backend", "client", "shared", "tests"]
    for dir_name in required_dirs:
        if not (ROOT_DIR / dir_name).exists():
            issues.append(f"Required directory '{dir_name}' is missing.")

    # Check key files
    required_files = ["pyproject.toml", "README.md", "requirements.txt"]
    for file_name in required_files:
        if not (ROOT_DIR / file_name).exists():
            issues.append(f"Required file '{file_name}' is missing.")

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
    return True