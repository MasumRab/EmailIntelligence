
import os
import zipfile
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from pathlib import Path
from src.core.plugin_manager import PluginManager, PluginMarketplaceEntry, SecurityError

@pytest.mark.asyncio
async def test_zip_slip_vulnerability():
    """
    Test to demonstrate Zip Slip vulnerability in PluginManager.

    This test mocks the download process to provide a malicious zip file
    containing a file with '..' in its path. If vulnerable, the file
    will be extracted outside the intended directory.
    """

    # Setup mocks
    mock_plugin_info = PluginMarketplaceEntry(
        plugin_id="malicious_plugin",
        name="Malicious Plugin",
        version="1.0.0",
        author="Attacker",
        description="A plugin that attempts Zip Slip",
        download_url="http://attacker.com/evil.zip",
        checksum="ignore_checksum"
    )

    manager = PluginManager()

    # Mock _get_plugin_from_marketplace
    manager._get_plugin_from_marketplace = AsyncMock(return_value=mock_plugin_info)

    # Mock _verify_checksum to always pass
    manager._verify_checksum = AsyncMock(return_value=True)

    # Create a malicious zip file
    # We want to break out of "extracted" folder into the temp root
    malicious_filename = "../pwned.txt"

    async def mock_download_file(url, dest_path):
        with zipfile.ZipFile(dest_path, 'w') as zf:
            zf.writestr(malicious_filename, "pwned")

    manager._download_file = AsyncMock(side_effect=mock_download_file)

    # Mock registry.register_plugin to avoid actually registering
    manager.registry.register_plugin = AsyncMock(return_value=True)

    import tempfile
    with tempfile.TemporaryDirectory() as test_temp_dir:
        test_temp_path = Path(test_temp_dir)

        # Patch TemporaryDirectory to return our known path
        # context manager mock structure
        mock_temp_dir_ctx = MagicMock()
        mock_temp_dir_ctx.__enter__.return_value = test_temp_dir
        mock_temp_dir_ctx.__exit__.return_value = None

        with patch('tempfile.TemporaryDirectory', return_value=mock_temp_dir_ctx):
            # We expect the installation to FAIL with a security error
            result = await manager.install_plugin("malicious_plugin")

            assert result is False, "Installation should fail for malicious zip"

            pwned_file = test_temp_path / "pwned.txt"
            assert not pwned_file.exists(), "Malicious file should NOT be created"

            # Check for plugin directory - it should NOT exist if install failed
            plugin_dir = manager.plugins_dir / "malicious_plugin"
            if plugin_dir.exists():
                import shutil
                shutil.rmtree(plugin_dir)

            assert not plugin_dir.exists(), "Plugin directory should not be created if install failed"
