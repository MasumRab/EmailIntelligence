"""
Legacy Component - Maintained for Backward Compatibility.
Kept to preserve compatibility and to allow open PRs to migrate into the main architecture.
Planned migration: track related PRs; do not remove without explicit cross-team approval.

Plugins Package

Contains extensible plugin modules for the Email Intelligence Platform.
This package follows the plugin architecture pattern allowing for
custom processing nodes and extended functionality.
"""

# Import plugin classes to make them available at package level
from .base_plugin import BasePlugin, ProcessingNode, UIComponentPlugin

__all__ = ["BasePlugin", "UIComponentPlugin", "ProcessingNode"]
