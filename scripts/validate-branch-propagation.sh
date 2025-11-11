#!/bin/bash

# Validate branch propagation across all branches
# Checks that branch propagation rules are followed
# Reports violations and contamination

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load common libraries
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/logging.sh" 2>/dev/null || {
    # Fallback logging if lib not available
    log_info() { echo "[INFO] $@"; }
    log_error() { echo "[ERROR] $@"; }
    log_warning() { echo "[WARN] $@"; }
}

# Configuration
VIOLATIONS=0
WARNINGS=0
ERRORS=0

# Protected files that should NEVER appear on certain branches
declare -A BRANCH_BLOCKED_FILES
BRANCH_BLOCKED_FILES[main]="^\.git/hooks/|^scripts/validate-|^scripts/extract-|^\.orchestration-"
BRANCH_BLOCKED_FILES[orchestration-tools]="^src/|^backend/|^client/|^plugins/|^AGENTS\.md|^CRUSH\.md|^\.taskmaster/"
BRANCH_BLOCKED_FILES[scientific]="^\.git/hooks/|^scripts/validate-|^scripts/extract-"

# Application files that MUST be on main
declare -A BRANCH_REQUIRED_FILES
BRANCH_REQUIRED_FILES[main]="src/|backend/|package\.json"
BRANCH_REQUIRED_FILES[scientific]="src/|backend/|package\.json"

# Parse arguments
SHOW_DETAILS=false
FIX_MODE=false
TARGET_BRANCH=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --details)
            SHOW_DETAILS=true
            shift
            ;;
        --fix)
            FIX_MODE=true
            shift
            ;;
        --branch)
            TARGET_BRANCH="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --details        Show detailed file listing"
            echo "  --fix            Attempt to fix violations (experimental)"
            echo "  --branch <name>  Check specific branch only"
            echo "  --help           Show this help message"
            echo ""
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Get list of branches to check
if [[ -n "$TARGET_BRANCH" ]]; then
    BRANCHES_TO_CHECK=("$TARGET_BRANCH")
else
    BRANCHES_TO_CHECK=($(git branch -r | grep -v HEAD | sed 's|origin/||' | sort -u))
fi

echo -e "${BLUE}=== Branch Propagation Validation ===${NC}"
echo "Checking branches: ${BRANCHES_TO_CHECK[@]}"
echo ""

# Function to check branch for violations
check_branch() {
    local branch=$1
    local full_branch="origin/$branch"
    
    # Skip if branch doesn't exist
    if ! git rev-parse --verify "$full_branch" > /dev/null 2>&1; then
        return 0
    fi
    
    echo -e "${BLUE}Checking branch: $branch${NC}"
    
    local branch_violations=0
    
    # Check for blocked files
    if [[ -v BRANCH_BLOCKED_FILES[$branch] ]]; then
        local blocked_pattern="${BRANCH_BLOCKED_FILES[$branch]}"
        
        # Get files in branch that match blocked pattern
        local blocked_files=$(git ls-tree -r --name-only "$full_branch" 2>/dev/null | grep -E "$blocked_pattern" || echo "")
        
        if [[ -n "$blocked_files" ]]; then
            echo -e "${RED}  ❌ Blocked files detected:${NC}"
            while IFS= read -r file; do
                echo -e "    ${RED}✗${NC} $file"
                branch_violations=$((branch_violations + 1))
            done <<< "$blocked_files"
        fi
    fi
    
    # Check for required files
    if [[ -v BRANCH_REQUIRED_FILES[$branch] ]]; then
        local required_pattern="${BRANCH_REQUIRED_FILES[$branch]}"
        
        # Get files in branch that match required pattern
        local required_files=$(git ls-tree -r --name-only "$full_branch" 2>/dev/null | grep -E "$required_pattern" | head -1 || echo "")
        
        if [[ -z "$required_files" ]]; then
            echo -e "${YELLOW}  ⚠️  Required files missing:${NC}"
            echo -e "    Pattern: $required_pattern"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
    
    # Check specific orchestration-tools requirements
    if [[ "$branch" == "orchestration-tools" ]]; then
        local hooks_present=$(git ls-tree -r --name-only "$full_branch" 2>/dev/null | grep -c "^\.git/hooks/" || echo "0")
        
        if [[ $hooks_present -eq 0 ]]; then
            echo -e "${YELLOW}  ⚠️  Orchestration hooks not found${NC}"
            WARNINGS=$((WARNINGS + 1))
        else
            echo -e "${GREEN}  ✓ Orchestration hooks present ($hooks_present files)${NC}"
        fi
    fi
    
    # Show file counts
    if [[ "$SHOW_DETAILS" == true ]]; then
        local app_files=$(git ls-tree -r --name-only "$full_branch" 2>/dev/null | grep -E "^(src|backend|client|plugins)/" | wc -l || echo "0")
        local hook_files=$(git ls-tree -r --name-only "$full_branch" 2>/dev/null | grep -c "^\.git/hooks/" || echo "0")
        
        echo "    📊 Application files: $app_files"
        echo "    🔧 Hook files: $hook_files"
    fi
    
    if [[ $branch_violations -gt 0 ]]; then
        VIOLATIONS=$((VIOLATIONS + branch_violations))
        echo -e "${RED}  Result: $branch_violations violations${NC}"
    else
        echo -e "${GREEN}  ✓ No violations detected${NC}"
    fi
    
    echo ""
}

# Function to validate branch relationships
check_branch_relationships() {
    echo -e "${BLUE}=== Checking Branch Relationships ===${NC}"
    echo ""
    
    # orchestration-tools should have hooks
    echo "Validating orchestration-tools branch..."
    if git rev-parse --verify "origin/orchestration-tools" > /dev/null 2>&1; then
        local orch_hooks=$(git ls-tree -r --name-only "origin/orchestration-tools" 2>/dev/null | grep "\.git/hooks/" | wc -l || echo "0")
        
        if [[ $orch_hooks -gt 0 ]]; then
            echo -e "${GREEN}  ✓ orchestration-tools has hook infrastructure ($orch_hooks files)${NC}"
        else
            echo -e "${RED}  ❌ orchestration-tools missing hook infrastructure${NC}"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
    echo ""
    
    # main should have application code
    echo "Validating main branch..."
    if git rev-parse --verify "origin/main" > /dev/null 2>&1; then
        local main_app=$(git ls-tree -r --name-only "origin/main" 2>/dev/null | grep -E "^(src|backend)/" | wc -l || echo "0")
        
        if [[ $main_app -gt 0 ]]; then
            echo -e "${GREEN}  ✓ main has application code ($main_app files)${NC}"
        else
            echo -e "${YELLOW}  ⚠️  main missing application code${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi
        
        # main should NOT have hooks
        local main_hooks=$(git ls-tree -r --name-only "origin/main" 2>/dev/null | grep -c "\.git/hooks/" || echo "0")
        if [[ $main_hooks -eq 0 ]]; then
            echo -e "${GREEN}  ✓ main correctly does not have hook infrastructure${NC}"
        else
            echo -e "${RED}  ❌ main has hook infrastructure (should not)${NC}"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
    echo ""
}

# Function to check for file sync consistency
check_file_consistency() {
    echo -e "${BLUE}=== Checking File Consistency ===${NC}"
    echo ""
    
    # Check if distribution docs are synced
    local sync_docs=(
        "ORCHESTRATION_PROCESS_GUIDE.md"
        "PHASE3_ROLLBACK_OPTIONS.md"
    )
    
    for doc in "${sync_docs[@]}"; do
        echo "Checking $doc..."
        
        local main_exists=false
        local orch_exists=false
        
        if git show "origin/main:$doc" > /dev/null 2>&1; then
            main_exists=true
        fi
        
        if git show "origin/orchestration-tools:$doc" > /dev/null 2>&1; then
            orch_exists=true
        fi
        
        if [[ "$main_exists" == true && "$orch_exists" == true ]]; then
            # Check if they're the same
            local main_hash=$(git show "origin/main:$doc" | sha256sum | cut -d' ' -f1)
            local orch_hash=$(git show "origin/orchestration-tools:$doc" | sha256sum | cut -d' ' -f1)
            
            if [[ "$main_hash" == "$orch_hash" ]]; then
                echo -e "${GREEN}  ✓ $doc synced correctly${NC}"
            else
                echo -e "${YELLOW}  ⚠️  $doc differs between branches${NC}"
                WARNINGS=$((WARNINGS + 1))
            fi
        elif [[ "$main_exists" == true ]]; then
            echo -e "${YELLOW}  ⚠️  $doc on main but not orchestration-tools${NC}"
            WARNINGS=$((WARNINGS + 1))
        elif [[ "$orch_exists" == true ]]; then
            echo -e "${GREEN}  ✓ $doc only on orchestration-tools (expected)${NC}"
        fi
    done
    echo ""
}

# Main validation loop
for branch in "${BRANCHES_TO_CHECK[@]}"; do
    check_branch "$branch"
done

# Additional checks
check_branch_relationships
check_file_consistency

# Summary
echo -e "${BLUE}=== Validation Summary ===${NC}"
echo "Total violations: $VIOLATIONS"
echo "Total warnings: $WARNINGS"
echo ""

if [[ $VIOLATIONS -eq 0 && $WARNINGS -eq 0 ]]; then
    echo -e "${GREEN}✓ All branches passed propagation validation${NC}"
    exit 0
elif [[ $VIOLATIONS -gt 0 ]]; then
    echo -e "${RED}❌ Found $VIOLATIONS propagation violations${NC}"
    echo ""
    echo "Recovery steps:"
    echo "1. Identify problematic commit: git log --oneline <branch>"
    echo "2. Revert: git revert <commit-sha>"
    echo "3. Or reset to clean state: git reset --hard <good-commit>"
    echo "4. Push: git push origin <branch>"
    echo ""
    exit 1
else
    echo -e "${YELLOW}⚠️  Found $WARNINGS warnings (no critical violations)${NC}"
    echo ""
    echo "Recommended actions:"
    echo "1. Review .github/BRANCH_PROPAGATION_POLICY.md"
    echo "2. Sync distribution docs across branches"
    echo "3. Check branch relationships are correct"
    echo ""
    exit 0
fi
