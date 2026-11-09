"""
Core module for EmailIntelligence CLI

This module provides minimal exports to avoid circular imports.
"""

# Minimal exports to avoid circular imports
# Full implementations are in their respective modules

__all__ = [
    "DatabaseManager",
    "ModernAIEngine",
    "NotmuchDataSource",
    "Workflow",
    "WorkflowRunner",
    "SmartFilterManager",
    "DynamicModelManager",
    "ModelRegistry",
    "PluginManager",
    "DataSourceFactory",
    "AuthManager",
    "SettingsManager",
    "SecurityManager",
    "PerformanceMonitor",
    "EnhancedCachingManager",
    "EnhancedErrorReporting",
    "Email",
    "Category",
    "DEFAULT_CATEGORY_COLOR",
    "DEFAULT_CATEGORIES",
    "EmailIntelligenceError",
    "DatabaseError",
    "AuthenticationError",
    "ValidationError",
    "WorkflowError",
    "initialize_workflow_system",
    "get_workflow_manager",
    "get_smart_filter_manager",
    "get_model_manager",
    "get_plugin_manager",
]
