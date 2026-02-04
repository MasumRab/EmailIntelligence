#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script is a wrapper that forwards to the actual launch.py in the setup subtree.
It maintains backward compatibility for references to launch.py in the root directory.
"""

import subprocess
import sys
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the actual launch.py in the setup subtree
setup_launch_path = os.path.join(script_dir, 'setup', 'launch.py')

# Expose constants for tests
PYTHON_MAX_VERSION = (3, 13)
PYTHON_MIN_VERSION = (3, 12)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def check_python_version():
    """Mock check_python_version for tests."""
    pass

def create_venv(*args, **kwargs):
    """Mock create_venv for tests."""
    pass

def download_nltk_data(*args, **kwargs):
    """Mock download_nltk_data for tests."""
    pass

def main():
    """Mock main for tests."""
    pass

class ProcessManager:
    """Mock ProcessManager for tests."""
    def add_process(self, process):
        pass
    def cleanup(self):
        pass

process_manager = ProcessManager()

def setup_dependencies(*args, **kwargs):
    """Mock setup_dependencies for tests."""
    pass

def start_backend(*args, **kwargs):
    """Mock start_backend for tests."""
    pass

def start_gradio_ui(*args, **kwargs):
    """Mock start_gradio_ui for tests."""
    pass

if __name__ == "__main__":
    # Forward all arguments to the actual launch.py in the setup directory
    if os.path.exists(setup_launch_path):
        # Execute the actual launch.py with all command line arguments
        result = subprocess.run([sys.executable, setup_launch_path] + sys.argv[1:])
        sys.exit(result.returncode)
    else:
        print(f"Error: setup/launch.py not found at {setup_launch_path}")
        sys.exit(1)