#!/bin/bash

# cleanup_application_files.sh
# Script to remove application-specific files from orchestration-tools branch
# This helps maintain the branch's focus on orchestration tools only

echo "=== Orchestration-Tools Branch Cleanup ==="
echo "This script removes application-specific files to maintain branch focus."
echo ""

# Check for uncommitted files that might be lost
UNCOMMITTED_FILES=$(git status --porcelain --untracked-files=all 2>/dev/null | grep -v "^scripts/" | grep -v "^setup/" | grep -v "^\..*taskmaster/" | wc -l)
if [[ $UNCOMMITTED_FILES -gt 0 ]]; then
    echo "⚠️  WARNING: There are $UNCOMMITTED_FILES uncommitted files that may be deleted:"
    git status --porcelain --untracked-files=all 2>/dev/null | grep -v "^scripts/" | grep -v "^setup/" | grep -v "^\..*taskmaster/" | head -10
    if [[ $UNCOMMITTED_FILES -gt 10 ]]; then
        echo "  ... and $((UNCOMMITTED_FILES - 10)) more files"
    fi
    echo ""
    read -p "Proceed with cleanup anyway? This may result in permanent loss of uncommitted files. (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cleanup cancelled."
        exit 0
    fi
fi

# Check for orchestration-tools and taskmaster files that would be affected
ORCHESTRATION_TOOLS_PRESENT=0
TASKMASTER_PRESENT=0

if [[ -d "scripts/" ]]; then
    ORCHESTRATION_TOOLS_PRESENT=1
    echo "INFO: Orchestration scripts directory detected ($ORCHESTRATION_TOOLS_PRESENT)"
fi

if [[ -d ".taskmaster/" ]]; then
    TASKMASTER_PRESENT=1
    echo "INFO: Task Master worktree directory detected ($TASKMASTER_PRESENT)"
fi

if [[ $ORCHESTRATION_TOOLS_PRESENT -eq 1 || $TASKMASTER_PRESENT -eq 1 ]]; then
    echo "⚠️  WARNING: Orchestration infrastructure detected:"
    [[ $ORCHESTRATION_TOOLS_PRESENT -eq 1 ]] && echo "  - scripts/ directory with orchestration tools"
    [[ $TASKMASTER_PRESENT -eq 1 ]] && echo "  - .taskmaster/ worktree directory"
    echo ""
    read -p "These directories will be preserved. Continue with cleanup? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cleanup cancelled."
        exit 0
    fi
fi

# Confirm before proceeding
read -p "Do you want to proceed with cleanup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo "Starting cleanup..."

# Remove application source code (preserve orchestration-specific directories)
echo "Removing application source code..."
rm -rf src/ 2>/dev/null
rm -rf modules/ 2>/dev/null
rm -rf backend/ 2>/dev/null
rm -rf client/ 2>/dev/null

# Remove application data and dependencies (preserve setup/ and orchestration files)
echo "Removing application data and dependencies..."
rm -rf data/ 2>/dev/null
rm -rf node_modules/ 2>/dev/null
# Preserve tests/ if it contains orchestration tests
if [[ -f "tests/test_orchestration.py" || -f "tests/test_hooks.py" || -f "tests/test_setup.py" ]]; then
    echo "Preserving tests/ directory (contains orchestration tests)"
else
    rm -rf tests/ 2>/dev/null
fi

# Remove application-specific configuration files but preserve orchestration configs
echo "Removing application-specific configurations..."
rm -f .env.example 2>/dev/null
rm -f .mcp.json 2>/dev/null
rm -f .rules 2>/dev/null
rm -f performance_metrics_log.jsonl 2>/dev/null

# Remove any other common application files but preserve orchestration files
echo "Removing other application files..."
rm -f tsconfig.json 2>/dev/null
rm -f package.json 2>/dev/null
rm -f tailwind.config.ts 2>/dev/null
rm -f vite.config.ts 2>/dev/null
rm -f drizzle.config.ts 2>/dev/null
rm -f components.json 2>/dev/null

# Preserve critical orchestration files and directories
echo "Preserving critical orchestration files and directories:"
echo "  - scripts/ (orchestration scripts)"
echo "  - setup/ (environment setup)"
echo "  - docs/ (orchestration documentation)"
echo "  - .flake8, .pylintrc (configuration files)"
echo "  - launch.py (orchestration wrapper)"
echo "  - .taskmaster/ (worktree - git handles isolation)"
echo "  - all git hooks (orchestration functionality)"

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