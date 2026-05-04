# Context-Agnostic Handoff Guide

**Purpose:** Run handoff checks from ANY folder and ANY branch.
**Created:** 2026-04-14

---

## Quick Start

```bash
# From any folder, any branch:
cd ~/anything
source /home/masum/github/EmailIntelligenceAider/docs/handoff/context-guard.sh
source /home/masum/github/EmailIntelligenceAider/docs/handoff/context-agnostic-gates.sh

# Run all phases:
phase1_gate
phase2_gate
phase3_gate
phase4_gate
phase5_gate
final_gate

# Or run a single phase:
final_gate
```

---

## How It Works

### context-guard.sh

1. **Walks up** the directory tree from CWD looking for `.git/` → sets `$PROJECT_ROOT`
2. **Detects** current branch and commit → exports `$CURRENT_BRANCH`, `$CURRENT_COMMIT`
3. **Discovers** which agent tools exist → exports `$AGENT_TOOLS` (space-separated list)
4. **Determines** branch-specific state file → exports `$STATE_FILE` = `STATE_<branch>.md`
5. **Does NOT change CWD** — all operations use `$PROJECT_ROOT` prefix

### context-agnostic-gates.sh

Provides helper functions that replace all hardcoded relative-path checks:

| Helper | What It Does | Example |
|--------|-------------|---------|
| `check_file "path" "desc"` | Checks if file exists | `✅ CLAUDE.md: EXISTS` or `⚪ CLAUDE.md: NOT PRESENT` |
| `check_file_content "path" "pattern" "desc"` | Greps file if it exists | `🔍 Merge conflicts: 0 matches` |
| `check_json "path" "desc"` | Validates JSON if file exists | `✅ Roo MCP: VALID JSON` |
| `check_dir "path" "desc"` | Checks if directory exists | `✅ .ruler: EXISTS` |
| `count_files "dir" "pattern" "desc"` | Counts matching files | `📁 .roo/rules: 3 files` |

**Key behavior:** Missing files are reported as `⚪ NOT PRESENT (branch doesn't configure this tool)`. This is NOT a skip — it's a **documented finding** that the current branch doesn't have this tool configured. The check WAS performed; the result was "absent." This is valuable information for branch comparison.

---

## Before vs After

### Before (fragile — only works from project root)

```bash
cd /home/masum/github/EmailIntelligenceAider
grep -c '<<<<<<' CLAUDE.md
python3 -c "import json; json.load(open('.roo/mcp.json'))"
```

**Fails if:** CWD = `~/`, branch = `main`, or file doesn't exist.

### After (agnostic — works from anywhere)

```bash
cd ~/
source docs/handoff/context-guard.sh
source docs/handoff/context-agnostic-gates.sh
check_file_content "CLAUDE.md" '<<<<<<' "Merge conflicts"
check_json ".roo/mcp.json" "Roo MCP"
```

**Works if:** CWD = anywhere, branch = any, file may or may not exist.

---

## What Each Phase Checks

### Phase 1: Emergency Fixes
- Merge conflicts in CLAUDE.md
- MCP config validity for all discovered tools
- Placeholder credentials in Windsurf config
- `.rules` file deletion

### Phase 2: Content Fixes
- Duplicate flags in Windsurf rules
- Prisma references across all rule directories
- Rulesync target count

### Phase 3: Ruler Setup
- Ruler config files exist
- Ruler dry-run succeeds
- Project name references in root docs

### Phase 4: Agent RuleZ
- rulez installation
- hooks.yaml existence
- hooks validation and lint

### Phase 5: File Cleanup
- Tier 2 root files (GEMINI.md, QWEN.md, IFLOW.md, CRUSH.md, LLXPRT.md)
- Jules template extraction

---

## Agent Tool Discovery

The `discover_agents()` function scans for 24 known agent configurations:

| Type | Tools Discovered |
|------|-----------------|
| **Directories** | `.roo`, `.cursor`, `.claude`, `.windsurf`, `.trae`, `.kiro`, `.kilo`, `.clinerules`, `.zed`, `.continue`, `.gemini`, `.qwen`, `.agent`, `.agents`, `.iflow`, `.ruler` |
| **Root files** | `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `QWEN.md`, `IFLOW.md`, `CRUSH.md`, `LLXPRT.md`, `.rules` |
| **Config files** | `.mcp.json`, `rulesync.jsonc`, `opencode.json` |

If a branch doesn't have a tool's directory, it's simply not listed — not treated as an error.

---

## Extending for New Tools

To add a new agent tool to discovery, add one line to `discover_agents()`:

```bash
[ -d "$r/.newtool" ]   && tools+=("newtool")    # Directory-based
[ -f "$r/NEWTOOL.md" ] && tools+=("NEWTOOL.md") # File-based
```

To add a new gate check, use the helper functions:

```bash
check_file ".newtool/config.yaml" "NewTool config"
check_file_content ".newtool/rules.md" "TODO" "NewTool TODOs"
```

---

## Execution Journal — Decision Tracking Across Phases

The handoff process now tracks **decisions, changes, and context** across all phases.

### What's Tracked

| Category | Fields | Captured By |
|----------|--------|-------------|
| **Environment** | Branch, commit, CWD, project root, discovered tools | `context-guard.sh` (auto) |
| **Agent Identity** | Agent name, model, session ID | Set by agent before `start_phase()` |
| **Decisions** | Decision, rationale, alternatives, outcome | `log_decision()` during phase |
| **Changes** | File, action, before, after, commit SHA | `log_change()` during phase |
| **Verification** | Full gate check output, pass/fail | `complete_phase()` after phase |

### How It Works

```bash
# 1. Detect environment (auto)
source docs/handoff/context-guard.sh

# 2. Start a phase (creates structured entry in STATE.md)
start_phase "5" "File Cleanup"

# 3. Log decisions as you make them
log_decision "5" "1" "Restore GEMINI.md from git history" \
  "File exists in commit abc123" \
  "Create new file from scratch" \
  "Restored — content matches original"

# 4. Log file changes
log_change "GEMINI.md" "Restored" "Missing" "Restored from abc123" "pending"

# 5. Complete phase with gate check
complete_phase "5" "PASS" "$(phase5_gate)"
```

### STATE.md Structure (After Execution)

Each phase entry now contains:

```markdown
### Phase N: Name
- **Status:** COMPLETE
- **Agent:** name
- **Agent Model:** model-identifier
- **Session ID:** session-uuid
- **Started:** timestamp
- **Completed:** timestamp
- **Context:**
  - Branch: detected-branch
  - Commit: detected-commit
  - CWD: detected-cwd
  - Discovered Tools: auto-discovered list
- **Decision Log:**
  | # | Decision | Rationale | Alternatives | Outcome |
  |---|----------|-----------|-------------|---------|
  | 1 | ... | ... | ... | ... |
- **Changes:**
  | File | Action | Before | After | Commit SHA |
  |------|--------|--------|-------|------------|
  | ... | ... | ... | ... | ... |
- **Gate Check:** PASS
- **Verification Evidence:** (full output)
- **Issues:** notes
```

### Why This Matters

When an agent runs from a **different branch** or **different folder**, the decision log captures:
1. **What tools were discovered** on that branch (may differ from orchestration-tools)
2. **Why decisions were made** based on what was actually found, not what was assumed
3. **What was changed** with before/after state and commit SHA
4. **What verification was performed** with full output, not just PASS/FAIL

### Branch Registry — Tracking Across Branches

STATE.md maintains a **Branch Registry** that tracks which branch each phase ran on:

| Phase | Branch | Commit | Tools Discovered | Status |
|-------|--------|--------|-----------------|--------|
| 1 | orchestration-tools | 8cd475ba | 24 tools | COMPLETE |
| 5 | main (auto-detected) | abc1234 | 8 tools | PENDING |
| 11 | scientific (auto-detected) | def5678 | 12 tools | PENDING |

This means:
- If Phase 5 runs on `main`, it discovers ~8 tools (only root files)
- If Phase 5 runs on `orchestration-tools`, it discovers 24 tools
- Both results are valid — they document the branch's actual configuration
- The Branch Registry makes it clear WHICH branch was evaluated in each phase

This is NOT "skipping" checks on branches that lack tools. It's **documenting** which tools each branch configures. A branch without `.windsurf/` is a valid finding — it means "this branch doesn't use Windsurf."

---

## Testing

```bash
# Test from project root
cd /home/masum/github/EmailIntelligenceAider
source docs/handoff/context-guard.sh
source docs/handoff/context-agnostic-gates.sh
final_gate

# Test from subfolder
cd docs/handoff
source /home/masum/github/EmailIntelligenceAider/docs/handoff/context-guard.sh
source /home/masum/github/EmailIntelligenceAider/docs/handoff/context-agnostic-gates.sh
phase1_gate

# Test from home directory
cd ~
source /home/masum/github/EmailIntelligenceAider/docs/handoff/context-guard.sh
source /home/masum/github/EmailIntelligenceAider/docs/handoff/context-agnostic-gates.sh
final_gate
```
