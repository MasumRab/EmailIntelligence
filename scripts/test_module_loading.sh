#!/bin/bash
# test_module_loading.sh - Test script to verify all modules load correctly

set -euo pipefail

echo "Testing module loading for orchestration distribution system..."

# Define paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_DIR="$SCRIPT_DIR/../modules"

echo "Module directory: $MODULE_DIR"

# Check if modules directory exists
if [[ ! -d "$MODULE_DIR" ]]; then
    echo "ERROR: Modules directory does not exist: $MODULE_DIR"
    exit 1
fi

# List of expected modules
EXPECTED_MODULES=("config.sh" "utils.sh" "branch.sh" "validate.sh" "distribute.sh" "logging.sh" "safety.sh")

# Check if each module exists
for module in "${EXPECTED_MODULES[@]}"; do
    module_path="$MODULE_DIR/$module"
    if [[ ! -f "$module_path" ]]; then
        echo "ERROR: Module file does not exist: $module_path"
        exit 1
    else
        echo "✓ Found module: $module"
    fi
done

# Try to source each module to test for syntax errors
echo ""
echo "Testing module syntax by sourcing..."

for module in "${EXPECTED_MODULES[@]}"; do
    module_path="$MODULE_DIR/$module"
    echo "Sourcing $module..."
    
    # Use bash to check syntax without executing
    if bash -n "$module_path"; then
        echo "✓ Syntax OK: $module"
    else
        echo "✗ Syntax ERROR: $module"
        exit 1
    fi
done

# Test the main script
MAIN_SCRIPT="$SCRIPT_DIR/distribute-orchestration-files.sh"
if [[ -f "$MAIN_SCRIPT" ]]; then
    echo ""
    echo "Testing main script syntax..."
    if bash -n "$MAIN_SCRIPT"; then
        echo "✓ Main script syntax OK"
    else
        echo "✗ Main script syntax ERROR"
        exit 1
    fi
else
    echo "ERROR: Main script does not exist: $MAIN_SCRIPT"
    exit 1
fi

# Test if main script can source all modules without errors
echo ""
echo "Testing if main script can source all modules..."
if bash -c "source '$MAIN_SCRIPT'" 2>/dev/null; then
    echo "✓ Main script can source all modules successfully"
else
    echo "✗ Error sourcing modules from main script"
    # Run with more verbose output to see the error
    bash -c "set -x; source '$MAIN_SCRIPT'" 2>&1
    exit 1
fi

echo ""
echo "🎉 All modules loaded successfully!"
echo "The orchestration distribution system is ready for use."
echo ""
echo "To run the distribution system, use:"
echo "  ./scripts/distribute-orchestration-files.sh --help"