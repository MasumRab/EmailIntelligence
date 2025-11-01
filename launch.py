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

if __name__ == "__main__":
    # Forward all arguments to the actual launch.py in the setup directory
    cmd = [sys.executable, setup_launch_path] + sys.argv[1:]
    result = subprocess.run(cmd)
    sys.exit(result.returncode)