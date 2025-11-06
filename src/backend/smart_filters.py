"""
Smart Filtering Engine for Email Intelligence Auto

This module provides intelligent filtering capabilities for email processing,
including content-based filtering, priority scoring, and automated categorization.
"""

class SmartFilter:
    """Main class for smart filtering operations."""

    def __init__(self):
        """Initialize the smart filter engine."""
        self.filters = []
        self.priority_weights = {
            'urgent': 1.0,
            'high': 0.8,
            'medium': 0.5,
            'low': 0.2
        }

    def add_filter(self, filter_rule):
        """Add a filtering rule."""
        self.filters.append(filter_rule)

    def get_priority_score(self, email_data):
        """Calculate priority score for an email."""
        # Simple priority calculation based on keywords
        score = 0.0
        content = email_data.get('content', '').lower()

        urgent_keywords = ['urgent', 'asap', 'emergency', 'critical']
        for keyword in urgent_keywords:
            if keyword in content:
                score += self.priority_weights['urgent']
                break

        return min(score, 1.0)  # Cap at 1.0


def apply_filters(email_data, filters=None):
    """Apply filtering logic to email data.

    Args:
        email_data: Dictionary containing email information
        filters: List of filter rules to apply

    Returns:
        Filtered email data with priority score
    """
    if filters is None:
        filters = []

    filter_engine = SmartFilter()

    # Apply custom filters
    for filter_rule in filters:
        filter_engine.add_filter(filter_rule)

    # Calculate and add priority score
    priority_score = filter_engine.get_priority_score(email_data)
    email_data['priority_score'] = priority_score

    return email_data