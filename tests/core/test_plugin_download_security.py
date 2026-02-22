
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path
from src.core.plugin_manager import PluginManager, SecurityError

@pytest.mark.asyncio
async def test_download_file_allows_http_and_https(tmp_path):
    # We mock httpx to avoid actual network calls
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        # Mock response context manager
        mock_response = MagicMock()
        mock_client.stream.return_value.__aenter__.return_value = mock_response
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        # Mock HEAD response for SSRF check
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_client.head = AsyncMock(return_value=mock_head_response)

        # Mock aiter_bytes to return an async iterator
        async def async_chunks():
            yield b"chunk1"
            yield b"chunk2"

        mock_response.aiter_bytes = lambda: async_chunks()

        pm = PluginManager(plugins_dir=tmp_path / "plugins")
        dest_path = tmp_path / "test_valid_download.zip"

        try:
            await pm._download_file("https://example.com/plugin.zip", dest_path)
            assert dest_path.exists()
            assert dest_path.read_bytes() == b"chunk1chunk2"
        finally:
            if dest_path.exists():
                dest_path.unlink()

@pytest.mark.asyncio
async def test_download_file_rejects_unsafe_schemes(tmp_path):
    pm = PluginManager(plugins_dir=tmp_path / "plugins")
    dest_path = tmp_path / "test_unsafe.zip"

    with pytest.raises(SecurityError, match="Invalid URL scheme"):
        await pm._download_file("ftp://example.com/plugin.zip", dest_path)

    with pytest.raises(SecurityError, match="Invalid URL scheme"):
        await pm._download_file("file:///etc/passwd", dest_path)

@pytest.mark.asyncio
async def test_download_file_timeout(tmp_path):
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        # Mock HEAD to pass
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_client.head = AsyncMock(return_value=mock_head_response)

        # Simulate timeout on stream
        mock_client.stream.side_effect = Exception("Timeout")

        pm = PluginManager(plugins_dir=tmp_path / "plugins")
        dest_path = tmp_path / "test_timeout.zip"

        # Should log error and raise
        with pytest.raises(Exception):
            await pm._download_file("https://example.com/slow.zip", dest_path)

@pytest.mark.asyncio
async def test_download_file_prevents_ssrf_redirects(tmp_path):
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = MagicMock()
        mock_client_cls.return_value.__aenter__.return_value = mock_client

        # Setup redirect chain: https -> ftp (unsafe)
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 302
        mock_response_1.headers = {"Location": "ftp://evil.com/payload"}

        mock_client.head = AsyncMock(return_value=mock_response_1)

        pm = PluginManager(plugins_dir=tmp_path / "plugins")
        dest_path = tmp_path / "test_ssrf.zip"

        with pytest.raises(SecurityError, match="Invalid redirect URL scheme"):
            await pm._download_file("https://example.com/redirect", dest_path)
