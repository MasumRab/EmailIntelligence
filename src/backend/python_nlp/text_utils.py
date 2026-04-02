"""
Text utility functions for NLP processing.
"""

import re


def clean_text(text: str | None) -> str:
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
    text = re.sub(r"\s+", " ", text.strip())

    # Remove special characters but keep basic punctuation
    text = re.sub(r"[^\w\s.,!?-]", "", text)

    return text
