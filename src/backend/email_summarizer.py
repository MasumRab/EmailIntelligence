"""
Email Summarization Module for Email Intelligence Auto

This module provides AI-powered email summarization capabilities,
extracting key information and generating concise summaries.
"""

class EmailSummarizer:
    """Main class for email summarization operations."""

    def __init__(self):
        """Initialize the email summarizer."""
        self.summary_templates = {
            'short': "Key points: {points}",
            'medium': "Summary: {content}. Key action: {action}",
            'long': "Full summary: {content}. Importance: {importance}. Action required: {action}"
        }

    def summarize(self, email_data, length='medium'):
        """Generate a summary of the email content.

        Args:
            email_data: Dictionary containing email information
            length: Summary length ('short', 'medium', 'long')

        Returns:
            String summary of the email
        """
        content = email_data.get('content', '')

        if not content:
            return "No content to summarize"

        # Simple extractive summarization (in real implementation would use NLP models)
        sentences = content.split('.')
        key_sentences = sentences[:2] if len(sentences) > 2 else sentences

        summary_points = []
        for sentence in key_sentences:
            sentence = sentence.strip()
            if sentence:
                # Extract key information
                if any(word in sentence.lower() for word in ['important', 'urgent', 'action', 'required']):
                    summary_points.append(sentence)

        if not summary_points:
            summary_points = [sentences[0].strip()] if sentences else ["General email content"]

        if length == 'short':
            return f"Key points: {'; '.join(summary_points)}"
        elif length == 'long':
            importance = "High" if any(word in content.lower() for word in ['urgent', 'asap', 'critical']) else "Normal"
            action = "Yes" if any(word in content.lower() for word in ['action', 'required', 'please']) else "No"
            return f"Full summary: {' '.join(summary_points)}. Importance: {importance}. Action required: {action}"
        else:  # medium
            action = "Review and respond" if any(word in content.lower() for word in ['action', 'required']) else "Review"
            return f"Summary: {' '.join(summary_points)}. Key action: {action}"


# Module-level convenience function
def summarize(email_data, length='medium'):
    """Convenience function for email summarization."""
    summarizer = EmailSummarizer()
    return summarizer.summarize(email_data, length)