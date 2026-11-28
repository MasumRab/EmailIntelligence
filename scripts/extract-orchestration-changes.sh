#!/bin/bash

# extract-orchestration-changes.sh - Extract orchestration file changes from a branch
#
# DESCRIPTION:
#   Extracts changes to orchestration-managed files from a source branch and creates
#   a new orchestration-* branch with only those changes. The orchestration changes
#   are squashed into a single commit with a summary.
#
#   Useful when a feature branch contains both application code and setup/configuration
#   changes. This allows the orchestration changes to be reviewed and merged separately
#   to orchestration-tools.
#
# USAGE:
#   ./scripts/extract-orchestration-changes.sh <source-branch> [options]
#
# OPTIONS:
#   --base <branch>     Base branch to compare against (default: main)
#   --auto-pr           Auto-create draft PR to orchestration-tools (requires gh CLI)
#   --dry-run           Show what would be extracted without creating branch
#   --verbose           Enable verbose output
#   --help              Show this help message
#
# EXAMPLES:
#   # Extract from feature branch
#   ./scripts/extract-orchestration-changes.sh feature/better-auth
#
#   # Preview before extracting
#   ./scripts/extract-orchestration-changes.sh feature/better-auth --dry-run
#
#   # Extract and auto-create PR
#   ./scripts/extract-orchestration-changes.sh feature/better-auth --auto-pr
#
# AUTHOR: Orchestration Team
# VERSION: 1.0.0

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SOURCE_BRANCH=""
BASE_BRANCH="main"
AUTO_PR=false
DRY_RUN=false
VERBOSE=false

# Orchestration-managed files/directories
ORCH_PATTERNS=(
    "setup/"
    "deployment/"
    "scripts/lib/"
    "scripts/install-hooks.sh"
    "scripts/sync_setup_worktrees.sh"
    "scripts/reverse_sync_orchestration.sh"
    "scripts/cleanup_orchestration.sh"
    ".flake8"
    ".pylintrc"
    "pyproject.toml"
    "requirements.txt"
    "requirements-dev.txt"
    "uv.lock"
    "tsconfig.json"
    "tailwind.config.ts"
    "vite.config.ts"
    "drizzle.config.ts"
    "components.json"
    ".gitignore"
    ".gitattributes"
    "launch.py"
)

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    if [[ "$VERBOSE" == true ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
    fi
}

print_usage() {
    head -40 "$0" | tail -30
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --base)
                BASE_BRANCH="$2"
                shift 2
                ;;
            --auto-pr)
                AUTO_PR=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                print_usage
                exit 0
                ;;
            *)
                if [[ -z "$SOURCE_BRANCH" ]]; then
                    SOURCE_BRANCH="$1"
                else
                    log_error "Unknown option: $1"
                    exit 1
                fi
                shift
                ;;
        esac
    done
}

validate_inputs() {
    if [[ -z "$SOURCE_BRANCH" ]]; then
        log_error "Source branch not specified"
        print_usage
        exit 1
    fi

    if ! git rev-parse --verify "$SOURCE_BRANCH" >/dev/null 2>&1; then
        log_error "Source branch '$SOURCE_BRANCH' does not exist"
        exit 1
    fi

    if ! git rev-parse --verify "$BASE_BRANCH" >/dev/null 2>&1; then
        log_error "Base branch '$BASE_BRANCH' does not exist"
        exit 1
    fi

    if [[ "$SOURCE_BRANCH" == "orchestration-tools" ]]; then
        log_error "Cannot extract from orchestration-tools branch (it's already the source)"
        exit 1
    fi
}

check_git_state() {
    if [[ -n $(git status -s) ]]; then
        log_error "Working directory is not clean"
        echo "Commit or stash changes before extracting"
        exit 1
    fi
}

get_orchestration_changes() {
    local changed_files=""
    
    # Get all changed files between base and source
    changed_files=$(git diff --name-only "$BASE_BRANCH"..."$SOURCE_BRANCH" 2>/dev/null || git diff --name-only "$BASE_BRANCH" "$SOURCE_BRANCH")
    
    if [[ -z "$changed_files" ]]; then
        log_warn "No changes found between $BASE_BRANCH and $SOURCE_BRANCH"
        return 1
    fi

    # Filter to orchestration patterns
    local orch_changes=""
    while IFS= read -r file; do
        for pattern in "${ORCH_PATTERNS[@]}"; do
            if [[ "$file" == "$pattern" || "$file" == "$pattern"* ]]; then
                orch_changes+="$file"$'\n'
                break
            fi
        done
    done <<< "$changed_files"

    echo "$orch_changes"
}

show_changes() {
    local orch_files="$1"
    
    if [[ -z "$orch_files" ]]; then
        log_warn "No orchestration files changed in $SOURCE_BRANCH"
        return 1
    fi

    echo -e "${BLUE}=== Orchestration Files Changed ===${NC}"
    echo "$orch_files" | nl
    echo ""

    # Show statistics
    local file_count=$(echo "$orch_files" | wc -l)
    echo -e "${BLUE}Total orchestration files changed: $file_count${NC}"
    echo ""

    # Show diff stats
    echo -e "${BLUE}=== Changes Summary ===${NC}"
    git diff --stat "$BASE_BRANCH"..."$SOURCE_BRANCH" -- $orch_files 2>/dev/null || \
    git diff --stat "$BASE_BRANCH" "$SOURCE_BRANCH" -- $orch_files
    echo ""

    return 0
}

create_extraction_commit_message() {
    local source="$1"
    local file_count="$2"
    
    # Get original commits between base and source
    local commit_count=$(git rev-list --count "$BASE_BRANCH"..."$SOURCE_BRANCH" 2>/dev/null || echo "N/A")
    
    cat << EOF
chore: extract orchestration changes from $source

This commit contains all orchestration-managed file changes from the
$source branch, squashed and ready for review/merge to orchestration-tools.

Source: $source (based on $BASE_BRANCH)
Orchestration files changed: $file_count
Original commits: $commit_count

Files:
EOF
    
    # Add file list
    get_orchestration_changes | sed 's/^/  - /'
}

create_orchestration_branch() {
    local source="$1"
    local orch_files="$2"
    local target_branch="orchestration/${source#*/}"
    
    log_info "Creating orchestration branch: $target_branch"
    
    # Check if branch already exists
    if git rev-parse --verify "$target_branch" >/dev/null 2>&1; then
        log_warn "Branch '$target_branch' already exists"
        read -p "Delete and recreate? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "Aborted"
            return 1
        fi
        git branch -D "$target_branch"
    fi

    # Create new branch from base
    git checkout -b "$target_branch" "$BASE_BRANCH" --quiet
    log_debug "Created branch $target_branch from $BASE_BRANCH"

    # Check out only orchestration files from source
    if [[ "$DRY_RUN" != true ]]; then
        while IFS= read -r file; do
            if [[ -n "$file" ]]; then
                git show "$SOURCE_BRANCH:$file" > "$file" 2>/dev/null || {
                    log_warn "Could not extract $file from $SOURCE_BRANCH"
                    # File might not exist in source, skip
                    continue
                }
                git add "$file"
            fi
        done <<< "$orch_files"
    fi

    # Create squashed commit
    local file_count=$(echo "$orch_files" | grep -c . || echo 0)
    local commit_msg=$(create_extraction_commit_message "$source" "$file_count")
    
    if [[ "$DRY_RUN" != true ]]; then
        git commit -m "$commit_msg"
        log_info "✓ Created orchestration extraction branch: $target_branch"
        log_info "Ready to push: git push origin $target_branch"
    else
        log_info "[DRY RUN] Would create branch: $target_branch"
        log_info "[DRY RUN] With $file_count orchestration files"
        
        # Return to previous branch
        git checkout - --quiet
    fi

    echo "$target_branch"
}

create_pr() {
    local branch="$1"
    
    if ! command -v gh &> /dev/null; then
        log_warn "GitHub CLI (gh) not available. Cannot auto-create PR."
        log_info "Create PR manually:"
        log_info "  1. Go to: https://github.com/MasumRab/EmailIntelligence/pulls"
        log_info "  2. Create PR: base=orchestration-tools head=$branch"
        return 1
    fi

    if ! gh auth status &> /dev/null; then
        log_warn "GitHub CLI not authenticated. Cannot auto-create PR."
        return 1
    fi

    log_info "Creating draft PR for $branch..."
    
    if gh pr create \
        --draft \
        --base orchestration-tools \
        --head "$branch" \
        --title "[AUTO] Orchestration: Extract from $(echo $branch | cut -d/ -f2-)" \
        --body "Orchestration files extracted from feature branch.

See commit details for what was changed.

**Next steps:**
1. Review the changes
2. Test on your system
3. Mark as ready for review when complete
4. Request review from orchestration maintainers" \
        --label "orchestration,auto-created"; then
        
        log_info "✓ Draft PR created"
        return 0
    else
        log_warn "Failed to create draft PR"
        return 1
    fi
}

main() {
    parse_args "$@"
    
    log_info "Orchestration Changes Extractor"
    log_info "=================================="
    echo ""

    validate_inputs
    check_git_state

    log_info "Analyzing changes in $SOURCE_BRANCH (compared to $BASE_BRANCH)..."
    echo ""

    # Get orchestration changes
    local orch_changes
    orch_changes=$(get_orchestration_changes) || {
        log_warn "No orchestration files found in changes"
        exit 0
    }

    # Show what will be extracted
    show_changes "$orch_changes" || exit 0

    if [[ "$DRY_RUN" == true ]]; then
        log_info "[DRY RUN] To proceed with extraction, run without --dry-run"
        exit 0
    fi

    # Confirm before creating
    read -p "Extract these orchestration changes? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Aborted"
        exit 0
    fi

    # Create extraction branch
    local target_branch
    target_branch=$(create_orchestration_branch "$SOURCE_BRANCH" "$orch_changes") || exit 1
    
    echo ""
    log_info "✓ Extraction complete!"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "  1. Review the extracted changes:"
    echo "     git show $target_branch"
    echo ""
    echo "  2. Push to remote:"
    echo "     git push origin $target_branch"
    echo ""
    echo "  3. Create PR to orchestration-tools:"
    if command -v gh &> /dev/null && gh auth status &> /dev/null; then
        echo "     gh pr create --base orchestration-tools --head $target_branch"
    else
        echo "     https://github.com/MasumRab/EmailIntelligence/pulls"
    fi
    echo ""

    if [[ "$AUTO_PR" == true ]]; then
        create_pr "$target_branch"
    fi
}

main "$@"
