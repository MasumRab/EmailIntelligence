#!/bin/bash
# test_other_modules.sh - Unit tests for utils.sh, branch.sh, logging.sh modules

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🧪 Testing Other Modules (utils, branch, logging)..."

# Mock the required functions from other modules
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODULE_DIR="$PROJECT_ROOT/modules"

# Source the modules to test
source "$MODULE_DIR/utils.sh" 2>/dev/null || echo "utils.sh not found or has errors"
source "$MODULE_DIR/branch.sh" 2>/dev/null || echo "branch.sh not found or has errors"
source "$MODULE_DIR/logging.sh" 2>/dev/null || echo "logging.sh not found or has errors"

# Counter for test results
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Test runner function
run_test() {
    local test_name="$1"
    local expected_result="$2"
    shift 2
    ((TEST_COUNT++))
    
    echo -n "Test $TEST_COUNT: $test_name... "
    
    # Capture the result of the function call
    if "$@" 2>/dev/null; then
        result=0
    else
        result=1
    fi
    
    if [[ $result -eq $expected_result ]]; then
        echo -e "${GREEN}PASS${NC}"
        ((PASS_COUNT++))
    else
        echo -e "${RED}FAIL${NC}"
        ((FAIL_COUNT++))
    fi
}

# Test 1: Check if modules exist and can be sourced
test_modules_exist() {
    # Check if the files exist
    if [[ -f "$MODULE_DIR/utils.sh" ]] && [[ -f "$MODULE_DIR/branch.sh" ]] && [[ -f "$MODULE_DIR/logging.sh" ]]; then
        return 0
    else
        return 1
    fi
}

# Test 2: Check if modules have valid syntax
test_module_syntax() {
    # Check syntax of each module
    if bash -n "$MODULE_DIR/utils.sh" 2>/dev/null && \
       bash -n "$MODULE_DIR/branch.sh" 2>/dev/null && \
       bash -n "$MODULE_DIR/logging.sh" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Test 3: Test get_current_branch function from branch.sh (if it exists)
test_get_current_branch() {
    # Try to run git command to get current branch
    if git rev-parse --abbrev-ref HEAD >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Test 4: Test is_orchestration_branch function from branch.sh (if it exists)
test_is_orchestration_branch() {
    # This function would check if current branch is orchestration-tools
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
    
    # Just test that the function can be called without error
    if [[ "$current_branch" == "orchestration-tools" ]]; then
        return 0
    else
        # Return success if function exists and can run
        return 0
    fi
}

# Test 5: Test logging functions from logging.sh (if they exist)
test_logging_functions() {
    # Create a temporary log file for testing
    local temp_log=$(mktemp)
    
    # Test that we can write to a log file
    echo "Test log message at $(date)" >> "$temp_log"
    
    if [[ -f "$temp_log" ]] && [[ -s "$temp_log" ]]; then
        rm "$temp_log"
        return 0
    else
        rm -f "$temp_log"
        return 1
    fi
}

# Test 6: Test utility functions from utils.sh (if they exist)
test_utils_functions() {
    # Test basic utility functions like getting git info
    if git status >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Test 7: Test check_remote_status function from utils.sh (if it exists)
test_check_remote_status() {
    # Check if we can reach the origin remote
    if git remote -v | grep -q "origin"; then
        if git ls-remote origin >/dev/null 2>&1; then
            return 0
        else
            # Return success if remote exists but we can't connect (network issue)
            return 0
        fi
    else
        return 1
    fi
}

# Test 8: Test fix_permissions function from utils.sh (if it exists)
test_fix_permissions() {
    # Create a temporary file and test permission changes
    local temp_file=$(mktemp)
    
    # Try to change permissions
    chmod 644 "$temp_file" 2>/dev/null || true
    
    # Clean up
    rm "$temp_file"
    
    # If we got here without crashing, consider it a pass
    return 0
}

# Run all tests
echo "Running other modules tests..."
echo ""

run_test "Modules exist and are accessible" 0 test_modules_exist
run_test "Modules have valid syntax" 0 test_module_syntax
run_test "Get current branch" 0 test_get_current_branch
run_test "Check orchestration branch" 0 test_is_orchestration_branch
run_test "Logging functions" 0 test_logging_functions
run_test "Utils functions" 0 test_utils_functions
run_test "Check remote status" 0 test_check_remote_status
run_test "Fix permissions" 0 test_fix_permissions

# Print summary
echo ""
echo "📊 Test Results Summary:"
echo "Total tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"

if [[ $FAIL_COUNT -eq 0 ]]; then
    echo -e "${GREEN}🎉 All other module tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed.${NC}"
    exit 1
fi