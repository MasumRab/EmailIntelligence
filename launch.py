#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script is a wrapper that forwards to the actual launch.py in the setup subtree.
It maintains backward compatibility for references to launch.py in the root directory.
"""

import subprocess
import sys
import os

# Version constraints for consistency checks
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 13)

# Project root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the actual launch.py in the setup subtree
setup_launch_path = os.path.join(script_dir, 'setup', 'launch.py')

def download_nltk_data() -> None:
    """Download required NLTK datasets."""
    import nltk
    nltk.download("punkt")
    nltk.download("stopwords")

def create_venv() -> None:
    """Create a virtual environment."""
    import venv
    venv.create(".venv", with_pip=True)

def check_python_version() -> bool:
    """Verify Python version requirements."""
    return PYTHON_MIN_VERSION <= sys.version_info[:2] <= PYTHON_MAX_VERSION

def main():
    """Main entry point."""
    # Forward all arguments to the actual launch.py in the setup directory
    if os.path.exists(setup_launch_path):
        cmd = [sys.executable, setup_launch_path] + sys.argv[1:]
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
    else:
        print(f"Error: setup/launch.py not found at {setup_launch_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
