#!/usr/bin/env bash
# detect-branch-stack.sh — Auto-detect tech stack and recommend agentrulegen.com templates
# Usage: bash scripts/detect-branch-stack.sh
# Works from any CWD inside the repo. Used by Phase 10 to determine which
# agentrulegen.com templates and rules to evaluate for the current branch.
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

echo "=== BRANCH TECH STACK DETECTION ==="
echo "Branch: $BRANCH  Root: $ROOT"
echo ""

# ============================================================
# Section 1: Python stack detection
# ============================================================
echo "--- Python Stack ---"

python_detected=false
python_deps=()

if [ -f "$ROOT/requirements.txt" ]; then
    python_detected=true
    echo "Source: requirements.txt"

    # Core frameworks
    grep -qi "^fastapi" "$ROOT/requirements.txt" && python_deps+=("fastapi")
    grep -qi "^pydantic" "$ROOT/requirements.txt" && python_deps+=("pydantic")
    grep -qi "^uvicorn" "$ROOT/requirements.txt" && python_deps+=("uvicorn")
    grep -qi "^sqlalchemy\|^aiosqlite" "$ROOT/requirements.txt" && python_deps+=("sqlalchemy-async")
    grep -qi "^django" "$ROOT/requirements.txt" && python_deps+=("django")
    grep -qi "^flask" "$ROOT/requirements.txt" && python_deps+=("flask")

    # AI/ML
    grep -qi "^torch" "$ROOT/requirements.txt" && python_deps+=("torch")
    grep -qi "^transformers" "$ROOT/requirements.txt" && python_deps+=("transformers")
    grep -qi "^accelerate" "$ROOT/requirements.txt" && python_deps+=("accelerate")
    grep -qi "^scikit-learn" "$ROOT/requirements.txt" && python_deps+=("scikit-learn")
    grep -qi "^nltk\|^textblob" "$ROOT/requirements.txt" && python_deps+=("nlp")
    grep -qi "^gradio" "$ROOT/requirements.txt" && python_deps+=("gradio")

    # Data/infra
    grep -qi "^redis" "$ROOT/requirements.txt" && python_deps+=("redis")
    grep -qi "^celery" "$ROOT/requirements.txt" && python_deps+=("celery")
    grep -qi "^httpx" "$ROOT/requirements.txt" && python_deps+=("httpx")

    # Testing
    grep -qi "^pytest" "$ROOT/requirements.txt" && python_deps+=("pytest")

    # Google APIs
    grep -qi "^google-api-python-client\|^google-auth" "$ROOT/requirements.txt" && python_deps+=("google-apis")

    echo "  Dependencies: ${python_deps[*]:-none}"
fi

if [ -f "$ROOT/pyproject.toml" ]; then
    python_detected=true
    echo "  Also has: pyproject.toml"
fi

if ! $python_detected; then
    echo "  No Python dependency files found"
fi

# ============================================================
# Section 2: JavaScript/TypeScript stack detection
# ============================================================
echo ""
echo "--- JavaScript/TypeScript Stack ---"

js_detected=false
js_deps=()

if [ -f "$ROOT/client/package.json" ]; then
    js_detected=true
    echo "Source: client/package.json"

    # Core framework
    python3 -c "
import json, sys
pkg = json.load(open('$ROOT/client/package.json'))
deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
markers = {
    'react': 'react', 'next': 'next', 'vue': 'vue', 'svelte': 'svelte',
    '@tanstack/react-query': 'tanstack-query',
    'wouter': 'wouter', 'react-router': 'react-router',
    'zod': 'zod', 'react-hook-form': 'react-hook-form',
    'tailwindcss': 'tailwind', 'tailwind-merge': 'tailwind-merge',
    '@radix-ui': 'radix-ui',
    'framer-motion': 'framer-motion',
    'recharts': 'recharts',
    'lucide-react': 'lucide',
    'typescript': 'typescript',
    'vite': 'vite', 'vitest': 'vitest',
    'class-variance-authority': 'cva',
}
found = []
for key, label in markers.items():
    if any(k.startswith(key) if key.startswith('@') else k == key for k in deps):
        found.append(label)
print(' '.join(found))
" 2>/dev/null | while read -r line; do
        echo "  Dependencies: $line"
    done

    # Count Radix components
    radix_count=$(python3 -c "
import json
pkg = json.load(open('$ROOT/client/package.json'))
deps = pkg.get('dependencies', {})
count = sum(1 for k in deps if k.startswith('@radix-ui/'))
print(count)
" 2>/dev/null)
    echo "  Radix UI components: ${radix_count:-0}"
fi

if [ -f "$ROOT/package.json" ] && [ ! -f "$ROOT/client/package.json" ]; then
    js_detected=true
    echo "Source: package.json (root)"
fi

if ! $js_detected; then
    echo "  No JavaScript/TypeScript dependency files found"
fi

# ============================================================
# Section 3: Shell/Bash stack detection
# ============================================================
echo ""
echo "--- Shell/Bash Stack ---"

sh_modules=0
sh_scripts=0

if [ -d "$ROOT/modules" ]; then
    sh_modules=$(find "$ROOT/modules" -name "*.sh" 2>/dev/null | wc -l)
fi
if [ -d "$ROOT/scripts" ]; then
    sh_scripts=$(find "$ROOT/scripts" -name "*.sh" 2>/dev/null | wc -l)
fi

echo "  modules/*.sh: $sh_modules files"
echo "  scripts/*.sh: $sh_scripts files"
echo "  Total shell scripts: $((sh_modules + sh_scripts))"

if [ "$((sh_modules + sh_scripts))" -gt 10 ]; then
    echo "  Shell is a SIGNIFICANT part of this branch"
fi

# ============================================================
# Section 4: Linter/formatter config detection
# ============================================================
echo ""
echo "--- Config Files (what agents can infer) ---"

for f in .flake8 setup.cfg pyproject.toml .pylintrc .mypy.ini mypy.ini pytest.ini \
         .eslintrc .eslintrc.json .eslintrc.js eslint.config.js \
         .prettierrc .prettierrc.json prettier.config.js \
         tsconfig.json client/tsconfig.json \
         tailwind.config.js tailwind.config.ts postcss.config.js; do
    [ -f "$ROOT/$f" ] && echo "  ✅ $f"
done

# ============================================================
# Section 5: Source code profile
# ============================================================
echo ""
echo "--- Source Code Profile ---"

py_files=$(find "$ROOT/src" -name "*.py" -not -path "*__pycache__*" 2>/dev/null | wc -l)
ts_files=$(find "$ROOT/client/src" -name "*.ts" -o -name "*.tsx" 2>/dev/null | wc -l)

echo "  Python files in src/: $py_files"
echo "  TypeScript files in client/src/: $ts_files"

# Check for specific patterns
has_async_routes=$(grep -rl "async def.*route\|@app\.\|@router\." "$ROOT/src" 2>/dev/null | wc -l)
has_sqlalchemy=$(grep -rl "sqlalchemy\|AsyncSession\|Base.metadata" "$ROOT/src" 2>/dev/null | wc -l)
has_cli=$([ -d "$ROOT/src/cli" ] && echo "yes" || echo "no")

echo "  Async route handlers: $has_async_routes files"
echo "  SQLAlchemy usage: $has_sqlalchemy files"
echo "  CLI architecture: $has_cli"

# ============================================================
# Section 6: Recommended agentrulegen.com templates
# ============================================================
echo ""
echo "=== RECOMMENDED TEMPLATES ==="
echo ""
echo "Based on detected stack, evaluate these agentrulegen.com templates:"
echo ""

# Python/FastAPI
if [[ " ${python_deps[*]} " =~ " fastapi " ]]; then
    if [ "$has_sqlalchemy" -gt 0 ]; then
        echo "  ✅ python-fastapi        — FULL MATCH (FastAPI + SQLAlchemy detected)"
    else
        echo "  ⚠️  python-fastapi        — PARTIAL (FastAPI detected, no SQLAlchemy on this branch)"
    fi
else
    echo "  ⚪ python-fastapi        — SKIP (no FastAPI usage on this branch)"
fi

# AI/ML
if [[ " ${python_deps[*]} " =~ " torch " ]] || [[ " ${python_deps[*]} " =~ " transformers " ]]; then
    echo "  ✅ ai-agent-workflow     — RELEVANT (torch/transformers in deps)"
else
    echo "  ⚠️  ai-agent-workflow     — PARTIAL (no AI/ML code on this branch, but orchestration patterns apply)"
fi

# Git workflow
if [ "$((sh_modules + sh_scripts))" -gt 5 ]; then
    echo "  ✅ git-workflow          — FULL MATCH ($((sh_modules + sh_scripts)) shell scripts, multi-branch project)"
else
    echo "  ⚪ git-workflow          — SKIP (minimal shell scripting)"
fi

# React/TypeScript
if $js_detected; then
    echo "  ✅ react-typescript      — FULL MATCH (React + TypeScript client detected)"
else
    echo "  ⚪ react-typescript      — SKIP (no frontend on this branch)"
fi

# Code review
echo "  ✅ code-review           — ALWAYS RELEVANT"

echo ""
echo "=== RULES GAP ANALYSIS TARGETS ==="
echo ""
echo "For each ✅ template above, the agent executing Phase 10 should:"
echo "  1. Read the template rules at agentrulegen.com/templates/<name>"
echo "  2. Compare each rule against .ruler/AGENTS.md"
echo "  3. Classify as: ALREADY COVERED | WORTH ADDING | NOT APPLICABLE | REDUNDANT"
echo "  4. Record findings in STATE file Phase 10 Decision Log"
echo ""
echo "For ⚠️ templates: extract only the rules that apply to code present on this branch."
echo "For ⚪ templates: skip entirely — no relevant code exists."
echo ""
echo "=== REDUNDANCY SIGNALS ==="
echo ""
echo "Rules that agents can INFER from config files (do NOT put in .ruler/AGENTS.md):"

[ -f "$ROOT/.flake8" ] && echo "  - Line length, ignore patterns → .flake8"
[ -f "$ROOT/setup.cfg" ] && echo "  - isort profile, test paths → setup.cfg"
[ -f "$ROOT/pytest.ini" ] && echo "  - Test markers, pytest options → pytest.ini"
[ -f "$ROOT/.pylintrc" ] && echo "  - Pylint config → .pylintrc"
[ -f "$ROOT/client/package.json" ] && echo "  - React version, framework choice → client/package.json"
[ -f "$ROOT/client/tsconfig.json" ] && echo "  - TypeScript strict mode, paths → client/tsconfig.json"

echo ""
echo "=== DONE ==="
