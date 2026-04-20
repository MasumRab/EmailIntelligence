#!/bin/bash
# test_config_module.sh - Unit tests for config.sh module

set -euo pipefail

# Source the test framework
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FRAMEWORK_DIR="$PROJECT_ROOT/tests/modules"
source "$FRAMEWORK_DIR/test_framework.sh"

echo "🧪 Testing Configuration Module..."

# Mock the required functions from other modules
MODULE_DIR="$PROJECT_ROOT/modules"

# Source the module to test
source "$MODULE_DIR/config.sh"

# Initialize test framework
test_framework_init

# Test 1: Test create_default_config function
test_create_default_config() {
    # Create a temporary config directory
    local temp_dir=$(mktemp -d)
    
    # Override the config path for testing using subshell to isolate
    (
        export CONFIG_FILE_PATH="$temp_dir/config/distribution.json"
        
        # Create the directory
        mkdir -p "$(dirname "$CONFIG_FILE_PATH")"
        
        # Run the function
        create_default_config
        
        # Check if the file was created
        if [[ -f "$CONFIG_FILE_PATH" ]]; then
            # Check if it contains expected content
            if grep -q "sources" "$CONFIG_FILE_PATH" && grep -q "targets" "$CONFIG_FILE_PATH"; then
                exit 0
            else
                exit 1
            fi
        else
            exit 1
        fi
    )
    
    # Clean up
    rm -rf "$temp_dir"
    return $?
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

test_run "Create default config" test_create_default_config 0
test_run "Get branch config for orchestration-tools" test_get_branch_config 0
test_run "Get branch config for taskmaster" test_get_branch_config_taskmaster 0
test_run "Check branch allowed for distribution" test_is_branch_allowed 0
test_run "Get large file threshold" test_get_large_file_threshold 0
test_run "Get sensitive patterns" test_get_sensitive_patterns 0
test_run "Get required files" test_get_required_files 0
test_run "Get distribution method" test_get_distribution_method 0
test_run "Check validation required after sync" test_is_validation_required_after_sync 0

# Print summary
test_framework_summary "Configuration Module"

if [[ $TEST_FRAMEWORK_FAIL -eq 0 ]]; then
    exit 0
else
    exit 1
fi