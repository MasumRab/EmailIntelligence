# Orchestration & GitHub Protection Summary

## What Changed

The orchestration system now protects all `.github/` files, including critical Copilot and agent instructions. Branch switching no longer silently overwrites these files without your approval.

## Protected `.github` Files (12 total)

### Agent Instructions (CRITICAL)
```
.github/instructions/
├── taskmaster.instructions.md
├── dev_workflow.instructions.md
├── self_improve.instructions.md
├── vscode_rules.instructions.md
└── tools-manifest.json
```
**Synced as:** Full directory (`.github/instructions/`)
**Protection Level:** CRITICAL - Always synced with approval

### CI/CD Workflows
```
.github/workflows/
├── lint.yml
├── test.yml
└── extract-orchestration-changes.yml
```
**Synced as:** Individual files
**Protection Level:** HIGH - Prevents pipeline breakage

### Configuration & Templates
```
.github/
├── BRANCH_PROPAGATION_POLICY.md
├── PROPAGATION_SETUP_CHECKLIST.md
├── DOCUMENTATION_DISTRIBUTION_REPORT.md
└── pull_request_templates/
    └── orchestration-pr.md
```
**Synced as:** Individual files
**Protection Level:** MEDIUM - Policy and consistency

## How It Works

### User Interaction
When you checkout a branch or merge:

```bash
$ git checkout main
```

System checks if `.github` files differ. If they do:

```
=== Orchestration File Updates ===
The following directories will be synchronized:
  → .github/instructions/ (all contents)

The following files will be updated from orchestration-tools:
  → .github/workflows/lint.yml
  → .github/workflows/test.yml
  → .github/BRANCH_PROPAGATION_POLICY.md
  ... 4 more files ...

Proceed with orchestration synchronization? (y/n)
```

You can:
- **Type `y`** → Files sync from orchestration-tools
- **Type `n`** → Files stay as-is, operation completes

### What Gets Logged
Every approval/denial is logged:

```bash
$ cat .git/hooks/.orchestration_log
[2024-11-17 15:32:10] [main] APPROVAL: GRANTED - orchestration sync
[2024-11-17 15:45:23] [scientific] APPROVAL: DENIED - orchestration sync
```

## Key Guarantees

| Guarantee | Before | After |
|-----------|--------|-------|
| Copilot instructions lost? | ❌ Possible | ✅ Protected |
| CI/CD workflow change noticed? | ❌ Silent | ✅ Prompted |
| Agent instructions overwritten? | ❌ Silently | ✅ User approves |
| Can deny sync? | ❌ No | ✅ Yes |
| Changes logged? | ❌ No | ✅ Yes |

## Implementation

**Hooks Modified:**
- `.git/hooks/post-checkout` - Syncs on branch switch
- `.git/hooks/post-merge` - Syncs on merge completion

**Library Added:**
- `scripts/lib/orchestration-approval.sh` - Approval logic

**Documentation Added:**
- `docs/ORCHESTRATION_APPROVAL.md` - Full guide
- `docs/.GITHUB_FILES_INVENTORY.md` - File inventory
- `docs/ORCHESTRATION_APPROVAL_QUICK_REFERENCE.md` - Quick reference

## For CI/CD Pipelines

In automation, skip prompts:

```bash
# Skip approval prompt (auto-approve)
ORCHESTRATION_APPROVAL_PROMPT=false git checkout main

# Disable orchestration entirely
DISABLE_ORCHESTRATION_CHECKS=1 git checkout main
```

## Manual Operations

If you denied a sync but need latest:

```bash
# Sync specific directory
git checkout orchestration-tools -- .github/instructions/

# Sync all workflows
git checkout orchestration-tools -- .github/workflows/

# Sync everything
git checkout orchestration-tools -- .github/
```

## File Status

**All `.github` files are identical across:**
- `main` branch
- `scientific` branch  
- `orchestration-tools` branch

This means:
- ✅ No conflicts when syncing
- ✅ Safe to sync without review
- ✅ Consistent across all branches

## Examples

### Scenario 1: Switch to main with approval
```bash
$ git checkout main
# Prompt appears: approve with 'y'
# Files sync successfully
# Logged: APPROVAL: GRANTED
```

### Scenario 2: Merge with denial
```bash
$ git merge origin/develop
# Prompt appears: deny with 'n'
# Files preserved locally
# Logged: APPROVAL: DENIED
# Continue with merge without .github changes
```

### Scenario 3: Automated CI/CD
```bash
#!/bin/bash
# In CI/CD script - skip prompts
export ORCHESTRATION_APPROVAL_PROMPT=false
git checkout main
# Orchestration syncs automatically
# No user interaction needed
```

## Related Documentation

- **Full Details:** `docs/ORCHESTRATION_APPROVAL.md`
- **File Inventory:** `docs/.GITHUB_FILES_INVENTORY.md`
- **Quick Reference:** `docs/ORCHESTRATION_APPROVAL_QUICK_REFERENCE.md`
- **Original System:** `ORCHESTRATION_PROCESS_GUIDE.md`

## Quick Troubleshooting

**Question:** Are my Copilot instructions safe?
**Answer:** Yes. `.github/instructions/` is synced with user approval only.

**Question:** What if CI/CD workflows break?
**Answer:** Workflows are synced individually with approval. You control updates.

**Question:** Can I skip approval?
**Answer:** Yes - use `ORCHESTRATION_APPROVAL_PROMPT=false` for CI/CD automation.

**Question:** Where are decisions recorded?
**Answer:** `.git/hooks/.orchestration_log` - view with `cat .git/hooks/.orchestration_log`

**Question:** Can I manually sync `.github` files?
**Answer:** Yes - `git checkout orchestration-tools -- .github/`

## Status

✅ **IMPLEMENTED**
- All 12 `.github` files protected
- Approval system active
- Logging enabled
- Documentation complete
- Backward compatible
- CI/CD friendly

✅ **TESTED**
- Syntax validation passed
- File identity verified across branches
- Mock scenarios reviewed

✅ **DOCUMENTED**
- 4 documentation files created
- Quick reference guides available
- Inventory complete
- Troubleshooting section included
