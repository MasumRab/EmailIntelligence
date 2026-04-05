#!/bin/bash
# test_validate_module.sh - Unit tests for validate.sh module

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🧪 Testing Validation Module..."

# Mock the required functions from other modules
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MODULE_DIR="$PROJECT_ROOT/modules"

# Source the module to test
source "$MODULE_DIR/validate.sh"

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

# Test 1: Test validate_branch_type function
test_validate_branch_type() {
    # Test orchestration-tools branch
    if validate_branch_type "orchestration-tools-feature"; then
        # Test main branch
        if validate_branch_type "main"; then
            # Test taskmaster branch
            if validate_branch_type "taskmaster-feature"; then
                return 0
            fi
        fi
    fi
    return 1
}

# Test 2: Test validate_file_integrity function
test_validate_file_integrity() {
    # Create temporary files for testing
    local temp_dir=$(mktemp -d)
    local source_file="$temp_dir/source.txt"
    local target_file="$temp_dir/target.txt"
    
    echo "test content" > "$source_file"
    echo "test content" > "$target_file"
    
    # Test with matching files
    if validate_file_integrity "$source_file" "$target_file"; then
        # Test with different files
        echo "different content" > "$temp_dir/different.txt"
        if ! validate_file_integrity "$source_file" "$temp_dir/different.txt"; then
            rm -rf "$temp_dir"
            return 0
        fi
    fi
    
    rm -rf "$temp_dir"
    return 1
}

# Test 3: Test validate_permissions function
test_validate_permissions() {
    # Create temporary script file
    local temp_dir=$(mktemp -d)
    local script_file="$temp_dir/test_script.sh"
    
    echo "#!/bin/bash\necho test" > "$script_file"
    
    # Make it executable
    chmod +x "$script_file"
    
    # Test with executable file
    if validate_permissions "$script_file"; then
        # Make it non-executable
        chmod -x "$script_file"
        
        # This should return 1 (fail) since it's a .sh file but not executable
        if ! validate_permissions "$script_file"; then
            rm -rf "$temp_dir"
            return 0
        fi
    fi
    
    rm -rf "$temp_dir"
    return 1
}

# Test 4: Test validate_large_files function
test_validate_large_files() {
    # Create temporary directory with small files
    local temp_dir=$(mktemp -d)
    echo "small content" > "$temp_dir/small_file.txt"
    
    # Test with small files (should pass)
    if validate_large_files "$temp_dir" 1000000; then  # 1MB threshold
        rm -rf "$temp_dir"
        return 0
    fi
    
    rm -rf "$temp_dir"
    return 1
}

# Test 5: Test validate_sensitive_data function
test_validate_sensitive_data() {
    # Create temporary file without sensitive data
    local temp_dir=$(mktemp -d)
    local safe_file="$temp_dir/safe.txt"
    echo "This is safe content" > "$safe_file"
    
    # Test with safe file (should pass)
    if validate_sensitive_data "$safe_file"; then
        # Create file with sensitive data
        local sensitive_file="$temp_dir/sensitive.txt"
        echo "This contains a password" > "$sensitive_file"
        
        # Test with sensitive file (should fail)
        if ! validate_sensitive_data "$sensitive_file"; then
            rm -rf "$temp_dir"
            return 0
        fi
    fi
    
    rm -rf "$temp_dir"
    return 1
}

# Test 6: Test validate_required_files function
test_validate_required_files() {
    # Create temporary files
    local temp_dir=$(mktemp -d)
    local file1="$temp_dir/file1.txt"
    local file2="$temp_dir/file2.txt"
    echo "content1" > "$file1"
    echo "content2" > "$file2"
    
    # Test with existing files (should pass)
    if validate_required_files "$file1" "$file2"; then
        # Test with missing file (should fail)
        local missing_file="$temp_dir/missing.txt"
        if ! validate_required_files "$file1" "$missing_file"; then
            rm -rf "$temp_dir"
            return 0
        fi
    fi
    
    rm -rf "$temp_dir"
    return 1
}

# Test 7: Test validate_commit_size function
test_validate_commit_size() {
    # This function depends on git state, so we'll test with a high threshold
    # that should always pass
    if validate_commit_size 100000000; then  # 100MB threshold
        return 0
    fi
    return 1
}

# Test 8: Test validate_merge_conflicts function
test_validate_merge_conflicts() {
    # This function checks for merge conflicts in the current git state
    # In a clean repo, it should pass
    if validate_merge_conflicts; then
        return 0
    fi
    return 1
}

# Test 9: Test validate_remote_sync function
test_validate_remote_sync() {
    # This function requires a git remote, so we'll test error handling
    # by providing a non-existent branch
    if ! validate_remote_sync "nonexistent-branch-12345"; then
        return 0
    fi
    return 1
}

# Run all tests
echo "Running validation module tests..."
echo ""

run_test "Validate branch type" 0 test_validate_branch_type
run_test "Validate file integrity" 0 test_validate_file_integrity
run_test "Validate permissions" 0 test_validate_permissions
run_test "Validate large files" 0 test_validate_large_files
run_test "Validate sensitive data" 0 test_validate_sensitive_data
run_test "Validate required files" 0 test_validate_required_files
run_test "Validate commit size" 0 test_validate_commit_size
run_test "Validate merge conflicts" 0 test_validate_merge_conflicts
run_test "Validate remote sync (negative test)" 0 test_validate_remote_sync

# Print summary
echo ""
echo "📊 Test Results Summary:"
echo "Total tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"

if [[ $FAIL_COUNT -eq 0 ]]; then
    echo -e "${GREEN}🎉 All validation module tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed.${NC}"
    exit 1
fi