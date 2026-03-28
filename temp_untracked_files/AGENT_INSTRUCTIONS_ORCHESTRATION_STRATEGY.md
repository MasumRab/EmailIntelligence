# Agent Instructions & Orchestration Strategy

## Summary

All agent instruction files and configurations are properly distributed across branches according to their purpose:
- **Branch-specific instructions** (AGENTS.md, CRUSH.md) stay on main/scientific only
- **Critical GitHub instructions** (.github/instructions/) synced via orchestration approval
- **Agent configurations** (.claude/, .cursor/, etc.) maintained per branch

---

## File Distribution

### What Goes on Orchestration-Tools

| Category | Examples | Reason |
|----------|----------|--------|
| Critical system config | `.github/instructions/` | Essential for CI/CD and automation |
| Git hooks | `.git/hooks/` | Infrastructure |
| Build config | `requirements.txt`, `pyproject.toml` | Dependency management |
| Orchestration scripts | `scripts/install-hooks.sh` | Orchestration infrastructure |

### What Stays on Main/Scientific (NOT Synced)

| Category | Examples | Reason |
|----------|----------|--------|
| Branch agent guides | `AGENTS.md`, `CRUSH.md` | Guide for development on that branch |
| Agent configs | `.claude/`, `.cursor/`, `.windsurf/` | Specific to development IDE |
| User task data | `.taskmaster/` | User's personal task tracking |
| Qwen/LLXPRT/CLAUDE instructions | `QWEN.md`, `LLXPRT.md`, `CLAUDE.md` | Development-specific guidance |

---

## Why AGENTS.md and CRUSH.md Are NOT on Orchestration-Tools

```
Main Branch                          Orchestration-Tools Branch
├── AGENTS.md ✅                    ├── (no AGENTS.md ❌)
├── CRUSH.md ✅                     ├── (no CRUSH.md ❌)
├── CLAUDE.md ✅                    ├── .git/hooks/ ✅
├── .claude/ ✅                     ├── scripts/ ✅
└── .taskmaster/ ✅                 └── .github/instructions/ ✅ (SYNCED)
```

**Reasoning:**

1. **Purpose**: AGENTS.md guides development on main/scientific, not orchestration
2. **Blocking Policy**: Explicitly blocked by branch propagation rules (line 33 of validate-branch-propagation.sh)
3. **Prevent Loss**: If synced, would overwrite main's AGENTS.md with orchestration version
4. **Clean Separation**: Keep orchestration infrastructure isolated from development guidance

---

## How This Works in Practice

### When You Checkout Orchestration-Tools from Main

```bash
$ git checkout orchestration-tools
```

**What happens:**
1. Git switches to orchestration-tools branch
2. `.github/instructions/` is NOT synced (different branch, no merge)
3. `AGENTS.md` and `CRUSH.md` naturally disappear (they don't exist on orchestration-tools)
4. Agent configs (`.claude/`, `.cursor/`) naturally disappear (branch-specific)
5. You have clean orchestration environment

### When You Checkout Main from Orchestration-Tools

```bash
$ git checkout main
```

**What happens:**
1. Git switches to main branch
2. Post-checkout hook runs
3. Orchestration approval system detects `.github/instructions/` changes
4. **User approves** → `.github/instructions/` syncs from orchestration-tools
5. `AGENTS.md` and `CRUSH.md` **reappear** (restored from main)
6. Agent configs **reappear** (restored from main)
7. You have full main development environment

---

## Protected GitHub Instructions

The only agent instructions synced via orchestration are in `.github/instructions/`:

```
.github/instructions/
├── taskmaster.instructions.md ← SYNCED (critical)
├── dev_workflow.instructions.md ← SYNCED (critical)
├── self_improve.instructions.md ← SYNCED (critical)
├── vscode_rules.instructions.md ← SYNCED (critical)
└── tools-manifest.json ← SYNCED (critical)
```

**Why these are critical:**
- Essential for all AI agents across branches
- Must stay consistent
- Synced with user approval to prevent loss

**How they're protected:**
- `.github/instructions/` synced as full directory
- Orchestration approval system detects changes
- User must approve before sync
- All decisions logged

---

## Agent Instruction Files by Branch

### Main/Scientific Branches

**Always Present:**
```
CLAUDE.md              ← Claude AI instructions
QWEN.md                ← Qwen AI instructions
LLXPRT.md              ← LLXPRT system docs
AGENTS.md              ← Development agent guide (NOT on orchestration-tools)
CRUSH.md               ← CRUSH system docs (NOT on orchestration-tools)
AGENTS.md             ← Integration guide
```

**Agent Configurations:**
```
.claude/               ← Claude Code settings
.cursor/               ← Cursor IDE settings
.windsurf/             ← Windsurf settings
.roo/                  ← Roo CLI config
.opencode/             ← OpenCode config (711 files!)
```

**User Data:**
```
.taskmaster/           ← User's task tracking
```

### Orchestration-Tools Branch

**Always Present:**
```
.git/hooks/            ← Git automation hooks
scripts/               ← Orchestration scripts
.github/instructions/  ← SYNCED: Critical agent instructions
.github/workflows/     ← SYNCED: CI/CD workflows
```

**Intentionally Absent:**
```
AGENTS.md              ← NOT present (branch-specific)
CRUSH.md               ← NOT present (branch-specific)
.claude/               ← NOT present (dev-specific)
.cursor/               ← NOT present (dev-specific)
.windsurf/             ← NOT present (dev-specific)
.taskmaster/           ← NOT present (user's data)
```

---

## Tracking the Strategy

### Validation Rules

File: `scripts/validate-branch-propagation.sh` (line 33)

```bash
BRANCH_BLOCKED_FILES[orchestration-tools]="^src/|^backend/|^client/|^plugins/|^AGENTS\.md|^CRUSH\.md|^\.taskmaster/"
```

**This prevents:**
- Application code (src/, backend/, client/) from being on orchestration-tools
- Development guides (AGENTS.md, CRUSH.md) from being synced
- User task data (.taskmaster/) from being exposed

---

## For AI Agents

### When Writing Agent Instructions

**For Development Work (Goes on Main/Scientific):**
```markdown
# [Agent Name] Instructions

These instructions guide development work on the main/scientific branches.

## Integration with Project
[How this agent integrates with EmailIntelligence]

## Key Workflows
[Common development patterns]
```

Examples: `CLAUDE.md`, `QWEN.md`, `LLXPRT.md`

**For Critical System Tasks (Goes in `.github/instructions/`):**
```markdown
These are essential for all agents and must stay synchronized.
They're synced via orchestration approval system.
```

Examples: `taskmaster.instructions.md`, `dev_workflow.instructions.md`

---

## Common Scenarios

### Scenario 1: Add New Agent Instructions

**For a new IDE (e.g., Cursor):**
1. Create `.cursor/settings.json`
2. Commit to main/scientific
3. Don't add to orchestration-tools (it's dev-specific)

**For system-wide instructions:**
1. Add to `.github/instructions/`
2. Will sync via orchestration approval
3. Available to all branches

### Scenario 2: Update Agent Guide

**Update AGENTS.md:**
```bash
$ git checkout main
# Edit AGENTS.md
$ git add AGENTS.md
$ git commit -m "Update agent integration guide"
$ git push origin main
# Don't merge to orchestration-tools (blocked by policy)
```

**Update .github/instructions/:**
```bash
$ git checkout orchestration-tools
# Edit .github/instructions/taskmaster.instructions.md
$ git add .github/instructions/taskmaster.instructions.md
$ git commit -m "Update TaskMaster instructions"
$ git push origin orchestration-tools
# Will sync to main/scientific via orchestration approval
```

### Scenario 3: Branch Switch Flow

```
Main Branch
  ├── AGENTS.md ✅
  ├── CRUSH.md ✅
  ├── .claude/ ✅
  └── .github/instructions/ ✅

Switch to Orchestration-Tools
  ↓ (Files disappear as they're not on this branch)

Orchestration-Tools Branch
  ├── .git/hooks/ ✅
  ├── scripts/ ✅
  └── .github/instructions/ ✅

Switch back to Main
  ↓ (Post-checkout hook syncs .github/instructions/ with approval)
  ↓ (Other files restored from git)

Main Branch
  ├── AGENTS.md ✅ (restored)
  ├── CRUSH.md ✅ (restored)
  ├── .claude/ ✅ (restored)
  └── .github/instructions/ ✅ (synced)
```

---

## Verification

### Confirm Correct Distribution

```bash
# Check what's on orchestration-tools
git show origin/orchestration-tools:AGENTS.md 2>&1 | head -5
# Should output: fatal: Path 'AGENTS.md' does not exist

# Check what's on main
git show origin/main:AGENTS.md 2>&1 | head -5
# Should output: # Agent Integration Guide...

# Check .github/instructions on both
git show origin/orchestration-tools:.github/instructions/taskmaster.instructions.md | head -5
git show origin/main:.github/instructions/taskmaster.instructions.md | head -5
# Both should have content (identical)
```

### View Complete Distribution

```bash
# All files on orchestration-tools
git ls-tree -r origin/orchestration-tools --name-only | grep -E "\.(md|json|yml)$" | sort

# All tracked files on main
git ls-tree -r origin/main --name-only | grep -E "\.(md|json|yml)$" | sort

# Compare
git diff --name-status origin/main origin/orchestration-tools
```

---

## Related Documentation

- `AGENT_INSTRUCTIONS_MANIFEST.md` - Complete file inventory
- `ORCHESTRATION_APPROVAL.md` - How `.github/instructions/` sync works
- `ORCHESTRATION_PROCESS_GUIDE.md` - Full orchestration system
- `AGENTS.md` - Main agent integration guide
- `CRUSH.md` - CRUSH system documentation
