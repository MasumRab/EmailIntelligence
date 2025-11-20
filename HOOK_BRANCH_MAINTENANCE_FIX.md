# Hook Branch Maintenance Fixes

## Problem Identified

The previous post-checkout and post-merge hooks were **blocking branch operations** and **forcing synchronization without user control**:

### Post-Checkout Hook Issues
1. ❌ Called functions that didn't exist or weren't properly sourced
2. ❌ Required approval prompts on every branch switch (blocking)
3. ❌ Tried to force sync from orchestration-tools on every checkout
4. ❌ Prevented fast branch switching
5. ❌ Could hang or fail silently if approval handler missing

### Post-Merge Hook Issues
1. ❌ Attempted forced synchronization on every merge
2. ❌ Could overwrite local changes without consent
3. ❌ Called undefined functions from orchestration-approval.sh
4. ❌ Blocked merge operations
5. ❌ Interfered with normal git workflows

### Impact
- ❌ Developers couldn't switch branches quickly
- ❌ Merges were slow and could fail
- ❌ Worktree operations were blocked
- ❌ Orchestration files were force-synced unexpectedly
- ❌ Branch maintenance impossible during approval handler issues

## Solution: Minimal, Non-Blocking Hooks

### New Post-Checkout Hook

**Design Principle:** Fast branch switching with zero blocking

```bash
# Only safe operations:
1. Update hooks if orchestration-tools changed (non-blocking)
2. Display informational messages
3. Verify .taskmaster/ is isolated (info only)
4. No approval prompts
5. No forced synchronization
```

**Key Changes:**
- ✅ Removed all approval prompts
- ✅ Removed forced file synchronization
- ✅ Removed undefined function calls
- ✅ Only updates hooks conditionally
- ✅ Allows fast branch switching

**Result:**
```bash
$ git checkout main
Switched to branch 'main'
Switched to branch: main
ℹ Task Master worktree is on branch: unknown (separate)
✓ Post-checkout complete

# Instant - no waiting, no blocking
```

### New Post-Merge Hook

**Design Principle:** Merges succeed without interference

```bash
# Only safe operations:
1. Log merge information
2. Check critical files (info only)
3. Update hooks conditionally
4. Verify .taskmaster/ isolation
5. No forced synchronization
```

**Key Changes:**
- ✅ Removed all forced file checkouts
- ✅ Removed synchronization logic
- ✅ Removed approval handler calls
- ✅ Only informational messages
- ✅ Allows merges to complete

**Result:**
- Merges complete instantly
- No unexpected file changes
- Developers control synchronization
- Worktree operations unblocked

## Orchestration File Management

### What Changed
The hooks **no longer force-sync orchestration files** on branch operations.

**Before:**
```
git checkout main
→ Hook forces sync of setup/, deployment/, .github/, etc.
→ Approval prompt blocks operation
→ User must approve or wait
```

**After:**
```
git checkout main
→ Hook updates only git hooks (if needed)
→ No file synchronization
→ Branch switch completes instantly
```

### How to Sync Orchestration Files (Explicit Control)

For developers who need to synchronize orchestration files:

```bash
# Manual sync from orchestration-tools
git checkout orchestration-tools -- setup/
git checkout orchestration-tools -- deployment/
git checkout orchestration-tools -- .github/

# Or sync all at once
git checkout orchestration-tools -- .
```

### Why This is Better

✅ **User control**: Developers choose when to sync
✅ **Fast operations**: No blocking on branch switch/merge
✅ **Predictable**: No unexpected file changes
✅ **Safe**: Can review changes before merging
✅ **Explicit**: Clear what's being synchronized

## Testing Results

```bash
# Test 1: Fast branch switching
$ time git checkout main
Switched to branch 'main'
real    0m0.524s

$ time git checkout orchestration-tools  
Switched to branch 'orchestration-tools'
real    0m0.483s

✓ Fast - no approval prompts, no syncing delays

# Test 2: Multiple branch switches
$ git checkout main && \
  git checkout scientific && \
  git checkout orchestration-tools && \
  git checkout taskmaster
✓ All succeed instantly without blocking

# Test 3: Merges work without blocking
$ git checkout orchestration-tools
$ git merge main
# Completes without forcing file changes
✓ Merge succeeds
```

## Hook Safety Guarantees

✅ **Branch switching never blocks**
- No approval prompts
- No forced synchronization
- Fast operation

✅ **Merges complete without interference**
- No file overwrites
- No blocking operations
- Developers control changes

✅ **Orchestration files only updated explicitly**
- Must use `git checkout` manually
- Developers see what's changing
- Safe and predictable

✅ **.taskmaster/ worktree stays isolated**
- Never synced on branch operations
- Always separate from main branch
- Informational tracking only

## Hook Propagation

All hooks are installed via `scripts/install-hooks.sh`:

```bash
# Update hooks (recommended after pulling orchestration-tools)
./scripts/install-hooks.sh
```

This ensures:
- Consistent behavior across clones
- Safe, non-blocking operations
- Latest hook versions installed

## Files Changed

- `scripts/hooks/post-checkout` - Simplified, non-blocking
- `scripts/hooks/post-merge` - Simplified, non-blocking
- `.git/hooks/post-checkout` - Updated copy
- `.git/hooks/post-merge` - Updated copy

## Related Documentation

- `HOOK_SAFETY_FIXES.md` - Safety improvements for branch switching
- `ORCHESTRATION_HOOK_FIXES_SUMMARY.md` - Validation check fixes
- `TASKMASTER_BRANCH_CONVENTIONS.md` - Worktree isolation requirements
