"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Plugins Package

Contains extensible plugin modules for the Email Intelligence Platform.
This package follows the plugin architecture pattern allowing for
custom processing nodes and extended functionality.
"""

# Import plugin classes to make them available at package level
from .base_plugin import BasePlugin, ProcessingNode, UIComponentPlugin

__all__ = ["BasePlugin", "UIComponentPlugin", "ProcessingNode"]
