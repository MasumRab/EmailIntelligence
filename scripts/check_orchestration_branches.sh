#!/bin/bash
# Script to identify orchestration-tools branches and critical functionalities

echo "=== Orchestration Tools Verification ==="

echo ""
echo "1. Identifying orchestration-related branches..."
git branch -a | grep -i -E "(orchestration|launch|worktree|agent|tool)"

echo ""
echo "2. Checking for launch-related files across branches..."
# Check the current branch first
echo "Current branch ($GIT_BRANCH):"
find . -name "*launch*" -type f 2>/dev/null | head -10

echo ""
echo "3. Looking for critical orchestration files..."
CRITICAL_FILES=(
    "launch.py"
    "launch.sh" 
    "launch.bat"
    "src/agents/"
    "src/core/agents/"
    "scripts/"
    "pyproject.toml"
    "Dockerfile"
    "docker-compose.yml"
    "src/orchestration/"
    "worktree_"
)

for file in "${CRITICAL_FILES[@]}"; do
    echo "Searching for: $file"
    find . -name "$file*" 2>/dev/null
    echo "---"
done

echo ""
echo "4. Checking git history for orchestration branches..."
git branch -r | grep -i -E "(orchestration|launch|worktree|agent|tool)"

echo ""
echo "5. Checking for worktree-related functionality..."
find . -name "worktree" -type d 2>/dev/null
find . -name "*worktree*" -type f 2>/dev/null

echo ""
echo "6. Examining agent-related functionality..."
find . -path "./src/agents*" -type f 2>/dev/null
find . -name "*agent*" -path "./src/*" -type f 2>/dev/null