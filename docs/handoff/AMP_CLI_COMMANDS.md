# AMP CLI Commands for Agent Rules Implementation

**Purpose:** Ready-to-use AMP CLI command strings with correct tool configurations based on actual usage patterns.

**Critical Insight:** Tools like Gemini CLI and Qwen Code use `settings.json` with `contextFileName: "AGENTS.md"` — they may NOT read what Ruler writes (`system.md`)!

**AMP Modes:**
- `rush` — Fast execution, minimal verification
- `deep` — Thorough analysis, comprehensive verification
- `large` — Extended context for complex tasks
- `smart` — Balanced approach (default)

---

## Tool Configuration Matrix

### Tier 1: CLI Tools with settings.json (AgentsMdAgent)

**Decision Implemented (2026-04-10):** CLI tools (amp, qwen, opencode, kilocode) extend `AgentsMdAgent` and read root `AGENTS.md` via `settings.json` `contextFileName`. NO custom `output_path` in ruler.toml — uses Ruler built-in defaults.

| Tool | Context Loading | contextFileName | Ruler Output | Status |
|------|-----------------|-----------------|--------------|--------|
| **Gemini CLI** | Hierarchical (AGENTS.md + GEMINI.md) | `AGENTS.md` | ROOT `AGENTS.md` (agentsmd) | ✅ ALIGNED |
| **Qwen Code** | Hierarchical (AGENTS.md + QWEN.md) | `AGENTS.md` | ROOT `AGENTS.md` (agentsmd) | ✅ ALIGNED |
| **OpenCode** | `.opencode/OPENCODE.md` | `AGENTS.md` | ROOT `AGENTS.md` (agentsmd) | ✅ ALIGNED |
| **Kilo Code** | `.kilo/rules/` | `AGENTS.md` | ROOT `AGENTS.md` (agentsmd) | ✅ ALIGNED |
| **Claude Code** | Root `CLAUDE.md` | N/A | `CLAUDE.md` | ✅ ALIGNED |

**Note:** `[agents.amp]`, `[agents.qwen]`, `[agents.opencode]`, `[agents.kilocode]` sections REMOVED from ruler.toml — they natively read root `AGENTS.md`.

### Tier 2: IDE Agents (Ruler Aligned)

| Tool | Context Directory | Config Pattern | Status |
|------|-------------------|----------------|--------|
| **Cursor** | `.cursor/rules/` | system.md + rules/*.md | ✅ Working |
| **Roo (Cline)** | `.roo/rules/` | system.md + roo_rules.md | ✅ Working |
| **Windsurf** | `.windsurf/rules/` | system.md + workflows/ | ✅ Working |
| **Trae** | `.trae/rules/` | system.md + trae_rules.md | ✅ Working |
| **Kiro** | `.kiro/steering/` | system.md + kiro_rules.md | ✅ Working |

---

## contextFileName Configuration (RESOLVED)

**Decision Implemented (2026-04-10):**

CLI tools (Gemini, Qwen, OpenCode, Kilo, AMP) use `settings.json`:
```json
{
  "contextFileName": "AGENTS.md",
  "mcpServers": { ... },
  "permissions": { "allow": [...], "deny": [...] }
}
```

**How it works NOW:**
- `agentsmd` agent in ruler.toml syncs to ROOT `AGENTS.md`
- CLI tools read root `AGENTS.md` via `contextFileName: "AGENTS.md"`
- **NO MISMATCH** — All CLI tools read from the same synced root `AGENTS.md`

**Hybrid tools (cursor, windsurf, roo):** `output_path` is optional — may read from both `{tool}/rules/system.md` AND root `AGENTS.md`.

**IDE tools (claude, cline, kiro, trae):** KEEP `output_path` (non-AgentsMdAgent).

---

## amp_phase_0_5: Configuration Audit (Deep Mode)

**Run BEFORE any other phases to verify correct tool configurations.**

```bash
amp threads new --mode deep --execute "You are auditing AI coding agent tool configurations.

**Critical Document:** docs/handoff/REAL_CONFIGURATION_AUDIT.md

**Tasks:**
0.5.1: Check all settings.json files for contextFileName
0.5.2: Verify context file alignment with Ruler outputs
0.5.3: Check for missing context files in tool directories
0.5.4: Verify MCP server configurations in settings.json

**Discovery (RESOLVED 2026-04-10):**
CLI tools (amp, qwen, opencode, kilocode) extend AgentsMdAgent and read root AGENTS.md via settings.json contextFileName.
NO custom output_path needed — Ruler's agentsmd agent syncs to root AGENTS.md.

**Check:**
for f in .gemini/settings.json .qwen/settings.json .claude/settings.json; do
  if [ -f \"\$f\" ]; then
    echo \"=== \$f ===\"
    python3 -c \"import json; d=json.load(open('\$f')); print('contextFileName:', d.get('contextFileName', 'NOT SET'))\"
  fi
done

**VERIFY:**
ls -la AGENTS.md  # Root AGENTS.md must exist
ruler apply --project-root . --dry-run  # Preview Ruler outputs"
```

---

## amp_phase_0: Content Bootstrap (Rush Mode)

```bash
amp threads new --mode rush --execute "You are bootstrapping Agent Rules content from templates.

**Option A: agentrulegen.com (Web UI)**
- URL: https://agentrulegen.com
- Select: Python, FastAPI, React, SQLAlchemy, Pydantic
- Export to: .ruler/AGENTS.md

**Option B: agent-rules-kit (CLI)**
```bash
agent-rules-kit --stack=react --ide=claude --global --auto-install
# Copy generated CLAUDE.md to .ruler/AGENTS.md
cat CLAUDE.md >> .ruler/AGENTS.md && rm CLAUDE.md
```

**CRITICAL for CLI Tools (AgentsMdAgent):**
CLI tools (Gemini, Qwen, OpenCode, Kilo, AMP) load root AGENTS.md by default (contextFileName: 'AGENTS.md').
Ruler.toml has NO output_path for these tools — they extend AgentsMdAgent.

**VERIFY:**
test -f AGENTS.md && echo 'AGENTS.md: ROOT EXISTS' || echo 'MISSING'
test -f .ruler/AGENTS.md && echo '.ruler/AGENTS.md: EXISTS' || echo 'MISSING'"
```

---

## amp_phase_1: Emergency Fixes (Rush Mode)

```bash
amp threads new --mode rush --execute "You are executing Phase 1 Emergency Fixes.

**Phase Document:** docs/handoff/phase-01-emergency-fixes.md

**Tasks (13 steps):**
1.1-1.2: Resolve CLAUDE.md merge conflict
1.3-1.4: Fix .roo/mcp.json (empty → populated)
1.5-1.6: Fix .cursor/mcp.json (empty → populated)
1.7-1.8: Fix .claude/mcp.json (empty → populated)
1.9-1.10: Fix .windsurf/mcp.json (placeholder keys → env vars)
1.11-1.12: Create .trae/mcp.json
1.13: Delete .rules file

**settings.json Pattern (for Gemini/Qwen):**
```json
{
  \"contextFileName\": \"AGENTS.md\",
  \"mcpServers\": {
    \"task-master-ai\": {
      \"command\": \"npm\",
      \"args\": [\"exec\", \"task-master-ai\"],
      \"env\": {
        \"GOOGLE_API_KEY\": \"\${GOOGLE_API_KEY}\",
        \"GITHUB_API_KEY\": \"\${GITHUB_API_KEY}\"
      }
    }
  },
  \"permissions\": {
    \"allow\": [\"Bash(git *)\"],
    \"deny\": [\"Read(credentials/)\"]
  }
}
```

**Critical Rules:**
1. Run VERIFY after EVERY step
2. Copy strings EXACTLY from phase document
3. NEVER use git add -A

**Start:** Read docs/handoff/phase-01-emergency-fixes.md"
```

---

## amp_phase_2: Content Fixes (Rush Mode)

```bash
amp threads new --mode rush --execute "You are executing Phase 2 Content Fixes.

**Phase Document:** docs/handoff/phase-02-content-fixes.md

**Tasks (8 steps):**
2.1-2.3: Fix Windsurf dev_workflow.md bugs
2.4-2.6: Fix Prisma references (project doesn't use Prisma)
2.7: Update rulesync.jsonc targets
2.8: Verify all content fixes

**Critical Rules:**
1. Run VERIFY after EVERY step
2. Copy strings EXACTLY from phase document
3. NEVER use git add -A

**Start:** Read docs/handoff/phase-02-content-fixes.md"
```

---

## amp_phase_3: Ruler Setup (Rush Mode)

```bash
amp threads new --mode rush --execute "You are executing Phase 3 Ruler Setup.

**Phase Document:** docs/handoff/phase-03-ruler-setup.md
**Config File:** .ruler/ruler.toml
**Source File:** .ruler/AGENTS.md

**Decision Implemented (2026-04-10):**
- CLI tools (amp, qwen, opencode, kilocode) — NO output_path needed (AgentsMdAgent)
- Hybrid tools (cursor, windsurf, roo) — output_path is OPTIONAL
- IDE tools (claude, cline, kiro, trae) — KEEP output_path

**Removed sections from ruler.toml:**
- `[agents.amp]` — extends AgentsMdAgent
- `[agents.qwen]` — extends AgentsMdAgent
- `[agents.opencode]` — extends AgentsMdAgent
- `[agents.kilocode]` — extends AgentsMdAgent

**Tasks (6 steps):**
3.1: Verify .ruler/ exists
3.2: Create .ruler/AGENTS.md
3.3: Verify ruler.toml has NO output_path for CLI tools
3.4: Verify Ruler config (dry-run)
3.5: Apply Ruler
3.6: Verify root AGENTS.md synced

**Commands:**
ruler apply --project-root . --dry-run 2>&1 | head -10
ruler apply --project-root . --backup

**VERIFY:**
ls -la AGENTS.md  # Must exist at root

**Start:** Read docs/handoff/phase-03-ruler-setup.md"
```

---

## amp_phase_4: Agent RuleZ Setup (Rush Mode)

```bash
amp threads new --mode rush --execute "You are executing Phase 4 Agent RuleZ Setup.

**Phase Document:** docs/handoff/phase-04-agent-rulez.md

**STATUS:** rulez binary already installed (v2.3.0 at ~/.local/bin/rulez)

**Tasks (5 steps — Step 4.1 COMPLETE):**
4.1: ✅ Install rulez binary (ALREADY DONE)
4.2: Create .claude/hooks.yaml
4.3: Validate hooks.yaml
4.4: Lint hooks.yaml
4.5: Debug test: force push blocked
4.6: Debug test: normal commit allowed

**Commands:**
which rulez  # → ~/.local/bin/rulez
rulez --version  # → rulez 2.3.0
rulez validate --config .claude/hooks.yaml
rulez debug --event 'Bash:git push --force origin main'

**Start with Step 4.2:** Read docs/handoff/phase-04-agent-rulez.md"
```

---

## amp_phase_5: Context File Alignment (Deep Mode)

**NEW PHASE — Critical for Gemini/Qwen**

```bash
amp threads new --mode deep --execute "You are verifying context file alignment post-decision.

**Decision Implemented (2026-04-10):**
CLI tools (amp, qwen, opencode, kilocode) extend AgentsMdAgent and read root AGENTS.md.
Ruler.toml has NO output_path sections for these tools — they use Ruler's built-in defaults.

**Deleted files:**
- .qwen/system.md
- .agents/system.md
- .opencode/system.md
- .kilo/rules/system.md

**Verification Tasks:**
5.1: Confirm root AGENTS.md exists
5.2: Confirm CLI tool settings.json has contextFileName: 'AGENTS.md'
5.3: Verify no orphaned system.md files in CLI tool directories
5.4: Test with actual tool invocation

**Check:**
ls -la AGENTS.md
grep contextFileName .qwen/settings.json .gemini/settings.json

**VERIFY:**
cat AGENTS.md | head -20
# Should show synced content from .ruler/AGENTS.md"
```

---

## amp_gate_check: Run Gate Check (Deep Mode)

```bash
amp threads new --mode deep --execute "You are running a Phase Gate Check.

**Phase:** [PHASE_NUMBER]

**Gate Check Commands:**
echo '=== PHASE [N] GATE CHECK ==='

# File existence checks
for f in [FILES_TO_CHECK]; do
  test -f \"\$f\" && echo '✅ '\$f': EXISTS' || echo '❌ '\$f': MISSING'
done

# Verify root AGENTS.md exists (CLI tools read from root)
test -f AGENTS.md && echo '✅ AGENTS.md: EXISTS (CLI tools read this)' || echo '❌ AGENTS.md: MISSING'

# contextFileName alignment check
for tool in gemini qwen opencode; do
  settings=\".\$tool/settings.json\"
  if [ -f \"\$settings\" ]; then
    ctx=\$(python3 -c \"import json; print(json.load(open('\$settings')).get('contextFileName', 'NOT SET'))\")
    echo \"\$tool: reads \$ctx\"
  fi
done

**Report results in format:**
## Phase [N] Gate Check Results
- File X: PASS/FAIL
- Overall: PASS/FAIL"
```

---

## Mode Usage Guidelines

| Phase | Recommended Mode | Reason |
|-------|------------------|--------|
| **Phase 0.5** (NEW) | `deep` | Configuration audit requires thoroughness |
| Phase 0 | `rush` | Quick template generation |
| Phase 1 | `rush` | Fast fixes, clear verification |
| Phase 2 | `rush` | Content edits, fast execution |
| Phase 3 | `rush` | Ruler apply is straightforward |
| Phase 4 | `rush` | RuleZ debug is fast |
| **Phase 5** | `deep` | Verify decision implementation |
| Phase 9 | `deep` | Comprehensive verification |

---

## Quick Reference

```bash
# Create Rush mode session
amp threads new --mode rush --execute "[PROMPT]"

# Create Deep mode session
amp threads new --mode deep --execute "[PROMPT]"

# Continue last thread
amp threads continue --last

# List threads
amp threads list
```

---

## Tool-Specific CLI Commands

### Claude Code
```bash
claude --version  # Check version
cat CLAUDE.md      # Verify context file at root
```

### Gemini CLI
```bash
gemini  # Runs in interactive mode
# Check settings.json for:
# - contextFileName: "AGENTS.md" (hierarchical loading)
# - mcpServers: MCP server configs
cat .gemini/settings.json
```

### Qwen Code
```bash
qwen  # Runs in interactive mode
# Check settings.json for:
# - contextFileName: "AGENTS.md"
# - permissions: allow/deny lists
# - mcpServers: MCP configs
cat .qwen/settings.json
```

### Ruler (Distribution)
```bash
ruler apply --project-root . --dry-run
ruler apply --project-root . --backup
ruler --version
```

### Agent RuleZ (Runtime Hooks)
```bash
rulez --version      # Check installed version
rulez validate        # Validate hooks.yaml
rulez lint           # Check for rule overlaps
rulez debug --event 'Bash:git push --force origin main'
```
