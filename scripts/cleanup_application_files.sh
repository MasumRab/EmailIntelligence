#!/bin/bash

# cleanup_application_files.sh
# Script to remove application-specific files from orchestration-tools branch
# This helps maintain the branch's focus on orchestration tools only

echo "=== Orchestration-Tools Branch Cleanup ==="
echo "This script removes application-specific files to maintain branch focus."
echo ""

# Confirm before proceeding
read -p "Do you want to proceed with cleanup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo "Starting cleanup..."

# Remove application source code
echo "Removing application source code..."
rm -rf src/ 2>/dev/null
rm -rf modules/ 2>/dev/null
rm -rf backend/ 2>/dev/null
rm -rf client/ 2>/dev/null

# Remove application data and dependencies
echo "Removing application data and dependencies..."
rm -rf data/ 2>/dev/null
rm -rf node_modules/ 2>/dev/null
rm -rf tests/ 2>/dev/null

# Remove application-specific configuration files
echo "Removing application-specific configurations..."
rm -f .env.example 2>/dev/null
rm -f .mcp.json 2>/dev/null
rm -f .rules 2>/dev/null
rm -f performance_metrics_log.jsonl 2>/dev/null

# Remove any other common application files
echo "Removing other application files..."
rm -f tsconfig.json 2>/dev/null
rm -f package.json 2>/dev/null
rm -f tailwind.config.ts 2>/dev/null
rm -f vite.config.ts 2>/dev/null
rm -f drizzle.config.ts 2>/dev/null
rm -f components.json 2>/dev/null

echo ""
echo "Cleanup completed!"
echo ""
echo "Remaining files should be orchestration tools only:"
echo "- scripts/ (orchestration scripts)"
echo "- setup/ (environment setup)"
echo "- docs/ (orchestration documentation)"
echo "- Configuration files (.flake8, .pylintrc, etc.)"
echo ""
echo "To verify, run: ls -la"
echo ""
echo "If you made changes to orchestration files, remember to reinstall hooks:"
echo "  scripts/install-hooks.sh --force"
echo ""
echo "See docs/orchestration_hook_management.md for complete procedures."