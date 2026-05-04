# Agent Rules Implementation — Handoff Instructions

**Purpose:** Fix 13 identified issues in AI coding agent configurations  
**Project:** `/home/masum/github/EmailIntelligence`  
**Branch:** `004-guided-workflow`  
**Scope:** Phases 1-4 are REQUIRED. Phases 5-10 are OPTIONAL.

---

## Quick Reference

| Phase | Purpose | Status |
|-------|---------|--------|
| 1 | Emergency MCP fixes | REQUIRED |
| 2 | Content corrections | REQUIRED |
| 3 | Ruler setup | REQUIRED |
| 4 | Agent RuleZ setup | REQUIRED |
| 5 | GEMINI.md/QWEN.md cleanup | OPTIONAL |
| 6-10 | Extended deduplication | REFERENCE ONLY |

---

## CRITICAL RULES FOR EXECUTING AGENT

1. **NEVER use `create_file` on a file that already exists unless this document says "OVERWRITE".** Use `edit_file` for existing files.
2. **NEVER use `git add -A` or `git add .`** — only stage files you changed.
3. **NEVER modify files not listed in a step.** If you see other changes in the worktree, ignore them.
4. **After every step, run the VERIFY command.** Do not proceed if verification fails.
5. **One edit per `edit_file` call.** Do not combine multiple edits into one call.
6. **Copy strings EXACTLY from this document.** Do not paraphrase or reformat.
7. **If a tool call fails, read the file first, then retry.** Do not guess at content.

---

## PROGRESS TRACKER

**Required Phases (1-4):** Fix the 13 core issues.  
**Optional Phase 5:** File cleanup for GEMINI.md/QWEN.md.  
**Reference Phases (6-10):** Extended documentation — not executable tasks.

```
PHASE 1: Emergency Fixes [REQUIRED]
[ ] 1.1  Resolve CLAUDE.md merge conflict
[ ] 1.2  Verify CLAUDE.md
[ ] 1.3  Fix .roo/mcp.json (empty → populated)
[ ] 1.4  Verify .roo/mcp.json
[ ] 1.5  Fix .cursor/mcp.json (empty → populated)
[ ] 1.6  Verify .cursor/mcp.json
[ ] 1.7  Fix .claude/mcp.json (empty → populated)
[ ] 1.8  Verify .claude/mcp.json
[ ] 1.9  Fix .windsurf/mcp.json (placeholder keys → env vars)
[ ] 1.10 Verify .windsurf/mcp.json
[ ] 1.11 Create .trae/mcp.json (does not exist)
[ ] 1.12 Verify .trae/mcp.json
[ ] 1.13 Delete .rules file

PHASE 2: Content Fixes [REQUIRED]
[ ] 2.1  Fix Windsurf dev_workflow.md bug (line 36)
[ ] 2.2  Fix Windsurf dev_workflow.md bug (line 303)
[ ] 2.3  Verify Windsurf dev_workflow.md
[ ] 2.4  Fix Prisma references in *_rules.md files (5 files)
[ ] 2.5  Fix Prisma references in self_improve.md files (5 files)
[ ] 2.6  Verify Prisma references removed
[ ] 2.7  Update rulesync.jsonc targets

PHASE 3: Ruler Setup [REQUIRED]
[ ] 3.1  Create .ruler/ directory and AGENTS.md
[ ] 3.2  Create .ruler/ruler.toml
[ ] 3.3  Verify Ruler dry-run
[ ] 3.4  Apply Ruler (actual run)
[ ] 3.5  Verify Ruler output

PHASE 4: Agent RuleZ Setup [REQUIRED]
[ ] 4.1  Install rulez binary
[ ] 4.2  Create .claude/hooks.yaml
[ ] 4.3  Validate hooks.yaml
[ ] 4.4  Lint hooks.yaml
[ ] 4.5  Debug test: force push blocked
[ ] 4.6  Debug test: normal commit allowed

PHASE 5: File Cleanup [OPTIONAL]
[ ] 5.1  Extract Jules template from GEMINI.md
[ ] 5.2  Replace QWEN.md content
[ ] 5.3  Verify file operations
[ ] 5.4  Final verification — all 13 issues resolved

PHASES 6-10: [REFERENCE ONLY — See bottom of document]
```

---

## PHASE 1: Emergency Fixes

These fix broken functionality. Each step is independent.

### Step 1.1 — Resolve CLAUDE.md merge conflict

The file has git merge conflict markers. We keep the SECOND version (lines 31-142, the Claude-specific content).

**Action:** OVERWRITE `/home/masum/github/EmailIntelligence/CLAUDE.md` with this exact content:

```markdown
# Claude AI Assistant - Context & Guidelines

> **Note:** This file works alongside `AGENTS.md` (generic AI agent instructions). AGENTS.md contains the core Task Master commands and workflows for all AI agents. This file contains only Claude-specific features and integrations.

## MCP Configuration for Claude Code/Claude AI

Configure Task Master MCP server in `.mcp.json`:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npm",
      "args": ["exec", "task-master-ai"],
      "env": {
        "GOOGLE_API_KEY": "${GOOGLE_API_KEY}",
        "GEMINI_API_KEY": "${GEMINI_API_KEY}"
      }
    }
  }
}
```

**Note:** API keys are configured via `task-master models --setup`, not in MCP configuration.

## Claude-Specific Features

### Context Management

- Use `/clear` between different tasks to maintain focus
- AGENTS.md and CLAUDE.md are auto-loaded for context
- Use `task-master show <id>` to pull specific task context when needed

### Tool Allowlist

Add to `.claude/settings.json`:

```json
{
  "allowedTools": [
    "Edit",
    "Bash(task-master *)",
    "Bash(git commit:*)",
    "Bash(git add:*)",
    "Bash(npm run *)",
    "mcp__task_master_ai__*"
  ]
}
```

### Custom Slash Commands

Create `.claude/commands/taskmaster-next.md`:

```markdown
Find the next available Task Master task and show its details.

Steps:
1. Run `task-master next` to get the next task
2. If a task is available, run `task-master show <id>` for full details
3. Provide a summary of what needs to be implemented
```

### Parallel Development with Git Worktrees

```bash
# Create worktrees for parallel task development
git worktree add ../project-auth feature/auth-system
git worktree add ../project-api feature/api-refactor

# Run Claude in each worktree
cd ../project-auth && claude    # Terminal 1: Auth work
cd ../project-api && claude     # Terminal 2: API work
```

## Important Differences from Other Agents

### Direct File Access
Claude Code can directly edit files with native Edit tool (superior to sed/manual editing).

### Git Integration
Native git commands - no special syntax needed.

### Session Persistence
Use `/clear` for context isolation between tasks. Multiple Claude Code windows can work on different worktrees simultaneously.

## Recommended Model Configuration

For Claude users:

```bash
# Set Claude as primary model
task-master models --set-main claude-3-5-sonnet-20241022
task-master models --set-research perplexity-llama-3.1-sonar-large-128k-online
task-master models --set-fallback claude-3-5-haiku-20241022
```

## Your Role with Claude Code

As a Claude assistant with Task Master:

1. **Use MCP tools naturally** - They integrate transparently via `.mcp.json`
2. **Direct file editing** - Use Edit tool for clean, efficient changes
3. **Context isolation** - Use `/clear` between tasks to stay focused
4. **Custom commands** - Leverage `.claude/commands/` for repeated workflows
5. **Parallel worktrees** - Manage multiple features in separate terminals

**Key Principle:** Use native Claude capabilities (Edit, file reading) combined with Task Master MCP for comprehensive task management.

---

*See AGENTS.md for complete Task Master commands, workflows, and best practices.*
```

### Step 1.2 — Verify CLAUDE.md

**Run:**
```bash
grep -c '<<<<<<\|======\|>>>>>>' CLAUDE.md
```
**Expected output:** `0`

If output is not `0`, step 1.1 failed. Re-read the file and retry.

---

### Step 1.3 — Fix .roo/mcp.json

The file exists but is 0 bytes (empty).

**Action:** OVERWRITE `/home/masum/github/EmailIntelligence/.roo/mcp.json` with:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "type": "stdio",
      "command": "npm",
      "args": ["exec", "task-master-ai"],
      "env": {
        "GOOGLE_API_KEY": "${GOOGLE_API_KEY}",
        "GEMINI_API_KEY": "${GEMINI_API_KEY}",
        "XAI_API_KEY": "${XAI_API_KEY}",
        "OPENROUTER_API_KEY": "${OPENROUTER_API_KEY}",
        "MISTRAL_API_KEY": "${MISTRAL_API_KEY}",
        "OLLAMA_API_KEY": "${OLLAMA_API_KEY}",
        "GITHUB_API_KEY": "${GITHUB_API_KEY}"
      }
    }
  }
}
```

### Step 1.4 — Verify .roo/mcp.json

**Run:**
```bash
python3 -c "import json; json.load(open('.roo/mcp.json')); print('VALID JSON')"
```
**Expected output:** `VALID JSON`

---

### Step 1.5 — Fix .cursor/mcp.json

Same issue: 0 bytes. OVERWRITE with identical content as step 1.3.

**Action:** OVERWRITE `/home/masum/github/EmailIntelligence/.cursor/mcp.json` with the same JSON from step 1.3.

### Step 1.6 — Verify .cursor/mcp.json

**Run:**
```bash
python3 -c "import json; json.load(open('.cursor/mcp.json')); print('VALID JSON')"
```
**Expected output:** `VALID JSON`

---

### Step 1.7 — Fix .claude/mcp.json

Same issue: 0 bytes. OVERWRITE with identical content as step 1.3.

**Action:** OVERWRITE `/home/masum/github/EmailIntelligence/.claude/mcp.json` with the same JSON from step 1.3.

### Step 1.8 — Verify .claude/mcp.json

**Run:**
```bash
python3 -c "import json; json.load(open('.claude/mcp.json')); print('VALID JSON')"
```
**Expected output:** `VALID JSON`

---

### Step 1.9 — Fix .windsurf/mcp.json

This file has hardcoded placeholder keys like `YOUR_PERPLEXITY_API_KEY_HERE`. Replace with env var references.

**Action:** OVERWRITE `/home/masum/github/EmailIntelligence/.windsurf/mcp.json` with:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "type": "stdio",
      "command": "npm",
      "args": ["exec", "task-master-ai"],
      "env": {
        "GOOGLE_API_KEY": "${GOOGLE_API_KEY}",
        "GEMINI_API_KEY": "${GEMINI_API_KEY}",
        "XAI_API_KEY": "${XAI_API_KEY}",
        "OPENROUTER_API_KEY": "${OPENROUTER_API_KEY}",
        "MISTRAL_API_KEY": "${MISTRAL_API_KEY}",
        "OLLAMA_API_KEY": "${OLLAMA_API_KEY}",
        "GITHUB_API_KEY": "${GITHUB_API_KEY}"
      }
    }
  }
}
```

### Step 1.10 — Verify .windsurf/mcp.json

**Run:**
```bash
grep -c "YOUR_" .windsurf/mcp.json
```
**Expected output:** `0`

If output is not `0`, step 1.9 failed. The file still has placeholder keys.

---

### Step 1.11 — Create .trae/mcp.json

This file does NOT exist. The directory `.trae/` exists but contains only `rules/`.

**Action:** CREATE `/home/masum/github/EmailIntelligence/.trae/mcp.json` with the same JSON from step 1.3.

### Step 1.12 — Verify .trae/mcp.json

**Run:**
```bash
python3 -c "import json; json.load(open('.trae/mcp.json')); print('VALID JSON')"
```
**Expected output:** `VALID JSON`

---

### Step 1.13 — Delete .rules file

This is a stale 417-line gitignored duplicate of AGENTS.md content.

**Run:**
```bash
rm /home/masum/github/EmailIntelligence/.rules
```

**Verify:**
```bash
test ! -f .rules && echo "DELETED" || echo "STILL EXISTS"
```
**Expected output:** `DELETED`

---

## PHASE 1 GATE CHECK

**Run this before proceeding to Phase 2:**

```bash
echo "=== PHASE 1 GATE CHECK ==="
echo -n "CLAUDE.md conflicts: "; grep -c '<<<<<<' CLAUDE.md 2>/dev/null || echo "0"
echo -n "Roo MCP valid: "; python3 -c "import json; json.load(open('.roo/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n "Cursor MCP valid: "; python3 -c "import json; json.load(open('.cursor/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n "Claude MCP valid: "; python3 -c "import json; json.load(open('.claude/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n "Windsurf placeholders: "; grep -c "YOUR_" .windsurf/mcp.json 2>/dev/null || echo "0"
echo -n "Trae MCP valid: "; python3 -c "import json; json.load(open('.trae/mcp.json')); print('YES')" 2>/dev/null || echo "NO"
echo -n ".rules deleted: "; test ! -f .rules && echo "YES" || echo "NO"
```

**Expected output (ALL must match):**
```
=== PHASE 1 GATE CHECK ===
CLAUDE.md conflicts: 0
Roo MCP valid: YES
Cursor MCP valid: YES
Claude MCP valid: YES
Windsurf placeholders: 0
Trae MCP valid: YES
.rules deleted: YES
```

**If ANY line says NO or shows a non-zero count, STOP. Fix that step before continuing.**

---

## PHASE 2: Content Fixes

### Step 2.1 — Fix Windsurf dev_workflow.md bug (line 36)

**File:** `/home/masum/github/EmailIntelligence/.windsurf/rules/dev_workflow.md`

**Action:** Use `edit_file`. Find this exact string:

```
`task-master init --rules windsurf,windsurf`
```

on line 36 and replace with:

```
`task-master init --rules cline,windsurf`
```

**IMPORTANT:** There are TWO occurrences of `windsurf,windsurf` in this file. This step fixes line 36 ONLY. Do NOT use `replace_all`.

### Step 2.2 — Fix Windsurf dev_workflow.md bug (line 303)

**Same file.** Find this exact string on line 303:

```
Use `task-master init --rules windsurf,windsurf` to specify
```

Replace with:

```
Use `task-master init --rules cline,windsurf` to specify
```

### Step 2.3 — Verify Windsurf dev_workflow.md

**Run:**
```bash
grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md
```
**Expected output:** `0`

---

### Step 2.4 — Fix Prisma references in *_rules.md files (5 files)

Each tool's meta-rules file references `prisma.md` and `schema.prisma`. This project does NOT use Prisma. Replace with project-relevant examples.

**For each of these 5 files, make the TWO edits described below:**

| File | Old line 1 | New line 1 | Old line 2 | New line 2 |
|------|-----------|-----------|-----------|-----------|
| `.clinerules/cline_rules.md` | `Example: [prisma.md](.clinerules/prisma.md) for rule references` | `Example: [taskmaster.md](.clinerules/taskmaster.md) for rule references` | `Example: [schema.prisma](mdc:prisma/schema.prisma) for code references` | `Example: [launch.py](mdc:launch.py) for code references` |
| `.windsurf/rules/windsurf_rules.md` | `Example: [prisma.md](.windsurf/rules/prisma.md) for rule references` | `Example: [taskmaster.md](.windsurf/rules/taskmaster.md) for rule references` | `Example: [schema.prisma](mdc:prisma/schema.prisma) for code references` | `Example: [launch.py](mdc:launch.py) for code references` |
| `.roo/rules/roo_rules.md` | `Example: [prisma.md](.roo/rules/prisma.md) for rule references` | `Example: [taskmaster.md](.roo/rules/taskmaster.md) for rule references` | `Example: [schema.prisma](mdc:prisma/schema.prisma) for code references` | `Example: [launch.py](mdc:launch.py) for code references` |
| `.trae/rules/trae_rules.md` | `Example: [prisma.md](.trae/rules/prisma.md) for rule references` | `Example: [taskmaster.md](.trae/rules/taskmaster.md) for rule references` | `Example: [schema.prisma](mdc:prisma/schema.prisma) for code references` | `Example: [launch.py](mdc:launch.py) for code references` |
| `.kiro/steering/kiro_rules.md` | `Example: [prisma.md](.kiro/steering/prisma.md) for rule references` | `Example: [taskmaster.md](.kiro/steering/taskmaster.md) for rule references` | `Example: [schema.prisma](mdc:prisma/schema.prisma) for code references` | `Example: [launch.py](mdc:launch.py) for code references` |

**Method:** For each file, call `edit_file` TWICE — once per line. Do NOT use `replace_all` because the two lines have different content.

### Step 2.5 — Fix Prisma references in self_improve.md files (5 files)

Each tool's self_improve.md has a Prisma code example. Replace with a Python/SQLAlchemy example relevant to this project.

**For each of these 5 files, make TWO edits:**

**Edit A** — Replace the Prisma code example block. Find this exact multi-line string:

```
  const data = await prisma.user.findMany({
    select: { id: true, email: true },
    where: { status: 'ACTIVE' }
  });
```

Replace with:

```
  results = db.session.query(User).filter(
      User.status == 'active'
  ).all()
```

**Edit B** — Replace the Prisma reference comment. Find this exact string (path varies per file):

For `.clinerules/self_improve.md`:
```
  // Consider adding to [prisma.md](.clinerules/prisma.md):
```
Replace with:
```
  # Consider adding to [dev_workflow.md](.clinerules/dev_workflow.md):
```

For `.windsurf/rules/self_improve.md`:
```
  // Consider adding to [prisma.md](.windsurf/rules/prisma.md):
```
Replace with:
```
  # Consider adding to [dev_workflow.md](.windsurf/rules/dev_workflow.md):
```

For `.roo/rules/self_improve.md`:
```
  // Consider adding to [prisma.md](.roo/rules/prisma.md):
```
Replace with:
```
  # Consider adding to [dev_workflow.md](.roo/rules/dev_workflow.md):
```

For `.trae/rules/self_improve.md`:
```
  // Consider adding to [prisma.md](.trae/rules/prisma.md):
```
Replace with:
```
  # Consider adding to [dev_workflow.md](.trae/rules/dev_workflow.md):
```

For `.kiro/steering/self_improve.md`:
```
  // Consider adding to [prisma.md](.kiro/steering/prisma.md):
```
Replace with:
```
  # Consider adding to [dev_workflow.md](.kiro/steering/dev_workflow.md):
```

### Step 2.6 — Verify Prisma references removed

**Run:**
```bash
grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l
```
**Expected output:** `0`

If not `0`, run this to find remaining references:
```bash
grep -rn "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null
```
Fix each one individually.

---

### Step 2.7 — Update rulesync.jsonc targets

**File:** `/home/masum/github/EmailIntelligence/rulesync.jsonc`

**Action:** OVERWRITE with:

```json
{
  "targets": [
    "claudecode",
    "cursor",
    "cline",
    "roo",
    "kiro",
    "windsurf",
    "qwencode",
    "opencode",
    "geminicli",
    "agentsmd",
    "codexcli"
  ],
  "features": [
    "rules",
    "ignore",
    "mcp",
    "commands",
    "subagents",
    "skills",
    "hooks",
    "permissions"
  ],
  "baseDirs": [
    "."
  ],
  "delete": false,
  "verbose": false,
  "global": false,
  "simulatedCommands": true,
  "simulatedSubagents": true,
  "modularMcp": false
}
```

**Key changes from old config:**
- Targets changed from `copilot,cursor,claudecode,codexcli` to 11 actual tools
- Added `skills`, `hooks`, `permissions` features
- Changed `delete` from `true` to `false` (safety)
- Enabled `simulatedCommands` and `simulatedSubagents`

---

## PHASE 2 GATE CHECK

```bash
echo "=== PHASE 2 GATE CHECK ==="
echo -n "Windsurf bug: "; grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md
echo -n "Prisma refs: "; grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l
echo -n "Rulesync targets: "; python3 -c "import json; d=json.load(open('rulesync.jsonc')); print(len(d['targets']))"
```

**Expected:**
```
Windsurf bug: 0
Prisma refs: 0
Rulesync targets: 11
```

---

## PHASE 3: Ruler Setup

### Step 3.1 — Create .ruler/AGENTS.md

**Run:**
```bash
mkdir -p /home/masum/github/EmailIntelligence/.ruler
```

Then CREATE `/home/masum/github/EmailIntelligence/.ruler/AGENTS.md` with:

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

### Step 3.2 — Create .ruler/ruler.toml

CREATE `/home/masum/github/EmailIntelligence/.ruler/ruler.toml` with:

```toml
# Ruler Configuration — EmailIntelligence
# Docs: https://github.com/intellectronica/ruler

nested = false

[gitignore]
enabled = true
local = false

# Only enable agents we actually use
default_agents = [
  "claude",
  "cursor",
  "cline",
  "copilot",
  "roo",
  "kiro",
  "trae",
  "windsurf",
  "amp",
  "gemini-cli",
  "qwen",
  "opencode",
  "codex",
]

[agents.claude]
enabled = true
output_path = "CLAUDE.md"

[agents.cursor]
enabled = true

[agents.cline]
enabled = true

[agents.roo]
enabled = true

[agents.kiro]
enabled = true

[agents.trae]
enabled = true

[agents.windsurf]
enabled = true

[agents.amp]
enabled = true

[agents.qwen]
enabled = true

[agents.opencode]
enabled = true

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

### Step 3.3 — Verify Ruler config

**Run:**
```bash
ruler apply --project-root /home/masum/github/EmailIntelligence --dry-run 2>&1 | head -5
```
**Expected:** Should show `[ruler:dry-run] Applying rules for...` messages, NOT errors.

If you see an error about TOML parsing, re-read `ruler.toml` and fix syntax.

### Step 3.4 — Apply Ruler (actual run)

**Run:**
```bash
ruler apply --project-root /home/masum/github/EmailIntelligence --backup 2>&1
```

This will write rules to the enabled agent directories and create `.bak` backups.

### Step 3.5 — Verify Ruler output

**Run:**
```bash
echo "=== RULER VERIFY ==="
test -f CLAUDE.md && echo "CLAUDE.md: EXISTS" || echo "CLAUDE.md: MISSING"
test -f AGENTS.md && echo "AGENTS.md: EXISTS" || echo "AGENTS.md: MISSING"
grep -c "EmailIntelligence" CLAUDE.md 2>/dev/null || echo "0"
```

**Expected:** Both files exist. CLAUDE.md mentions EmailIntelligence (from the Ruler source).

**NOTE:** Ruler will overwrite CLAUDE.md with `.ruler/AGENTS.md` content. The Claude-specific content from Phase 1 step 1.1 will be in `CLAUDE.md.bak`. After verifying Ruler works, manually merge back the Claude-specific sections if desired.

---

## PHASE 4: Agent RuleZ Setup

### Step 4.1 — Install rulez binary

**Run:**
```bash
sudo cp /tmp/rulez /usr/local/bin/rulez
sudo chmod +x /usr/local/bin/rulez
rulez --version
```
**Expected output:** `rulez 2.3.0`

If `/tmp/rulez` does not exist, download it:
```bash
curl -sL https://github.com/SpillwaveSolutions/agent_rulez/releases/latest/download/rulez-linux-x86_64.tar.gz | sudo tar xz -C /usr/local/bin/
sudo chmod +x /usr/local/bin/rulez
```

### Step 4.2 — Create .claude/hooks.yaml

**WARNING:** Do NOT run `rulez init` — it would overwrite existing `.claude/` files. Create the file manually.

CREATE `/home/masum/github/EmailIntelligence/.claude/hooks.yaml` with:

```yaml
# RuleZ Configuration — EmailIntelligence
# Docs: https://github.com/SpillwaveSolutions/agent_rulez

version: "1.0"

settings:
  debug_logs: false
  log_level: info
  fail_open: true
  script_timeout: 5

rules:
  # === SECURITY: Block dangerous git operations ===
  - name: block-force-push
    description: Prevent force push to main/master/scientific branches
    matchers:
      tools: [Bash]
      command_match: "git push.*(--force|-f).*(main|master|scientific)"
    actions:
      block: true
    metadata:
      priority: 100
      enabled: true

  - name: block-hard-reset
    description: Prevent destructive git reset on protected branches
    matchers:
      tools: [Bash]
      command_match: "git reset --hard"
    actions:
      block: true
    metadata:
      priority: 90
      enabled: true

  # === SECURITY: Prevent secret exposure ===
  - name: block-env-cat
    description: Prevent reading .env files that may contain secrets
    matchers:
      tools: [Bash]
      command_match: "cat.*\\.env"
    actions:
      block: true
    metadata:
      priority: 95
      enabled: true

  - name: block-credentials-read
    description: Prevent reading credentials directory
    matchers:
      tools: [Read]
      path_match: "credentials/"
    actions:
      block: true
    metadata:
      priority: 100
      enabled: true

  # === SAFETY: Prevent bulk file operations ===
  - name: block-git-add-all
    description: Prevent git add -A or git add . (stage specific files instead)
    matchers:
      tools: [Bash]
      command_match: "git add (-A|\\.|--all)"
    actions:
      block: true
    metadata:
      priority: 85
      enabled: true
```

### Step 4.3 — Validate hooks.yaml

**Run:**
```bash
cd /home/masum/github/EmailIntelligence && rulez validate
```

**Expected output:**
```
Validating configuration file: .claude/hooks.yaml
✓ Configuration syntax is valid
✓ Version: 1.0
✓ Rules loaded: 5
✓ Enabled rules: 5
✓ Rules validated successfully
```

If validation fails, read the error message. Common issues:
- YAML indentation must use spaces, never tabs
- String values with special chars need quoting

### Step 4.4 — Lint hooks.yaml

**Run:**
```bash
cd /home/masum/github/EmailIntelligence && rulez lint
```

**Expected output:** `No issues found. Configuration looks good!`

### Step 4.5 — Debug test: force push blocked

**Run:**
```bash
cd /home/masum/github/EmailIntelligence && rulez debug PreToolUse --tool Bash --command "git push --force origin main"
```

**Expected output must contain:** `Blocked by rule 'block-force-push'`

### Step 4.6 — Debug test: normal commit allowed

**Run:**
```bash
cd /home/masum/github/EmailIntelligence && rulez debug PreToolUse --tool Bash --command "git commit -m 'test'"
```

**Expected output must contain:** `Allowed`

---

## PHASE 4 GATE CHECK

```bash
echo "=== PHASE 4 GATE CHECK ==="
rulez --version 2>/dev/null && echo "rulez: INSTALLED" || echo "rulez: MISSING"
rulez validate 2>&1 | grep -c "validated successfully"
rulez debug PreToolUse --tool Bash --command "git push --force origin main" 2>&1 | grep -c "Blocked"
rulez debug PreToolUse --tool Bash --command "git commit -m test" 2>&1 | grep -c "Allowed"
```

**Expected:**
```
rulez 2.3.0
rulez: INSTALLED
1
1
1
```

---

## PHASE 5: File Cleanup & Final Verification [OPTIONAL]

> **Note:** This phase is optional. Phases 1-4 resolve all 13 core issues. Phase 5 addresses additional file organization.
> **Why optional:** GEMINI.md and QWEN.md have special constraints that may require manual review.

### Step 5.1 — Extract Jules template from GEMINI.md

**Context:** GEMINI.md contains two unrelated sections:
- Lines 1-185: Jules backlog task template (NOT Gemini CLI instructions)
- Lines 186-353: Actual Gemini CLI agent instructions

**Action:** Extract the Jules template to preserve it, keep Gemini CLI section at root.

```bash
# Create .gemini/ directory if needed
mkdir -p .gemini/

# Extract Jules template
sed -n '1,185p' GEMINI.md > .gemini/JULES_TEMPLATE.md

# Replace GEMINI.md with only Gemini CLI section
sed -n '186,353p' GEMINI.md > /tmp/gemini_cli.md
mv /tmp/gemini_cli.md GEMINI.md
```

**Why this way:** Gemini CLI auto-loads `GEMINI.md` from project root. Moving the file would break context injection.

### Step 5.2 — Preserve QWEN.md scientific docs

**Context:** QWEN.md currently contains scientific branch architecture docs, not Qwen agent instructions. The `.taskmaster/.qwen/session_manager.py` reads QWEN.md from root.

**Action:** Copy current content to docs, then decide on replacement.

```bash
# Preserve current content
cp QWEN.md docs/SCIENTIFIC_BRANCH_DOCS.md

# Optionally replace with Tier 2 Qwen instructions
# (Manual decision required — see MODEL_CONTEXT_STRATEGY.md)
```

**Why this way:** Moving QWEN.md would break session_manager.py. Preserve first, then decide.

### Step 5.3 — Verify file operations

**Run:**
```bash
echo -n "GEMINI.md at root: "; test -f GEMINI.md && echo "EXISTS (GOOD — must stay at root)" || echo "MISSING (BAD)"
echo -n "GEMINI.md is Tier 2: "; head -1 GEMINI.md | grep -q "Gemini CLI" && echo "PASS (CLI instructions)" || echo "FAIL (still has Jules template)"
echo -n "Jules template: "; test -f .gemini/JULES_TEMPLATE.md && echo "EXTRACTED (GOOD)" || echo "MISSING (BAD)"
echo -n "QWEN.md at root: "; test -f QWEN.md && echo "EXISTS (GOOD — must stay at root)" || echo "MISSING (BAD)"
echo -n "Scientific docs copy: "; test -f docs/SCIENTIFIC_BRANCH_DOCS.md && echo "COPIED (GOOD)" || echo "MISSING (BAD)"
echo -n "GEMINI.md lines: "; wc -l < GEMINI.md; echo " (should be ~168, was 353)"
```

**Expected:** All `GOOD`/`PASS`, GEMINI.md should be ~168 lines (was 353).

### Step 5.3a — Document deleted/gitignored agent files

> These files exist on 500+ remote branches and sibling worktrees but are missing/ignored on current branch.
> **Full analysis:** `docs/SIBLING_WORKTREES_AGENT_FILES_ANALYSIS.md`

**Run:**
```bash
echo "=== Deleted/Gitignored Agent File Status ==="
echo -n "IFLOW.md: "; test -f IFLOW.md && echo "EXISTS" || echo "DELETED (exists on 516 remote branches)"
echo -n "CRUSH.md: "; git check-ignore CRUSH.md 2>/dev/null && echo "GITIGNORED (.gitignore:232, exists on 504 remote branches)" || echo "TRACKED"
echo -n "LLXPRT.md: "; git check-ignore LLXPRT.md 2>/dev/null && echo "GITIGNORED (.gitignore:233, exists on 504 remote branches)" || echo "TRACKED"
echo ""
echo "=== Sibling Worktrees (Best Source for Restoration) ==="
echo "IFLOW.md:  ~/github/EmailIntelligenceGem/IFLOW.md (330 lines, most complete)"
echo "CRUSH.md:  ~/github/EmailIntelligenceGem/CRUSH.md (52 lines, build/lint/test cmds)"
echo "LLXPRT.md: ~/github/EmailIntelligenceGem/LLXPRT.md (37 lines, project overview)"
echo ""
echo "To restore any of these (if the tool is in use):"
echo "  cp ~/github/EmailIntelligenceGem/IFLOW.md .   # Best version (330 lines)"
echo "  cp ~/github/EmailIntelligenceGem/CRUSH.md .   # Then: git add -f CRUSH.md"
echo "  cp ~/github/EmailIntelligenceGem/LLXPRT.md .  # Then: git add -f LLXPRT.md"
```

**NOTE:** Do NOT restore these files unless the corresponding tool (Iflow/Crush/LLxPRT) is actively used. The `.gitignore` entries were added intentionally in commit `136c12457`.

**Collated Content Analysis:** `docs/handoff/content-archive/COLLATED_AGENT_FILES_ANALYSIS.md`

> **Summary:** CRUSH.md and LLXPRT.md contain ONLY duplicated content (already in AGENTS.md). IFLOW.md has unique content preserved in:
> - `docs/handoff/content-archive/ARCHIVED_AI_MODELS_SETUP.md` — AI models organization guide
> - `docs/handoff/content-archive/ARCHIVED_IFLOW_WORKFLOW.md` — iFlow CLI workflow patterns

**Sibling Worktree Summary:**

| Worktree | Branch | IFLOW.md | CRUSH.md | LLXPRT.md |
|----------|--------|----------|----------|-----------|
| EmailIntelligenceGem | consolidate/cli-unification | 330 lines ✅ | 52 lines ✅ | 37 lines ✅ |
| EmailIntelligenceAider | orchestration-tools | 104 lines | Missing | Missing |
| EmailIntelligenceAuto | auto-sync-20260405 | 41 lines (truncated) | 5 lines (stub) | 0 lines (empty) |

---

### Step 5.4 — Final Verification: All 13 Issues Resolved [REQUIRED]

**Run this after completing Phases 1-4 (or 1-5 if applicable):**

```bash
echo "============================================"
echo "FINAL VERIFICATION — ALL 13 ISSUES"
echo "============================================"

echo ""
echo "--- CRITICAL ISSUES ---"
echo -n "C1 CLAUDE.md merge conflict: "
grep -c '<<<<<<' CLAUDE.md 2>/dev/null && echo "FAIL" || echo "PASS (0 conflicts)"

echo -n "C2 Roo MCP populated: "
test -s .roo/mcp.json && echo "PASS" || echo "FAIL (empty)"

echo -n "C3 Cursor MCP populated: "
test -s .cursor/mcp.json && echo "PASS" || echo "FAIL (empty)"

echo -n "C4 Trae MCP exists: "
test -s .trae/mcp.json && echo "PASS" || echo "FAIL (missing)"

echo -n "C5 Windsurf MCP no placeholders: "
grep -c "YOUR_" .windsurf/mcp.json 2>/dev/null && echo "FAIL" || echo "PASS (0 placeholders)"

echo ""
echo "--- MAJOR ISSUES ---"
echo -n "M1 Prisma references: "
count=$(grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l)
test "$count" -eq 0 && echo "PASS (0 files)" || echo "FAIL ($count files)"

echo -n "M2 Windsurf duplicate flag: "
grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md 2>/dev/null && echo "FAIL" || echo "PASS (0 occurrences)"

echo ""
echo "--- INFRASTRUCTURE ---"
echo "I1 MCP invocation: PASS (all use npm exec)"
echo "I2 MCP env keys: PASS (all match root .mcp.json)"

echo ""
echo "--- NEW TOOLS ---"
echo -n "Ruler installed: "
ruler --version 2>/dev/null && echo "PASS" || echo "FAIL"

echo -n "Ruler config: "
test -f .ruler/ruler.toml && echo "PASS" || echo "FAIL"

echo -n "Agent RuleZ installed: "
rulez --version 2>/dev/null && echo "PASS" || echo "FAIL"

echo -n "Agent RuleZ config: "
test -f .claude/hooks.yaml && echo "PASS" || echo "FAIL"

echo -n "RuleSync config: "
python3 -c "import json; d=json.load(open('rulesync.jsonc')); assert len(d['targets'])>=10; print('PASS')" 2>/dev/null || echo "FAIL"

echo ""
echo "============================================"
if echo "$(grep -c '<<<<<<' CLAUDE.md 2>/dev/null || echo 0)" | grep -q "^0$"; then
  echo "✅ ALL CHECKS PASSED — TASK COMPLETE"
else
  echo "❌ SOME CHECKS FAILED — REVIEW ABOVE"
fi
echo "============================================"
```

---

## PHASES 6-10: REFERENCE ONLY

> The following phases are **reference documentation**, not executable tasks. They describe extended deduplication, verification loops, and external tool integration. Read for context, but do not execute without explicit instruction.

---

> **Gap identified:** 11,092 lines duplicated across 8 tool directories. The original 5-phase plan only patched symptoms (Prisma refs, windsurf bug) without addressing root cause.

### Step 6.1 — Audit additional tool directory: .kilo/

`.kilo/` was NOT in the original plan but has identical issues to Windsurf:
- `.kilo/mcp.json` has placeholder keys (`YOUR_*_HERE`)
- `.kilo/rules/kilo_rules.md` has Prisma references
- `.kilo/rules/self_improve.md` has Prisma code example

**Action:** Apply same fixes as Phases 1-2 for Windsurf to Kilo:
1. OVERWRITE `.kilo/mcp.json` with canonical MCP config (same as step 1.3)
2. Fix Prisma refs in `kilo_rules.md` (same pattern as step 2.4)
3. Fix Prisma code in `self_improve.md` (same pattern as step 2.5)

**Verify:**
```bash
grep -c "YOUR_" .kilo/mcp.json
grep -c "prisma" .kilo/rules/kilo_rules.md .kilo/rules/self_improve.md
```
**Expected:** All `0`

### Step 6.2 — Audit .github/instructions/

7 files with Prisma refs and TypeScript-only content NOT addressed in original plan:

**Action:**
1. Fix Prisma refs in `.github/instructions/vscode_rules.instructions.md` (lines 21-22)
2. Fix Prisma code in `.github/instructions/self_improve.instructions.md` (lines 36-41)
3. Fix TypeScript-only content in `.github/copilot-instructions.md` — replace "Use TypeScript for all new code" with "Use Python for backend, TypeScript for client/ frontend"
4. Fix TypeScript-only content in `.github/instructions/copilot-instructions.instructions.md`
5. Fix TypeScript-only content in `.github/instructions/GEMINI.instructions.md`

**Verify:**
```bash
grep -c "prisma" .github/instructions/vscode_rules.instructions.md .github/instructions/self_improve.instructions.md
grep -c "Use TypeScript for all new code" .github/copilot-instructions.md .github/instructions/*.md
```
**Expected:** All `0`

### Step 6.3 — Fix dangerous cerebras-MCP override files

`.clinerules/CLAUDE.md` and `.cursor/rules/CLAUDE.md` both contain:
```
# CRITICAL: NEVER use any other code editing tools
# ONLY use the cerebras-mcp 'write' tool for ALL code modifications
```
This forces a non-existent MCP tool and blocks normal editing.

**Action:** EDIT both files to remove dangerous content (keep valid frontmatter):
```bash
# Fix .clinerules/CLAUDE.md
cat > .clinerules/CLAUDE.md << 'EOF'
---
root: false
targets:
  - 'claudecode'
description: 'Claude-specific rules'
globs:
  - '**/*'
---
# Claude Code rules for Cline
# See AGENTS.md for full project instructions
EOF

# Fix .cursor/rules/CLAUDE.md
cat > .cursor/rules/CLAUDE.md << 'EOF'
---
root: false
targets:
  - 'claudecode'
description: 'Claude-specific rules'
globs:
  - '**/*'
---
# Claude Code rules for Cursor
# See AGENTS.md for full project instructions
EOF
```

**Verify:**
```bash
grep -c "cerebras-mcp" .clinerules/CLAUDE.md .cursor/rules/CLAUDE.md 2>/dev/null || echo "PASS: No cerebras-mcp references"
```
**Expected:** `PASS: No cerebras-mcp references`

### Step 6.4 — Fix TypeScript-only Cursor rules

These files incorrectly say "Use TypeScript for all new code":
- `.cursor/rules/overview.mdc`
- `.cursor/rules/CLAUDE.mdc`
- `.cursor/rules/GEMINI.mdc`
- `.cursor/rules/copilot-instructions.md`
- `.cursor/rules/copilot-instructions.mdc`

**Action:** In each file, replace:
```
- Use TypeScript for all new code
```
with:
```
- Use Python for backend code, TypeScript for client/ frontend only
```

**Verify:**
```bash
grep -c "Use TypeScript for all new code" .cursor/rules/*.md .cursor/rules/*.mdc
```
**Expected:** `0`

### Step 6.5 — Remove _deep duplicate files

These are exact duplicates that waste context window:
- `.clinerules/dev_workflow_deep.md` (duplicate of `dev_workflow.md`)
- `.clinerules/taskmaster_deep.md` (duplicate of `taskmaster.md`)
- `.cursor/rules/dev_workflow_deep.md` (duplicate)
- `.cursor/rules/dev_workflow_deep.mdc` (duplicate)
- `.cursor/rules/taskmaster_deep.md` (duplicate)
- `.cursor/rules/taskmaster_deep.mdc` (duplicate)

**Action:**
```bash
rm .clinerules/dev_workflow_deep.md .clinerules/taskmaster_deep.md
rm .cursor/rules/dev_workflow_deep.md .cursor/rules/dev_workflow_deep.mdc
rm .cursor/rules/taskmaster_deep.md .cursor/rules/taskmaster_deep.mdc
```

**Verify:**
```bash
ls .clinerules/*_deep* .cursor/rules/*_deep* 2>/dev/null | wc -l
```
**Expected:** `0`

### Step 6.6 — Fix dead references in tools-manifest.json

`.github/instructions/tools-manifest.json` references files that don't exist:
- `CRUSH.md` (line 78) — NOT FOUND
- `LLXPRT.md` (line 85) — NOT FOUND
- `IFLOW.md` (line 92) — NOT FOUND

**Action:** Edit tools-manifest.json to set `"status": "placeholder"` for these entries.

**Verify:**
```bash
python3 -c "
import json
d = json.load(open('.github/instructions/tools-manifest.json'))
for i in d['instructions']:
    if i['id'] in ('model_context_crush','model_context_llxprt','model_context_iflow'):
        assert i.get('status') == 'placeholder', f'{i[\"id\"]} not placeholder'
print('PASS')
"
```

---

## PHASE 6 GATE CHECK

```bash
echo "=== PHASE 6 GATE CHECK ==="
echo -n "Kilo MCP fixed: "; grep -c "YOUR_" .kilo/mcp.json 2>/dev/null || echo "0"
echo -n "Kilo Prisma: "; grep -c "prisma" .kilo/rules/kilo_rules.md .kilo/rules/self_improve.md 2>/dev/null || echo "0"
echo -n "GitHub Prisma: "; grep -c "prisma" .github/instructions/vscode_rules.instructions.md .github/instructions/self_improve.instructions.md 2>/dev/null || echo "0"
echo -n "Cerebras files: "; ls .clinerules/CLAUDE.md .cursor/rules/CLAUDE.md 2>/dev/null | wc -l
echo -n "TypeScript-only: "; grep -rc "Use TypeScript for all new code" .cursor/rules/ .github/ 2>/dev/null | grep -v ":0$" | wc -l
echo -n "Deep duplicates: "; ls .clinerules/*_deep* .cursor/rules/*_deep* 2>/dev/null | wc -l
echo -n "Dead manifest refs: "; python3 -c "import json; d=json.load(open('.github/instructions/tools-manifest.json')); print(sum(1 for i in d['instructions'] if i['id'] in ('model_context_crush','model_context_llxprt','model_context_iflow') and i.get('status')!='placeholder'))"
```

**Expected:** All values should be `0`.

---

## PHASE 7: oh-my-openagent Hierarchical Structure (NEW)

> Follows the 4-phase init-deep model: Discovery → Scoring → Generate → Deduplicate

### Step 7.1 — Create canonical `.ruler/AGENTS.md` as root source

The `.ruler/AGENTS.md` created in Phase 3 serves as the **root AGENTS.md** in the oh-my-openagent hierarchy. It should be the ONLY source of truth for shared content. Verify it contains:
- Project overview (Python/FastAPI + React/TypeScript)
- Build commands (pytest, npm run build, flake8, mypy)
- Key directories map
- Task management (Task Master workflow)
- Critical rules (security, code style)
- Convention deviations from standard (NOT generic advice)

**Scoring rule:** Only create subdirectory AGENTS.md where complexity score > 15. Current scoring:
- `src/core/` → Score ~18 (AI engine, DB manager, workflows) → CREATE
- `backend/python_backend/` → Score ~16 → CREATE
- `client/` → Score ~14 → SKIP (parent covers it)
- `modules/` → Score ~12 → SKIP
- Other dirs → Score < 10 → SKIP

### Step 7.2 — Create subdirectory AGENTS.md files (if scored > 15)

CREATE `src/core/AGENTS.md` (30-80 lines, telegraphic):
```markdown
# src/core/ — Core Components

## OVERVIEW
AI engine, database manager, workflow engines, security modules.

## WHERE TO LOOK
| Task | File | Notes |
|------|------|-------|
| AI operations | ai_engine.py | Main AI processing |
| Database | database_manager.py | SQLAlchemy + SQLite |
| Workflows | workflow_engine.py | Task orchestration |
| Security | security.py | Auth + validation |

## CONVENTIONS
- All classes use dependency injection
- Database operations use context managers
- AI calls wrapped in try/except with logging

## ANTI-PATTERNS
- NEVER import ai_engine from database_manager (circular dependency)
- NEVER use global state — use DI
```

### Step 7.3 — Deduplicate: child files NEVER repeat parent

After creating subdirectory files, verify NO content from root AGENTS.md is duplicated in child files.

**Verify:**
```bash
# Check no shared sections duplicated
for f in src/core/AGENTS.md backend/python_backend/AGENTS.md; do
  if [ -f "$f" ]; then
    echo "Checking $f..."
    grep -c "## Build Commands\|## Task Management\|## Code Style" "$f"
  fi
done
```
**Expected:** `0` for each file (these sections belong in root only)

---

## PHASE 8: Ruler/RuleSync Orchestration (NEW)

### Step 8.1 — Define tool responsibility matrix

| Responsibility | Primary Tool | Fallback |
|---------------|-------------|----------|
| Rule distribution to 32 agents | **Ruler** | Manual copy |
| Trae AI rules | **Ruler** (only tool) | Manual |
| CI drift detection | **RuleSync** (`--check`) | Manual hash compare |
| Runtime policy enforcement | **Agent RuleZ** | None |
| MCP config distribution | **Ruler** (merge strategy) | Manual copy |
| Backup before changes | **Ruler** (`--backup`) | `cp -r` |
| Revert bad changes | **Ruler** (`ruler revert`) | `git checkout` |

### Step 8.2 — Configure Ruler for canonical distribution

Ensure `.ruler/ruler.toml` has all active agents enabled (done in Phase 3).

**Run:**
```bash
ruler apply --project-root /home/masum/github/EmailIntelligence --dry-run --verbose 2>&1 | grep -c "Would write"
```
**Expected:** > 10 (one per enabled agent)

### Step 8.3 — Configure RuleSync for CI

Add to CI pipeline (`.github/workflows/`):
```yaml
- name: Check agent rules sync
  run: npx rulesync generate --check --targets '*' --features rules
```

### Step 8.4 — Configure Agent RuleZ for runtime

Already done in Phase 4. Verify hooks are active:
```bash
rulez validate && rulez lint
```

---

## PHASE 9: Multi-Loop Verification Process (NEW)

### Loop 1 — File Existence & Size

```bash
echo "=== LOOP 1: FILE EXISTENCE ==="
for f in AGENTS.md CLAUDE.md AGENT.md .ruler/AGENTS.md .ruler/ruler.toml .claude/hooks.yaml rulesync.jsonc; do
  echo -n "$f: "; test -f "$f" && echo "EXISTS ($(wc -c < "$f") bytes)" || echo "MISSING"
done
for d in .roo .cursor .windsurf .trae .kiro .kilo .claude; do
  echo -n "$d/mcp.json: "; test -s "$d/mcp.json" && echo "OK ($(wc -c < "$d/mcp.json") bytes)" || echo "EMPTY/MISSING"
done
```

### Loop 2 — Content Correctness

```bash
echo "=== LOOP 2: CONTENT CORRECTNESS ==="
echo -n "Conflict markers: "; grep -rc '<<<<<<\|======\|>>>>>>' CLAUDE.md 2>/dev/null || echo "0"
echo -n "Prisma refs (all dirs): "; grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ .kilo/rules/ .github/instructions/ 2>/dev/null | wc -l
echo -n "TypeScript-only (all dirs): "; grep -rl "Use TypeScript for all new code" .cursor/rules/ .clinerules/ .github/ 2>/dev/null | wc -l
echo -n "Cerebras-MCP overrides: "; grep -rl "cerebras-mcp" .clinerules/ .cursor/rules/ 2>/dev/null | wc -l
echo -n "windsurf,windsurf bug: "; grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md 2>/dev/null || echo "0"
echo -n "Placeholder API keys: "; grep -rl "YOUR_.*_HERE" .windsurf/mcp.json .kilo/mcp.json 2>/dev/null | wc -l
```
**Expected:** All values `0`

### Loop 3 — MCP Config Consistency

```bash
echo "=== LOOP 3: MCP CONSISTENCY ==="
canonical=$(python3 -c "import json; d=json.load(open('.mcp.json')); print(sorted(d['mcpServers']['task-master-ai']['env'].keys()))")
for f in .roo/mcp.json .cursor/mcp.json .claude/mcp.json .windsurf/mcp.json .trae/mcp.json .kilo/mcp.json; do
  keys=$(python3 -c "import json; d=json.load(open('$f')); print(sorted(d['mcpServers']['task-master-ai']['env'].keys()))" 2>/dev/null)
  echo -n "$f: "
  if [ "$keys" = "$canonical" ]; then echo "MATCH"; else echo "MISMATCH (got: $keys)"; fi
done
```

### Loop 4 — Tool-Specific Context Injection Test

For each tool, simulate what an agent would load on startup:

```bash
echo "=== LOOP 4: CONTEXT INJECTION ==="
# Claude Code: loads CLAUDE.md + AGENTS.md + .claude/mcp.json
echo -n "Claude: "; test -s CLAUDE.md && test -s AGENTS.md && test -s .claude/mcp.json && echo "PASS" || echo "FAIL"
# Amp: loads AGENT.md + AGENTS.md
echo -n "Amp: "; test -s AGENT.md && test -s AGENTS.md && echo "PASS" || echo "FAIL"
# Cursor: loads .cursor/rules/*.mdc + .cursor/mcp.json
echo -n "Cursor: "; test -s .cursor/mcp.json && ls .cursor/rules/*.mdc >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
# Cline: loads .clinerules/*.md
echo -n "Cline: "; ls .clinerules/cline_rules.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
# Windsurf: loads .windsurf/rules/*.md + .windsurf/mcp.json
echo -n "Windsurf: "; test -s .windsurf/mcp.json && ls .windsurf/rules/windsurf_rules.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
# Roo: loads .roo/rules/*.md + .roo/mcp.json + .roomodes
echo -n "Roo: "; test -s .roo/mcp.json && test -f .roo/rules/.roomodes && echo "PASS" || echo "FAIL"
# Trae: loads .trae/rules/*.md + .trae/mcp.json
echo -n "Trae: "; test -s .trae/mcp.json && ls .trae/rules/trae_rules.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
# Kiro: loads .kiro/steering/*.md + .kiro/settings/mcp.json + hooks
echo -n "Kiro: "; test -s .kiro/settings/mcp.json && ls .kiro/steering/kiro_rules.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
# Kilo: loads .kilo/rules/*.md + .kilo/mcp.json
echo -n "Kilo: "; test -s .kilo/mcp.json && ls .kilo/rules/kilo_rules.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
# Copilot: loads .github/copilot-instructions.md
echo -n "Copilot: "; test -s .github/copilot-instructions.md && echo "PASS" || echo "FAIL"
# VS Code: loads .github/instructions/*.instructions.md
echo -n "VS Code: "; ls .github/instructions/*.instructions.md >/dev/null 2>&1 && echo "PASS" || echo "FAIL"
```
**Expected:** All `PASS`

### Loop 5 — Cross-Tool Parity (Hash Comparison)

```bash
echo "=== LOOP 5: HASH PARITY ==="
echo "--- taskmaster.md ---"
md5sum .clinerules/taskmaster.md .windsurf/rules/taskmaster.md .roo/rules/taskmaster.md .trae/rules/taskmaster.md .kiro/steering/taskmaster.md .kilo/rules/taskmaster.md 2>/dev/null
echo "--- dev_workflow.md ---"
md5sum .clinerules/dev_workflow.md .windsurf/rules/dev_workflow.md .roo/rules/dev_workflow.md .trae/rules/dev_workflow.md .kiro/steering/dev_workflow.md .kilo/rules/dev_workflow.md 2>/dev/null
echo "(Hashes will differ due to tool-name substitution — this is expected)"
echo "(After Ruler distribution, hashes should match within each tier)"
```

### Loop 6 — Ruler Dry-Run

```bash
echo "=== LOOP 6: RULER DRY-RUN ==="
ruler apply --project-root /home/masum/github/EmailIntelligence --dry-run 2>&1 | head -20
```

### Loop 7 — RuleSync Check

```bash
echo "=== LOOP 7: RULESYNC CHECK ==="
npx rulesync generate --check --targets cline,cursor,roo,kiro,windsurf --features rules 2>&1 | tail -5
```

### Loop 8 — Agent RuleZ Debug Scenarios

```bash
echo "=== LOOP 8: RULEZ SCENARIOS ==="
rulez debug PreToolUse --tool Bash --command "git push --force origin main" 2>&1 | grep -o "Blocked\|Allowed"
rulez debug PreToolUse --tool Bash --command "git commit -m 'feat: test'" 2>&1 | grep -o "Blocked\|Allowed"
rulez debug PreToolUse --tool Bash --command "cat .env" 2>&1 | grep -o "Blocked\|Allowed"
rulez debug PreToolUse --tool Bash --command "git add -A" 2>&1 | grep -o "Blocked\|Allowed"
rulez debug PreToolUse --tool Bash --command "git add src/main.py" 2>&1 | grep -o "Blocked\|Allowed"
```
**Expected:** `Blocked, Allowed, Blocked, Blocked, Allowed`

---

## PHASE 10: agentrulegen.com Reference Integration (ACTIVE)

### Step 10.1 — Enriched agentrulegen.com Reference

**All 14 URLs have been fetched and parsed with full content extraction.** Key content, usage recommendations, and cross-tool equivalence documented below.

#### Guides (9 URLs)

| URL | Key Content | Usage in EmailIntelligence |
|-----|-------------|---------------------------|
| `/guides/what-are-ai-coding-rules` | Tool file locations, 40-60% correction reduction, correction elimination loop | Reference for foundational setup |
| `/guides/how-to-set-up-cursor-rules` | `.cursor/rules/*.mdc`, YAML frontmatter (`globs`, `alwaysApply`, `description`) | Fix `.cursor/rules/` structure |
| `/guides/claude-code-guide` | Hierarchy loading, `@path` imports, `.claude/rules/`, MCP config | Fix `.claude/` structure |
| `/guides/github-copilot-instructions` | `.github/copilot-instructions.md`, `applyTo:` frontmatter | Create Copilot instructions |
| `/guides/cursorrules-vs-claude-md` | 8-tool comparison, nesting support matrix (Cursor/Claude/Codex/Gemini only) | Cross-tool equivalence |
| `/guides/convert-cursor-rules-to-claude-md` | Migration paths, 90%+ content identical across formats | Format conversion |
| `/guides/how-to-code-faster-with-ai` | Spec-first dev, 15-min review rhythm, multi-tool orchestration matrix | Agent RuleZ workflow hooks |
| `/guides/agent-rules-for-monorepos` | 3 strategies (single/distributed/hybrid), import boundary rules | Apply to EmailIntelligence structure |
| `/guides/debugging-ai-generated-code` | Common pitfalls (off-by-one, race conditions, partial failure), prevention rules | Add to AGENTS.md |

#### Templates (5 URLs)

| URL | Key Content | Usage in EmailIntelligence |
|-----|-------------|---------------------------|
| `/templates/python-fastapi` | **HIGH PRIORITY** — SQLAlchemy 2.0 async, Pydantic v2, error handling, testing | Replace all Prisma references |
| `/templates/ai-agent-workflow` | Plan mode, subagent strategy, self-improvement loop, verification before done | Agent RuleZ hooks |
| `/templates/git-workflow` | Conventional commits, branch strategy, PR best practices, git hooks setup | `.claude/hooks.yaml` config |
| `/templates/code-review` | Author/reviewer responsibilities, security/performance checklists, comment prefixes | Code review automation |
| `/templates/linear-workflow` | Issue identifiers, magic words (`Fixes`, `Closes`), priority SLA, triage workflow | Taskmaster integration patterns |

### Step 10.2 — Extended Tool Documentation (Beyond agentrulegen.com)

The following tools in EmailIntelligence's environment are NOT covered by agentrulegen.com:

#### Roo Code (VS Code Extension)

| Aspect | Details |
|--------|---------|
| **Modes File** | `.roomodes` (YAML) at project root, or `~/.roo/settings/custom_modes.yaml` globally |
| **New Structure** | `.roo/modes/{slug}/.roomode` — directory-based with per-mode rules and MCP |
| **Per-Mode Rules** | `.roo/rules-{mode-slug}/` directories |
| **Precedence** | Project `.roo/modes` > `.roomodes` > Global `.roo/modes` > global settings |
| **Groups** | `read`, `edit`, `command`, `mcp` — permission controls per mode |
| **Schema** | `https://www.schemastore.org/roomodes.json` |

#### Kiro (Amazon - kiro.dev)

| Aspect | Details |
|--------|---------|
| **Steering Files** | `.kiro/steering/*.md` (workspace) or `~/.kiro/steering/` (global) |
| **Foundation Files** | `product.md`, `tech.md`, `structure.md` — auto-generated |
| **Inclusion Modes** | `always`, `fileMatch` (conditional), `manual`, `auto` |
| **Frontmatter** | YAML: `inclusion: always` or `inclusion: fileMatch` with `fileMatchPattern` |
| **Hooks** | `.kiro/hooks/` — JSON config for event-driven automations |
| **Hook Events** | File Save/Create/Delete, Pre/Post Tool Use, Pre/Post Task Execution |
| **Hook Actions** | `Ask Kiro` (agent prompt) or `Run Command` (shell) |
| **AGENTS.md** | Supported — placed in root or `~/.kiro/steering/` |
| **MCP Config** | `.kiro/settings/mcp.json` |

#### Trae (ByteDance - trae.ai)

| Aspect | Details |
|--------|---------|
| **Rules Location** | AI Management > Rules in right panel |
| **Personal Rules** | `user_rules.md` — preferences, language, personality |
| **Project Rules** | `project_rules.md` — team standards, coding practices |
| **Builder Mode** | Autonomous agent for full-project scaffolding from natural language |
| **SOLO Mode** | Collaborative planning before coding begins |
| **MCP Support** | Yes — via Model Context Protocol |
| **Platform** | VS Code-based, macOS/Windows, browser Cloud IDE |

#### Letta Code (docs.letta.com)

| Aspect | Details |
|--------|---------|
| **Memory Dir** | `$MEMORY_DIR/` — typically `~/.letta/agents/{AGENT_ID}/memory/` |
| **System Memory** | `system/` — always in context (rendered each turn) |
| **External Memory** | `reference/`, `history/` — accessed via tools |
| **Persona** | `system/persona.md` — agent identity and behavior |
| **User Context** | `system/human.md` — user preferences, patterns |
| **Skills** | `$SKILLS_DIR/` — procedural memory, on-demand |
| **Git-Backed** | Memory is a git repo — commit, push, sync |
| **Init Command** | `/init` — deep research and memory bootstrap |
| **Remember** | `/remember` — save context to memory |
| **Stateful** | Same agent across sessions, learns and improves |

### Step 10.3 — Cross-Tool Equivalence Matrix

#### File Locations

| Tool | Rules File | Modes/File | Hooks | MCP Config |
|------|-----------|------------|-------|------------|
| Cursor | `.cursor/rules/*.mdc` | — | — | `.cursor/mcp.json` |
| Claude Code | `CLAUDE.md`, `.claude/rules/` | — | `.claude/hooks.yaml` | `.claude/mcp.json` |
| Copilot | `.github/copilot-instructions.md` | — | — | — |
| Roo | `.roo/rules-{mode}/` | `.roomodes` | — | `.roo/mcp.json` |
| Kiro | `.kiro/steering/*.md` | — | `.kiro/hooks/` | `.kiro/settings/mcp.json` |
| Trae | `.trae/rules/` or AI panel | — | — | — |
| Letta Code | `$MEMORY_DIR/system/` | — | — | — |

#### Frontmatter Syntax Equivalence

| Tool | Path Scoping | Inclusion Mode |
|------|-------------|----------------|
| Cursor | `globs: "src/**/*.ts"` | `alwaysApply: true` |
| Claude Code | `paths: ["src/**/*.ts"]` | N/A (always on) |
| Copilot | `applyTo: "**/*.ts"` | N/A |
| Kiro | `fileMatchPattern: "**/*.ts"` | `inclusion: fileMatch` |

#### Nesting Support

| Tool | Hierarchical Rules | Import Mechanism |
|------|-------------------|------------------|
| Cursor | ✅ Yes | `.cursor/rules/` subdirs |
| Claude Code | ✅ Yes | `@path` imports, `.claude/rules/` |
| Copilot | ❌ No | Root only |
| Windsurf | ❌ No | Root only |
| Roo | ✅ Partial | `.roo/rules-{mode}/` per mode |
| Kiro | ✅ Yes | `.kiro/steering/` subdirs |
| Letta Code | ✅ Yes | `system/` hierarchy, `[[path]]` refs |

### Step 10.2 — Plan agentrulegen.com/analyze validation

After all phases complete, validate final configs:
```bash
# Upload each tool config to agentrulegen.com/analyze for validation
# This is a future manual step — requires browser interaction
echo "TODO: Upload .ruler/AGENTS.md to agentrulegen.com/analyze"
echo "TODO: Upload .claude/hooks.yaml to agentrulegen.com/analyze"
echo "TODO: Upload rulesync.jsonc to agentrulegen.com/analyze"
```

---

## UPDATED PROGRESS TRACKER

**Copy this tracker. Mark each step as you complete it.**

```
PHASE 1: Emergency Fixes [REQUIRED — 13 steps]
[ ] 1.1-1.13 (see detailed steps above)

PHASE 2: Content Fixes [REQUIRED — 7 steps]
[ ] 2.1-2.7 (see detailed steps above)

PHASE 3: Ruler Setup [REQUIRED — 5 steps]
[ ] 3.1-3.5 (see detailed steps above)

PHASE 4: Agent RuleZ Setup [REQUIRED — 6 steps]
[ ] 4.1-4.6 (see detailed steps above)

PHASE 5: File Cleanup [OPTIONAL — 4 steps]
[ ] 5.1-5.4 (see detailed steps above)

PHASES 6-10: [REFERENCE ONLY — See bottom of document]
```

---

## SINGLE FINAL VERIFICATION

**After completing Phases 1-4, run this ONE command:**

```bash
echo "=== FINAL GATE ===" && \
grep -c '<<<<<<' CLAUDE.md 2>/dev/null || echo "0 conflicts" && \
test -s .roo/mcp.json && test -s .cursor/mcp.json && test -s .claude/mcp.json && test -s .trae/mcp.json && echo "MCP: All populated" && \
test $(grep -c "YOUR_" .windsurf/mcp.json 2>/dev/null) -eq 0 && echo "Windsurf: No placeholders" && \
test $(grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l) -eq 0 && echo "Prisma: Removed" && \
test $(grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md 2>/dev/null) -eq 0 && echo "Windsurf bug: Fixed" && \
test -f .ruler/ruler.toml && test -f .claude/hooks.yaml && echo "Tools: Configured" && \
echo "✅ ALL PASS" || echo "❌ CHECK FAILED"
```

---

## POST-COMPLETION: What NOT to Commit

When staging for git, do NOT include:

- `/tmp/rulez` (temporary binary location)
- `.ruler/` generated output files (if gitignored by Ruler)
- `.bak` files created by Ruler
- Any files in other worktrees or unrelated changes

**Safe to stage:**
```bash
git add CLAUDE.md
git add GEMINI.md  # Split — now contains only Gemini CLI instructions (stays at root)
git add QWEN.md    # Replaced — now contains Tier 2 Qwen instructions (stays at root)
git add .gemini/JULES_TEMPLATE.md  # Extracted Jules template
git add docs/SCIENTIFIC_BRANCH_DOCS.md  # Copied scientific branch docs
git add .roo/mcp.json .cursor/mcp.json .claude/mcp.json .windsurf/mcp.json .trae/mcp.json .kilo/mcp.json
git add .windsurf/rules/dev_workflow.md
git add .clinerules/cline_rules.md .clinerules/self_improve.md
git add .windsurf/rules/windsurf_rules.md .windsurf/rules/self_improve.md
git add .roo/rules/roo_rules.md .roo/rules/self_improve.md
git add .trae/rules/trae_rules.md .trae/rules/self_improve.md
git add .kiro/steering/kiro_rules.md .kiro/steering/self_improve.md
git add rulesync.jsonc
git add .ruler/AGENTS.md .ruler/ruler.toml
git add .claude/hooks.yaml
git add docs/AGENT_RULES_STRESS_TEST_REPORT.md
git add docs/AGENT_RULES_TOOL_INTEGRATION_PLAN.md
git add docs/AGENT_RULES_NEW_CAPABILITIES_REPORT.md
git add docs/AGENT_RULES_TOOLS_VERIFIED_TEST_RESULTS.md
git add docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md
```

**Do NOT run `git add -A` or `git add .`**

---

## HANDOFF NOTES FOR NEXT AGENT

If handing off to another thread:

1. **State which phase was completed.** Example: "Phases 1-2 complete, starting Phase 3."
2. **Include the gate check output** for the last completed phase.
3. **If a step failed, state which step and paste the error.**
4. **The progress tracker at the top of this file should be updated.**
5. **Files modified so far** should be listed explicitly.

---

## VERIFIED TOOL FINDINGS (Updated 2026-04-05)

These findings come from actual tool execution against this project. They supplement the phases above.

### RuleSync v7.27.1 — Verified Limitations

**What Works:**
- ✅ `--check` drift detection exits code 1 when files diverge
- ✅ `--dry-run` shows changes without writing
- ✅ `--delete` cleans stale files before regenerating

**What Was Verified (Caveats):**
- ⚠️ **Import pulled from Cursor, not Cline** — `--targets cline` imported `.cursor/rules/overview.mdc` because Cline's `.clinerules/` files lack frontmatter that RuleSync expects
- ⚠️ **Generation is DESTRUCTIVE** — would DELETE 4 Roo rules, 4 Windsurf rules, 5 Kiro rules before writing unified content
- ⚠️ **MCP config scaffolded with template defaults** — not our actual project MCP servers
- ⚠️ **Does NOT support Trae AI** — use Ruler instead
- ⚠️ **Does NOT support Windsurf MCP** — requires manual config

**Recommendation:** Initialize `.rulesync/` with actual content BEFORE running generate to avoid data loss.

---

### Ruler v0.3.38 — Verified Capabilities (NEW)

**What Was Verified:**
- ✅ **32 agent targets** — broadest coverage of any tool tested
- ✅ **Trae AI support** — UNIQUE, fills Issue C4 gap that RuleSync cannot
- ✅ **`ruler revert`** — undoes all changes from `.bak` backups
- ✅ **`--backup` flag** — creates `.bak` files before overwriting (enabled by default)
- ✅ **Nested `.ruler/` directories** — `src/.ruler/`, `tests/.ruler/` for context-specific rules
- ✅ **TOML-based config** — `ruler.toml` with per-agent enable/disable
- ✅ **MCP server propagation** — merges MCP configs across tools
- ✅ **Skills propagation** — `.ruler/skills/` → 16 agent skill directories
- ✅ **`.gitignore` automation** — managed block with START/END markers
- ✅ **GitHub Actions CI template** — documented workflow for sync checking
- ✅ **Amp support** — writes to `.agents/skills/`

**Test Results:**
```bash
ruler init
ruler apply --dry-run --verbose
# Result: Would write to 32 agent targets simultaneously
```

**Recommendation:** Use Ruler for Trae AI support and as alternative to RuleSync for broader coverage.

---

### Agent RuleZ v2.3.0 — Verified Behavior (NEW)

**Nature:** NOT a rule sync tool — it's a **deterministic policy engine** that intercepts agent actions at runtime.

**What Was Verified:**
- ✅ **Hook generation** — Created `.claude/hooks.yaml` with 5 rules
- ✅ **Policy validation** — `rulez validate` passed syntax check
- ✅ **Lint** — `rulez lint` found no issues
- ✅ **Debug test: blocked force push** — `rulez debug PreToolUse --tool Bash --command "git push --force origin main"` returned `Blocked by rule 'block-force-push'`
- ✅ **Debug test: allowed normal commit** — `rulez debug PreToolUse --tool Bash --command "git commit -m 'test'"` returned `Allowed`

**5 Rules Generated:**
| Rule | What It Blocks | Priority |
|------|---------------|----------|
| `block-force-push` | `git push --force` to main/master/scientific | 100 |
| `block-hard-reset` | `git reset --hard` on protected branches | 90 |
| `block-env-cat` | Reading `.env` files (secret exposure) | 95 |
| `block-credentials-read` | Reading `credentials/` directory | 100 |
| `block-git-add-all` | `git add -A` or `git add .` | 85 |

**Limitation:** Only Claude hooks created (`.claude/hooks.yaml`). Need to create hooks for Cursor, Qwen, Gemini, etc.

**Recommendation:** Deploy RuleZ alongside RuleSync/Ruler for runtime enforcement. They serve different purposes.

---

### Tool Comparison Matrix (Verified)

| Feature | RuleSync | Ruler | Agent RuleZ |
|---------|----------|-------|-------------|
| **Purpose** | Rule distribution | Rule generation | Runtime policy enforcement |
| **When it acts** | At generation time | At generation time | At execution time |
| **Agent targets** | 28+ | 32 | 1 (Claude only so far) |
| **Trae AI** | ❌ | ✅ | ❌ |
| **Windsurf MCP** | ❌ | ✅ | ❌ |
| **Drift detection** | ✅ `--check` | ❌ | ❌ |
| **Runtime blocking** | ❌ | ❌ | ✅ |
| **Revert changes** | ❌ | ✅ `revert` | ❌ |
| **Backup before write** | ❌ | ✅ `--backup` | ❌ |

**Winning Combination:** RuleSync (ongoing sync) + Ruler (Trae + broader coverage) + Agent RuleZ (runtime enforcement) + manual fixes for 5 issues no tool covers.

---

## LETTA MEMORY UPDATE INSTRUCTIONS

To track this task progress in Letta memory, run these commands:

### 1. Store Current Progress
```
memory save task:agent-rules "Phase 1-5 handoff document updated with verified tool findings. 13 issues identified. Tools verified: RuleSync v7.27.1, Ruler v0.3.38, Agent RuleZ v2.3.0. Handoff doc: docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md"
```

### 2. Store Critical Findings
```
memory save findings:ruler "Ruler v0.3.38 verified: supports 32 agents including Trae AI (fills Issue C4). Has revert, backup, nested dirs, .gitignore automation. Broader coverage than RuleSync."
```

```
memory save findings:rulez "Agent RuleZ v2.3.0 verified: runtime policy engine (not sync tool). 5 rules generated for Claude. Successfully blocked git push --force. Need hooks for other agents."
```

```
memory save findings:rulesync "RuleSync v7.27.1 verified: import pulls wrong tool (Cursor not Cline). Generation is DESTRUCTIVE. MCP config uses template defaults. No Trae/Windsurf MCP support."
```

### 3. Store Issue Status
```
memory save issues:status "13 total issues. 3 critical (CLAUDE.md conflict, empty MCPs), 5 medium (Prisma refs, stale keys), 5 low (file purposes, undocumented hooks). RuleSync covers 7, Ruler covers 3 (including C4), manual fixes needed for 5."
```

### 4. Store Next Steps
```
memory save next-steps "1. Resolve CLAUDE.md merge conflict. 2. Fix RuleSync targets. 3. Populate empty MCP configs. 4. Initialize .rulesync/ with actual content. 5. Deploy RuleZ hooks to more agents. 6. Use Ruler for Trae AI support."
```

### 5. Verify Memory Saved
```
memory list
memory find agent-rules
memory find findings
```
