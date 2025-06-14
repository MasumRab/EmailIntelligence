import unittest
import json
from unittest.mock import patch, MagicMock # Import MagicMock for AdvancedAIEngine test

from server.python_nlp.nlp_engine import NLPEngine
from server.python_backend.ai_engine import AdvancedAIEngine, AIAnalysisResult

class TestNLPEngineIntegration(unittest.TestCase):

    def setUp(self):
        self.nlp_engine = NLPEngine()
        # We might need an AdvancedAIEngine instance for some tests,
        # but its direct analysis method calls a script.
        # We'll primarily mock the script call for AdvancedAIEngine.
        self.advanced_ai_engine = AdvancedAIEngine()

    def test_nlp_engine_analyze_email_includes_action_items(self):
        subject = "Test Subject for Action Items"
        content = "This is a test email. Please complete the task by Monday. We need to also review the report."

        # Ensure NLTK is available for full action item extraction testing if possible,
        # otherwise, it will use the regex-only path which is also fine to test.
        analysis = self.nlp_engine.analyze_email(subject, content)

        self.assertIn('action_items', analysis)
        self.assertIsInstance(analysis['action_items'], list)

        if analysis['action_items']: # If any actions were found
            action_item = analysis['action_items'][0]
            self.assertIn('action_phrase', action_item)
            self.assertIn('verb', action_item)
            self.assertIn('object', action_item)
            self.assertIn('raw_due_date_text', action_item)
            self.assertIn('context', action_item)

            # Check if one of the expected actions is present
            phrases = [item['action_phrase'] for item in analysis['action_items']]
            self.assertTrue(any("Please complete the task by Monday." in phrase for phrase in phrases))
            self.assertTrue(any("need to also review the report." in phrase for phrase in phrases))


    def test_nlp_engine_fallback_analysis_includes_empty_action_items(self):
        # Test _get_fallback_analysis
        fallback_result = self.nlp_engine._get_fallback_analysis("Some error occurred.")
        self.assertIn('action_items', fallback_result)
        self.assertEqual(fallback_result['action_items'], [])

        # Test _get_simple_fallback_analysis
        simple_fallback_result = self.nlp_engine._get_simple_fallback_analysis("Subject", "Content")
        self.assertIn('action_items', simple_fallback_result)
        self.assertEqual(simple_fallback_result['action_items'], [])

    @patch('server.python_backend.ai_engine._execute_async_command')
    async def test_advanced_ai_engine_analyze_email_parses_action_items(self, mock_execute_async):
        # Mock the output of the nlp_engine.py script
        mock_script_output = {
            "topic": "work_business",
            "sentiment": "neutral",
            "intent": "request",
            "urgency": "medium",
            "confidence": 0.8,
            "categories": ["Work & Business"],
            "keywords": ["task", "report"],
            "reasoning": "Detected request for task completion.",
            "suggested_labels": ["work", "task"],
            "risk_flags": [],
            "validation": {"method": "model_all", "score": 0.8, "reliable": True, "feedback": ""},
            "action_items": [
                {
                    "action_phrase": "Please complete the task by Monday.",
                    "verb": "complete",
                    "object": "task",
                    "raw_due_date_text": "by Monday",
                    "context": "This is a test email. Please complete the task by Monday."
                }
            ],
            "details": {} # Add other details if your AIAnalysisResult expects them
        }
        mock_execute_async.return_value = json.dumps(mock_script_output)

        subject = "Test Subject for Advanced AI"
        content = "Please complete the task by Monday."

        # Need to run async method in a way that unittest can handle
        # For Python 3.8+, asyncio.run can be used if the test method is async
        # Here, we'll assume the test runner handles the async nature of this test method.
        ai_result = await self.advanced_ai_engine.analyze_email(subject, content)

        self.assertIsInstance(ai_result, AIAnalysisResult)
        self.assertIsNotNone(ai_result.action_items)
        self.assertEqual(len(ai_result.action_items), 1)

        action_item = ai_result.action_items[0]
        self.assertEqual(action_item['action_phrase'], "Please complete the task by Monday.")
        self.assertEqual(action_item['verb'], "complete")
        self.assertEqual(action_item['raw_due_date_text'], "by Monday")

    def test_advanced_ai_engine_fallback_includes_empty_action_items(self):
        # This tests the synchronous fallback method in AdvancedAIEngine
        fallback_ai_result = self.advanced_ai_engine._get_fallback_analysis("Subject", "Content", "Test error")

        self.assertIsInstance(fallback_ai_result, AIAnalysisResult)
        self.assertIsNotNone(fallback_ai_result.action_items)
        self.assertEqual(len(fallback_ai_result.action_items), 0)


# This allows running the async test method with unittest
# Note: This basic way of running async tests might not work with all test runners or older Python versions.
# For more complex scenarios, consider using a library like `pytest-asyncio` or `asynctest`.
if __name__ == '__main__':
    # To run async tests with unittest's default runner, you might need something like this:
    import asyncio

    # Create a new event loop for tests if necessary, or get the existing one
    # This is a simplified setup.
    # loop = asyncio.get_event_loop()
    # test_suite = unittest.TestLoader().loadTestsFromTestCase(TestNLPEngineIntegration)
    # for test in test_suite:
    #     if asyncio.iscoroutinefunction(test.test_advanced_ai_engine_analyze_email):
    #         # This is a simplistic way to run one async test.
    #         # A proper async test runner is better.
    #         async def run_async_test():
    #             instance = TestNLPEngineIntegration()
    #             instance.setUp()
    #             await instance.test_advanced_ai_engine_analyze_email()
    #         loop.run_until_complete(run_async_test())
    #     else:
    #         # For synchronous tests, run them normally (though TestLoader does this)
    #         pass # Or integrate with a test runner properly
    unittest.main()
