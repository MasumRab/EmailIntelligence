"""
Core security functionalities for the Email Intelligence Platform.
This module includes input validation, data sanitization, and other
security-related utilities to protect against common vulnerabilities.
"""

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)

# --- Constants for Sanitization ---
# Stricter regex for path validation to disallow '..'
SAFE_PATH_REGEX = re.compile(r"^[a-zA-Z0-9._-]+$")

# Regex to detect potentially sensitive key-value pairs in strings
# Looks for common key names followed by variations of separators and the value.
SENSITIVE_KEY_REGEX = re.compile(
    r"""
    (['"]?
    (password|secret|token|api_key|access_key|private_key|key|credentials|auth)
    ['"]?
    \s*[:=]\s*)
    (['"]?
    [^'"\s,}\]]+
    ['"]?)
    """,
    re.IGNORECASE | re.VERBOSE,
)
REDACTED_MESSAGE = "[REDACTED]"


# --- Data Sanitization ---

class DataSanitizer:
    """A class to handle redaction of sensitive data from logs and outputs."""

    def __init__(self, sensitive_keys: List[str] = None, redaction_string: str = REDACTED_MESSAGE):
        """
        Initializes the DataSanitizer with a list of sensitive keys.
        """
        if sensitive_keys is None:
            sensitive_keys = [
                "password", "secret", "token", "api_key",
                "access_key", "private_key", "credentials", "auth"
            ]

        self.sensitive_keys = sensitive_keys
        self.redaction_string = redaction_string
        self.sensitive_key_pattern = self._build_sensitive_key_regex(self.sensitive_keys)

    def _build_sensitive_key_regex(self, keys: List[str]) -> re.Pattern:
        """Builds a regex to find sensitive key-value pairs from a list of keys."""
        key_pattern = "|".join(re.escape(key) for key in keys)

        # Group 1: The entire key part, including separator and opening quote for the value.
        # Group 2: The opening quote for the value, which should be matched at the end.
        return re.compile(
            r"""
            ( # Group 1: Key part up to the value's opening quote
                ['"]?                  # Optional opening quote for the key
                (?:{key_pattern})      # The sensitive key itself
                ['"]?                  # Optional closing quote for the key
                \s*[:=]\s*              # Separator
                (['"]?)                # Group 2: Optional opening quote for the value
            )
            (?:[^\s,'"{{}}]+)          # The value itself (non-capturing group)
            \2                         # Match the same quote as Group 2
            """.format(key_pattern=key_pattern),
            re.IGNORECASE | re.VERBOSE
        )

    def redact(self, data: Any) -> Any:
        """
        Recursively redacts sensitive information from various data structures.
        """
        if isinstance(data, dict):
            return {key: self.redact(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.redact(item) for item in data]
        elif isinstance(data, str):
            return self.redact_string(data)
        return data

    def redact_string(self, text: str) -> str:
        """
        Redacts sensitive key-value pairs from a string.
        """
        def repl(m):
            # m.group(1) is the key part (e.g., 'password": "')
            # m.group(2) is the quote character
            # We replace the whole match with key part + redacted string + closing quote
            return f"{m.group(1)}{self.redaction_string}{m.group(2)}"

        return self.sensitive_key_pattern.sub(repl, text)

# Default instance for convenience
default_sanitizer = DataSanitizer()

def sanitize_data(data: Any) -> Any:
    """
    Sanitizes data by redacting sensitive information using the default sanitizer.
    """
    return default_sanitizer.redact(data)


# --- Input Validation ---

def validate_path_safety(path: str, base_dir: str = None) -> bool:
    """
    Validates a path to prevent directory traversal attacks.
    Ensures the path is within the intended directory and contains no malicious components.

    - Disallows absolute paths.
    - Prevents ".." components to stop directory traversal.
    - If base_dir is provided, ensures the resolved path is within base_dir.
    """
    if not isinstance(path, str) or not path:
        return False

    # 1. Disallow absolute paths
    if os.path.isabs(path):
        logger.warning(f"Path validation failed: Absolute path detected '{path}'")
        return False

    # 2. Check for directory traversal attempts
    if ".." in path.split(os.path.sep):
        logger.warning(f"Path validation failed: Directory traversal attempt in '{path}'")
        return False

    # 3. Normalize the path to resolve any redundant separators
    normalized_path = os.path.normpath(path)

    # 4. If a base directory is provided, check that the path is contained within it
    if base_dir:
        # Ensure base_dir is an absolute path for reliable comparison
        abs_base_dir = os.path.abspath(base_dir)

        # Resolve the full path of the user-provided path relative to the base directory
        full_path = os.path.abspath(os.path.join(abs_base_dir, normalized_path))

        # Check if the resolved path is a subdirectory of the base directory
        if not full_path.startswith(abs_base_dir):
            logger.warning(
                f"Path validation failed: Path '{full_path}' is outside of base directory '{abs_base_dir}'"
            )
            return False

    return True

def sanitize_path(path: str) -> str:
    """
    Sanitizes a path by removing potentially malicious characters and components.
    This is a stronger measure than validation alone, intended to produce a safe
    version of a given path.
    """
    if not isinstance(path, str) or not path:
        return ""

    # Split the path into components
    parts = path.split(os.path.sep)

    # Filter out any dangerous components ('..', '.', etc.)
    safe_parts = [part for part in parts if part and part not in ('.', '..')]

    # Further sanitize each part to remove unsafe characters
    sanitized_parts = [SAFE_PATH_REGEX.sub('', part) for part in safe_parts]

    # Rejoin the sanitized parts
    return os.path.join(*sanitized_parts)

def validate_email_format(email: str) -> bool:
    """
    Validates if a string is a correctly formatted email address.
    """
    # A simple but effective regex for email validation
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    return email_regex.match(email) is not None

def validate_user_input(
    data: Dict[str, Any],
    required_fields: List[str],
    field_validators: Dict[str, callable] = None
) -> List[str]:
    """
    A generic utility to validate user-provided data dictionaries.

    - Checks for the presence of all required fields.
    - Applies specific validation functions to fields if provided.

    Returns a list of validation error messages. An empty list means success.
    """
    errors = []

    # 1. Check for missing required fields
    for field in required_fields:
        if field not in data or data[field] is None:
            errors.append(f"Missing required field: '{field}'")

    if errors:
        return errors  # Return early if required fields are missing

    # 2. Apply custom validators for specific fields
    if field_validators:
        for field, validator in field_validators.items():
            if field in data:
                if not validator(data[field]):
                    errors.append(f"Invalid format for field: '{field}'")

    return errors


class SecurityValidator:
    """
    Consolidated security validator for the Email Intelligence Platform.
    Provides methods for path safety, data sanitization, and I/O gating.
    """

    def __init__(self, base_dir: str = None):
        self.base_dir = base_dir or os.getcwd()

    def validate_io(self, path: str, mode: str = "r") -> bool:
        """
        Validates an I/O operation.
        Returns True if the path is safe, False otherwise.
        """
        return validate_path_safety(path, self.base_dir)

    def sanitize(self, path: str) -> str:
        """Sanitizes a path."""
        return sanitize_path(path)


# --- Missing classes from main ---

class PathValidator:
    """Secure path validation to prevent directory traversal attacks"""

    @staticmethod
    def is_safe_path(
        base_path: Union[str, Path], requested_path: Union[str, Path]
    ) -> bool:
        """
        Check if a requested path is safe (doesn't escape the base directory)

        Args:
            base_path: The base directory that should not be escaped
            requested_path: The path to validate

        Returns:
            True if the path is safe, False otherwise
        """
        try:
            base_path = Path(base_path).resolve()
            requested_path = Path(requested_path).resolve()

            # Check if the resolved path starts with the base path
            return requested_path.is_relative_to(base_path)
        except ValueError:
            # If the path is not relative to base (or other path resolution issues)
            return False

    @staticmethod
    def validate_and_resolve_db_path(
        db_path: Union[str, Path], allowed_dir: Optional[Union[str, Path]] = None
    ) -> Path:
        """
        Validate and resolve a database path with security checks

        Args:
            db_path: The database path to validate
            allowed_dir: Optional base directory that the path must be within

        Returns:
            Validated and resolved Path object

        Raises:
            ValueError: If the path is not safe
        """
        if not db_path:
            raise ValueError("Database path cannot be empty")

        # Handle special in-memory database
        if str(db_path) == ":memory:":
            return Path(":memory:")

        path = Path(db_path)

        # Sanitize filename if it's just a filename
        if not path.is_absolute() and len(path.parts) == 1:
            path = Path(PathValidator.sanitize_filename(str(path)))

        # Resolve the path
        try:
            resolved_path = path.resolve()
        except (OSError, RuntimeError) as e:
            raise ValueError(f"Invalid path: {e}")

        # Check against allowed directory if specified
        if allowed_dir:
            allowed_dir = Path(allowed_dir).resolve()
            if not resolved_path.is_relative_to(allowed_dir):
                raise ValueError(
                    f"Database path escapes allowed directory: {allowed_dir}"
                )

        # Additional security checks
        if any(part.startswith(".") for part in resolved_path.parts):
            raise ValueError("Database path contains hidden files/directories")

        return resolved_path

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize a filename by removing dangerous characters

        Args:
            filename: The filename to sanitize

        Returns:
            Sanitized filename
        """
        # Remove any path traversal attempts and dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)

        # Also avoid names that might be problematic on various systems
        if sanitized.upper() in [
            "CON",
            "PRN",
            "AUX",
            "NUL",
        ] or sanitized.upper().startswith(("COM", "LPT")):
            sanitized = f"_{sanitized}"

        return sanitized


def secure_path_join(
    base_dir: Union[str, Path], *paths: Union[str, Path]
) -> Optional[Path]:
    """
    Securely join paths, preventing directory traversal attacks.

    Args:
        base_dir: Base directory
        *paths: Path components to join

    Returns:
        Joined path if safe, None otherwise
    """
    import pathlib  # Already imported at module level as Path

    try:
        # Start with base directory
        result_path = pathlib.Path(base_dir).resolve()

        # Join each path component securely
        for path_component in paths:
            if not validate_path_safety(path_component, str(result_path)):
                return None
            result_path = (result_path / path_component).resolve()

        return result_path
    except (OSError, RuntimeError, ValueError):
        return None
