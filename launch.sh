#!/bin/bash

# EmailIntelligence Launcher for Unix-based systems
# This script identifies a Python interpreter and executes launch.py.
# All environment setup (venv, dependencies) is handled by launch.py.

# Ensure launch.py exists
if [ ! -f "launch.py" ]; then
    echo "Error: launch.py not found in the current directory." >&2
    exit 1
fi

PYTHON_INTERP=""

# 1. Try python3.11
if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_INTERP="python3.11"
# 2. Fallback to python3
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_INTERP="python3"
else
    echo "Error: Python 3 (3.11 recommended) not found in PATH." >&2
    echo "Please install Python 3.11 or ensure it's accessible via 'python3.11' or 'python3'." >&2
    exit 1
fi

echo "Using Python interpreter: $PYTHON_INTERP"
"$PYTHON_INTERP" launch.py "$@"

EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo
    echo "The application exited with error code: $EXIT_CODE."
    # The read command is removed for non-interactive CI/CD,
    # but can be added back for local debugging if desired.
    # read -p "Press Enter to continue..."
fi

exit $EXIT_CODE
