# Orchestration System - Machine-Readable Specification

**Version**: 1.0
**For**: AI Agents, Developers, CI/CD Systems
**Last Updated**: November 9, 2025

---

## 🎯 System Purpose

**Goal**: Keep setup/deployment/config files synchronized across all branches while allowing independent development.

**Mechanism**: Git hooks on orchestration-tools branch propagate changes to all other branches.

**Constraint**: Only orchestration-tools is source of truth. All other branches receive from it, never write to it.

---

## 📋 Core Concepts

### Branches

```
orchestration-tools (SOURCE OF TRUTH)
  ↓
  Git Hooks (post-checkout, post-merge, post-commit, post-push, pre-commit)
  ↓
  All other branches (main, scientific, feature/*, etc.)
```

### Managed Files

```
Files that SYNC automatically from orchestration-tools → all branches:

setup/                     # All setup scripts
  ├─ setup_environment_system.sh
  ├─ setup_environment_python.sh
  ├─ setup_environment_node.sh
  └─ setup_env*.py

deployment/                # Deployment configurations
  ├─ test_stages.py
  ├─ deployment_config.yaml
  └─ ...

scripts/                   # Utility scripts (except orchestration extraction)
  ├─ hooks/                # Git hooks
  ├─ disable-hooks.sh
  ├─ enable-hooks.sh
  └─ ... (but NOT extract-orchestration-changes.sh - stays isolated)

Config files:
  ├─ .flake8
  ├─ .pylintrc
  ├─ setup.cfg
  ├─ pyproject.toml
  ├─ pytest.ini
  ├─ tsconfig.json
  ├─ package.json
  ├─ vite.config.ts
  ├─ tailwind.config.ts
  ├─ drizzle.config.ts
  └─ components.json
```

### Files that DON'T sync

```
Application code:
  - src/
  - client/
  - plugins/
  - tests/ (application tests only)

Branch-specific:
  - docs/ (branch-specific documentation)
  - .github/workflows/ (branch-specific workflows, except extracts)
  - README.md (branch-specific)

Configuration:
  - .env (local only, never synced)
  - .taskmaster/ (local only, never synced)
```

---

## 🔄 Sync Propagation Model

### When Files Sync

```
SCENARIO 1: Developer switches branches
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ git checkout main
  ↓
post-checkout hook triggers (unless DISABLE_ORCHESTRATION_CHECKS=1)
  ↓
Detects: current_branch != orchestration-tools
  ↓
Syncs managed files FROM orchestration-tools → current branch
  ↓
If .git/hooks.disabled exists:
  → SKIP syncing (developer disabled hooks)
  → Log: "Hooks disabled, skipping orchestration sync"
  ↓
Result: Your local main now has latest setup files from orchestration-tools


SCENARIO 2: Developer commits on orchestration-tools
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ git commit -m "feat: update setup script"  (on orchestration-tools)
  ↓
pre-commit hook validates (checks for violations)
post-commit hook logs (informational)
  ↓
Commit succeeds, stays local
  ↓
Developer pushes: $ git push origin orchestration-tools
  ↓
Remote receives commit on orchestration-tools


SCENARIO 3: Developer pulls orchestration-tools
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ git pull origin orchestration-tools  (while on orchestration-tools)
  ↓
Merge happens
  ↓
post-merge hook triggers
  ↓
Validates: current_branch == orchestration-tools
  ↓
No sync needed (already on source of truth)
  ↓
Result: Local orchestration-tools updated


SCENARIO 4: Developer merges orchestration-tools into feature branch
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ git checkout feature/my-feature
$ git merge origin/orchestration-tools
  ↓
Merge happens (gets latest setup files in merge commit)
  ↓
post-merge hook triggers
  ↓
Detects: current_branch != orchestration-tools
  ↓
Syncs managed files again (ensures consistency)
  ↓
Result: feature/my-feature has latest setup files

```

---

## 🚫 Constraints & Safety Rules

### RULE 1: Write to Source Only

```
✅ SAFE: Modify files on orchestration-tools
  $ git checkout orchestration-tools
  $ nano setup/setup_environment_system.sh
  $ git commit -m "feat: ..."
  $ git push origin orchestration-tools

❌ UNSAFE: Modify setup files on other branches (will be overwritten)
  $ git checkout main
  $ nano setup/setup_environment_system.sh  # DON'T DO THIS
  $ git commit -m "fix: ..."  # Will be overwritten next sync!
  → Post-merge will sync from orchestration-tools and overwrite your change
```

### RULE 2: One-Way Sync Only

```
✅ CORRECT: orchestration-tools → all other branches (auto)

❌ WRONG: other branches → orchestration-tools (manual only)
  → Requires reverse-sync script (scripts/reverse_sync_orchestration.sh)
  → Manual, intentional, documented
  → Never automatic
```

### RULE 3: Hooks can be disabled

```
✅ ALLOW: Developer disables hooks for independent development
  $ ./scripts/disable-hooks.sh
  # Now can work on setup files without auto-sync
  # .git/hooks.disabled signals to hooks to skip

❌ NEVER: Commit with hooks disabled without re-enabling
  → Creates surprise when hooks re-enabled
  → Sync happens, local changes may conflict

✅ RE-ENABLE after independent work:
  $ ./scripts/enable-hooks.sh
  # Hooks restored, next operation triggers sync
```

---

## 🔍 How to Determine Current State

### Check if hooks are active

```bash
# Case 1: Hooks enabled (normal state)
$ ls -la .git/hooks/
  post-checkout  post-commit  post-merge  ...  [all present]

Result: Hooks ACTIVE → Syncing will happen

# Case 2: Hooks disabled
$ ls -la .git/hooks.disabled/
  post-checkout  post-commit  post-merge  ...  [all present]
$ ls -la .git/hooks/
  [empty or missing]

Result: Hooks DISABLED → No syncing happens
  Next operation will check .git/hooks.disabled flag
```

### Check which branch you're on

```bash
$ git branch
  main
  feature/my-feature
* orchestration-tools    ← Source of truth
  scientific
```

### Check if orchestration-tools has uncommitted changes

```bash
$ git status

On branch orchestration-tools
Your branch is [ahead|behind|up to date]

Changes not staged:
  modified: setup/setup_environment_system.sh  ← Will NOT sync yet

To sync to other branches, must commit & push
```

---

## 📊 Decision Tree for Agents

### "I want to modify a setup file"

```
START: Want to modify setup/setup_environment_system.sh

├─ Is the file in the MANAGED_FILES list?
│  ├─ YES → Continue
│  └─ NO → Modify wherever you want, no sync needed
│
├─ Are you on orchestration-tools branch?
│  ├─ YES → ✅ Safe to modify
│  │   $ git checkout orchestration-tools
│  │   $ nano setup/...
│  │   $ git commit && git push
│  │   ✓ Change propagates to all branches on next sync
│  │
│  └─ NO → ⚠️ Risky, will be overwritten
│      ├─ Option A: Switch to orchestration-tools
│      │   $ git checkout orchestration-tools
│      │   [make change]
│      │   $ git commit && git push
│      │
│      ├─ Option B: Create feature branch from orchestration-tools
│      │   $ git checkout orchestration-tools
│      │   $ git checkout -b feature/setup-improvement
│      │   [make changes]
│      │   $ git commit && git push origin feature/setup-improvement
│      │   [create PR to orchestration-tools]
│      │
│      └─ Option C: Temporarily disable hooks (NOT RECOMMENDED)
│          $ ./scripts/disable-hooks.sh
│          [make change]
│          [merge back to orchestration-tools when ready]
│          $ ./scripts/enable-hooks.sh
│
END
```

### "I want to work on application code without auto-sync interference"

```
START: Want to modify src/ or application code

├─ Are hooks currently enabled?
│  ├─ YES (normal) → No problem
│  │   ✓ Application files don't sync anyway
│  │   ✓ Can modify freely
│  │
│  └─ NO (hooks disabled) → Re-enable immediately
│      $ ./scripts/enable-hooks.sh
│
├─ Can I modify setup files on this branch?
│  ├─ NO (they will be overwritten)
│  │
│  ├─ YES (hooks disabled) → RISKY
│  │   ⚠️ Re-enable hooks when done
│  │
│  └─ UNSURE → Check: git branch
│      If not orchestration-tools: Don't modify setup files
│
END
```

### "I want to merge main into orchestration-tools"

```
START: Feature complete in main, want orchestration-tools to have it

├─ Should orchestration-tools have this feature?
│  ├─ YES → Use normal merge
│  │   $ git checkout orchestration-tools
│  │   $ git merge main  ← Brings in app code
│  │   ✓ Setup files stay as-is
│  │   ✓ No conflict expected
│  │
│  └─ NO → Don't merge
│
├─ After merge, test:
│  $ ./scripts/disable-hooks.sh
│  [run tests]
│  $ ./scripts/enable-hooks.sh
│
END
```

### "I merged orchestration-tools into my branch, what happens?"

```
START: Just did: git merge orchestration-tools (on feature branch)

├─ Merge result:
│  ✓ Your app code stays (feature branch code)
│  ✓ Your setup files updated to match orchestration-tools
│  ✓ post-merge hook syncs to ensure consistency
│
├─ Next sync:
│  $ git checkout other-branch
│  ✓ post-checkout hook triggers
│  ✓ Syncs setup files from orchestration-tools
│
END
```

---

## 🛡️ Safety Guardrails

### For Developers

| Action | Safety Level | Reason |
|--------|--------------|--------|
| Modify setup/ on orchestration-tools | ✅ SAFE | Direct source |
| Modify setup/ on other branches | 🔴 DANGEROUS | Will be overwritten |
| Commit on orchestration-tools | ✅ SAFE | Source of truth |
| Push to orchestration-tools | ⚠️ REQUIRES REVIEW | Affects all branches |
| Run disable-hooks.sh | ✅ SAFE | Intentional, reversible |
| Leave hooks disabled | 🔴 DANGEROUS | Creates surprise syncs |
| Merge main → orchestration-tools | ✅ SAFE | One-way acceptable |
| Merge orchestration-tools → main | ✅ SAFE | Brings latest setup |
| Rebase on orchestration-tools | ⚠️ RISKY | Rewrites history |
| Force push to orchestration-tools | 🔴 FORBIDDEN | Breaks other branches |

### For CI/CD & Agents

```
BEFORE modifying any file:

1. Check: Is this in MANAGED_FILES?
   $ grep -q "$(git diff)" MANAGED_FILES

2. If YES and NOT on orchestration-tools:
   ❌ STOP - Request to switch branch or use reverse-sync

3. If YES and on orchestration-tools:
   ✅ Proceed - Will propagate to all branches

4. If NO:
   ✅ Proceed - No sync implications

BEFORE pushing to orchestration-tools:

1. Check: What files are in this commit?
   $ git show --stat

2. If contains SETUP/DEPLOYMENT files:
   ⚠️ WARN: "This affects all branches"

3. If contains APP CODE:
   ⚠️ WARN: "App code in orchestration-tools: intentional?"

BEFORE merging to main/scientific:

1. Check: Are setup files consistent with orchestration-tools?
   $ git diff orchestration-tools -- setup/ deployment/

2. If differences exist:
   ⚠️ WARN: "Setup files diverging from source"
```

---

## 🔗 Hook Behavior Reference

| Hook | Trigger | When orchestration-tools? | When other branch? |
|------|---------|---------------------------|-------------------|
| **post-checkout** | Branch switch | Skip (already source) | Sync managed files |
| **post-merge** | After merge | Skip | Sync managed files |
| **post-commit** | After commit | Log state | Log state |
| **pre-commit** | Before commit | Validate | Validate |
| **post-push** | After push | Warn developers | Warn developers |

---

## 🐛 Troubleshooting Decision Tree

### "Setup files aren't syncing"

```
Question 1: Are hooks enabled?
  $ ls -la .git/hooks.disabled/

  ├─ Files exist (hooks disabled)
  │  → Run: ./scripts/enable-hooks.sh
  │
  └─ Directory doesn't exist (hooks enabled)
     → Continue to Question 2

Question 2: Which branch are you on?
  $ git branch

  ├─ orchestration-tools
  │  → Syncing not needed (you're source)
  │
  └─ Other branch (main, feature/*, etc.)
     → Continue to Question 3

Question 3: When did you last sync?
  $ git log --oneline -1 orchestration-tools
  $ git log --oneline -1 HEAD

  ├─ orchestration-tools is ahead
  │  → Run: git merge origin/orchestration-tools
  │  → OR: git checkout another-branch && back
  │
  └─ Same commits
     → Setup files should be in sync
     → Check: git status setup/
```

### "I modified setup files on main and they disappeared"

```
Diagnosis: post-merge/post-checkout synced over your changes

Why it happened:
  1. You modified setup/ on main (not orchestration-tools)
  2. Someone pushed to orchestration-tools
  3. You pulled or switched branches
  4. post-merge/post-checkout ran
  5. Setup files synced from orchestration-tools, overwriting yours

Recovery:
  $ git reflog
  → Find commit before sync
  $ git show COMMIT_SHA:setup/filename
  → View your changes
  $ git checkout orchestration-tools
  [re-apply your changes]
  $ git commit && git push

Prevention:
  Always modify setup files on orchestration-tools, not other branches
```

---

## 📐 System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION SYSTEM ARCHITECTURE            │
└──────────────────────────────────────────────────────────────┘

LOCAL GIT REPOSITORY
├─ orchestration-tools (source of truth)
│  ├─ setup/
│  ├─ deployment/
│  ├─ scripts/hooks/
│  ├─ config files
│  └─ commits → push origin/orchestration-tools
│
├─ main (develops in parallel)
│  ├─ setup/ (synced copy)
│  ├─ deployment/ (synced copy)
│  ├─ src/ (application code)
│  └─ post-checkout hook → syncs if behind
│
├─ scientific (develops in parallel)
│  ├─ setup/ (synced copy)
│  ├─ deployment/ (synced copy)
│  ├─ src/ (advanced features)
│  └─ post-checkout hook → syncs if behind
│
└─ feature/* (many feature branches)
   ├─ setup/ (synced copy)
   ├─ deployment/ (synced copy)
   ├─ src/ (feature code)
   └─ post-checkout hook → syncs on switch

REMOTE GITHUB
├─ origin/orchestration-tools
│  ├─ Receive pushes from orchestration-tools
│  └─ Source for all other branches
│
├─ origin/main
├─ origin/scientific
└─ origin/feature/*
   └─ Pull latest orchestration-tools if needed

SYNC FLOW
┌─ orchestration-tools (local)
├─→ push origin/orchestration-tools
├─→ pull from origin/orchestration-tools
├─→ post-checkout hook [if on other branch]
└─→ Setup files sync to that branch
```

---

## 🎓 Examples for LLM Agents

### Example 1: Safe modification pattern

```bash
# Task: Fix setup script bug

# Step 1: Verify orchestration-tools is source of truth
$ git branch
* orchestration-tools ✓

# Step 2: Make changes
$ nano setup/setup_environment_python.sh
# ... fix bug ...

# Step 3: Test locally
$ bash setup/setup_environment_python.sh

# Step 4: Commit (always with clear message)
$ git add setup/setup_environment_python.sh
$ git commit -m "fix: resolve python setup timeout issue"

# Step 5: Push (this syncs to all branches)
$ git push origin orchestration-tools

# Step 6: Verify on other branches (next time they sync)
$ git checkout main
# post-checkout hook runs automatically
# Verifies: setup/setup_environment_python.sh updated ✓
```

### Example 2: Feature branch with setup changes

```bash
# Task: Improve Node setup as part of feature

# Step 1: Create feature branch FROM orchestration-tools
$ git checkout orchestration-tools
$ git pull origin orchestration-tools  # Latest
$ git checkout -b feature/node-setup-improvement

# Step 2: Make changes
$ nano setup/setup_environment_node.sh

# Step 3: Create PR
$ git push origin feature/node-setup-improvement
# [Create PR in GitHub: feature/node-setup-improvement → orchestration-tools]

# Step 4: After PR approved & merged
# orchestration-tools receives commit
# Other branches sync on next post-checkout/post-merge

# Step 5: Delete feature branch (cleanup)
$ git branch -d feature/node-setup-improvement
```

### Example 3: Risky pattern (AVOID)

```bash
# ❌ ANTI-PATTERN: Modifying setup on main

$ git checkout main
$ nano setup/setup_environment_system.sh  # Modifying synced file!
$ git commit -m "feat: update setup"
$ git push origin main

# PROBLEM: Next sync from orchestration-tools OVERWRITES your change
# When someone pulls orchestration-tools or switches branches:
# post-merge/post-checkout hook runs
# → Syncs setup/ from orchestration-tools
# → Your local main setup/ change is GONE

# FIX: Always make setup changes on orchestration-tools
```

---

## ✅ Validation Checklist

Before proposing changes to setup/deployment/config files:

- [ ] Changes are on orchestration-tools branch
- [ ] Commit message describes the change (not just "update")
- [ ] Change has been tested locally
- [ ] No managed files modified on other branches
- [ ] Hooks are enabled (unless temporarily disabled with reason)
- [ ] Ready to propagate to all branches (intentional, approved)

---

**For Questions**: Refer to ORCHESTRATION.md for quick reference
**For Detailed Workflows**: See orchestration-push-workflow.md
**For Hook Details**: See ORCHESTRATION_HOOK_MANAGEMENT.md
