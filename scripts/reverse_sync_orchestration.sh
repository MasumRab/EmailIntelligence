#!/bin/bash
# Reverse sync script: Pull approved changes from feature branches into orchestration-tools
# Usage: ./reverse_sync_orchestration.sh <source_branch> <commit_sha>
#
# This script is for controlled reverse synchronization of orchestration-managed files.
# It should only be run after review and approval.

set -e

if [[ $# -lt 2 ]]; then
    echo "Usage: $0 <source_branch> <commit_sha> [--dry-run]"
    echo ""
    echo "Pull approved changes from feature branch into orchestration-tools"
    echo ""
    echo "Arguments:"
    echo "  source_branch  Branch containing the approved changes"
    echo "  commit_sha     Specific commit SHA to cherry-pick"
    echo "  --dry-run      Show what would be done without making changes"
    echo ""
    echo "Example:"
    echo "  $0 feature/fix-launch-bug abc123"
    exit 1
fi

SOURCE_BRANCH="$1"
COMMIT_SHA="$2"
DRY_RUN=false

if [[ "$3" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Validate inputs
if ! git show-ref --verify --quiet "refs/heads/$SOURCE_BRANCH"; then
    echo -e "${RED}Error: Source branch '$SOURCE_BRANCH' does not exist${NC}"
    exit 1
fi

if ! git cat-file -e "$COMMIT_SHA" 2>/dev/null; then
    echo -e "${RED}Error: Commit '$COMMIT_SHA' does not exist${NC}"
    exit 1
fi

# Check if we're on orchestration-tools
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$CURRENT_BRANCH" != "orchestration-tools" ]]; then
    echo -e "${RED}Error: Must be on orchestration-tools branch to run reverse sync${NC}"
    echo -e "${YELLOW}Run: git checkout orchestration-tools${NC}"
    exit 1
fi

echo -e "${BLUE}Reverse Sync: $SOURCE_BRANCH ($COMMIT_SHA) → orchestration-tools${NC}"
echo ""

# Show commit details
echo -e "${YELLOW}Commit details:${NC}"
git show --no-patch --format="Author: %an <%ae>%nDate: %ad%nSubject: %s%n" "$COMMIT_SHA"
echo ""

# Check what files are changed in this commit
echo -e "${YELLOW}Files changed in commit:${NC}"
git show --name-only --format="" "$COMMIT_SHA"
echo ""

# Define managed files
MANAGED_FILES=(
    "setup/launch.py"
    "setup/launch.bat"
    "setup/launch.sh"
    "setup/pyproject.toml"
    "setup/requirements.txt"
    "setup/requirements-dev.txt"
    "setup/requirements-cpu.txt"
    "setup/setup_environment_system.sh"
    "setup/setup_environment_wsl.sh"
    "setup/project_config.py"
    "setup/environment.py"
    "setup/services.py"
    "setup/test_config.py"
    "setup/test_stages.py"
        "setup/utils.py"
        "setup/validation.py"
        "setup/README.md"
        "scripts/sync_setup_worktrees.sh"
        "scripts/reverse_sync_orchestration.sh"
        "scripts/cleanup_orchestration.sh"
        ".flake8"
        ".pylintrc"
        ".gitignore"
        ".gitattributes"
    )

# Check if commit contains managed files
COMMIT_FILES=$(git show --name-only --format="" "$COMMIT_SHA")
ORCHESTRATION_CHANGES=false

for file in "${MANAGED_FILES[@]}"; do
    if echo "$COMMIT_FILES" | grep -q "^${file}$"; then
        echo -e "${GREEN}✓ Contains orchestration-managed file: $file${NC}"
        ORCHESTRATION_CHANGES=true
    fi
done

if [[ "$ORCHESTRATION_CHANGES" == false ]]; then
    echo -e "${YELLOW}Warning: Commit does not contain any orchestration-managed files${NC}"
    echo "This reverse sync may not be necessary."
    echo ""
fi

# Show diff
echo -e "${YELLOW}Changes in commit:${NC}"
git show --stat "$COMMIT_SHA"
echo ""

if [[ "$DRY_RUN" == true ]]; then
    echo -e "${BLUE}DRY RUN - Would execute:${NC}"
    echo "git cherry-pick $COMMIT_SHA"
    echo ""
    echo -e "${YELLOW}Review the changes above and run without --dry-run to apply.${NC}"
    exit 0
fi

# Confirm action
echo -e "${RED}⚠️  WARNING: This will modify the orchestration-tools canonical source${NC}"
echo "Make sure this change has been reviewed and approved."
echo ""
read -p "Continue with reverse sync? (yes/no): " -r
if [[ ! "$REPLY" =~ ^[Yy][Ee][Ss]$ ]]; then
    echo "Reverse sync cancelled."
    exit 0
fi

# Perform cherry-pick
echo -e "${BLUE}Performing cherry-pick...${NC}"
if git cherry-pick "$COMMIT_SHA"; then
    echo -e "${GREEN}✓ Successfully applied changes to orchestration-tools${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Test the changes: python setup/launch.py --help"
    echo "2. Push to remote: git push origin orchestration-tools"
    echo "3. Changes will propagate to other branches on next pull/merge"
    echo ""
    echo -e "${GREEN}Reverse sync completed successfully!${NC}"
else
    echo -e "${RED}✗ Cherry-pick failed. Resolve conflicts and run:${NC}"
    echo "git cherry-pick --continue  # or"
    echo "git cherry-pick --abort     # to cancel"
    exit 1
fi