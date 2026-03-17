"""
Container and service initialization utilities.

Provides dependency injection container and service initialization for the EmailIntelligence application.
"""

from typing import Any


class Container:
    """
    Simple dependency injection container.
    
    This class manages the creation and lifecycle of application services.
    """
    
    def __init__(self):
        self._services = {}
        self._singletons = {}
    
    def register(self, name: str, service: Any, singleton: bool = False):
        """Register a service with the container."""
        if singleton:
            self._singletons[name] = service
        else:
            self._services[name] = service
    
    def get(self, name: str) -> Any:
        """Get a service from the container."""
        if name in self._singletons:
            return self._singletons[name]
        return self._services.get(name)
    
    def has(self, name: str) -> bool:
        """Check if a service is registered."""
        return name in self._services or name in self._singletons


def get_container() -> Container:
    """Get the application container."""
    if not hasattr(get_container, '_container'):
        get_container._container = Container()
    return get_container._container


def initialize_all_services(container: Container):
    """Initialize all services in the container."""
    # Placeholder implementation - in a real application, this would
    # initialize actual services like database connections, API clients, etc.
    pass