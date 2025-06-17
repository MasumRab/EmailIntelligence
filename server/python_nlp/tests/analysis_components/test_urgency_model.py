import logging
import unittest
from unittest.mock import MagicMock

from server.python_nlp.analysis_components.urgency_model import UrgencyModel

logging.disable(logging.CRITICAL)

class TestUrgencyModel(unittest.TestCase):

    def test_analyze_model_success(self):
        mock_sklearn_model = MagicMock()
        mock_sklearn_model.predict.return_value = ['high']
        # Probabilities for [critical, high, low, medium] or whatever order model uses
        mock_sklearn_model.predict_proba.return_value = [[0.1, 0.8, 0.05, 0.05]]

        analyzer = UrgencyModel(urgency_model=mock_sklearn_model)
        result = analyzer.analyze("This needs to be done soon.")

        mock_sklearn_model.predict.assert_called_once_with(["This needs to be done soon."])
        mock_sklearn_model.predict_proba.assert_called_once_with(["This needs to be done soon."])
        self.assertEqual(result['urgency'], 'high')
        self.assertEqual(result['confidence'], 0.8)
        self.assertEqual(result['method_used'], 'model_urgency')

    def test_analyze_model_fails_fallback_to_regex(self):
        mock_sklearn_model = MagicMock()
        mock_sklearn_model.predict.side_effect = Exception("Model error")

        analyzer = UrgencyModel(urgency_model=mock_sklearn_model)
        result = analyzer.analyze("This is an emergency!") # Regex keyword for critical

        self.assertEqual(result['urgency'], 'critical')
        self.assertEqual(result['confidence'], 0.9) # Confidence from regex matching
        self.assertEqual(result['method_used'], 'fallback_regex_urgency')

    def test_analyze_no_model_fallback_to_regex(self):
        analyzer = UrgencyModel(urgency_model=None) # No model
        result = analyzer.analyze("Please review this when you can.") # Should be low by regex

        self.assertEqual(result['urgency'], 'low')
        self.assertEqual(result['confidence'], 0.5) # Default for low via regex
        self.assertEqual(result['method_used'], 'fallback_regex_urgency')

    def test_regex_analysis_critical(self):
        analyzer = UrgencyModel(urgency_model=None)
        result = analyzer._analyze_regex("URGENT action required immediately for system failure")
        self.assertEqual(result['urgency'], 'critical')

    def test_regex_analysis_high(self):
        analyzer = UrgencyModel(urgency_model=None)
        result = analyzer._analyze_regex("This is important and has a deadline approaching.")
        self.assertEqual(result['urgency'], 'high')

    def test_regex_analysis_medium(self):
        analyzer = UrgencyModel(urgency_model=None)
        result = analyzer._analyze_regex("Let's discuss this next week.")
        self.assertEqual(result['urgency'], 'medium')

    def test_regex_analysis_low(self):
        analyzer = UrgencyModel(urgency_model=None)
        result = analyzer._analyze_regex("FYI only.")
        self.assertEqual(result['urgency'], 'low')

if __name__ == '__main__':
    unittest.main()
[end of server/python_nlp/tests/analysis_components/test_urgency_model.py]
