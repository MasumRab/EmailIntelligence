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

# Arguments are forwarded to the setup launcher. Arguments come from the
# invoking shell, so they are untrusted input: only an allowlisted shape reaches
# the child process. This is defence in depth -- subprocess.run(shell=False)
# already prevents shell interpretation -- but it also stops control characters
# from reaching the child's own argument parser.
#
# The allowlist is matched, not merely tested: _safe_arg returns the matched
# text, so what reaches argv is the string the regex accepted. A boolean
# "reject if unsafe" check leaves the original value in the taint graph and the
# analyzer keeps reporting the sink.
_SAFE_ARG = re.compile(r"[A-Za-z0-9_./=:@+-]*")

# Path to the actual launch.py in the setup subtree
script_dir = os.path.dirname(os.path.abspath(__file__))
setup_launch_path = os.path.join(script_dir, "setup", "launch.py")


def _safe_arg(argument: str) -> str:
    """Return the argument, or raise if any character falls outside the allowlist."""
    match = _SAFE_ARG.fullmatch(argument)
    if not match:
        raise ValueError(argument)
    return match.group(0)


def main():
    """Forward all arguments to the actual launch.py in the setup directory."""
    if not os.path.exists(setup_launch_path):
        print(f"Error: setup/launch.py not found at {setup_launch_path}")
        return 1

    try:
        args = [_safe_arg(argument) for argument in sys.argv[1:]]
    except ValueError as rejected:
        print(
            f"Error: rejecting unsafe argument: {rejected.args[0]!r}", file=sys.stderr
        )
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
