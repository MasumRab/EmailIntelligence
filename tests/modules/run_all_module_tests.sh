#!/bin/bash
# run_all_module_tests.sh - Main test runner for all orchestration distribution modules

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Running Comprehensive Module Test Suite${NC}"
echo "========================================"

# Define test directory
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../.." && pwd)"

# Counter for test results
TOTAL_TESTS=0
TOTAL_PASSES=0
TOTAL_FAILS=0

# Function to run a single test file
run_test_file() {
    local test_file="$1"
    local test_name="$2"
    
    echo ""
    echo -e "${BLUE}🧪 Running $test_name tests...${NC}"
    echo "----------------------------------------"
    
    if [[ -f "$test_file" ]]; then
        if chmod +x "$test_file" 2>/dev/null; then
            if "$test_file"; then
                echo -e "${GREEN}✅ $test_name tests PASSED${NC}"
                # Extract results from the test output
                local test_count=$(grep -c "Total tests:" "$test_file" 2>/dev/null || echo 0)
                if [[ $test_count -gt 0 ]]; then
                    local passes=$(grep "Passed:" "$test_file" 2>/dev/null | tail -1 | awk '{print $2}')
                    local fails=$(grep "Failed:" "$test_file" 2>/dev/null | tail -1 | awk '{print $2}')
                    TOTAL_PASSES=$((TOTAL_PASSES + ${passes:-0}))
                    TOTAL_FAILS=$((TOTAL_FAILS + ${fails:-0}))
                    TOTAL_TESTS=$((TOTAL_TESTS + (${passes:-0} + ${fails:-0})))
                else
                    # If we can't extract from output, assume all passed
                    TOTAL_PASSES=$((TOTAL_PASSES + 1))
                    TOTAL_TESTS=$((TOTAL_TESTS + 1))
                fi
            else
                echo -e "${RED}❌ $test_name tests FAILED${NC}"
                TOTAL_FAILS=$((TOTAL_FAILS + 1))
                TOTAL_TESTS=$((TOTAL_TESTS + 1))
            fi
        else
            echo -e "${RED}❌ Cannot make $test_file executable${NC}"
            TOTAL_FAILS=$((TOTAL_FAILS + 1))
            TOTAL_TESTS=$((TOTAL_TESTS + 1))
        fi
    else
        echo -e "${RED}❌ Test file $test_file does not exist${NC}"
        TOTAL_FAILS=$((TOTAL_FAILS + 1))
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
    fi
}

# Run all module tests
run_test_file "$TEST_DIR/test_config_module.sh" "Configuration"
run_test_file "$TEST_DIR/test_validate_module.sh" "Validation"
run_test_file "$TEST_DIR/test_distribute_module.sh" "Distribution"
run_test_file "$TEST_DIR/test_safety_module.sh" "Safety"
run_test_file "$TEST_DIR/test_other_modules.sh" "Other (Utils/Branch/Logging)"

# Calculate totals from actual test results
# We need to run the tests again to get accurate counts
echo ""
echo -e "${BLUE}📊 Calculating Final Results...${NC}"

# Actually run tests and count results properly
CONFIG_RESULTS=$(bash "$TEST_DIR/test_config_module.sh" 2>/dev/null | grep -E "Total tests:|Passed:|Failed:" | tail -3)
VALIDATE_RESULTS=$(bash "$TEST_DIR/test_validate_module.sh" 2>/dev/null | grep -E "Total tests:|Passed:|Failed:" | tail -3)
DISTRIBUTE_RESULTS=$(bash "$TEST_DIR/test_distribute_module.sh" 2>/dev/null | grep -E "Total tests:|Passed:|Failed:" | tail -3)
SAFETY_RESULTS=$(bash "$TEST_DIR/test_safety_module.sh" 2>/dev/null | grep -E "Total tests:|Passed:|Failed:" | tail -3)
OTHER_RESULTS=$(bash "$TEST_DIR/test_other_modules.sh" 2>/dev/null | grep -E "Total tests:|Passed:|Failed:" | tail -3)

# Extract actual numbers
CONFIG_TOTAL=$(echo "$CONFIG_RESULTS" | grep "Total tests:" | awk '{print $3}')
CONFIG_PASS=$(echo "$CONFIG_RESULTS" | grep "Passed:" | awk '{print $2}')
CONFIG_FAIL=$(echo "$CONFIG_RESULTS" | grep "Failed:" | awk '{print $2}')

VALIDATE_TOTAL=$(echo "$VALIDATE_RESULTS" | grep "Total tests:" | awk '{print $3}')
VALIDATE_PASS=$(echo "$VALIDATE_RESULTS" | grep "Passed:" | awk '{print $2}')
VALIDATE_FAIL=$(echo "$VALIDATE_RESULTS" | grep "Failed:" | awk '{print $2}')

DISTRIBUTE_TOTAL=$(echo "$DISTRIBUTE_RESULTS" | grep "Total tests:" | awk '{print $3}')
DISTRIBUTE_PASS=$(echo "$DISTRIBUTE_RESULTS" | grep "Passed:" | awk '{print $2}')
DISTRIBUTE_FAIL=$(echo "$DISTRIBUTE_RESULTS" | grep "Failed:" | awk '{print $2}')

SAFETY_TOTAL=$(echo "$SAFETY_RESULTS" | grep "Total tests:" | awk '{print $3}')
SAFETY_PASS=$(echo "$SAFETY_RESULTS" | grep "Passed:" | awk '{print $2}')
SAFETY_FAIL=$(echo "$SAFETY_RESULTS" | grep "Failed:" | awk '{print $2}')

OTHER_TOTAL=$(echo "$OTHER_RESULTS" | grep "Total tests:" | awk '{print $3}')
OTHER_PASS=$(echo "$OTHER_RESULTS" | grep "Passed:" | awk '{print $2}')
OTHER_FAIL=$(echo "$OTHER_RESULTS" | grep "Failed:" | awk '{print $2}')

# Calculate totals
TOTAL_TESTS=$((CONFIG_TOTAL + VALIDATE_TOTAL + DISTRIBUTE_TOTAL + SAFETY_TOTAL + OTHER_TOTAL))
TOTAL_PASSES=$((CONFIG_PASS + VALIDATE_PASS + DISTRIBUTE_PASS + SAFETY_PASS + OTHER_PASS))
TOTAL_FAILS=$((CONFIG_FAIL + VALIDATE_FAIL + DISTRIBUTE_FAIL + SAFETY_FAIL + OTHER_FAIL))

# Print final summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🏆 FINAL TEST RESULTS${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Total Tests Run: ${TOTAL_TESTS}"
echo -e "✅ Passed: ${GREEN}${TOTAL_PASSES}${NC}"
echo -e "❌ Failed: ${RED}${TOTAL_FAILS}${NC}"
echo ""

if [[ $TOTAL_FAILS -eq 0 ]]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! The orchestration distribution system is working correctly.${NC}"
    echo ""
    echo "📋 Module Coverage:"
    echo "   • Configuration module: $CONFIG_PASS/$CONFIG_TOTAL tests passed"
    echo "   • Validation module: $VALIDATE_PASS/$VALIDATE_TOTAL tests passed"
    echo "   • Distribution module: $DISTRIBUTE_PASS/$DISTRIBUTE_TOTAL tests passed"
    echo "   • Safety module: $SAFETY_PASS/$SAFETY_TOTAL tests passed"
    echo "   • Other modules: $OTHER_PASS/$OTHER_TOTAL tests passed"
    echo ""
    echo -e "${GREEN}✨ The modular orchestration distribution system is ready for production!${NC}"
    exit 0
else
    echo -e "${RED}💥 SOME TESTS FAILED! Please review the failing tests above.${NC}"
    echo ""
    echo "📋 Failure Breakdown:"
    echo "   • Configuration module: $CONFIG_FAIL failures"
    echo "   • Validation module: $VALIDATE_FAIL failures"
    echo "   • Distribution module: $DISTRIBUTE_FAIL failures"
    echo "   • Safety module: $SAFETY_FAIL failures"
    echo "   • Other modules: $OTHER_FAIL failures"
    echo ""
    echo -e "${YELLOW}⚠️  Please fix the failing tests before deploying.${NC}"
    exit 1
fi