"""
Email Filter Node Module for Email Intelligence Auto

This module provides AI-powered email filtering capabilities as a processing node
in the workflow engine, integrating with other AI components.
"""

class EmailFilterNode:
    """Processing node for AI-powered email filtering."""

    def __init__(self):
        """Initialize the email filter node."""
        self.filters = {
            'spam': self._check_spam,
            'priority': self._check_priority,
            'category': self._check_category
        }
        self.node_config = {
            'enabled_filters': ['spam', 'priority'],
            'thresholds': {
                'spam_score': 0.8,
                'priority_score': 0.7
            }
        }

    def _check_spam(self, email_data):
        """Check if email is spam based on content analysis."""
        content = email_data.get('content', '').lower()

        spam_indicators = ['win money', 'free offer', 'click here', 'urgent action required']
        spam_score = sum(1 for indicator in spam_indicators if indicator in content) / len(spam_indicators)

        return {
            'is_spam': spam_score >= self.node_config['thresholds']['spam_score'],
            'spam_score': spam_score,
            'confidence': min(spam_score * 100, 100)
        }

    def _check_priority(self, email_data):
        """Determine email priority based on content and metadata."""
        content = email_data.get('content', '').lower()
        subject = email_data.get('subject', '').lower()

        priority_keywords = {
            'urgent': ['urgent', 'asap', 'emergency', 'critical', 'immediate'],
            'high': ['important', 'priority', 'attention', 'review'],
            'normal': []
        }

        priority_score = 0.0

        # Check subject and content for priority indicators
        all_text = subject + ' ' + content

        for level, keywords in priority_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                if level == 'urgent':
                    priority_score = 1.0
                elif level == 'high':
                    priority_score = max(priority_score, 0.7)
                break

        return {
            'priority_level': 'urgent' if priority_score >= 0.9 else 'high' if priority_score >= 0.7 else 'normal',
            'priority_score': priority_score
        }

    def _check_category(self, email_data):
        """Categorize email based on content."""
        content = email_data.get('content', '').lower()

        categories = {
            'work': ['meeting', 'project', 'deadline', 'report', 'task'],
            'personal': ['family', 'friend', 'personal', 'vacation'],
            'financial': ['invoice', 'payment', 'billing', 'account'],
            'marketing': ['offer', 'promotion', 'newsletter', 'update']
        }

        best_category = 'general'
        max_matches = 0

        for category, keywords in categories.items():
            matches = sum(1 for keyword in keywords if keyword in content)
            if matches > max_matches:
                max_matches = matches
                best_category = category

        return {
            'category': best_category,
            'confidence': min(max_matches * 20, 100)  # Simple confidence calculation
        }

    def process(self, email_data):
        """Process an email through the filter node.

        Args:
            email_data: Dictionary containing email information

        Returns:
            Processed email data with filter results
        """
        results = {}

        # Apply enabled filters
        for filter_name in self.node_config['enabled_filters']:
            if filter_name in self.filters:
                filter_func = self.filters[filter_name]
                results[filter_name] = filter_func(email_data)

        # Add processing metadata
        results['processed_by'] = 'EmailFilterNode'
        results['processing_timestamp'] = '2024-01-01T00:00:00Z'  # Would be current timestamp

        # Update email data with results
        email_data['filter_results'] = results

        return email_data

    def configure(self, config):
        """Configure the filter node."""
        if 'enabled_filters' in config:
            self.node_config['enabled_filters'] = config['enabled_filters']
        if 'thresholds' in config:
            self.node_config['thresholds'].update(config['thresholds'])


# Module-level convenience function
def process(email_data):
    """Convenience function for email processing."""
    node = EmailFilterNode()
    return node.process(email_data)