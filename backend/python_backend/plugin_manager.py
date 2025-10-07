"""
Plugin Manager for the Email Intelligence Platform

This module provides a system for discovering, loading, and managing
external plugins.
"""
import logging
import os
import importlib.util
from typing import List

logger = logging.getLogger(__name__)

class PluginManager:
    """
    Manages the discovery and loading of plugins.
    """
    def __init__(self, plugin_folder: str = "plugins/"):
        self.plugin_folder = plugin_folder
        self.loaded_plugins = []

    def discover_and_load_plugins(self, **kwargs):
        """
        Scans the plugin folder, loads valid plugins, and calls their
        `register` function.
        """
        logger.info(f"Discovering plugins in '{self.plugin_folder}'...")
        if not os.path.exists(self.plugin_folder):
            logger.warning(f"Plugin folder '{self.plugin_folder}' not found. Skipping plugin loading.")
            return

        for item in os.listdir(self.plugin_folder):
            item_path = os.path.join(self.plugin_folder, item)
            if os.path.isdir(item_path):
                plugin_init_file = os.path.join(item_path, "__init__.py")
                if os.path.exists(plugin_init_file):
                    self._load_plugin(item, plugin_init_file, **kwargs)

        logger.info(f"Discovered and loaded {len(self.loaded_plugins)} plugins.")

    def _load_plugin(self, plugin_name: str, file_path: str, **kwargs):
        """
        Loads a single plugin and calls its register function.
        """
        try:
            # Dynamically import the plugin module
            module_name = f"plugins.{plugin_name}"
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            plugin_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin_module)

            # Call the plugin's register function if it exists
            if hasattr(plugin_module, "register"):
                plugin_module.register(**kwargs)
                self.loaded_plugins.append(plugin_name)
                logger.info(f"Successfully registered plugin: '{plugin_name}'")
            else:
                logger.warning(f"Plugin '{plugin_name}' does not have a 'register' function.")

        except Exception as e:
            logger.error(f"Failed to load plugin '{plugin_name}': {e}", exc_info=True)