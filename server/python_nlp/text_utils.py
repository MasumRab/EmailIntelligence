import re


def clean_text(text: str) -> str:
    """
    Cleans the input text by lowercasing, stripping whitespace,
    and normalizing punctuation.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = text.strip()
    # Normalize punctuation by removing or replacing unwanted characters
    text = re.sub(r"[^a-zA-Z0-9\s.,?!']", "", text)  # Keep basic punctuation
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace
    return text
