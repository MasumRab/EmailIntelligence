# Branch Update - Quick Start Guide

Update all branches with infrastructure scripts from orchestration-tools in minutes.

---

## 30-Second Summary

This procedure updates all branches (main, scientific, feature/*, etc.) with the latest versions of infrastructure scripts (hooks, validation tools, helpers).

```bash
# See what would be updated
./scripts/update-all-branches.sh --dry-run

# Update all branches (with confirmation)
./scripts/update-all-branches.sh

# Or auto-confirm (CI/CD)
./scripts/update-all-branches.sh --no-interactive
```

---

## Step-by-Step Execution

### Step 1: Verify Everything is Ready (2 min)

```bash
# Make sure working directory is clean
git status
# Should show: "nothing to commit, working tree clean"

# Update local branch references
git fetch origin
```

### Step 2: Preview Changes (2 min)

```bash
# See what would be updated WITHOUT making changes
./scripts/update-all-branches.sh --dry-run
```

Review the output:
- ✓ See list of 70 branches that will be updated
- ✓ See list of scripts being propagated
- ✓ Confirm no errors in source verification

### Step 3: Execute Update (varies by branch count)

**Option A: Interactive (safer, requires confirmation)**
```bash
./scripts/update-all-branches.sh
# When prompted: Proceed with updating branches? (y/N): y
```

**Option B: Automated (no prompts, good for CI/CD)**
```bash
./scripts/update-all-branches.sh --no-interactive
```

**Option C: Update Specific Branches Only**
```bash
./scripts/update-all-branches.sh --branches main,scientific,orchestration-tools
```

### Step 4: Verify Success (2 min)

```bash
# Check the summary at the end of script output
# Should show:
# - Updated branches: 70
# - Failed branches: 0

# Verify on main branch
git checkout main
git log --oneline -1
# Should show: "chore: sync infrastructure scripts from orchestration-tools"

# Verify scripts exist
ls -la scripts/install-hooks.sh scripts/validate-*.sh
```

---

## Common Usage Patterns

### Pattern 1: Regular Maintenance

Update all branches every month:

```bash
./scripts/update-all-branches.sh --no-interactive
```

Expected time: 10-15 minutes (depends on network and number of branches)

### Pattern 2: After Tool Updates

Update scripts quickly when a tool is fixed:

```bash
./scripts/update-all-branches.sh --branches main,orchestration-tools,scientific --no-interactive
```

Expected time: 2-3 minutes (just critical branches)

### Pattern 3: Testing

Test on subset before full rollout:

```bash
./scripts/update-all-branches.sh --branches main,scientific --dry-run
# Review output

./scripts/update-all-branches.sh --branches main,scientific --no-interactive
# Execute
```

### Pattern 4: Troubleshooting

Get detailed information about what's happening:

```bash
./scripts/update-all-branches.sh --verbose --dry-run
# See every operation

./scripts/update-all-branches.sh --branches problem-branch --verbose
# Debug specific branch
```

---

## What Gets Updated

| File | Copies From | Updates To |
|------|-------------|-----------|
| install-hooks.sh | orchestration-tools | all branches |
| enable-hooks.sh | orchestration-tools | all branches |
| disable-hooks.sh | orchestration-tools | all branches |
| validate-orchestration-context.sh | orchestration-tools | all branches |
| validate-branch-propagation.sh | orchestration-tools | all branches |
| extract-orchestration-changes.sh | orchestration-tools | all branches |
| sync_setup_worktrees.sh | orchestration-tools | all branches |
| scripts/lib/ (all) | orchestration-tools | all branches |

---

## Expected Results

After update completes, all branches should have:

✅ Latest infrastructure scripts  
✅ Latest helper libraries  
✅ Consistent with orchestration-tools source  
✅ Commit message: "chore: sync infrastructure scripts..."  
✅ Pushed to remote

---

## Troubleshooting

### Issue: Some branches failed to update

**Check the error message:**
```bash
# Look for: "Failed branches: X"
# Listed branches that failed
```

**For each failed branch:**
```bash
# Manual update approach
git checkout <branch>
git show orchestration-tools:scripts/install-hooks.sh > scripts/install-hooks.sh
chmod +x scripts/install-hooks.sh
git add scripts/install-hooks.sh
git commit -m "chore: sync infrastructure scripts from orchestration-tools"
git push origin <branch>
```

### Issue: Script says "No scripts to update on <branch>"

This means the branch doesn't exist on remote or is local-only. It's safe to ignore.

### Issue: "Failed to push <branch>"

This usually means the branch has protection rules. Contact your branch administrator or:

```bash
# Update branch protection temporarily to allow the update
# Then re-run: ./scripts/update-all-branches.sh --branches <branch>
```

### Issue: Working directory has changes

```bash
# Stash your changes first
git stash

# Then run update
./scripts/update-all-branches.sh --no-interactive

# Restore your changes
git stash pop
```

---

## Advanced: Single Branch Manual Update

If the automated script doesn't work, manually update a single branch:

```bash
# Checkout the branch
git checkout <branch>

# Copy each script
git show orchestration-tools:scripts/install-hooks.sh > scripts/install-hooks.sh
git show orchestration-tools:scripts/enable-hooks.sh > scripts/enable-hooks.sh
git show orchestration-tools:scripts/disable-hooks.sh > scripts/disable-hooks.sh
git show orchestration-tools:scripts/validate-orchestration-context.sh > scripts/validate-orchestration-context.sh
git show orchestration-tools:scripts/validate-branch-propagation.sh > scripts/validate-branch-propagation.sh
git show orchestration-tools:scripts/extract-orchestration-changes.sh > scripts/extract-orchestration-changes.sh

# Make executable
chmod +x scripts/*.sh

# Copy lib files
git show orchestration-tools:scripts/lib/common.sh > scripts/lib/common.sh
git show orchestration-tools:scripts/lib/logging.sh > scripts/lib/logging.sh
git show orchestration-tools:scripts/lib/validation.sh > scripts/lib/validation.sh
git show orchestration-tools:scripts/lib/error_handling.sh > scripts/lib/error_handling.sh
git show orchestration-tools:scripts/lib/git_utils.sh > scripts/lib/git_utils.sh

# Commit and push
git add scripts/
git commit -m "chore: sync infrastructure scripts from orchestration-tools"
git push origin <branch>
```

---

## FAQs

**Q: How long does this take?**
A: 10-15 minutes for all 70 branches. Use `--branches main,scientific,orchestration-tools` for ~2-3 minutes on critical branches only.

**Q: Is it safe?**
A: Yes. The script:
- Uses `--dry-run` mode for preview
- Requires confirmation before executing
- Only updates scripts, not application code
- Enforces branch propagation policy
- Returns to original branch on completion

**Q: What if I made changes to a script on a branch?**
A: The update will overwrite your changes with the source version. If you have branch-specific changes, back them up first or skip that branch with `--skip`.

**Q: Can I update just main?**
A: Yes: `./scripts/update-all-branches.sh --branches main`

**Q: Do I need to install hooks after update?**
A: No, the scripts are already present. Use `./scripts/install-hooks.sh` if needed.

**Q: What if a branch is stuck?**
A: The script automatically skips problematic branches. Manually update later or investigate the issue.

---

## Next Steps

After updating branches:

1. **Verify:** `git log main --oneline -1` (check commit message)
2. **Test hooks:** `./scripts/install-hooks.sh` (on important branches)
3. **Validate:** `./scripts/validate-branch-propagation.sh` (check compliance)

---

## Full Documentation

For detailed information, see:
- `BRANCH_UPDATE_PROCEDURE.md` - Complete procedure with troubleshooting
- `.github/BRANCH_PROPAGATION_POLICY.md` - Propagation rules
- `ORCHESTRATION_PROCESS_GUIDE.md` - Orchestration workflow

---

**Quick Command Reference:**

| Command | Purpose |
|---------|---------|
| `./scripts/update-all-branches.sh --dry-run` | Preview without changes |
| `./scripts/update-all-branches.sh` | Update all (interactive) |
| `./scripts/update-all-branches.sh --no-interactive` | Update all (auto-confirm) |
| `./scripts/update-all-branches.sh --branches main,scientific` | Update specific branches |
| `./scripts/update-all-branches.sh --verbose` | Show detailed output |
| `./scripts/update-all-branches.sh --help` | Show help |

---

**Ready to go!** Start with `./scripts/update-all-branches.sh --dry-run` to see what would be updated.
