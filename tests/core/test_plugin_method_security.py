import pytest
from src.core.plugin_manager import PluginManager, PluginSecurityLevel
from unittest.mock import MagicMock

class MockPlugin:
    def safe_method(self):
        return "safe"
    def _private_method(self):
        return "private"
    def __init__(self):
        pass

def test_validate_method_execution_allows_safe():
    pm = PluginManager()
    obj = MockPlugin()
    assert pm._validate_method_execution(obj, "safe_method", PluginSecurityLevel.STANDARD) == True

def test_validate_method_execution_rejects_private():
    pm = PluginManager()
    obj = MockPlugin()
    assert pm._validate_method_execution(obj, "_private_method", PluginSecurityLevel.STANDARD) == False

def test_validate_method_execution_rejects_dunder():
    pm = PluginManager()
    obj = MockPlugin()
    assert pm._validate_method_execution(obj, "__init__", PluginSecurityLevel.STANDARD) == False

def test_validate_method_execution_rejects_system():
    pm = PluginManager()
    obj = MockPlugin()
    assert pm._validate_method_execution(obj, "system", PluginSecurityLevel.STANDARD) == False
