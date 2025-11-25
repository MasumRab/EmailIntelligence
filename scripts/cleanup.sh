#!/bin/bash

# Check for uncommitted files that might be lost
UNCOMMITTED_FILES=$(git status --porcelain --untracked-files=all 2>/dev/null | grep -v "^scripts/" | grep -v "^setup/" | grep -v "^\..*taskmaster/" | wc -l)
if [[ $UNCOMMITTED_FILES -gt 0 ]]; then
    echo "⚠️  WARNING: There are $UNCOMMITTED_FILES uncommitted files that may be affected:"
    git status --porcelain --untracked-files=all 2>/dev/null | grep -v "^scripts/" | grep -v "^setup/" | grep -v "^\..*taskmaster/" | head -10
    if [[ $UNCOMMITTED_FILES -gt 10 ]]; then
        echo "  ... and $((UNCOMMITTED_FILES - 10)) more files"
    fi
    echo ""
    read -p "Proceed with cleanup anyway? This may result in loss of uncommitted files. (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cleanup cancelled."
        exit 0
    fi
fi

echo "Cleaning up virtual environment (venv)..."
rm -rf venv

echo "Cleaning up Python cache (__pycache__) directories..."
find . -type d -name "__pycache__" -exec rm -rf {} +

echo "Cleaning up typescript log file..."
rm -f typescript

# For orchestration-tools branch: Remove application-specific files
# (See scripts/cleanup_application_files.sh for dedicated cleanup)
if [[ "$(git branch --show-current)" == *"orchestration-tools"* ]]; then
    echo ""
    echo "Note: This is the orchestration-tools branch."
    echo "For thorough cleanup of application files, run:"
    echo "  scripts/cleanup_application_files.sh"
    echo ""
    echo "Preserving orchestration-specific files:"
    echo "  - All scripts in scripts/ directory"
    echo "  - setup/ directory with orchestration setup files"
    echo "  - git hooks in .git/hooks/"
    echo "  - launch.py orchestration wrapper"
    echo "  - .taskmaster/ worktree (git handles isolation)"
    echo "  - Orchestration configuration files"
fi

echo "Cleanup complete."
