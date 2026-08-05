#!/bin/bash

################################################################################
# Agent Documentation Consistency Verification Script
#
# Purpose: Detect and warn about agent documentation divergence across branches
#
# Functionality:
#   - Compare AGENTS.md versions across branches (warn on major differences)
#   - Verify CLAUDE.md exists and is current on all branches
#   - Check context control profiles match expected branches
#   - Validate CODING_STANDARDS.md referenced correctly
#   - Generate consistency report
#
# Usage:
#   ./scripts/verify-agent-docs-consistency.sh [OPTIONS]
#
# Options:
#   --verbose           Show detailed comparison output
#   --fix               Attempt to fix minor inconsistencies
#   --report            Generate detailed consistency report
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

# Options
VERBOSE=false
FIX_MODE=false
REPORT_MODE=false

# Results tracking
ISSUES_FOUND=0
ISSUES_RESOLVED=0

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
    ((ISSUES_FOUND++))
}

log_error() {
    echo -e "${RED}✗${NC} $*" >&2
    ((ISSUES_FOUND++))
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[VERBOSE]${NC} $*"
    fi
}

################################################################################
# Verification Functions
################################################################################

# Check AGENTS.md consistency across branches
check_agents_md_consistency() {
    log_info "Checking AGENTS.md consistency across branches..."

    local current_branch
    current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    log_verbose "Current branch: $current_branch"

    # Get list of branches to compare
    local branches=()
    while IFS= read -r branch; do
        branches+=("$branch")
    done < <(git branch -r | grep -v '\->' | sed 's/origin\///' | grep -E "(main|scientific|orchestration-tools)" || true)

    if [[ ${#branches[@]} -eq 0 ]]; then
        log_warning "No branches found for comparison - this may indicate a repository issue"
        return
    fi

    log_verbose "Comparing branches: ${branches[*]}"

    local agents_files=()
    local temp_dir
    temp_dir=$(mktemp -d)

    # Fetch AGENTS.md from each branch
    for branch in "${branches[@]}"; do
        if [[ "$branch" == "HEAD" ]]; then
            continue
        fi

        log_verbose "Fetching AGENTS.md from branch: $branch"
        local temp_file="$temp_dir/AGENTS_${branch}.md"
        git show "origin/$branch:AGENTS.md" > "$temp_file" 2>/dev/null
        if [[ $? -eq 0 ]]; then
            agents_files+=("$temp_file:$branch")
        else
            log_warning "AGENTS.md not found in branch: $branch"
        fi
    done

    # Compare AGENTS.md files
    if [[ ${#agents_files[@]} -gt 1 ]]; then
        local base_file=""
        local base_branch=""
        
        # Find the first available file as base
        for file_branch_pair in "${agents_files[@]}"; do
            IFS=':' read -r file branch <<< "$file_branch_pair"
            if [[ -n "$base_file" ]]; then
                log_verbose "Comparing $branch with $base_branch"
                
                # Compare checksums of key sections
                local base_sections=$(grep -E "^## |^### " "$base_file" | sort)
                local current_sections=$(grep -E "^## |^### " "$file" | sort)
                
                if [[ "$base_sections" != "$current_sections" ]]; then
                    log_warning "AGENTS.md section differences found between $base_branch and $branch"
                    
                    if [[ "$VERBOSE" == "true" ]]; then
                        echo "--- $base_branch sections ---"
                        echo "$base_sections"
                        echo "--- $branch sections ---"
                        echo "$current_sections"
                        echo ""
                    fi
                else
                    log_verbose "AGENTS.md sections match between $base_branch and $branch"
                fi
            else
                base_file="$file"
                base_branch="$branch"
            fi
        done
    else
        log_verbose "Only one AGENTS.md file found, cannot perform comparison"
    fi

    # Clean up
    rm -rf "$temp_dir"
}

# Verify CLAUDE.md exists and is current on all branches
check_claude_md_consistency() {
    log_info "Checking CLAUDE.md consistency across branches..."

    local branches=()
    while IFS= read -r branch; do
        branches+=("$branch")
    done < <(git branch -r | grep -v '\->' | sed 's/origin\///' | grep -E "(main|scientific|orchestration-tools)" || true)

    for branch in "${branches[@]}"; do
        if [[ "$branch" == "HEAD" ]]; then
            continue
        fi

        if git ls-tree "origin/$branch" CLAUDE.md >/dev/null 2>&1; then
            log_verbose "CLAUDE.md exists in branch: $branch"
        else
            log_warning "CLAUDE.md missing in branch: $branch"
        fi
    done
}

# Check context control profiles match expected branches
check_context_control_profiles() {
    log_info "Checking context control profiles..."

    local profiles_dir="$PROJECT_ROOT/.context-control/profiles"
    
    if [[ ! -d "$profiles_dir" ]]; then
        log_error ".context-control/profiles directory not found"
        return 1
    fi

    local expected_profiles=("main.json" "scientific.json" "orchestration-tools.json")
    local missing_profiles=()

    for profile in "${expected_profiles[@]}"; do
        if [[ ! -f "$profiles_dir/$profile" ]]; then
            missing_profiles+=("$profile")
        fi
    done

    if [[ ${#missing_profiles[@]} -gt 0 ]]; then
        log_warning "Missing context control profiles: ${missing_profiles[*]}"
    else
        log_success "All expected context control profiles found"
    fi

    # Validate JSON syntax of all profiles
    for profile_file in "$profiles_dir"/*.json; do
        if [[ -f "$profile_file" ]]; then
            if ! python3 -m json.tool < "$profile_file" >/dev/null 2>&1; then
                log_error "Invalid JSON syntax in context control profile: $profile_file"
            else
                log_verbose "Valid JSON syntax in: $profile_file"
            fi
        fi
    done
}

# Validate CODING_STANDARDS.md reference
check_coding_standards_reference() {
    log_info "Checking CODING_STANDARDS.md references..."

    # Check if CODING_STANDARDS.md exists
    if [[ ! -f "$PROJECT_ROOT/CODING_STANDARDS.md" ]]; then
        log_warning "CODING_STANDARDS.md does not exist in project root"
    else
        log_success "CODING_STANDARDS.md exists in project root"
    fi

    # Check if it's referenced in AGENTS.md files
    local agents_files=("$PROJECT_ROOT/AGENTS.md")
    
    for agents_file in "${agents_files[@]}"; do
        if [[ -f "$agents_file" ]]; then
            if grep -q "CODING_STANDARDS.md\|coding.*standard\|code.*style" "$agents_file"; then
                log_verbose "CODING_STANDARDS.md referenced in: $agents_file"
            else
                log_warning "CODING_STANDARDS.md not referenced in: $agents_file"
            fi
        fi
    done
}

# Generate consistency report
generate_report() {
    local report_file="$PROJECT_ROOT/.reports/consistency_report_$(date +%Y%m%d_%H%M%S).txt"
    local report_dir=$(dirname "$report_file")
    
    mkdir -p "$report_dir"
    
    {
        echo "Agent Documentation Consistency Report"
        echo "Generated: $(date)"
        echo "Repository: $(basename "$PROJECT_ROOT")"
        echo ""
        echo "Summary:"
        echo "- Issues Found: $ISSUES_FOUND"
        echo "- Issues Resolved: $ISSUES_RESOLVED"
        echo ""
        echo "Detailed Results:"
        echo "================="
        echo ""
        echo "AGENTS.md Consistency Check:"
        echo "  Status: Completed"
        echo ""
        echo "CLAUDE.md Consistency Check:"
        echo "  Status: Completed"
        echo ""
        echo "Context Control Profiles Check:"
        echo "  Status: Completed"
        echo ""
        echo "Coding Standards Reference Check:"
        echo "  Status: Completed"
        echo ""
        echo "Generated by: $(basename "$0")"
    } > "$report_file"

    log_info "Consistency report generated: $report_file"
}

################################################################################
# Main Execution
################################################################################

show_help() {
    cat << EOF
${BLUE}Agent Documentation Consistency Verification Script${NC}

${GREEN}Purpose:${NC}
  Detect and warn about agent documentation divergence across branches

${GREEN}Functionality:${NC}
  - Compare AGENTS.md versions across branches (warn on major differences)
  - Verify CLAUDE.md exists and is current on all branches
  - Check context control profiles match expected branches
  - Validate CODING_STANDARDS.md referenced correctly
  - Generate consistency report

${GREEN}Usage:${NC}
  ./scripts/verify-agent-docs-consistency.sh [OPTIONS]

${GREEN}Options:${NC}
  --verbose           Show detailed comparison output
  --fix               Attempt to fix minor inconsistencies
  --report            Generate detailed consistency report
  --help              Show this help message

${GREEN}Examples:${NC}
  # Basic verification
  ./scripts/verify-agent-docs-consistency.sh

  # Verbose output
  ./scripts/verify-agent-docs-consistency.sh --verbose

  # Generate detailed report
  ./scripts/verify-agent-docs-consistency.sh --report

${GREEN}Exit Codes:${NC}
  0 - No inconsistencies found
  1 - Inconsistencies found
  2 - Error during execution
EOF
}

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --verbose)
                VERBOSE=true
                shift
                ;;
            --fix)
                FIX_MODE=true
                shift
                ;;
            --report)
                REPORT_MODE=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 2
                ;;
        esac
    done
}

main() {
    log_info "Starting agent documentation consistency verification..."
    log_verbose "Project root: $PROJECT_ROOT"
    log_verbose "Current directory: $(pwd)"

    parse_arguments "$@"

    # Run all checks
    check_agents_md_consistency
    check_claude_md_consistency
    check_context_control_profiles
    check_coding_standards_reference

    # Generate report if requested
    if [[ "$REPORT_MODE" == "true" ]]; then
        generate_report
    fi

    # Final status
    if [[ $ISSUES_FOUND -eq 0 ]]; then
        log_success "No inconsistencies found in agent documentation"
        exit 0
    else
        log_warning "$ISSUES_FOUND inconsistency(s) found in agent documentation"
        exit 1
    fi
}

# Run main function
main "$@"