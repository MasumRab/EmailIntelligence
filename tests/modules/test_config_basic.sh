#!/bin/bash
# test_config_module_basic.sh - Basic tests for config.sh module

set -u  # Only check for undefined variables, not exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🧪 Testing Configuration Module..."

# Mock the required functions from other modules
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODULE_DIR="$PROJECT_ROOT/modules"

# Source the module to test
source "$MODULE_DIR/config.sh"

# Counter for test results
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

# Test runner function - modified to handle errors gracefully
run_test() {
    local test_name="$1"
    local expected_result="$2"
    shift 2
    ((TEST_COUNT++))
    
    echo -n "Test $TEST_COUNT: $test_name... "
    
    # Capture the result of the function call using a subshell to isolate errors
    if ( "$@" 2>/dev/null ); then
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

# Test 1: Test create_default_config function
test_create_default_config() {
    # Create a temporary config directory
    local temp_dir=$(mktemp -d)
    local original_config_path="$CONFIG_FILE_PATH"
    
    # Override the config path for testing
    CONFIG_FILE_PATH="$temp_dir/config/distribution.json"
    
    # Create the directory
    mkdir -p "$(dirname "$CONFIG_FILE_PATH")"
    
    # Run the function
    create_default_config
    
    # Check if the file was created
    if [[ -f "$CONFIG_FILE_PATH" ]]; then
        # Check if it contains expected content
        if grep -q "sources" "$CONFIG_FILE_PATH" && grep -q "targets" "$CONFIG_FILE_PATH"; then
            # Restore original path
            CONFIG_FILE_PATH="$original_config_path"
            rm -rf "$temp_dir"
            return 0
        else
            # Restore original path
            CONFIG_FILE_PATH="$original_config_path"
            rm -rf "$temp_dir"
            return 1
        fi
    else
        # Restore original path
        CONFIG_FILE_PATH="$original_config_path"
        rm -rf "$temp_dir"
        return 1
    fi
}

# Test 2: Test get_branch_config function
test_get_branch_config() {
    local result
    result=$(get_branch_config "orchestration-tools-feature")
    
    # Check if result contains expected content
    if [[ "$result" == *"allowed"* ]] && [[ "$result" == *"true"* ]]; then
        return 0
    else
        return 1
    fi
}

# Test 3: Test get_branch_config for taskmaster branch
test_get_branch_config_taskmaster() {
    local result
    result=$(get_branch_config "taskmaster-feature")
    
    # Check if result indicates taskmaster is not allowed
    if [[ "$result" == *"allowed"* ]] && [[ "$result" == *"false"* ]]; then
        return 0
    else
        return 1
    fi
}

# Test 4: Test is_branch_allowed_for_distribution function
test_is_branch_allowed() {
    # Test allowed branch
    if is_branch_allowed_for_distribution "orchestration-tools-feature"; then
        # Now test disallowed branch
        if ! is_branch_allowed_for_distribution "main"; then
            return 0
        else
            return 1
        fi
    else
        return 1
    fi
}

# Test 5: Test get_large_file_threshold function
test_get_large_file_threshold() {
    local threshold
    threshold=$(get_large_file_threshold)
    
    # Check if threshold is a number and reasonable
    if [[ "$threshold" =~ ^[0-9]+$ ]] && [[ $threshold -gt 1000000 ]]; then
        return 0
    else
        return 1
    fi
}

# Test 6: Test get_sensitive_patterns function
test_get_sensitive_patterns() {
    local patterns
    patterns=$(get_sensitive_patterns)
    
    # Check if patterns contain expected keywords
    if [[ "$patterns" == *"password"* ]] && [[ "$patterns" == *"secret"* ]]; then
        return 0
    else
        return 1
    fi
}

# Test 7: Test get_required_files function
test_get_required_files() {
    local files
    files=$(get_required_files)
    
    # Check if files contain expected paths
    if [[ "$files" == *"install-hooks.sh"* ]] && [[ "$files" == *"launch.py"* ]]; then
        return 0
    else
        return 1
    fi
}

# Test 8: Test get_distribution_method function
test_get_distribution_method() {
    local method
    method=$(get_distribution_method "orchestration-tools-feature")
    
    if [[ "$method" == "git-worktree-safe" ]]; then
        return 0
    else
        return 1
    fi
}

# Test 9: Test is_validation_required_after_sync function
test_is_validation_required_after_sync() {
    # Test orchestration-tools branch (should require validation)
    if is_validation_required_after_sync "orchestration-tools-feature"; then
        # Test other branch (should not require validation)
        if ! is_validation_required_after_sync "main"; then
            return 0
        else
            return 1
        fi
    else
        return 1
    fi
}

# Run all tests
echo "Running configuration module tests..."
echo ""

run_test "Create default config" 0 test_create_default_config
run_test "Get branch config for orchestration-tools" 0 test_get_branch_config
run_test "Get branch config for taskmaster" 0 test_get_branch_config_taskmaster
run_test "Check branch allowed for distribution" 0 test_is_branch_allowed
run_test "Get large file threshold" 0 test_get_large_file_threshold
run_test "Get sensitive patterns" 0 test_get_sensitive_patterns
run_test "Get required files" 0 test_get_required_files
run_test "Get distribution method" 0 test_get_distribution_method
run_test "Check validation required after sync" 0 test_is_validation_required_after_sync

# Print summary
echo ""
echo "📊 Test Results Summary:"
echo "Total tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"

if [[ $FAIL_COUNT -eq 0 ]]; then
    echo -e "${GREEN}🎉 All configuration module tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed.${NC}"
    exit 1
fi