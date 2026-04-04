#!/usr/bin/env python3
import os
import sys
import subprocess

# This is a shim to redirect calls from the root launch.py to setup/launch.py
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
setup_launch_path = os.path.join(project_root, "setup", "launch.py")

if __name__ == "__main__":
    if os.path.exists(setup_launch_path):
        # Forward all arguments to the actual launch.py in the setup directory
        # Add the script directory to Python path so imports work
        env = os.environ.copy()
        python_path = env.get('PYTHONPATH', '')
        if python_path:
            env['PYTHONPATH'] = f"{script_dir}:{python_path}"
        else:
            env['PYTHONPATH'] = script_dir

        cmd = [sys.executable, setup_launch_path] + sys.argv[1:]
        result = subprocess.run(cmd, env=env)
        sys.exit(result.returncode)
    else:
        print(f"Error: setup/launch.py not found at {setup_launch_path}")
        sys.exit(1)
