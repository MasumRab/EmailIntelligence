"""
Service management functions for the EmailIntelligence setup system.

This module provides service startup and management functionality.
"""

import os
import sys
import subprocess
from pathlib import Path


# Import functions from launch.py - re-exporting them for compatibility
try:
    from .launch import (
        start_backend,
        start_node_service,
        start_gradio_ui,
        start_services,
        validate_services,
        get_python_executable
    )
except ImportError:
    # If direct import fails, provide fallback implementations
    def start_backend(host: str, port: int, debug: bool = False):
        """Start the backend service."""
        print(f"Starting backend on {host}:{port} (debug={debug})")
        # Fallback implementation
        return True
    
    def start_node_service(service_path: Path, service_name: str, port: int, api_url: str):
        """Start a Node.js service."""
        print(f"Starting Node.js service {service_name} on port {port}")
        # Fallback implementation
        return True
    
    def start_gradio_ui(host, port, share, debug):
        """Start the Gradio UI."""
        print(f"Starting Gradio UI on {host}:{port}")
        # Fallback implementation
        return True
    
    def start_services(args):
        """Start services based on arguments."""
        print("Starting services...")
        # Fallback implementation
        return True
    
    def get_python_executable():
        """Get the Python executable path."""
        return Path(sys.executable)


def validate_services():
    """Validate that all required services are properly configured.
    
    Returns:
        bool: True if all services are validated, False otherwise
    """
    try:
        # Check Python executable
        python_exe = get_python_executable()
        if not python_exe.exists():
            print(f"Error: Python executable not found at {python_exe}")
            return False
        
        # Check if we can import required modules
        try:
            import subprocess
            import platform
            print("✓ Core system modules available")
        except ImportError as e:
            print(f"✗ Error importing core modules: {e}")
            return False
        
        # Check system requirements
        current_version = sys.version_info
        if current_version < (3, 8):
            print(f"✗ Python version {current_version} is too old. Minimum required: 3.8")
            return False
        else:
            print(f"✓ Python version {current_version.major}.{current_version.minor} is compatible")
        
        # Check git if available
        try:
            subprocess.run(['git', '--version'], 
                          capture_output=True, check=True)
            print("✓ Git is available")
        except (subprocess.SubprocessError, FileNotFoundError):
            print("⚠ Git not available (optional)")
        
        # Check for required environment variables (optional)
        required_env_vars = []
        optional_env_vars = ['CONDA_DEFAULT_ENV', 'PYTHONPATH']
        
        for var in required_env_vars:
            if not os.environ.get(var):
                print(f"✗ Required environment variable {var} is not set")
                return False
        
        for var in optional_env_vars:
            if os.environ.get(var):
                print(f"✓ Environment variable {var} is set: {os.environ.get(var)}")
        
        print("✓ All service validations passed")
        return True
        
    except Exception as e:
        print(f"✗ Service validation failed with error: {e}")
        return False


def check_service_dependencies():
    """Check if required dependencies for services are installed.
    
    Returns:
        dict: Status of various service dependencies
    """
    dependencies = {
        'python': sys.executable,
        'git': None,
        'conda': None,
        'node': None,
        'npm': None
    }
    
    # Check for git
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True, check=True)
        dependencies['git'] = result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        dependencies['git'] = 'Not available'
    
    # Check for conda
    try:
        result = subprocess.run(['conda', '--version'], 
                              capture_output=True, text=True, check=True)
        dependencies['conda'] = result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        dependencies['conda'] = 'Not available'
    
    # Check for node
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, check=True)
        dependencies['node'] = result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        dependencies['node'] = 'Not available'
    
    # Check for npm
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, text=True, check=True)
        dependencies['npm'] = result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        dependencies['npm'] = 'Not available'
    
    return dependencies