
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
async def test_download_file_allows_http_and_https():
    # We mock httpx to avoid actual network calls
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        # Ensure stream is a MagicMock, not AsyncMock, because it returns a ContextManager, not a Coroutine
        mock_client.stream = MagicMock()

        mock_response = AsyncMock()
        mock_response.raise_for_status = MagicMock()

        # Mocking aiter_bytes
        async def mock_aiter_bytes():
            yield b"chunk1"
            yield b"chunk2"

        mock_response.aiter_bytes = mock_aiter_bytes
        mock_client.stream.return_value.__aenter__.return_value = mock_response

        pm = PluginManager()
        dest_path = Path("test_valid_download.zip")

        try:
            await pm._download_file("https://example.com/plugin.zip", dest_path)
            assert dest_path.exists()
            assert dest_path.read_bytes() == b"chunk1chunk2"
        finally:
            if dest_path.exists():
                dest_path.unlink()

@pytest.mark.asyncio
async def test_download_file_timeout():
    # Verify timeout configuration
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        # Same fix for stream
        mock_client.stream = MagicMock()

        pm = PluginManager()
        dest_path = Path("test_timeout.zip")

        # We assume the call fails or succeeds, but we check if timeout was passed
        mock_response = AsyncMock()
        mock_response.aiter_bytes = AsyncMock(return_value=[])
        mock_client.stream.return_value.__aenter__.return_value = mock_response

        try:
            await pm._download_file("https://example.com/slow.zip", dest_path)
        except:
            pass

        # Check that AsyncClient was initialized with timeout
        mock_client_cls.assert_called_with(timeout=30.0)
