"""
Service Container for dependency injection.

This module provides a simple service container that manages
dependencies and services for the launch system, following
the Dependency Inversion Principle.
"""

from typing import Any, Dict, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class ServiceContainer:
    """
    Simple service container for dependency injection.

    Provides registration and resolution of services, enabling
    loose coupling and testability.
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}
        self._singletons: Dict[str, Any] = {}

    def register(self, name: str, service: Any, singleton: bool = False) -> None:
        """
        Register a service instance.

        Args:
            name: Service name
            service: Service instance
            singleton: Whether this is a singleton service
        """
        if singleton:
            self._singletons[name] = service
        else:
            self._services[name] = service
        logger.debug(f"Registered service: {name}")

    def register_factory(self, name: str, factory: Callable[[], Any], singleton: bool = True) -> None:
        """
        Register a service factory.

        Args:
            name: Service name
            factory: Factory function that creates the service
            singleton: Whether to cache the created instance
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

        # Check regular services
        if name in self._services:
            return self._services[name]

        # Check factories
        if name in self._factories:
            service = self._factories[name]()
            if name in self._singletons:
                # Cache singleton
                pass  # Already cached above
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
                name in self._singletons or
                name in self._factories)

    def clear(self) -> None:
        """Clear all registered services."""
        self._services.clear()
        self._factories.clear()
        self._singletons.clear()
        logger.debug("Cleared all services")


# Global service container instance
_container: Optional[ServiceContainer] = None


def get_container() -> ServiceContainer:
    """Get the global service container instance."""
    global _container
    if _container is None:
        _container = ServiceContainer()
        initialize_services(_container)
    return _container


def initialize_services(container: ServiceContainer) -> None:
    """
    Initialize core services in the container.

    Args:
        container: Service container to initialize
    """
    # Import here to avoid circular imports
    from deployment.test_stages import test_stages

    # Register core services
    container.register('test_stages', test_stages, singleton=True)

    # Register logger
    container.register('logger', logging.getLogger('launcher'), singleton=True)

    logger.debug("Core services initialized")


def initialize_all_services(container: ServiceContainer) -> None:
    """
    Initialize all application services.

    Args:
        container: Service container to initialize
    """
    initialize_services(container)
    # Add additional service initialization here as needed


def cleanup_all_services(container: ServiceContainer) -> None:
    """
    Cleanup all services.

    Args:
        container: Service container to cleanup
    """
    try:
        # Add cleanup logic for services that need it
        container.clear()
        logger.debug("All services cleaned up")
    except Exception as e:
        logger.warning(f"Error during service cleanup: {e}")