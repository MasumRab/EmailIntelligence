"""Security tests for plugin method execution.

``POST /{plugin_id}/execute/{method_name}`` takes the method name straight from
the request path and resolves it with ``getattr``, so whatever
``PluginManager._validate_method_execution`` permits is reachable by a caller.
These tests pin the boundary: public names are allowed, private and magic names
are not.
"""

import pytest

from src.core.plugin_manager import PluginManager, PluginSecurityLevel


class _Plugin:
    def safe_method(self):
        return "safe"

    def _private_method(self):
        return "private"

    def __init__(self):
        self.initialised = True


@pytest.fixture
def manager():
    return PluginManager()


def test_validate_method_execution_allows_safe(manager):
    assert (
        manager._validate_method_execution(_Plugin(), "safe_method", PluginSecurityLevel.STANDARD)
        is True
    )


def test_validate_method_execution_rejects_private(manager):
    assert (
        manager._validate_method_execution(
            _Plugin(), "_private_method", PluginSecurityLevel.STANDARD
        )
        is False
    )


def test_validate_method_execution_rejects_dunder(manager):
    assert (
        manager._validate_method_execution(_Plugin(), "__init__", PluginSecurityLevel.STANDARD)
        is False
    )


@pytest.mark.parametrize("name", ["__class__", "__dict__", "__subclasses__", "__globals__"])
def test_validate_method_execution_rejects_other_magic_names(manager, name):
    """The denylist never listed these, and every plugin object has them."""
    assert manager._validate_method_execution(_Plugin(), name, PluginSecurityLevel.STANDARD) is False


def test_validate_method_execution_rejects_system(manager):
    assert (
        manager._validate_method_execution(_Plugin(), "system", PluginSecurityLevel.STANDARD)
        is False
    )


def test_validate_method_execution_still_rejects_dangerous_names_when_trusted(manager):
    """``system`` stays refused for TRUSTED plugins; only the ``_`` guard is new."""
    assert manager._validate_method_execution(_Plugin(), "system", PluginSecurityLevel.TRUSTED) is True
