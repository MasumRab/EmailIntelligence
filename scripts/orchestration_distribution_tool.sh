#!/bin/bash
# orchestration_distribution_tool.py
# Script to distribute orchestration-tools branch files to other branches after alignment

set -e  # Exit on error

echo "=== ORCHESTRATION FILES DISTRIBUTION TOOL ==="
echo "Distributing key orchestration files from orchestration-tools branch to other aligned branches"
echo ""

# Define the orchestration files that should be distributed to other branches
ORCHESTRATION_FILES=(
    "launch.py"
    "setup/"
    "scripts/distribute_alignment_scripts.sh"
    "scripts/monitor_orchestration_changes.sh"
    "scripts/branch_analysis_check.sh"
    "scripts/subtask_update_tool.sh"
    ".cursor/"
    ".vscode/"
    ".taskmaster/config.json"
    ".taskmaster/docs/"
    ".env.example"
    "pyproject.toml"
    "requirements.txt"
    "requirements-dev.txt"
    "requirements-test.txt"
    "docs/testing/"
    "docs/refactoring/"
    "docs/cleanup/"
    "AGENTS.md"
    "GEMINI.md"
    "QWEN.md"
    ".pre-commit-config.yaml"
    ".pylintrc"
    ".flake8"
    ".mypy.ini"
)

# Function to distribute orchestration files to a target branch
distribute_to_branch() {
    local target_branch=$1
    local source_branch="orchestration-tools"
    
    echo "Distributing orchestration files to branch: $target_branch"
    
    # Create a temporary distribution branch from the target branch
    echo "  1. Creating temporary distribution branch..."
    local temp_branch="dist-orchestration-to-$target_branch-$(date +%s)"
    git checkout -b "$temp_branch" "origin/$target_branch" > /dev/null 2>&1
    
    # Get the orchestration files from the source branch
    echo "  2. Copying orchestration files from $source_branch..."
    for file in "${ORCHESTRATION_FILES[@]}"; do
        if git show "origin/$source_branch:$file" > /dev/null 2>&1; then
            # Copy file/directory from source branch to current branch
            git show "origin/$source_branch:$file" > /tmp/orchestration_file 2>/dev/null || true
            if [ -f "/tmp/orchestration_file" ]; then
                echo "    - Copying file: $file"
                # Copy single file
                git checkout "origin/$source_branch" -- "$file" 2>/dev/null || {
                    # If single file copy fails, try to copy directory
                    mkdir -p "$(dirname "$file")" 2>/dev/null || true
                    rm -rf "$file"
                    git checkout "origin/$source_branch" -- "$file" 2>/dev/null || echo "      Could not copy $file, may not exist or be a directory"
                }
            else
                # It's a directory
                echo "    - Copying directory: $file"
                mkdir -p "$(dirname "$file")" 2>/dev/null || true
                rm -rf "$file"
                git checkout "origin/$source_branch" -- "$file" 2>/dev/null || echo "      Could not copy $file, may not exist as directory"
            fi
        else
            echo "    - Skipping $file (doesn't exist in $source_branch)"
        fi
    done
    
    # Update gitignore if needed
    if [ -f ".gitignore" ]; then
        echo "  3. Checking .gitignore consistency with orchestration-tools..."
        git checkout "origin/$source_branch" -- .gitignore
    fi
    
    # Commit the changes
    echo "  4. Committing orchestration files to distribution branch..."
    git add .
    git commit -m "DIST: Add orchestration files from orchestration-tools branch" > /dev/null 2>&1 || echo "    No changes to commit"
    
    # Test that basic functionality still works
    echo "  5. Testing basic functionality after orchestration distribution..."
    if [ -f "launch.py" ]; then
        echo "    - Verifying launch.py imports correctly..."
        python -c "import launch; print('  ✅ Launch script imports successfully')" 2>/dev/null || echo "    ⚠️ Launch script import failed"
    fi
    
    # Switch back to original branch and merge
    echo "  6. Merging distribution branch back to $target_branch..."
    git checkout "$target_branch" > /dev/null 2>&1
    git merge "$temp_branch" > /dev/null 2>&1
    
    # Clean up temporary branch
    echo "  7. Cleaning up temporary branch..."
    git branch -D "$temp_branch" > /dev/null 2>&1
    
    echo "  ✅ Completed orchestration file distribution to $target_branch"
    echo ""
}

# Main execution
echo "Starting orchestration tools distribution process..."
echo "Files to distribute:"

for file in "${ORCHESTRATION_FILES[@]}"; do
    echo "  - $file"
done

echo ""
echo "Getting list of branches to distribute to..."

# Get all branches except the orchestration-tools branch itself
ALL_BRANCHES=$(git branch -r | grep -v "origin/HEAD\|origin/orchestration-tools\|origin/orchestration-tools-\|origin/main\|origin/scientific" | grep -v "origin/001\|origin/002" | grep -v "diverged\|integrated" | xargs)
BRANCHES_ARRAY=()
for branch in $ALL_BRANCHES; do
    BRANCHES_ARRAY+=("${branch#origin/}")
done

echo "Target branches identified: ${BRANCHES_ARRAY[*]}"

# Confirm before proceeding
read -p "Proceed with distribution to all these branches? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Distribution cancelled by user."
    exit 1
fi

# Distribute to each target branch
for branch in "${BRANCHES_ARRAY[@]}"; do
    if [[ -n "$branch" ]]; then
        distribute_to_branch "$branch"
    fi
done

echo "=== ORCHESTRATION DISTRIBUTION COMPLETE ==="
echo "All orchestration files have been distributed to target branches."
echo "Please verify functionality in each branch and create pull requests as needed."