#!/bin/bash
# Script to temporarily access orchestration-tools branch for setup operations
# Creates temporary worktree, runs command, then cleans up
# Usage: ./setup-orchestration-worktree.sh [command]

set -e

ORCHESTRATION_DIR="/tmp/orchestration-tools-$$"
COMMAND="${1:-help}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

cleanup() {
    if [[ -d "$ORCHESTRATION_DIR" ]]; then
        cd /tmp 2>/dev/null || true
        rm -rf "$ORCHESTRATION_DIR" 2>/dev/null || true
    fi
}

trap cleanup EXIT

show_help() {
    echo "Temporary Orchestration Access Script"
    echo ""
    echo "Creates temporary worktree from orchestration-tools branch,"
    echo "runs the specified command, then cleans up automatically."
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  setup         - Run environment setup"
    echo "  sync          - Run worktree synchronization"
    echo "  test          - Run tests"
    echo "  access        - Access orchestration files directly"
    echo "  help          - Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 setup    # Run setup in temporary orchestration environment"
    echo "  $0 sync     # Run sync from orchestration-tools"
    echo "  $0 access   # Get shell access to orchestration files"
}

if [[ "$COMMAND" == "help" ]]; then
    show_help
    exit 0
fi

echo -e "${BLUE}Setting up temporary orchestration access...${NC}"

# Create temporary directory
mkdir -p "$ORCHESTRATION_DIR"

# Create worktree from orchestration-tools branch
if ! git worktree add "$ORCHESTRATION_DIR" origin/orchestration-tools 2>/dev/null; then
    echo -e "${RED}Failed to create orchestration worktree${NC}"
    echo "Make sure you're in the main repository and orchestration-tools branch exists"
    exit 1
fi

cd "$ORCHESTRATION_DIR"

echo -e "${GREEN}✓ Orchestration environment ready${NC}"

case "$COMMAND" in
    "setup")
        echo -e "${BLUE}Running setup...${NC}"
        python setup/launch.py --setup
        ;;
    "sync")
        echo -e "${BLUE}Running synchronization...${NC}"
        bash scripts/sync_setup_worktrees.sh
        ;;
    "test")
        echo -e "${BLUE}Running tests...${NC}"
        python setup/launch.py test
        ;;
    "access")
        echo -e "${BLUE}Orchestration files accessible at: $ORCHESTRATION_DIR${NC}"
        echo -e "${YELLOW}Type 'exit' to cleanup and return${NC}"
        echo ""
        echo "Available in this environment:"
        echo "  setup/           - Launch and setup files"
        echo "  configs/         - Branch-specific configurations"
        echo "  scripts/         - Orchestration scripts"
        echo ""
        bash
        ;;
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo -e "${GREEN}✓ Command completed${NC}"
