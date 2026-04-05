#!/bin/bash

##
# Markdown Link Standardization Script
#
# Purpose: Standardize relative links in markdown files to use ./ prefix
# Date: December 11, 2025
# Requirements: bash, sed, find
#
# Usage:
#   bash scripts/markdown/standardize-links.sh [options] [files...]
#
# Options:
#   --check          Show changes without applying them
#   --fix            Apply changes (default)
#   --all            Process all .md files in project
#   --dry-run        Show what would be changed
#   --help           Show this help message
#
# Examples:
#   # Standardize specific file
#   bash scripts/markdown/standardize-links.sh DOCUMENTATION_INDEX.md
#   
#   # Check all markdown files
#   bash scripts/markdown/standardize-links.sh --check --all
#   
#   # Apply fixes to all files
#   bash scripts/markdown/standardize-links.sh --fix --all
##

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Settings
CHECK_ONLY=false
DRY_RUN=false
PROCESS_ALL=false
FILES=()
CHANGES_MADE=0

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --check)
      CHECK_ONLY=true
      shift
      ;;
    --fix)
      CHECK_ONLY=false
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --all)
      PROCESS_ALL=true
      shift
      ;;
    --help)
      head -32 "$0" | tail -30
      exit 0
      ;;
    *)
      FILES+=("$1")
      shift
      ;;
  esac
done

# Get files to process
get_files() {
  if [ "$PROCESS_ALL" = true ]; then
    find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" -not -path "./venv/*"
  else
    if [ ${#FILES[@]} -eq 0 ]; then
      ls -1 *.md 2>/dev/null || echo ""
    else
      printf '%s\n' "${FILES[@]}"
    fi
  fi
}

# Standardize links in a file
process_file() {
  local file="$1"
  
  if [ ! -f "$file" ]; then
    echo -e "${RED}Error: File not found: $file${NC}"
    return 1
  fi
  
  echo -e "${BLUE}Processing: $file${NC}"
  
  # Create backup
  local backup="${file}.backup"
  cp "$file" "$backup"
  
  # Pattern 1: Convert [text](FILE.md) → [text](./FILE.md) when FILE is at root
  # Only if it doesn't already have ./ or ../
  sed -i.tmp 's/\(\[[^]]*\]\)(\([A-Z][A-Za-z_]*\.md\))/\1(.\/.\/\2)/g' "$file" || true
  
  # Pattern 2: Fix docs/ paths: [text](docs/FILE.md) → [text](./docs/FILE.md)
  sed -i.tmp 's/\(\[[^]]*\]\)(docs\//\1(\.\/docs\//g' "$file" || true
  
  # Pattern 3: Update broken paths like docs/core/* → docs/*
  sed -i.tmp 's/\.\/docs\/core\//\.\/docs\//g' "$file" || true
  sed -i.tmp 's/docs\/core\//\.\/docs\//g' "$file" || true
  
  # Pattern 4: Update docs/guides/* correctly
  sed -i.tmp 's/\.\/docs\/guides\/branch_switching\.md/\.\/docs\/guides\/branch_switching_guide\.md/g' "$file" || true
  sed -i.tmp 's/docs\/guides\/branch_switching\.md/\.\/docs\/guides\/branch_switching_guide\.md/g' "$file" || true
  
  # Pattern 5: Fix workflow doc reference
  sed -i.tmp 's/docs\/guides\/workflow_and_review_process\.md/\.\/docs\/git_workflow_plan\.md/g' "$file" || true
  
  # Pattern 6: Remove double ./ if created
  sed -i.tmp 's/\.\/(\.\/\(.*\))/\1/g' "$file" || true
  
  # Clean up temp files
  rm -f "${file}.tmp"
  
  # Check if changes were made
  if ! diff -q "$file" "$backup" > /dev/null 2>&1; then
    CHANGES_MADE=$((CHANGES_MADE + 1))
    
    if [ "$DRY_RUN" = true ]; then
      echo -e "${YELLOW}  Changes to be applied:${NC}"
      diff -u "$backup" "$file" || true
    elif [ "$CHECK_ONLY" = false ]; then
      echo -e "${GREEN}  ✓ Updated${NC}"
    fi
  else
    echo -e "${YELLOW}  No changes needed${NC}"
  fi
  
  # Keep backup if check_only or dry_run
  if [ "$CHECK_ONLY" = true ] || [ "$DRY_RUN" = true ]; then
    mv "$backup" "$file"
  else
    rm -f "$backup"
  fi
}

# Validate links exist
validate_links() {
  local file="$1"
  
  echo -e "${BLUE}Validating links in: $file${NC}"
  
  # Extract all markdown links
  grep -oP '\]\(\K[^)]+' "$file" | while read -r link; do
    # Skip external URLs and anchors-only
    if [[ "$link" =~ ^https?:// ]] || [[ "$link" =~ ^# ]]; then
      continue
    fi
    
    # Extract file path (remove anchor)
    local file_path="${link%#*}"
    
    # Skip if empty
    [ -z "$file_path" ] && continue
    
    # Check if file exists
    if [ ! -f "$file_path" ]; then
      echo -e "${YELLOW}  Warning: Link target not found: $link${NC}"
    fi
  done
}

# Main
main() {
  echo -e "${YELLOW}Markdown Link Standardization${NC}"
  echo "=============================="
  echo ""
  
  if [ "$CHECK_ONLY" = true ]; then
    echo -e "${YELLOW}Mode: Check Only (no changes)${NC}"
  elif [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}Mode: Dry Run (show changes)${NC}"
  else
    echo -e "${YELLOW}Mode: Fix (apply changes)${NC}"
  fi
  echo ""
  
  # Get files
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
  
  echo -e "${YELLOW}Found ${#FILES_ARRAY[@]} file(s)${NC}"
  echo ""
  
  # Process files
  for file in "${FILES_ARRAY[@]}"; do
    process_file "$file"
    echo ""
  done
  
  echo "=============================="
  echo -e "${YELLOW}Summary:${NC}"
  echo "Files processed: ${#FILES_ARRAY[@]}"
  echo "Files changed: $CHANGES_MADE"
  echo ""
  
  if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}This was a dry run. Use --fix to apply changes.${NC}"
  elif [ "$CHECK_ONLY" = true ]; then
    echo -e "${YELLOW}Check mode completed.${NC}"
  else
    echo -e "${GREEN}Link standardization completed${NC}"
  fi
}

main "$@"
