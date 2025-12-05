import sys
from unittest.mock import MagicMock

# Mock google.generativeai before importing the module under test
sys.modules["google"] = MagicMock()
sys.modules["google.generativeai"] = MagicMock()

import pytest
from unittest.mock import patch
import os
from src.ai.gemini_client import GeminiClient

@pytest.fixture
def mock_genai():
    with patch("src.ai.gemini_client.genai") as mock:
        yield mock

@pytest.fixture
def mock_settings():
    with patch("src.ai.gemini_client.settings") as mock:
        mock.gemini_api_key = "test_key"
        mock.gemini_model = "gemini-test"
        yield mock

def test_init_success(mock_genai, mock_settings):
    """Test successful initialization of GeminiClient."""
    client = GeminiClient()
    assert client.model is not None
    mock_genai.configure.assert_called_with(api_key="test_key")
    mock_genai.GenerativeModel.assert_called_with("gemini-test")

def test_init_no_api_key(mock_genai):
    """Test initialization fails gracefully without API key."""
    with patch("src.ai.gemini_client.settings") as mock_settings:
        mock_settings.gemini_api_key = None
        with patch.dict("os.environ", {}, clear=True):
            client = GeminiClient()
            assert client.model is None

@pytest.mark.asyncio
async def test_generate_content_success(mock_genai, mock_settings):
    """Test successful content generation."""
    client = GeminiClient()
    
    # Mock the response
    mock_response = MagicMock()
    mock_response.text = "Generated content"
    
    # Mock generate_content_async
    async def async_response(*args, **kwargs):
        return mock_response
        
    client.model.generate_content_async = MagicMock(side_effect=async_response)
    
    result = await client.generate_content("prompt")
    assert result == "Generated content"
    client.model.generate_content_async.assert_called_with("prompt")

@pytest.mark.asyncio
async def test_generate_content_failure(mock_genai, mock_settings):
    """Test content generation failure handling."""
    client = GeminiClient()
    
    client.model.generate_content_async = MagicMock(side_effect=Exception("API Error"))
    
    result = await client.generate_content("prompt")
    assert result is None

@pytest.mark.asyncio
async def test_generate_content_not_initialized(mock_genai):
    """Test generate_content when client is not initialized."""
    with patch("src.ai.gemini_client.settings") as mock_settings:
        mock_settings.gemini_api_key = None
        with patch.dict("os.environ", {}, clear=True):
            client = GeminiClient()
            result = await client.generate_content("prompt")
            assert result is None
