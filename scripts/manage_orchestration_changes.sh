#!/bin/bash
# manage_orchestration_changes.sh - Framework for isolating and managing changes to orchestration-managed files
# Usage: ./manage_orchestration_changes.sh [check|isolate|apply] [source_branch]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Managed files list (from docs)
MANAGED_FILES=(
    "setup/launch.py"
    "setup/launch.bat"
    "setup/launch.sh"
    "scripts/sync_setup_worktrees.sh"
    ".flake8"
    ".pylintrc"
    "tsconfig.json"
    "package.json"
    "tailwind.config.ts"
    "vite.config.ts"
    "drizzle.config.ts"
    "components.json"
    ".gitignore"
    ".gitattributes"
)

print_usage() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Framework for managing orchestration-managed file changes"
    echo ""
    echo "Commands:"
    echo "  check [branch]     Check if current/source branch has only managed file changes"
    echo "  isolate [branch]   Create isolated patch of managed file changes"
    echo "  apply <patch_file> Apply isolated patch to orchestration-tools"
    echo ""
    echo "Options:"
    echo "  -h, --help         Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 check main"
    echo "  $0 isolate feature/launch-update"
    echo "  $0 apply orchestration_changes.patch"
}

validate_managed_files() {
    local branch=${1:-HEAD}
    local uncommitted_only=${2:-false}
    
    echo -e "${BLUE}Checking changes to orchestration-managed files...${NC}"
    
    local changed_files
    if [[ "$uncommitted_only" == true ]]; then
        changed_files=$(git diff --name-only)
    else
        changed_files=$(git diff --name-only "$branch")
    fi
    
    local managed_changes=()
    local unmanaged_changes=()
    
    for file in $changed_files; do
        local is_managed=false
        for managed in "${MANAGED_FILES[@]}"; do
            if [[ "$file" == "$managed" ]]; then
                is_managed=true
                break
            fi
        done
        
        if [[ "$is_managed" == true ]]; then
            managed_changes+=("$file")
        else
            unmanaged_changes+=("$file")
        fi
    done
    
    if [[ ${#unmanaged_changes[@]} -gt 0 ]]; then
        echo -e "${RED}✗ Found changes to non-orchestration files:${NC}"
        printf '  %s\n' "${unmanaged_changes[@]}"
        echo -e "${YELLOW}Warning: Only orchestration-managed files should be changed in orchestration-tools${NC}"
        return 1
    fi
    
    if [[ ${#managed_changes[@]} -gt 0 ]]; then
        echo -e "${GREEN}✓ Only orchestration-managed files changed:${NC}"
        printf '  %s\n' "${managed_changes[@]}"
    else
        echo -e "${YELLOW}No orchestration-managed files changed${NC}"
    fi
    
    return 0
}

create_isolated_patch() {
    local source_branch=$1
    local patch_file="orchestration_changes_$(date +%Y%m%d_%H%M%S).patch"
    
    echo -e "${BLUE}Creating isolated patch from $source_branch...${NC}"
    
    # Get diff of only managed files
    local diff_content=""
    for file in "${MANAGED_FILES[@]}"; do
        if git cat-file -e "$source_branch:$file" 2>/dev/null; then
            local file_diff=$(git diff "$source_branch" -- "$file" 2>/dev/null || true)
            if [[ -n "$file_diff" ]]; then
                diff_content+="$file_diff\n"
            fi
        fi
    done
    
    if [[ -z "$diff_content" ]]; then
        echo -e "${YELLOW}No changes to orchestration-managed files found${NC}"
        return 0
    fi
    
    echo "$diff_content" > "$patch_file"
    echo -e "${GREEN}✓ Isolated patch created: $patch_file${NC}"
    echo "To apply: $0 apply $patch_file"
}

apply_patch() {
    local patch_file=$1
    
    if [[ ! -f "$patch_file" ]]; then
        echo -e "${RED}Error: Patch file '$patch_file' not found${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Applying isolated patch: $patch_file${NC}"
    
    if git apply --check "$patch_file" 2>/dev/null; then
        git apply "$patch_file"
        echo -e "${GREEN}✓ Patch applied successfully${NC}"
        echo "Review changes and commit when ready"
    else
        echo -e "${RED}✗ Patch conflicts detected. Resolve manually or check patch content${NC}"
        exit 1
    fi
}

main() {
    case "${1:-}" in
        check)
            validate_managed_files "${2:-HEAD}"
            ;;
        isolate)
            if [[ -z "$2" ]]; then
                echo -e "${RED}Error: Source branch required for isolate command${NC}"
                print_usage
                exit 1
            fi
            create_isolated_patch "$2"
            ;;
        apply)
            if [[ -z "$2" ]]; then
                echo -e "${RED}Error: Patch file required for apply command${NC}"
                print_usage
                exit 1
            fi
            apply_patch "$2"
            ;;
        -h|--help|"")
            print_usage
            ;;
        *)
            echo -e "${RED}Unknown command: $1${NC}"
            print_usage
            exit 1
            ;;
    esac
}

main "$@"
