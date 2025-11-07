"""
Service Container for dependency injection.

This module implements a simple service container following the Dependency Injection
pattern to manage application services and their dependencies.
"""

from typing import Dict, Any, Optional, Type, TypeVar
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class ServiceContainer:
    """
    Simple service container for dependency injection.

    Provides registration and resolution of services with automatic
    dependency injection and singleton management.
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, callable] = {}
        self._singletons: Dict[str, Any] = {}

    def register(self, name: str, service: Any, singleton: bool = True) -> None:
        """
        Register a service instance.

        Args:
            name: Service name
            service: Service instance
            singleton: Whether this is a singleton service
        """
        self._services[name] = service
        if singleton:
            self._singletons[name] = service
        logger.debug(f"Registered service: {name}")

    def register_factory(self, name: str, factory: callable, singleton: bool = True) -> None:
        """
        Register a service factory function.

        Args:
            name: Service name
            factory: Factory function that returns service instance
            singleton: Whether the factory result should be cached as singleton
        """
        self._factories[name] = factory
        logger.debug(f"Registered factory: {name}")

    def resolve(self, name: str) -> Any:
        """
        Resolve a service by name.

        Args:
            name: Service name

        Returns:
            Service instance

        Raises:
            KeyError: If service is not registered
        """
        # Check singletons first
        if name in self._singletons:
            return self._singletons[name]

        # Check direct services
        if name in self._services:
            service = self._services[name]
            self._singletons[name] = service  # Cache as singleton
            return service

        # Check factories
        if name in self._factories:
            factory = self._factories[name]
            service = factory()
            self._singletons[name] = service  # Cache as singleton
            return service

        raise KeyError(f"Service '{name}' not registered")

    def has_service(self, name: str) -> bool:
        """
        Check if a service is registered.

        Args:
            name: Service name

        Returns:
            bool: True if service is registered
        """
        return (name in self._services or
                name in self._factories or
                name in self._singletons)

    def clear(self) -> None:
        """Clear all registered services and singletons."""
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()
        logger.debug("Cleared all services")

    def get_registered_services(self) -> list:
        """
        Get list of all registered service names.

        Returns:
            List of service names
        """
        return list(set(self._services.keys()) |
                   set(self._factories.keys()) |
                   set(self._singletons.keys()))


# Global container instance
_container: Optional[ServiceContainer] = None


def get_container() -> ServiceContainer:
    """Get the global service container instance."""
    global _container
    if _container is None:
        _container = ServiceContainer()
    return _container


def initialize_all_services(container: ServiceContainer) -> None:
    """
    Initialize all application services.

    Args:
        container: Service container to register services in
    """
    logger.info("Initializing application services...")

    # Import and register core services
    try:
        # Register test stages if available
        from setup.test_stages import test_stages
        container.register('test_stages', test_stages)
        logger.debug("Registered test_stages service")
    except ImportError:
        logger.warning("test_stages not available")

    # Register other services as needed
    # This would include database, AI engine, workflow engine, etc.

    logger.info("Service initialization complete")


def cleanup_all_services() -> None:
    """Clean up all services."""
    global _container
    if _container:
        _container.clear()
        _container = None
    logger.info("All services cleaned up")