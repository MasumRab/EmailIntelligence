"""
Configuration for unit tests.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_real_settings():
    """Ensure the real settings module is used for all tests."""
    # Import the actual module first
    import importlib
    import src.config.settings as settings_module
    
    # Store a reference to the original module
    original_module = settings_module
    
    yield
    
    # Restore the original module after tests
    sys.modules['src.config.settings'] = original_module
