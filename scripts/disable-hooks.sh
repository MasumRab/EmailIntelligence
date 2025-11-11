#!/bin/bash

# Script to temporarily disable Git hooks for development work
# This helps avoid hook-related warnings when working on non-orchestration branches

set -e

echo "Disabling Git hooks..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a Git repository"
    exit 1
fi

# Backup existing hooks if they exist
HOOKS_DIR=".git/hooks"
BACKUP_DIR=".git/hooks_backup"

if [ -d "$HOOKS_DIR" ] && [ "$(ls -A $HOOKS_DIR)" ]; then
    echo "Backing up existing hooks..."
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
    fi
    
    # Move all hook files to backup directory
    for hook in "$HOOKS_DIR"/*; do
        if [ -f "$hook" ]; then
            hook_name=$(basename "$hook")
            echo "  Backing up $hook_name"
            mv "$hook" "$BACKUP_DIR/$hook_name"
        fi
    done
fi

# Create dummy hooks that simply exit successfully
echo "Creating dummy hooks..."

HOOK_NAMES=("pre-commit" "post-commit" "post-merge" "post-checkout" "post-push")

for hook_name in "${HOOK_NAMES[@]}"; do
    hook_path="$HOOKS_DIR/$hook_name"
    
    # Create the hook file with a simple exit 0
    cat > "$hook_path" << 'EOF'
#!/bin/bash
# Dummy hook - does nothing
exit 0
EOF
    
    # Make it executable
    chmod +x "$hook_path"
    echo "  Created dummy $hook_name hook"
done

echo "Git hooks have been disabled successfully!"
echo ""
echo "To restore the original hooks later, run:"
echo "  ./scripts/restore-hooks.sh"