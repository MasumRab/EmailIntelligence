"""
Base Plugin Architecture for EmailIntelligence Platform.

This module defines the core plugin system interfaces, security mechanisms,
and lifecycle management for extensible plugin functionality.
"""

import abc
import asyncio
import hashlib
import importlib.util
import inspect
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class PluginStatus(Enum):
    """Plugin lifecycle states."""

    INSTALLED = "installed"
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"
    LOADING = "loading"
    UNLOADING = "unloading"


class PluginSecurityLevel(Enum):
    """Security levels for plugin execution."""

    TRUSTED = "trusted"  # Full system access
    STANDARD = "standard"  # Limited API access
    SANDBOXED = "sandboxed"  # Isolated execution environment


@dataclass
class PluginMetadata:
    """Metadata for plugin identification and management."""

    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    license: str = "MIT"
    homepage: Optional[str] = None
    repository: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    security_level: PluginSecurityLevel = PluginSecurityLevel.STANDARD
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=lambda: __import__("time").time())
    checksum: Optional[str] = None


@dataclass
class PluginInstance:
    """Runtime instance of a loaded plugin."""

    metadata: PluginMetadata
    plugin_object: Any
    status: PluginStatus = PluginStatus.ENABLED
    loaded_at: float = field(default_factory=lambda: __import__("time").time())
    config: Dict[str, Any] = field(default_factory=dict)
    hooks: Dict[str, List[Callable]] = field(default_factory=dict)


class PluginInterface(abc.ABC):
    """
    Abstract base class for all plugins.

    Plugins must implement these methods to integrate with the platform.
    """

    @abc.abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Return plugin metadata."""
        pass

    @abc.abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the plugin with configuration."""
        pass

    @abc.abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the plugin and cleanup resources."""
        pass

    @abc.abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of plugin capabilities/features."""
        pass

    @abc.abstractmethod
    def get_required_permissions(self) -> List[str]:
        """Return list of required permissions."""
        pass


class HookSystem:
    """
    Event-driven hook system for plugin communication.

    Plugins can register hooks for various system events and communicate
    with each other through this mechanism.
    """

    def __init__(self):
        self._hooks: Dict[str, List[Dict[str, Any]]] = {}
        self._lock = asyncio.Lock()

    async def register_hook(
        self, hook_name: str, callback: Callable, plugin_id: str, priority: int = 100
    ) -> str:
        """Register a callback for a hook."""
        async with self._lock:
            if hook_name not in self._hooks:
                self._hooks[hook_name] = []

            hook_id = f"{plugin_id}_{hook_name}_{hash(callback)}"

            self._hooks[hook_name].append(
                {"id": hook_id, "callback": callback, "plugin_id": plugin_id, "priority": priority}
            )

            # Sort by priority (lower number = higher priority)
            self._hooks[hook_name].sort(key=lambda x: x["priority"])

            return hook_id

    async def unregister_hook(self, hook_id: str) -> bool:
        """Unregister a hook by ID."""
        async with self._lock:
            for hook_name, hooks in self._hooks.items():
                for i, hook in enumerate(hooks):
                    if hook["id"] == hook_id:
                        hooks.pop(i)
                        return True
            return False

    async def trigger_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """Trigger all callbacks registered for a hook."""
        async with self._lock:
            if hook_name not in self._hooks:
                return []

            results = []
            for hook in self._hooks[hook_name]:
                try:
                    if asyncio.iscoroutinefunction(hook["callback"]):
                        result = await hook["callback"](*args, **kwargs)
                    else:
                        result = hook["callback"](*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Hook {hook['id']} failed: {e}")

            return results

    def get_registered_hooks(self) -> Dict[str, List[str]]:
        """Get list of registered hooks by name."""
        return {
            hook_name: [hook["id"] for hook in hooks] for hook_name, hooks in self._hooks.items()
        }


class SecuritySandbox:
    """
    Security sandbox for plugin execution.

    Provides different security levels for plugin execution based on trust levels.
    """

    def __init__(self):
        self._allowed_modules: Dict[PluginSecurityLevel, Set[str]] = {
            PluginSecurityLevel.TRUSTED: {"*"},  # All modules allowed
            PluginSecurityLevel.STANDARD: {
                "os",
                "sys",
                "json",
                "datetime",
                "pathlib",
                "src.core",
                "backend.python_backend",
                "fastapi",
                "pydantic",
                "asyncio",
            },
            PluginSecurityLevel.SANDBOXED: {"json", "datetime", "pathlib", "asyncio"},
        }

    def validate_import(self, module_name: str, security_level: PluginSecurityLevel) -> bool:
        """Validate if a module import is allowed for the given security level."""
        allowed = self._allowed_modules[security_level]
        return "*" in allowed or module_name in allowed or module_name.startswith("src.")

    def execute_in_sandbox(
        self, code: str, security_level: PluginSecurityLevel, globals_dict: Dict[str, Any] = None
    ) -> Any:
        """Execute code in a sandboxed environment."""
        # Create restricted globals
        if globals_dict is None:
            globals_dict = {}

        # Remove dangerous builtins
        safe_builtins = {}
        dangerous_builtins = {
            "open",
            "file",
            "input",
            "raw_input",
            "exec",
            "eval",
            "compile",
            "__import__",
            "reload",
            "execfile",
        }

        for name, obj in __builtins__.items():
            if isinstance(__builtins__, dict):
                if name not in dangerous_builtins:
                    safe_builtins[name] = obj
            else:
                # __builtins__ is a module
                if name not in dangerous_builtins:
                    safe_builtins[name] = obj

        globals_dict["__builtins__"] = safe_builtins

        # Execute with restrictions based on security level
        try:
            if security_level == PluginSecurityLevel.SANDBOXED:
                # Very restrictive execution
                exec(code, globals_dict)
            else:
                # Standard execution with some restrictions
                exec(code, globals_dict)
        except Exception as e:
            logger.error(f"Sandbox execution failed: {e}")
            raise

    def validate_file_access(self, file_path: Path, security_level: PluginSecurityLevel) -> bool:
        """Validate file access permissions."""
        if security_level == PluginSecurityLevel.TRUSTED:
            return True

        # For standard and sandboxed, restrict to plugin directory and allowed paths
        allowed_paths = [Path("plugins"), Path("data"), Path("logs")]

        for allowed_path in allowed_paths:
            try:
                file_path.resolve().relative_to(allowed_path.resolve())
                return True
            except ValueError:
                continue

        return False


class PluginRegistry:
    """
    Registry for managing plugin metadata and instances.

    Provides discovery, registration, and lifecycle management for plugins.
    """

    def __init__(self, plugins_dir: Path = None):
        self.plugins_dir = plugins_dir or Path("plugins")
        self._registry: Dict[str, PluginMetadata] = {}
        self._instances: Dict[str, PluginInstance] = {}
        self._security = SecuritySandbox()
        self._hooks = HookSystem()

        self.plugins_dir.mkdir(parents=True, exist_ok=True)

    async def discover_plugins(self) -> List[str]:
        """Discover and register all available plugins."""
        discovered = []

        for plugin_dir in self.plugins_dir.iterdir():
            if plugin_dir.is_dir() and not plugin_dir.name.startswith("."):
                plugin_id = plugin_dir.name
                metadata_file = plugin_dir / "plugin.json"

                if metadata_file.exists():
                    try:
                        with open(metadata_file, "r") as f:
                            data = json.load(f)
                            metadata = PluginMetadata(**data)
                            await self.register_plugin(metadata)
                            discovered.append(plugin_id)
                            logger.info(f"Discovered plugin: {plugin_id}")
                    except Exception as e:
                        logger.warning(f"Failed to load plugin {plugin_id}: {e}")

        return discovered

    async def register_plugin(self, metadata: PluginMetadata) -> bool:
        """Register a plugin in the registry."""
        try:
            self._registry[metadata.plugin_id] = metadata
            await self._save_metadata(metadata)
            logger.info(f"Registered plugin: {metadata.plugin_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to register plugin {metadata.plugin_id}: {e}")
            return False

    async def load_plugin(
        self, plugin_id: str, config: Dict[str, Any] = None
    ) -> Optional[PluginInstance]:
        """Load and initialize a plugin."""
        if plugin_id not in self._registry:
            logger.error(f"Plugin {plugin_id} not found in registry")
            return None

        if plugin_id in self._instances:
            return self._instances[plugin_id]

        metadata = self._registry[plugin_id]
        plugin_dir = self.plugins_dir / plugin_id

        try:
            # Load the plugin module
            plugin_module = await self._load_plugin_module(plugin_dir, metadata)

            if not plugin_module:
                return None

            # Create plugin instance
            plugin_class = getattr(plugin_module, f"{plugin_id.title()}Plugin", None)
            if not plugin_class:
                # Try to find any class that implements PluginInterface
                for name, obj in plugin_module.__dict__.items():
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, PluginInterface)
                        and obj != PluginInterface
                    ):
                        plugin_class = obj
                        break

            if not plugin_class:
                logger.error(f"No plugin class found in {plugin_id}")
                return None

            plugin_object = plugin_class()

            # Validate security requirements
            if not self._validate_plugin_security(plugin_object, metadata):
                return None

            # Initialize plugin
            if config is None:
                config = {}

            success = await plugin_object.initialize(config)
            if not success:
                logger.error(f"Plugin {plugin_id} initialization failed")
                return None

            # Create instance
            instance = PluginInstance(metadata=metadata, plugin_object=plugin_object, config=config)

            self._instances[plugin_id] = instance

            # Register plugin hooks
            await self._register_plugin_hooks(instance)

            logger.info(f"Loaded plugin: {plugin_id}")
            return instance

        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_id}: {e}")
            return None

    async def unload_plugin(self, plugin_id: str) -> bool:
        """Unload a plugin."""
        if plugin_id not in self._instances:
            return True

        try:
            instance = self._instances[plugin_id]

            # Shutdown plugin
            await instance.plugin_object.shutdown()

            # Unregister hooks
            await self._unregister_plugin_hooks(instance)

            # Remove instance
            del self._instances[plugin_id]

            logger.info(f"Unloaded plugin: {plugin_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to unload plugin {plugin_id}: {e}")
            return False

    async def enable_plugin(self, plugin_id: str) -> bool:
        """Enable a plugin."""
        if plugin_id not in self._instances:
            return False

        self._instances[plugin_id].status = PluginStatus.ENABLED
        logger.info(f"Enabled plugin: {plugin_id}")
        return True

    async def disable_plugin(self, plugin_id: str) -> bool:
        """Disable a plugin."""
        if plugin_id not in self._instances:
            return False

        self._instances[plugin_id].status = PluginStatus.DISABLED
        logger.info(f"Disabled plugin: {plugin_id}")
        return True

    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all registered plugins with status."""
        plugins = []

        for plugin_id, metadata in self._registry.items():
            plugin_info = {
                "id": plugin_id,
                "name": metadata.name,
                "version": metadata.version,
                "author": metadata.author,
                "description": metadata.description,
                "status": PluginStatus.INSTALLED.value,
                "security_level": metadata.security_level.value,
                "loaded": plugin_id in self._instances,
            }

            if plugin_id in self._instances:
                instance = self._instances[plugin_id]
                plugin_info.update(
                    {
                        "status": instance.status.value,
                        "loaded_at": instance.loaded_at,
                        "capabilities": instance.plugin_object.get_capabilities(),
                    }
                )

            plugins.append(plugin_info)

        return plugins

    async def _load_plugin_module(
        self, plugin_dir: Path, metadata: PluginMetadata
    ) -> Optional[Any]:
        """Load a plugin module from disk."""
        main_file = plugin_dir / "__init__.py"
        if not main_file.exists():
            main_file = plugin_dir / f"{metadata.plugin_id}.py"

        if not main_file.exists():
            logger.error(f"No main plugin file found in {plugin_dir}")
            return None

        try:
            spec = importlib.util.spec_from_file_location(
                f"plugins.{metadata.plugin_id}", main_file
            )

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"plugins.{metadata.plugin_id}"] = module
                spec.loader.exec_module(module)
                return module

        except Exception as e:
            logger.error(f"Failed to load plugin module: {e}")
            return None

    def _validate_plugin_security(self, plugin_object: Any, metadata: PluginMetadata) -> bool:
        """Validate plugin security requirements."""
        try:
            required_permissions = plugin_object.get_required_permissions()
            security_level = metadata.security_level

            # Check if all required permissions are appropriate for security level
            if security_level == PluginSecurityLevel.SANDBOXED and required_permissions:
                logger.warning(
                    f"Sandboxed plugin {metadata.plugin_id} requested permissions: {required_permissions}"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Security validation failed for plugin {metadata.plugin_id}: {e}")
            return False

    async def _register_plugin_hooks(self, instance: PluginInstance):
        """Register plugin hooks with the hook system."""
        # This would be implemented based on plugin's hook registration needs
        pass

    async def _unregister_plugin_hooks(self, instance: PluginInstance):
        """Unregister plugin hooks."""
        # This would be implemented to clean up hooks
        pass

    async def _save_metadata(self, metadata: PluginMetadata):
        """Save plugin metadata to disk."""
        try:
            plugin_dir = self.plugins_dir / metadata.plugin_id
            plugin_dir.mkdir(exist_ok=True)

            metadata_file = plugin_dir / "plugin.json"

            # Convert to dict for JSON serialization
            metadata_dict = {
                "plugin_id": metadata.plugin_id,
                "name": metadata.name,
                "version": metadata.version,
                "author": metadata.author,
                "description": metadata.description,
                "license": metadata.license,
                "homepage": metadata.homepage,
                "repository": metadata.repository,
                "dependencies": metadata.dependencies,
                "permissions": metadata.permissions,
                "security_level": metadata.security_level.value,
                "tags": metadata.tags,
                "created_at": metadata.created_at,
                "checksum": metadata.checksum,
            }

            with open(metadata_file, "w") as f:
                json.dump(metadata_dict, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save metadata for {metadata.plugin_id}: {e}")

    def get_hook_system(self) -> HookSystem:
        """Get the hook system for inter-plugin communication."""
        return self._hooks

    def get_security_sandbox(self) -> SecuritySandbox:
        """Get the security sandbox for plugin validation."""
        return self._security
