import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from pathlib import Path
from src.core.plugin_manager import PluginManager

@pytest.mark.asyncio
async def test_download_file_ssrf_protection():
    """Test that _download_file rejects non-HTTP/HTTPS schemes."""
    manager = PluginManager()
    dest_path = Path("dummy_dest")

    # Test file scheme
    with pytest.raises(ValueError, match="Only HTTP/HTTPS protocols are supported"):
        await manager._download_file("file:///etc/passwd", dest_path)

    # Test ftp scheme
    with pytest.raises(ValueError, match="Only HTTP/HTTPS protocols are supported"):
        await manager._download_file("ftp://example.com/file", dest_path)

@pytest.mark.asyncio
async def test_download_file_valid_scheme():
    """Test that _download_file works with valid HTTP/HTTPS schemes."""
    manager = PluginManager()
    dest_path = Path("dummy_dest")
    url = "https://example.com/plugin.zip"

    # Mock the response
    mock_response = MagicMock()
    mock_response.status_code = 200
    # aiter_bytes needs to be an async iterator
    async def async_iter():
        yield b"chunk1"
        yield b"chunk2"
    mock_response.aiter_bytes.return_value = async_iter()
    mock_response.raise_for_status = MagicMock()

    # Mock the stream context manager
    mock_stream_ctx = MagicMock()
    mock_stream_ctx.__aenter__.return_value = mock_response
    mock_stream_ctx.__aexit__.return_value = None

    # Mock the client
    # client.stream(...) should return the context manager
    mock_client = MagicMock()
    mock_client.stream.return_value = mock_stream_ctx
    # client.__aenter__ should return self
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None

    # When httpx.AsyncClient() is called, it should return our mock client
    # Since we use 'async with httpx.AsyncClient()', the constructor returns an object
    # that has __aenter__ which returns the client.
    # But usually httpx.AsyncClient() returns the client instance directly, and that instance is an async context manager.

    # So httpx.AsyncClient() -> returns client instance.
    # client instance __aenter__ -> returns client instance.

    mock_client_instance = AsyncMock() # This is the object returned by httpx.AsyncClient()
    # But we want to control .stream which is synchronous method returning async context manager
    mock_client_instance.stream = MagicMock(return_value=mock_stream_ctx)

    # But wait, AsyncMock methods are async by default.
    # We need to ensure .stream is NOT async if we want to return the ctx directly.
    # OR if usage is `async with client.stream(...)`, it expects stream(...) to return an object with __aenter__

    # Let's simplify.

    with patch("httpx.AsyncClient", return_value=mock_client_instance) as MockClientCls:
        # MockClientCls() returns mock_client_instance
        # async with mock_client_instance:
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = None

        # Mock file opening
        m_open = mock_open()
        with patch("builtins.open", m_open):
            await manager._download_file(url, dest_path)

            # Verify client was called with correct args
            mock_client_instance.stream.assert_called_with("GET", url, follow_redirects=True)

            # Verify file was written
            handle = m_open()
            handle.write.assert_any_call(b"chunk1")
            handle.write.assert_any_call(b"chunk2")
