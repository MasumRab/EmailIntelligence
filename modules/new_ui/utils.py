"""
Utility functions for the Email Intelligence Platform
"""

import re
import hashlib
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timezone


def clean_text(text: Optional[str]) -> str:
    """Clean and normalize text for analysis"""
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())

    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)

    return text


def extract_email_address(sender_header: str) -> str:
    """Extract email address from a sender header"""
    if not sender_header:
        return ""

    # Try to extract email from format "Name <email@domain.com>"
    match = re.search(r'<([^>]+)>', sender_header)
    if match:
        return match.group(1).lower()

    # If no angle brackets, assume the whole string is an email
    if '@' in sender_header:
        return sender_header.strip().lower()

    return ""


def extract_domain(email_address: str) -> str:
    """Extract domain from email address"""
    if '@' in email_address:
        return email_address.split('@')[-1].lower()
    return ""


def generate_id(prefix: str, content: str) -> str:
    """Generate a unique ID based on content hash"""
    timestamp = datetime.now(timezone.utc).timestamp()
    hash_input = f"{content}_{timestamp}"
    content_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
    return f"{prefix}_{content_hash}"


def extract_keywords(text: str, min_length: int = 4, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text"""
    if not text:
        return []

    # Common stop words to filter out
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
        'her', 'was', 'one', 'our', 'out', 'has', 'have', 'been', 'were', 'they',
        'this', 'that', 'with', 'from', 'your', 'will', 'would', 'could', 'should',
        'what', 'when', 'where', 'which', 'their', 'there', 'these', 'those'
    }

    # Extract words
    words = re.findall(r'\b\w+\b', text.lower())

    # Filter words
    keywords = [
        word for word in words
        if len(word) >= min_length and word not in stop_words and word.isalpha()
    ]

    # Count frequency and return top keywords
    from collections import Counter
    word_freq = Counter(keywords)
    return [word for word, _ in word_freq.most_common(max_keywords)]


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime to ISO string"""
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.isoformat()


def parse_json_safely(json_str: Union[str, Dict, List], default: Any = None) -> Any:
    """Safely parse JSON string"""
    import json
    if isinstance(json_str, (dict, list)):
        return json_str
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default if default is not None else {}


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def calculate_confidence(scores: List[float]) -> float:
    """Calculate average confidence from a list of scores"""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def validate_email_format(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def sanitize_html(html_content: str) -> str:
    """Remove potentially dangerous HTML tags"""
    if not html_content:
        return ""

    # Remove script tags
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # Remove style tags
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # Remove event handlers
    html_content = re.sub(r'\s+on\w+\s*=\s*["\'][^"\']*["\']', '', html_content, flags=re.IGNORECASE)

    return html_content
