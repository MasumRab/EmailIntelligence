# Phase 3: Ruler Setup

**Purpose:** Configure Ruler for TOML-based multi-agent sync.
**Steps:** 6
**Dependencies:** Phase 1 complete

---

## ⚠️ CRITICAL: contextFileName Alignment

**Discovery:** Gemini CLI and Qwen Code use `settings.json` with `contextFileName: "AGENTS.md"`.

This means **8+ tools read AGENTS.md natively** (AgentsMdAgent base class):
- `gemini-cli`, `qwen`, `opencode`, `amp`, `kilocode`, `cursor`, `windsurf`, `roo`

**Implication:**
- Custom `output_path` entries create files these tools may never read
- Only tools with unique paths need custom output_path:
  - `claude` → `CLAUDE.md`
  - `cline` → `.clinerules/`
  - `kiro` → `.kiro/steering/`
  - `trae` → `.trae/rules/`

**Decision Implemented:**
- **No `output_path` for pure CLI tools** (amp, qwen, opencode, kilocode) — they read root `AGENTS.md` natively
- **Keep `output_path` for IDE tools** (claude, cline, kiro, trae) — unique paths required
- **Keep `output_path` for hybrid tools** (cursor, windsurf, roo) — optional, may read both locations
- **6 redundant `system.md` files were DELETED:** `.qwen/system.md`, `.agents/system.md`, `.cursor/rules/system.md`, `.windsurf/rules/system.md`, `.roo/rules/system.md`, `.kilo/rules/system.md`

**Result:** ruler.toml NO LONGER has agent sections for amp, qwen, opencode, kilocode — Ruler uses built-in defaults.

**Files that should be DELETED:**
- `.qwen/system.md`, `.agents/system.md`, `.opencode/system.md`, `.kilo/rules/system.md` (pure CLI tools — no output_path)

**Files that MAY exist (hybrid tools with optional output_path):**
- `.cursor/rules/system.md`, `.windsurf/rules/system.md`, `.roo/rules/system.md` (may be recreated by ruler apply)

**Verification:**
```bash
# Verify AGENTS.md exists at project root
test -f AGENTS.md && echo "AGENTS.md: EXISTS" || echo "AGENTS.md: MISSING"
```

---

## External Reference

- **Ruler GitHub:** https://github.com/intellectronica/ruler
- **Supported agents:** claude, cursor, cline, copilot, roo, kiro, trae, windsurf, amp, gemini-cli, qwen, opencode, codex

---

## Step 3.1 — Create .ruler/ directory

```bash
mkdir -p .ruler
```

---

## Step 3.2 — Create .ruler/AGENTS.md

**File:** `.ruler/AGENTS.md`
**Action:** CREATE

```markdown
# EmailIntelligence — AI Agent Instructions

## Project Overview
EmailIntelligence is a Python/FastAPI + React/TypeScript full-stack application for intelligent email analysis. Primary language is Python 3.11+.

## Code Conventions
- Python: Black formatting, 100 char line length, type hints required, Google-style docstrings
- TypeScript: Strict mode, 2-space indent, semicolons, double quotes
- Test: pytest for Python, npm run test for TypeScript

## Build Commands
- Backend: `python launch.py`
- Frontend: `cd client && npm run build`
- Test: `pytest` (Python), `cd client && npm run lint` (TypeScript)
- Lint: `flake8 .` / `mypy .` / `pylint src modules`

## Key Directories
- `src/core/` — AI engine, database manager, workflow engines
- `backend/python_backend/` — FastAPI backend
- `client/` — React frontend (Vite)
- `modules/` — Pluggable feature modules
- `rules/` — Shared YAML linting rules

## Task Management
This project uses Task Master AI for task tracking. See `.taskmaster/` for configuration.
Use `task-master list`, `task-master next`, `task-master show <id>` for workflow.

## Critical Rules
- NEVER commit secrets or API keys
- NEVER use `eval()` or `exec()`
- NEVER hard-code file paths
- Use dependency injection over global state
- Add type hints to all function parameters and return values
```

---

## Step 3.3 — Create .ruler/ruler.toml

**File:** `.ruler/ruler.toml`
**Action:** CREATE

```toml
# Ruler Configuration — EmailIntelligence
# Docs: https://github.com/intellectronica/ruler

nested = false

[gitignore]
enabled = true
local = false

# Only enable agents we actually use
default_agents = [
  "gemini-cli",   # CLI Tier 1 (primary)
  "qwen",         # CLI Tier 1
  "opencode",     # CLI Tier 1
  "amp",          # CLI Tier 1
  "kilocode",     # CLI Tier 1
  "claude",       # IDE Tier 2
  "cursor",       # IDE Tier 2
  "cline",        # IDE Tier 2
  "roo",          # IDE Tier 2
  "kiro",         # IDE Tier 2
  "trae",         # IDE Tier 2
  "windsurf",     # IDE Tier 2
]

[agents.claude]
enabled = true
output_path = "CLAUDE.md"

[agents.cursor]
enabled = true
output_path = ".cursor/rules/system.md"

[agents.cline]
enabled = true
output_path = ".clinerules/system.md"

[agents.roo]
enabled = true
output_path = ".roo/rules/system.md"

[agents.kiro]
enabled = true
output_path = ".kiro/steering/system.md"

[agents.trae]
enabled = true
output_path = ".trae/rules/system.md"

[agents.windsurf]
enabled = true
output_path = ".windsurf/rules/system.md"

# MCP Server Configuration
[mcp_servers.task-master-ai]
command = "npm"
args = ["exec", "task-master-ai"]

[mcp_servers.task-master-ai.env]
GOOGLE_API_KEY = "${GOOGLE_API_KEY}"
GEMINI_API_KEY = "${GEMINI_API_KEY}"
XAI_API_KEY = "${XAI_API_KEY}"
OPENROUTER_API_KEY = "${OPENROUTER_API_KEY}"
MISTRAL_API_KEY = "${MISTRAL_API_KEY}"
OLLAMA_API_KEY = "${OLLAMA_API_KEY}"
GITHUB_API_KEY = "${GITHUB_API_KEY}"
```

---

## Step 3.4 — Verify Ruler config (dry-run)

```bash
ruler apply --project-root . --dry-run 2>&1 | head -5
```

**Expected:** `[ruler:dry-run] Applying rules for...` messages

---

## Step 3.5 — Apply Ruler

```bash
ruler apply --project-root . --backup
```

This writes rules to enabled agent directories and creates `.bak` backups.

---

## Step 3.6 — Verify Ruler output

```bash
echo "=== RULER VERIFY ==="
test -f CLAUDE.md && echo "CLAUDE.md: EXISTS" || echo "CLAUDE.md: MISSING"
test -f AGENTS.md && echo "AGENTS.md: EXISTS" || echo "AGENTS.md: MISSING"
grep -c "EmailIntelligence" CLAUDE.md 2>/dev/null || echo "0"
```

---

## Gate Check

```bash
echo "=== PHASE 3 GATE CHECK ==="
test -f .ruler/AGENTS.md && echo ".ruler/AGENTS.md: PASS" || echo ".ruler/AGENTS.md: FAIL"
test -f .ruler/ruler.toml && echo ".ruler/ruler.toml: PASS" || echo ".ruler/ruler.toml: FAIL"
grep -q "EmailIntelligence" CLAUDE.md && echo "CLAUDE.md content: PASS" || echo "CLAUDE.md content: FAIL"
```
