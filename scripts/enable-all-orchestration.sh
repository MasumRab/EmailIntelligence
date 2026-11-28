#!/bin/bash
# Re-enable all orchestration workflows and integrations
# Usage: ./scripts/enable-all-orchestration.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Re-enabling all orchestration workflows and integrations..."
echo ""

# Step 1: Clear environment variable
echo "[1/4] Clearing ORCHESTRATION_DISABLED environment variable..."
export ORCHESTRATION_DISABLED=false

# Remove from .env files
if [[ -f "$PROJECT_ROOT/.env" ]]; then
    sed -i.bak '/ORCHESTRATION_DISABLED/d' "$PROJECT_ROOT/.env"
    echo "  ✓ Updated .env"
fi

if [[ -f "$PROJECT_ROOT/.env.local" ]]; then
    sed -i.bak '/ORCHESTRATION_DISABLED/d' "$PROJECT_ROOT/.env.local"
    echo "  ✓ Updated .env.local"
fi

# Step 2: Restore git hooks
echo ""
echo "[2/4] Restoring git hooks..."
if [[ -d "$PROJECT_ROOT/.git/hooks" ]]; then
    HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
    
    # Find most recent backup
    LATEST_BACKUP=$(find "$PROJECT_ROOT/.git" -maxdepth 1 -name "hooks.backup-*" -type d 2>/dev/null | sort -V | tail -1)
    
    if [[ -n "$LATEST_BACKUP" ]]; then
        hook_count=0
        for hook in "$HOOKS_DIR"/*.disabled; do
            if [[ -f "$hook" ]]; then
                # Rename back to original
                original="${hook%.disabled}"
                mv "$hook" "$original" 2>/dev/null || true
                chmod +x "$original" 2>/dev/null || true
                ((hook_count++))
            fi
        done
        
        if [[ $hook_count -gt 0 ]]; then
            echo "  ✓ Restored $hook_count git hooks from .disabled files"
        fi
        
        echo "  ✓ Using backup from: $LATEST_BACKUP"
    else
        echo "  ⚠ No backup found, you may need to reinstall hooks"
        echo "    Run: ./scripts/install-hooks.sh"
    fi
else
    echo "  ⚠ Git hooks directory not found"
fi

# Step 3: Remove marker file
echo ""
echo "[3/4] Removing orchestration disabled marker..."
if [[ -f "$PROJECT_ROOT/.orchestration-disabled" ]]; then
    rm -f "$PROJECT_ROOT/.orchestration-disabled"
    echo "  ✓ Removed .orchestration-disabled marker"
else
    echo "  ✓ Marker file not present"
fi

# Step 4: Verification
echo ""
echo "[4/4] Verification..."
if [[ ! -f "$PROJECT_ROOT/.orchestration-disabled" ]]; then
    echo "  ✓ Marker file removed"
fi

if [[ -f "$PROJECT_ROOT/.env.local" ]]; then
    if ! grep -q "ORCHESTRATION_DISABLED" "$PROJECT_ROOT/.env.local"; then
        echo "  ✓ .env.local cleaned"
    fi
fi

active_hooks=$(find "$PROJECT_ROOT/.git/hooks" -type f ! -name "*.disabled" ! -name "*.sample" 2>/dev/null | wc -l)
if [[ $active_hooks -gt 0 ]]; then
    echo "  ✓ $active_hooks git hooks active"
fi

echo ""
echo "================================="
echo "✅ All orchestration enabled!"
echo "================================="
echo ""
echo "To disable orchestration again, run:"
echo "  ./scripts/disable-all-orchestration.sh"
echo ""
