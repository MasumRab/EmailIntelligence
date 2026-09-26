
import pytest
import zipfile
import io
import os
from unittest.mock import MagicMock, AsyncMock, patch
from pathlib import Path
from src.core.plugin_manager import PluginManager, PluginMarketplaceEntry

@pytest.mark.asyncio
async def test_plugin_installation_zip_slip_prevention(tmp_path):
    """
    Test that the plugin manager rejects plugins with Zip Slip vulnerabilities
    (files containing '..' in their path).
    """
    # Setup
    plugins_dir = tmp_path / "plugins"
    plugin_manager = PluginManager(plugins_dir=plugins_dir)

    # Create a malicious zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        # Add a file with directory traversal
        # We use a filename that definitely looks like a traversal attack
        zf.writestr("../evil.txt", "malicious content")
        zf.writestr("good_plugin.json", "{}")

    zip_buffer.seek(0)

    # Mock download to write our malicious zip
    async def mock_download_file(url, dest_path):
        with open(dest_path, "wb") as f:
            f.write(zip_buffer.getvalue())

    # Mock marketplace entry
    plugin_info = PluginMarketplaceEntry(
        plugin_id="malicious_plugin",
        name="Malicious Plugin",
        version="1.0.0",
        author="Attacker",
        description="Evil",
        download_url="http://example.com/malicious.zip",
        checksum="ignore",
    )

    # Patch dependencies
    plugin_manager._download_file = AsyncMock(side_effect=mock_download_file)
    plugin_manager._verify_checksum = AsyncMock(return_value=True)
    plugin_manager._get_plugin_from_marketplace = AsyncMock(return_value=plugin_info)

    # Attempt installation
    # This should return False because of our fix
    result = await plugin_manager.install_plugin("malicious_plugin")

    assert result is False, "Plugin manager should reject plugins with unsafe file paths"

    # Verify the file was NOT created in the plugins directory
    # (Checking cleanup was successful and install didn't happen)
    assert not (plugins_dir / "evil.txt").exists()
    assert not (plugins_dir / "malicious_plugin").exists()
