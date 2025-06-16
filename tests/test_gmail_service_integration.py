import unittest
from unittest.mock import MagicMock, AsyncMock # AsyncMock for async methods
import json # Added import

from server.python_nlp.gmail_service import GmailAIService
# Assuming AdvancedAIEngine and AIAnalysisResult are importable for type hinting or mocking structure
# from server.python_backend.ai_engine import AdvancedAIEngine, AIAnalysisResult
from server.python_nlp.gmail_metadata import GmailMessage # For structuring metadata input

class TestGmailAIServiceIntegration(unittest.TestCase):

    async def test_perform_ai_analysis_includes_action_items(self):
        # Mock AdvancedAIEngine
        mock_advanced_ai_engine = MagicMock()

        # Define the mock return value for advanced_ai_engine.analyze_email
        # This should be an object that has a to_dict() method, or just a dict
        # matching what _perform_ai_analysis expects.
        # Let's assume it returns a dictionary directly for simplicity in this mock.
        mock_analysis_output = {
            "topic": "work",
            "sentiment": "positive",
            "intent": "request",
            "urgency": "high",
            "confidence": 0.95,
            "categories": ["Work"],
            "keywords": ["project", "deadline"],
            "reasoning": "AI reasoned this.",
            "suggested_labels": ["important"],
            "risk_flags": [],
            "action_items": [
                {"action_phrase": "Follow up on Theme D", "verb": "Follow", "object": "Theme", "raw_due_date_text": None, "context": "Follow up on Theme D"}
            ]
        }
        # Configure the mock for an async method call
        mock_advanced_ai_engine.analyze_email = AsyncMock(return_value=mock_analysis_output)

        # Instantiate GmailAIService with the mocked AdvancedAIEngine
        gmail_service = GmailAIService(advanced_ai_engine=mock_advanced_ai_engine)

        # Prepare a sample email_data input for _perform_ai_analysis
        email_data_for_analysis = {
            'id': 'test_email_123',
            'subject': 'Project Update and Action Items',
            'content': 'Hello team, please Follow up on Theme D. We also need to discuss the budget.',
            'sender_email': 'test@example.com',
            'timestamp': '2023-01-01T12:00:00Z'
        }

        # Call the method under test
        result_analysis = await gmail_service._perform_ai_analysis(email_data_for_analysis)

        # Assertions
        self.assertIsNotNone(result_analysis)
        self.assertIn('action_items', result_analysis)
        self.assertEqual(len(result_analysis['action_items']), 1)
        self.assertEqual(result_analysis['action_items'][0]['action_phrase'], "Follow up on Theme D")

        # Verify that the mocked analyze_email was called correctly
        mock_advanced_ai_engine.analyze_email.assert_called_once_with(
            subject=email_data_for_analysis['subject'],
            content=email_data_for_analysis['content']
        )

    def test_convert_to_db_format_includes_action_items_in_metadata(self):
        # No actual AI engine needed here, we pass the ai_analysis_result directly
        gmail_service = GmailAIService(advanced_ai_engine=None)

        mock_gmail_metadata = MagicMock(spec=GmailMessage)
        mock_gmail_metadata.message_id = "msg1"
        mock_gmail_metadata.thread_id = "thread1"
        mock_gmail_metadata.history_id = "hist1"
        mock_gmail_metadata.from_address = "sender@example.com"
        mock_gmail_metadata.subject = "DB Format Test"
        mock_gmail_metadata.body_plain = "Content with action: please do this."
        mock_gmail_metadata.body_html = "<p>Content with action: please do this.</p>" # Added
        mock_gmail_metadata.snippet = "Content with action..."
        mock_gmail_metadata.date = "2023-10-26 10:00:00"
        mock_gmail_metadata.internal_date = 1672531200000
        mock_gmail_metadata.to_addresses = ["r@x.com"]
        mock_gmail_metadata.cc_addresses = []
        mock_gmail_metadata.bcc_addresses = []
        mock_gmail_metadata.reply_to = None
        mock_gmail_metadata.label_ids = ["INBOX", "IMPORTANT"]
        mock_gmail_metadata.labels = ["Inbox", "Important"] # Assuming labels are processed
        mock_gmail_metadata.category = "primary"
        mock_gmail_metadata.is_unread = False
        mock_gmail_metadata.is_starred = True
        mock_gmail_metadata.is_important = True
        mock_gmail_metadata.is_draft = False
        mock_gmail_metadata.is_sent = True
        mock_gmail_metadata.is_spam = False
        mock_gmail_metadata.is_trash = False
        mock_gmail_metadata.is_chat = False
        mock_gmail_metadata.has_attachments = False
        mock_gmail_metadata.attachments = []
        mock_gmail_metadata.size_estimate = 1024
        mock_gmail_metadata.spf_status = "pass"
        mock_gmail_metadata.dkim_status = "pass"
        mock_gmail_metadata.dmarc_status = "pass"
        mock_gmail_metadata.encryption_info = {}
        mock_gmail_metadata.priority = "normal"
        mock_gmail_metadata.auto_reply = False
        mock_gmail_metadata.mailing_list = None
        mock_gmail_metadata.in_reply_to = None
        mock_gmail_metadata.references = None
        mock_gmail_metadata.thread_info = {}
        mock_gmail_metadata.importance_markers = []
        mock_gmail_metadata.custom_headers = {}


        ai_analysis_result_with_actions = {
            "topic": "work", "sentiment": "neutral", "intent": "request", "urgency": "medium",
            "confidence": 0.88, "categories": ["Work"], "keywords": ["do this"],
            "reasoning": "Detected a task.", "suggested_labels": [], "risk_flags": [],
            "action_items": [
                {"action_phrase": "please do this", "verb": "do", "object": "this", "raw_due_date_text": None, "context": "Content with action: please do this."}
            ]
        }

        db_email = gmail_service._convert_to_db_format(mock_gmail_metadata, ai_analysis_result_with_actions)

        self.assertIn('analysisMetadata', db_email)
        analysis_metadata = json.loads(db_email['analysisMetadata'])

        self.assertIn('ai_analysis', analysis_metadata)
        self.assertIn('action_items', analysis_metadata['ai_analysis'])
        self.assertEqual(len(analysis_metadata['ai_analysis']['action_items']), 1)
        self.assertEqual(analysis_metadata['ai_analysis']['action_items'][0]['action_phrase'], "please do this")

    def test_convert_to_db_format_no_ai_analysis(self):
        gmail_service = GmailAIService(advanced_ai_engine=None)
        mock_gmail_metadata = MagicMock(spec=GmailMessage) # Populate as above
        # ... (populate mock_gmail_metadata with minimal fields for the test)
        mock_gmail_metadata.message_id = "msg2"
        mock_gmail_metadata.thread_id = "thread2"
        mock_gmail_metadata.history_id = "hist2" # Added
        # ... (other fields)
        mock_gmail_metadata.from_address = "sender2@example.com"
        mock_gmail_metadata.subject = "No AI Test"
        mock_gmail_metadata.body_plain = "Content"
        mock_gmail_metadata.body_html = "<p>Content</p>" # Added
        mock_gmail_metadata.snippet = "Content"
        mock_gmail_metadata.date = "2023-10-27 10:00:00"
        mock_gmail_metadata.internal_date = 1672531200000
        mock_gmail_metadata.to_addresses = []
        mock_gmail_metadata.cc_addresses = []
        mock_gmail_metadata.bcc_addresses = []
        mock_gmail_metadata.reply_to = None
        mock_gmail_metadata.label_ids = []
        mock_gmail_metadata.labels = []
        mock_gmail_metadata.category = "primary" # Default category
        mock_gmail_metadata.attachments = []
        mock_gmail_metadata.importance_markers = []
        mock_gmail_metadata.thread_info = {}
        mock_gmail_metadata.custom_headers = {}
        # Adding other attributes that might be accessed, with default values
        mock_gmail_metadata.is_unread = False
        mock_gmail_metadata.is_starred = False
        mock_gmail_metadata.is_important = False
        mock_gmail_metadata.is_draft = False
        mock_gmail_metadata.is_sent = True
        mock_gmail_metadata.is_spam = False
        mock_gmail_metadata.is_trash = False
        mock_gmail_metadata.is_chat = False
        mock_gmail_metadata.has_attachments = False
        mock_gmail_metadata.size_estimate = 100
        mock_gmail_metadata.spf_status = "pass"
        mock_gmail_metadata.dkim_status = "pass"
        mock_gmail_metadata.dmarc_status = "pass"
        mock_gmail_metadata.encryption_info = {}
        mock_gmail_metadata.priority = "normal"
        mock_gmail_metadata.auto_reply = False
        mock_gmail_metadata.mailing_list = None
        mock_gmail_metadata.in_reply_to = None
        mock_gmail_metadata.references = None


        db_email = gmail_service._convert_to_db_format(mock_gmail_metadata, None) # Pass None for ai_analysis_result

        self.assertIn('analysisMetadata', db_email)
        analysis_metadata = json.loads(db_email['analysisMetadata'])

        self.assertIn('ai_analysis', analysis_metadata)
        self.assertIn('action_items', analysis_metadata['ai_analysis'])
        self.assertEqual(len(analysis_metadata['ai_analysis']['action_items']), 0)
        self.assertEqual(analysis_metadata['ai_analysis']['topic'], "unknown")


if __name__ == '__main__':
    # Unittest runner doesn't directly support async test methods out of the box
    # without helpers or specific runners like pytest-asyncio or asynctest.
    # For a simple case, one might run specific async tests using asyncio.run(),
    # but it's better to use an async-compatible test runner.
    # This example focuses on the test structure.
    # To run the async test `test_perform_ai_analysis_includes_action_items`:
    # import asyncio
    # async def run_single_async_test():
    #     test = TestGmailAIServiceIntegration("test_perform_ai_analysis_includes_action_items")
    #     await test.test_perform_ai_analysis_includes_action_items()
    # if __name__ == '__main__':
    #    asyncio.run(run_single_async_test())
    # else:
    #    unittest.main()
    # This is typically handled by the test runner itself (e.g. pytest with pytest-asyncio)
    unittest.main()
