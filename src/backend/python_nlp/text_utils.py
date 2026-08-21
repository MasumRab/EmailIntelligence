"""
Text utility functions for NLP processing.
"""

import re
from typing import Optional

_WHITESPACE_RE = re.compile(r"\s+")
_SPECIAL_CHARS_RE = re.compile(r"[^\ws.,!?-]")


def clean_text(text: Optional[str]) -> str:
    """
    Clean and normalize text for NLP processing.

    Args:
        text: Input text to clean

    Returns:
        Cleaned text string
    """
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = _WHITESPACE_RE.sub(" ", text.strip())

    # Remove special characters but keep basic punctuation
    text = _SPECIAL_CHARS_RE.sub("", text)

    return text
