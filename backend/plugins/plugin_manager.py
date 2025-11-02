"""
It will be removed in a future release.

Plugin Manager for Email Intelligence Platform

Manages the loading, registration, and execution of plugins in the system.
"""

import importlib
import inspect
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from backend.plugins.base_plugin import BasePlugin, ProcessingNode, UIComponentPlugin

logger = logging.getLogger(__name__)


class PluginManager:
    """Manages all plugins in the system"""

    def __init__(self, plugins_dir: str = "backend/plugins"):
        self.plugins_dir = Path(plugins_dir)
        self._plugins: Dict[str, BasePlugin] = {}
        self._ui_plugins: Dict[str, UIComponentPlugin] = {}
        self._processing_nodes: Dict[str, ProcessingNode] = {}

    def load_plugins(self) -> bool:
        """Discover and load all plugins in the plugins directory"""
        try:
            # Import all Python files in the plugins directory
            for py_file in self.plugins_dir.glob("*.py"):
                if py_file.name == "__init__.py":
                    continue

                module_name = f"backend.plugins.{py_file.stem}"
                try:
                    module = importlib.import_module(module_name)

                    # Look for plugin classes in the module
                    for name, obj in inspect.getmembers(module):
                        if (
                            inspect.isclass(obj)
                            and obj != BasePlugin
                            and obj != UIComponentPlugin
                            and obj != ProcessingNode
                        ):
                            if issubclass(obj, ProcessingNode):
                                # Create an instance and register it
                                plugin_instance = obj()
                                self._processing_nodes[plugin_instance.name] = plugin_instance
                                logger.info(
                                    f"Loaded processing node plugin: {plugin_instance.name}"
                                )
                            elif issubclass(obj, UIComponentPlugin):
                                # Create an instance and register it
                                plugin_instance = obj()
                                self._ui_plugins[plugin_instance.name] = plugin_instance
                                logger.info(f"Loaded UI component plugin: {plugin_instance.name}")
                            elif issubclass(obj, BasePlugin):
                                # Create an instance and register it
                                plugin_instance = obj()
                                self._plugins[plugin_instance.name] = plugin_instance
                                logger.info(f"Loaded plugin: {plugin_instance.name}")

                except Exception as e:
                    logger.error(f"Error loading plugin from {py_file}: {str(e)}")
                    continue

            logger.info(
                f"Plugin loading completed. Total plugins: {len(self._plugins)}, "
                f"UI plugins: {len(self._ui_plugins)}, Processing nodes: {len(self._processing_nodes)}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to load plugins: {str(e)}")
            return False

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get a plugin by name"""
        return self._plugins.get(name)

    def get_ui_plugin(self, name: str) -> Optional[UIComponentPlugin]:
        """Get a UI component plugin by name"""
        return self._ui_plugins.get(name)

    def get_processing_node(self, name: str) -> Optional[ProcessingNode]:
        """Get a processing node by name"""
        return self._processing_nodes.get(name)

    def get_all_plugins(self) -> Dict[str, BasePlugin]:
        """Get all loaded plugins"""
        return self._plugins.copy()

    def get_all_ui_plugins(self) -> Dict[str, UIComponentPlugin]:
        """Get all loaded UI component plugins"""
        return self._ui_plugins.copy()

    def get_all_processing_nodes(self) -> Dict[str, ProcessingNode]:
        """Get all loaded processing nodes"""
        return self._processing_nodes.copy()

    def register_plugin(self, plugin: BasePlugin) -> bool:
        """Register a plugin instance directly"""
        try:
            if plugin.name in self._plugins:
                logger.warning(f"Plugin {plugin.name} already exists, replacing")

            self._plugins[plugin.name] = plugin
            logger.info(f"Registered plugin: {plugin.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to register plugin {plugin.name}: {str(e)}")
            return False

    def initialize_all_plugins(self) -> bool:
        """Initialize all loaded plugins"""
        success_count = 0
        total_count = 0

        # Initialize regular plugins
        for name, plugin in self._plugins.items():
            total_count += 1
            try:
                if plugin.initialize():
                    logger.info(f"Plugin {name} initialized successfully")
                    success_count += 1
                else:
                    logger.error(f"Plugin {name} failed to initialize")
            except Exception as e:
                logger.error(f"Error initializing plugin {name}: {str(e)}")

        # Initialize UI plugins
        for name, plugin in self._ui_plugins.items():
            total_count += 1
            try:
                if plugin.initialize():
                    logger.info(f"UI plugin {name} initialized successfully")
                    success_count += 1
                else:
                    logger.error(f"UI plugin {name} failed to initialize")
            except Exception as e:
                logger.error(f"Error initializing UI plugin {name}: {str(e)}")

        # Initialize processing nodes
        for name, plugin in self._processing_nodes.items():
            total_count += 1
            try:
                if plugin.initialize():
                    logger.info(f"Processing node {name} initialized successfully")
                    success_count += 1
                else:
                    logger.error(f"Processing node {name} failed to initialize")
            except Exception as e:
                logger.error(f"Error initializing processing node {name}: {str(e)}")

        logger.info(
            f"Initialization completed: {success_count}/{total_count} plugins initialized successfully"
        )
        return success_count == total_count


# Global plugin manager instance
plugin_manager = PluginManager()


def get_plugin_manager() -> PluginManager:
    """Get the global plugin manager instance"""
    return plugin_manager
