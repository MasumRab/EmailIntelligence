#!/bin/bash
# Orchestration Status Dashboard
# Comprehensive monitoring and reporting for orchestration system health

# Note: Not using 'set -e' to allow graceful error handling and continue monitoring

# Colors and formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Symbols
CHECK="✅"
CROSS="❌"
WARNING="⚠️"
INFO="ℹ️"
GEAR="⚙️"

# Configuration
ORCHESTRATION_BRANCH="orchestration-tools"

# Status tracking
STATUS_PASSED=0
STATUS_WARNINGS=0
STATUS_FAILED=0

# Logging functions
log_header() {
    echo -e "\n${BLUE}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${WHITE} $1 ${BLUE}$(printf '%*s' $((78-${#1})) '')║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════════════════╝${NC}\n"
}

log_section() {
    echo -e "\n${CYAN}┌─ $1 ${CYAN}$(printf '%.0s─' $(seq 1 $((75-${#1}))))┐${NC}"
}

log_item() {
    local status="$1"
    local message="$2"

    case "$status" in
        "PASS")
            echo -e "${GREEN}${CHECK} ${message}${NC}"
            ((STATUS_PASSED++))
            ;;
        "FAIL")
            echo -e "${RED}${CROSS} ${message}${NC}"
            ((STATUS_FAILED++))
            ;;
        "WARN")
            echo -e "${YELLOW}${WARNING} ${message}${NC}"
            ((STATUS_WARNINGS++))
            ;;
        "INFO")
            echo -e "${BLUE}${INFO} ${message}${NC}"
            ;;
    esac
}

check_orchestration_files() {
    log_section "Orchestration Files Status"

    local managed_files=(
        "setup/launch.py"
        "setup/launch.bat"
        "setup/launch.sh"
        "setup/pyproject.toml"
        "setup/requirements.txt"
        "setup/requirements-dev.txt"
        "setup/requirements-cpu.txt"
        ".flake8"
        ".pylintrc"
        ".gitignore"
        ".gitattributes"
        "scripts/sync_setup_worktrees.sh"
        "scripts/reverse_sync_orchestration.sh"
        "scripts/cleanup_orchestration.sh"
        "scripts/install-hooks.sh"
    )

    local missing_files=()
    local corrupted_files=()

    for file in "${managed_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        elif [[ ! -s "$file" ]]; then
            corrupted_files+=("$file (empty)")
        fi
    done

    if [[ ${#missing_files[@]} -eq 0 ]]; then
        log_item "PASS" "All orchestration-managed files present"
    else
        log_item "FAIL" "Missing orchestration files: ${missing_files[*]}"
    fi

    if [[ ${#corrupted_files[@]} -eq 0 ]]; then
        log_item "PASS" "No corrupted orchestration files detected"
    else
        log_item "WARN" "Potentially corrupted files: ${corrupted_files[*]}"
    fi
}

check_git_hooks() {
    log_section "Git Hooks Status"

    local required_hooks=("pre-commit" "post-commit" "post-merge" "post-checkout" "post-push")
    local installed_hooks=0
    local executable_hooks=0

    for hook in "${required_hooks[@]}"; do
        local hook_path=".git/hooks/$hook"
        if [[ -f "$hook_path" ]]; then
            ((installed_hooks++))
            if [[ -x "$hook_path" ]]; then
                ((executable_hooks++))
            fi
        fi
    done

    if [[ $installed_hooks -eq ${#required_hooks[@]} ]]; then
        log_item "PASS" "All required Git hooks installed ($installed_hooks/${#required_hooks[@]})"
    else
        log_item "WARN" "Missing Git hooks: $installed_hooks/${#required_hooks[@]} installed"
    fi

    if [[ $executable_hooks -eq $installed_hooks ]]; then
        log_item "PASS" "All installed hooks are executable"
    else
        log_item "WARN" "Some hooks not executable: $executable_hooks/$installed_hooks executable"
    fi

    # Check hook syntax
    local syntax_errors=0
    for hook in .git/hooks/*; do
        if [[ -f "$hook" && -x "$hook" && "${hook##*/}" != *"sample"* ]]; then
            if ! bash -n "$hook" 2>/dev/null; then
                ((syntax_errors++))
                log_item "FAIL" "Syntax error in hook: ${hook##*/}"
            fi
        fi
    done

    if [[ $syntax_errors -eq 0 ]]; then
        log_item "PASS" "All hook syntax is valid"
    fi
}

generate_summary() {
    log_header "ORCHESTRATION STATUS SUMMARY"

    echo -e "${WHITE}Status Overview:${NC}"
    echo -e "  ${GREEN}${CHECK} Passed: $STATUS_PASSED${NC}"
    if [[ $STATUS_WARNINGS -gt 0 ]]; then
        echo -e "  ${YELLOW}${WARNING} Warnings: $STATUS_WARNINGS${NC}"
    fi
    if [[ $STATUS_FAILED -gt 0 ]]; then
        echo -e "  ${RED}${CROSS} Failed: $STATUS_FAILED${NC}"
    fi

    echo -e "\n${WHITE}System Health:${NC}"
    if [[ $STATUS_FAILED -eq 0 && $STATUS_WARNINGS -eq 0 ]]; then
        echo -e "  ${GREEN}${GEAR} Orchestration system is HEALTHY${NC}"
    elif [[ $STATUS_FAILED -eq 0 ]]; then
        echo -e "  ${YELLOW}${WARNING} Orchestration system has minor issues${NC}"
    else
        echo -e "  ${RED}${CROSS} Orchestration system has critical issues${NC}"
    fi

    echo -e "\n${PURPLE}Report generated on: $(date)${NC}"
}

main() {
    log_header "ORCHESTRATION SYSTEM STATUS DASHBOARD"

    echo -e "${WHITE}Monitoring orchestration system health...${NC}\n"

    check_orchestration_files
    check_git_hooks

    generate_summary
}

main "$@"
EOF && chmod +x scripts/orchestration_status.sh && git add scripts/orchestration_status.sh && git commit -m "Add orchestration status monitoring dashboard to orchestration-tools" && git push origin orchestration-tools
