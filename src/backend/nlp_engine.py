"""
NLP Engine Module for Email Intelligence Auto

This module provides natural language processing capabilities including
sentiment analysis, entity extraction, and text processing.
"""

class NLPEngine:
    """Main class for NLP processing operations."""

    def __init__(self):
        """Initialize the NLP engine."""
        self.sentiment_keywords = {
            'positive': ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'best'],
            'negative': ['bad', 'terrible', 'awful', 'hate', 'worst', 'disappointed', 'angry', 'frustrated'],
            'neutral': ['okay', 'fine', 'average', 'normal', 'standard']
        }

    def analyze_sentiment(self, text):
        """Analyze the sentiment of the given text.

        Args:
            text: Input text to analyze

        Returns:
            Sentiment label ('positive', 'negative', 'neutral') or score
        """
        if not text:
            return 'neutral'

        text_lower = text.lower()
        positive_count = sum(1 for word in self.sentiment_keywords['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.sentiment_keywords['negative'] if word in text_lower)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def extract_entities(self, text):
        """Extract named entities from the text.

        Args:
            text: Input text to analyze

        Returns:
            Dictionary of extracted entities
        """
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'dates': [],
            'emails': []
        }

        # Simple entity extraction (in real implementation would use NER models)
        words = text.split()

        # Extract email addresses (simple pattern)
        for word in words:
            if '@' in word and '.' in word:
                entities['emails'].append(word.strip('.,'))

        # Extract capitalized words as potential entities
        for word in words:
            if word.istitle() and len(word) > 2:
                # Simple heuristic: long capitalized words might be organizations
                if len(word) > 4:
                    entities['organizations'].append(word)
                else:
                    entities['persons'].append(word)

        return entities

    def preprocess_text(self, text):
        """Preprocess text for NLP operations.

        Args:
            text: Input text

        Returns:
            Preprocessed text
        """
        if not text:
            return ""

        # Basic preprocessing
        processed = text.lower().strip()
        # Remove extra whitespace
        processed = ' '.join(processed.split())

        return processed


# Module-level convenience functions
def analyze_sentiment(text):
    """Convenience function for sentiment analysis."""
    engine = NLPEngine()
    return engine.analyze_sentiment(text)


def extract_entities(text):
    """Convenience function for entity extraction."""
    engine = NLPEngine()
    return engine.extract_entities(text)


def preprocess_text(text):
    """Convenience function for text preprocessing."""
    engine = NLPEngine()
    return engine.preprocess_text(text)