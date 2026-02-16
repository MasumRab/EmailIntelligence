
import pytest
import asyncio
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock
from src.core.plugin_manager import PluginManager, SecurityError

@pytest.mark.asyncio
async def test_download_file_rejects_file_scheme():
    pm = PluginManager()
    dest_path = Path("test_dest.zip")
    url = "file:///etc/passwd"

    # We need to ensure that the method is actually called and fails
    # The current implementation of _download_file is async
    with pytest.raises(SecurityError, match="Invalid URL scheme: file"):
        await pm._download_file(url, dest_path)

@pytest.mark.asyncio
async def test_download_file_rejects_ftp_scheme():
    pm = PluginManager()
    dest_path = Path("test_dest.zip")
    url = "ftp://example.com/file.zip"

    with pytest.raises(SecurityError, match="Invalid URL scheme: ftp"):
        await pm._download_file(url, dest_path)

@pytest.mark.asyncio
async def test_download_file_allows_http_and_https(tmp_path):
    # We mock httpx to avoid actual network calls
    with patch("httpx.AsyncClient") as mock_client_cls:
        # The context manager returns the client instance
        mock_client_instance = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client_instance

        # Mock the stream method to return a response context manager
        # client.stream(...) is a synchronous call returning an async context manager
        # So stream must be a MagicMock, not AsyncMock
        mock_client_instance.stream = MagicMock()

        # The response object itself
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()

        # Mocking aiter_bytes as an async generator
        async def mock_aiter_bytes():
            yield b"chunk1"
            yield b"chunk2"

        # Assign the generator function to side_effect
        mock_response.aiter_bytes.side_effect = mock_aiter_bytes

        # The stream method returns an async context manager that yields the response
        mock_stream_ctx = AsyncMock()
        mock_stream_ctx.__aenter__.return_value = mock_response
        mock_client_instance.stream.return_value = mock_stream_ctx

        pm = PluginManager()
        dest_path = tmp_path / "test_valid_download.zip"

        await pm._download_file("https://example.com/plugin.zip", dest_path)

        assert dest_path.exists()
        assert dest_path.read_bytes() == b"chunk1chunk2"


@pytest.mark.asyncio
async def test_download_file_timeout(tmp_path):
    # Verify timeout configuration
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client_instance = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client_instance

        # Explicitly set stream as MagicMock
        mock_client_instance.stream = MagicMock()

        # Setup minimal response mock
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()

        async def mock_aiter_bytes():
            yield b""

        mock_response.aiter_bytes.side_effect = mock_aiter_bytes

        mock_stream_ctx = AsyncMock()
        mock_stream_ctx.__aenter__.return_value = mock_response
        mock_client_instance.stream.return_value = mock_stream_ctx

        pm = PluginManager()
        dest_path = tmp_path / "test_timeout.zip"

        await pm._download_file("https://example.com/slow.zip", dest_path)

        # Check that AsyncClient was initialized with timeout
        mock_client_cls.assert_called_with(timeout=30.0)
