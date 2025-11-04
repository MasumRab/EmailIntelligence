"""
Core module for the Email Intelligence Platform.

This module provides the foundational components for the platform's functionality.
"""

# Import core components
from .database import DatabaseManager
from .ai_engine import ModernAIEngine
from .notmuch_data_source import NotmuchDataSource
from .workflow_engine import Workflow, WorkflowRunner
from .advanced_workflow_engine import initialize_workflow_system, get_workflow_manager
from .smart_filter_manager import SmartFilterManager, get_smart_filter_manager
from .dynamic_model_manager import DynamicModelManager, get_model_manager
from .model_registry import ModelRegistry
from .plugin_manager import PluginManager, get_plugin_manager
from .models import Email, Category
from .settings import Settings, SettingsManager
from .exceptions import (
    EmailIntelligenceError,
    DatabaseError,
    AuthenticationError,
    ValidationError,
    WorkflowError,
)
from .constants import DEFAULT_CATEGORY_COLOR, DEFAULT_CATEGORIES
from .security import SecurityManager
from .performance_monitor import PerformanceMonitor
from .enhanced_caching import EnhancedCachingManager
from .enhanced_error_reporting import ErrorReporter
from .factory import DataSourceFactory

# Initialize core components
workflow_manager = initialize_workflow_system()

__all__ = [
    # Core components
    "DatabaseManager",
    "ModernAIEngine",
    "NotmuchDataSource",
    "Workflow",
    "WorkflowRunner",
    "SmartFilterManager",
    "DynamicModelManager",
    "ModelRegistry",
    "PluginManager",
    
    # Managers and factories
    "DataSourceFactory",
    "Settings",
    "SettingsManager",
    "SecurityManager",
    "PerformanceMonitor",
    "EnhancedCachingManager",
    "ErrorReporter",
    
    # Models
    "Email",
    "Category",
    
    # Constants
    "DEFAULT_CATEGORY_COLOR",
    "DEFAULT_CATEGORIES",
    
    # Exceptions
    "EmailIntelligenceError",
    "DatabaseError",
    "AuthenticationError",
    "ValidationError",
    "WorkflowError",
    
    # Functions
    "initialize_workflow_system",
    "get_workflow_manager",
    "get_smart_filter_manager",
    "get_model_manager",
    "get_plugin_manager",
]