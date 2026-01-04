#!/bin/bash
# Code formatting script for Task Master project
# This script applies Black and Ruff formatting to all Python files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Task Master Code Formatting Script${NC}"
echo "=================================="
echo ""

# Check if Black is installed
if ! python3 -m black --version &> /dev/null; then
    echo -e "${RED}Error: Black is not installed${NC}"
    echo "Install with: pip install black"
    exit 1
fi

# Check if Ruff is installed
if ! python3 -m ruff --version &> /dev/null; then
    echo -e "${RED}Error: Ruff is not installed${NC}"
    echo "Install with: pip install ruff"
    exit 1
fi

# Parse command line arguments
CHECK_ONLY=false
FIX_RUFF=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --check)
            CHECK_ONLY=true
            shift
            ;;
        --no-fix-ruff)
            FIX_RUFF=false
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --check       Check formatting without making changes"
            echo "  --no-fix-ruff  Skip Ruff auto-fix (check only)"
            echo "  -h, --help    Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Directories to format
DIRECTORIES="task_scripts/ scripts/ task_data/branch_clustering_implementation.py"

if [ "$CHECK_ONLY" = true ]; then
    echo -e "${YELLOW}Checking Black formatting...${NC}"
    if python3 -m black --check $DIRECTORIES; then
        echo -e "${GREEN}✓ Black formatting is correct${NC}"
    else
        echo -e "${RED}✗ Black formatting issues found${NC}"
        echo "Run without --check to fix"
        exit 1
    fi

    echo ""
    echo -e "${YELLOW}Checking Ruff linting...${NC}"
    if python3 -m ruff check $DIRECTORIES; then
        echo -e "${GREEN}✓ Ruff linting passed${NC}"
    else
        echo -e "${RED}✗ Ruff linting issues found${NC}"
        echo "Run without --check to fix"
        exit 1
    fi
else
    echo -e "${YELLOW}Applying Black formatting...${NC}"
    python3 -m black $DIRECTORIES
    echo -e "${GREEN}✓ Black formatting applied${NC}"

    echo ""
    echo -e "${YELLOW}Applying Ruff formatting...${NC}"
    python3 -m ruff format $DIRECTORIES
    echo -e "${GREEN}✓ Ruff formatting applied${NC}"

    if [ "$FIX_RUFF" = true ]; then
        echo ""
        echo -e "${YELLOW}Fixing Ruff linting issues...${NC}"
        python3 -m ruff check --fix --unsafe-fixes $DIRECTORIES
        echo -e "${GREEN}✓ Ruff linting issues fixed${NC}"
    else
        echo ""
        echo -e "${YELLOW}Checking Ruff linting...${NC}"
        python3 -m ruff check $DIRECTORIES
    fi
fi

echo ""
echo -e "${GREEN}✨ Code formatting complete! ✨${NC}"
echo ""
echo "Next steps:"
echo "  1. Review the changes with: git diff"
echo "  2. Commit the formatted code"
echo "  3. Consider installing pre-commit hooks: pre-commit install"