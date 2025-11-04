"""
Model provider interface for Email Intelligence Platform
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class BaseModelProvider(ABC):
    """
    Abstract base class for all model providers in the platform.
    
    This class defines the standard interface that all model providers must
    implement. This ensures that different models and backends can be plugged
    into the application seamlessly.
    """
    
    @abstractmethod
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing sentiment analysis results
        """
        pass
    
    @abstractmethod
    async def analyze_topics(self, text: str) -> Dict[str, Any]:
        """
        Analyze topics in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing topic analysis results
        """
        pass
    
    @abstractmethod
    async def analyze_intent(self, text: str) -> Dict[str, Any]:
        """
        Analyze intent of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing intent analysis results
        """
        pass
    
    @abstractmethod
    async def analyze_urgency(self, text: str) -> Dict[str, Any]:
        """
        Analyze urgency of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing urgency analysis results
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the model provider.
        
        Returns:
            A dictionary containing the health status of the provider.
        """
        pass


class ModelProviderRegistry:
    """
    Registry for managing different model providers.
    """
    
    def __init__(self):
        self._providers: Dict[str, BaseModelProvider] = {}
        self._active_provider: Optional[str] = None
        logger.info("ModelProviderRegistry initialized")
    
    def register_provider(self, name: str, provider: BaseModelProvider) -> bool:
        """
        Register a model provider with the registry.
        
        Args:
            name: Name of the provider
            provider: Instance of the provider
            
        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self._providers[name] = provider
            if self._active_provider is None:
                self._active_provider = name
            logger.info(f"Registered model provider: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to register provider {name}: {e}")
            return False
    
    def get_provider(self, name: str) -> Optional[BaseModelProvider]:
        """
        Get a model provider by name.
        
        Args:
            name: Name of the provider
            
        Returns:
            The provider instance or None if not found
        """
        return self._providers.get(name)
    
    def get_active_provider(self) -> Optional[BaseModelProvider]:
        """
        Get the currently active model provider.
        
        Returns:
            The active provider instance or None if no active provider
        """
        if self._active_provider:
            return self._providers.get(self._active_provider)
        return None
    
    def set_active_provider(self, name: str) -> bool:
        """
        Set the active model provider by name.
        
        Args:
            name: Name of the provider to set as active
            
        Returns:
            True if successful, False otherwise
        """
        if name in self._providers:
            self._active_provider = name
            logger.info(f"Set active model provider to: {name}")
            return True
        else:
            logger.warning(f"Provider {name} not found in registry")
            return False
    
    def list_providers(self) -> List[str]:
        """
        List all registered model providers.
        
        Returns:
            List of provider names
        """
        return list(self._providers.keys())
    
    async def health_check_all(self) -> Dict[str, Any]:
        """
        Perform health check on all registered providers.
        
        Returns:
            Dictionary containing health check results for all providers
        """
        health_results = {}
        
        for name, provider in self._providers.items():
            try:
                health_results[name] = await provider.health_check()
            except Exception as e:
                health_results[name] = {
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": asyncio.get_event_loop().time()
                }
        
        return health_results


# Global registry instance
provider_registry = ModelProviderRegistry()


def register_provider(name: str, provider: BaseModelProvider) -> bool:
    """
    Register a model provider with the global registry.
    
    Args:
        name: Name of the provider
        provider: Instance of the provider
        
    Returns:
        True if registration was successful, False otherwise
    """
    return provider_registry.register_provider(name, provider)


def get_provider(name: str) -> Optional[BaseModelProvider]:
    """
    Get a model provider by name from the global registry.
    
    Args:
        name: Name of the provider
        
    Returns:
        The provider instance or None if not found
    """
    return provider_registry.get_provider(name)


def get_active_provider() -> Optional[BaseModelProvider]:
    """
    Get the currently active model provider from the global registry.
    
    Returns:
        The active provider instance or None if no active provider
    """
    return provider_registry.get_active_provider()


def set_active_provider(name: str) -> bool:
    """
    Set the active model provider by name in the global registry.
    
    Args:
        name: Name of the provider to set as active
        
    Returns:
        True if successful, False otherwise
    """
    return provider_registry.set_active_provider(name)


def list_providers() -> List[str]:
    """
    List all registered model providers in the global registry.
    
    Returns:
        List of provider names
    """
    return provider_registry.list_providers()