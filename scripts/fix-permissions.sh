#!/bin/bash
#
# fix-permissions.sh - Repair all file permissions in the project
#
# DESCRIPTION:
#   Diagnoses and fixes common permission issues in the EmailIntelligence project.
#   Ensures scripts are executable, hooks work, and directories are accessible.
#
# USAGE:
#   ./scripts/fix-permissions.sh [--check] [--verbose] [--help]
#
# OPTIONS:
#   --check    Only check, don't fix (dry-run)
#   --verbose  Show detailed output
#   --help     Show this help message
#
# AUTHOR: EmailIntelligence Team
# VERSION: 1.0.0

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Config
CHECK_ONLY=false
VERBOSE=false
FIXED_COUNT=0
CHECKED_COUNT=0

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_debug() {
    if $VERBOSE; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
    fi
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --check)
                CHECK_ONLY=true
                shift
                ;;
            --verbose|-v)
                VERBOSE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

show_help() {
    head -25 "$0" | tail -21
}

# Fix file permission
fix_file() {
    local file=$1
    local expected_mode=$2
    local description=$3
    
    if [[ ! -e "$file" ]]; then
        log_debug "File not found: $file"
        return 0
    fi
    
    local current_mode=$(stat -c %a "$file" 2>/dev/null || stat -f %A "$file" 2>/dev/null || echo "unknown")
    ((CHECKED_COUNT++))
    
    if [[ "$current_mode" != "$expected_mode" ]]; then
        log_warn "$description: $file ($current_mode → $expected_mode)"
        
        if ! $CHECK_ONLY; then
            if chmod "$expected_mode" "$file"; then
                log_success "Fixed: $file"
                ((FIXED_COUNT++))
            else
                log_error "Failed to fix: $file"
            fi
        fi
    else
        log_debug "OK: $file ($current_mode)"
    fi
}

# Fix directory permission
fix_directory() {
    local dir=$1
    local expected_mode=$2
    local description=$3
    
    if [[ ! -d "$dir" ]]; then
        log_debug "Directory not found: $dir"
        return 0
    fi
    
    local current_mode=$(stat -c %a "$dir" 2>/dev/null || stat -f %A "$dir" 2>/dev/null || echo "unknown")
    ((CHECKED_COUNT++))
    
    if [[ "$current_mode" != "$expected_mode" ]]; then
        log_warn "$description: $dir ($current_mode → $expected_mode)"
        
        if ! $CHECK_ONLY; then
            if chmod "$expected_mode" "$dir"; then
                log_success "Fixed: $dir"
                ((FIXED_COUNT++))
            else
                log_error "Failed to fix: $dir"
            fi
        fi
    else
        log_debug "OK: $dir ($current_mode)"
    fi
}

# Fix all shell scripts in directory
fix_directory_scripts() {
    local dir=$1
    local description=$2
    
    if [[ ! -d "$dir" ]]; then
        log_debug "Directory not found: $dir"
        return 0
    fi
    
    log_info "Checking $description: $dir"
    
    while IFS= read -r -d '' file; do
        if [[ -x "$file" ]]; then
            log_debug "Already executable: $file"
        else
            ((CHECKED_COUNT++))
            log_warn "Not executable: $file"
            
            if ! $CHECK_ONLY; then
                if chmod +x "$file"; then
                    log_success "Fixed: $file"
                    ((FIXED_COUNT++))
                else
                    log_error "Failed to fix: $file"
                fi
            fi
        fi
    done < <(find "$dir" -maxdepth 1 -type f -name "*.sh" -print0)
}

# Main checks and fixes
main() {
    parse_args "$@"
    
    cd "$PROJECT_ROOT"
    
    log_info "================================"
    log_info "FILE PERMISSION CHECKER"
    log_info "================================"
    echo ""
    
    if $CHECK_ONLY; then
        log_info "Running in CHECK-ONLY mode (no changes will be made)"
        echo ""
    fi
    
    # 1. Git Hooks
    log_info "1. Checking Git Hooks..."
    fix_file ".git/hooks/pre-commit" "755" "Git hook"
    fix_file ".git/hooks/post-commit" "755" "Git hook"
    fix_file ".git/hooks/post-checkout" "755" "Git hook"
    fix_file ".git/hooks/post-merge" "755" "Git hook"
    fix_file ".git/hooks/post-push" "755" "Git hook"
    fix_file ".git/hooks/pre-push" "755" "Git hook"
    fix_file ".git/hooks/post-commit-setup-sync" "755" "Git hook"
    echo ""
    
    # 2. Scripts directory
    log_info "2. Checking Scripts Directory..."
    fix_directory_scripts "scripts" "shell scripts"
    echo ""
    
    # 3. Setup directory
    log_info "3. Checking Setup Directory..."
    fix_directory_scripts "setup" "setup scripts"
    echo ""
    
    # 4. Individual important scripts
    log_info "4. Checking Important Scripts..."
    fix_file "auto_sync_docs.py" "755" "Python script"
    fix_file "launch.py" "644" "Python launcher"
    echo ""
    
    # 5. Directories
    log_info "5. Checking Directory Permissions..."
    fix_directory "." "755" "Project root"
    fix_directory "scripts" "755" "Scripts directory"
    fix_directory "setup" "755" "Setup directory"
    fix_directory "src" "755" "Source directory"
    fix_directory "backend" "755" "Backend directory"
    fix_directory "client" "755" "Client directory"
    fix_directory ".git/hooks" "755" "Git hooks directory"
    echo ""
    
    # 6. Special files
    log_info "6. Checking Special Files..."
    if [[ -f "GEMINI.md" ]]; then
        local gemini_mode=$(stat -c %a "GEMINI.md" 2>/dev/null || stat -f %A "GEMINI.md" 2>/dev/null || echo "unknown")
        log_warn "GEMINI.md permissions: $gemini_mode (restricted file - skipping)"
        log_info "To make GEMINI.md readable: chmod 644 GEMINI.md"
        ((CHECKED_COUNT++))
    fi
    echo ""
    
    # Summary
    log_info "================================"
    log_info "SUMMARY"
    log_info "================================"
    echo "Files checked: $CHECKED_COUNT"
    echo "Files fixed: $FIXED_COUNT"
    
    if ! $CHECK_ONLY; then
        if [[ $FIXED_COUNT -gt 0 ]]; then
            log_success "Fixed $FIXED_COUNT permission issues"
            echo ""
            echo "Next steps:"
            echo "  1. Verify changes: git status"
            echo "  2. If needed: git diff --cached --raw"
            echo "  3. Commit if desired: git add -A && git commit -m 'chore: fix file permissions'"
        else
            log_success "All permissions are correct"
        fi
    else
        log_info "Run without --check flag to apply fixes"
    fi
    echo ""
}

main "$@"
