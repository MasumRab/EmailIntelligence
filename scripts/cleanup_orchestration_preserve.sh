#!/bin/bash

# cleanup_orchestration_preserve.sh
# Script to clean up temporary files while preserving essential orchestration files
# This script is safe to run on orchestration-tools branches

echo "=== Orchestration-Preserving Cleanup ==="
echo "This script removes temporary and cache files while preserving orchestration tools."
echo ""

# Confirm before proceeding
read -p "Proceed with cleanup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo "Starting orchestration-preserving cleanup..."

# Remove Python cache and temporary files
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true

# Remove temporary files
echo "Removing temporary files..."
rm -f *.tmp 2>/dev/null || true
rm -f *.temp 2>/dev/null || true
rm -f *~ 2>/dev/null || true
rm -f .DS_Store 2>/dev/null || true

# Remove log files but preserve important ones
echo "Removing log files..."
find . -name "*.log" ! -name "hook-*.log" ! -name "orchestration-*.log" -delete 2>/dev/null || true

# Remove build/cache directories but preserve setup/
echo "Removing build/cache directories..."
rm -rf build/ 2>/dev/null || true 
rm -rf dist/ 2>/dev/null || true
rm -rf *.egg-info/ 2>/dev/null || true

# Remove virtual environment
echo "Removing virtual environment..."
rm -rf venv/ 2>/dev/null || true
rm -rf .venv/ 2>/dev/null || true

# Do NOT remove these orchestration-critical directories/files:
# - scripts/ (orchestration scripts)
# - setup/ (environment setup files)
# - .git/hooks/ (orchestration functionality)
# - .taskmaster/ (worktree - git handles isolation)
# - launch.py (orchestration wrapper)
# - All configuration files (.flake8, .pylintrc, etc.)

echo ""
echo "Cleanup completed!"
echo ""
echo "Preserved critical orchestration files:"
echo "  - scripts/ (all orchestration scripts including newly created ones)"
echo "  - setup/ (environment setup and configuration)"
echo "  - .git/hooks/ (orchestration functionality)"
echo "  - .taskmaster/ (worktree - git handles isolation)"
echo "  - launch.py (orchestration wrapper)"
echo "  - All configuration files"
echo "  - All orchestration-related documentation"
echo ""
