#!/bin/bash
# Alignment Script Distribution Tool
# This script handles cherry-picking essential alignment tools to target branches before alignment begins

set -e  # Exit on any error

echo "=== ALIGNMENT SCRIPT DISTRIBUTION TOOL ==="
echo "Ensuring critical tools are available on target branch before alignment..."
echo ""

# Function to check if critical scripts exist on current branch
check_critical_scripts() {
    echo "Checking for critical alignment scripts on current branch..."
    
    local missing_scripts=()
    
    if [ ! -f "scripts/monitor_orchestration_changes.sh" ]; then
        missing_scripts+=("scripts/monitor_orchestration_changes.sh")
    fi
    
    if [ ! -f "scripts/branch_analysis_check.sh" ]; then
        missing_scripts+=("scripts/branch_analysis_check.sh") 
    fi
    
    if [ ${#missing_scripts[@]} -gt 0 ]; then
        echo "⚠️  Critical scripts missing from current branch:"
        for script in "${missing_scripts[@]}"; do
            echo "   - $script"
        done
        echo ""
        return 1
    else
        echo "✅ All critical alignment scripts are available on current branch"
        echo ""
        return 0
    fi
}

# Function to find recent commits containing scripts
find_script_commits() {
    echo "Finding recent commits containing alignment scripts..."
    
    # Search for commits that added the critical scripts
    COMMIT_HASH=""
    
    # Look for the most recent commit that added any of our critical scripts
    COMMIT_HASH=$(git log --oneline --all -- scripts/monitor_orchestration_changes.sh 2>/dev/null | head -1 | cut -d' ' -f1)
    
    if [ -n "$COMMIT_HASH" ]; then
        echo "✅ Found commit containing alignment scripts: $COMMIT_HASH"
        echo ""
        echo "$COMMIT_HASH"
    else
        echo "❌ No commits found containing monitor_orchestration_changes.sh, trying alternative..."
        # Try to find any recent commit that modified scripts directory
        COMMIT_HASH=$(git log --oneline --all -- scripts/ 2>/dev/null | head -1 | cut -d' ' -f1)
        if [ -n "$COMMIT_HASH" ]; then
            echo "✅ Found recent commit in scripts/: $COMMIT_HASH"
            echo ""
            echo "$COMMIT_HASH"
        else
            echo "❌ No suitable commits found in scripts directory"
            echo ""
            return 1
        fi
    fi
}

# Function to cherry-pick scripts to current branch
cherry_pick_scripts() {
    local script_commit=$1
    local branch_name=$(git rev-parse --abbrev-ref HEAD)
    
    echo "Cherry-picking alignment scripts to $branch_name..."
    echo "Using commit: $script_commit"
    echo ""
    
    # Create temporary branch for safe cherry-picking
    TEMP_BRANCH="temp-align-scripts-$branch_name-$(date +%s)"
    echo "Creating temporary branch: $TEMP_BRANCH"
    git checkout -b "$TEMP_BRANCH"
    
    # Attempt to cherry-pick the commit containing the scripts
    if git show --name-only "$script_commit" | grep -q "monitor_orchestration_changes.sh"; then
        if git cherry-pick "$script_commit"; then
            echo "✅ Successfully cherry-picked scripts to temporary branch: $TEMP_BRANCH"
            
            # Run verification to ensure scripts work after cherry-pick
            echo "Verifying cherry-picked scripts functionality..."
            if [ -f "scripts/monitor_orchestration_changes.sh" ]; then
                chmod +x "scripts/monitor_orchestration_changes.sh"
                echo "✅ Script file exists and is executable"
            else
                echo "❌ Script file not found after cherry-pick"
                # Clean up temporary branch
                git checkout "$branch_name"
                git branch -D "$TEMP_BRANCH"
                return 1
            fi
            
            # Try a basic run to verify functionality
            if bash scripts/monitor_orchestration_changes.sh > /dev/null 2>&1; then
                echo "✅ Script is functional after cherry-pick"
                
                # Merge temporary branch back to original branch
                echo "Merging $TEMP_BRANCH back to $branch_name..."
                git checkout "$branch_name"
                git merge "$TEMP_BRANCH"
                git branch -D "$TEMP_BRANCH"
                echo "✅ Successfully merged scripts to $branch_name"
                return 0
            else
                echo "⚠️  Script exists but may not run properly, continuing with warning"
                
                # Merge temporary branch back to original branch anyway
                echo "Merging $TEMP_BRANCH back to $branch_name..."
                git checkout "$branch_name"
                git merge "$TEMP_BRANCH"
                git branch -D "$TEMP_BRANCH"
                echo "✅ Merged scripts to $branch_name with functionality warning"
                return 0
            fi
        else
            echo "❌ Cherry-pick failed, likely due to conflicts"
            
            # Abort the cherry-pick to clean up
            git cherry-pick --abort 2>/dev/null || true
            
            # Clean up temporary branch
            git checkout "$branch_name"
            git branch -D "$TEMP_BRANCH"
            
            return 1
        fi
    else
        echo "⚠️  Commit $script_commit doesn't contain monitor_orchestration_changes.sh"
        echo "Looking for alternative commits that might contain necessary scripts..."
        
        # Look for any commit that modified the scripts directory
        ALT_COMMIT=$(git log --oneline -n 1 --since="1 week ago" -- scripts/ 2>/dev/null | head -1 | cut -d' ' -f1)
        if [ -n "$ALT_COMMIT" ]; then
            echo "Trying alternative commit: $ALT_COMMIT"
            git reset --hard
            if git cherry-pick "$ALT_COMMIT"; then
                echo "✅ Successfully cherry-picked scripts with alternative commit"
                
                # Verify script existence after alternative cherry-pick
                if [ -f "scripts/monitor_orchestration_changes.sh" ]; then
                    chmod +x "scripts/monitor_orchestration_changes.sh"
                    echo "✅ Alternative script found and made executable"
                    
                    # Merge temporary branch back to original branch
                    echo "Merging $TEMP_BRANCH back to $branch_name..."
                    git checkout "$branch_name"
                    git merge "$TEMP_BRANCH"
                    git branch -D "$TEMP_BRANCH"
                    echo "✅ Successfully merged scripts to $branch_name"
                    return 0
                else
                    echo "❌ Script still not available after alternative cherry-pick"
                    git checkout "$branch_name"
                    git branch -D "$TEMP_BRANCH"
                    return 1
                fi
            else
                echo "❌ Alternative cherry-pick also failed"
                git cherry-pick --abort 2>/dev/null || true
                git checkout "$branch_name"
                git branch -D "$TEMP_BRANCH"
                return 1
            fi
        else
            echo "❌ Could not find any suitable commits containing scripts"
            git checkout "$branch_name"
            git branch -D "$TEMP_BRANCH"
            return 1
        fi
    fi
}

# Main execution
main() {
    echo "Starting alignment script distribution process..."
    echo "Current branch: $(git rev-parse --abbrev-ref HEAD)"
    echo ""
    
    # Check if scripts already exist
    if check_critical_scripts; then
        echo "All critical scripts already exist on branch. No cherry-picking needed."
        echo "Continuing with alignment preparation..."
        exit 0
    fi
    
    echo "Scripts not found, initiating cherry-pick process..."
    
    # Find the commit containing the scripts
    SCRIPT_COMMIT=$(find_script_commits)
    if [ -z "$SCRIPT_COMMIT" ]; then
        echo "❌ Could not find commits containing alignment scripts."
        echo "Please ensure the scripts exist in your repository history."
        exit 1
    fi
    
    # Cherry-pick the scripts to the current branch
    if cherry_pick_scripts "$SCRIPT_COMMIT"; then
        echo ""
        echo "✅ Successfully distributed alignment scripts to current branch."
        echo "Branch is now ready for alignment process with safety tools available."
        echo ""
        return 0
    else
        echo ""
        echo "❌ Failed to distribute alignment scripts to current branch."
        echo "Please resolve any issues before proceeding with alignment."
        echo ""
        return 1
    fi
}

# Run main function
main "$@"