"""
DEPRECATED: This module is part of the deprecated `backend` package.
It will be removed in a future release.

Base Plugin Interface for Email Intelligence Platform

Defines the standard interface for creating plugins in the modular system.
This follows patterns similar to leading AI frameworks like ComfyUI.
"""

from abc import ABC, abstractmethod
from typing import Any

import gradio as gr


class BasePlugin(ABC):
    """
    Abstract base class for all plugins in the Email Intelligence Platform.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of the plugin."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Version of the plugin."""
        pass

    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the plugin.
        Returns True if initialization was successful, False otherwise.
        """
        pass

    @abstractmethod
    def process(self, data: Any) -> Any:
        """
        Process the input data and return the result.
        """
        pass

    def get_config_schema(self) -> dict[str, Any]:
        """
        Return the configuration schema for this plugin.
        Override this method to provide custom configuration requirements.
        """
        return {}

    def validate_config(self, config: dict[str, Any]) -> bool:
        """
        Validate the plugin configuration.
        """
        return True


class UIComponentPlugin(BasePlugin):
    """
    Base class for plugins that provide UI components for the Gradio interface.
    """

    @abstractmethod
    def get_ui_components(self) -> list[gr.components.Component]:
        """
        Return Gradio UI components that this plugin provides.
        """
        pass

    @abstractmethod
    def get_input_widgets(self) -> list[gr.components.Component]:
        """
        Return custom input widgets that this plugin provides.
        """
        pass

    @abstractmethod
    def get_visualization_components(self) -> list[gr.components.Component]:
        """
        Return visualization components for displaying results.
        """
        pass

    @abstractmethod
    def register_custom_events(self, blocks: gr.Blocks) -> None:
        """
        Register any custom Gradio events that this plugin needs.
        """
        pass


class ProcessingNode(BasePlugin):
    """
    Base class for processing nodes in the node-based workflow system.
    Similar to ComfyUI's node architecture.
    """

    @property
    @abstractmethod
    def input_types(self) -> dict[str, type]:
        """Define expected input types for this node."""
        pass

    @property
    @abstractmethod
    def output_types(self) -> dict[str, type]:
        """Define output types for this node."""
        pass

    @abstractmethod
    def run(self, **kwargs) -> dict[str, Any]:
        """
        Execute the node with the provided inputs.
        Returns a dictionary of outputs based on output_types.
        """
        pass

    def get_ui_elements(self) -> dict[str, Any] | None:
        """
        Return UI elements for configuring this node in the workflow editor.
        Override this method to provide custom UI for node configuration.
        """
        return None
