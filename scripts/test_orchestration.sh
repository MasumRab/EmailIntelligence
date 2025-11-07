#!/bin/bash
# Orchestration Testing Framework
# Tests the orchestration system components and workflows

# set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEST_RESULTS=()
FAILED_TESTS=0
PASSED_TESTS=0

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Test runner
run_test() {
    local test_name="$1"
    local test_function="$2"

    log_info "Running test: $test_name"

    if $test_function; then
        log_success "$test_name"
        TEST_RESULTS+=("$test_name:PASS")
        ((PASSED_TESTS++))
        return 0
    else
        log_error "$test_name"
        TEST_RESULTS+=("$test_name:FAIL")
        ((FAILED_TESTS++))
        return 1
    fi
}

# Test functions

test_hook_installation() {
    # Test hook installation script
    if [[ -f "$SCRIPT_DIR/install-hooks.sh" ]]; then
        bash "$SCRIPT_DIR/install-hooks.sh" --help >/dev/null 2>&1
        return $?
    fi
    return 1
}

test_hook_syntax() {
    # Test hook script syntax
    local failed=false

    for hook in "$SCRIPT_DIR/hooks"/*; do
        if [[ -f "$hook" && -x "$hook" ]]; then
            if ! bash -n "$hook" 2>/dev/null; then
                log_error "Syntax error in hook: $(basename "$hook")"
                failed=true
            fi
        fi
    done

    if [[ "$failed" == true ]]; then
        return 1
    fi
    return 0
}

test_managed_files_list() {
    # Test that managed files lists are consistent
    local reverse_sync_list
    local post_push_list

    # Extract managed files from reverse sync script
    reverse_sync_list=$(grep -A 50 "MANAGED_FILES=(" "$SCRIPT_DIR/reverse_sync_orchestration.sh" | grep -E '^    "[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/' | sort)

    # Extract managed files from post-push script
    post_push_list=$(grep -A 50 "MANAGED_FILES=(" "$SCRIPT_DIR/hooks/post-push" | grep -E '^        "[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/' | sort)

    if [[ "$reverse_sync_list" != "$post_push_list" ]]; then
        log_error "MANAGED_FILES lists are inconsistent between scripts"
        echo "Reverse sync list:"
        echo "$reverse_sync_list"
        echo "Post-push list:"
        echo "$post_push_list"
        return 1
    fi

    return 0
}

test_setup_file_syntax() {
    # Test Python files in setup directory
    local failed=false

    for py_file in "$PROJECT_ROOT/setup"/*.py; do
        if [[ -f "$py_file" ]]; then
            if ! python3 -m py_compile "$py_file" 2>/dev/null; then
                log_error "Syntax error in setup file: $(basename "$py_file")"
                failed=true
            fi
        fi
    done

    if [[ "$failed" == true ]]; then
        return 1
    fi
    return 0
}

test_orchestration_branch_exists() {
    # Test that orchestration-tools branch exists
    if ! git show-ref --verify --quiet refs/heads/orchestration-tools && \
       ! git ls-remote --exit-code --heads origin orchestration-tools >/dev/null 2>&1; then
        log_error "orchestration-tools branch not found"
        return 1
    fi
    return 0
}

# Main test execution
main() {
    log_info "Starting Orchestration Testing Framework"
    log_info "Project root: $PROJECT_ROOT"
    echo

    # Run all tests
    run_test "Hook Installation Script" test_hook_installation
    run_test "Hook Script Syntax" test_hook_syntax
    run_test "Managed Files List Consistency" test_managed_files_list
    run_test "Setup File Syntax" test_setup_file_syntax
    run_test "Orchestration Branch Exists" test_orchestration_branch_exists

    echo
    log_info "Test Results Summary:"
    log_info "======================"
    log_success "Passed: $PASSED_TESTS"
    if [[ $FAILED_TESTS -gt 0 ]]; then
        log_error "Failed: $FAILED_TESTS"
    else
        log_success "Failed: $FAILED_TESTS"
    fi

    echo
    log_info "Detailed Results:"
    for result in "${TEST_RESULTS[@]}"; do
        if [[ $result == *":PASS" ]]; then
            log_success "${result%:*}"
        else
            log_error "${result%:*}"
        fi
    done

    # Exit with failure if any tests failed
    if [[ $FAILED_TESTS -gt 0 ]]; then
        echo
        log_error "Some orchestration tests failed. Please review the errors above."
        exit 1
    else
        echo
        log_success "All orchestration tests passed! ✅"
        exit 0
    fi
}

# Run main function
main "$@"
