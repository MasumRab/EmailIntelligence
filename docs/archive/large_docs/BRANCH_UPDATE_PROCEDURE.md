# Branch Update Procedure - Infrastructure Script Propagation

**Date:** November 10, 2025  
**Purpose:** Systematically update all branches with essential infrastructure scripts from orchestration-tools  
**Status:** Ready for execution

---

## Overview

This procedure distributes critical infrastructure scripts to all branches while maintaining branch propagation integrity. Scripts are copied from orchestration-tools (the authoritative source) to all other branches via automated git operations.

### Scripts Distributed

```
install-hooks.sh                      - Install/update git hooks
enable-hooks.sh                       - Enable installed hooks
disable-hooks.sh                      - Disable hooks temporarily
validate-orchestration-context.sh     - Check for context contamination
validate-branch-propagation.sh        - Check branch compliance
extract-orchestration-changes.sh      - Selective cherry-pick utility
sync_setup_worktrees.sh               - Worktree synchronization

scripts/lib/                          - Helper libraries (all files)
  ├─ common.sh
  ├─ logging.sh
  ├─ validation.sh
  ├─ error_handling.sh
  └─ git_utils.sh
```

### What This Does

1. **Fetches** latest orchestration-tools from remote
2. **Checks out** each branch sequentially
3. **Copies** scripts from orchestration-tools to target branch
4. **Commits** changes with standard message
5. **Pushes** to remote
6. **Returns** to original branch

### What This Does NOT Do

- ❌ Commits application code changes
- ❌ Commits .git/hooks/ (use scripts/install-hooks.sh instead)
- ❌ Modifies branch propagation policy
- ❌ Commits internal process files
- ❌ Forcefully overwrites branch-specific scripts

---

## Quick Start

### Option 1: Dry Run (Recommended First)

See what would be updated without making changes:

```bash
./scripts/update-all-branches.sh --dry-run
```

**Output Example:**
```
Branches to update (45):
  001-implement-planning-workflow
  align-feature-notmuch-tagging-1
  ...
  scientific

Scripts to propagate:
  - install-hooks.sh
  - enable-hooks.sh
  ...

DRY-RUN MODE: No changes will be made
```

### Option 2: Update Specific Branches

Update only main, orchestration-tools, and scientific:

```bash
./scripts/update-all-branches.sh --branches main,orchestration-tools,scientific --no-interactive
```

### Option 3: Update All Branches

Update all branches with confirmation:

```bash
./scripts/update-all-branches.sh
```

**Then confirm when prompted:**
```
Proceed with updating branches? (y/N): y
```

### Option 4: Automated (CI/CD)

No prompts, full verbosity:

```bash
./scripts/update-all-branches.sh --no-interactive --verbose
```

---

## Command Options

### --dry-run
Shows what would be done without making any actual changes.

```bash
./scripts/update-all-branches.sh --dry-run
```

Useful for:
- Validating procedure before execution
- Testing on clean environment
- Checking which branches have issues

### --no-interactive
Skip confirmation prompts. Use for automated/CI workflows.

```bash
./scripts/update-all-branches.sh --no-interactive
```

⚠️ **Warning:** This will proceed with updates immediately without confirmation.

### --branches BRANCH1,BRANCH2,...
Update only specified branches (comma-separated, no spaces).

```bash
./scripts/update-all-branches.sh --branches main,scientific,orchestration-tools
```

Use when:
- Testing on subset of branches
- Need partial update only
- Want to update critical branches first

### --skip BRANCH1,BRANCH2,...
Skip specified branches (comma-separated, no spaces).

```bash
./scripts/update-all-branches.sh --skip feature/wip,experimental
```

Automatically skips:
- HEAD (current branch reference)
- taskmaster (special branch)

### --verbose
Show detailed output including every file operation.

```bash
./scripts/update-all-branches.sh --verbose
```

Output includes:
- Each git operation
- File-by-file updates
- Branch-specific details

### --help
Display help message with all options.

```bash
./scripts/update-all-branches.sh --help
```

---

## Recommended Execution Plan

### Phase 1: Validation (5 minutes)

```bash
# Step 1: Verify no changes in working tree
git status
# Should show: "nothing to commit, working tree clean"

# Step 2: Dry run to see what would happen
./scripts/update-all-branches.sh --dry-run

# Step 3: Review the output
# Verify all branches are listed correctly
# Verify scripts match expected list
```

### Phase 2: Update Critical Branches (10 minutes)

```bash
# Step 1: Update main and orchestration-tools first
./scripts/update-all-branches.sh --branches main,orchestration-tools --no-interactive

# Step 2: Verify updates
git checkout main
git log --oneline -2
# Should show latest commit: "chore: sync infrastructure scripts..."

# Step 3: Verify scripts are present
ls -la scripts/install-hooks.sh scripts/validate-*.sh
# All should be present with correct timestamps
```

### Phase 3: Update Feature Branches (15 minutes)

```bash
# Step 1: Update all remaining branches
./scripts/update-all-branches.sh --no-interactive

# Step 2: Monitor for failures
# Watch for ✗ entries in output
# Note any branches that failed

# Step 3: Return to main
git checkout main
```

### Phase 4: Verification (5 minutes)

```bash
# Step 1: Verify update across branches
for branch in main scientific orchestration-tools; do
  git show $branch:scripts/install-hooks.sh > /dev/null && \
    echo "✓ $branch: install-hooks.sh present" || \
    echo "✗ $branch: install-hooks.sh missing"
done

# Step 2: Check script versions match
git show orchestration-tools:scripts/validate-orchestration-context.sh > /tmp/src.sh
git show main:scripts/validate-orchestration-context.sh > /tmp/main.sh
diff /tmp/src.sh /tmp/main.sh && echo "✓ Scripts match" || echo "✗ Scripts differ"
```

---

## Detailed Workflow

### Before Execution

**Checklist:**
- [ ] Working directory is clean (`git status`)
- [ ] On main or orchestration-tools branch
- [ ] All changes committed
- [ ] Remote is up to date (`git fetch origin`)
- [ ] Backups taken (if needed)

**Commands:**
```bash
# Clean up any uncommitted changes
git status  # Check for uncommitted changes
git stash   # If changes present

# Update remote references
git fetch origin

# Verify orchestration-tools has scripts
git show orchestration-tools:scripts/install-hooks.sh > /dev/null && \
  echo "✓ Source branch ready" || \
  echo "✗ Source branch missing scripts"
```

### During Execution

**Monitoring:**
- Watch for success/failure indicators (✓/✗)
- Note any branches that fail to update
- Check for unexpected errors

**Sample Output:**
```
Updating branch: main
  Checking script: install-hooks.sh
  Copying script: install-hooks.sh
  ...
  Committing changes...
  Pushing to origin/main...
✓ Updated: main

Updating branch: scientific
  Checking script: install-hooks.sh
  Copying script: install-hooks.sh
  ...
  Committing changes...
  Pushing to origin/scientific...
✓ Updated: scientific
```

**If Issues Occur:**
```
⚠ Failed to checkout branch/branch
  → Branch may not exist on remote
  → May be local-only branch

✗ Failed to push branch/branch
  → May have protection rules
  → May have merge conflicts
  → Check branch protection settings
```

### After Execution

**Verification Steps:**

```bash
# Step 1: Check summary output
# Should show:
# - Updated branches: X (all expected branches)
# - Failed branches: 0 (or list specific failures)

# Step 2: Verify script presence on main
git checkout main
./scripts/install-hooks.sh --help  # Should work

# Step 3: Verify script presence on other branches
git checkout scientific
./scripts/validate-orchestration-context.sh --help

# Step 4: Check commit messages
git log main --oneline | grep "chore: sync infrastructure"

# Step 5: Compare with source
git diff orchestration-tools:scripts/validate-branch-propagation.sh main:scripts/validate-branch-propagation.sh
# Should show no differences
```

---

## Troubleshooting

### Problem: "Branch not found on remote"

**Cause:** Branch doesn't exist on remote or was recently deleted

**Solution:**
```bash
# Skip that branch
./scripts/update-all-branches.sh --skip local-only-branch

# Or delete the local branch if not needed
git branch -D local-only-branch
git push origin --delete local-only-branch
```

### Problem: "Failed to push <branch>"

**Possible Causes:**
1. Branch protection rules preventing push
2. Merge conflicts on remote
3. Insufficient permissions
4. Network issues

**Solution:**
```bash
# Check what failed
git log <branch>..origin/<branch>

# Option 1: Manually merge conflicts
git checkout <branch>
git pull origin <branch>
git merge orchestration-tools  # Merge latest from source

# Option 2: Skip protected branches
./scripts/update-all-branches.sh --skip protected-branch

# Option 3: Update branch protection rules to allow updates
# (In GitHub: Settings → Branches → Branch protection rules)
```

### Problem: "Commit failed (may be no changes)"

**Cause:** Scripts already at latest version on that branch

**Solution:** This is normal and not an error. The branch already has the latest scripts.

### Problem: Script shows different content than source

**Cause:** Local changes to script on target branch

**Solution:**
```bash
# Check differences
git show orchestration-tools:scripts/install-hooks.sh > /tmp/orch.sh
cat scripts/install-hooks.sh > /tmp/current.sh
diff /tmp/orch.sh /tmp/current.sh

# Option 1: Accept target version (if intentional)
# Do nothing - keep branch-specific version

# Option 2: Force source version
git show orchestration-tools:scripts/install-hooks.sh > scripts/install-hooks.sh
git add scripts/install-hooks.sh
git commit -m "chore: sync scripts/install-hooks.sh from orchestration-tools"
git push origin <branch>
```

---

## Advanced Usage

### Update with Custom Filters

```bash
# Update only main branch branches
./scripts/update-all-branches.sh --branches main

# Update all except experimental branches
./scripts/update-all-branches.sh --skip "feature/experimental,wip,test-*"

# Update only branches starting with "feature/"
# (Manually list them)
./scripts/update-all-branches.sh --branches "feature/auth,feature/api,feature/db"
```

### Verify All Branches Have Latest Scripts

```bash
# Create verification script
for branch in $(git branch -r | grep -v HEAD | sed 's|origin/||'); do
  HASH=$(git show $branch:scripts/install-hooks.sh 2>/dev/null | sha256sum | cut -d' ' -f1)
  SOURCE_HASH=$(git show orchestration-tools:scripts/install-hooks.sh | sha256sum | cut -d' ' -f1)
  if [[ "$HASH" == "$SOURCE_HASH" ]]; then
    echo "✓ $branch: scripts up-to-date"
  else
    echo "✗ $branch: scripts outdated"
  fi
done
```

### Rollback Updates

```bash
# If something goes wrong, revert the update commits

# Option 1: Revert specific branch
git checkout <affected-branch>
git log --oneline | grep "chore: sync infrastructure"
git revert <commit-hash>
git push origin <affected-branch>

# Option 2: Reset branch to before update
git checkout <affected-branch>
git reset --hard origin/<affected-branch>~1
git push origin <affected-branch> --force-with-lease
```

---

## Common Scenarios

### Scenario 1: Regular Maintenance (Monthly)

```bash
# Update all branches with latest scripts
./scripts/update-all-branches.sh --no-interactive --verbose

# Log the results
./scripts/update-all-branches.sh --dry-run > /tmp/branch-update-report.txt

# Archive report
cp /tmp/branch-update-report.txt ~/backups/branch-update-$(date +%Y-%m-%d).txt
```

### Scenario 2: Emergency Update (Critical Fix)

```bash
# Update only critical branches first
./scripts/update-all-branches.sh \
  --branches main,orchestration-tools,scientific \
  --no-interactive

# Verify update
git show main:scripts/validate-orchestration-context.sh | head -20

# Then update remaining branches
./scripts/update-all-branches.sh --no-interactive
```

### Scenario 3: CI/CD Integration

```bash
# In CI pipeline, run automated update
#!/bin/bash
set -e

git config user.email "ci@example.com"
git config user.name "CI Bot"
git checkout main

./scripts/update-all-branches.sh --no-interactive --verbose

echo "Branch update complete"
```

### Scenario 4: Testing on Subset

```bash
# Test update procedure on subset
./scripts/update-all-branches.sh \
  --dry-run \
  --branches feature/test-update,docs-cleanup

# Review output, then execute
./scripts/update-all-branches.sh \
  --branches feature/test-update,docs-cleanup \
  --no-interactive
```

---

## Success Criteria

After running the update, verify:

✅ **All Branches Updated**
```bash
git log main --oneline -1 | grep "chore: sync infrastructure"
git log scientific --oneline -1 | grep "chore: sync infrastructure"
```

✅ **Scripts Present**
```bash
for script in install-hooks enable-hooks disable-hooks validate-orchestration-context validate-branch-propagation; do
  test -f scripts/${script}.sh && echo "✓ $script" || echo "✗ $script"
done
```

✅ **Scripts Are Executable**
```bash
stat -c '%a' scripts/install-hooks.sh
# Should be: 755
```

✅ **Scripts Match Source**
```bash
git diff orchestration-tools:scripts/install-hooks.sh main:scripts/install-hooks.sh
# Should be empty (no differences)
```

✅ **All Branches Synced**
```bash
git branch -r | wc -l  # Count of branches
# Verify all important branches in list

git log main --grep="chore: sync infrastructure" --oneline | head -1
# Should show recent update commit
```

---

## Safety Features

The update script includes:

1. **Dry-run mode** - Preview changes without executing
2. **Interactive confirmation** - Confirm before proceeding
3. **Branch verification** - Check source has scripts before updating
4. **Error handling** - Graceful failure with clear messages
5. **Return to original branch** - Always returns to starting point
6. **Pre-commit hook enforcement** - Prevents bad commits
7. **Detailed logging** - Track all operations with --verbose

---

## Schedule & Maintenance

### Recommended Schedule

| Frequency | Task | Command |
|-----------|------|---------|
| Monthly | Update all branches | `./scripts/update-all-branches.sh --no-interactive` |
| After tool updates | Immediate update | `./scripts/update-all-branches.sh --branches main,orchestration-tools` |
| Weekly | Verify via dry-run | `./scripts/update-all-branches.sh --dry-run` |
| Quarterly | Full audit | `./scripts/update-all-branches.sh --verbose --dry-run` |

### Monitoring

```bash
# Create cron job for automated updates
# Edit crontab: crontab -e

# Update all branches first day of month
0 2 1 * * cd /path/to/repo && ./scripts/update-all-branches.sh --no-interactive >> /var/log/branch-updates.log 2>&1
```

---

## References

### Related Scripts
- `scripts/install-hooks.sh` - Install hooks on current branch
- `scripts/validate-orchestration-context.sh` - Check context
- `scripts/validate-branch-propagation.sh` - Check compliance
- `scripts/extract-orchestration-changes.sh` - Selective cherry-pick

### Documentation
- `.github/BRANCH_PROPAGATION_POLICY.md` - Propagation rules
- `BRANCH_PROPAGATION_IMPLEMENTATION_SUMMARY.md` - Implementation details
- `ORCHESTRATION_PROCESS_GUIDE.md` - Orchestration workflow

---

## Support

For issues or questions:

1. **Check error message** - Script provides specific guidance
2. **Review logs** - Run with `--verbose` for details
3. **Use dry-run** - Test with `--dry-run` first
4. **See documentation** - Reference relevant docs above
5. **Manual update** - Can update single branch manually:
   ```bash
   git checkout <branch>
   git show orchestration-tools:scripts/install-hooks.sh > scripts/install-hooks.sh
   chmod +x scripts/install-hooks.sh
   git add scripts/install-hooks.sh
   git commit -m "chore: sync scripts from orchestration-tools"
   git push origin <branch>
   ```

---

**Last Updated:** 2025-11-10  
**Version:** 1.0  
**Status:** Ready for Production Use
