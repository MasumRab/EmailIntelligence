# Phase 0: Content Bootstrap

**Purpose:** Generate framework-specific rules from agentrulegen.com templates before sync.
**Steps:** 4
**Dependencies:** None (can run independently, but should run BEFORE Phase 3)

---

## Why This Phase?

Before running Ruler to sync agent rules across tools, we need quality content.

**Option A:** agentrulegen.com (Web UI) — 10,000+ curated rules, 41 languages  
**Option B:** agent-rules-kit (CLI) — 15+ stacks, 9+ IDEs, MCP tool integration

**Recommendation:** Use Option A or B for templates, then customize for project.

---

## External Reference

- **Agent Rules Builder:** https://agentrulegen.com
- **Languages:** Python, TypeScript, Go, Rust, Java, C#, Ruby, Swift (41+)
- **Frameworks:** FastAPI, Next.js, React, SQLAlchemy, Pydantic
- **AI Tools:** Cursor, Claude Code, Copilot, Windsurf, Cline, Codex, Gemini CLI

---

## Option B: agent-rules-kit CLI (Alternative)

**Repository:** https://github.com/tecnomanu/agent-rules-kit  
**Version:** v3.8.1 (installed globally at `~/.local/share/mise/installs/node/22.22.2/bin/agent-rules-kit`)

### Multi-Step CLI Process

Agent-Rules-Kit is an **interactive CLI tool** that supports both:
1. **Interactive mode** — Prompts for user input
2. **Non-interactive mode** — CLI flags to skip prompts

### Available CLI Flags (Non-Interactive)

```bash
# Core Options
--stack=<name>         # Framework: laravel, nextjs, react, vue, angular, nodejs, go, etc.
--version=<num>        # Stack version
--architecture=<name>   # Architecture: standard, ddd, hexagonal, app, pages
--ide=<name>           # Target IDE (see table below)

# Global Rules
--global               # Include global best practice rules
--no-global            # Skip global rules

# MCP Tools Integration
--mcp-tools=<list>     # Comma-separated: pampa,github,memory,filesystem,git

# Utility
--auto-install         # Skip all prompts and use defaults
--debug               # Show detailed logs
--update              # Update existing rules
```

### Supported Stacks

| Stack | Versions | Architectures |
|-------|----------|---------------|
| **laravel** | 8-12 | standard, ddd, hexagonal |
| **nextjs** | 12-14 | app, pages |
| **react** | 17-18 | standard, hooks, concurrent |
| **angular** | 14-17 | standard, standalone, micro-frontends |
| **vue** | 2-3 | options, composition, nuxt |
| **nestjs** | 8-10 | standard, microservices, graphql |
| **nodejs** | 18-20 | standard |
| **go** | 1.20-1.22 | standard, ddd, hexagonal |
| **svelte** | 3-5 | standard, runes |
| **astro** | 2-5 | static, ssr, hybrid |
| **mcp** | SDKs | server, client, toolkit |
| **pampa** | latest | standard |

### Supported IDEs (--ide flag)

| IDE | Value | Output |
|-----|-------|--------|
| Cursor | `cursor` | `.cursor/rules/rules-kit/*.mdc` |
| VS Code/Copilot | `vscode` | `.github/copilot-instructions.md` |
| Windsurf | `windsurf` | `.windsurf/rules/*.md` |
| Continue | `continue` | `.continue/rules/*.md` |
| Claude Code | `claude` | `CLAUDE.md` |
| Gemini Code | `gemini` | `GEMINI.md` |
| Zed | `zed` | `.rules` |
| Codex | `codex` | `AGENTS.md` |
| Cline | `cline` | `.clinerules` |

### Usage Examples

```bash
# Interactive mode (requires user input)
npx agent-rules-kit
# → Prompts for: stack, version, architecture, IDE, global rules, MCP tools

# Non-interactive single stack
agent-rules-kit --stack=react --version=18 --ide=claude --global --auto-install

# Multiple MCP tools
agent-rules-kit --mcp-tools=pampa,github,memory --global --auto-install

# Full configuration
agent-rules-kit --stack=nextjs --version=14 --architecture=app --ide=cursor --global --mcp-tools=pampa,github --auto-install
```

### EmailIntelligence Recommended Commands

```bash
# Option 1: Global best practices only (no stack-specific rules)
agent-rules-kit --global --ide=claude --auto-install

# Option 2: React frontend rules
agent-rules-kit --stack=react --version=18 --global --ide=claude --auto-install

# Option 3: MCP tools integration
agent-rules-kit --mcp-tools=pampa,github --global --auto-install
```

### Step-by-Step Integration with Ruler

```bash
# Step 1: Run agent-rules-kit (generates to IDE-specific path)
agent-rules-kit --stack=react --version=18 --global --ide=claude --auto-install
# → Creates: ./CLAUDE.md (if --ide=claude)

# Step 2: COPY content to Ruler source
cat CLAUDE.md >> .ruler/AGENTS.md

# Step 3: Remove CLAUDE.md (Ruler will recreate it)
rm CLAUDE.md

# Step 4: Apply Ruler to distribute to all tools
ruler apply --project-root .

# Step 5: VERIFY results
head -30 CLAUDE.md
head -30 .cursor/rules/CLAUDE.md
```

### ⚠️ CRITICAL WARNINGS

| DO NOT | Why |
|--------|-----|
| Run without `--auto-install` | Interactive mode requires user input |
| Use `--ide=cursor` directly | Creates files in `.cursor/rules/` that may conflict with Ruler |
| Skip the copy step | Ruler expects `.ruler/AGENTS.md` as source of truth |

### MCP Tools Available

| Tool | Purpose | Installed? |
|------|---------|------------|
| **pampa** | Semantic code search | ⚠️ Optional |
| **github** | Repository management | ✅ via MCP |
| **memory** | Persistent knowledge | ✅ via MCP |
| **filesystem** | File operations | ✅ via MCP |
| **git** | Version control | ✅ via MCP |

**Note:** For semantic code search, prefer **existing tools** over pampa:

```bash
# AST-grep — Search and rewrite code using AST patterns (v0.42.0)
ast-grep run 'console.log($VAR)' --lang typescript

# Semgrep — Code security analysis with AST patterns (v1.157.0)
semgrep --config=auto .

# CK-search — Code search tool (v0.7.0)
ck-search "authentication"
```

---

## Step 0.1 — Choose Template Source

### Option A: agentrulegen.com (Web UI — Manual Workflow)

**IMPORTANT: No API available** — Must use manual cut-paste workflow.

```bash
# Step 1: OPEN — Visit in browser
open https://agentrulegen.com

# Step 2: SELECT — On the website:
# - Choose Language: Python, TypeScript
# - Choose Framework: FastAPI, React
# - Select AI Tools: Claude Code, Cursor, Windsurf

# Step 3: GENERATE — Click "Generate Rules" button
# - Website generates ~150-200 lines of curated rules
# - Rules appear in browser text area

# Step 4: COPY — Select all generated content
# - Use Ctrl+A (select all) + Ctrl+C (copy)
# - Or use browser "Copy" button if available

# Step 5: PASTE — Create/update the Ruler source file
# - Create: .ruler/AGENTS.md
# - Paste: Insert copied content
# - Save the file
```

**Workflow Summary:** Website → Select options → Generate → CUT → PASTE → `.ruler/AGENTS.md`

### Option B: agent-rules-kit (CLI — Partially Automated)

```bash
# Step 1: RUN CLI (generates files locally)
npx agent-rules-kit --stack=python --global

# Step 2: VIEW generated content
cat .cursor/rules/*.mdc

# Step 3: COPY relevant sections (remove frontmatter first)
# - Files have --- frontmatter blocks
# - Strip frontmatter before pasting

# Step 4: PASTE to .ruler/AGENTS.md
# - DO NOT use: npx agent-rules-kit install (CAUSES SYNC DRIFT)
# - Instead: manually copy content to Ruler source
```

**Both options feed `.ruler/AGENTS.md` → Ruler distributes to all tools.**

---

## Step 0.2 — Export Generated Rules

**Action:** Use Agent Rules Builder to generate Python/FastAPI/React rules.

**URLs:**
- Main builder: https://agentrulegen.com
- Python/FastAPI template: https://agentrulegen.com/templates/python-fastapi
- Git workflow template: https://agentrulegen.com/templates/git-workflow

**Select:**
1. Language: **Python**, **TypeScript**
2. Framework: **FastAPI**, **React**, **SQLAlchemy**, **Pydantic**
3. AI Tools: **Claude Code**, **Cursor**, **Windsurf**, **Roo**

**Expected Output:** ~150-200 lines of curated rules per tool.

---

## Step 0.2 — Export Generated Rules

**Action:** Copy generated rules to `.ruler/AGENTS.md`.

**Generated content includes:**

```markdown
## Code Style
- Use `interface` for object shapes, `type` for unions
- Prefer `const` by default; avoid `any`
- Enable strict mode with no implicit any

## Architecture
- Keep functions under 20 lines; extract helpers early
- Discriminated unions for state, not boolean flags

## Testing
- Follow Arrange-Act-Assert in every test case
- Mock all external deps — test logic, not network
```

**Export to:** `.ruler/AGENTS.md`

---

## Step 0.3 — Customize for EmailIntelligence

**Action:** Add project-specific rules to `.ruler/AGENTS.md`.

**Add:**

```markdown
## Project Overview
EmailIntelligence is a Python/FastAPI + React/TypeScript application for AI-powered email analysis.

## Key Directories
- `src/core/` — AI engine, database manager
- `backend/python_backend/` — FastAPI backend
- `client/` — React frontend (Vite)
- `modules/` — Pluggable feature modules

## Task Management
Uses Task Master AI. See `.taskmaster/` for configuration.
Use `task-master list`, `task-master next`, `task-master show <id>`.

## Critical Rules
- NEVER commit secrets or API keys
- NEVER use `eval()` or `exec()`
- Add type hints to all function parameters
```

---

## Step 0.4 — Verify Bootstrap Content

**Run:**
```bash
echo "=== PHASE 0 VERIFY ==="
test -f .ruler/AGENTS.md && echo "✅ .ruler/AGENTS.md exists" || echo "❌ MISSING"
lines=$(wc -l < .ruler/AGENTS.md)
test "$lines" -gt 30 && echo "✅ Content sufficient ($lines lines)" || echo "⚠️ Content brief ($lines lines)"
grep -q "Code Style" .ruler/AGENTS.md && echo "✅ Has Code Style section" || echo "❌ Missing Code Style"
grep -q "Architecture" .ruler/AGENTS.md && echo "✅ Has Architecture section" || echo "❌ Missing Architecture"
grep -q "Testing" .ruler/AGENTS.md && echo "✅ Has Testing section" || echo "❌ Missing Testing"
grep -q "Project Overview\|EmailIntelligence" .ruler/AGENTS.md && echo "✅ Has project-specific content" || echo "❌ Missing project content"
```

**Expected:** All checks pass.

---

## Gate Check

```bash
echo "=== PHASE 0 GATE CHECK ==="
test -f .ruler/AGENTS.md && echo "PASS: .ruler/AGENTS.md exists" || echo "FAIL: MISSING"
lines=$(wc -l < .ruler/AGENTS.md); test "$lines" -gt 30 && echo "PASS: $lines lines" || echo "FAIL: too brief"
grep -q "Code Style\|Architecture\|Testing" .ruler/AGENTS.md && echo "PASS: Has template content" || echo "FAIL: Missing sections"
grep -q "EmailIntelligence" .ruler/AGENTS.md && echo "PASS: Has project content" || echo "FAIL: No project customization"
```

---

## Token Impact

| Source | Lines | Tokens (approx) |
|--------|-------|-----------------|
| agentrulegen.com Python/FastAPI | ~100 | ~500 |
| agentrulegen.com TypeScript/React | ~100 | ~500 |
| Project-specific additions | ~50 | ~250 |
| **Total** | ~250 | **~1,250** |

**Per-session impact:** ~400-800 tokens (depends on tool)

---

## Notes

- This phase can be done manually via browser or automated via API
- agentrulegen.com is free, no signup required
- Generated rules should be reviewed before export
- Consider rule length: 80-150 lines is optimal (Claude ignores longer files)
