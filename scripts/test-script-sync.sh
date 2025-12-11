#!/bin/bash

##
# Test Script Synchronization
#
# Purpose: Verify that critical scripts are synced across all branches
# Date: December 11, 2025
# Requirements: bash 4.0+, git 2.20+
#
# Usage:
#   bash scripts/test-script-sync.sh [options]
#
# Options:
#   --check-all   Check all critical files
#   --fix         Attempt to fix sync issues (manual merge)
#   --report      Generate detailed report
#   --help        Show this help message
#
# Exit Codes:
#   0 = All scripts synced correctly
#   1 = Sync issues detected
#   2 = Git command failed
##

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Settings
CHECK_ALL=false
FIX_MODE=false
REPORT_MODE=false
FAILED_CHECKS=0
PASSED_CHECKS=0
REPORT_FILE="/tmp/script-sync-report.txt"

# Critical files that must be on all branches
CRITICAL_FILES=(
  "scripts/install-hooks.sh"
  "scripts/hooks/post-checkout"
  "scripts/hooks/post-commit"
  "scripts/hooks/post-merge"
  "scripts/hooks/pre-commit"
  "scripts/hooks/post-push"
  "scripts/lib/common.sh"
  "scripts/markdown/lint-and-format.sh"
  "scripts/markdown/standardize-links.sh"
  "scripts/markdown/README.md"
)

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --check-all)
      CHECK_ALL=true
      shift
      ;;
    --fix)
      FIX_MODE=true
      shift
      ;;
    --report)
      REPORT_MODE=true
      shift
      ;;
    --help)
      head -30 "$0" | tail -28
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Print header
echo -e "${BLUE}Script Synchronization Test${NC}"
echo "============================"
echo "Date: $(date)"
echo ""

# Initialize report
if [ "$REPORT_MODE" = true ]; then
  {
    echo "# Script Synchronization Report"
    echo "Date: $(date)"
    echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
    echo ""
  } > "$REPORT_FILE"
fi

# Test a single file on all branches
test_file_sync() {
  local file="$1"
  local all_present=true
  
  echo -e "${YELLOW}Testing: $file${NC}"
  
  for branch in orchestration-tools scientific main; do
    if git show $branch:$file > /dev/null 2>&1; then
      echo -e "  ${GREEN}✓${NC} $branch"
      if [ "$REPORT_MODE" = true ]; then
        echo "✓ $file on $branch" >> "$REPORT_FILE"
      fi
    else
      echo -e "  ${RED}✗${NC} $branch (MISSING)"
      echo -e "  ${RED}✗${NC} $branch (MISSING)" >> "$REPORT_FILE"
      all_present=false
      FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
  done
  
  if [ "$all_present" = true ]; then
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
  fi
  
  echo ""
}

# Test all critical files
test_critical_files() {
  echo -e "${BLUE}Critical Files Check${NC}"
  echo "====================="
  echo ""
  
  local failed=0
  for file in "${CRITICAL_FILES[@]}"; do
    test_file_sync "$file"
    if [ "$FAILED_CHECKS" -gt 0 ]; then
      failed=$((failed + 1))
    fi
  done
  
  return $failed
}

# Count files on branch
count_scripts_on_branch() {
  local branch="$1"
  git ls-tree -r --name-only $branch scripts/ 2>/dev/null | wc -l || echo "0"
}

# Compare branches
compare_branches() {
  echo -e "${BLUE}Branch Comparison${NC}"
  echo "================="
  echo ""
  
  echo "Script counts:"
  for branch in orchestration-tools scientific main; do
    count=$(count_scripts_on_branch $branch)
    echo -e "  $branch: ${YELLOW}$count${NC} files"
  done
  
  echo ""
  echo "Differences (orchestration-tools vs other branches):"
  
  echo ""
  echo "  vs scientific:"
  diff <(git ls-tree -r --name-only orchestration-tools scripts/ 2>/dev/null | sort) \
       <(git ls-tree -r --name-only scientific scripts/ 2>/dev/null | sort) \
       | head -10 || true
  
  echo ""
  echo "  vs main:"
  diff <(git ls-tree -r --name-only orchestration-tools scripts/ 2>/dev/null | sort) \
       <(git ls-tree -r --name-only main scripts/ 2>/dev/null | sort) \
       | head -10 || true
  
  echo ""
}

# Attempt fix (manual merge)
attempt_fix() {
  echo -e "${YELLOW}Attempting to fix sync issues...${NC}"
  echo ""
  
  current_branch=$(git rev-parse --abbrev-ref HEAD)
  
  echo "Current branch: $current_branch"
  echo ""
  
  # Only allow fix on branches other than orchestration-tools
  if [ "$current_branch" = "orchestration-tools" ]; then
    echo -e "${RED}Cannot fix from orchestration-tools branch.${NC}"
    echo "Make changes on orchestration-tools, then:"
    echo "  git checkout scientific && git merge orchestration-tools"
    echo "  git checkout main && git merge orchestration-tools"
    return 1
  fi
  
  echo -e "${YELLOW}To sync $current_branch with orchestration-tools:${NC}"
  echo ""
  echo "  git merge orchestration-tools"
  echo ""
  echo -e "${YELLOW}Or to sync all branches:${NC}"
  echo ""
  echo "  git checkout scientific && git merge orchestration-tools"
  echo "  git checkout main && git merge orchestration-tools"
  echo "  git push origin scientific main"
  echo ""
}

# Show summary
show_summary() {
  echo -e "${BLUE}Test Summary${NC}"
  echo "============"
  echo ""
  
  total=$((PASSED_CHECKS + FAILED_CHECKS))
  
  if [ $total -eq 0 ]; then
    echo -e "${YELLOW}No files tested.${NC}"
    return 0
  fi
  
  echo "Passed: ${GREEN}$PASSED_CHECKS${NC}"
  echo "Failed: ${RED}$FAILED_CHECKS${NC}"
  echo "Total:  $total"
  echo ""
  
  if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}✓ All critical files are synced!${NC}"
    return 0
  else
    echo -e "${RED}✗ Sync issues detected!${NC}"
    
    if [ "$REPORT_MODE" = true ]; then
      echo ""
      echo "Report saved to: $REPORT_FILE"
      echo "View with: cat $REPORT_FILE"
    fi
    
    if [ "$FIX_MODE" = false ]; then
      echo ""
      echo -e "${YELLOW}Use --fix flag to attempt auto-fix${NC}"
    fi
    
    return 1
  fi
}

# Main execution
main() {
  # Verify git repo
  if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 2
  fi
  
  # Run tests
  if test_critical_files; then
    CRITICAL_OK=true
  else
    CRITICAL_OK=false
  fi
  
  echo ""
  
  if [ "$CHECK_ALL" = true ]; then
    compare_branches
  fi
  
  echo ""
  
  if [ "$FIX_MODE" = true ]; then
    attempt_fix
  fi
  
  # Summary
  if show_summary; then
    exit 0
  else
    exit 1
  fi
}

main "$@"
