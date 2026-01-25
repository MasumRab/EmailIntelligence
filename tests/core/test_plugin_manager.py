
import asyncio
import os
import tempfile
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.core.plugin_manager import PluginManager, SecurityError

@pytest.mark.asyncio
async def test_download_file_security():
    """Test security fix for _download_file method."""

    # Setup
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = os.path.join(temp_dir, "test_file.txt")
        # Write some content
        with open(temp_path, "w") as f:
            f.write("Secret content")

        plugin_manager = PluginManager(plugins_dir=Path(temp_dir))
        dest_path = Path(temp_dir) / "downloaded.txt"

        # Test 1: file:// scheme should fail
        file_url = f"file://{temp_path}"

        with pytest.raises(SecurityError) as excinfo:
            await plugin_manager._download_file(file_url, dest_path)

        assert "Invalid URL scheme" in str(excinfo.value)
        assert "Only http and https are allowed" in str(excinfo.value)

        # Test 2: http:// scheme should pass validation (but fail download since URL is fake)
        # We mock urlopen to avoid actual network request and to verify it was called
        with patch('src.core.plugin_manager.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__enter__.return_value = mock_response
            mock_response.read.return_value = b"fake zip content"
            mock_urlopen.return_value = mock_response

            await plugin_manager._download_file("http://example.com/plugin.zip", dest_path)

            # Verify urlopen was called with correct args including timeout
            mock_urlopen.assert_called_once()
            args, kwargs = mock_urlopen.call_args
            assert args[0] == "http://example.com/plugin.zip"
            assert kwargs.get('timeout') == 30
