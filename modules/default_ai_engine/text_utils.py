"""
Text Processing Utilities for NLP.

This module provides common utility functions for cleaning and normalizing
text data, preparing it for natural language processing tasks.
"""

import re


def clean_text(text: str) -> str:
    """
    Cleans input text by lowercasing, stripping, and normalizing whitespace.

    This function performs a series of basic cleaning operations to produce a
    more uniform text representation for NLP analysis.

    Args:
        text: The input string to be cleaned.

    Returns:
        The cleaned and normalized string. Returns an empty string if the
        input is not a string.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.strip()
    text = re.sub(r"[^a-zA-Z0-9\s.,?!']", "", text)
    text = re.sub(r"\s+", " ", text)
    return text
