"""
Tests for src/core/plugin_base.py
"""

import pytest
import time
from src.core.plugin_base import (
    PluginStatus,
    PluginSecurityLevel,
    PluginMetadata,
)


class TestPluginStatus:
    """Tests for PluginStatus enum."""

    def test_plugin_status_values(self):
        """Test all PluginStatus enum values exist."""
        expected = ["installed", "enabled", "disabled", "error", "loading", "unloading"]
        actual = [status.value for status in PluginStatus]
        
        assert sorted(actual) == sorted(expected)

    def test_plugin_status_installed(self):
        """Test INSTALLED status."""
        assert PluginStatus.INSTALLED.value == "installed"

    def test_plugin_status_enabled(self):
        """Test ENABLED status."""
        assert PluginStatus.ENABLED.value == "enabled"

    def test_plugin_status_disabled(self):
        """Test DISABLED status."""
        assert PluginStatus.DISABLED.value == "disabled"

    def test_plugin_status_error(self):
        """Test ERROR status."""
        assert PluginStatus.ERROR.value == "error"

    def test_plugin_status_loading(self):
        """Test LOADING status."""
        assert PluginStatus.LOADING.value == "loading"

    def test_plugin_status_unloading(self):
        """Test UNLOADING status."""
        assert PluginStatus.UNLOADING.value == "unloading"


class TestPluginSecurityLevel:
    """Tests for PluginSecurityLevel enum."""

    def test_security_level_values(self):
        """Test all PluginSecurityLevel enum values exist."""
        expected = ["trusted", "standard", "sandboxed"]
        actual = [level.value for level in PluginSecurityLevel]
        
        assert sorted(actual) == sorted(expected)

    def test_security_level_trusted(self):
        """Test TRUSTED security level."""
        assert PluginSecurityLevel.TRUSTED.value == "trusted"

    def test_security_level_standard(self):
        """Test STANDARD security level."""
        assert PluginSecurityLevel.STANDARD.value == "standard"

    def test_security_level_sandboxed(self):
        """Test SANDBOXED security level."""
        assert PluginSecurityLevel.SANDBOXED.value == "sandboxed"


class TestPluginMetadata:
    """Tests for PluginMetadata dataclass."""

    def test_plugin_metadata_required_fields(self):
        """Test PluginMetadata with required fields only."""
        metadata = PluginMetadata(
            plugin_id="test_plugin",
            name="Test Plugin",
            version="1.0.0",
            author="Test Author",
            description="A test plugin",
        )
        
        assert metadata.plugin_id == "test_plugin"
        assert metadata.name == "Test Plugin"
        assert metadata.version == "1.0.0"
        assert metadata.author == "Test Author"
        assert metadata.description == "A test plugin"

    def test_plugin_metadata_default_values(self):
        """Test PluginMetadata default values."""
        before = time.time()
        metadata = PluginMetadata(
            plugin_id="default_test",
            name="Default Test",
            version="0.1.0",
            author="Default",
            description="Test",
        )
        after = time.time()
        
        assert metadata.license == "MIT"
        assert metadata.homepage is None
        assert metadata.repository is None
        assert metadata.dependencies == []
        assert metadata.permissions == []
        assert metadata.security_level == PluginSecurityLevel.STANDARD
        assert metadata.tags == []
        assert metadata.checksum is None
        assert before <= metadata.created_at <= after

    def test_plugin_metadata_all_fields(self):
        """Test PluginMetadata with all fields."""
        metadata = PluginMetadata(
            plugin_id="full_plugin",
            name="Full Plugin",
            version="2.0.0",
            author="Full Author",
            description="A fully configured plugin",
            license="Apache-2.0",
            homepage="https://example.com",
            repository="https://github.com/example/plugin",
            dependencies=["dep1", "dep2"],
            permissions=["read", "write"],
            security_level=PluginSecurityLevel.TRUSTED,
            tags=["email", "ai", "filter"],
            checksum="abc123",
        )
        
        assert metadata.plugin_id == "full_plugin"
        assert metadata.license == "Apache-2.0"
        assert metadata.homepage == "https://example.com"
        assert metadata.repository == "https://github.com/example/plugin"
        assert metadata.dependencies == ["dep1", "dep2"]
        assert metadata.permissions == ["read", "write"]
        assert metadata.security_level == PluginSecurityLevel.TRUSTED
        assert metadata.tags == ["email", "ai", "filter"]
        assert metadata.checksum == "abc123"

    def test_plugin_metadata_custom_security_level(self):
        """Test PluginMetadata with custom security level."""
        metadata = PluginMetadata(
            plugin_id="sandboxed_plugin",
            name="Sandboxed Plugin",
            version="1.0.0",
            author="Sandboxed Author",
            description="A sandboxed plugin",
            security_level=PluginSecurityLevel.SANDBOXED,
        )
        
        assert metadata.security_level == PluginSecurityLevel.SANDBOXED