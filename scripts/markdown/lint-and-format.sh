#!/bin/bash

##
# Markdown Linting and Formatting Script
# 
# Purpose: Lint and format markdown files using markdownlint-cli and prettier
# Date: December 11, 2025
# Requirements: npm, prettier, markdownlint-cli
#
# Usage:
#   bash scripts/markdown/lint-and-format.sh [options] [files...]
#   
# Options:
#   --check          Check only (no modifications)
#   --fix            Apply fixes automatically
#   --all            Process all .md files in project
#   --help           Show this help message
#
# Examples:
#   # Lint specific files
#   bash scripts/markdown/lint-and-format.sh DOCUMENTATION_INDEX.md
#   
#   # Fix all markdown files
#   bash scripts/markdown/lint-and-format.sh --fix --all
#   
#   # Check without modifying
#   bash scripts/markdown/lint-and-format.sh --check --all
##

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default settings
CHECK_ONLY=false
FIX_FILES=false
PROCESS_ALL=false
FILES=()

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --check)
      CHECK_ONLY=true
      shift
      ;;
    --fix)
      FIX_FILES=true
      shift
      ;;
    --all)
      PROCESS_ALL=true
      shift
      ;;
    --help)
      head -30 "$0" | tail -26
      exit 0
      ;;
    *)
      FILES+=("$1")
      shift
      ;;
  esac
done

# Verify dependencies
check_dependencies() {
  if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm is not installed${NC}"
    exit 1
  fi
  
  if ! npm list prettier markdownlint-cli 2>/dev/null | grep -q prettier; then
    echo -e "${YELLOW}Installing prettier and markdownlint-cli...${NC}"
    npm install --save-dev prettier markdownlint-cli
  fi
}

# Get file list
get_files() {
  if [ "$PROCESS_ALL" = true ]; then
    find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" -not -path "./venv/*"
  elif [ ${#FILES[@]} -eq 0 ]; then
    # Default: lint root-level markdown files
    ls -1 *.md 2>/dev/null || echo "No markdown files found in current directory"
  else
    printf '%s\n' "${FILES[@]}"
  fi
}

# Run markdownlint
run_markdownlint() {
  local files=("$@")
  
  echo -e "${YELLOW}Running markdownlint...${NC}"
  
  if npx markdownlint "${files[@]}"; then
    echo -e "${GREEN}✓ Markdownlint passed${NC}"
    return 0
  else
    echo -e "${RED}✗ Markdownlint found issues${NC}"
    return 1
  fi
}

# Run prettier
run_prettier() {
  local files=("$@")
  
  echo -e "${YELLOW}Running prettier...${NC}"
  
  if [ "$CHECK_ONLY" = true ]; then
    if npx prettier --check "${files[@]}"; then
      echo -e "${GREEN}✓ Prettier check passed${NC}"
      return 0
    else
      echo -e "${RED}✗ Prettier found formatting issues${NC}"
      return 1
    fi
  else
    if npx prettier --write "${files[@]}"; then
      echo -e "${GREEN}✓ Prettier formatting applied${NC}"
      return 0
    else
      echo -e "${RED}✗ Prettier failed${NC}"
      return 1
    fi
  fi
}

# Main execution
main() {
  echo -e "${YELLOW}Markdown Linting and Formatting${NC}"
  echo "================================"
  
  check_dependencies
  
  # Get files to process
  FILES_ARRAY=()
  while IFS= read -r file; do
    if [ -n "$file" ]; then
      FILES_ARRAY+=("$file")
    fi
  done < <(get_files)
  
  if [ ${#FILES_ARRAY[@]} -eq 0 ]; then
    echo -e "${YELLOW}No markdown files found${NC}"
    exit 0
  fi
  
  echo -e "${YELLOW}Processing ${#FILES_ARRAY[@]} file(s)${NC}"
  echo ""
  
  # Run linting and formatting
  MARKDOWNLINT_RESULT=0
  PRETTIER_RESULT=0
  
  run_markdownlint "${FILES_ARRAY[@]}" || MARKDOWNLINT_RESULT=$?
  echo ""
  run_prettier "${FILES_ARRAY[@]}" || PRETTIER_RESULT=$?
  
  echo ""
  echo "================================"
  
  if [ $MARKDOWNLINT_RESULT -eq 0 ] && [ $PRETTIER_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed${NC}"
    exit 0
  else
    echo -e "${RED}✗ Some checks failed${NC}"
    exit 1
  fi
}

main "$@"
