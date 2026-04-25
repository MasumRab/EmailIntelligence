#!/usr/bin/env bash
# detect-branch-stack.sh — Branch-style-aware tech stack detection
# Usage: bash scripts/detect-branch-stack.sh [--generate-eval]
# 
# This script:
# 1. Classifies the current branch into a style family (scientific, orchestration-tools, main, taskmaster)
# 2. Detects the cumulative tech stack for that style family across all branches
# 3. Detects what's actually present on the current branch
# 4. Recommends agentrulegen.com templates with PERMISSIVE inclusion
# 5. Optionally generates a branch-specific evaluation skeleton (--generate-eval)
#
# Key principle: if ANY branch targeting this style uses a tool, the agent rules
# should mention it. Rules are permissive — include unless hard conflict.

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
SAFE_BRANCH="$(echo "$BRANCH" | sed 's|/|_|g')"
EVAL_FILE="$ROOT/docs/handoff/phase-10-stack-evaluation-${SAFE_BRANCH}.md"
SKIP_GEN=false
[ "${1:-}" = "--skip-gen" ] && SKIP_GEN=true
# Auto-generate eval file if missing (unless --skip-gen flag)
GENERATE_EVAL=false
[ ! -f "$EVAL_FILE" ] && [ "$SKIP_GEN" = false ] && GENERATE_EVAL=true

# ============================================================
# Section 1: Branch style classification
# ============================================================

classify_branch() {
    local branch="$1"
    case "$branch" in
        main|add-comparison-files-to-main)
            echo "main"
            ;;
        scientific|update-scientific|backup/scientific-*|add-comparison-files-to-scientific)
            echo "scientific"
            ;;
        orchestration-tools|orchestration-tools-*|add-comparison-files-to-orchestration-tools)
            echo "orchestration-tools"
            ;;
        taskmaster|taskmaster-*)
            echo "taskmaster"
            ;;
        # Feature branches — classify by prefix/pattern to their target
        bolt*|sentinel*|feat/modular*|configurable-*)
            echo "scientific"  # Performance/security/feature work targets scientific
            ;;
        001-*|002-*|003-*|004-*|migration-*|clean-launch*)
            echo "orchestration-tools"  # Numbered tasks target orchestration-tools
            ;;
        feature/task-*|task-*)
            echo "taskmaster"  # Task branches target taskmaster
            ;;
        cto/*|dependabot/*|backend-*)
            echo "scientific"  # CI/backend work targets scientific
            ;;
        000-*|consolidat*|spec-*|beads-*)
            echo "spec"  # Spec/experimental branches
            ;;
        *)
            # Default: check merge-base proximity to known roots
            # Fall back to scientific as it has the most branches
            echo "scientific"
            ;;
    esac
}

BRANCH_STYLE="$(classify_branch "$BRANCH")"

echo "=== BRANCH TECH STACK DETECTION ==="
echo "Branch:  $BRANCH"
echo "Style:   $BRANCH_STYLE"
echo "Root:    $ROOT"
echo ""

# ============================================================
# Section 2: Style profile definitions
# ============================================================
# These are cumulative profiles — they describe what the style FAMILY uses,
# not just what the current branch has. Profiles grow as feature branches
# add capabilities. They should only be trimmed on major reworks.

echo "--- Style Profile: $BRANCH_STYLE ---"
echo ""

# Each style has:
#   PROFILE_DESC     — what this style does
#   PROFILE_PYTHON   — Python tools/frameworks used across all branches in this style
#   PROFILE_JS       — JS/TS tools used across all branches in this style
#   PROFILE_SHELL    — Shell scripting characteristics
#   PROFILE_TEMPLATES — agentrulegen.com templates to evaluate (permissive)
#   PROFILE_NOTES    — special considerations

case "$BRANCH_STYLE" in
    scientific)
        PROFILE_DESC="Full application backend: AI engine, database, caching, auth, email processing, model management, workflow engine, Gradio UI"
        PROFILE_PYTHON="fastapi pydantic pydantic-settings uvicorn sqlalchemy aiosqlite torch transformers accelerate scikit-learn nltk gradio httpx redis celery"
        PROFILE_JS="react vite tanstack-query wouter zod tailwind radix-ui"
        PROFILE_SHELL="moderate (setup scripts, CI)"
        PROFILE_TEMPLATES="python-fastapi python-ml ai-agent-workflow git-workflow code-review"
        PROFILE_NOTES="Primary application branch. Has async routes, SQLAlchemy models, ML inference, Gradio UI. All ML/AI rules apply."
        ;;
    orchestration-tools)
        PROFILE_DESC="CLI tooling, agent infrastructure, shell orchestration, multi-branch management, agent rules framework"
        PROFILE_PYTHON="fastapi pydantic uvicorn torch transformers accelerate scikit-learn nltk gradio httpx redis"
        PROFILE_JS="react vite tanstack-query wouter zod tailwind radix-ui"
        PROFILE_SHELL="heavy (78+ scripts in modules/ and scripts/, branch management, distribution, validation)"
        PROFILE_TEMPLATES="python-fastapi python-ml ai-agent-workflow git-workflow code-review"
        PROFILE_NOTES="CLI-focused. FastAPI/SQLAlchemy deps present but routes live on scientific. Shell scripting is a first-class concern. Agent rules infrastructure is primary purpose."
        ;;
    main)
        PROFILE_DESC="Stable production branch — union of scientific + orchestration capabilities that have been merged"
        PROFILE_PYTHON="fastapi pydantic pydantic-settings uvicorn transformers accelerate scikit-learn nltk gradio httpx redis"
        PROFILE_JS="react vite tanstack-query wouter zod tailwind radix-ui"
        PROFILE_SHELL="moderate (merged orchestration scripts)"
        PROFILE_TEMPLATES="python-fastapi python-ml ai-agent-workflow git-workflow code-review"
        PROFILE_NOTES="Production baseline. Gets capabilities from both scientific and orchestration-tools merges. Rules should cover both domains."
        ;;
    taskmaster)
        PROFILE_DESC="Task management infrastructure, agent memory systems, triage workflows"
        PROFILE_PYTHON="fastapi pydantic"
        PROFILE_JS=""
        PROFILE_SHELL="light"
        PROFILE_TEMPLATES="ai-agent-workflow code-review"
        PROFILE_NOTES="Focused on .taskmaster/ config, .agent_memory/, .iflow/ predictions, .beads/ interaction tracking. Minimal application code."
        ;;
    spec|*)
        PROFILE_DESC="Spec consolidation, experimental, or unclassified branch"
        PROFILE_PYTHON="varies"
        PROFILE_JS="varies"
        PROFILE_SHELL="varies"
        PROFILE_TEMPLATES="code-review"
        PROFILE_NOTES="Check actual branch contents — may inherit from any style."
        ;;
esac

echo "  Description:  $PROFILE_DESC"
echo "  Python deps:  $PROFILE_PYTHON"
echo "  JS/TS deps:   $PROFILE_JS"
echo "  Shell weight: $PROFILE_SHELL"
echo "  Templates:    $PROFILE_TEMPLATES"
echo "  Notes:        $PROFILE_NOTES"
echo ""

# ============================================================
# Section 3: Current branch actual state
# ============================================================

echo "--- Current Branch Actual State ---"
echo ""

# Python deps from requirements.txt or setup/requirements.txt
python_deps=()
req_file=""
if [ -f "$ROOT/requirements.txt" ]; then
    req_file="$ROOT/requirements.txt"
elif [ -f "$ROOT/setup/requirements.txt" ]; then
    req_file="$ROOT/setup/requirements.txt"
fi

if [ -n "$req_file" ]; then
    echo "  Python source: $req_file"
    for dep in fastapi pydantic uvicorn sqlalchemy aiosqlite torch transformers accelerate scikit-learn nltk gradio redis celery httpx pytest; do
        grep -qi "^${dep}" "$req_file" 2>/dev/null && python_deps+=("$dep")
    done
    echo "  Python deps found: ${python_deps[*]:-none}"
fi

# JS/TS deps
js_deps=""
if [ -f "$ROOT/client/package.json" ]; then
    js_deps=$(python3 -c "
import json
pkg = json.load(open('$ROOT/client/package.json'))
deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
markers = {'react':'react','@tanstack/react-query':'tanstack-query','wouter':'wouter',
    'zod':'zod','tailwindcss':'tailwind','@radix-ui':'radix-ui','vite':'vite',
    'typescript':'typescript','gradio':'gradio'}
found = [label for key,label in markers.items() if any(k.startswith(key) if key.startswith('@') else k==key for k in deps)]
print(' '.join(found))
" 2>/dev/null)
    echo "  JS/TS deps: ${js_deps:-none}"
fi

# Shell scripts
sh_count=0
[ -d "$ROOT/modules" ] && sh_count=$((sh_count + $(find "$ROOT/modules" -name "*.sh" 2>/dev/null | wc -l)))
[ -d "$ROOT/scripts" ] && sh_count=$((sh_count + $(find "$ROOT/scripts" -name "*.sh" 2>/dev/null | wc -l)))
echo "  Shell scripts: $sh_count"

# Source code
py_src=$(find "$ROOT/src" -name "*.py" -not -path "*__pycache__*" 2>/dev/null | wc -l)
ts_src=$(find "$ROOT/client/src" -name "*.ts" -o -name "*.tsx" 2>/dev/null | wc -l)
echo "  Python src/ files: $py_src"
echo "  TypeScript client/ files: $ts_src"

# Key patterns
has_async_routes=$(grep -rl "async def.*route\|@app\.\|@router\." "$ROOT/src" 2>/dev/null | wc -l)
has_sqlalchemy=$(grep -rl "sqlalchemy\|AsyncSession\|Base.metadata" "$ROOT/src" 2>/dev/null | wc -l)
has_cli=$([ -d "$ROOT/src/cli" ] && echo "yes" || echo "no")
has_gradio=$(grep -rl "gr\.\|gradio\." "$ROOT/src" 2>/dev/null | wc -l)
echo "  Async routes: $has_async_routes files"
echo "  SQLAlchemy: $has_sqlalchemy files"
echo "  CLI arch: $has_cli"
echo "  Gradio UI: $has_gradio files"

# Config files (redundancy signals)
echo ""
echo "--- Config Files (agents can infer from these) ---"
for f in .flake8 setup.cfg pyproject.toml .pylintrc .mypy.ini pytest.ini \
         client/tsconfig.json tailwind.config.js tailwind.config.ts; do
    [ -f "$ROOT/$f" ] && echo "  ✅ $f"
done

# ============================================================
# Section 4: Template recommendations (PERMISSIVE)
# ============================================================

echo ""
echo "=== RECOMMENDED TEMPLATES (permissive) ==="
echo ""
echo "Style $BRANCH_STYLE evaluates: $PROFILE_TEMPLATES"
echo ""

# For each template in the profile, determine match level
for tmpl in $PROFILE_TEMPLATES; do
    case "$tmpl" in
        python-fastapi)
            if [ "$has_async_routes" -gt 0 ] && [ "$has_sqlalchemy" -gt 0 ]; then
                echo "  ✅ python-fastapi        — FULL (async routes + SQLAlchemy on this branch)"
            elif [[ " ${python_deps[*]:-} " =~ " fastapi " ]]; then
                echo "  ⚠️  python-fastapi        — INCLUDE (FastAPI in deps; routes may be on sibling branches)"
            else
                echo "  📋 python-fastapi        — STYLE INCLUDE (FastAPI used across $BRANCH_STYLE branches)"
            fi
            ;;
        python-ml)
            if [ "$has_gradio" -gt 0 ] || [[ " ${python_deps[*]:-} " =~ " torch " ]]; then
                echo "  ✅ python-ml             — FULL (ML deps + code on this branch)"
            elif echo "$PROFILE_PYTHON" | grep -q "torch"; then
                echo "  ⚠️  python-ml             — INCLUDE (ML deps in style profile; code may be on sibling branches)"
            else
                echo "  ⚪ python-ml             — SKIP (no ML in this style)"
            fi
            ;;
        ai-agent-workflow)
            if [ "$has_cli" = "yes" ] || [ "$sh_count" -gt 10 ]; then
                echo "  ✅ ai-agent-workflow     — FULL (CLI + orchestration patterns)"
            else
                echo "  ⚠️  ai-agent-workflow     — INCLUDE (agent workflow patterns relevant to style)"
            fi
            ;;
        git-workflow)
            if [ "$sh_count" -gt 5 ]; then
                echo "  ✅ git-workflow          — FULL ($sh_count shell scripts, multi-branch project)"
            else
                echo "  ⚠️  git-workflow          — INCLUDE (multi-branch project, git conventions apply)"
            fi
            ;;
        code-review)
            echo "  ✅ code-review           — ALWAYS RELEVANT"
            ;;
    esac
done

echo ""
echo "=== PERMISSIVE INCLUSION PRINCIPLE ==="
echo ""
echo "If a branch in the '$BRANCH_STYLE' style family uses a tool, it should be"
echo "mentioned in .ruler/AGENTS.md — even if not actively used on THIS branch."
echo "Only exclude if it creates a HARD CONFLICT with the current branch's purpose."
echo ""
echo "Redundancy signals (rules agents can infer from config files):"
[ -f "$ROOT/.flake8" ] && echo "  - Line length, ignore patterns → .flake8"
[ -f "$ROOT/setup.cfg" ] && echo "  - isort profile, test paths → setup.cfg"
[ -f "$ROOT/pytest.ini" ] && echo "  - Test markers, pytest options → pytest.ini"
[ -f "$ROOT/.pylintrc" ] && echo "  - Pylint config → .pylintrc"
[ -f "$ROOT/client/package.json" ] && echo "  - JS framework choice → client/package.json"

# ============================================================
# Section 5: Generate evaluation skeleton (optional)
# ============================================================

if $GENERATE_EVAL; then
    echo ""
    echo "=== GENERATING EVALUATION SKELETON ==="
    echo "Output: $EVAL_FILE"

    cat > "$EVAL_FILE" << EVALEOF
# Phase 10 Appendix: Branch-Dependent Stack Evaluation

**Generated for:** \`$BRANCH\` branch (style: \`$BRANCH_STYLE\`)
**Generated at:** $(date -Iseconds)
**Detection script:** \`bash scripts/detect-branch-stack.sh --generate-eval\`

---

## Branch Classification

| Property | Value |
|----------|-------|
| Branch | \`$BRANCH\` |
| Style | \`$BRANCH_STYLE\` |
| Style Description | $PROFILE_DESC |
| Templates to Evaluate | $PROFILE_TEMPLATES |
| Python src/ files | $py_src |
| Shell scripts | $sh_count |
| TypeScript files | $ts_src |

---

## Style Profile: \`$BRANCH_STYLE\`

**Cumulative Python deps across all branches in this style:**
$PROFILE_PYTHON

**Special notes:** $PROFILE_NOTES

**Permissive inclusion principle:** If any branch targeting \`$BRANCH_STYLE\` uses a tool,
the agent rules should mention it — even if not actively used on this specific branch.
Only exclude if it creates a hard conflict.

---

## Current Branch Actual State

- **Python deps on this branch:** ${python_deps[*]:-none}
- **JS/TS deps on this branch:** ${js_deps:-none}
- **Shell scripts:** $sh_count
- **Async route handlers:** $has_async_routes files
- **SQLAlchemy usage:** $has_sqlalchemy files
- **CLI architecture:** $has_cli
- **Gradio UI:** $has_gradio files

---

## Template Evaluations

> For each template below, classify every rule as:
> - **INCLUDE** — Rule is relevant to the style family (permissive default)
> - **ALREADY COVERED** — Rule exists in \`.ruler/AGENTS.md\`
> - **REDUNDANT** — Rule is expressed in a config file (\`.flake8\`, \`setup.cfg\`, etc.)
> - **HARD CONFLICT** — Rule contradicts a project convention (only reason to exclude)

EVALEOF

    for tmpl in $PROFILE_TEMPLATES; do
        cat >> "$EVAL_FILE" << TMPLEOF

### Template: \`$tmpl\`

| # | Rule | Verdict | Rationale |
|---|------|---------|-----------|
| 1 | [evaluate from agentrulegen.com/templates/$tmpl] | [INCLUDE/ALREADY COVERED/REDUNDANT/HARD CONFLICT] | [reason] |

TMPLEOF
    done

    cat >> "$EVAL_FILE" << FOOTEREOF

---

## Consolidated Gap Analysis

### Rules to ADD to \`.ruler/AGENTS.md\`

| # | Rule | Source Template | Proposed Text |
|---|------|----------------|---------------|
| 1 | [fill in after evaluation] | | |

### Rules confirmed REDUNDANT (already in config files)

| Rule | Config File |
|------|-------------|
| [fill in] | [fill in] |

### Rules confirmed ESSENTIAL (keep)

| Rule | Why Essential |
|------|--------------|
| [fill in] | [fill in] |

---

## Line Count Impact

Current \`.ruler/AGENTS.md\`: $(wc -l < "$ROOT/.ruler/AGENTS.md" 2>/dev/null || echo "?") lines
Gate check threshold: 80 lines

| Change | Lines Added | Running Total |
|--------|-------------|---------------|
| [fill in] | | |
FOOTEREOF

    echo "✅ Generated: $EVAL_FILE"
elif [ -f "$EVAL_FILE" ]; then
    echo ""
    echo "=== EVALUATION SKELETON ==="
    echo "✅ Using existing: $EVAL_FILE"
    echo "   To regenerate, delete the file and re-run this script"
fi

echo ""
echo "=== DONE ==="
