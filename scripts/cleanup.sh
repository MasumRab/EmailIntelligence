#!/bin/bash

echo "Cleaning up virtual environment (venv)..."
rm -rf venv

echo "Cleaning up Python cache (__pycache__) directories..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "Cleaning up typescript log file..."
rm -f typescript

# For orchestration-tools branch: Remove application-specific files
# (See scripts/cleanup_application_files.sh for dedicated cleanup)
if [[ "$(git branch --show-current)" == "orchestration-tools" ]]; then
    echo ""
    echo "Note: This is the orchestration-tools branch."
    echo "For thorough cleanup of application files, run:"
    echo "  scripts/cleanup_application_files.sh"
fi

echo "Cleanup complete."
