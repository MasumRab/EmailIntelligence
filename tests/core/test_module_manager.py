"""
Tests for src/core/module_manager.py
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest


class TestModuleManager:
    """Tests for ModuleManager class."""

    def test_module_manager_initialization(self):
        """Test that ModuleManager initializes correctly."""
        from src.core.module_manager import ModuleManager
        
        app = MagicMock()
        gradio_app = MagicMock()
        manager = ModuleManager(app, gradio_app)
        
        assert manager.app is app
        assert manager.gradio_app is gradio_app
        assert manager.modules_dir.name == "modules"

    def test_modules_dir_path(self):
        """Test that modules directory path is set correctly."""
        from src.core.module_manager import ModuleManager
        
        app = MagicMock()
        gradio_app = MagicMock()
        manager = ModuleManager(app, gradio_app)
        
        # Should be in the parent directory
        expected = Path(__file__).resolve().parent.parent.parent / "modules"
        assert manager.modules_dir == expected

    def test_load_modules_handles_missing_directory(self):
        """Test load_modules handles missing modules directory gracefully."""
        from src.core.module_manager import ModuleManager
        
        app = MagicMock()
        gradio_app = MagicMock()
        
        with patch.object(ModuleManager, '__init__', lambda self, a, g: None):
            manager = ModuleManager(app, gradio_app)
            manager.modules_dir = Path("/nonexistent/path")
            manager.app = app
            manager.gradio_app = gradio_app
            
            # Should not raise, just log a warning
            manager.load_modules()

    @patch("src.core.module_manager.importlib.util")
    def test_load_module_without_init_file(self, mock_util):
        """Test loading a module without __init__.py file."""
        from src.core.module_manager import ModuleManager
        
        app = MagicMock()
        gradio_app = MagicMock()
        
        with patch.object(ModuleManager, '__init__', lambda self, a, g: None):
            manager = ModuleManager(app, gradio_app)
            manager.app = app
            manager.gradio_app = gradio_app
            
            # Create a mock module path without __init__.py
            module_path = MagicMock()
            module_path.name = "test_module"
            module_path.is_dir.return_value = True
            module_path.__truediv__ = lambda self, x: MagicMock(exists=MagicMock(return_value=False))
            
            manager._load_module(module_path)
            # Should not raise, just skip

    @patch("src.core.module_manager.importlib.util")
    def test_load_module_with_register_function(self, mock_util):
        """Test loading a module with a register function."""
        from src.core.module_manager import ModuleManager
        
        app = MagicMock()
        gradio_app = MagicMock()
        
        # Create mock module with register function
        mock_module = MagicMock()
        mock_module.register = MagicMock()
        
        # Create mock spec
        mock_spec = MagicMock()
        mock_spec.loader = MagicMock()
        
        # Setup mock module_from_spec
        mock_util.spec_from_file_location.return_value = mock_spec
        mock_util.module_from_spec.return_value = mock_module
        
        with patch.object(ModuleManager, '__init__', lambda self, a, g: None):
            manager = ModuleManager(app, gradio_app)
            manager.app = app
            manager.gradio_app = gradio_app
            
            module_path = MagicMock()
            module_path.name = "test_module"
            
            init_file = MagicMock()
            init_file.exists.return_value = True
            module_path.__truediv__ = lambda self, x: init_file
            
            with patch("sys.modules", {}):
                manager._load_module(module_path)
                
                # Check that register was called
                mock_module.register.assert_called_once()

    @patch("src.core.module_manager.importlib.util")
    def test_load_module_without_register_function(self, mock_util):
        """Test loading a module without a register function."""
        from src.core.module_manager import ModuleManager
        
        app = MagicMock()
        gradio_app = MagicMock()
        
        # Create mock module without register function
        mock_module = MagicMock()
        del mock_module.register  # Remove register attribute
        
        # Create mock spec
        mock_spec = MagicMock()
        mock_spec.loader = MagicMock()
        
        # Setup mock module_from_spec
        mock_util.spec_from_file_location.return_value = mock_spec
        mock_util.module_from_spec.return_value = mock_module
        
        with patch.object(ModuleManager, '__init__', lambda self, a, g: None):
            manager = ModuleManager(app, gradio_app)
            manager.app = app
            manager.gradio_app = gradio_app
            
            module_path = MagicMock()
            module_path.name = "test_module"
            
            init_file = MagicMock()
            init_file.exists.return_value = True
            module_path.__truediv__ = lambda self, x: init_file
            
            with patch("sys.modules", {}):
                # Should not raise, just log a warning
                manager._load_module(module_path)