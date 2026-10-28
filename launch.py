#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script is a wrapper that forwards to the actual launch.py in the setup subtree.
It maintains backward compatibility for references to launch.py in the root directory.
"""

import os
import re
import subprocess
import sys

# Arguments are forwarded verbatim to the setup launcher. Arguments come from
# the invoking shell, so they are untrusted input: reject anything carrying a
# shell/control metacharacter before it reaches a child process. This is
# defence in depth -- subprocess.run(shell=False) already prevents shell
# interpretation -- but it also stops control characters from reaching the
# child's own argument parser.
_UNSAFE_ARG = re.compile(r"[;&|$`<>\x00-\x1f\x7f]")

# Path to the actual launch.py in the setup subtree
script_dir = os.path.dirname(os.path.abspath(__file__))
setup_launch_path = os.path.join(script_dir, "setup", "launch.py")


def main():
    """Forward all arguments to the actual launch.py in the setup directory."""
    if not os.path.exists(setup_launch_path):
        print(f"Error: setup/launch.py not found at {setup_launch_path}")
        return 1

    args = sys.argv[1:]
    for arg in args:
        if _UNSAFE_ARG.search(arg):
            print(f"Error: rejecting unsafe argument: {arg!r}", file=sys.stderr)
            return 2

    # setup/launch.py does `from setup.environment import ...`, which needs the
    # repository root on sys.path. Running it as a file puts setup/ on sys.path
    # instead, so the import fails with ModuleNotFoundError. Put the root on
    # PYTHONPATH so `setup` resolves as a package.
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        p for p in (script_dir, env.get("PYTHONPATH", "")) if p
    )
    result = subprocess.run([sys.executable, setup_launch_path, *args], env=env)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
