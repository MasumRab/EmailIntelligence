
import pytest
import asyncio
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch
from src.core.plugin_manager import PluginManager, SecurityError

@pytest.fixture
def plugin_manager():
    return PluginManager(plugins_dir=Path("./test_plugins"))

@pytest.mark.asyncio
async def test_download_file_rejects_file_scheme(plugin_manager):
    """Test that _download_file rejects file:// URLs"""
    unsafe_url = "file:///etc/passwd"
    dest_path = Path("test_download.zip")

    with pytest.raises((ValueError, SecurityError), match="URL scheme must be http or https"):
        await plugin_manager._download_file(unsafe_url, dest_path)

@pytest.mark.asyncio
async def test_download_file_accepts_https_scheme(plugin_manager, tmp_path):
    """Test that _download_file accepts https:// URLs and downloads content using httpx"""
    url = "https://example.com/plugin.zip"
    dest_path = tmp_path / "plugin.zip"
    content = b"fake plugin content"

    # mock_stream must be an async context manager
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None

    async def async_iter():
        yield content
    mock_response.aiter_bytes.return_value = async_iter()

    mock_stream = MagicMock()
    mock_stream.__aenter__ = AsyncMock(return_value=mock_response)
    mock_stream.__aexit__ = AsyncMock(return_value=None)

    # mock_client must be an async context manager AND have a stream method
    mock_client = MagicMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)
    mock_client.stream.return_value = mock_stream

    with patch("httpx.AsyncClient", return_value=mock_client):
        await plugin_manager._download_file(url, dest_path)

    assert dest_path.exists()
    assert dest_path.read_bytes() == content
