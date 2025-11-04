"""
AI package for Email Intelligence Platform
"""

from .ai_engine import AdvancedAIEngine, AIAnalysisResult, get_ai_engine, get_active_ai_engine
from .model_provider import (
    BaseModelProvider,
    ModelProviderRegistry,
    register_provider,
    get_provider,
    get_active_provider,
    set_active_provider,
    list_providers
)
from .rule_based_provider import RuleBasedModelProvider
from .dynamic_model_provider import DynamicModelProvider

__all__ = [
    'AdvancedAIEngine',
    'AIAnalysisResult',
    'get_ai_engine',
    'get_active_ai_engine',
    'BaseModelProvider',
    'ModelProviderRegistry',
    'register_provider',
    'get_provider',
    'get_active_provider',
    'set_active_provider',
    'list_providers',
    'RuleBasedModelProvider',
    'DynamicModelProvider'
]