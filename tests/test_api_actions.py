import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from server.python_backend.ai_engine import \
    AIAnalysisResult  # To help mock the return
from server.python_backend.main import \
    app  # Assuming your FastAPI app instance is named 'app'

# If your Pydantic models are in main.py, they would be imported via `app` or directly if structured so.
# For this test, we might not need to import them if we're just checking response structure.


class TestActionExtractionAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("server.python_backend.main.ai_engine.analyze_email", new_callable=AsyncMock)
    def test_extract_actions_from_text_success(self, mock_analyze_email):
        # Mock the return value of ai_engine.analyze_email
        mock_action_item_data = [
            {
                "action_phrase": "Please review the document by tomorrow",
                "verb": "review",
                "object": "document",
                "raw_due_date_text": "by tomorrow",
                "context": "A test sentence. Please review the document by tomorrow. Thank you.",
            },
            {
                "action_phrase": "Also, submit the report.",
                "verb": "submit",
                "object": "report",
                "raw_due_date_text": None,
                "context": "Also, submit the report. And another thing.",
            },
        ]
        # This is what AIAnalysisResult object would contain
        mock_ai_result = AIAnalysisResult(
            data={
                "topic": "test",
                "sentiment": "neutral",
                "intent": "test",
                "urgency": "low",
                "confidence": 0.9,
                "categories": [],
                "keywords": [],
                "reasoning": "",
                "suggested_labels": [],
                "risk_flags": [],
                "category_id": None,
                "action_items": mock_action_item_data,
            }
        )
        mock_analyze_email.return_value = mock_ai_result

        request_payload = {
            "subject": "Meeting Follow-up",
            "content": "A test sentence. Please review the document by tomorrow. Thank you. Also, submit the report. And another thing.",
        }

        response = self.client.post(
            "/api/actions/extract-from-text", json=request_payload
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 2)

        # Check structure of the first action item
        self.assertEqual(
            response_data[0]["action_phrase"], "Please review the document by tomorrow"
        )
        self.assertEqual(response_data[0]["verb"], "review")
        self.assertEqual(response_data[0]["object"], "document")
        self.assertEqual(response_data[0]["raw_due_date_text"], "by tomorrow")
        self.assertTrue("A test sentence." in response_data[0]["context"])

        mock_analyze_email.assert_called_once_with(
            subject=request_payload["subject"], content=request_payload["content"]
        )

    @patch("server.python_backend.main.ai_engine.analyze_email", new_callable=AsyncMock)
    def test_extract_actions_no_actions_found(self, mock_analyze_email):
        # Mock AI engine to return no action items
        mock_ai_result = AIAnalysisResult(
            data={
                "topic": "test",
                "sentiment": "neutral",
                "intent": "test",
                "urgency": "low",
                "confidence": 0.9,
                "categories": [],
                "keywords": [],
                "reasoning": "",
                "suggested_labels": [],
                "risk_flags": [],
                "category_id": None,
                "action_items": [],  # Empty list
            }
        )
        mock_analyze_email.return_value = mock_ai_result

        request_payload = {
            "subject": "General Update",
            "content": "This is just a general update, no specific actions required.",
        }

        response = self.client.post(
            "/api/actions/extract-from-text", json=request_payload
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 0)

    def test_extract_actions_missing_content(self):
        request_payload = {
            "subject": "Missing content"
            # "content" field is missing
        }

        response = self.client.post(
            "/api/actions/extract-from-text", json=request_payload
        )

        # FastAPI should return a 422 Unprocessable Entity for Pydantic validation errors
        self.assertEqual(response.status_code, 422)
        response_data = response.json()
        self.assertIn("detail", response_data)
        # Check that the error detail mentions the 'content' field
        self.assertTrue(
            any(
                "content" in error["loc"]
                for error in response_data["detail"]
                if "loc" in error
            )
        )

    @patch("server.python_backend.main.ai_engine.analyze_email", new_callable=AsyncMock)
    def test_extract_actions_ai_engine_exception(self, mock_analyze_email):
        # Mock AI engine to raise an exception
        mock_analyze_email.side_effect = Exception("AI Engine processing error")

        request_payload = {
            "subject": "Test Error",
            "content": "This content will cause an error in the mocked AI engine.",
        }

        response = self.client.post(
            "/api/actions/extract-from-text", json=request_payload
        )

        self.assertEqual(response.status_code, 500)
        response_data = response.json()
        self.assertIn("detail", response_data)
        self.assertTrue(
            "Failed to extract action items: AI Engine processing error"
            in response_data["detail"]
        )


if __name__ == "__main__":
    unittest.main()
