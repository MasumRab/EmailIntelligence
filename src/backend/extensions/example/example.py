#!/usr/bin/env python3
"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Example Extension for EmailIntelligence

This extension demonstrates the extension system by adding a simple
sentiment analysis enhancement to the EmailIntelligence application.
"""

import logging
from typing import Any, Dict

# Configure logging
logger = logging.getLogger(__name__)

# Define emoji mappings for sentiment
SENTIMENT_EMOJIS = {"positive": "😊", "negative": "😞", "neutral": "😐"}


def initialize():
    """Initialize the extension."""
    logger.info("--- Example extension: TOP of initialize() ---")

    # Register hooks
    try:
        logger.info("--- Example extension: About to import NLPEngine ---")
        from src.backend.python_nlp.nlp_engine import NLPEngine

        logger.info("--- Example extension: SUCCESSFULLY imported NLPEngine ---")

        # Store the original method
        original_analyze_sentiment = NLPEngine._analyze_sentiment

        # Define the enhanced method
        def enhanced_analyze_sentiment(self, text: str) -> Dict[str, Any]:
            # Call the original method
            result = original_analyze_sentiment(self, text)

            # Add emoji to the result
            sentiment = result.get("sentiment", "neutral")
            result["emoji"] = SENTIMENT_EMOJIS.get(sentiment, "❓")

            # Add more detailed analysis
            result["enhanced"] = True
            result["word_count"] = len(text.split())
            result["character_count"] = len(text)
            result["exclamation_count"] = text.count("!")
            result["question_count"] = text.count("?")

            return result

        # Replace the original method with the enhanced one
        NLPEngine._analyze_sentiment = enhanced_analyze_sentiment

        logger.info("Enhanced sentiment analysis with emojis and detailed metrics")
    except ImportError:
        logger.warning("Could not find NLPEngine, sentiment enhancement not applied")


def shutdown():
    """Shutdown the extension."""
    logger.info("Shutting down example extension")

    # Restore original methods if needed
    try:
        from src.backend.python_nlp.nlp_engine import NLPEngine

        # If we stored the original method somewhere, we could restore it here
        # For now, we'll just log that we're not restoring anything
        logger.info("Note: Original methods not restored on shutdown")
    except ImportError:
        pass


# Additional utility functions that could be used by the application
def get_sentiment_emoji(sentiment: str) -> str:
    """Get an emoji for a sentiment."""
    return SENTIMENT_EMOJIS.get(sentiment, "❓")


def analyze_text_with_emojis(text: str) -> Dict[str, Any]:
    """Analyze text and add emojis to the result."""
    # This is a simple example that could be called directly from the application
    result = {
        "text": text,
        "word_count": len(text.split()),
        "character_count": len(text),
        "exclamation_count": text.count("!"),
        "question_count": text.count("?"),
    }

    # Simple sentiment analysis based on keywords
    positive_words = ["good", "great", "excellent", "happy", "love", "like", "thank"]
    negative_words = ["bad", "terrible", "hate", "dislike", "sorry", "problem", "issue"]

    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        result["sentiment"] = "positive"
    elif negative_count > positive_count:
        result["sentiment"] = "negative"
    else:
        result["sentiment"] = "neutral"

    result["emoji"] = SENTIMENT_EMOJIS.get(result["sentiment"], "❓")

    return result
