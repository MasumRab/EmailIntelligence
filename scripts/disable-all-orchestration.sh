#!/bin/bash
# Disable all orchestration workflows and integrations
# Usage: ./scripts/disable-all-orchestration.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Disabling all orchestration workflows and integrations..."
echo ""

# Step 1: Set environment variable
echo "[1/4] Setting ORCHESTRATION_DISABLED environment variable..."
export ORCHESTRATION_DISABLED=true

# Add to .env files
if [[ -f "$PROJECT_ROOT/.env" ]]; then
    # Remove existing line if present
    sed -i.bak '/ORCHESTRATION_DISABLED/d' "$PROJECT_ROOT/.env"
    echo "ORCHESTRATION_DISABLED=true" >> "$PROJECT_ROOT/.env"
    echo "  ✓ Updated .env"
fi

if [[ -f "$PROJECT_ROOT/.env.local" ]]; then
    sed -i.bak '/ORCHESTRATION_DISABLED/d' "$PROJECT_ROOT/.env.local"
else
    touch "$PROJECT_ROOT/.env.local"
fi
echo "ORCHESTRATION_DISABLED=true" >> "$PROJECT_ROOT/.env.local"
echo "  ✓ Updated .env.local"

# Step 2: Disable git hooks
echo ""
echo "[2/4] Disabling git hooks..."
if [[ -d "$PROJECT_ROOT/.git/hooks" ]]; then
    HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
    BACKUP_DIR="$PROJECT_ROOT/.git/hooks.backup-$(date +%s)"
    
    mkdir -p "$BACKUP_DIR"
    
    hook_count=0
    for hook in "$HOOKS_DIR"/*; do
        if [[ -f "$hook" ]] && [[ ! "$hook" =~ \.disabled$ ]]; then
            cp "$hook" "$BACKUP_DIR/" 2>/dev/null || true
            mv "$hook" "$hook.disabled" 2>/dev/null || true
            ((hook_count++))
        fi
    done
    
    if [[ $hook_count -gt 0 ]]; then
        echo "  ✓ Disabled $hook_count git hooks"
        echo "  ✓ Backup saved to: $BACKUP_DIR"
    else
        echo "  ✓ No active hooks to disable"
    fi
else
    echo "  ⚠ Git hooks directory not found"
fi

# Step 3: Create marker file
echo ""
echo "[3/4] Creating orchestration disabled marker..."
if touch "$PROJECT_ROOT/.orchestration-disabled"; then
    echo "  ✓ Created .orchestration-disabled marker"
    
    # Add to .gitignore if not present
    if [[ -f "$PROJECT_ROOT/.gitignore" ]]; then
        if ! grep -q "^\.orchestration-disabled$" "$PROJECT_ROOT/.gitignore"; then
            echo ".orchestration-disabled" >> "$PROJECT_ROOT/.gitignore"
            echo "  ✓ Added to .gitignore"
        fi
    fi
else
    echo "  ⚠ Failed to create marker file"
fi

# Step 4: Summary
echo ""
echo "[4/4] Verification..."
if [[ "$ORCHESTRATION_DISABLED" == "true" ]]; then
    echo "  ✓ ORCHESTRATION_DISABLED=true"
fi

if [[ -f "$PROJECT_ROOT/.env.local" ]]; then
    if grep -q "ORCHESTRATION_DISABLED=true" "$PROJECT_ROOT/.env.local"; then
        echo "  ✓ .env.local configured"
    fi
fi

if [[ -f "$PROJECT_ROOT/.orchestration-disabled" ]]; then
    echo "  ✓ Marker file created"
fi

disabled_hooks=$(find "$PROJECT_ROOT/.git/hooks" -name "*.disabled" 2>/dev/null | wc -l)
if [[ $disabled_hooks -gt 0 ]]; then
    echo "  ✓ $disabled_hooks git hooks disabled"
fi

echo ""
echo "================================="
echo "✅ All orchestration disabled!"
echo "================================="
echo ""
echo "To re-enable orchestration, run:"
echo "  ./scripts/enable-all-orchestration.sh"
echo ""
echo "To disable only git hooks (keep workflows):"
echo "  ./scripts/disable-orchestration-hooks.sh"
echo ""
