# Orphaned Work Recovery Guide

## Overview

When working with orchestration-managed files (setup/, deployment/, .flake8, etc.) on non-orchestration-tools branches, switching branches without committing changes can result in lost work. This guide explains how to prevent and recover from this scenario.

## Prevention: Automated Stashing

The **pre-checkout hook** automatically detects when you're about to switch branches with uncommitted changes to orchestration-managed files and offers to stash them before switching.

### What the Hook Does

1. **Detects** uncommitted changes to orchestration-managed files
2. **Alerts** you with a clear warning
3. **Prompts** you to choose an action:
   - **Option 1**: Auto-stash changes and proceed (RECOMMENDED)
   - **Option 2**: Abort the switch and commit changes first
   - **Option 3**: Continue anyway without stashing (NOT RECOMMENDED)

### Example

```bash
$ git checkout main

════════════════════════════════════════════════════
⚠️  UNCOMMITTED ORCHESTRATION FILE CHANGES DETECTED
════════════════════════════════════════════════════

The following orchestration-managed files have uncommitted changes:

  • setup/launch.py
  • .flake8

Switching branches could lose this work!

OPTIONS:
  1) Stash changes and switch (work will be saved, recovery available)
  2) Abort switch and commit/push changes first
  3) Continue anyway (NOT RECOMMENDED - changes may be lost)

Choose (1-3): 1

Creating stash: AUTO-STASH: orchestration files before switching to main...
✓ Changes stashed successfully

To recover this work later, use:
  git stash list              # See all stashes
  git stash apply stash@{0}   # Apply most recent stash

Or use the recovery script:
  ./scripts/recover_orphaned_work.sh scan
```

## Orchestration-Managed Files

The following files are monitored for automatic stashing:

```
setup/                  # Setup and launch scripts
deployment/             # Docker and deployment configs
.flake8                 # Python linting config
.pylintrc               # Python linting config
.gitignore              # Git ignore rules
.gitattributes          # Git attributes
pyproject.toml          # Python project config
requirements.txt        # Python dependencies
requirements-dev.txt    # Dev dependencies
launch.py               # Launch script
launch.sh               # Bash launch script
```

## Recovery: The Recovery Script

### Quick Start

```bash
# Run full recovery scan
./scripts/recover_orphaned_work.sh scan
```

This performs a comprehensive search for:
- Current uncommitted changes
- Git stashes (auto-created by pre-checkout hook)
- Recent commits with changes
- WIP (Work In Progress) commits
- Branches containing your work

### All Commands

#### 1. List All Stashes

```bash
./scripts/recover_orphaned_work.sh stashes
```

Output:
```
[WARN] Found 3 stash(es):
stash@{0}: AUTO-STASH: orchestration files before switching to main...
stash@{1}: WIP: work on setup script
stash@{2}: Save progress on .flake8
```

#### 2. Recover Specific Stash

```bash
./scripts/recover_orphaned_work.sh recover-stash 0
```

The script will:
- Show you which files are in the stash
- Ask for confirmation before applying
- Apply the stash to your working directory

#### 3. Check Git Reflog

```bash
# Check reflog for current branch
./scripts/recover_orphaned_work.sh reflog

# Check reflog for specific branch
./scripts/recover_orphaned_work.sh reflog main
```

Shows recent commits and branch movements that might contain your work.

#### 4. Find Branches with Your Work

```bash
./scripts/recover_orphaned_work.sh branches
```

Lists branches that have changes to orchestration-managed files.

#### 5. Check Current Status

```bash
./scripts/recover_orphaned_work.sh status
```

Shows any uncommitted changes in the current working directory.

#### 6. Create Backup Patch

```bash
# Create patch of current changes
./scripts/recover_orphaned_work.sh patch my_changes.patch

# Apply patch later
git apply my_changes.patch
```

#### 7. Find WIP Commits

```bash
./scripts/recover_orphaned_work.sh wip
```

Lists commits with WIP, TODO, FIXME, or Draft in the message.

#### 8. Restore from Specific Commit

```bash
# Restore all files from a commit
./scripts/recover_orphaned_work.sh restore abc1234

# Restore specific file pattern
./scripts/recover_orphaned_work.sh restore abc1234 "setup/"
```

## Workflow Best Practices

### When Modifying Orchestration Files

1. **Make your changes** on any branch (main, scientific, feature branch, etc.)

2. **Before switching branches**, the hook will prompt you:
   ```bash
   git checkout other-branch
   # Hook detects changes and offers to stash
   ```

3. **Choose option 1** (stash and switch)

4. **After changes are stashed**:
   - You can work on other branches
   - Your changes are safely preserved
   - You can recover them anytime

5. **To continue the work**:
   ```bash
   # Switch back to original branch
   git checkout original-branch
   
   # Recover the stash
   ./scripts/recover_orphaned_work.sh stashes
   # Then: ./scripts/recover_orphaned_work.sh recover-stash 0
   
   # Or apply most recent stash directly
   git stash apply
   ```

6. **Commit and push**:
   ```bash
   git add setup/ .flake8 # etc
   git commit -m "Update orchestration files"
   git push origin original-branch
   ```

### Creating PRs for Orchestration Changes

```bash
# 1. Make changes on any branch
git checkout -b feature/update-setup

# 2. Edit setup files
vim setup/launch.py

# 3. Commit and push
git add setup/
git commit -m "Update setup script"
git push origin feature/update-setup

# 4. The post-push hook detects orchestration changes
# and creates automatic draft PR to orchestration-tools

# 5. Review and merge PR to orchestration-tools
# 6. Hook will auto-sync changes to other branches
```

## Understanding Stash Naming

Auto-stashes created by the pre-checkout hook have descriptive names:

```
AUTO-STASH: orchestration files before switching to main at 2024-11-11 14:30:45
        ↑                                      ↑          ↑
      Type                                Branch      Timestamp
```

This naming helps you:
- Identify auto-stashes vs manual stashes
- Know which branch you were switching to
- Remember when the stash was created
- Easily find multiple stashes

## Recovering Lost Work - Step by Step

### Scenario 1: You Switched Branches Without Committing

```bash
# 1. Run full scan
./scripts/recover_orphaned_work.sh scan

# 2. You'll see stashes created by pre-checkout hook
# Example output:
# [WARN] Found 1 stash(es):
# stash@{0}: AUTO-STASH: orchestration files before switching to main...

# 3. Apply the stash
./scripts/recover_orphaned_work.sh recover-stash 0

# 4. Commit the recovered files
git add .
git commit -m "Recovered orchestration file changes"
git push origin your-branch
```

### Scenario 2: You Lost Changes and Can't Find a Stash

```bash
# 1. Check reflog for recent commits
./scripts/recover_orphaned_work.sh reflog

# 2. Find the commit hash that had your changes
# (Look for commits before your branch switch)

# 3. Restore files from that commit
./scripts/recover_orphaned_work.sh restore abc1234 "setup/"

# 4. Verify the files were restored
git status

# 5. Commit and push
git add .
git commit -m "Restored setup files from previous state"
git push origin your-branch
```

### Scenario 3: Multiple Stashes Exist

```bash
# 1. List all stashes
./scripts/recover_orphaned_work.sh stashes

# Output:
# stash@{0}: AUTO-STASH: orchestration files before switching to scientific...
# stash@{1}: AUTO-STASH: orchestration files before switching to main...
# stash@{2}: WIP: Save progress on setup

# 2. The most recent is stash@{0}, older ones shift up

# 3. Apply specific stash
./scripts/recover_orphaned_work.sh recover-stash 1

# 4. If you want to keep a stash for later
# (recovery applies it but leaves it in the stash list)
# You can delete stashes after verifying recovery:
git stash drop stash@{1}
```

## Troubleshooting

### "Pre-checkout hook didn't trigger"

The hook might not be installed or executable:

```bash
# Verify hook is installed
ls -la .git/hooks/pre-checkout

# Install hooks
./scripts/install-hooks.sh

# Make executable
chmod +x .git/hooks/pre-checkout
```

### "Stash apply had conflicts"

The stash may conflict with changes on the destination branch:

```bash
# View conflicts
git status

# Resolve conflicts manually
# Then continue
git add .
git commit -m "Resolved stash conflicts"
```

### "I accidentally deleted the stash"

Git keeps stashes for 30 days by default:

```bash
# View all stashes including recent deletions
git reflog show stash

# Recover deleted stash (within 30 days)
git stash apply sha1hash
```

### "Recovery script isn't finding my work"

Try the full scan with more details:

```bash
# Full scan with all options
./scripts/recover_orphaned_work.sh scan

# Check specific branches
./scripts/recover_orphaned_work.sh branches

# Look at WIP commits
./scripts/recover_orphaned_work.sh wip

# Check reflog for main branch
./scripts/recover_orphaned_work.sh reflog main
```

## Key Takeaways

1. **Prevention is automatic**: The pre-checkout hook saves your work automatically
2. **Stashing is safe**: Stashed changes don't disappear; they're fully recoverable
3. **Recovery is easy**: Use `./scripts/recover_orphaned_work.sh scan` to find lost work
4. **Multiple recovery options**: Git stashes, reflog, WIP commits, and branches all help recover work
5. **Orchestration-managed files** are monitored for protection

## Additional Resources

- `./scripts/recover_orphaned_work.sh help` - View all recovery commands
- `git stash --help` - Git stash documentation
- `git reflog --help` - Git reflog documentation
- `.git/hooks/pre-checkout` - Pre-checkout hook implementation
