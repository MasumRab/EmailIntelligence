import logging
import unittest
from unittest.mock import MagicMock

from backend.python_nlp.analysis_components.intent_model import IntentModel

logging.disable(logging.CRITICAL)


class TestIntentModel(unittest.TestCase):

    def test_analyze_model_success(self):
        mock_sklearn_model = MagicMock()
        mock_sklearn_model.predict.return_value = ["request"]
        mock_sklearn_model.predict_proba.return_value = [[0.1, 0.75, 0.15]]  # Example probabilities

        analyzer = IntentModel(intent_model=mock_sklearn_model)
        result = analyzer.analyze("Could you please send the report?")

        mock_sklearn_model.predict.assert_called_once_with(["Could you please send the report?"])
        mock_sklearn_model.predict_proba.assert_called_once_with(
            ["Could you please send the report?"]
        )
        self.assertEqual(result["intent"], "request")
        self.assertEqual(result["confidence"], 0.75)
        self.assertEqual(result["method_used"], "model_intent")

    def test_analyze_model_fails_fallback_to_regex(self):
        mock_sklearn_model = MagicMock()
        mock_sklearn_model.predict.side_effect = Exception("Model error")

        analyzer = IntentModel(intent_model=mock_sklearn_model)
        result = analyzer.analyze(
            "I have a question about the schedule."
        )  # Regex keywords for inquiry/scheduling

        # Regex fallback might pick 'question' (inquiry) or 'schedule' (scheduling)
        self.assertIn(result["intent"], ["inquiry", "scheduling"])
        self.assertTrue(0.0 < result["confidence"] < 1.0)
        self.assertEqual(result["method_used"], "fallback_regex_intent")

    def test_analyze_no_model_fallback_to_regex(self):
        analyzer = IntentModel(intent_model=None)  # No model
        result = analyzer.analyze("Thank you for your help.")  # Regex keyword for gratitude

        self.assertEqual(result["intent"], "gratitude")
        self.assertEqual(result["method_used"], "fallback_regex_intent")

    def test_regex_analysis_specific_intent(self):
        analyzer = IntentModel(intent_model=None)
        result = analyzer._analyze_regex("This is a complaint about the service.")
        self.assertEqual(result["intent"], "complaint")

    def test_regex_analysis_informational_if_no_match(self):
        analyzer = IntentModel(intent_model=None)
        result = analyzer._analyze_regex("The sky is blue today.")
        self.assertEqual(result["intent"], "informational")
        self.assertEqual(result["confidence"], 0.6)  # Default for informational regex


if __name__ == "__main__":
    unittest.main()
