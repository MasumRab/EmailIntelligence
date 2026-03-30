import sys
import os
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import asyncio

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from modules.new_ui.backend_adapter import BackendClient

class TestBackendClient(unittest.TestCase):

    def setUp(self):
        self.client = BackendClient()

    @patch("modules.new_ui.backend_adapter.get_ai_engine")
    def test_analyze_text(self, mock_get_ai):
        # Create a mock for the AI Engine
        mock_engine = AsyncMock()

        # Create a mock for the analysis result
        mock_analysis_result = MagicMock()
        mock_analysis_result.to_dict.return_value = {
            "sentiment": "positive", "confidence": 0.9, "topic": "work"
        }

        # Configure analyze_email to return the result object
        # Note: Since mock_engine is AsyncMock, calling a method on it creates an AsyncMock
        # When awaited, it returns its .return_value
        mock_engine.analyze_email.return_value = mock_analysis_result

        # correctly mock async context manager
        # __aenter__ is an async method, so it should return the engine
        mock_get_ai.return_value.__aenter__.return_value = mock_engine

        # Run async test
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.client.analyze_text("Subject\nContent"))
        finally:
            loop.close()

        self.assertIsInstance(result, dict)
        self.assertEqual(result["sentiment"], "positive")
        self.assertEqual(result["confidence"], 0.9)

    def test_persistence(self):
        # Test generic fallback persistence
        key = "test_item_123"
        data = {"foo": "bar"}

        # Save
        self.assertTrue(self.client.persist_item(key, data))

        # Retrieve
        retrieved = self.client.retrieve_item(key)
        self.assertEqual(retrieved, data)

        # Clean up
        import pathlib
        file_path = pathlib.Path(__file__).parent.parent / "data" / f"{key}.json"
        if file_path.exists():
            file_path.unlink()

if __name__ == "__main__":
    unittest.main()
