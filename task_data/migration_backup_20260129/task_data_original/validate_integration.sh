#!/bin/bash

# HANDOFF Integration Validation Script
# Checks if integration was done correctly across all 9 task files

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# Functions
print_header() {
  echo -e "${BLUE}================================${NC}"
  echo -e "${BLUE}$1${NC}"
  echo -e "${BLUE}================================${NC}"
}

check_pass() {
  echo -e "${GREEN}✓ PASS:${NC} $1"
  ((PASSED_CHECKS++))
  ((TOTAL_CHECKS++))
}

check_fail() {
  echo -e "${RED}✗ FAIL:${NC} $1"
  ((FAILED_CHECKS++))
  ((TOTAL_CHECKS++))
}

check_warn() {
  echo -e "${YELLOW}⚠ WARN:${NC} $1"
  ((TOTAL_CHECKS++))
}

# Main validation script
print_header "HANDOFF Integration Validation"

echo -e "\nValidating integration of HANDOFF files into task specifications...\n"

# Task IDs to check
TASKS=(75.1 75.2 75.3 75.4 75.5 75.6 75.7 75.8 75.9)

# 1. Check if all task files exist
print_header "Phase 1: File Existence Check"

for task in "${TASKS[@]}"; do
  if [ -f "task-${task}.md" ]; then
    check_pass "task-${task}.md exists"
  else
    check_fail "task-${task}.md MISSING"
  fi
done

# 2. Check line counts (should be 350-460 lines after integration)
print_header "Phase 2: Line Count Validation (Target: 350-460 lines)"

declare -A line_counts
for task in "${TASKS[@]}"; do
  if [ -f "task-${task}.md" ]; then
    count=$(wc -l < "task-${task}.md")
    line_counts[$task]=$count
    
    if [ "$count" -ge 350 ] && [ "$count" -le 500 ]; then
      check_pass "task-${task}.md has $count lines (acceptable)"
    elif [ "$count" -lt 350 ]; then
      check_warn "task-${task}.md has $count lines (may not be fully integrated)"
    else
      check_warn "task-${task}.md has $count lines (possibly too long)"
    fi
  fi
done

# 3. Check for required integrated sections
print_header "Phase 3: Integrated Section Validation"

for task in "${TASKS[@]}"; do
  if [ -f "task-${task}.md" ]; then
    # Check Developer Quick Reference
    if grep -q "## Developer Quick Reference" "task-${task}.md"; then
      check_pass "task-${task}.md has Developer Quick Reference"
    else
      check_fail "task-${task}.md MISSING Developer Quick Reference"
    fi
    
    # Check Implementation Checklist from HANDOFF
    if grep -q "### Implementation Checklist (From HANDOFF)" "task-${task}.md"; then
      # Count how many times it appears (should be multiple)
      count=$(grep -c "### Implementation Checklist (From HANDOFF)" "task-${task}.md")
      if [ "$count" -ge 5 ]; then
        check_pass "task-${task}.md has $count Implementation Checklists"
      else
        check_warn "task-${task}.md has only $count Implementation Checklists (expected 5+)"
      fi
    else
      check_fail "task-${task}.md MISSING Implementation Checklist (From HANDOFF)"
    fi
    
    # Check Test Case Examples
    if grep -q "### Test Case Examples (From HANDOFF)" "task-${task}.md"; then
      check_pass "task-${task}.md has Test Case Examples"
    else
      check_fail "task-${task}.md MISSING Test Case Examples (From HANDOFF)"
    fi
    
    # Check Technical Reference
    if grep -q "## Technical Reference" "task-${task}.md"; then
      check_pass "task-${task}.md has Technical Reference"
    else
      check_fail "task-${task}.md MISSING Technical Reference"
    fi
  fi
done

# 4. Check for "From HANDOFF" labels (should appear multiple times)
print_header "Phase 4: Attribution Labels Check"

for task in "${TASKS[@]}"; do
  if [ -f "task-${task}.md" ]; then
    count=$(grep -c "(From HANDOFF)" "task-${task}.md" || echo "0")
    if [ "$count" -ge 3 ]; then
      check_pass "task-${task}.md has $count '(From HANDOFF)' labels"
    else
      check_warn "task-${task}.md has only $count '(From HANDOFF)' labels (expected 3+)"
    fi
  fi
done

# 5. Check for markdown formatting issues
print_header "Phase 5: Markdown Formatting Check"

for task in "${TASKS[@]}"; do
  if [ -f "task-${task}.md" ]; then
    # Check for proper header formatting
    if grep -q "^## " "task-${task}.md"; then
      check_pass "task-${task}.md has proper section headers"
    else
      check_fail "task-${task}.md MISSING proper section headers"
    fi
    
    # Check for unclosed code blocks
    backtick_count=$(grep -c '```' "task-${task}.md" || echo "0")
    if [ $((backtick_count % 2)) -eq 0 ]; then
      check_pass "task-${task}.md has properly closed code blocks"
    else
      check_fail "task-${task}.md has UNCLOSED code blocks"
    fi
  fi
done

# 6. Check for critical content completeness
print_header "Phase 6: Content Completeness Check"

for task in "${TASKS[@]}"; do
  if [ -f "task-${task}.md" ]; then
    # Check for Purpose section
    if grep -q "^## Purpose" "task-${task}.md"; then
      check_pass "task-${task}.md has Purpose section"
    else
      check_fail "task-${task}.md MISSING Purpose section"
    fi
    
    # Check for Success Criteria
    if grep -q "^## Success Criteria" "task-${task}.md"; then
      check_pass "task-${task}.md has Success Criteria"
    else
      check_fail "task-${task}.md MISSING Success Criteria"
    fi
    
    # Check for Subtasks
    if grep -q "^## Subtasks" "task-${task}.md"; then
      check_pass "task-${task}.md has Subtasks section"
    else
      check_fail "task-${task}.md MISSING Subtasks section"
    fi
    
    # Check for Done Definition
    if grep -q "^## Done Definition" "task-${task}.md"; then
      check_pass "task-${task}.md has Done Definition"
    else
      check_fail "task-${task}.md MISSING Done Definition"
    fi
  fi
done

# 7. Summary Report
print_header "Validation Summary"

echo ""
echo "Total Checks: $TOTAL_CHECKS"
echo -e "Passed: ${GREEN}$PASSED_CHECKS${NC}"
echo -e "Failed: ${RED}$FAILED_CHECKS${NC}"
echo ""

# Calculate success rate
if [ "$TOTAL_CHECKS" -gt 0 ]; then
  success_rate=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
  echo "Success Rate: ${success_rate}%"
  echo ""
fi

# Overall result
if [ "$FAILED_CHECKS" -eq 0 ]; then
  echo -e "${GREEN}✓ All validations passed!${NC}"
  echo "Integration appears complete and correct."
  exit 0
else
  echo -e "${RED}✗ $FAILED_CHECKS validation(s) failed.${NC}"
  echo "Please review the failures above and correct them."
  exit 1
fi
