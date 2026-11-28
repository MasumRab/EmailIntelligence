#!/bin/bash
# TARGETED REGRESSION FIXES FOR PR BRANCHES
# Applies specific regression fixes from main to PR branches without full rebase
# Usage: ./scripts/fix_pr_regressions.sh <PR_NUMBER>

set -e

PR=${1:-}

if [ -z "$PR" ]; then
    echo "Usage: $0 <PR_NUMBER>"
    echo "Example: $0 139"
    exit 1
fi

ROOT="/home/masum/github/remote/EmailIntelligence"
PR_WT="$ROOT/wt/pr-$PR-fix"

echo "=== TARGETED REGRESSION FIX for PR #$PR ==="

# Create worktree from PR head
if [ ! -d "$PR_WT" ]; then
    echo "Creating worktree for PR #$PR..."
    cd "$ROOT"
    git worktree add "$PR_WT" "origin/pull/$PR/head" 2>/dev/null || {
        echo "Trying alternative fetch..."
        git fetch origin "pull/$PR/head:pr-$PR-head"
        git worktree add "$PR_WT" "pr-$PR-head"
    }
fi

cd "$PR_WT"
echo "Worktree at: $PR_WT"
echo "Current branch: $(git branch --show-current)"

# Link shared .venv
if [ ! -L ".venv" ]; then
    ln -s ../../.venv .venv
fi

echo "=== APPLYING TARGETED REGRESSION FIXES ==="

# Fix 1: verify_model_safety in security.py
echo "Fix 1: Restore verify_model_safety in src/core/security.py"
git show main:src/core/security.py > /tmp/security_main.py
cp /tmp/security_main.py src/core/security.py
echo "  ✓ Restored verify_model_safety"

# Fix 2: shell=True in branch_rename_migration.py (only if file exists)
if [ -f "scripts/branch_rename_migration.py" ]; then
    echo "Fix 2: Fix shell=True in scripts/branch_rename_migration.py"
    git show main:scripts/branch_rename_migration.py > /tmp/branch_rename_main.py
    cp /tmp/branch_rename_main.py scripts/branch_rename_migration.py
    echo "  ✓ Fixed shell=True → shell=False"
else
    echo "Fix 2: scripts/branch_rename_migration.py not in this PR - skipping"
fi

# Fix 3: SecurityHeadersMiddleware.__call__ in middleware.py
echo "Fix 3: Restore SecurityHeadersMiddleware.__call__ in src/core/middleware.py"
git show main:src/core/middleware.py > /tmp/middleware_main.py
cp /tmp/middleware_main.py src/core/middleware.py
echo "  ✓ Restored SecurityHeadersMiddleware.__call__"

# Fix 4: rate_limiter.py
echo "Fix 4: Restore rate_limiter.py (157 lines)"
git show main:src/core/rate_limiter.py > /tmp/rate_limiter_main.py
cp /tmp/rate_limiter_main.py src/core/rate_limiter.py
echo "  ✓ Restored rate_limiter.py (157 lines)"

# Fix 5: dashboard.tsx
echo "Fix 5: Restore dashboard.tsx (235 lines)"
git show main:client/src/pages/dashboard.tsx > /tmp/dashboard_main.tsx
cp /tmp/dashboard_main.tsx client/src/pages/dashboard.tsx
echo "  ✓ Restored dashboard.tsx (235 lines)"

# Fix 6: Remove duplicate def main in launch.py (if present)
echo "Fix 6: Check for duplicate def main in setup/launch.py"
if [ -f "setup/launch.py" ] && git show HEAD:setup/launch.py | grep "^def main" | sort | uniq -c | awk '$1>1' | grep -q .; then
    echo "  Found duplicate def main - restoring from main"
    git show main:setup/launch.py > /tmp/launch_main.py
    cp /tmp/launch_main.py setup/launch.py
    echo "  ✓ Fixed duplicate def main"
else
    echo "  ✓ No duplicate def main found or file missing"
fi

echo ""
echo "=== VERIFICATION ==="
echo "1. verify_model_safety: $(cat src/core/security.py | grep -c "verify_model_safety")"
echo "2. shell=True: $(cat scripts/branch_rename_migration.py 2>/dev/null | grep -c "shell=True" || echo "0 (file missing)")"
echo "3. SecurityHeadersMiddleware.__call__: $(cat src/core/middleware.py | grep -c "def __call__")"
echo "4. rate_limiter.py lines: $(cat src/core/rate_limiter.py | wc -l)"
echo "5. dashboard.tsx lines: $(cat client/src/pages/dashboard.tsx | wc -l)"
echo "6. Duplicate def main: $(cat setup/launch.py 2>/dev/null | grep "^def main" | sort | uniq -c | awk '\$1>1 {print \$1 " duplicates of " \$2}' || echo "0 (file missing)")"

echo ""
echo "=== COMMITTING FIXES ==="
git add -A
git commit -m "fix: apply targeted regression fixes from main

- Restore verify_model_safety() in src/core/security.py
- Fix shell=True → shell=False in scripts/branch_rename_migration.py (if present)
- Restore SecurityHeadersMiddleware.__call__ in src/core/middleware.py
- Restore rate_limiter.py (157 lines)
- Restore dashboard.tsx (235 lines)
- All fixes cherry-picked from main branch

👾 Generated with [Letta Code](https://letta.com)

Co-Authored-By: Letta Code <noreply@letta.com>"

echo ""
echo "=== PUSHING FIXES ==="
git push origin HEAD:refs/heads/$(git branch --show-current) --force

echo ""
echo "=== FIXES APPLIED TO PR #$PR ==="
echo "Run verification: cd $ROOT/wt/pr-$PR-fix && ./scripts/verify_fixes.sh"
