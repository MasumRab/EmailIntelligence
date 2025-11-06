"""
Core security functionalities for the Email Intelligence Platform.
This module includes input validation, data sanitization, and other
security-related utilities to protect against common vulnerabilities.
"""

import logging
import os
import re
from typing import Any, Dict, List

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
