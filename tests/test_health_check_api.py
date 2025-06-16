import unittest
from fastapi.testclient import TestClient
from server.python_backend.main import app # Assuming your FastAPI app instance is named 'app'
from unittest.mock import patch, MagicMock
from datetime import datetime

class TestHealthCheckAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_check_success(self):
        print("Running test_health_check_success")
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("timestamp", data)
        try:
            # Attempt to parse the timestamp to validate its format
            # FastAPI/Starlette usually return timezone-aware ISO 8601 strings.
            # If it's naive, fromisoformat might need adjustment or .replace('Z', '+00:00')
            # For example, if timestamp is "2023-10-27T12:34:56.789012" (naive)
            # or "2023-10-27T12:34:56.789012Z" (UTC)
            # or "2023-10-27T12:34:56.789012+00:00" (UTC)
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError as e:
            self.fail(f"Timestamp is not a valid ISO 8601 format: {data['timestamp']}. Error: {e}")
        self.assertEqual(data["version"], "2.0.0") # As defined in main.py

    # Example of how to test a failure scenario if the health check had dependencies
    # For the current simple health check, this might be overkill unless we mock 'datetime.now'
    # or introduce a mockable dependency check.
    # Let's assume for now the main.py health check is simple.
    # If it involved a DB check, we would mock that.
    # For instance, if it had:
    # from .database import get_db
    # @app.get("/health")
    # async def health_check(request: Request, db: DatabaseManager = Depends(get_db)):
    #    await db.execute_query("SELECT 1") # Example DB check
    # Then we would mock db.execute_query to raise an exception.

    # For now, the current health check is too simple to easily simulate a 503 without
    # deeper, potentially flaky, mocking of internal FastAPI/Starlette components or datetime.
    # The existing error handling in the health_check endpoint catches generic Exception.
    # We can test this generic error handling by forcing an exception during the request.
    @patch('server.python_backend.main.datetime') # Patch datetime used within health_check
    def test_health_check_generic_error(self, mock_datetime_module): # Renamed for clarity
        print("Running test_health_check_generic_error")

        # Configure the mock for datetime.now().isoformat()
        # First call raises an exception, subsequent calls return a fixed string
        mock_isoformat_instance = MagicMock(side_effect=[
            Exception("Forced isoformat error"), # First call
            "2023-01-01T00:00:00+00:00"          # Second call (in except block)
        ])
        mock_datetime_module.now.return_value.isoformat = mock_isoformat_instance

        response = self.client.get("/health")
        self.assertEqual(response.status_code, 503)
        data = response.json()
        self.assertEqual(data["status"], "unhealthy")
        self.assertEqual(data["error"], "Service health check failed.")
        self.assertIn("timestamp", data) # Timestamp should still be there from the error response formatting

if __name__ == '__main__':
    unittest.main()
