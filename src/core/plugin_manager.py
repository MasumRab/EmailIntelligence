"""
Dynamic Plugin Manager for EmailIntelligence Platform.

This module provides comprehensive plugin lifecycle management, security,
marketplace integration, and runtime monitoring for extensible functionality.
"""

import asyncio
import hashlib
import logging
import shutil
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from urllib.request import urlopen

from .plugin_base import (
    HookSystem,
    PluginInstance,
    PluginMetadata,
    PluginRegistry,
    PluginSecurityLevel,
    PluginStatus,
    SecuritySandbox,
)

logger = logging.getLogger(__name__)


@dataclass
class PluginMarketplaceEntry:
    """Entry in the plugin marketplace."""

    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    download_url: str
    checksum: str
    tags: List[str] = field(default_factory=list)
    rating: float = 0.0
    downloads: int = 0
    last_updated: float = field(default_factory=time.time)


class PluginManager:
    """
    Comprehensive plugin management system with marketplace integration,
    security, and lifecycle management.
    """

    def __init__(self, plugins_dir: Path = None, marketplace_url: str = None):
        self.plugins_dir = plugins_dir or Path("plugins")
        self.marketplace_url = (
            marketplace_url or "https://api.emailintelligence.plugins/marketplace"
        )
        self.registry = PluginRegistry(plugins_dir)
        self._marketplace_cache: Dict[str, PluginMarketplaceEntry] = {}
        self._marketplace_cache_time: float = 0
        self._cache_ttl = 3600  # 1 hour
        self._background_tasks: Set[asyncio.Task] = set()

        # Create plugins directory
        self.plugins_dir.mkdir(parents=True, exist_ok=True)

    async def initialize(self):
        """Initialize the plugin manager."""
        logger.info("Initializing PluginManager")

        # Discover installed plugins
        await self.registry.discover_plugins()

        # Start background monitoring
        self._start_background_tasks()

        logger.info("PluginManager initialized")

    async def shutdown(self):
        """Shutdown the plugin manager and cleanup."""
        logger.info("Shutting down PluginManager")

        # Cancel background tasks
        for task in self._background_tasks:
            task.cancel()

        # Wait for tasks to complete
        if self._background_tasks:
            await asyncio.gather(*self._background_tasks, return_exceptions=True)

        # Unload all plugins
        loaded_plugins = list(self.registry._instances.keys())
        for plugin_id in loaded_plugins:
            await self.unload_plugin(plugin_id)

        logger.info("PluginManager shutdown complete")

    async def install_plugin(self, plugin_id: str, version: str = None) -> bool:
        """Install a plugin from the marketplace."""
        try:
            # Get plugin info from marketplace
            plugin_info = await self._get_plugin_from_marketplace(plugin_id, version)
            if not plugin_info:
                logger.error(f"Plugin {plugin_id} not found in marketplace")
                return False

            # Download and install
            success = await self._download_and_install_plugin(plugin_info)
            if success:
                logger.info(f"Successfully installed plugin: {plugin_id}")
                # Auto-load if possible
                await self.load_plugin(plugin_id)
            return success

        except Exception as e:
            logger.error(f"Failed to install plugin {plugin_id}: {e}")
            return False

    async def uninstall_plugin(self, plugin_id: str) -> bool:
        """Uninstall a plugin completely."""
        try:
            # Unload if loaded
            await self.unload_plugin(plugin_id)

            # Remove from registry
            success = await self.registry._registry.pop(plugin_id, None) is not None

            if success:
                # Remove plugin directory
                plugin_dir = self.plugins_dir / plugin_id
                if plugin_dir.exists():
                    shutil.rmtree(plugin_dir)

                logger.info(f"Successfully uninstalled plugin: {plugin_id}")

            return success

        except Exception as e:
            logger.error(f"Failed to uninstall plugin {plugin_id}: {e}")
            return False

    async def load_plugin(
        self, plugin_id: str, config: Dict[str, Any] = None
    ) -> Optional[PluginInstance]:
        """Load a plugin into memory."""
        return await self.registry.load_plugin(plugin_id, config)

    async def unload_plugin(self, plugin_id: str) -> bool:
        """Unload a plugin from memory."""
        return await self.registry.unload_plugin(plugin_id)

    async def enable_plugin(self, plugin_id: str) -> bool:
        """Enable a plugin."""
        return await self.registry.enable_plugin(plugin_id)

    async def disable_plugin(self, plugin_id: str) -> bool:
        """Disable a plugin."""
        return await self.registry.disable_plugin(plugin_id)

    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all installed plugins."""
        return self.registry.list_plugins()

    async def get_plugin_info(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a plugin."""
        plugins = self.list_plugins()
        return next((p for p in plugins if p["id"] == plugin_id), None)

    async def update_plugin(self, plugin_id: str) -> bool:
        """Update a plugin to the latest version."""
        try:
            # Check if update is available
            current_version = None
            if plugin_id in self.registry._registry:
                current_version = self.registry._registry[plugin_id].version

            latest_info = await self._get_plugin_from_marketplace(plugin_id)
            if not latest_info or latest_info.version == current_version:
                logger.info(f"Plugin {plugin_id} is already up to date")
                return True

            # Install update
            logger.info(
                f"Updating plugin {plugin_id} from {current_version} to {latest_info.version}"
            )
            await self.uninstall_plugin(plugin_id)
            return await self.install_plugin(plugin_id, latest_info.version)

        except Exception as e:
            logger.error(f"Failed to update plugin {plugin_id}: {e}")
            return False

    async def validate_plugin(self, plugin_id: str) -> Dict[str, Any]:
        """Validate a plugin's integrity and security."""
        return await self.registry.validate_model(plugin_id)  # Reuse validation logic

    def get_hook_system(self) -> HookSystem:
        """Get the hook system for inter-plugin communication."""
        return self.registry.get_hook_system()

    def get_security_sandbox(self) -> SecuritySandbox:
        """Get the security sandbox."""
        return self.registry.get_security_sandbox()

    async def get_marketplace_plugins(
        self, refresh: bool = False
    ) -> List[Dict[str, Any]]:
        """Get available plugins from the marketplace."""
        try:
            if refresh or self._should_refresh_marketplace_cache():
                await self._refresh_marketplace_cache()

            plugins = []
            for plugin_id, entry in self._marketplace_cache.items():
                plugin_info = {
                    "id": entry.plugin_id,
                    "name": entry.name,
                    "version": entry.version,
                    "author": entry.author,
                    "description": entry.description,
                    "tags": entry.tags,
                    "rating": entry.rating,
                    "downloads": entry.downloads,
                    "installed": plugin_id in self.registry._registry,
                }

                if plugin_id in self.registry._registry:
                    installed_version = self.registry._registry[plugin_id].version
                    plugin_info["installed_version"] = installed_version
                    plugin_info["update_available"] = entry.version != installed_version

                plugins.append(plugin_info)

            return plugins

        except Exception as e:
            logger.error(f"Failed to get marketplace plugins: {e}")
            return []

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive plugin system status."""
        plugins = self.list_plugins()
        loaded_plugins = [p for p in plugins if p.get("loaded", False)]
        enabled_plugins = [p for p in loaded_plugins if p.get("status") == "enabled"]

        return {
            "total_plugins": len(plugins),
            "loaded_plugins": len(loaded_plugins),
            "enabled_plugins": len(enabled_plugins),
            "disabled_plugins": len(loaded_plugins) - len(enabled_plugins),
            "marketplace_available": bool(self._marketplace_cache),
            "background_tasks_active": len(self._background_tasks),
            "plugins_dir": str(self.plugins_dir),
            "security_levels": {
                level.value: len(
                    [p for p in plugins if p.get("security_level") == level.value]
                )
                for level in PluginSecurityLevel
            },
        }

    async def execute_plugin_method(
        self, plugin_id: str, method_name: str, *args, **kwargs
    ) -> Any:
        """Execute a method on a loaded plugin safely."""
        if plugin_id not in self.registry._instances:
            raise ValueError(f"Plugin {plugin_id} is not loaded")

        instance = self.registry._instances[plugin_id]
        if instance.status != PluginStatus.ENABLED:
            raise ValueError(f"Plugin {plugin_id} is not enabled")

        plugin_object = instance.plugin_object

        if not hasattr(plugin_object, method_name):
            raise ValueError(f"Plugin {plugin_id} does not have method {method_name}")

        method = getattr(plugin_object, method_name)

        # Execute with security validation
        security_level = instance.metadata.security_level
        if not self._validate_method_execution(
            plugin_object, method_name, security_level
        ):
            raise SecurityError(
                f"Method execution not allowed for security level {security_level}"
            )

        try:
            if asyncio.iscoroutinefunction(method):
                return await method(*args, **kwargs)
            else:
                return method(*args, **kwargs)
        except Exception as e:
            logger.error(
                f"Plugin method execution failed: {plugin_id}.{method_name}: {e}"
            )
            raise

    async def _get_plugin_from_marketplace(
        self, plugin_id: str, version: str = None
    ) -> Optional[PluginMarketplaceEntry]:
        """Get plugin information from marketplace."""
        try:
            if self._should_refresh_marketplace_cache():
                await self._refresh_marketplace_cache()

            if plugin_id not in self._marketplace_cache:
                return None

            entry = self._marketplace_cache[plugin_id]

            # Check version
            if version and entry.version != version:
                logger.warning(
                    f"Requested version {version} not available for {plugin_id}"
                )
                return None

            return entry

        except Exception as e:
            logger.error(f"Failed to get plugin from marketplace: {e}")
            return None

    async def _download_and_install_plugin(
        self, plugin_info: PluginMarketplaceEntry
    ) -> bool:
        """Download and install a plugin from the marketplace."""
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)

                # Download plugin archive
                download_path = temp_path / f"{plugin_info.plugin_id}.zip"
                await self._download_file(plugin_info.download_url, download_path)

                # Verify checksum
                if not await self._verify_checksum(download_path, plugin_info.checksum):
                    logger.error(
                        f"Checksum verification failed for {plugin_info.plugin_id}"
                    )
                    return False

                # Extract archive
                extract_path = temp_path / "extracted"
                extract_path.mkdir()

                with zipfile.ZipFile(download_path, "r") as zip_ref:
                    zip_ref.extractall(extract_path)

                # Move to plugins directory
                plugin_dir = self.plugins_dir / plugin_info.plugin_id
                if plugin_dir.exists():
                    shutil.rmtree(plugin_dir)

                # Find the plugin directory in extracted files
                extracted_dirs = [d for d in extract_path.iterdir() if d.is_dir()]
                if extracted_dirs:
                    shutil.move(str(extracted_dirs[0]), str(plugin_dir))
                else:
                    # Single file plugin
                    plugin_dir.mkdir()
                    for file_path in extract_path.iterdir():
                        if file_path.is_file():
                            shutil.move(
                                str(file_path), str(plugin_dir / file_path.name)
                            )

                # Register the plugin
                metadata = PluginMetadata(
                    plugin_id=plugin_info.plugin_id,
                    name=plugin_info.name,
                    version=plugin_info.version,
                    author=plugin_info.author,
                    description=plugin_info.description,
                )

                return await self.registry.register_plugin(metadata)

        except Exception as e:
            logger.error(
                f"Failed to download and install plugin {plugin_info.plugin_id}: {e}"
            )
            return False

    async def _download_file(self, url: str, dest_path: Path):
        """Download a file from URL."""
        try:
            with urlopen(url) as response:
                with open(dest_path, "wb") as f:
                    f.write(response.read())
        except Exception as e:
            logger.error(f"Failed to download file from {url}: {e}")
            raise

    async def _verify_checksum(self, file_path: Path, expected_checksum: str) -> bool:
        """Verify file checksum."""
        try:
            with open(file_path, "rb") as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            return file_hash == expected_checksum
        except Exception as e:
            logger.error(f"Failed to verify checksum: {e}")
            return False

    def _should_refresh_marketplace_cache(self) -> bool:
        """Check if marketplace cache should be refreshed."""
        return (time.time() - self._marketplace_cache_time) > self._cache_ttl

    async def _refresh_marketplace_cache(self):
        """Refresh the marketplace cache."""
        try:
            # This would make an actual API call to the marketplace
            # For now, we'll simulate with some example plugins
            self._marketplace_cache = {
                "sentiment_enhancer": PluginMarketplaceEntry(
                    plugin_id="sentiment_enhancer",
                    name="Advanced Sentiment Enhancer",
                    version="1.0.0",
                    author="EmailIntelligence Team",
                    description="Enhanced sentiment analysis with emoji and confidence scoring",
                    download_url="https://plugins.emailintelligence.com/sentiment_enhancer.zip",
                    checksum="dummy_checksum",
                    tags=["sentiment", "ai", "enhancement"],
                ),
                "email_filter_pro": PluginMarketplaceEntry(
                    plugin_id="email_filter_pro",
                    name="Professional Email Filter",
                    version="2.1.0",
                    author="Filter Experts Inc",
                    description="Advanced email filtering with machine learning",
                    download_url="https://plugins.emailintelligence.com/email_filter_pro.zip",
                    checksum="dummy_checksum_2",
                    tags=["filtering", "ml", "productivity"],
                ),
            }
            self._marketplace_cache_time = time.time()
            logger.info("Refreshed marketplace cache")

        except Exception as e:
            logger.error(f"Failed to refresh marketplace cache: {e}")

    def _validate_method_execution(
        self, plugin_object: Any, method_name: str, security_level: PluginSecurityLevel
    ) -> bool:
        """Validate if a method execution is allowed."""
        # Basic validation - could be enhanced
        dangerous_methods = ["__del__", "system", "exec", "eval", "__import__"]

        if method_name in dangerous_methods:
            if security_level in [
                PluginSecurityLevel.SANDBOXED,
                PluginSecurityLevel.STANDARD,
            ]:
                return False

        return True

    def _start_background_tasks(self):
        """Start background monitoring tasks."""
        # Plugin health monitoring
        health_task = asyncio.create_task(self._plugin_health_monitor())
        self._background_tasks.add(health_task)

        # Marketplace cache refresh
        cache_task = asyncio.create_task(self._marketplace_cache_refresher())
        self._background_tasks.add(cache_task)

    async def _plugin_health_monitor(self):
        """Monitor plugin health in the background."""
        while True:
            try:
                await asyncio.sleep(300)  # Check every 5 minutes

                for plugin_id in list(self.registry._instances.keys()):
                    try:
                        validation = await self.validate_plugin(plugin_id)
                        if not validation.get("valid", True):
                            logger.warning(
                                f"Plugin {plugin_id} health check failed: {validation}"
                            )
                    except Exception as e:
                        logger.error(f"Health check failed for plugin {plugin_id}: {e}")

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Plugin health monitor error: {e}")
                await asyncio.sleep(60)

    async def _marketplace_cache_refresher(self):
        """Refresh marketplace cache periodically."""
        while True:
            try:
                await asyncio.sleep(3600)  # Refresh every hour
                await self._refresh_marketplace_cache()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Marketplace cache refresh error: {e}")
                await asyncio.sleep(300)  # Retry in 5 minutes


class SecurityError(Exception):
    """Exception raised for plugin security violations."""

    pass


# Global plugin manager instance
_plugin_manager_instance: Optional['PluginManager'] = None


async def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance."""
    global _plugin_manager_instance
    if _plugin_manager_instance is None:
        _plugin_manager_instance = PluginManager()
        await _plugin_manager_instance._ensure_initialized()
    return _plugin_manager_instance
