# Agent Instructions Manifest

## Overview

This document tracks all AI agent instruction files across the repository and their distribution across branches.

## Branch Strategy

- **Main/Scientific branches**: Store agent-specific instructions (CLAUDE.md, AGENTS.md, etc.)
- **Orchestration-tools branch**: Stores critical system instructions (AGENTS.md is intentionally blocked)
- **GitHub instructions**: Distributed via `.github/instructions/` (protected by orchestration)

---

## Root-Level Agent Instructions

### Files in `/` Root Directory

| File | Purpose | Branches | Status |
|------|---------|----------|--------|
| `CLAUDE.md` | Claude AI instructions | main, scientific | ✅ Tracked |
| `AGENTS.md` | Agent integration guide | **main, scientific ONLY** | ✅ Tracked (blocked on orch-tools) |
| `CRUSH.md` | CRUSH system docs | **main, scientific ONLY** | ✅ Tracked (blocked on orch-tools) |
| `QWEN.md` | Qwen AI instructions | main, scientific | ✅ Tracked |
| `GEMINI.md` | Gemini API guide | Not yet created | ⚠️ TODO |
| `LLXPRT.md` | LLXPRT system docs | main, scientific | ✅ Tracked |
| `CODEBUDDY.md` | CodeBuddy integration | Not yet created | ⚠️ TODO |
| `SHAI.md` | SHAI system docs | Not yet created | ⚠️ TODO |
| `OPENCODE.md` | OpenCode instructions | Not yet created | ⚠️ TODO |

---

## Agent Configuration Directories

### IDE & Tool Specific Configs

| Directory | Purpose | Files | Status |
|-----------|---------|-------|--------|
| `.claude/` | Claude Code settings | 7 files | ✅ Exists |
| `.cursor/` | Cursor IDE settings | 5 files | ✅ Exists |
| `.windsurf/` | Windsurf settings | 5 files | ✅ Exists |
| `.roo/` | Roo CLI config | 12 files | ✅ Exists |
| `.opencode/` | OpenCode config | 711 files | ✅ Exists |
| `.kilocode/` | KiloCode settings | Not yet tracked | ⚠️ TODO |
| `.codebuddy/` | CodeBuddy config | Not yet tracked | ⚠️ TODO |

---

## GitHub Instructions (Protected by Orchestration)

### `.github/instructions/`

These are **synced via orchestration approval system**:

| File | Purpose | Sync Method |
|------|---------|------------|
| `taskmaster.instructions.md` | Task Master instructions | Directory sync |
| `dev_workflow.instructions.md` | Development workflow | Directory sync |
| `self_improve.instructions.md` | Self-improvement patterns | Directory sync |
| `vscode_rules.instructions.md` | VSCode rules | Directory sync |
| `tools-manifest.json` | Tool registry | Directory sync |

---

## Branch Distribution Strategy

### Main/Scientific Branches

**Include:**
- Root agent instruction files (CLAUDE.md, QWEN.md, LLXPRT.md, etc.)
- Agent-specific configurations (.claude/, .cursor/, .windsurf/, etc.)
- `.github/instructions/` (protected by orchestration)
- Task Master data (.taskmaster/)

**Exclude:**
- Orchestration hooks (`.git/hooks/`)
- Orchestration scripts

### Orchestration-Tools Branch

**Include:**
- Git hooks (`.git/hooks/`)
- Orchestration scripts
- Critical system config
- `.github/instructions/` (critical agent instructions)

**Intentionally Exclude:**
- `AGENTS.md` - Branch-specific agent integration guide
- `CRUSH.md` - Branch-specific system docs
- `.taskmaster/` - User's task data
- Agent-specific configs (.claude/, .cursor/, etc.)

---

## Missing Agent Instruction Files

The following files are documented but not yet created:

| File | Purpose | Priority |
|------|---------|----------|
| `GEMINI.md` | Google Gemini API integration | Medium |
| `CODEBUDDY.md` | CodeBuddy IDE integration | Low |
| `SHAI.md` | SHAI system documentation | Low |
| `OPENCODE.md` | OpenCode framework guide | Medium |

Create as needed with standardized format:
```markdown
# [Tool Name] Instructions

## Overview
[Brief description]

## Integration
[How it integrates with the project]

## Configuration
[Setup instructions]

## Usage
[Common workflows]

## Troubleshooting
[Common issues and solutions]
```

---

## Tracking & Syncing

### How Instructions Are Maintained

1. **Root Files** (`CLAUDE.md`, `QWEN.md`, etc.)
   - Tracked in git
   - Version controlled
   - Available on main/scientific branches
   - User can edit without orchestration interference

2. **GitHub Instructions** (`.github/instructions/`)
   - Tracked in git
   - **Synced via orchestration approval system**
   - Protected from silent overwrites
   - User approval required before sync

3. **Agent Config Directories** (`.claude/`, `.cursor/`, etc.)
   - Tracked in git
   - Branch-specific (main/scientific)
   - Not synced via orchestration
   - User maintains independently

---

## Distribution Map

```
orchestration-tools branch
    ├── .github/instructions/ ✅ (SYNCED via orchestration)
    ├── .git/hooks/ ✅
    ├── scripts/ ✅
    ├── AGENTS.md ❌ (BLOCKED)
    └── CRUSH.md ❌ (BLOCKED)

main / scientific branches
    ├── .github/instructions/ ✅ (Synced from orch-tools)
    ├── CLAUDE.md ✅
    ├── AGENTS.md ✅
    ├── CRUSH.md ✅
    ├── QWEN.md ✅
    ├── LLXPRT.md ✅
    ├── .claude/ ✅
    ├── .cursor/ ✅
    ├── .windsurf/ ✅
    ├── .roo/ ✅
    ├── .opencode/ ✅ (711 files)
    └── .taskmaster/ ✅ (User's tasks)
```

---

## Synchronization Behavior

### When Switching from Orchestration-Tools to Main/Scientific

The orchestration system will sync:

```
=== Orchestration File Updates ===
The following directories will be synchronized:
  → .github/instructions/ (all contents)

Proceed with orchestration synchronization? (y/n)
```

**Files synchronized:**
- `.github/instructions/` (via directory sync)
- Root configuration files
- Shared libraries

**NOT synchronized** (branch-specific):
- Agent instruction files (AGENTS.md, CRUSH.md)
- Agent config directories (.claude/, .cursor/, etc.)
- Task Master data (.taskmaster/)

---

## Verification Commands

### Check which agent files are on orchestration-tools
```bash
git ls-tree -r origin/orchestration-tools --name-only | grep -E "^(CLAUDE|AGENTS|CRUSH|QWEN|LLXPRT)"
```

### Check which agent configs are tracked
```bash
git ls-files | grep "^\." | sort
```

### View all agent instruction files
```bash
ls -la *.md | grep -E "(CLAUDE|AGENTS|CRUSH|QWEN|LLXPRT|GEMINI|CODEBUDDY|SHAI|OPENCODE)"
```

### Compare agent files between branches
```bash
git diff main orchestration-tools -- AGENTS.md CRUSH.md
```

---

## Policy: Agent Instructions Should NOT Be on Orchestration-Tools

**Why AGENTS.md and CRUSH.md are blocked from orchestration-tools:**

1. **Branch Specific** - These guide development on main/scientific, not orchestration
2. **Prevent Overwrites** - User's main/scientific branch instructions should not be overwritten by orchestration
3. **Clear Separation** - Keep orchestration configuration isolated from development guidance
4. **Avoid Conflicts** - Prevents merge conflicts when orchestration-tools updates are pulled

**How this is enforced:**
```bash
# In scripts/validate-branch-propagation.sh line 33:
BRANCH_BLOCKED_FILES[orchestration-tools]="^src/|^backend/|^client/|^plugins/|^AGENTS\.md|^CRUSH\.md|^\.taskmaster/"
```

If these files accidentally appear on orchestration-tools, the validation script will flag them as violations.

---

## Related Documentation

- `ORCHESTRATION_APPROVAL.md` - Approval system for syncing
- `.GITHUB_FILES_INVENTORY.md` - GitHub instructions protection
- `AGENTS.md` - Main agent integration guide
- `CRUSH.md` - CRUSH system documentation
