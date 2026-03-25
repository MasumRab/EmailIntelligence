# EmailIntelligenceAider (EIAider) — Config File Analysis

**Generated:** 2026-03-25  
**Status:** ✅ **COMPLETED** — Cleanup committed and pushed (c6238b87)  
**Current Branch:** `orchestration-tools` (up to date with origin)  
**Previous Status:** 🟡 MEDIUM — 1 unpushed commit (136c1245 cleanup of 76 files)  
**Branches Analyzed:** 12

---

## Branch State Overview

### Current Branch State for EmailIntelligenceAider
- **Current checked out**: `orchestration-tools`
- **Remote**: `origin`
- **Status**: Clean, up to date with origin

### Local Branches (12 total) - ALL have tracking remotes:

| Branch | Tracking | Status |
|--------|----------|--------|
| 001-agent-context-control | origin/001-agent-context-control | |
| 001-command-registry-integration | origin/001-command-registry-integration | |
| 001-orchestration-tools-consistency | origin/001-orchestration-tools-consistency | |
| 001-orchestration-tools-verification-review | origin/001-orchestration-tools-verification-review | |
| feature/task-18-import-validation-test | origin/feature/task-18-import-validation-test | |
| main | origin/main | |
| migration-backend-to-src-backend | origin/migration-backend-to-src-backend | |
| **orchestration-tools** | origin/orchestration-tools | **CHECKED OUT** ⭐ |
| orchestration-tools-changes-emailintelligence-cli-20251112 | origin/orchestration-tools-changes-emailintelligence-cli-20251112 | |
| orchestration-tools-changes-recovery-framework | origin/orchestration-tools-changes-recovery-framework | |
| scientific | origin/scientific | |
| task-15-backup-recovery | origin/task-15-backup-recovery | |

### Key Observations:
- All 12 local branches have tracking remotes ✓
- No orphan local branches
- No branches exist only on remote
- `orchestration-tools` is the canonical source branch
- `scientific` has significant divergence (247 ahead, 529 behind origin/scientific)

---

### Branch Checkout Instructions

**Navigation:**
```bash
cd ~/github/EmailIntelligenceAider
```

**For each recommended action, specify the exact branch to checkout:**

1. **To fix setup/launch.py conflicts (82 markers on main and orchestration-tools):**
   ```bash
   # Fix on main first
   git checkout main
   # Resolve conflicts in setup/launch.py
   
   # Then fix on orchestration-tools (canonical)
   git checkout orchestration-tools
   # Resolve conflicts and push
   git push origin orchestration-tools
   ```

2. **To fix CLAUDE.md gitignore issue:**
   ```bash
   git checkout orchestration-tools
   # Edit .gitignore line 241 to remove CLAUDE.md
   # Commit and push
   git add .gitignore
   git commit -m "fix: remove CLAUDE.md from gitignore"
   git push origin orchestration-tools
   ```

3. **To fix AGENTS.md conflicts on orchestration-tools-changes-recovery-framework:**
   ```bash
   git checkout orchestration-tools-changes-recovery-framework
   # Resolve 3 conflict markers in AGENTS.md
   git push origin orchestration-tools-changes-recovery-framework
   ```

4. **To sync with main (65 commits behind):**
   ```bash
   git checkout main
   git pull origin main
   # Or rebase onto main from orchestration-tools
   git checkout orchestration-tools
   git rebase main
   ```

**Push/pull commands for each branch:**
```bash
# Pull latest for tracked branch
git pull origin <branch-name>

# Push changes
git push origin <branch-name>

# Force push (if needed)
git push --force-with-lease origin <branch-name>
```

---

## Latest Update (2026-03-25)

**COMMIT c6238b87 PUSHED:** Comprehensive orchestration workflow and branch analysis tools

### What Was Accomplished
- ✅ Expanded `docs/orchestration-workflow.md` with troubleshooting and conflict prevention
- ✅ Added branch analysis tools (`branch_analysis_tool.py`, `branch_analysis_summary.py`)
- ✅ Documented branch sync architecture with metrics and comparisons
- ✅ Created implementation checklist and quick start guides
- ✅ Removed outdated orchestration documentation files

### Remaining Issues from This Analysis

The following critical issues identified in this analysis still need resolution:

1. **`setup/launch.py` has conflict markers on ALL 12 branches** — Must be resolved
2. **`CLAUDE.md` is wrongly gitignored** — Line 241 of `.gitignore`
3. **`AGENTS.md` has 3 conflict markers** on `orchestration-tools-changes-recovery-framework`
4. **22 agent config files still tracked** — Should be untracked/ignored
5. **`.gitignore` missing patterns** — `.specify/templates/`, `.claude/settings.local.json`, `IFLOW.md`

See "Priority Action Matrix" below for detailed remediation steps.

---

---

## Executive Summary

EmailIntelligenceAider is the **closest worktree to a clean state** among the EmailIntelligence variants. Commit `136c1245` already untracked 76 files on `orchestration-tools` but has **not yet been pushed**. Despite this progress, several issues remain:

1. **`setup/launch.py` has conflict markers on ALL 12 branches** — 82 markers on `main` and `orchestration-tools`, 1 marker on every other branch. This is a universal corruption that must be resolved before any other cleanup.
2. **`CLAUDE.md` is wrongly gitignored** (line 241 of `.gitignore` on `orchestration-tools`), causing it to be MISSING from git despite being a project-level config file that MUST stay tracked.
3. **`AGENTS.md` has 3 conflict markers** on `orchestration-tools-changes-recovery-framework` (21751B — the largest variant).
4. **22 agent config files are still tracked** on `orchestration-tools`; several (`.specify/templates/`, `.claude/settings.local.json`, `IFLOW.md`) should be untracked/ignored.
5. **`orchestration-tools` is the planned canonical source branch** for cleanup propagation to all other branches and worktrees.

---

## Per-Branch Config Matrix

File sizes in bytes. `MISSING` = file does not exist on that branch. `0` = file exists but is empty.

| Branch | AGENTS.md | CLAUDE.md | .gitignore | .gitattributes | .mcp.json | pyproject.toml | setup/pyproject.toml | Conflicts |
|--------|-----------|-----------|------------|----------------|-----------|----------------|----------------------|-----------|
| `001-agent-context-control` | 18823 | 2704 | 1144 | 0 | MISSING | 20 | 3311 | setup/launch.py: 1 marker |
| `001-command-registry-integration` | MISSING | 13369 | 1089 | 0 | MISSING | 20 | 1531 | setup/launch.py: 1 marker |
| `001-orchestration-tools-consistency` | MISSING | MISSING | 1089 | 0 | MISSING | 20 | 1531 | setup/launch.py: 1 marker |
| `001-orchestration-tools-verification-review` | MISSING | 13369 | 1089 | 0 | MISSING | 20 | 1531 | setup/launch.py: 1 marker |
| `feature/task-18-import-validation-test` | 16379 | MISSING | 1144 | 0 | MISSING | 20 | 1991 | setup/launch.py: 1 marker |
| `main` | 15326 | MISSING | 1351 | 0 | 411 | 20 | 2962 | setup/launch.py: **82 markers** |
| `migration-backend-to-src-backend` | 842 | 662 | 1089 | 0 | MISSING | 20 | 1991 | setup/launch.py: 1 marker |
| **`orchestration-tools`** *(current)* | **2879** | **MISSING** | **3128** | **178** | **411** | **MISSING** | **2546** | **setup/launch.py: 82 markers** |
| `orchestration-tools-changes-emailintelligence-cli-20251112` | 16191 | 3226 | 1241 | MISSING | MISSING | 3318 | 3286 | .gitignore: 1 marker |
| `orchestration-tools-changes-recovery-framework` | 21751 | 3224 | 1090 | MISSING | MISSING | 20 | 3286 | AGENTS.md: **3 markers**, setup/launch.py: 1 |
| `scientific` | 16379 | 3402 | 1489 | MISSING | MISSING | 20 | 3286 | .gitignore: 1, setup/launch.py: 1 |
| `task-15-backup-recovery` | 16379 | 3402 | 1489 | MISSING | MISSING | 20 | 3286 | .gitignore: 1, setup/launch.py: 1 |

### Key Observations from the Matrix

- **AGENTS.md** sizes range from 842B to 21751B — massive divergence across branches. Three branches have it MISSING entirely.
- **CLAUDE.md** is present on 7 branches, MISSING on 5 (including `orchestration-tools` where it's gitignored).
- **.gitignore** on `orchestration-tools` is the largest at 3128B (~250 lines) — the most complete version.
- **.gitattributes** only exists (non-empty) on `orchestration-tools` (178B).
- **.mcp.json** only exists on `main` and `orchestration-tools` (411B each).
- **pyproject.toml** (root): Most branches use a 20B stub. `orchestration-tools` has it MISSING. `orchestration-tools-changes-emailintelligence-cli-20251112` has a full 3318B config.
- **setup/pyproject.toml**: Ranges from 1531B to 3311B across branches.

---

## setup/launch.py — Universal Conflict Analysis

**This is the single most critical issue: `setup/launch.py` has unresolved conflict markers on EVERY branch.**

| Severity | Branches | Marker Count |
|----------|----------|--------------|
| 🔴 CRITICAL | `main`, `orchestration-tools` | **82 markers** each |
| 🟡 MEDIUM | All 10 other branches | **1 marker** each |

### Impact

- The file is **non-functional** on `main` and `orchestration-tools` due to 82 conflict markers (likely spanning the entire file).
- Even branches with only 1 marker are technically corrupted — the file won't parse correctly.
- Since `main` has 82 markers, this corruption has been present since before branching for most feature branches (which then partially resolved conflicts, leaving 1 residual marker each).

### Recommended Resolution

1. Identify the correct version of `setup/launch.py` by examining the content between conflict markers on a branch with only 1 marker (simplest to resolve).
2. Resolve on `orchestration-tools` first (canonical source).
3. Propagate the clean version to all other branches.
4. The `main` branch resolution should come from merging the cleaned `orchestration-tools` branch.

---

## .gitignore Analysis (orchestration-tools — 3128B, ~250 lines)

The `orchestration-tools` branch has the most comprehensive `.gitignore` at 3128B. However, it contains several issues:

### 🔴 Critical Issues

| Line | Issue | Impact |
|------|-------|--------|
| **241** | `CLAUDE.md` is listed in `.gitignore` | **CLAUDE.md is MISSING from git** — project-level config file wrongly excluded. Must be removed from `.gitignore` and the file re-added to tracking. |

### 🟡 Missing Patterns

| Pattern | Reason |
|---------|--------|
| `.specify/templates/` | 5 template files are still tracked (agent-file-template.md, checklist-template.md, plan-template.md, spec-template.md, tasks-template.md) — should be ignored |
| `.claude/settings.local.json` | Local-only settings file should never be tracked (contains machine-specific config) |
| `IFLOW.md` | Not listed in the agent MD ignore block — still tracked, should be evaluated for exclusion |

### Conflict Markers in .gitignore on Other Branches

| Branch | Markers |
|--------|---------|
| `orchestration-tools-changes-emailintelligence-cli-20251112` | 1 marker |
| `scientific` | 1 marker |
| `task-15-backup-recovery` | 1 marker |

---

## Agent Config Tracking Analysis (orchestration-tools)

**22 agent config files are currently tracked** on `orchestration-tools`. Below is the should-keep vs. should-remove breakdown:

### ✅ KEEP Tracked (7 files)

These are project-level configuration files that should remain in version control:

| File | Reason |
|------|--------|
| `.claude/settings.json` | Shared project Claude settings |
| `.claude/slash_commands.json` | Team-shared slash commands |
| `.cursor/rules/CLAUDE.mdc` | Cursor rule: Claude integration |
| `.cursor/rules/GEMINI.mdc` | Cursor rule: Gemini integration |
| `.cursor/rules/copilot-instructions.mdc` | Cursor rule: Copilot |
| `.cursor/rules/cursor_rules.mdc` | Cursor rule: base rules |
| `.cursor/rules/overview.mdc` | Cursor rule: project overview |

### ❌ REMOVE from Tracking (15 files)

These are local-only, generated, or agent-specific files that should be gitignored:

| File | Reason |
|------|--------|
| `.claude/mcp.json` | Local MCP server config (machine-specific paths/ports) |
| `.claude/settings.local.json` | **Local-only** settings — never track |
| `.cursor/mcp.json` | Local MCP server config |
| `.cursor/rules/self_improve.mdc` | Agent self-modification rule (non-project) |
| `.cursor/rules/taskmaster/dev_workflow.mdc` | Taskmaster-specific (agent tooling) |
| `.cursor/rules/taskmaster/hamster.mdc` | Taskmaster-specific (agent tooling) |
| `.cursor/rules/taskmaster/taskmaster.mdc` | Taskmaster-specific (agent tooling) |
| `.gemini/settings.json` | Local Gemini settings |
| `.qwen/PROJECT_SUMMARY.md` | Agent-generated summary |
| `.specify/templates/agent-file-template.md` | Agent template (should be ignored) |
| `.specify/templates/checklist-template.md` | Agent template (should be ignored) |
| `.specify/templates/plan-template.md` | Agent template (should be ignored) |
| `.specify/templates/spec-template.md` | Agent template (should be ignored) |
| `.specify/templates/tasks-template.md` | Agent template (should be ignored) |
| `IFLOW.md` | Agent workflow doc (non-project) |

---

## Priority Action Matrix

Actions ordered by priority for the `orchestration-tools` branch (canonical source):

| Priority | Action | Files Affected | Git Commands | Risk |
|----------|--------|----------------|--------------|------|
| **P0** | Resolve `setup/launch.py` conflict markers (82 markers) | 1 file | `git checkout main` → resolve → `git checkout orchestration-tools` → resolve → `git push origin orchestration-tools` | 🔴 HIGH — file is non-functional |
| **P1** | Remove `CLAUDE.md` from `.gitignore` line 241 | .gitignore | `git checkout orchestration-tools` → edit .gitignore line 241 → `git add .gitignore` → `git commit -m "fix: remove CLAUDE.md from gitignore"` → `git push origin orchestration-tools` | 🔴 HIGH — project config missing from git |
| **P1** | Re-add/create `CLAUDE.md` and track it | CLAUDE.md | `git checkout orchestration-tools` → create/restore CLAUDE.md → `git add CLAUDE.md` → `git commit -m "feat: add CLAUDE.md to tracking"` → `git push` | 🔴 HIGH — project config must be tracked |
| **P2** | Untrack 15 agent config files (see REMOVE list above) | 15 files | `git checkout orchestration-tools` → update .gitignore → `git rm --cached <files>` → `git add .gitignore` → `git commit -m "chore: untrack local agent configs"` → `git push` | 🟡 MEDIUM — clutter, potential secret leak |
| **P2** | Add missing `.gitignore` patterns (`.specify/templates/`, `.claude/settings.local.json`, `IFLOW.md`) | .gitignore | `git checkout orchestration-tools` → edit .gitignore → `git add .gitignore` → `git commit -m "chore: add missing gitignore patterns"` → `git push` | 🟡 MEDIUM — prevents re-tracking |
| **P3** | Resolve `AGENTS.md` conflict markers on `orchestration-tools-changes-recovery-framework` | 1 file, 1 branch | `git checkout orchestration-tools-changes-recovery-framework` → resolve 3 markers → `git add AGENTS.md` → `git commit -m "fix: resolve AGENTS.md conflicts"` → `git push origin orchestration-tools-changes-recovery-framework` | 🟡 MEDIUM — 3 markers in 21751B file |
| **P3** | Resolve `.gitignore` conflict markers on 3 branches | 1 file, 3 branches | For each branch: `git checkout <branch>` → resolve → `git add .gitignore` → `git commit` → `git push` | 🟡 MEDIUM — 1 marker each |
| **P4** | Sync with main (65 commits behind) | n/a | `git checkout orchestration-tools` → `git rebase main` → resolve conflicts if any → `git push origin orchestration-tools` (force if needed) | 🟢 LOW — already committed, just needs push |
| **P4** | Evaluate `pyproject.toml` strategy (root stub vs. full config) | 1 file | Review and decide → implement → commit → push | 🟢 LOW — functional divergence |
| **P5** | Propagate cleanup to all 11 other branches | all config files | `git checkout <target-branch>` → `git merge orchestration-tools` or cherry-pick → resolve → push → repeat for all branches | 🟢 LOW — after canonical is clean |

---

## Canonical Source for Cleanup Propagation

**`orchestration-tools` on `EmailIntelligenceAider` is the planned canonical source branch.**

### Propagation Order

```
orchestration-tools (EIAider)     ← CLEAN THIS FIRST
    │
    ├──► other EIAider branches   ← merge/cherry-pick cleanup
    │
    ├──► EmailIntelligence        ← propagate .gitignore, agent config patterns
    ├──► EmailIntelligenceAuto    ← propagate .gitignore, agent config patterns
    └──► EmailIntelligenceGem     ← propagate .gitignore, agent config patterns
```

### Why This Branch

- Already has commit `136c1245` untracking 76 files (most cleanup done).
- Has the most complete `.gitignore` (3128B / ~250 lines).
- Is the only branch with a non-empty `.gitattributes` (178B).
- Has `.mcp.json` tracked (411B) — same as `main`, needs evaluation.
- Fewest remaining issues relative to other worktrees.

---

## References

- **Workspace root:** `/home/masum/github/EmailIntelligenceAider/`
- **Worktree analysis:** `/home/masum/github/WORKTREE_ANALYSIS_REPORT.md`
- **Cross-branch inconsistency:** `/home/masum/github/CROSS_BRANCH_INCONSISTENCY_ANALYSIS.md`
- **Cleanup checklist:** `/home/masum/github/CLEANUP_CHECKLIST.md`
- **Agent tools audit:** `/home/masum/github/AGENT_TOOLS_AUDIT.md`
- **Config investigation plan:** `/home/masum/github/CONFIG_FILE_INVESTIGATION_PLAN.md`
