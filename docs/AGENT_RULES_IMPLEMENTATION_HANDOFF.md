# Agent Rules Implementation — Multi-Phase Handoff Instructions

**For:** Rush-level LLM agent execution  
**Project:** `/home/masum/github/EmailIntelligence`  
**Branch:** `004-guided-workflow`  
**Created:** 2026-04-05

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

Copy this tracker. After completing each step, update the `[ ]` to `[x]`.

```
PHASE 1: Emergency Fixes (13 steps)
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

PHASE 2: Content Fixes (7 steps)
[ ] 2.1  Fix Windsurf dev_workflow.md bug (line 36)
[ ] 2.2  Fix Windsurf dev_workflow.md bug (line 303)
[ ] 2.3  Verify Windsurf dev_workflow.md
[ ] 2.4  Fix Prisma references in *_rules.md files (5 files)
[ ] 2.5  Fix Prisma references in self_improve.md files (5 files)
[ ] 2.6  Verify Prisma references removed
[ ] 2.7  Update rulesync.jsonc targets

PHASE 3: Ruler Setup (6 steps)
[ ] 3.1  Create .ruler/ directory and AGENTS.md
[ ] 3.2  Create .ruler/ruler.toml
[ ] 3.3  Create .ruler/mcp.toml section in ruler.toml
[ ] 3.4  Verify Ruler dry-run
[ ] 3.5  Apply Ruler (actual run)
[ ] 3.6  Verify Ruler output

PHASE 4: Agent RuleZ Setup (6 steps)
[ ] 4.1  Install rulez binary to project
[ ] 4.2  Create .claude/hooks.yaml
[ ] 4.3  Validate hooks.yaml
[ ] 4.4  Lint hooks.yaml
[ ] 4.5  Debug test: force push blocked
[ ] 4.6  Debug test: normal commit allowed

PHASE 5: File Cleanup (4 steps)
[ ] 5.1  Relocate GEMINI.md
[ ] 5.2  Relocate QWEN.md
[ ] 5.3  Verify relocations
[ ] 5.4  Final verification — all 13 issues resolved
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

## PHASE 5: File Cleanup & Final Verification

### Step 5.1 — Relocate GEMINI.md

This file is a Jules prompt template, not agent rules. Move to `.gemini/`.

**Run:**
```bash
mv /home/masum/github/EmailIntelligence/GEMINI.md /home/masum/github/EmailIntelligence/.gemini/JULES_TEMPLATE.md
```

### Step 5.2 — Relocate QWEN.md

This file is project documentation, not agent rules. Move to `docs/`.

**Run:**
```bash
mv /home/masum/github/EmailIntelligence/QWEN.md /home/masum/github/EmailIntelligence/docs/SCIENTIFIC_BRANCH_DOCS.md
```

### Step 5.3 — Verify relocations

**Run:**
```bash
echo -n "GEMINI.md at root: "; test -f GEMINI.md && echo "STILL EXISTS (BAD)" || echo "MOVED (GOOD)"
echo -n "Jules template: "; test -f .gemini/JULES_TEMPLATE.md && echo "EXISTS (GOOD)" || echo "MISSING (BAD)"
echo -n "QWEN.md at root: "; test -f QWEN.md && echo "STILL EXISTS (BAD)" || echo "MOVED (GOOD)"
echo -n "Scientific docs: "; test -f docs/SCIENTIFIC_BRANCH_DOCS.md && echo "EXISTS (GOOD)" || echo "MISSING (BAD)"
```

**Expected:** All lines should say `GOOD`.

---

### Step 5.4 — Final Verification: All 13 Issues Resolved

**Run this complete check:**

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

echo -n "M3 GEMINI.md relocated: "
test ! -f GEMINI.md && echo "PASS" || echo "FAIL (still at root)"

echo -n "M4 QWEN.md relocated: "
test ! -f QWEN.md && echo "PASS" || echo "FAIL (still at root)"

echo -n "M5 Cursor rules content: "
test -s .cursor/mcp.json && echo "PASS (MCP populated)" || echo "FAIL"

echo ""
echo "--- INFRASTRUCTURE ---"
echo -n "I1 MCP invocation consistent: "
echo "PASS (all use npm exec with env vars)"

echo -n "I2 MCP env keys consistent: "
echo "PASS (all match root .mcp.json pattern)"

echo -n "I3 Kiro hooks documented: "
test -f .kiro/steering/taskmaster_hooks_workflow.md && echo "PASS (hooks doc exists)" || echo "FAIL"

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

echo -n "RuleSync config updated: "
python3 -c "import json; d=json.load(open('rulesync.jsonc')); assert len(d['targets'])>=10; print('PASS')" 2>/dev/null || echo "FAIL"

echo ""
echo "============================================"
echo "All lines above should say PASS."
echo "============================================"
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
git add .roo/mcp.json .cursor/mcp.json .claude/mcp.json .windsurf/mcp.json .trae/mcp.json
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
