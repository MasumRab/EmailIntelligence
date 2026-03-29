"""Plugin Manager for Email Intelligence."""
from typing import Dict, List, Optional, Any

class PluginManager:
    """Manager for Email Intelligence plugins."""

    def __init__(self):
        self._plugins: Dict[str, Any] = {}

    def register(self, name: str, plugin: Any) -> None:
        """Register a plugin."""
        self._plugins[name] = plugin

    def get_plugin(self, name: str) -> Optional[Any]:
        """Get a registered plugin by name."""
        return self._plugins.get(name)

    def list_plugins(self) -> List[str]:
        """List all registered plugin names."""
        return list(self._plugins.keys())

    def unregister(self, name: str) -> bool:
        """Unregister a plugin."""
        if name in self._plugins:
            del self._plugins[name]
            return True
        return False
