# Orchestration Disable/Enable with Branch Synchronization

Complete guide for disabling and re-enabling orchestration workflows with automatic branch profile updates and push to scientific and main branches.

---

## Overview

This system provides two complementary scripts that handle the complete orchestration lifecycle:

### Disable Script (`disable-all-orchestration-with-branch-sync.sh`)
- ✅ Disables all git hooks (backs them up)
- ✅ Sets `ORCHESTRATION_DISABLED=true` environment variable
- ✅ Updates branch profiles with `orchestration_disabled: true`
- ✅ Creates `.orchestration-disabled` marker file
- ✅ Commits and pushes changes to scientific and main branches

### Enable Script (`enable-all-orchestration-with-branch-sync.sh`)
- ✅ Restores all git hooks from backup
- ✅ Clears `ORCHESTRATION_DISABLED` from environment files
- ✅ Updates branch profiles with `orchestration_disabled: false`
- ✅ Removes `.orchestration-disabled` marker file
- ✅ Commits and pushes changes to scientific and main branches

---

## Quick Start

### Disable Orchestration (with branch sync)
```bash
./scripts/disable-all-orchestration-with-branch-sync.sh
```

This will:
1. Disable all git hooks and backup them
2. Set `ORCHESTRATION_DISABLED=true` in `.env.local`
3. Update `.context-control/profiles/*.json` files with orchestration status
4. Create `.orchestration-disabled` marker
5. Commit changes with message: "chore: disable all orchestration workflows..."
6. Push changes to current branch, scientific, and main branches

### Re-enable Orchestration (with branch sync)
```bash
./scripts/enable-all-orchestration-with-branch-sync.sh
```

This will:
1. Restore all git hooks from backup
2. Remove `ORCHESTRATION_DISABLED` from environment files
3. Update `.context-control/profiles/*.json` files with orchestration status
4. Remove `.orchestration-disabled` marker
5. Commit changes with message: "chore: re-enable all orchestration workflows..."
6. Push changes to current branch, scientific, and main branches

---

## Options

### Skip Automatic Push
To disable automatic push to branches, use the `--skip-push` flag:

```bash
# Disable orchestration without pushing
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push

# Re-enable orchestration without pushing
./scripts/enable-all-orchestration-with-branch-sync.sh --skip-push
```

This is useful when you want to:
- Review changes before pushing
- Test locally first
- Manually push to specific branches

---

## What Gets Modified

### 1. Environment Files
- `.env` (if present)
- `.env.local`

Sets/removes:
```
ORCHESTRATION_DISABLED=true/false
```

### 2. Git Hooks
Location: `.git/hooks/`

Affected hooks:
- `pre-commit`
- `post-commit`
- `post-merge`
- `post-checkout`
- `post-push`

Backup location: `.git/hooks.backup-<timestamp>/`

### 3. Branch Profiles
Location: `.context-control/profiles/`

Updated files:
- `main.json`
- `scientific.json`
- `orchestration-tools.json`

New profile fields:
```json
{
  "metadata": {
    "orchestration_disabled": true/false,
    "orchestration_disabled_timestamp": true/false
  },
  "agent_settings": {
    "orchestration_aware": true/false
  }
}
```

### 4. Marker File
- `.orchestration-disabled` (created when disabled, removed when enabled)
- Added to `.gitignore` automatically

### 5. Git Commits
Automatic commits with descriptive messages:

**When disabling:**
```
chore: disable all orchestration workflows (hooks, server-side check, branch profiles)
```

**When enabling:**
```
chore: re-enable all orchestration workflows (hooks restored, server-side check enabled, branch profiles updated)
```

### 6. Branch Synchronization
Changes are automatically pushed to:
1. Current branch (always)
2. `scientific` branch (if not current)
3. `main` branch (if not current)

---

## Step-by-Step Execution Flow

### Disable Flow
```
1. Save current branch
   ↓
2. Set ORCHESTRATION_DISABLED=true in .env files
   ↓
3. Disable all git hooks (.git/hooks/* → *.disabled)
   ↓
4. Backup hooks to .git/hooks.backup-<timestamp>/
   ↓
5. Create .orchestration-disabled marker file
   ↓
6. Add to .gitignore
   ↓
7. Update .context-control/profiles/*.json:
   - orchestration_disabled = true
   - orchestration_aware = false
   ↓
8. Stage all changes
   ↓
9. Commit with descriptive message
   ↓
10. Push to current branch
   ↓
11. Push to scientific branch
   ↓
12. Push to main branch
   ↓
13. Verify all changes
```

### Enable Flow
```
1. Save current branch
   ↓
2. Clear ORCHESTRATION_DISABLED from .env files
   ↓
3. Restore git hooks (.git/hooks/*.disabled → *)
   ↓
4. Make hooks executable
   ↓
5. Remove .orchestration-disabled marker file
   ↓
6. Update .context-control/profiles/*.json:
   - orchestration_disabled = false
   - orchestration_aware = true
   ↓
7. Stage all changes
   ↓
8. Commit with descriptive message
   ↓
9. Push to current branch
   ↓
10. Push to scientific branch
   ↓
11. Push to main branch
   ↓
12. Verify all changes
```

---

## Verification

### Check If Orchestration Is Disabled

```bash
# Check environment variable
cat .env.local | grep ORCHESTRATION_DISABLED

# Check marker file
ls -la .orchestration-disabled

# Check hooks are disabled
ls -la .git/hooks/*.disabled

# Check branch profile status
cat .context-control/profiles/main.json | grep orchestration_disabled
```

### Check If Orchestration Is Enabled

```bash
# Verify env file is clean
grep -v "ORCHESTRATION_DISABLED" .env.local

# Verify marker is gone
! [[ -f .orchestration-disabled ]] && echo "Marker removed"

# Verify hooks are active
ls -la .git/hooks/post-commit

# Verify profile status
cat .context-control/profiles/main.json | grep orchestration_disabled
```

---

## Integration with Other Tools

### Orchestration Control Module
These scripts work seamlessly with the existing orchestration control module:

```python
# Python code checks this centralized control
from setup.orchestration_control import is_orchestration_enabled

if is_orchestration_enabled():
    # Run orchestration workflows
else:
    # Skip orchestration workflows
```

### Git Hooks
Updated hooks should check the orchestration status:

```bash
#!/bin/bash
source scripts/lib/orchestration-control.sh
is_orchestration_enabled || exit 0

# Hook logic
```

---

## Common Scenarios

### Scenario 1: Temporarily Disable for Local Development
```bash
# Disable orchestration
./scripts/disable-all-orchestration-with-branch-sync.sh

# Work on your feature
# ... make changes, commit, etc. ...

# Re-enable when done
./scripts/enable-all-orchestration-with-branch-sync.sh
```

### Scenario 2: Disable Without Pushing
```bash
# Disable but review changes first
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push

# Review commits
git log --oneline -5

# Push manually when ready
git push origin <branch-name>
```

### Scenario 3: Multiple Developers Coordinating
```bash
# Developer 1: Disable orchestration and push
./scripts/disable-all-orchestration-with-branch-sync.sh

# Developer 2: Pull the changes
git pull origin scientific

# Both can now work without orchestration hooks interfering
```

### Scenario 4: Emergency: Just Disable Hooks (No Branch Sync)
Use the original scripts instead:
```bash
./scripts/disable-all-orchestration-hooks.sh

# Work...

./scripts/restore-orchestration-hooks.sh
```

---

## Troubleshooting

### Hooks Won't Restore
If hooks don't restore properly:

```bash
# Check if backup exists
ls -d .git/hooks.backup-* 2>/dev/null | tail -1

# If no backup, manually restore from git
git checkout HEAD -- .git/hooks/

# Make them executable
chmod +x .git/hooks/*
```

### Push Failed
If push to a branch fails:

```bash
# Check branch existence
git branch -a | grep scientific
git branch -a | grep main

# Try pushing individually
git push origin scientific
git push origin main

# Or skip push and push manually later
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push
```

### Profile Files Corrupted
If JSON profile files become invalid:

```bash
# Restore from git
git checkout HEAD -- .context-control/profiles/

# Then re-run the script
./scripts/disable-all-orchestration-with-branch-sync.sh --skip-push
```

### Marker File Won't Delete
```bash
# Force remove
sudo rm -f .orchestration-disabled

# Or just re-run enable script
./scripts/enable-all-orchestration-with-branch-sync.sh
```

---

## Branch Profile Structure

After disable/enable, profiles will have:

```json
{
  "id": "main",
  "name": "Main Development Branch",
  "branch_patterns": ["main", "master"],
  "metadata": {
    "orchestration_disabled": false,
    "orchestration_disabled_timestamp": true
  },
  "agent_settings": {
    "enable_code_execution": true,
    "enable_file_writing": true,
    "enable_shell_commands": true,
    "orchestration_aware": true
  }
}
```

---

## Related Documentation

- `ORCHESTRATION_DISABLE_FLAG.md` - Original disable flag guide
- `ORCHESTRATION_CONTROL_MODULE.md` - Centralized control module
- `ORCHESTRATION_QUICK_DISABLE.md` - Quick reference
- `ORCHESTRATION_PROCESS_GUIDE.md` - Complete process guide

---

## Notes

- Scripts are idempotent: running them multiple times is safe
- Changes are automatically committed with descriptive messages
- All changes are pushed to maintain branch consistency
- Hook backups are timestamped and preserved
- Profile updates include status metadata for tracking

---

## Files Modified by These Scripts

### Created/Modified
- `.env` (if present)
- `.env.local`
- `.orchestration-disabled` (only when disabled)
- `.gitignore`
- `.context-control/profiles/main.json`
- `.context-control/profiles/scientific.json`
- `.context-control/profiles/orchestration-tools.json`
- `.git/hooks/*` (disabled/restored)
- `.git/hooks.backup-<timestamp>/` (created when disabling)

### Unchanged
- Source code files
- Tests
- Documentation (except this file)
- Configuration files (except environment)

---

## Safe to Use With

✅ Multiple developers (script handles race conditions)
✅ Different branches (automatically syncs to scientific and main)
✅ CI/CD pipelines (use `--skip-push` for automated systems)
✅ Git hooks (hooks are properly backed up and restored)
✅ Existing orchestration modules (compatible with control module)

---
