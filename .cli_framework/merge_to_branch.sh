#!/bin/bash
# CLI Branch Merger Script
# Safely merges CLI branch features into other branches with minimal interference

set -e  # Exit on any error

# Configuration
SOURCE_BRANCH="cli-enhanced"
TARGET_BRANCH=""
BACKUP_BRANCH=""
LOG_FILE=".cli_framework/merge.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Print colored output
print_status() {
    echo -e "${GREEN}[STATUS]${NC} $1"
    log "STATUS: $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    log "INFO: $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    log "WARNING: $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    log "ERROR: $1"
}

# Function to display usage
usage() {
    echo "Usage: $0 --target <branch_name> [--backup <backup_name>] [--mode <minimal|full>]"
    echo "  --target: Target branch to merge CLI features into"
    echo "  --backup: Name for the backup branch (optional, defaults to 'backup-<target>-cli-merge')"
    echo "  --mode: Installation mode (minimal or full, defaults to minimal)"
    echo ""
    echo "Examples:"
    echo "  $0 --target main"
    echo "  $0 --target scientific --mode full"
    echo "  $0 --target feature-x --backup feature-x-pre-cli --mode minimal"
    exit 1
}

# Parse command line arguments
TARGET_BRANCH=""
BACKUP_NAME=""
INSTALL_MODE="minimal"

while [[ $# -gt 0 ]]; do
    case $1 in
        --target)
            TARGET_BRANCH="$2"
            shift 2
            ;;
        --backup)
            BACKUP_NAME="$2"
            shift 2
            ;;
        --mode)
            INSTALL_MODE="$2"
            if [[ "$INSTALL_MODE" != "minimal" && "$INSTALL_MODE" != "full" ]]; then
                print_error "Invalid mode: $INSTALL_MODE. Use 'minimal' or 'full'."
                exit 1
            fi
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate required arguments
if [[ -z "$TARGET_BRANCH" ]]; then
    print_error "Target branch is required"
    usage
fi

# Main function
main() {
    print_status "Starting CLI branch merge process from '$SOURCE_BRANCH' to '$TARGET_BRANCH'"
    print_info "Installation mode: $INSTALL_MODE"
    
    # Check if source branch exists
    if ! git rev-parse --verify "$SOURCE_BRANCH" >/dev/null 2>&1; then
        print_error "Source branch '$SOURCE_BRANCH' does not exist"
        exit 1
    fi
    
    # Check if target branch exists
    if ! git rev-parse --verify "$TARGET_BRANCH" >/dev/null 2>&1; then
        print_error "Target branch '$TARGET_BRANCH' does not exist"
        exit 1
    fi
    
    # Create backup branch name if not provided
    if [[ -z "$BACKUP_NAME" ]]; then
        BACKUP_NAME="backup-${TARGET_BRANCH}-pre-cli-$(date +%Y%m%d-%H%M%S)"
    fi
    
    # Create backup of target branch
    print_status "Creating backup branch: $BACKUP_NAME"
    git branch -f "$BACKUP_NAME" "$TARGET_BRANCH"
    print_info "Backup branch created: $BACKUP_NAME"
    
    # Switch to target branch
    print_status "Switching to target branch: $TARGET_BRANCH"
    git checkout "$TARGET_BRANCH"
    
    # Create temporary merge branch
    TEMP_MERGE_BRANCH="temp-cli-merge-$(date +%s)"
    print_status "Creating temporary merge branch: $TEMP_MERGE_BRANCH"
    git checkout -b "$TEMP_MERGE_BRANCH"
    
    # Get the list of files that changed in the CLI branch
    print_status "Getting list of files to merge from $SOURCE_BRANCH"
    CHANGED_FILES=$(git diff --name-only "$TARGET_BRANCH" "$SOURCE_BRANCH" | grep -v ".git")
    
    if [[ -z "$CHANGED_FILES" ]]; then
        print_warning "No differences found between $TARGET_BRANCH and $SOURCE_BRANCH"
        print_info "Maybe the branches are already synchronized?"
        git checkout "$TARGET_BRANCH"
        git branch -D "$TEMP_MERGE_BRANCH"
        exit 0
    fi
    
    print_info "Files to be merged:"
    echo "$CHANGED_FILES" | while read -r file; do
        if [[ -n "$file" ]]; then
            echo "  - $file"
        fi
    done
    
    # Create a patch with only the necessary files
    print_status "Creating selective patch with CLI-specific files"
    
    # Create a temporary directory for the patch
    TEMP_PATCH_DIR=$(mktemp -d)
    
    # Copy only the CLI-related files to the patch directory
    echo "$CHANGED_FILES" | while read -r file; do
        if [[ -n "$file" ]]; then
            # Only include CLI-related files
            if [[ "$file" == "emailintelligence_cli.py" ]] || 
               [[ "$file" == src/* ]] && 
               ([[ "$file" == */resolution/* ]] || 
                [[ "$file" == */git/* ]] || 
                [[ "$file" == */analysis/* ]] || 
                [[ "$file" == */core/* ]] || 
                [[ "$file" == */strategy/* ]] || 
                [[ "$file" == */validation/* ]] || 
                [[ "$file" == */utils/* ]]); then
               
               # Create directory structure in temp patch
               mkdir -p "$TEMP_PATCH_DIR/$(dirname "$file")"
               cp "$file" "$TEMP_PATCH_DIR/$file" 2>/dev/null || echo "Could not copy $file" >&2
            fi
        fi
    done
    
    # Apply the selective changes
    print_status "Applying CLI-specific changes to temporary branch"
    
    # Switch to the temporary branch
    git checkout "$TEMP_MERGE_BRANCH" 2>/dev/null || git checkout -b "$TEMP_MERGE_BRANCH"
    
    # Copy the files from the patch directory to the current branch
    find "$TEMP_PATCH_DIR" -type f -exec cp --parents {} . \; 2>/dev/null || true
    
    # Add the copied files
    git add $(find "$TEMP_PATCH_DIR" -type f | sed 's|.*/||' | xargs -I {} find . -name {} 2>/dev/null) 2>/dev/null || true
    
    # Commit the changes
    if ! git diff --cached --quiet; then
        git commit -m "feat: Integrate CLI features from $SOURCE_BRANCH to $TARGET_BRANCH [non-interference mode]"
        print_status "Changes committed to temporary branch"
    else
        print_warning "No CLI-specific files were added to the commit"
    fi
    
    # Switch back to target branch
    print_status "Switching back to target branch: $TARGET_BRANCH"
    git checkout "$TARGET_BRANCH"
    
    # Merge the temporary branch into the target branch
    print_status "Merging temporary branch into target branch"
    git merge --no-ff "$TEMP_MERGE_BRANCH" -m "Merge CLI features into $TARGET_BRANCH (non-interference merge)"
    
    # Clean up temporary branch
    print_status "Cleaning up temporary branch: $TEMP_MERGE_BRANCH"
    git branch -D "$TEMP_MERGE_BRANCH"
    
    # Clean up temporary directory
    rm -rf "$TEMP_PATCH_DIR"
    
    print_status "CLI branch merge completed successfully!"
    print_info "Target branch: $TARGET_BRANCH"
    print_info "Backup branch: $BACKUP_NAME"
    print_info "Changes applied in non-interference mode"
    
    # Run the installation script to ensure proper integration
    if [[ -f ".cli_framework/install.sh" ]]; then
        print_status "Running CLI framework installation script in $INSTALL_MODE mode"
        ./.cli_framework/install.sh "$INSTALL_MODE"
    else
        print_warning "CLI framework installation script not found"
    fi
    
    print_status "Merge process completed. Please review changes before pushing."
}

# Run main function
main