# Git Hooks: Blocking Scenarios & Triggers

**Quick Reference**: What prevents commits from being made  
**Date**: 2025-11-18  

---

## Summary: What Actually Blocks Commits

```
ONLY pre-commit hook can block commits.
Only 2 conditions trigger blocking:

1. File > 50MB
2. Sensitive data in staged files
```

---

## Scenario 1: Large File Blocked

### Trigger
```bash
git add huge_model.bin          # 100MB file
git commit -m "Add large model"
```

### Result
```
ERROR: Large files detected (>50MB):
huge_model.bin
Please remove or use Git LFS for large files

[pre-commit hook exits with code 1 - COMMIT BLOCKED]
```

### Resolution
```bash
# Option 1: Use Git LFS
git lfs install
git lfs track "*.bin"
git add huge_model.bin .gitattributes
git commit -m "Add large model via LFS"

# Option 2: Remove the file
git reset HEAD huge_model.bin
git commit -m "Add other files"

# Option 3: Add to .gitignore
echo "huge_model.bin" >> .gitignore
git commit -m "Add files without large file"
```

### Branches
- Affects: ALL branches (main, scientific, orchestration-tools, etc.)
- No exceptions

---

## Scenario 2: Sensitive Data Blocked

### Trigger
```bash
git add config.py  # Contains: api_key = "sk-1234567890"
git commit -m "Add configuration"
```

### Result
```
WARNING: Potential sensitive data detected in staged files
Please review and ensure no secrets are being committed

[pre-commit hook detects keyword "key" - WARNING, but allows commit]
```

**Note**: This is a WARNING, not a hard block. Commit proceeds.

### Resolution
```bash
# Option 1: Remove the secret
# Edit config.py, remove api_key = "sk-..."
git add config.py
git commit -m "Remove API key from config"

# Option 2: Use environment variables
# Edit config.py: api_key = os.environ.get('API_KEY')
git add config.py
git commit -m "Use environment variable for API key"

# Option 3: Move to .env file (and gitignore it)
echo "api_key = sk-1234567890" > .env
echo ".env" >> .gitignore
git add config.py .gitignore
git commit -m "Move secrets to .env"
```

### Branches
- Affects: ALL branches (main, scientific, orchestration-tools, etc.)
- No exceptions

---

## Scenario 3: Normal Commit (Passes)

### Trigger
```bash
git add src/feature.py src/test.py
git commit -m "Add new feature"
```

### Result
```
✓ All pre-commit checks passed
[commit created successfully]
```

### Branches
- Works on: ALL branches
- No restrictions

---

## Scenario 4: Post-Commit Hook (Cannot Block)

### Trigger
```bash
git commit -m "Update code"  # Commit already created
```

### Result
```
Post-commit hook triggered on branch: main
Commit: abc123def456...
✓ Post-commit hook completed successfully
```

**Key Point**: Post-commit runs AFTER commit is created.  
**Cannot block** - commit already exists in repository.

### What Happens
- Validates files (informational)
- Logs commit info (optional)
- Checks hook consistency (optional)
- **Result**: Exit code always 0 (success)

---

## Scenario 5: Post-Merge Hook (Cannot Block)

### Trigger
```bash
git merge feature/something
```

### Result
```
Post-merge on branch: main
✓ Task Master worktree isolated (separate from merge)
✓ Hooks updated
✓ Post-merge complete
```

**Key Point**: Post-merge runs AFTER merge completes.  
**Cannot block** - merge already completed.

### What Happens
- Validates merge integrity (informational)
- Updates hooks if needed (optional)
- Verifies critical files (informational)
- **Result**: Exit code always 0 (success)

---

## Scenario 6: Post-Checkout Hook (Cannot Block)

### Trigger
```bash
git checkout feature/branch
```

### Result
```
Switched to branch: feature/branch
On orchestration-tools branch
Updating git hooks from orchestration-tools branch...
✓ Hooks updated
ℹ Task Master worktree is on branch: unknown (separate)
✓ Post-checkout complete
```

**Key Point**: Post-checkout runs AFTER branch switch.  
**Cannot block** - branch switch already happened.

### What Happens
- Detects branch switch (informational)
- Updates hooks if changed (optional)
- Verifies Task Master isolation (informational)
- **Result**: Exit code always 0 (success)

---

## Scenario 7: Push (No Hook)

### Trigger
```bash
git push origin main
```

### Result
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Writing objects: 100% (5/5), 1.23 KiB | 1.23 MiB/s, done.
Total 5 (delta 2), reused 0 (delta 0), received 0 (delta 0)
To github.com:user/repo.git
   abc123..def456 main -> main
```

**No push hooks** - nothing blocks or validates.

---

## Summary Table: Hook Blocking Behavior

| Git Operation | Hook | Runs When | Can Block? | Exit Code |
|---------------|------|-----------|-----------|-----------|
| `git commit` | pre-commit | Before commit | **YES** | 0 = allow, 1 = block |
| `git push` | post-push | After push | NO | Always 0 |
| `git merge` | post-merge | After merge | NO | Always 0 |
| `git checkout` | post-checkout | After switch | NO | Always 0 |
| `git pull` | N/A | - | NO | N/A |
| `git rebase` | N/A | - | NO | N/A |

---

## Blocking Conditions Summary

### Pre-Commit (ONLY BLOCKER)

✅ **Condition 1: Large Files**
```bash
if file > 50MB:
    exit 1  # BLOCK COMMIT
```

✅ **Condition 2: Sensitive Data**
```bash
if grep "password|secret|key|token" in staged files:
    # WARNING printed, but commit allowed (exit 0)
    # User should fix but can force if needed
```

### All Other Hooks

```bash
exit 0  # Always - cannot block operations
```

---

## Disabling Hooks (Advanced Users)

### Temporarily Disable All Checks
```bash
export DISABLE_ORCHESTRATION_CHECKS=1
git commit -m "Skip checks"
unset DISABLE_ORCHESTRATION_CHECKS
```

### Force Commit (Skip Pre-Commit)
```bash
git commit --no-verify -m "Skip pre-commit checks"
```

**Note**: Use with caution - bypasses safety checks.

---

## Environment Control

### Enable/Disable Checks
```bash
# Disable orchestration checks
export DISABLE_ORCHESTRATION_CHECKS=1

# Re-enable (default)
unset DISABLE_ORCHESTRATION_CHECKS
```

### Optional Logging
```bash
# Log commits to file
export ORCHESTRATION_LOG="/path/to/log.txt"
# Each commit logged with timestamp and message
```

---

## Related Files

- `scripts/hooks/pre-commit` - The blocking hook
- `scripts/hooks/post-commit` - Non-blocking
- `scripts/hooks/post-merge` - Non-blocking
- `scripts/hooks/post-checkout` - Non-blocking
- `scripts/sync_orchestration_files.sh` - File distribution (separate from hooks)

---

## Key Takeaways

1. **Only pre-commit blocks** - Other hooks are informational
2. **2 blocking conditions** - Large files and sensitive data
3. **Other hooks can't block** - They run after operations complete
4. **Sync is separate** - Use `sync_orchestration_files.sh` for distribution
5. **Control available** - Use flags to disable checks if needed

---

**Last Updated**: 2025-11-18 17:45  
**For full details**: See `GIT_HOOKS_BLOCKING_SUMMARY.md`
