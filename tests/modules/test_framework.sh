#!/bin/bash
# test_framework.sh - Bash test framework with proper isolation and error handling

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TEST_FRAMEWORK_TOTAL=0
TEST_FRAMEWORK_PASS=0
TEST_FRAMEWORK_FAIL=0

# Initialize test framework
test_framework_init() {
    TEST_FRAMEWORK_TOTAL=0
    TEST_FRAMEWORK_PASS=0
    TEST_FRAMEWORK_FAIL=0
}

# Run a test function in a subshell to isolate errors
# Usage: test_run "Test name" test_function_name [expected_result]
test_run() {
    local test_name="$1"
    local test_func="$2"
    local expected="${3:-0}"

    TEST_FRAMEWORK_TOTAL=$((TEST_FRAMEWORK_TOTAL + 1))

    echo -n "  Test $TEST_FRAMEWORK_TOTAL: $test_name... "

    # Run in subshell to capture exit code without exiting
    local result
    (
        # Disable exit-on-error for the test
        set +e
        "$test_func"
        exit $?
    ) 2>/dev/null
    result=$?

    if [[ $result -eq $expected ]]; then
        echo -e "${GREEN}PASS${NC}"
        TEST_FRAMEWORK_PASS=$((TEST_FRAMEWORK_PASS + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC} (expected: $expected, got: $result)"
        TEST_FRAMEWORK_FAIL=$((TEST_FRAMEWORK_FAIL + 1))
        return 1
    fi
}

# Run a test with inline code instead of function
# Usage: test_run_inline "Test name" 'inline bash code' [expected_result]
test_run_inline() {
    local test_name="$1"
    local test_code="$2"
    local expected="${3:-0}"

    TEST_FRAMEWORK_TOTAL=$((TEST_FRAMEWORK_TOTAL + 1))

    echo -n "  Test $TEST_FRAMEWORK_TOTAL: $test_name... "

    # Run in subshell
    local result
    (
        set +e
        eval "$test_code"
        exit $?
    ) 2>/dev/null
    result=$?

    if [[ $result -eq $expected ]]; then
        echo -e "${GREEN}PASS${NC}"
        TEST_FRAMEWORK_PASS=$((TEST_FRAMEWORK_PASS + 1))
        return 0
    else
        echo -e "${RED}FAIL${NC} (expected: $expected, got: $result)"
        TEST_FRAMEWORK_FAIL=$((TEST_FRAMEWORK_FAIL + 1))
        return 1
    fi
}

# Print test summary
test_framework_summary() {
    local module_name="${1:-Unknown}"

    echo ""
    echo "  📊 $module_name Test Results:"
    echo "  Total tests: $TEST_FRAMEWORK_TOTAL"
    echo -e "  ${GREEN}Passed: $TEST_FRAMEWORK_PASS${NC}"
    echo -e "  ${RED}Failed: $TEST_FRAMEWORK_FAIL${NC}"
    echo ""

    if [[ $TEST_FRAMEWORK_FAIL -eq 0 ]]; then
        echo -e "  ${GREEN}✅ All $module_name tests passed!${NC}"
        return 0
    else
        echo -e "  ${RED}❌ $TEST_FRAMEWORK_FAIL $module_name test(s) failed${NC}"
        return 1
    fi
}

# Create a temporary directory for testing and clean up after
# Usage: test_with_temp_dir test_function
test_with_temp_dir() {
    local test_func="$1"
    local temp_dir

    temp_dir=$(mktemp -d)

    # Run test with TEMP_DIR variable set
    (
        set +e
        export TEMP_DIR="$temp_dir"
        "$test_func"
        local result=$?

        # Cleanup
        rm -rf "$temp_dir"
        exit $result
    ) 2>/dev/null

    return $?
}

# Mock a function temporarily
# Usage: with_mock "function_name() { ... }" test_function
with_mock() {
    local mock_def="$1"
    local test_func="$2"

    (
        set +e
        # Define the mock
        eval "$mock_def"
        # Run the test
        "$test_func"
        exit $?
    ) 2>/dev/null

    return $?
}

# Simple assertion helpers (avoiding complex quote nesting)
assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Values do not match}"

    if [[ "$expected" == "$actual" ]]; then
        return 0
    else
        echo "    ASSERTION FAILED: $message (expected: $expected, got: $actual)" >&2
        return 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String not found}"

    if [[ "$haystack" == *"$needle"* ]]; then
        return 0
    else
        echo "    ASSERTION FAILED: $message (expected to contain: $needle, in: $haystack)" >&2
        return 1
    fi
}

assert_file_exists() {
    local file="$1"
    local message="${2:-File should exist}"

    if [[ -f "$file" ]]; then
        return 0
    else
        echo "    ASSERTION FAILED: $message ($file)" >&2
        return 1
    fi
}

assert_file_not_exists() {
    local file="$1"
    local message="${2:-File should not exist}"

    if [[ ! -f "$file" ]]; then
        return 0
    else
        echo "    ASSERTION FAILED: $message ($file)" >&2
        return 1
    fi
}

assert_success() {
    local message="${1:-Command should succeed}"
    shift

    if "$@" 2>/dev/null; then
        return 0
    else
        echo "    ASSERTION FAILED: $message" >&2
        return 1
    fi
}

assert_failure() {
    local message="${1:-Command should fail}"
    shift

    if ! "$@" 2>/dev/null; then
        return 0
    else
        echo "    ASSERTION FAILED: $message" >&2
        return 1
    fi
}

# Export framework functions
export -f test_framework_init
export -f test_run
export -f test_run_inline
export -f test_framework_summary
export -f test_with_temp_dir
export -f with_mock
export -f assert_equals
export -f assert_contains
export -f assert_file_exists
export -f assert_file_not_exists
export -f assert_success
export -f assert_failure
export TEST_FRAMEWORK_TOTAL
export TEST_FRAMEWORK_PASS
export TEST_FRAMEWORK_FAIL