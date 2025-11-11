# Orphaned Work Quick Reference

## TL;DR

**Work lost when switching branches?** Run this:
```bash
./scripts/recover_orphaned_work.sh scan
```

---

## Prevention (Automatic)

When you switch branches with uncommitted orchestration file changes:

```
⚠️  UNCOMMITTED ORCHESTRATION FILE CHANGES DETECTED

Choose (1-3):
1) Stash and switch (RECOMMENDED - your work is saved)
2) Abort and commit first
3) Continue anyway (NOT RECOMMENDED)
```

**Choose 1** and your work is automatically saved.

---

## Stash is Lost - How to Recover

### Quick Recovery
```bash
# Find everything
./scripts/recover_orphaned_work.sh scan

# See all stashes
./scripts/recover_orphaned_work.sh stashes

# Apply most recent stash
git stash apply

# Or recover specific stash
./scripts/recover_orphaned_work.sh recover-stash 0
```

### Detailed Recovery
```bash
# Check what changed recently
./scripts/recover_orphaned_work.sh reflog

# Find branches with your changes
./scripts/recover_orphaned_work.sh branches

# Find WIP commits
./scripts/recover_orphaned_work.sh wip

# Restore from specific commit
./scripts/recover_orphaned_work.sh restore abc1234
```

---

## Common Scenarios

### "I stashed changes and switched branches, now I'm on main and want my work back"

```bash
# See all stashes
git stash list

# Apply the most recent (usually stash@{0})
git stash apply

# Or use the recovery script
./scripts/recover_orphaned_work.sh scan
./scripts/recover_orphaned_work.sh recover-stash 0
```

### "I switched branches and don't know if my work is stashed"

```bash
./scripts/recover_orphaned_work.sh scan
```

This tells you:
- What's uncommitted now
- What's in stashes
- Recent commits that might have your work
- WIP branches
- Which branches have similar changes

### "I need to keep my changes but start fresh"

```bash
# Create a patch backup
./scripts/recover_orphaned_work.sh patch my_backup.patch

# Now you can reset and restore later
git reset --hard
# ... do other work ...

# Apply the patch
git apply my_backup.patch
```

### "My stash has conflicts when applying"

```bash
# Try to apply
git stash apply stash@{0}

# If conflicts occur:
# 1. Resolve conflicts manually (edit files)
# 2. Stage resolved files
git add .

# 3. Commit
git commit -m "Resolved stash conflicts"
```

### "I accidentally deleted a stash (within 30 days)"

```bash
# Find recent deletions
git reflog show stash

# Recover the specific stash by its hash
git stash apply abc1234
```

### "There are multiple stashes and I don't know which is which"

```bash
# List all with creation info
git stash list

# Look for the one with AUTO-STASH timestamp
# Example: stash@{0}: AUTO-STASH: orchestration files before switching to main...

# Show what's in a specific stash
git stash show -p stash@{0}

# If you find the right one, apply it
git stash apply stash@{0}
```

---

## Orchestration-Managed Files (Protected)

These files trigger the protection hook:
```
setup/               launch.py           launch.sh
deployment/          .flake8             .pylintrc
.gitignore           .gitattributes       pyproject.toml
requirements.txt     requirements-dev.txt
```

When you change these and switch branches, the hook automatically offers to stash.

---

## Recovery Script Commands

| Command | Purpose | When to Use |
|---------|---------|------------|
| `scan` | Find all orphaned work | Start here if work is lost |
| `stashes` | List saved stashes | See all saved work |
| `recover-stash N` | Apply specific stash | Recover particular stash |
| `reflog` | Check git history | Find work in commits |
| `branches` | Find branches with changes | Locate work on other branches |
| `patch FILE` | Create backup | Save current work as file |
| `wip` | Find WIP commits | Find incomplete work |
| `status` | Check uncommitted changes | See current state |
| `restore HASH` | Restore from commit | Recover from specific commit |

---

## Best Practices

✅ **DO**
- Let the hook auto-stash when switching branches (choose option 1)
- Use `git stash apply` or recovery script to get work back
- Commit and push recovered work to create PR
- Run `scan` if unsure what happened

❌ **DON'T**
- Ignore the stash prompt and continue (option 3)
- Delete stashes without checking what's in them
- Switch branches repeatedly without stashing
- Edit orchestration files then switch branches without saving first

---

## One-Liner Recovery Commands

```bash
# Find lost work
./scripts/recover_orphaned_work.sh scan

# Get most recent stash
git stash apply

# See all your stashes
git stash list

# Recover from stash #0
./scripts/recover_orphaned_work.sh recover-stash 0

# Find WIP work
./scripts/recover_orphaned_work.sh wip

# Create patch backup
./scripts/recover_orphaned_work.sh patch backup.patch
```

---

## Still Lost?

```bash
# Get help with all commands
./scripts/recover_orphaned_work.sh help

# Read full documentation
cat docs/ORPHANED_WORK_RECOVERY.md

# Or ask for help in the issue tracker
# Include output from: ./scripts/recover_orphaned_work.sh scan
```

---

## Hook Installation

If the protection hook isn't working:

```bash
# Install all hooks
./scripts/install-hooks.sh

# Verify pre-checkout hook exists
ls -la .git/hooks/pre-checkout

# Make sure it's executable
chmod +x .git/hooks/pre-checkout
```

---

## Technical Details

- **Stashes persist for 30 days** in git by default
- **Auto-stashes have format**: `AUTO-STASH: orchestration files before switching to [branch] at [timestamp]`
- **Hook runs before branch switch** (pre-checkout)
- **Recovery works on all branches** (can recover stash from any branch you're on)
- **No data loss** - stashed work is never automatically deleted

---

Remember: **When in doubt, run**: `./scripts/recover_orphaned_work.sh scan`
