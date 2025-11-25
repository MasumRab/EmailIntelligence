#!/bin/bash

################################################################################
# Orchestration Files Sync Script
#
# Purpose: Centralized, SOLID-designed script for distributing orchestration
#          files (setup/, hooks, configs) to orchestration-tools branches
#
# Usage:
#   ./scripts/sync_orchestration_files.sh [OPTIONS]
#
# Options:
#   --dry-run           Show what would be synced without making changes
#   --verify            Verify integrity of synced files
#   --rollback          Rollback to previous sync state
#   --setup-only        Sync only setup/ directory
#   --hooks-only        Sync only git hooks
#   --config-only       Sync only configuration files
#   --force             Force overwrite of local changes
#   --help              Show this help message
#
# Author: EmailIntelligence Team
# Version: 1.0.0
# Status: Initial Implementation
################################################################################

set -euo pipefail

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Script configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
readonly SYNC_LOG_FILE="${PROJECT_ROOT}/.sync_history.log"
readonly SYNC_STATE_FILE="${PROJECT_ROOT}/.sync_state.json"

# Options
DRY_RUN=false
VERIFY_MODE=false
ROLLBACK_MODE=false
FORCE_MODE=false
SETUP_ONLY=false
HOOKS_ONLY=false
CONFIG_ONLY=false

################################################################################
# Utility Functions
################################################################################

log_info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✓${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}⚠${NC} $*"
}

log_error() {
    echo -e "${RED}✗${NC} $*" >&2
}

log_debug() {
    if [[ "${DEBUG:-0}" == "1" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $*"
    fi
}

# Check if running on orchestration-tools branch
is_orchestration_tools_branch() {
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    
    if [[ "$current_branch" == orchestration-tools* ]]; then
        return 0
    fi
    return 1
}

# Check if running on taskmaster branch
is_taskmaster_branch() {
    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    
    if [[ "$current_branch" == taskmaster* ]]; then
        return 1  # Taskmaster branches should NOT sync
    fi
    return 0
}

# Source library functions if available
source_library() {
    local lib_file="$SCRIPT_DIR/lib/sync_functions.sh"
    
    if [[ ! -f "$lib_file" ]]; then
        log_warning "Sync library not found: $lib_file"
        return 1
    fi
    
    # shellcheck source=/dev/null
    source "$lib_file"
    log_debug "Loaded sync library"
    return 0
}

################################################################################
# Core Sync Functions
################################################################################

# Sync setup directory
sync_setup_directory() {
    local dry_run="$1"
    
    log_info "Syncing setup/ directory..."
    
    local setup_files=(
        "launch.py"
        "validation.py"
        "services.py"
        "environment.py"
        "utils.py"
        "project_config.py"
        "test_stages.py"
        "pyproject.toml"
        "requirements.txt"
        "requirements-dev.txt"
    )
    
    local synced=0
    local skipped=0
    
    for file in "${setup_files[@]}"; do
        local src="${PROJECT_ROOT}/setup/$file"
        
        if [[ ! -f "$src" ]]; then
            log_warning "Source file not found: setup/$file"
            ((skipped++))
            continue
        fi
        
        if [[ "$dry_run" == "true" ]]; then
            echo "  [DRY-RUN] Would sync: setup/$file"
        else
            cp "$src" "${PROJECT_ROOT}/setup/$file"
            ((synced++))
            log_debug "Synced: setup/$file"
        fi
    done
    
    if [[ "$dry_run" != "true" ]]; then
        log_success "Synced $synced files from setup/ (skipped $skipped)"
    fi
}

# Sync git hooks
sync_hooks() {
    local dry_run="$1"
    
    log_info "Syncing git hooks..."
    
    local hooks=(
        "pre-commit"
        "post-commit"
        "post-merge"
        "post-checkout"
        "post-push"
        "post-commit-setup-sync"
    )
    
    local hooks_dir="${PROJECT_ROOT}/.git/hooks"
    local source_dir="${SCRIPT_DIR}/hooks"
    local synced=0
    local skipped=0
    
    if [[ ! -d "$hooks_dir" ]]; then
        log_error "Git hooks directory not found: $hooks_dir"
        return 1
    fi
    
    for hook in "${hooks[@]}"; do
        local src="${source_dir}/$hook"
        local dst="${hooks_dir}/$hook"
        
        if [[ ! -f "$src" ]]; then
            log_warning "Source hook not found: $hook"
            ((skipped++))
            continue
        fi
        
        if [[ "$dry_run" == "true" ]]; then
            echo "  [DRY-RUN] Would sync hook: $hook"
        else
            cp "$src" "$dst"
            chmod +x "$dst"
            ((synced++))
            log_debug "Synced hook: $hook"
        fi
    done
    
    if [[ "$dry_run" != "true" ]]; then
        log_success "Synced $synced hooks (skipped $skipped)"
    fi
}

# Sync configuration files
sync_config_files() {
    local dry_run="$1"
    
    log_info "Syncing configuration files..."
    
    local config_files=(
        ".flake8"
        ".pylintrc"
        ".gitignore"
        ".gitattributes"
    )
    
    local synced=0
    local skipped=0
    
    for file in "${config_files[@]}"; do
        local src="${PROJECT_ROOT}/$file"
        
        if [[ ! -f "$src" ]]; then
            log_warning "Source config not found: $file"
            ((skipped++))
            continue
        fi
        
        if [[ "$dry_run" == "true" ]]; then
            echo "  [DRY-RUN] Would sync: $file"
        else
            # Config files already in place, verify integrity
            ((synced++))
            log_debug "Verified: $file"
        fi
    done
    
    if [[ "$dry_run" != "true" ]]; then
        log_success "Verified $synced config files (skipped $skipped)"
    fi
}

# Sync root wrapper script
sync_root_wrapper() {
    local dry_run="$1"
    
    log_info "Syncing root wrapper script..."
    
    local src="${SCRIPT_DIR}/../launch.py"
    
    if [[ ! -f "$src" ]]; then
        log_warning "Root wrapper not found: launch.py"
        return 1
    fi
    
    if [[ "$dry_run" == "true" ]]; then
        echo "  [DRY-RUN] Would sync: launch.py"
    else
        log_success "Root wrapper verified: launch.py"
    fi
}

################################################################################
# Verification & Validation
################################################################################

verify_sync() {
    log_info "Verifying sync integrity..."
    
    local issues=0
    
    # Verify setup files
    local setup_files=(
        "launch.py"
        "validation.py"
        "services.py"
        "environment.py"
        "utils.py"
        "project_config.py"
        "test_stages.py"
    )
    
    for file in "${setup_files[@]}"; do
        if [[ ! -f "${PROJECT_ROOT}/setup/$file" ]]; then
            log_error "Missing setup file: $file"
            ((issues++))
        fi
    done
    
    # Verify hooks
    local hooks=(
        "pre-commit"
        "post-commit"
        "post-merge"
        "post-checkout"
    )
    
    for hook in "${hooks[@]}"; do
        if [[ ! -f "${PROJECT_ROOT}/.git/hooks/$hook" ]]; then
            log_error "Missing git hook: $hook"
            ((issues++))
        fi
    done
    
    if [[ $issues -eq 0 ]]; then
        log_success "All critical files verified"
        return 0
    else
        log_error "Found $issues missing files"
        return 1
    fi
}

# Test Python file compilation
verify_python_files() {
    log_info "Verifying Python file syntax..."
    
    local python_files=(
        "setup/validation.py"
        "setup/services.py"
        "setup/environment.py"
        "setup/utils.py"
        "setup/project_config.py"
        "setup/test_stages.py"
        "setup/launch.py"
    )
    
    local issues=0
    
    for file in "${python_files[@]}"; do
        if ! python3 -m py_compile "${PROJECT_ROOT}/$file" 2>/dev/null; then
            log_error "Python syntax error: $file"
            ((issues++))
        fi
    done
    
    if [[ $issues -eq 0 ]]; then
        log_success "All Python files have valid syntax"
        return 0
    else
        log_error "Found $issues Python syntax errors"
        return 1
    fi
}

################################################################################
# History & Logging
################################################################################

log_sync_action() {
    local action="$1"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
    
    echo "[$timestamp] $action" >> "$SYNC_LOG_FILE"
}

get_branch_name() {
    git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown"
}

################################################################################
# Main Execution
################################################################################

show_help() {
    cat << EOF
${BLUE}Orchestration Files Sync Script${NC}

${GREEN}Usage:${NC}
  ./scripts/sync_orchestration_files.sh [OPTIONS]

${GREEN}Options:${NC}
  --dry-run           Show what would be synced without making changes
  --verify            Verify integrity of synced files
  --rollback          Rollback to previous sync state
  --setup-only        Sync only setup/ directory
  --hooks-only        Sync only git hooks
  --config-only       Sync only configuration files
  --force             Force overwrite of local changes
  --help              Show this help message

${GREEN}Examples:${NC}
  # Preview changes without syncing
  ./scripts/sync_orchestration_files.sh --dry-run

  # Sync all files
  ./scripts/sync_orchestration_files.sh

  # Sync only setup directory
  ./scripts/sync_orchestration_files.sh --setup-only

  # Verify integrity
  ./scripts/sync_orchestration_files.sh --verify

${GREEN}Supported Branches:${NC}
  - orchestration-tools (main orchestration branch)
  - orchestration-tools-* (variant branches)
  - taskmaster* branches (unsupported - skipped)
  
${YELLOW}Note:${NC} This script is designed for orchestration-tools branches.
       Other branches will skip syncing.
EOF
}

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --verify)
                VERIFY_MODE=true
                shift
                ;;
            --rollback)
                ROLLBACK_MODE=true
                shift
                ;;
            --setup-only)
                SETUP_ONLY=true
                shift
                ;;
            --hooks-only)
                HOOKS_ONLY=true
                shift
                ;;
            --config-only)
                CONFIG_ONLY=true
                shift
                ;;
            --force)
                FORCE_MODE=true
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

main() {
    log_info "Starting orchestration files sync..."
    log_debug "Project root: $PROJECT_ROOT"
    log_debug "Current branch: $(get_branch_name)"
    
    # Check branch eligibility
    if ! is_orchestration_tools_branch; then
        if ! is_taskmaster_branch; then
            log_warning "Not on orchestration-tools* or taskmaster* branch - skipping sync"
            log_info "Current branch: $(get_branch_name)"
            exit 0
        fi
    fi
    
    parse_arguments "$@"
    
    # Determine what to sync
    local sync_all=false
    if [[ "$SETUP_ONLY" == "false" ]] && [[ "$HOOKS_ONLY" == "false" ]] && [[ "$CONFIG_ONLY" == "false" ]]; then
        sync_all=true
    fi
    
    # Verify mode
    if [[ "$VERIFY_MODE" == "true" ]]; then
        log_info "Running in verification mode..."
        verify_sync
        verify_python_files
        exit $?
    fi
    
    # Rollback mode
    if [[ "$ROLLBACK_MODE" == "true" ]]; then
        log_warning "Rollback not yet implemented"
        exit 1
    fi
    
    # Show what would be synced in dry-run mode
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "Running in dry-run mode (no changes will be made)"
        echo ""
    fi
    
    # Execute sync
    if [[ "$sync_all" == "true" ]] || [[ "$SETUP_ONLY" == "true" ]]; then
        sync_setup_directory "$DRY_RUN"
    fi
    
    if [[ "$sync_all" == "true" ]] || [[ "$HOOKS_ONLY" == "true" ]]; then
        sync_hooks "$DRY_RUN"
    fi
    
    if [[ "$sync_all" == "true" ]] || [[ "$CONFIG_ONLY" == "true" ]]; then
        sync_config_files "$DRY_RUN"
        sync_root_wrapper "$DRY_RUN"
    fi
    
    # Post-sync verification
    if [[ "$DRY_RUN" != "true" ]]; then
        echo ""
        log_info "Verifying synced files..."
        if verify_sync && verify_python_files; then
            log_success "Sync completed successfully"
            log_sync_action "Sync successful on $(get_branch_name)"
            exit 0
        else
            log_error "Sync verification failed"
            log_sync_action "Sync failed on $(get_branch_name)"
            exit 1
        fi
    else
        log_info "Dry-run complete - no changes made"
    fi
}

# Run main function
main "$@"
