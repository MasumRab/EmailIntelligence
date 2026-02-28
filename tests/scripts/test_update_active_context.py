import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import json

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import update_active_context
from update_active_context import get_repository, fetch_paginated, generate_context, DEGRADED_MESSAGE, API_ERROR_MESSAGE

class TestUpdateActiveContext(unittest.TestCase):

    @patch.dict(os.environ, {"GITHUB_REPOSITORY": "testowner/testrepo"}, clear=True)
    def test_get_repository_env_var(self):
        self.assertEqual(get_repository(), "testowner/testrepo")

    @patch.dict(os.environ, {}, clear=True)
    @patch("subprocess.run")
    def test_get_repository_git_config_https(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "https://github.com/gitowner/gitrepo.git\n"
        mock_run.return_value = mock_result

        self.assertEqual(get_repository(), "gitowner/gitrepo")
        mock_run.assert_called_once()
        called_args = mock_run.call_args[0][0]
        self.assertTrue(called_args[0].endswith("git"))
        self.assertEqual(called_args[1:], ["config", "--get", "remote.origin.url"])

    @patch.dict(os.environ, {}, clear=True)
    @patch("subprocess.run")
    def test_get_repository_git_config_ssh(self, mock_run):
        mock_result = MagicMock()
        mock_result.stdout = "git@github.com:sshowner/sshrepo.git\n"
        mock_run.return_value = mock_result

        self.assertEqual(get_repository(), "sshowner/sshrepo")

    @patch("requests.get")
    def test_fetch_paginated_single_page(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = [{"id": 1}, {"id": 2}]
        mock_response.headers.get.return_value = None # No Link header
        mock_get.return_value = mock_response

        items = fetch_paginated("http://api.example.com", {"Auth": "Token"})
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["id"], 1)

    @patch("requests.get")
    def test_fetch_paginated_multiple_pages(self, mock_get):
        # We need requests.get to return different responses based on the request URL
        def mock_get_side_effect(url, **kwargs):
            mock_response = MagicMock()
            if "page=2" in url:
                mock_response.json.return_value = [{"id": 3}]
                mock_response.headers.get.return_value = None
            else:
                mock_response.json.return_value = [{"id": 1}, {"id": 2}]
                # Mock the Link header to point to page 2
                mock_response.headers.get.return_value = '<http://api.example.com?page=2>; rel="next"'
            return mock_response

        mock_get.side_effect = mock_get_side_effect

        items = fetch_paginated("http://api.example.com?page=1", {"Auth": "Token"})
        self.assertEqual(len(items), 3)
        self.assertEqual(items[2]["id"], 3)
        self.assertEqual(mock_get.call_count, 2)

    @patch.dict(os.environ, {}, clear=True) # Ensure NO token
    @patch("update_active_context.write_context")
    def test_generate_context_missing_token_degraded_mode(self, mock_write):
        generate_context()
        mock_write.assert_called_once_with(DEGRADED_MESSAGE)

    @patch.dict(os.environ, {"GITHUB_TOKEN": "faketoken", "GITHUB_REPOSITORY": "owner/repo"}, clear=True)
    @patch("update_active_context.fetch_paginated")
    @patch("update_active_context.write_context")
    def test_generate_context_api_error_degraded_mode(self, mock_write, mock_fetch):
        # Simulate an API error during fetching
        import requests
        mock_fetch.side_effect = requests.RequestException("API rate limit exceeded")

        generate_context()
        mock_write.assert_called_once_with(API_ERROR_MESSAGE)

    @patch.dict(os.environ, {"GITHUB_TOKEN": "faketoken", "GITHUB_REPOSITORY": "owner/repo"}, clear=True)
    @patch("update_active_context.fetch_paginated")
    @patch("update_active_context.write_context")
    def test_generate_context_success(self, mock_write, mock_fetch):
        # First call fetches PRs, subsequent calls fetch files for those PRs
        def fetch_side_effect(url, headers):
            if "pulls?" in url:
                return [
                    {"number": 101, "title": "Add feature", "html_url": "http://pr1", "user": {"login": "dev1"}}
                ]
            elif "pulls/101/files" in url:
                return [
                    {"filename": "src/app.py", "status": "modified"},
                    {"filename": "tests/test_app.py", "status": "added"}
                ]
            return []

        mock_fetch.side_effect = fetch_side_effect

        generate_context()

        # Verify the write_context was called with the correctly formatted markdown
        mock_write.assert_called_once()
        written_content = mock_write.call_args[0][0]

        self.assertIn("# Active GitHub Context", written_content)
        self.assertIn("## [PR #101](http://pr1) - Add feature (by @dev1)", written_content)
        self.assertIn("- `src/app.py` (modified)", written_content)
        self.assertIn("- `tests/test_app.py` (added)", written_content)

if __name__ == "__main__":
    unittest.main()
