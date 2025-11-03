#!/bin/bash
# Script to organize documentation files based on branch

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get current branch
branch=$(git rev-parse --abbrev-ref HEAD)

echo -e "${BLUE}Organizing docs for branch: $branch${NC}"

# Function to categorize file
categorize_file() {
    local file="$1"
    local content=$(head -20 "$file" 2>/dev/null | tr '[:upper:]' '[:lower:]')
    
    # Check for branch-specific keywords
    if [[ "$branch" == "main" ]] && echo "$content" | grep -q "main\|production\|stable"; then
        echo "main"
    elif [[ "$branch" == "scientific" ]] && echo "$content" | grep -q "scientific\|ai\|ml\|research"; then
        echo "scientific"
    else
        echo "common"
    fi
}

# Find docs files outside docs/
find . -name "*.md" -o -name "*.txt" -o -name "*.rst" | grep -v "^./docs/" | while read -r file; do
    if [[ "$file" == "./.branch_docs/"* ]]; then
        continue  # Skip .branch_docs
    fi
    
    category=$(categorize_file "$file")
    target_dir="docs/$category"
    target_file="$target_dir/$(basename "$file")"
    
    # Create dir if needed
    mkdir -p "$target_dir"
    
    # Move file
    if [[ ! -f "$target_file" ]]; then
        mv "$file" "$target_file"
        echo -e "${GREEN}Moved $file to $target_file${NC}"
    else
        echo -e "${YELLOW}Skipping $file (target exists)${NC}"
    fi
done

echo -e "${GREEN}Docs organization complete for $branch${NC}"
