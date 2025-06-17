import logging
import unittest
from unittest.mock import MagicMock

from server.python_nlp.analysis_components.topic_model import TopicModel

logging.disable(logging.CRITICAL)

class TestTopicModel(unittest.TestCase):

    def test_analyze_model_success(self):
        mock_sklearn_model = MagicMock()
        mock_sklearn_model.predict.return_value = ['Work & Business']
        mock_sklearn_model.predict_proba.return_value = [[0.1, 0.8, 0.1]] # Example probabilities

        analyzer = TopicModel(topic_model=mock_sklearn_model)
        result = analyzer.analyze("Discussing project deadlines.")

        mock_sklearn_model.predict.assert_called_once_with(["Discussing project deadlines."])
        mock_sklearn_model.predict_proba.assert_called_once_with(["Discussing project deadlines."])
        self.assertEqual(result['topic'], 'Work & Business')
        self.assertEqual(result['confidence'], 0.8)
        self.assertEqual(result['method_used'], 'model_topic')

    def test_analyze_model_fails_fallback_to_keyword(self):
        mock_sklearn_model = MagicMock()
        mock_sklearn_model.predict.side_effect = Exception("Model error")

        analyzer = TopicModel(topic_model=mock_sklearn_model)
        result = analyzer.analyze("Let's talk about the invoice and payment.") # Keywords for Finance

        self.assertEqual(result['topic'], 'Finance & Banking') # Based on keyword fallback
        self.assertTrue(0.0 < result['confidence'] < 1.0) # Confidence from keyword matching
        self.assertEqual(result['method_used'], 'fallback_keyword_topic')

    def test_analyze_no_model_fallback_to_keyword(self):
        analyzer = TopicModel(topic_model=None) # No model
        result = analyzer.analyze("My family vacation was great.") # Keywords for Personal/Travel

        # Keyword logic might pick 'Personal & Family' or 'Travel & Leisure'
        self.assertIn(result['topic'], ['Personal & Family', 'Travel & Leisure'])
        self.assertEqual(result['method_used'], 'fallback_keyword_topic')

    def test_keyword_analysis_specific_topic(self):
        analyzer = TopicModel(topic_model=None)
        result = analyzer._analyze_keyword("This email is about a project meeting and presentation.")
        self.assertEqual(result['topic'], 'Work & Business')

    def test_keyword_analysis_general_if_no_keywords(self):
        analyzer = TopicModel(topic_model=None)
        result = analyzer._analyze_keyword("This is a simple statement.")
        self.assertEqual(result['topic'], 'General')
        self.assertEqual(result['confidence'], 0.5) # Default for general

if __name__ == '__main__':
    unittest.main()
[end of server/python_nlp/tests/analysis_components/test_topic_model.py]
