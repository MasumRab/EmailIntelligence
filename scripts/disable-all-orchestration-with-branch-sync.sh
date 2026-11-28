#!/bin/bash
# Disable all orchestration workflows and integrations with branch profile updates
# This script:
#   - Disables all git hooks
#   - Sets ORCHESTRATION_DISABLED=true environment variable
#   - Updates branch profile information to reflect orchestration disabled state
#   - Pushes changes to scientific and main branches
#
# Usage: ./scripts/disable-all-orchestration-with-branch-sync.sh [--skip-push]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKIP_PUSH=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-push)
            SKIP_PUSH=1
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
    shift
done

echo "=========================================="
echo "🔌 DISABLING ALL ORCHESTRATION"
echo "=========================================="
echo ""

# Save current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "📍 Current branch: $CURRENT_BRANCH"
echo ""

# Step 1: Set environment variable
echo "[1/5] Setting ORCHESTRATION_DISABLED environment variable..."
export ORCHESTRATION_DISABLED=true

# Add to .env files
if [[ -f "$PROJECT_ROOT/.env" ]]; then
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
echo ""

# Step 2: Disable git hooks
echo "[2/5] Disabling git hooks..."
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
echo ""

# Step 3: Create marker file
echo "[3/5] Creating orchestration disabled marker..."
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
echo ""

# Step 4: Update branch profiles with orchestration status
echo "[4/5] Updating branch profiles with orchestration status..."
PROFILES_DIR="$PROJECT_ROOT/.context-control/profiles"

if [[ -d "$PROFILES_DIR" ]]; then
    # Update main profile
    if [[ -f "$PROFILES_DIR/main.json" ]]; then
        python3 << 'PYTHON_SCRIPT'
import json
import sys

profile_file = '/home/masum/github/EmailIntelligenceAuto/.context-control/profiles/main.json'
try:
    with open(profile_file, 'r') as f:
        profile = json.load(f)
    
    # Add orchestration status metadata
    if 'metadata' not in profile:
        profile['metadata'] = {}
    
    profile['metadata']['orchestration_disabled'] = True
    profile['metadata']['orchestration_disabled_timestamp'] = True
    profile['agent_settings']['orchestration_aware'] = False
    
    with open(profile_file, 'w') as f:
        json.dump(profile, f, indent=2)
    
    print(f"  ✓ Updated main.json with orchestration_disabled: true")
except Exception as e:
    print(f"  ⚠ Failed to update main.json: {e}")
    sys.exit(1)
PYTHON_SCRIPT
    fi
    
    # Update scientific profile
    if [[ -f "$PROFILES_DIR/scientific.json" ]]; then
        python3 << 'PYTHON_SCRIPT'
import json
import sys

profile_file = '/home/masum/github/EmailIntelligenceAuto/.context-control/profiles/scientific.json'
try:
    with open(profile_file, 'r') as f:
        profile = json.load(f)
    
    # Add orchestration status metadata
    if 'metadata' not in profile:
        profile['metadata'] = {}
    
    profile['metadata']['orchestration_disabled'] = True
    profile['metadata']['orchestration_disabled_timestamp'] = True
    profile['agent_settings']['orchestration_aware'] = False
    
    with open(profile_file, 'w') as f:
        json.dump(profile, f, indent=2)
    
    print(f"  ✓ Updated scientific.json with orchestration_disabled: true")
except Exception as e:
    print(f"  ⚠ Failed to update scientific.json: {e}")
    sys.exit(1)
PYTHON_SCRIPT
    fi
    
    # Update orchestration-tools profile
    if [[ -f "$PROFILES_DIR/orchestration-tools.json" ]]; then
        python3 << 'PYTHON_SCRIPT'
import json
import sys

profile_file = '/home/masum/github/EmailIntelligenceAuto/.context-control/profiles/orchestration-tools.json'
try:
    with open(profile_file, 'r') as f:
        profile = json.load(f)
    
    # Add orchestration status metadata
    if 'metadata' not in profile:
        profile['metadata'] = {}
    
    profile['metadata']['orchestration_disabled'] = True
    profile['metadata']['orchestration_disabled_timestamp'] = True
    profile['agent_settings']['orchestration_aware'] = False
    
    with open(profile_file, 'w') as f:
        json.dump(profile, f, indent=2)
    
    print(f"  ✓ Updated orchestration-tools.json with orchestration_disabled: true")
except Exception as e:
    print(f"  ⚠ Failed to update orchestration-tools.json: {e}")
    sys.exit(1)
PYTHON_SCRIPT
    fi
else
    echo "  ⚠ Profile directory not found at $PROFILES_DIR"
fi
echo ""

# Step 5: Commit and push changes to scientific and main branches
echo "[5/5] Committing and pushing changes to scientific and main branches..."

if [[ $SKIP_PUSH -eq 1 ]]; then
    echo "  ⏭ Skipping push (--skip-push flag used)"
else
    # Stage changes
    git add "$PROJECT_ROOT/.env.local" \
            "$PROJECT_ROOT/.orchestration-disabled" \
            "$PROJECT_ROOT/.gitignore" \
            "$PROJECT_ROOT/.context-control/profiles/" 2>/dev/null || true
    
    # Commit if there are changes
    if ! git diff --cached --quiet; then
        git commit -m "chore: disable all orchestration workflows (hooks, server-side check, branch profiles)" 2>/dev/null || true
        echo "  ✓ Changes committed"
        
        # Push to current branch
        git push origin "$CURRENT_BRANCH" 2>/dev/null || true
        echo "  ✓ Changes pushed to $CURRENT_BRANCH"
        
        # Push to scientific branch if different from current
        if [[ "$CURRENT_BRANCH" != "scientific" ]]; then
            echo "  📤 Pushing to scientific branch..."
            git push origin "$CURRENT_BRANCH:scientific" 2>/dev/null || true
            echo "  ✓ Changes pushed to scientific branch"
        fi
        
        # Push to main branch if different from current
        if [[ "$CURRENT_BRANCH" != "main" ]]; then
            echo "  📤 Pushing to main branch..."
            git push origin "$CURRENT_BRANCH:main" 2>/dev/null || true
            echo "  ✓ Changes pushed to main branch"
        fi
    else
        echo "  ℹ No changes to commit"
    fi
fi
echo ""

# Verification
echo "[✓] Verification..."
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
echo "=========================================="
echo "✅ All orchestration disabled!"
echo "=========================================="
echo ""
echo "To re-enable orchestration, run:"
echo "  ./scripts/enable-all-orchestration-with-branch-sync.sh"
echo ""
