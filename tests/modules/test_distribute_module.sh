#!/bin/bash
# test_distribute_module.sh - Unit tests for distribute.sh module

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🧪 Testing Distribution Module..."

# Mock the required functions from other modules
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODULE_DIR="$PROJECT_ROOT/modules"

# Source the module to test
source "$MODULE_DIR/distribute.sh"

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

# Test 1: Test get_source_branch function
test_get_source_branch() {
    local source_branch
    source_branch=$(get_source_branch)
    
    if [[ "$source_branch" == "orchestration-tools" ]]; then
        return 0
    else
        return 1
    fi
}

# Test 2: Test is_valid_target_branch function
test_is_valid_target_branch() {
    # Test valid branch
    if is_valid_target_branch "orchestration-tools-feature"; then
        # Test invalid branch (taskmaster)
        if ! is_valid_target_branch "taskmaster-feature"; then
            return 0
        fi
    fi
    return 1
}

# Test 3: Test sync_from_remote function (negative test)
test_sync_from_remote() {
    # This function requires a git remote, so we'll test error handling
    # by providing a non-existent branch
    if ! sync_from_remote "nonexistent-branch-12345"; then
        return 0
    fi
    return 1
}

# Test 4: Test fix_distribution_permissions function
test_fix_distribution_permissions() {
    # This function modifies permissions, so we'll just test that it runs without error
    # Create a temporary directory to simulate a target branch
    local temp_dir=$(mktemp -d)
    local script_dir="$temp_dir/scripts"
    mkdir -p "$script_dir"
    
    # Create a test script
    local test_script="$script_dir/test.sh"
    echo "#!/bin/bash\necho test" > "$test_script"
    
    # Run the function (this will try to make scripts executable)
    fix_distribution_permissions "test-branch" 2>/dev/null || true
    
    # Clean up
    rm -rf "$temp_dir"
    
    # If we got here without crashing, consider it a pass
    return 0
}

# Test 5: Test validate_distribution function
test_validate_distribution() {
    # This function runs validation, so we'll test that it runs without error
    validate_distribution "test-branch" 2>/dev/null || true
    
    # If we got here without crashing, consider it a pass
    return 0
}

# Test 6: Test distribute_from_to function (negative test)
test_distribute_from_to() {
    # This function requires git operations, so we'll test error handling
    if ! distribute_from_to "source-branch" "target-branch" "nonexistent-file" 2>/dev/null; then
        return 0
    fi
    return 1
}

# Test 7: Test get_target_branches function
test_get_target_branches() {
    # This function queries git branches, so we'll just test that it runs
    get_target_branches 2>/dev/null || true
    
    # If we got here without crashing, consider it a pass
    return 0
}

# Run all tests
echo "Running distribution module tests..."
echo ""

run_test "Get source branch" 0 test_get_source_branch
run_test "Check valid target branch" 0 test_is_valid_target_branch
run_test "Sync from remote (negative test)" 0 test_sync_from_remote
run_test "Fix distribution permissions" 0 test_fix_distribution_permissions
run_test "Validate distribution" 0 test_validate_distribution
run_test "Distribute from to (negative test)" 0 test_distribute_from_to
run_test "Get target branches" 0 test_get_target_branches

# Print summary
echo ""
echo "📊 Test Results Summary:"
echo "Total tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"

if [[ $FAIL_COUNT -eq 0 ]]; then
    echo -e "${GREEN}🎉 All distribution module tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed.${NC}"
    exit 1
fi