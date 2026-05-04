#!/usr/bin/env bash
# verify-agent-content.sh — Audit agent files against live branch state
# Usage: bash scripts/verify-agent-content.sh
# Works from any CWD inside the repo.
set -uo pipefail

# --- Detect project root ---
detect_root() {
    local dir="$PWD"
    while [ "$dir" != "/" ]; do
        [ -f "$dir/.git/HEAD" ] || [ -f "$dir/.git" ] && { echo "$dir"; return 0; }
        dir="$(dirname "$dir")"
    done
    echo "ERROR: not inside a git repo" >&2; return 1
}

ROOT="$(detect_root)"
BRANCH="$(git -C "$ROOT" branch --show-current 2>/dev/null || echo 'detached')"
RULER_SRC="$ROOT/.ruler/AGENTS.md"

claimed_valid=0
claimed_missing=0
undocumented=0

echo "=== AGENT CONTENT VERIFICATION ==="
echo "Branch: $BRANCH  Root: $ROOT"
echo ""

# --- Helper: check a claimed directory ---
check_claimed_dir() {
    local dir="$1" desc="$2"
    if [ -d "$ROOT/$dir" ]; then
        echo "  ✅ $dir — EXISTS ($desc)"
        claimed_valid=$((claimed_valid + 1))
    else
        echo "  ❌ $dir — CLAIMED BUT MISSING"
        claimed_missing=$((claimed_missing + 1))
    fi
}

# --- Helper: check undocumented directory ---
check_undocumented() {
    local dir="$1" desc="$2"
    if [ -d "$ROOT/$dir" ]; then
        # Check if it's mentioned in .ruler/AGENTS.md
        if grep -q "$dir" "$RULER_SRC" 2>/dev/null; then
            return 0
        fi
        echo "  ⚠️  $dir — EXISTS, NOT DOCUMENTED ($desc)"
        undocumented=$((undocumented + 1))
    fi
}

# --- Helper: check file exists ---
check_claimed_file() {
    local file="$1" desc="$2"
    if [ -f "$ROOT/$file" ]; then
        echo "  ✅ $file — EXISTS ($desc)"
        claimed_valid=$((claimed_valid + 1))
    else
        echo "  ❌ $file — CLAIMED BUT MISSING"
        claimed_missing=$((claimed_missing + 1))
    fi
}

# ============================================================
# Tier 1: .ruler/AGENTS.md claims
# ============================================================
echo "--- Tier 1 Shared Content (.ruler/AGENTS.md) ---"

if [ ! -f "$RULER_SRC" ]; then
    echo "  ❌ .ruler/AGENTS.md does not exist — cannot audit"
    exit 1
fi

echo ""
echo "Key Directories (claimed in .ruler/AGENTS.md):"
# Parse claimed directories dynamically from the Key Directories section
while IFS= read -r line; do
    dir=$(echo "$line" | sed -n 's/^- `\([^`]*\)`.*/\1/p' | sed 's|/$||')
    desc=$(echo "$line" | sed -n 's/.*— \(.*\)/\1/p')
    [ -z "$dir" ] && continue
    check_claimed_dir "$dir" "$desc"
done < <(sed -n '/^## Key Directories/,/^## /p' "$RULER_SRC" | grep '^- ')

# Content accuracy checks
echo ""
echo "Content Accuracy:"

# Verify claimed descriptions match file reality
if [ -d "$ROOT/src/core" ]; then
    core_files=$(ls "$ROOT/src/core/"*.py 2>/dev/null | wc -l)
    # Extract the claim text from .ruler/AGENTS.md
    core_claim=$(grep "src/core/" "$RULER_SRC" 2>/dev/null | head -1 | sed 's/.*— //')
    if echo "$core_claim" | grep -qi "AI engine\|database manager\|workflow"; then
        has_ai_engine=$([ -f "$ROOT/src/core/ai_engine.py" ] && echo "yes" || echo "no")
        has_database=$([ -f "$ROOT/src/core/database.py" ] && echo "yes" || echo "no")
        if [ "$has_ai_engine" = "no" ] || [ "$has_database" = "no" ]; then
            echo "  ⚠️  src/core/ claim: '$core_claim'"
            echo "     Reality: $core_files files — ai_engine=$has_ai_engine, database=$has_database"
            claimed_missing=$((claimed_missing + 1))
        else
            echo "  ✅ src/core/ description matches"
            claimed_valid=$((claimed_valid + 1))
        fi
    else
        echo "  ✅ src/core/ — $core_files files, claim: '$core_claim'"
        claimed_valid=$((claimed_valid + 1))
    fi
fi

# modules description check
if [ -d "$ROOT/modules" ]; then
    py_count=$(find "$ROOT/modules" -name "*.py" -not -path "*__pycache__*" 2>/dev/null | wc -l)
    sh_count=$(find "$ROOT/modules" -name "*.sh" 2>/dev/null | wc -l)
    modules_claim=$(grep "modules/" "$RULER_SRC" 2>/dev/null | head -1 | sed 's/.*— //')
    if echo "$modules_claim" | grep -qi "Pluggable\|Python\|feature module"; then
        if [ "$sh_count" -gt "$py_count" ]; then
            echo "  ⚠️  modules/ claim: '$modules_claim'"
            echo "     Reality: $sh_count shell scripts, $py_count Python files"
            claimed_missing=$((claimed_missing + 1))
        else
            echo "  ✅ modules/ description matches"
            claimed_valid=$((claimed_valid + 1))
        fi
    else
        echo "  ✅ modules/ — $sh_count shell, $py_count Python, claim: '$modules_claim'"
        claimed_valid=$((claimed_valid + 1))
    fi
fi

# backend/python_backend check
if [ -d "$ROOT/backend/python_backend" ]; then
    backend_claim=$(grep "backend/python_backend/" "$RULER_SRC" 2>/dev/null | head -1 | sed 's/.*— //')
    if echo "$backend_claim" | grep -qi "FastAPI backend$"; then
        if grep -q "DEPRECATED" "$ROOT/backend/python_backend/models.py" 2>/dev/null; then
            echo "  ⚠️  backend/ claim: '$backend_claim'"
            echo "     Reality: models.py is marked DEPRECATED"
            claimed_missing=$((claimed_missing + 1))
        else
            echo "  ✅ backend/ has active FastAPI code"
            claimed_valid=$((claimed_valid + 1))
        fi
    else
        echo "  ✅ backend/ — claim: '$backend_claim'"
        claimed_valid=$((claimed_valid + 1))
    fi
fi

# Build commands check
echo ""
echo "Build Commands:"
check_claimed_file "launch.py" "backend launcher"
check_claimed_file "client/package.json" "frontend build"
check_claimed_file "pytest.ini" "pytest config"

echo ""
echo "Undocumented Directories:"
check_undocumented "src/cli" "CLI command architecture with git/agent/task/analysis/infra subcommands"
check_undocumented "src/strategy" "Multi-phase resolution strategy, risk assessment"
check_undocumented "src/analysis" "Code analysis modules"
check_undocumented "src/validation" "Validation framework"
check_undocumented "src/resolution" "Conflict resolution engine"
check_undocumented "src/git" "Git integration layer"
check_undocumented "src/context_control" "Context contamination control"
check_undocumented "src/utils" "Shared utility modules"
check_undocumented "cli" "Root CLI package (backward-compatible entry point)"
check_undocumented "setup" "Launcher with DI container, routing, services"
check_undocumented "scripts" "$(ls "$ROOT/scripts/"*.{py,sh} 2>/dev/null | wc -l) automation/orchestration scripts"
check_undocumented "config" "Configuration files"
check_undocumented "data" "Data directory"
check_undocumented "docs/handoff" "Multi-phase handoff framework"

# ============================================================
# Tier 2: GEMINI.md / QWEN.md accuracy
# ============================================================
echo ""
echo "--- Tier 2 Files ---"

for tool in GEMINI QWEN; do
    file="$ROOT/$tool.md"
    if [ ! -f "$file" ]; then
        echo "$tool.md: NOT PRESENT (branch policy decision)"
        continue
    fi
    echo "$tool.md:"

    # Check if MCP config claim matches settings file
    case "$tool" in
        GEMINI) settings="$ROOT/.gemini/settings.json" ;;
        QWEN)   settings="$ROOT/.qwen/settings.json" ;;
    esac

    if [ -f "$settings" ]; then
        # Check contextFileName alignment
        settings_ctx=$(python3 -c "import json; d=json.load(open('$settings')); print(d.get('contextFileName', d.get('context', {}).get('fileName', 'UNKNOWN')))" 2>/dev/null)
        if grep -q "\"contextFileName\": \"$settings_ctx\"" "$file" 2>/dev/null || \
           grep -q "\"fileName\": \"$settings_ctx\"" "$file" 2>/dev/null; then
            echo "  ✅ MCP config matches $settings (context=$settings_ctx)"
        else
            echo "  ⚠️  MCP config in $tool.md may not match $settings (context=$settings_ctx)"
        fi
    else
        echo "  ⚠️  $settings not found — cannot verify MCP claim"
    fi
done

# Check other Tier 2 files
for file in IFLOW.md CRUSH.md LLXPRT.md; do
    if [ -f "$ROOT/$file" ]; then
        echo "$file: EXISTS"
    else
        echo "$file: NOT PRESENT"
    fi
done

# ============================================================
# Summary
# ============================================================
echo ""
echo "--- Summary ---"
echo "Claimed & Valid:   $claimed_valid"
echo "Claimed & Stale:   $claimed_missing"
echo "Undocumented:      $undocumented"
total_issues=$((claimed_missing + undocumented))
if [ "$total_issues" -eq 0 ]; then
    echo "✅ Agent content is aligned with branch reality"
else
    echo "⚠️  $total_issues issue(s) — agent files need updating for this branch"
fi
