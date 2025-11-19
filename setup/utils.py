"""
Utility functions for the EmailIntelligence setup system.

This module contains shared utility functions used across the setup system.
"""

import platform
import sys
import os
from pathlib import Path


def print_system_info():
    """Print detailed system, Python, and project configuration information."""
    print("=== System Information ===")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Project Root: {Path(__file__).parent.parent}")
    
    # Check environment variables
    python_path = os.environ.get('PYTHONPATH', 'Not set')
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'Not in conda environment')
    
    print(f"Python Path: {python_path}")
    print(f"Conda Environment: {conda_env}")
    
    # Check git information
    try:
        import subprocess
        result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], 
                              capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        if result.returncode == 0:
            print(f"Git Commit: {result.stdout.strip()}")
        else:
            print("Git: Not in a git repository or git not available")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Git: Not available")
    
    print("=========================")


def process_manager():
    """Basic process management utility function."""
    # This is a placeholder for any process management functionality
    # that might be needed in the future
    return {
        'status': 'active',
        'version': '1.0.0'
    }