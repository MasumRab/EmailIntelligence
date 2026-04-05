# Orchestration Workflow Documentation

**Effective Date:** 2025-11-10  
**Model:** Centralized (orchestration-tools as single source of truth)

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Core Concepts](#core-concepts)
4. [File Ownership Matrix](#file-ownership-matrix)
5. [Branch Hierarchy](#branch-hierarchy)
6. [Hook Behavior](#hook-behavior)
7. [Workflow Diagrams](#workflow-diagrams)
8. [Quick Start](#quick-start)
9. [Updating Orchestration Files](#updating-orchestration-files)
10. [Troubleshooting](#troubleshooting)
11. [Merge Conflict Contamination Prevention](#merge-conflict-contamination-prevention)
12. [Maintenance Procedures](#maintenance-procedures)
13. [Implementation Checklist](#implementation-checklist)
14. [FAQ](#faq)

---

## Overview

The `orchestration-tools` branch serves as the **single source of truth** for development environment tooling and configuration management. It maintains scripts, hooks, and configurations that ensure consistency across all project branches while keeping the core email intelligence codebase clean.

---

## Architecture

### Before (Contaminated Model)
```
main (app code + orchestration files)
  ↓ sync ↓
orchestration-tools (app code + orchestration files)
  ↓ sync ↓
feature branches (app code + orchestration files)

❌ Problem: Main is central point, contamination spreads
```

### After (Centralized Model)
```
orchestration-tools (ONLY: setup/, deployment/, config/, scripts/hooks/)
  ↓ one-way sync ↓
  ├─ main (app code only: src/, client/, plugins/)
  ├─ scientific (app code only)
  ├─ feature/* (app code + local orchestration changes)
  └─ other branches

✓ Clean: orchestration-tools is exclusive source of truth
```

---

## Core Concepts

### Separation of Concerns

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION WORKFLOW                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  orchestration-tools branch:                                   │
│  ├─ Contains: Orchestration tooling & shared configs           │
│  └─ Purpose: Development environment management                │
│                                                                 │
│  main/scientific/feature branches:                              │
│  ├─ Contains: Core application code + synced essentials        │
│  └─ Purpose: Feature development & application logic           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Key Rules

1. **Orchestration-tools is the source of truth** for shared configurations
2. **Main/other branches get synced essentials** but not orchestration tooling
3. **Project-specific files stay branch-local** (no orchestration management)
4. **Hooks enforce PR process** for orchestration-managed file changes
5. **Post-merge ensures consistency** across all worktrees

---

## File Ownership Matrix

### Files ONLY in `orchestration-tools` branch (Core Orchestration Files):
- `scripts/` - All orchestration scripts, utilities, and hooks
- `scripts/lib/` - Shared utility libraries (common.sh, error_handling.sh, etc.)
- `scripts/hooks/` - Git hook source files
- `scripts/install-hooks.sh` - Hook installation script
- `scripts/cleanup*.sh` - Cleanup utilities
- `scripts/sync_setup_worktrees.sh` - Worktree synchronization
- `scripts/reverse_sync_orchestration.sh` - Reverse sync utilities
- `scripts/architectural_rule_engine.py` - Code architecture validation

### Files synced TO other branches (orchestration-managed):
- `setup/` - Launch scripts and environment setup (launch.py, launch.sh, etc.)
- `deployment/` - Docker and deployment configurations
- `docs/orchestration*.md` - Orchestration documentation
- `docs/env_management.md` - Environment management docs
- `docs/git_workflow_plan.md` - Git workflow documentation
- `docs/guides/` - Branch switching and workflow guides
- `docs/critical_files_check.md` - File validation documentation
- `pyproject.toml` - Python project configuration
- `requirements*.txt` - Python dependencies
- `uv.lock` - Dependency lock file
- `.gitignore`, `.gitattributes` - Git configuration
- `launch.py` - Main application launcher

### Files that remain BRANCH-SPECIFIC (not orchestration-managed):
- `tsconfig.json` - TypeScript configuration
- `package.json` - Node.js dependencies
- `tailwind.config.ts` - Tailwind CSS configuration
- `vite.config.ts` - Vite build configuration
- `drizzle.config.ts` - Database configuration
- `components.json` - UI component configuration
- All application source code (`src/`, `modules/`, `client/`, `plugins/`)

---

## Branch Hierarchy

| Branch | Purpose | Can modify orchestration files? |
|--------|---------|--------------------------------|
| orchestration-tools | Central source of truth | ✓ YES (authoritative) |
| orchestration-tools-changes | Aggregates agent pushes | ✓ YES (staging) |
| main | Application code | ✗ NO (read-only for orchestration) |
| feature/* | Feature development | ✓ YES (with intent marker) |
| scientific | Scientific branch | ✗ NO (read-only) |

### Sync Direction (One-Way)

```
orchestration-tools (authoritative)
    ↓ sync only
all other branches
```

- **orchestration-tools → main:** Sync on demand via PR
- **orchestration-tools → feature branches:** Sync on demand via cherry-pick
- **main → orchestration-tools:** ✗ BLOCKED (pre-merge-abort hook)
- **feature → orchestration-tools:** Promotion via orchestration-tools-changes branch

---

## Hook Behavior

### pre-commit Hook
**Purpose**: Prevent accidental changes to orchestration-managed files

```
pre-commit Flow:
├── Check current branch
├── If orchestration-tools: Allow all changes
└── If other branch:
    ├── Warn about setup/ changes → Require PR
    ├── Warn about orchestration scripts → Require PR
    ├── Warn about shared configs (.flake8, .pylintrc, etc.) → Require PR
    └── Allow project-specific changes (tsconfig.json, package.json, etc.)
```

### post-commit Hook
**Purpose**: Trigger synchronization after orchestration changes

```
post-commit Flow:
├── Check current branch
├── If orchestration-tools:
│   └── Offer to run worktree sync
└── If other branch: No action
```

### post-merge Hook
**Purpose**: Ensure environment consistency after merges

```
post-merge Flow:
├── Skip if documentation worktree (docs-main, docs-scientific)
├── Sync setup/ directory
├── If main/scientific worktree:
│   ├── Create temp worktree from orchestration-tools
│   ├── Copy setup files and shared configs
│   └── Apply branch-specific configurations
├── Sync orchestration scripts (for reference)
├── Install/update Git hooks
└── Clean up temp worktree
```

### post-push Hook
**Purpose**: Detect orchestration changes and create PRs

```
post-push Flow:
├── Parse push information (local_sha → remote_sha)
├── If orchestration-tools pushed: Log completion
└── If other branch pushed:
    └── Check for orchestration-managed file changes
        ├── If changes detected: Create automatic draft PR
        └── If no changes: Continue normally
```

### post-checkout Hook
**Purpose**: Sync essential files when switching branches

```
post-checkout Flow:
├── Skip if switching TO orchestration-tools
├── Sync setup/ directory
├── Sync deployment/ directory (if exists)
├── Sync shared configuration files (.flake8, .pylintrc, etc.)
├── Sync documentation
├── Install/update Git hooks to .git/hooks/
└── DO NOT sync orchestration tooling (scripts/, etc.)
```

### pre-merge-abort Hook
**Purpose**: Block contamination from main to orchestration-tools

```bash
$ git merge main
fatal: Forbidden merge detected
This would contaminate orchestration-tools
```

**Allowed merges:**
- `orchestration-tools-changes → orchestration-tools` ✓
- Any branch → orchestration-tools (via PR review) ✓
- orchestration-tools → other branches ✓

---

## Workflow Diagrams

### Branch Switching Workflow

```
User runs: git checkout main

post-checkout hook activates:
├── Current branch: main
├── Source branch: orchestration-tools
├── Actions:
│   ├── Sync setup/launch.py → main
│   ├── Sync .flake8 → main
│   ├── Install hooks to main/.git/hooks/
│   └── Skip: scripts/ (orchestration-only)
└── Result: main has clean environment + synced essentials

User runs: git checkout orchestration-tools

post-checkout hook activates:
├── Current branch: orchestration-tools
├── Source branch: main
├── Actions: NONE (skip sync on orchestration-tools)
└── Result: Full orchestration tooling available
```

### Development Workflow

```
Developer working on feature:

1. On main branch:
   ├── Edit: src/components/Button.tsx ✓ (project-specific)
   ├── Edit: tsconfig.json ✓ (branch-specific)
   ├── Edit: setup/launch.py ⚠️ (orchestration-managed)
   └── pre-commit: "WARNING: setup/ changes require PR"

2. Push to feature branch:
   ├── post-push detects setup/launch.py change
   ├── Creates automatic draft PR to orchestration-tools
   └── Developer reviews and merges PR

3. Merge orchestration changes:
   ├── post-merge syncs to all branches
   └── All worktrees get updated setup/launch.py
```

### File Synchronization Flow

```
orchestration-tools (source of truth)
├── setup/launch.py
├── .flake8
├── scripts/install-hooks.sh
└── scripts/hooks/pre-commit

↓ post-checkout syncs ↓

main/scientific branches
├── setup/launch.py ← synced
├── .flake8 ← synced
├── .git/hooks/pre-commit ← installed
└── scripts/ ← NOT synced (orchestration-only)
```

---

## Quick Start

### For New Developers

```bash
# 1. Clone the repository
git clone https://github.com/MasumRab/EmailIntelligence.git
cd EmailIntelligence

# 2. Install orchestration hooks
bash scripts/install-hooks.sh

# 3. Set up development environment
python setup/launch.py setup

# 4. Start development
python setup/launch.py run --dev
```

### For Existing Contributors

```bash
# Update to latest orchestration
git pull origin main
# Hooks will auto-sync during checkout
```

---

## Updating Orchestration Files

### Developer on Feature Branch
1. Make orchestration changes locally (setup/, deployment/, etc.)
2. Mark as intentional: `scripts/orchestration-intent.sh mark file.sh`
3. Push to feature branch: `git push origin feature-name`

### Agent/Automation
1. Detect orchestration changes
2. Extract to orchestration-tools-changes (GitHub Actions)
3. Debounce aggregates multiple pushes (5-second wait)
4. Single PR created: orchestration-tools-changes → orchestration-tools

### Approval
1. Review PR on orchestration-tools
2. Merge when ready (or cherry-pick selective files)
3. All branches can sync from orchestration-tools

### Sync to Other Branches
1. On main: `git pull origin orchestration-tools` (cherry-pick only specific files)
2. On feature: `git merge orchestration-tools` (selective, respecting intent markers)
3. On scientific: Manual review + merge (if compatible)

---

## Troubleshooting

### "Scripts directory shouldn't be in main branch"
**Cause**: Orchestration tooling was accidentally committed to main  
**Fix**: Remove scripts/ from main, ensure only orchestration-tools has it

### "Pre-commit warns about tsconfig.json changes"
**Cause**: tsconfig.json is incorrectly marked as orchestration-managed  
**Fix**: tsconfig.json is project-specific, warnings should not appear

### "Post-checkout syncs too many files"
**Cause**: Hook syncing orchestration source files to other branches  
**Fix**: Only sync essentials (setup/, shared configs), not tooling

### "Changes to setup/ files blocked"
```
Error: Changes to setup/ files should only be made in the 'orchestration-tools' branch
```
**Solution:**
```bash
# Move changes to orchestration-tools branch
git stash
git checkout orchestration-tools
git stash pop
# Make changes and commit
git push origin orchestration-tools
```

---

## Merge Conflict Contamination Prevention

### Background

In December 2025, a repository-wide contamination was discovered where **252 of 435 branches (58%)** had committed merge conflict markers into `.gitignore` and `.gitattributes`.

#### Root Cause Analysis

| Date | Commit | Issue |
|------|--------|-------|
| Nov 25, 2025 | `ab35f4ef` | Clean merge (0 conflicts) |
| Dec 16, 2025 | `2b422cfe` | **Revert introduced 4 conflict markers** |
| Dec 21, 2025 | `0199e802` | Added 1 more conflict (128 branches) |
| Jan 4, 2026 | `4228e058` | Merge compounded to 6 conflicts (90 branches) |

**The Problem:** A `git revert` of a merge commit incorrectly re-introduced conflict markers that were resolved in the original merge.

### Prevention Rules

#### Rule 1: Never Commit Conflict Markers
```bash
# Before any commit, check for conflict markers
grep -r "<<<<<<< HEAD\|=======\|>>>>>>>" --include="*.py" --include="*.md" --include=".gitignore" --include=".gitattributes" .
# Should return empty
```

#### Rule 2: Validate Reverts of Merge Commits
```bash
# After reverting a merge, verify no conflicts introduced
git show HEAD:.gitignore | grep -c "<<<<<<< HEAD"
# Should be 0

git show HEAD:.gitattributes | grep -c "<<<<<<< HEAD"
# Should be 0
```

#### Rule 3: Use Pre-Commit Hook for Conflict Detection
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Check for accidental conflict marker commits
if git diff --cached | grep -q "<<<<<<< HEAD"; then
    echo "ERROR: Conflict markers detected in staged changes"
    echo "Resolve conflicts before committing"
    exit 1
fi
```

### Detection Commands

#### Check Single Branch
```bash
# Check current branch for conflict markers
grep -c "<<<<<<< HEAD" .gitignore .gitattributes 2>/dev/null
# Should be 0 for both files
```

#### Check All Remote Branches
```bash
# Scan all remote branches for .gitignore conflicts
for branch in $(git branch -r | grep -v HEAD); do
  conflicts=$(git show "$branch:.gitignore" 2>/dev/null | grep -c "<<<<<<< HEAD")
  if [ "$conflicts" -gt 0 ]; then
    echo "$branch: $conflicts conflicts"
  fi
done
```

#### Find Unique .gitignore Versions
```bash
# Count unique .gitignore versions across branches
git branch -r | grep -v HEAD | while read branch; do
  git show "$branch:.gitignore" 2>/dev/null | md5sum | cut -d' ' -f1
done | sort -u | wc -l
# High number indicates fragmentation
```

### Remediation Procedure

#### For Single Branch
```bash
# 1. Checkout the affected branch
git checkout <branch>

# 2. Get clean .gitignore from orchestration-tools
git checkout origin/orchestration-tools -- .gitignore

# 3. Verify no conflicts
grep -c "<<<<<<< HEAD" .gitignore  # Should be 0

# 4. Commit the fix
git commit -m "fix: clean .gitignore conflict markers"

# 5. Push
git push origin <branch>
```

#### For Bulk Remediation (Multiple Branches)
```bash
# Create a script to fix all affected branches
for branch in $(git branch -r | grep -v HEAD); do
  conflicts=$(git show "$branch:.gitignore" 2>/dev/null | grep -c "<<<<<<< HEAD")
  if [ "$conflicts" -gt 0 ]; then
    echo "Fixing $branch..."
    git checkout "$branch"
    git checkout origin/orchestration-tools -- .gitignore .gitattributes
    git commit -m "fix: remove committed conflict markers from .gitignore/.gitattributes"
    git push origin "$branch"
  fi
done
```

### Contamination Metrics

| Metric | Target | Current State |
|--------|--------|---------------|
| Branches with .gitignore conflicts | 0 | 252 (58%) |
| Branches with .gitattributes conflicts | 0 | 83 (19%) |
| Unique .gitignore versions | 1-3 | 71 |
| .gitignore line count variance | ±10 lines | 78-311 lines |

### Post-Remediation Verification

```bash
# Verify all branches are clean
conflict_count=0
for branch in $(git branch -r | grep -v HEAD); do
  conflicts=$(git show "$branch:.gitignore" 2>/dev/null | grep -c "<<<<<<< HEAD")
  conflict_count=$((conflict_count + conflicts))
done
echo "Total conflict markers: $conflict_count"
# Should be 0
```

### "Hook installation failed"
**Symptoms:** Hooks not working, commands failing  
**Solution:**
```bash
# Check permissions
ls -la .git/hooks/

# Reinstall hooks
bash scripts/install-hooks.sh --force

# Verify hook executability
chmod +x .git/hooks/*
```

---

## Maintenance Procedures

### Validation Tools

#### Check Context Purity
```bash
./scripts/validate-orchestration-context.sh
# Exit 0 = clean, 1 = contaminated
```

#### Checks Performed
- No src/, client/, plugins/ on orchestration-tools
- No AGENTS.md, CRUSH.md, GEMINI.md, IFLOW.md, LLXPRT.md
- setup/launch.sh has no recursive references
- setup/launch.py exists and is valid

### Regular Maintenance

#### Weekly Tasks
- [ ] Review open orchestration PRs
- [ ] Update dependencies in `orchestration-tools`
- [ ] Test hook functionality across branches
- [ ] Clean up old worktrees

#### Monthly Tasks
- [ ] Audit orchestration-managed files
- [ ] Review hook performance
- [ ] Update documentation
- [ ] Test recovery procedures

---

## Implementation Checklist

- [x] Revert contamination commit 421317c
- [x] Update extract-orchestration-changes.yml (main → orchestration-tools)
- [x] Create pre-merge-abort hook
- [x] Create validate-orchestration-context.sh
- [ ] Activate pre-merge-abort hook in all local repos
- [ ] Document in README / CONTRIBUTING
- [ ] Update branch protection rules on GitHub
- [ ] Train team on new workflow

### Contamination Cleanup (Discovered Mar 2026)

- [ ] Add pre-commit hook for conflict marker detection
- [ ] Remediate 252 branches with .gitignore conflicts
- [ ] Remediate 83 branches with .gitattributes conflicts
- [ ] Consolidate 71 unique .gitignore versions to 1 canonical
- [ ] Apply CLEANUP_CHECKLIST.md agent config changes (~88 files)
- [ ] Verify all branches pass conflict marker check

---

## FAQ

**Q: Can I modify setup/launch.py on main?**  
A: Yes, but changes won't be synchronized to orchestration-tools. Make changes on orchestration-tools or feature branch and promote.

**Q: What if I accidentally merge main → orchestration-tools?**  
A: pre-merge-abort hook blocks it. If already merged, `git revert` the merge commit.

**Q: How do branches get orchestration updates?**  
A: Manually cherry-pick from orchestration-tools, or use: `git merge -X theirs orchestration-tools` (for full merge).

**Q: Can I test orchestration changes on feature branch first?**  
A: Yes! Mark with intent marker, test, then promote via orchestration-tools-changes.

**Q: How did 58% of branches get conflict markers?**  
A: A Dec 16, 2025 revert of a merge commit (`2b422cfe`) incorrectly re-introduced conflict markers. The original merge was clean, but the revert corrupted .gitignore and .gitattributes. See "Merge Conflict Contamination Prevention" section.

**Q: How do I fix conflict markers in my branch?**  
A: `git checkout origin/orchestration-tools -- .gitignore .gitattributes && git commit -m "fix: clean conflict markers"`

**Q: Should I commit GEMINI.md, QWEN.md, etc.?**  
A: No. Per CLEANUP_CHECKLIST.md, these should be untracked (`git rm --cached`) and added to .gitignore. They're user-level configs that should live in `~/github/` or individual worktrees.
