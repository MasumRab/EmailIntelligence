import logging
import unittest
from unittest.mock import MagicMock, patch

# Ensure imports work from the test directory context.
# This might mean setting PYTHONPATH or using relative imports carefully.
# Assuming tests are run from a level where 'server' is a package.
from backend.python_nlp.analysis_components.sentiment_model import SentimentModel

# Suppress logging for tests if not needed
logging.disable(logging.CRITICAL)


class TestSentimentModel(unittest.TestCase):

    def test_analyze_model_success(self):
        mock_sklearn_model = MagicMock()
        mock_sklearn_model.predict.return_value = ["positive"]
        mock_sklearn_model.predict_proba.return_value = [[0.1, 0.9]]  # neutral, positive

        analyzer = SentimentModel(sentiment_model=mock_sklearn_model, has_nltk_installed=True)
        result = analyzer.analyze("This is a great test!")

        mock_sklearn_model.predict.assert_called_once_with(["This is a great test!"])
        mock_sklearn_model.predict_proba.assert_called_once_with(["This is a great test!"])
        self.assertEqual(result["sentiment"], "positive")
        self.assertEqual(result["confidence"], 0.9)
        self.assertEqual(result["method_used"], "model_sentiment")
        self.assertAlmostEqual(result["polarity"], 0.9)  # For positive, polarity is confidence

    def test_analyze_model_fails_fallback_to_textblob(self):
        mock_sklearn_model = MagicMock()
        mock_sklearn_model.predict.side_effect = Exception("Model error")

        # Mock TextBlob
        mock_textblob_instance = MagicMock()
        mock_textblob_instance.sentiment.polarity = 0.8
        mock_textblob_instance.sentiment.subjectivity = 0.5

        with patch(
            "server.python_nlp.analysis_components.sentiment_model.TextBlob",
            return_value=mock_textblob_instance,
        ) as mock_textblob_class:
            analyzer = SentimentModel(sentiment_model=mock_sklearn_model, has_nltk_installed=True)
            result = analyzer.analyze("This is a great test!")

            mock_textblob_class.assert_called_once_with("This is a great test!")
            self.assertEqual(result["sentiment"], "positive")
            self.assertAlmostEqual(result["polarity"], 0.8)
            self.assertEqual(result["method_used"], "fallback_textblob_sentiment")

    def test_analyze_model_and_textblob_fail_fallback_to_keyword(self):
        mock_sklearn_model = MagicMock()
        mock_sklearn_model.predict.side_effect = Exception("Model error")

        with patch(
            "server.python_nlp.analysis_components.sentiment_model.TextBlob",
            side_effect=Exception("TextBlob error"),
        ):
            analyzer = SentimentModel(sentiment_model=mock_sklearn_model, has_nltk_installed=True)
            result = analyzer.analyze("This is a good test!")  # "good" is a positive keyword

            self.assertEqual(result["sentiment"], "positive")
            self.assertEqual(result["confidence"], 0.6)  # Default for keyword
            self.assertEqual(result["method_used"], "fallback_keyword_sentiment")

    def test_analyze_no_model_fallback_to_textblob(self):
        mock_textblob_instance = MagicMock()
        mock_textblob_instance.sentiment.polarity = -0.7
        mock_textblob_instance.sentiment.subjectivity = 0.4

        with patch(
            "server.python_nlp.analysis_components.sentiment_model.TextBlob",
            return_value=mock_textblob_instance,
        ) as mock_textblob_class:
            analyzer = SentimentModel(sentiment_model=None, has_nltk_installed=True)  # No model
            result = analyzer.analyze("This is a bad test.")

            mock_textblob_class.assert_called_once_with("This is a bad test.")
            self.assertEqual(result["sentiment"], "negative")
            self.assertAlmostEqual(result["polarity"], -0.7)
            self.assertEqual(result["method_used"], "fallback_textblob_sentiment")

    def test_analyze_no_model_nltk_disabled_fallback_to_keyword(self):
        analyzer = SentimentModel(
            sentiment_model=None, has_nltk_installed=False
        )  # NLTK (for TextBlob) disabled
        result = analyzer.analyze("This is a neutral test.")

        self.assertEqual(result["sentiment"], "neutral")
        self.assertEqual(result["confidence"], 0.5)
        self.assertEqual(result["method_used"], "fallback_keyword_sentiment")

    def test_keyword_analysis_positive(self):
        analyzer = SentimentModel(sentiment_model=None, has_nltk_installed=False)
        result = analyzer._analyze_keyword("This is good and happy.")
        self.assertEqual(result["sentiment"], "positive")

    def test_keyword_analysis_negative(self):
        analyzer = SentimentModel(sentiment_model=None, has_nltk_installed=False)
        result = analyzer._analyze_keyword("This is bad and sad.")
        self.assertEqual(result["sentiment"], "negative")

    def test_keyword_analysis_neutral(self):
        analyzer = SentimentModel(sentiment_model=None, has_nltk_installed=False)
        result = analyzer._analyze_keyword("This is a test.")
        self.assertEqual(result["sentiment"], "neutral")


if __name__ == "__main__":
    unittest.main()
