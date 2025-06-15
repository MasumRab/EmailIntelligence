import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from server.python_backend.main import app, get_db
from server.python_backend.models import EmailResponse # Import specific model
from typing import List, Optional # Ensure List and Optional are imported

# Mock DatabaseManager for dependency injection
mock_db_manager = MagicMock()

async def override_get_db():
    return mock_db_manager

app.dependency_overrides[get_db] = override_get_db

class TestEmailAPI_GET(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        mock_db_manager.reset_mock()
        mock_db_manager.get_all_emails = AsyncMock()
        mock_db_manager.get_emails_by_category = AsyncMock()
        mock_db_manager.search_emails = AsyncMock()
        mock_db_manager.get_email_by_id = AsyncMock()

    def test_get_emails_all(self):
        print("Running test_get_emails_all")
        # Ensure all fields required by EmailResponse are present
        mock_data = [
            {
                "id": 1, "messageId": "msg1", "threadId": "thread1",
                "sender": "sender1@example.com", "senderEmail": "sender1@example.com",
                "subject": "Subject 1", "content": "Content 1", "preview": "Preview 1",
                "time": "2023-01-01T10:00:00Z", "category": "CategoryA",
                "labels": ["label1"], "isImportant": False, "isStarred": False,
                "isUnread": True, "confidence": 80
            },
            {
                "id": 2, "messageId": "msg2", "threadId": "thread2",
                "sender": "sender2@example.com", "senderEmail": "sender2@example.com",
                "subject": "Subject 2", "content": "Content 2", "preview": "Preview 2",
                "time": "2023-01-02T10:00:00Z", "category": "CategoryB",
                "labels": ["label2"], "isImportant": True, "isStarred": True,
                "isUnread": False, "confidence": 90
            }
        ]
        mock_db_manager.get_all_emails.return_value = mock_data

        response = self.client.get("/api/emails")

        print(f"Response Status Code: {response.status_code}")
        try:
            print(f"Response JSON: {response.json()}")
        except Exception as e:
            print(f"Response Text: {response.text}")
            print(f"Error decoding JSON: {e}")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["subject"], "Subject 1")
        mock_db_manager.get_all_emails.assert_called_once()

    def test_get_emails_by_category(self):
        print("Running test_get_emails_by_category")
        mock_data = [
            {"id": 1, "messageId": "msg1", "threadId": "thread1", "sender": "sender1@example.com", "senderEmail": "sender1@example.com", "subject": "Subject 1", "content": "Content 1", "preview": "Preview 1", "time": "2023-01-01T10:00:00Z", "category": "CategoryA", "labels": ["label1"], "isImportant": False, "isStarred": False, "isUnread": True, "confidence": 80}
        ]
        mock_db_manager.get_emails_by_category.return_value = mock_data
        response = self.client.get("/api/emails?category_id=1")
        print(f"Response Status Code (category): {response.status_code}")
        try:
            print(f"Response JSON (category): {response.json()}")
        except Exception as e:
            print(f"Response Text (category): {response.text}")
            print(f"Error decoding JSON (category): {e}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["category"], "CategoryA")
        mock_db_manager.get_emails_by_category.assert_called_once_with(1)

    def test_get_emails_by_search(self):
        print("Running test_get_emails_by_search")
        mock_data = [
            {"id": 2, "messageId": "msg2", "threadId": "thread2", "sender": "sender2@example.com", "senderEmail": "sender2@example.com", "subject": "Subject 2", "content": "Content 2", "preview": "Preview 2", "time": "2023-01-02T10:00:00Z", "category": "CategoryB", "labels": ["label2"], "isImportant": True, "isStarred": True, "isUnread": False, "confidence": 90}
        ]
        mock_db_manager.search_emails.return_value = mock_data
        response = self.client.get("/api/emails?search=Subject%202")
        print(f"Response Status Code (search): {response.status_code}")
        try:
            print(f"Response JSON (search): {response.json()}")
        except Exception as e:
            print(f"Response Text (search): {response.text}")
            print(f"Error decoding JSON (search): {e}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["subject"], "Subject 2")
        mock_db_manager.search_emails.assert_called_once_with("Subject 2")

    def test_get_email_by_id_found(self):
        print("Running test_get_email_by_id_found")
        mock_data = {"id": 1, "messageId": "msg1", "threadId": "thread1", "sender": "sender1@example.com", "senderEmail": "sender1@example.com", "subject": "Subject 1", "content": "Content 1", "preview": "Preview 1", "time": "2023-01-01T10:00:00Z", "category": "CategoryA", "labels": ["label1"], "isImportant": False, "isStarred": False, "isUnread": True, "confidence": 80}
        mock_db_manager.get_email_by_id.return_value = mock_data
        response = self.client.get("/api/emails/1")
        print(f"Response Status Code (id_found): {response.status_code}")
        try:
            print(f"Response JSON (id_found): {response.json()}")
        except Exception as e:
            print(f"Response Text (id_found): {response.text}")
            print(f"Error decoding JSON (id_found): {e}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["subject"], "Subject 1")
        mock_db_manager.get_email_by_id.assert_called_once_with(1)

    def test_get_email_by_id_not_found(self):
        print("Running test_get_email_by_id_not_found")
        mock_db_manager.get_email_by_id.return_value = None
        response = self.client.get("/api/emails/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Email not found"})
        mock_db_manager.get_email_by_id.assert_called_once_with(999)

    def test_get_email_by_id_db_error(self):
        print("Running test_get_email_by_id_db_error")
        mock_db_manager.get_email_by_id.side_effect = Exception("Database connection error")
        response = self.client.get("/api/emails/1")
        self.assertEqual(response.status_code, 500)
        self.assertIn("Failed to fetch email", response.json()["detail"])
        mock_db_manager.get_email_by_id.assert_called_once_with(1)

    def test_get_emails_db_error(self):
        print("Running test_get_emails_db_error")
        mock_db_manager.get_all_emails.side_effect = Exception("Database connection error")
        response = self.client.get("/api/emails")
        self.assertEqual(response.status_code, 500)
        self.assertIn("Failed to fetch emails", response.json()["detail"])
        mock_db_manager.get_all_emails.assert_called_once()

# Import Pydantic models if not already at the top
from server.python_backend.models import EmailCreate, EmailUpdate
from server.python_backend.ai_engine import AIAnalysisResult # Ensure this is imported

# Mock ai_engine and filter_manager for the new tests
# These might be better placed at the module level if used by multiple classes
# For now, let's assume they are patched within the test methods or a new test class.

class TestEmailAPI_POST_PUT(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        # Reset mocks before each test
        # Ensure mock_db_manager is the same instance as used by override_get_db
        global mock_db_manager
        mock_db_manager.reset_mock()
        mock_db_manager.create_email = AsyncMock()
        mock_db_manager.update_email = AsyncMock()
        mock_db_manager.get_email_by_id = AsyncMock() # Potentially used by update logic before actual update

    @patch('server.python_backend.main.ai_engine.analyze_email', new_callable=AsyncMock)
    @patch('server.python_backend.main.filter_manager.apply_filters_to_email', new_callable=AsyncMock)
    @patch('server.python_backend.main.performance_monitor.record_email_processing') # Mock background task
    def test_create_email_success(self, mock_record_processing, mock_apply_filters, mock_analyze_email):
        print("Running test_create_email_success")
        email_data = {
            "sender": "test@example.com",
            "senderEmail": "test@example.com",
            "subject": "New Email",
            "content": "This is the content of the new email.",
            "preview": "New email preview",
            "time": "2023-10-26T10:00:00Z",
            "isImportant": False,
            "isStarred": False,
            "isUnread": True
        }

        mock_ai_result = AIAnalysisResult(data={
            "topic": "general", "sentiment": "neutral", "intent": "informational", "urgency": "low",
            "confidence": 0.95, "categories": [], "keywords": ["new", "email"], "reasoning": "N/A",
            "suggested_labels": ["inbox"], "risk_flags": [], "category_id": 1,
            "action_items": []
        })
        mock_analyze_email.return_value = mock_ai_result
        mock_apply_filters.return_value = {"matched_filters": [], "applied_actions": []}

        created_email_response = {
            "id": 100,
            "sender": "test@example.com",
            "senderEmail": "test@example.com",
            "subject": "New Email",
            "content": "This is the content of the new email.",
            "preview": "New email preview",
            "time": "2023-10-26T10:00:00Z",
            "category": "General",
            "labels": ["inbox"],
            "isImportant": False,
            "isStarred": False,
            "isUnread": True,
            "confidence": 95,
            # "analysisMetadata": mock_ai_result.to_dict() # This field is in EmailCreate, not directly in EmailResponse from main.py
        }
        # The main.py EmailResponse model does not have analysisMetadata directly.
        # The db.create_email should return data that can be parsed by EmailResponse.
        # The endpoint /api/emails (POST) in main.py returns `created_email` which comes from `db.create_email`.
        # Let's assume db.create_email returns a dict compatible with the main.py EmailResponse.
        # For the test, mock_db_manager.create_email.return_value should be this compatible dict.
        # The actual `created_email` from `db.create_email` in `main.py` for the endpoint is:
        #   created_email = await db.create_email(email_data)
        #   where email_data was:
        #       email_data = email.dict()
        #       email_data.update({
        #           'confidence': int(ai_analysis.confidence * 100),
        #           'categoryId': ai_analysis.category_id, # This would need to be resolved to category name for EmailResponse
        #           'labels': ai_analysis.suggested_labels,
        #           'analysisMetadata': ai_analysis.to_dict() # This field is NOT in main.py's EmailResponse
        #       })
        # So, the data passed to db.create_email has 'analysisMetadata', but the main.py EmailResponse model for the endpoint does not.
        # This means the db layer should return a dict that, when passed to EmailResponse(**db_return_dict), works.
        # The test's `created_email_response` for the mock should align with what the main.py `EmailResponse` model expects.
        # `main.py`'s `EmailResponse` does not have `analysisMetadata`.
        # It has `category: Optional[str]`. The `db.create_email` would likely store `categoryId` but needs to return `category` (name).
        # For the purpose of this test, we are mocking `db.create_email`'s return value.
        # So, it should be a dict that FastAPI can convert using `EmailResponse` as the response_model.

        mock_db_manager.create_email.return_value = created_email_response # This mock is what the endpoint returns after db call

        response = self.client.post("/api/emails", json=email_data)

        print(f"POST /api/emails Response Status Code: {response.status_code}")
        try:
            print(f"POST /api/emails Response JSON: {response.json()}")
        except Exception as e:
            print(f"POST /api/emails Response Text: {response.text}")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["subject"], "New Email")
        self.assertEqual(data["confidence"], 95) # This matches our created_email_response
        self.assertEqual(data["id"], 100)

        mock_analyze_email.assert_called_once_with(email_data["subject"], email_data["content"])
        mock_apply_filters.assert_called_once()

        # What `db.create_email` is called with in main.py:
        expected_db_payload_to_main_create_email_func = {
            **EmailCreate(**email_data).model_dump(), # Ensures it's validated by EmailCreate first
            'confidence': 95,
            'categoryId': 1,
            'labels': ['inbox'],
            'analysisMetadata': mock_ai_result.to_dict()
        }
        # Ensure all fields from EmailCreate are present in the base of expected_db_payload
        # EmailCreate fields: sender, senderEmail, subject, content, time, messageId, threadId, contentHtml, preview, labels, isImportant, isStarred, isUnread, hasAttachments, attachmentCount, sizeEstimate
        # The test email_data only has some of these. Let's use the model_dump from EmailCreate.

        # Correct payload passed to db.create_email
        # The `email` Pydantic model in main.py's `create_email` endpoint is `EmailCreate`.
        # So, `email.dict()` will be based on `EmailCreate`.
        # `email_data` in the test is a simple dict. To accurately mock the call to `db.create_email`,
        # we should ensure `expected_db_payload` reflects what `main.py`'s `create_email` function
        # would pass to `db.create_email`.

        # The `email_data` in `main.py` is `email.dict()` (from `EmailCreate`) then updated.
        temp_email_create_obj = EmailCreate(**email_data) # Pydantic validation of input
        db_call_arg = temp_email_create_obj.model_dump()
        db_call_arg.update({
            'confidence': 95,
            'categoryId': 1,
            'labels': ['inbox'],
            'analysisMetadata': mock_ai_result.to_dict()
        })

        mock_db_manager.create_email.assert_called_once_with(db_call_arg)
        mock_record_processing.assert_called_once()


    def test_create_email_validation_error(self):
        print("Running test_create_email_validation_error")
        email_data = { # Missing sender, senderEmail, time, preview
            "subject": "New Email",
            "content": "This is the content of the new email."
        }
        response = self.client.post("/api/emails", json=email_data)
        self.assertEqual(response.status_code, 422)
        response_data = response.json()
        print(f"POST /api/emails Validation Error JSON: {response_data}")
        self.assertIn("detail", response_data)

        missing_fields = set()
        for error in response_data['detail']:
            if error['type'] == 'missing':
                missing_fields.add(error['loc'][-1]) # Get the last element of loc list for field name

        # Fields from EmailCreate that are required (not Optional, no default in Pydantic model)
        # sender, senderEmail, subject, content, time are from EmailBase
        # preview is optional in EmailCreate but has a validator that sets it if None, based on content.
        # However, if content itself is missing or preview is explicitly required by model, it can be 'missing'.
        # The validator for preview runs *after* initial field presence check.
        # EmailCreate does not define preview as Optional, but it does have a default_factory for labels.
        # Let's check `EmailBase` and `EmailCreate` definitions in `models.py`
        # EmailBase: sender, senderEmail, subject, content, time are all required.
        # EmailCreate inherits these. `preview` is Optional[str] = None. So it's not required.
        self.assertIn("sender", missing_fields)
        self.assertIn("senderEmail", missing_fields)
        # self.assertIn("preview", missing_fields) # Preview is Optional
        self.assertIn("time", missing_fields)


    @patch('server.python_backend.main.ai_engine.analyze_email', new_callable=AsyncMock)
    @patch('server.python_backend.main.filter_manager.apply_filters_to_email', new_callable=AsyncMock)
    def test_create_email_db_error(self, mock_apply_filters, mock_analyze_email):
        print("Running test_create_email_db_error")
        email_data = {
            "sender": "test@example.com",
            "senderEmail": "test@example.com",
            "subject": "New Email",
            "content": "This is the content of the new email.",
            "preview": "New email preview", # Added to pass EmailCreate validation
            "time": "2023-10-26T10:00:00Z",
            # Fields from EmailCreate that are not Optional and have no defaults:
            # (sender, senderEmail, subject, content, time are from EmailBase)
            # isImportant, isStarred, isUnread, hasAttachments, attachmentCount, sizeEstimate all have defaults in EmailCreate
        }
        mock_ai_result = AIAnalysisResult(data={
            "topic": "general", "sentiment": "neutral", "intent": "informational", "urgency": "low",
            "confidence": 0.95, "categories": [], "keywords": ["new", "email"], "reasoning": "N/A",
            "suggested_labels": ["inbox"], "risk_flags": [], "category_id": 1,
            "action_items": []
        })
        mock_analyze_email.return_value = mock_ai_result
        mock_apply_filters.return_value = {"matched_filters": [], "applied_actions": []}

        mock_db_manager.create_email.side_effect = Exception("DB write error")

        response = self.client.post("/api/emails", json=email_data)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Failed to create email", response.json()["detail"])

    def test_update_email_success(self):
        print("Running test_update_email_success")
        email_id = 1
        email_update_payload = {"subject": "Updated Subject", "isUnread": False} # isUnread is in EmailUpdate

        # This mock should return data that is compatible with main.py's EmailResponse model
        mock_db_manager.update_email.return_value = {
            "id": email_id, "messageId": "msg1", "threadId": "thread1",
            "sender": "sender1@example.com", "senderEmail": "sender1@example.com",
            "subject": "Updated Subject", "content": "Content 1", "preview": "Preview 1",
            "time": "2023-01-01T10:00:00Z", "category": "CategoryA", "labels": ["label1"],
            "isImportant": False, "isStarred": False, "isUnread": False, "confidence": 80
        }
        response = self.client.put(f"/api/emails/{email_id}", json=email_update_payload)

        print(f"PUT /api/emails/{email_id} Response Status Code: {response.status_code}")
        try:
            print(f"PUT /api/emails/{email_id} Response JSON: {response.json()}")
        except Exception as e:
            print(f"PUT /api/emails/{email_id} Response Text: {response.text}")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["subject"], "Updated Subject")
        self.assertEqual(data["isUnread"], False)
        # The call to db.update_email in main.py is:
        # await db.update_email(email_id, email_update.dict(exclude_unset=True))
        # So, the mock should expect the payload with exclude_unset=True applied.
        # For `email_update_payload` this is the same.
        mock_db_manager.update_email.assert_called_once_with(email_id, email_update_payload)


    def test_update_email_not_found(self):
        print("Running test_update_email_not_found")
        email_id = 999
        email_update_payload = {"subject": "Updated Subject"}
        mock_db_manager.update_email.return_value = None # This signifies not found

        response = self.client.put(f"/api/emails/{email_id}", json=email_update_payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Email not found"})
        mock_db_manager.update_email.assert_called_once_with(email_id, email_update_payload)

    def test_update_email_validation_error(self):
        print("Running test_update_email_validation_error")
        email_update_payload = {"isImportant": "not-a-boolean"} # Invalid data type
        response = self.client.put("/api/emails/1", json=email_update_payload)
        self.assertEqual(response.status_code, 422)
        response_data = response.json()
        print(f"PUT /api/emails/1 Validation Error JSON: {response_data}")
        self.assertIn("detail", response_data)
        self.assertEqual(response_data['detail'][0]['type'], 'bool_parsing')
        # Location for Pydantic V2 for request body is typically ['body', <field_name>]
        self.assertEqual(response_data['detail'][0]['loc'], ['body', 'isImportant'])


    def test_update_email_db_error(self):
        print("Running test_update_email_db_error")
        email_id = 1
        email_update_payload = {"subject": "Updated Subject"}
        mock_db_manager.update_email.side_effect = Exception("DB update error")
        response = self.client.put(f"/api/emails/{email_id}", json=email_update_payload)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Failed to update email", response.json()["detail"])
        mock_db_manager.update_email.assert_called_once_with(email_id, email_update_payload)

if __name__ == '__main__':
    unittest.main()
