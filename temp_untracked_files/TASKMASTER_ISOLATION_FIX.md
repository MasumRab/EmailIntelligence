# Task Master Branch Isolation - Complete Fix

## Problem Statement

Previous commit violated taskmaster branch isolation requirements:

1. ❌ Tried to whitelist `.taskmaster/**` in orchestration-tools `.gitignore`
2. ❌ Created `.taskmaster/.gitignore` file inside worktree
3. ❌ Unresolved merge conflict markers
4. ❌ Attempted to use `.git/info/exclude` (repo-specific, doesn't propagate)

This would have:
- Tracked taskmaster files in orchestration-tools branch
- Contaminated branch history
- Required manual setup for each clone
- Blocked agent access if using `.gitignore` mechanism

## Solution: Pre-Commit Hook Isolation

### Approach

Use **pre-commit hooks** to prevent commits rather than `.gitignore`:

```bash
# scripts/hooks/pre-commit (orchestration-tools branch)
TASKMASTER_FILES=$(git diff --cached --name-only | grep "^\.taskmaster/" || true)
if [[ -n "$TASKMASTER_FILES" ]]; then
    echo "ERROR: Task Master worktree files cannot be committed to orchestration-tools"
    exit 1
fi
```

### Benefits

✅ **Visible to agents**: `.taskmaster/` not in `.gitignore` or `.git/info/exclude`
✅ **Automatic enforcement**: Hook prevents commits on all clones
✅ **Propagates**: Via `scripts/install-hooks.sh` on setup
✅ **Clear error messages**: Tells users exactly what went wrong
✅ **No accidental tracking**: Pre-commit hook blocks staging

### How It Works

1. **Local development**: Agent can read/access `.taskmaster/` files freely
2. **Staging files**: `git add .taskmaster/file.txt` succeeds (no gitignore filter)
3. **Committing**: Pre-commit hook checks staged files
4. **Hook blocks**: If `.taskmaster/` files staged, exits with error
5. **User action**: Run `git restore --staged .taskmaster/` to unstage

### Setup & Propagation

```bash
# On clone, install hooks (run once)
./scripts/install-hooks.sh

# Hook is installed to .git/hooks/pre-commit
# It contains the .taskmaster/ check
```

### Verification

```bash
# Verify .taskmaster is accessible
ls -la .taskmaster/

# Verify it's NOT in gitignore
git check-ignore -v .taskmaster/  # Should return nothing

# Verify hook is installed
grep "TASKMASTER_FILES" .git/hooks/pre-commit

# Test the hook (should fail)
git add .taskmaster/config.json
git commit -m "test"  # ERROR: Task Master worktree files cannot be committed
```

## Changes Made

### 1. Pre-commit Hook (scripts/hooks/pre-commit)
- Added `.taskmaster/` file check for orchestration-tools branch
- Provides clear error message with recovery instructions
- Prevents accidental commits

### 2. .gitignore
- ❌ Removed `!.taskmaster/**` whitelist
- ❌ Removed `.taskmaster/` explicit ignore
- ✅ Leaves `.taskmaster/` naturally untracked (visible to agents)

### 3. .git/info/exclude
- Removed repo-specific rule (doesn't propagate)
- Hook approach supersedes this

### 4. Documentation
- Created `TASKMASTER_BRANCH_CONVENTIONS.md` with all requirements
- Updated `AGENTS.md` to reference conventions
- Documented hook-based isolation approach

## Commits

```
ab43d333 docs: update conventions to reflect pre-commit hook isolation approach
9d6cf594 fix: use pre-commit hook to prevent taskmaster worktree commits
536a3aaf docs: add taskmaster branch isolation conventions and requirements
a0400993 fix: correct .taskmaster worktree gitignore isolation
```

## Key Requirements for Future Commits

✅ Do:
- Use pre-commit hooks to enforce branch isolation
- Keep `.taskmaster/` visible to agents
- Document isolation approach
- Test that hooks propagate to clones

❌ Don't:
- Add `.taskmaster/**` to `.gitignore`
- Create `.taskmaster/.gitignore`
- Use `.git/info/exclude` alone (not propagated)
- Whitelist taskmaster files on orchestration-tools branch

## Testing

Verify isolation is working:

```bash
# On orchestration-tools branch
cd orchestration-tools

# These should all succeed (agent access)
ls .taskmaster/AGENTS.md
find .taskmaster -name "*.json" | head -3
cat .taskmaster/config.json

# This should fail (commit prevention)
git add .taskmaster/config.json
git commit -m "test"  # ERROR message expected
```

## Related Documentation

- `TASKMASTER_BRANCH_CONVENTIONS.md` - Complete isolation requirements
- `AGENTS.md` - Branch-specific guidance (references conventions)
- `scripts/install-hooks.sh` - Hook installation script
- `scripts/hooks/pre-commit` - Hook source file
