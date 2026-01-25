import pytest
import os
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock
from src.core.plugin_manager import PluginManager, SecurityError

@pytest.mark.asyncio
async def test_download_file_rejects_unsafe_schemes():
    """Test that _download_file rejects non-http/https schemes."""
    manager = PluginManager()

    # Create a dummy file for file:// test
    dummy_file = Path("dummy_test_file.txt")
    dummy_file.touch()

    try:
        unsafe_url = f"file://{dummy_file.absolute()}"
        dest_path = Path("downloaded_file.txt")

        # Test file:// scheme
        # This is expected to FAIL before the fix if the code doesn't raise SecurityError
        with pytest.raises(SecurityError) as excinfo:
            await manager._download_file(unsafe_url, dest_path)
        assert "Invalid URL scheme" in str(excinfo.value)

        # Test ftp:// scheme
        with pytest.raises(SecurityError) as excinfo:
            await manager._download_file("ftp://example.com/file.zip", dest_path)
        assert "Invalid URL scheme" in str(excinfo.value)

    finally:
        if dummy_file.exists():
            dummy_file.unlink()
        if Path("downloaded_file.txt").exists():
            Path("downloaded_file.txt").unlink()

@pytest.mark.asyncio
async def test_download_file_uses_httpx():
    """Test that _download_file uses httpx for http/https schemes."""
    manager = PluginManager()
    dest_path = Path("test_download.zip")

    # Mock httpx.AsyncClient
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()

    # Mock aiter_bytes async iterator
    async def async_iter_bytes():
        yield b"chunk1"
        yield b"chunk2"

    mock_response.aiter_bytes = async_iter_bytes

    # Mock the client instance
    mock_client_instance = AsyncMock()
    mock_client_instance.get.return_value = mock_response
    mock_client_instance.__aenter__.return_value = mock_client_instance
    mock_client_instance.__aexit__.return_value = None

    # Mock built-in open
    mock_file = MagicMock()
    mock_file_ctx = MagicMock()
    mock_file_ctx.__enter__.return_value = mock_file
    mock_file_ctx.__exit__.return_value = None

    with patch("httpx.AsyncClient", return_value=mock_client_instance) as MockClient:
        with patch("builtins.open", return_value=mock_file_ctx):
            await manager._download_file("https://example.com/plugin.zip", dest_path)

            # Verify httpx usage
            MockClient.assert_called_once()
            mock_client_instance.get.assert_called_once()
            args, kwargs = mock_client_instance.get.call_args
            assert args[0] == "https://example.com/plugin.zip"
            assert kwargs.get("follow_redirects") is True
            assert kwargs.get("timeout") == 30.0

            # Verify file writing
            assert mock_file.write.call_count == 2
            mock_file.write.assert_any_call(b"chunk1")
            mock_file.write.assert_any_call(b"chunk2")
