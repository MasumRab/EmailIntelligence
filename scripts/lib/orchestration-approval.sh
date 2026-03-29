#!/bin/bash

# Orchestration Approval Handler
# Provides user confirmation before orchestration overwrites local files
# Use this in post-merge, post-checkout, and post-push hooks

# Color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if file differs and needs update
file_needs_update() {
    local file_path="$1"
    local source_ref="${2:-orchestration-tools}"
    
    if ! git ls-tree -r "$source_ref" --name-only 2>/dev/null | grep -q "^$file_path$"; then
        return 1  # File doesn't exist in source
    fi
    
    if git diff --quiet "$source_ref":"$file_path" "$file_path" 2>/dev/null; then
        return 1  # Files are identical
    fi
    
    return 0  # File differs, update needed
}

# Function to collect all files that would be changed
collect_changed_files() {
    local source_ref="${1:-orchestration-tools}"
    local files_array="$2"
    local changed_files=()
    
    # List of files to check for updates
    local files_to_check=(
        "scripts/install-hooks.sh"
        "scripts/sync_setup_worktrees.sh"
        "scripts/reverse_sync_orchestration.sh"
        "scripts/cleanup_orchestration.sh"
        "docs/orchestration-workflow.md"
        "docs/orchestration_summary.md"
        "docs/env_management.md"
        ".flake8"
        ".pylintrc"
        ".gitignore"
        ".gitattributes"
        "launch.py"
        "pyproject.toml"
        "requirements.txt"
        "requirements-dev.txt"
        "uv.lock"
        "scripts/hooks/pre-commit"
        "scripts/hooks/post-commit"
        "scripts/hooks/post-merge"
        "scripts/hooks/post-push"
        ".github/BRANCH_PROPAGATION_POLICY.md"
        ".github/DOCUMENTATION_DISTRIBUTION_REPORT.md"
        ".github/PROPAGATION_SETUP_CHECKLIST.md"
        ".github/pull_request_templates/orchestration-pr.md"
        ".github/workflows/extract-orchestration-changes.yml"
        ".github/workflows/lint.yml"
        ".github/workflows/test.yml"
        # Note: AGENTS.md and CRUSH.md are intentionally NOT synced from orchestration-tools
        # They are branch-specific instruction files (main/scientific only)
        # See docs/AGENT_INSTRUCTIONS_MANIFEST.md
    )
    
    for file in "${files_to_check[@]}"; do
        if file_needs_update "$file" "$source_ref"; then
            changed_files+=("$file")
        fi
    done
    
    # Return results via array variable
    if [[ -n "$files_array" ]]; then
        eval "$files_array=('${changed_files[@]}')"
    else
        printf '%s\n' "${changed_files[@]}"
    fi
}

# Function to check directories that would be synced
collect_changed_directories() {
    local source_ref="${1:-orchestration-tools}"
    local is_worktree="${2:-true}"
    local dirs_array="$3"
    local changed_dirs=()
    
    # Only include setup/deployment for worktrees
    if [[ "$is_worktree" == "true" ]]; then
        if git ls-tree -d "$source_ref" --name-only 2>/dev/null | grep -q "^setup$"; then
            changed_dirs+=("setup/")
        fi
        if git ls-tree -d "$source_ref" --name-only 2>/dev/null | grep -q "^deployment$"; then
            changed_dirs+=("deployment/")
        fi
    fi
    
    if git ls-tree -d "$source_ref" --name-only 2>/dev/null | grep -q "^scripts/lib$"; then
        changed_dirs+=("scripts/lib/")
    fi
    
    # CRITICAL: Agent instructions must be synced
    if git ls-tree -d "$source_ref" --name-only 2>/dev/null | grep -q "^\.github/instructions$"; then
        changed_dirs+=(".github/instructions/")
    fi
    
    if [[ -n "$dirs_array" ]]; then
        eval "$dirs_array=('${changed_dirs[@]}')"
    else
        printf '%s\n' "${changed_dirs[@]}"
    fi
}

# Function to display what would be changed
display_changes() {
    local changed_files=("$@")
    
    echo ""
    echo -e "${YELLOW}=== Orchestration File Updates ===${NC}"
    echo -e "${YELLOW}The following files will be updated from orchestration-tools:${NC}"
    echo ""
    
    for file in "${changed_files[@]}"; do
        echo -e "  ${YELLOW}→${NC} $file"
    done
    
    echo ""
}

# Function to display directories that would be synced
display_directory_changes() {
    local changed_dirs=("$@")
    
    if [[ ${#changed_dirs[@]} -eq 0 ]]; then
        return
    fi
    
    echo -e "${YELLOW}The following directories will be synchronized:${NC}"
    echo ""
    
    for dir in "${changed_dirs[@]}"; do
        echo -e "  ${YELLOW}→${NC} $dir (all contents)"
    done
    
    echo ""
}

# Function to prompt user for approval
prompt_for_approval() {
    local action_desc="${1:-Update orchestration files}"
    local enable_env="${ORCHESTRATION_APPROVAL_PROMPT:-true}"
    
    # If not in interactive terminal or env var disables prompts, auto-approve
    if [[ ! -t 0 ]] || [[ "$enable_env" == "false" ]]; then
        return 0  # Auto-approve
    fi
    
    echo -e "${BLUE}───────────────────────────────────────${NC}"
    echo -e "${BLUE}$action_desc${NC}"
    echo -e "${BLUE}───────────────────────────────────────${NC}"
    echo ""
    echo -e "Proceed with orchestration synchronization? ${GREEN}(y/n)${NC} "
    read -r -t 30 response  # 30 second timeout
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        return 0  # Approve
    else
        return 1  # Deny
    fi
}

# Function to log orchestration action
log_orchestration_action() {
    local action="$1"
    local status="$2"
    local details="$3"
    local log_file=".git/hooks/.orchestration_log"
    
    mkdir -p "$(dirname "$log_file")"
    
    local timestamp=$(date -u '+%Y-%m-%d %H:%M:%S')
    local branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    
    echo "[$timestamp] [$branch] $action: $status - $details" >> "$log_file"
}

# Function to show what was approved/denied
show_approval_result() {
    local approved="$1"
    local action="${2:-orchestration sync}"
    
    echo ""
    if [[ "$approved" == "true" ]]; then
        echo -e "${GREEN}✓ Approved: $action will proceed${NC}"
        log_orchestration_action "APPROVAL" "GRANTED" "$action"
    else
        echo -e "${RED}✗ Denied: $action skipped${NC}"
        log_orchestration_action "APPROVAL" "DENIED" "$action"
        echo -e "${YELLOW}To force orchestration, run:${NC}"
        echo -e "  ${GREEN}ORCHESTRATION_APPROVAL_PROMPT=false git <command>${NC}"
    fi
    echo ""
}

# Export functions for use in hooks
export -f file_needs_update
export -f collect_changed_files
export -f collect_changed_directories
export -f display_changes
export -f display_directory_changes
export -f prompt_for_approval
export -f log_orchestration_action
export -f show_approval_result
