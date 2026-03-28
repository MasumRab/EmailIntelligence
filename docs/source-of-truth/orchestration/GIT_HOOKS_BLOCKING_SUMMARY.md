# Git Hooks Blocking & Triggering Summary

**Status**: Current behavior documented  
**Date**: 2025-11-18 17:35  
**Branch**: orchestration-tools  

---

## Overview

This document summarizes what git operations STOP commits from being made and the scenarios where they are triggered.

---

## Git Operations That Can Block Commits

| Operation | Hook | Blocks? | Scenario |
|-----------|------|---------|----------|
| `git commit` | pre-commit | **YES** | Large files >50MB OR sensitive data detected |
| `git push` | N/A | **NO** | No push hooks installed |
| `git pull` | N/A | **NO** | No pull hooks |
| `git merge` | post-merge | **NO** | Info-only, non-blocking |
| `git checkout` | post-checkout | **NO** | Info-only, non-blocking |

---

## 1. Pre-Commit Hook (`scripts/hooks/pre-commit`)

### ✓ WHAT IT DOES
Runs **before** commit is created. Can **BLOCK** the commit.

### ✗ BLOCKING CONDITIONS (Exit Code 1)

Only **2 conditions** block commits:

#### Condition 1: Large Files Detected
```bash
# Blocks if file > 50MB
LARGE_FILES=$(echo "$STAGED_FILES" | xargs ls -l | awk '$5 > 50000000')
if [[ -n "$LARGE_FILES" ]]; then
    exit 1  # BLOCKS COMMIT
fi
```

**Scenario**: User tries to commit file > 50MB  
**Error Message**: "Large files detected (>50MB): [filename]"  
**Branch**: ALL branches  
**Solution**: Use Git LFS or remove file

#### Condition 2: Sensitive Data Detected
```bash
# Blocks if password/secret/key/token found in staged files
if git diff --cached | xargs grep -l "password\|secret\|key\|token"; then
    exit 1  # BLOCKS COMMIT (with warning)
fi
```

**Scenario**: User tries to commit with plaintext secrets  
**Error Message**: "WARNING: Potential sensitive data detected"  
**Branch**: ALL branches  
**Solution**: Remove secrets and .gitignore them

### ✓ NON-BLOCKING CHECKS (Exit Code 0)

Everything else is **informational only**:

| Check | Triggered On | Result |
|-------|--------------|--------|
| Script permissions | orchestration-tools branches | Makes executable (non-blocking) |
| CLI validation | orchestration-tools branches | Info message (non-blocking) |
| Task Master check | main/scientific branches | Info message (non-blocking) |
| Task Master config | main/scientific branches | Info message (non-blocking) |

### Branch-Specific Behavior

**orchestration-tools & orchestration-tools-\***
```bash
# Checks:
# - Makes scripts executable (chmod +x)
# - Validates emailintelligence_cli.py present (info)
# - Non-blocking, commit proceeds
```

**main & scientific**
```bash
# Checks:
# - Task Master directory present (info)
# - setup/setup_environment_system.sh present (info)
# - Non-blocking, commit proceeds
```

**taskmaster**
```bash
# Checks:
# - AGENT.md present (info)
# - Task Master scripts present (info)
# - Non-blocking, commit proceeds
```

---

## 2. Post-Commit Hook (`scripts/hooks/post-commit`)

### ✓ WHAT IT DOES
Runs **after** commit succeeds. **CANNOT** block commits (already created).

### ✗ BLOCKING CONDITIONS

**NONE** - This hook runs after commit, so it cannot block.

```bash
# Exit code 0 always - hook never blocks
exit 0
```

### ✓ ACTIONS PERFORMED

**Info Checks** (non-blocking):
- Validates CLI script present
- Checks hook consistency
- Validates setup directory integrity (on main/scientific)
- Checks Task Master JSON validity (on taskmaster)

**Actions** (non-blocking):
- Logs commit to orchestration tracking
- Reports large commits (>100 changes)
- Validates JSON structure (warnings only)

**Branch-Specific Behavior**

| Branch | Action |
|--------|--------|
| orchestration-tools* | Validate CLI present, check hook consistency |
| main/scientific | Check shared files changed, validate setup dir |
| taskmaster | Validate JSON structure, check task files |

---

## 3. Post-Merge Hook (`scripts/hooks/post-merge`)

### ✓ WHAT IT DOES
Runs **after** merge succeeds. **CANNOT** block merges.

### ✗ BLOCKING CONDITIONS

**NONE** - Explicitly designed NOT to block:

```bash
# IMPORTANT: Do NOT force sync of orchestration files
# Developers should control synchronization explicitly
# Automatic sync on merge can cause unexpected file changes
```

### ✓ ACTIONS PERFORMED

**Info Checks** (non-blocking):
- Validates branch name (detects unknown branches)
- Checks critical files present (info only)
- Verifies Task Master isolation (info only)
- Updates hooks if changed (optional, safe)

**Hook Updates** (on orchestration-tools branches):
```bash
if [[ "$CURRENT_BRANCH" == "orchestration-tools"* ]]; then
    # Update hooks if orchestration-tools commit changed
    # Non-blocking, proceed with merge
fi
```

---

## 4. Post-Checkout Hook (`scripts/hooks/post-checkout`)

### ✓ WHAT IT DOES
Runs **after** branch switch succeeds. **CANNOT** block checkout.

### ✗ BLOCKING CONDITIONS

**NONE** - Explicitly designed NOT to block:

```bash
# IMPORTANT: Do NOT force sync or require approval on branch switch
# Branch switching must be fast and unblocked for normal workflows
```

### ✓ ACTIONS PERFORMED

**Info Checks** (non-blocking):
- Reports current branch
- Checks critical files present (info only)
- Verifies Task Master isolation (info only)
- Reports Task Master worktree branch

**Hook Updates** (on orchestration-tools branches):
```bash
if [[ "$CURRENT_BRANCH" == "orchestration-tools"* ]]; then
    # Update hooks if orchestration-tools commit changed
    # Non-blocking, proceed with checkout
fi
```

---

## 5. Push Hook

### ✓ WHAT IT DOES

**Nothing** - No push hook is installed.

```bash
# No scripts/hooks/post-push implementation
# (post-push exists but does minimal validation)
```

### ✗ BLOCKING CONDITIONS

**NONE** - No push validation.

---

## Summary Table: What Actually Blocks Commits

| Git Operation | Hook | Blocks? | Condition |
|---------------|------|---------|-----------|
| **`git commit`** | pre-commit | **YES** | File > 50MB OR password/secret/key/token found |
| `git push` | N/A | NO | - |
| `git pull` | N/A | NO | - |
| `git merge` | post-merge | NO | - |
| `git checkout` | post-checkout | NO | - |

**Key Insight**: Only **pre-commit** hook can block operations, and only for 2 reasons.

---

## Exit Codes

### Pre-Commit Hook

```bash
exit 0  # Commit allowed
exit 1  # Commit BLOCKED (large file or sensitive data)
```

### All Other Hooks

```bash
exit 0  # Always - cannot block operations
```

---

## Environment Variables

### Control Flags

```bash
# Disable all orchestration checks
export DISABLE_ORCHESTRATION_CHECKS=1
git commit ...  # Skips pre-commit checks

# Recursion prevention (internal use)
export ORCHESTRATION_SYNC_ACTIVE=1
```

### Logging

```bash
# Optional orchestration logging
export ORCHESTRATION_LOG="/path/to/log.txt"
# Each commit logged to file
```

---

## Current Issues with This Design

### ✗ Problems Identified

1. **Overly Complex Hooks**
   - Pre-commit: 124 lines but only 2 blocking conditions
   - Post-commit: 131 lines but doesn't block anything
   - Post-merge: 75 lines but doesn't block anything
   - Post-checkout: 70 lines but doesn't block anything

2. **Confusing Purpose**
   - Hooks mixing concerns: blocking + info + distribution
   - Users don't know what will block vs. what's just info
   - Hard to understand hook responsibilities

3. **Distribution Logic in Hooks**
   - post-commit tries to sync files
   - post-merge tries to sync hooks
   - post-checkout tries to sync hooks
   - But these don't block, so unclear if they actually work

4. **Redundant Checks**
   - Multiple hooks checking same things
   - Same validation code repeated across hooks
   - Hard to maintain consistency

---

## Proposed Improvements

### Phase 3: Simplify Hooks (In Progress)

**New Philosophy**: Hooks do only what they need to do.

**Simplified Pre-Commit** (60 lines, down from 124):
- Check for large files (50MB) - **BLOCKS**
- Check for sensitive data - **BLOCKS**
- That's it. No distribution, no complex validation.

**Simplified Post-Commit** (40 lines, down from 131):
- Log commit info (optional)
- That's it. No validation, no distribution.

**Simplified Post-Merge** (30 lines, down from 75):
- Update hooks if needed (optional)
- That's it. Info-only.

**Simplified Post-Checkout** (35 lines, down from 70):
- Update hooks if needed (optional)
- That's it. Info-only.

### Centralized Sync Script (Complete ✓)

- `scripts/sync_orchestration_files.sh` handles all distribution
- Clear, documented, testable
- Separate from hooks entirely
- User explicitly controls when sync happens

---

## Next Steps

1. Simplify pre-commit (keep only 2 blocking conditions)
2. Simplify post-commit (remove distribution logic)
3. Simplify post-merge (remove blocking)
4. Simplify post-checkout (remove blocking)
5. Update documentation with clear expectations

---

## Related Documentation

- `ORCHESTRATION_TOOLS_REDESIGN.md` - Full redesign plan
- `ORCHESTRATION_SYNC_GUIDE.md` - Sync script usage
- `scripts/hooks/` - Current hook implementations
- `scripts/sync_orchestration_files.sh` - Centralized sync script

---

**Created**: 2025-11-18 17:35  
**Next Review**: After Phase 3 (Hook Simplification)
