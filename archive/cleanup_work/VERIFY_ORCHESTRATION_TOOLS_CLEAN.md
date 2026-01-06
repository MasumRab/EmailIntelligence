# Verify orchestration-tools Branch is Clean

**Purpose:** Before merging orchestration-tools to scientific, verify it contains ONLY alignment framework code  
**Status:** Verification Guide  
**Date:** January 6, 2026

---

## Why This Matters

With **275 non-safe branches** in the repository, there's risk that orchestration-tools branch has been contaminated with:
- TaskMaster code (feature/taskmaster-protection, taskmaster branch)
- Bolt optimization experiments (52+ remotes/origin/bolt-* branches)
- Old orchestration-tools variants (orchestration-tools-changes, etc.)
- Task execution code (001/002/003 branches)
- Experimental features (tagging, backend refactor, etc.)

**Before merging to scientific or main, you MUST verify orchestration-tools is clean.**

---

## Quick Verification (5 minutes)

### 1. Check Recent Commits

```bash
git checkout orchestration-tools
git log --oneline -20
```

**What you should see:**
```
✅ Commits related to alignment framework
✅ Task 079, 080, 083 implementation
✅ Orchestration code
✅ Validation integration
✅ E2E testing

❌ RED FLAGS - STOP if you see:
❌ taskmaster-related commits
❌ bolt-optimize-* commits
❌ orchestration-tools-changes merges
❌ 001/002/003 task commits
❌ feature/tagging or backend refactor commits
```

### 2. Compare to main

```bash
git diff main..orchestration-tools --stat
```

**What you should see:**
- Only files in alignment framework scope
- No .taskmaster/ folder files
- No bolt-related changes
- No experimental code

**What would be RED FLAGS:**
```
❌ .taskmaster/  files
❌ bolt-*  changes
❌ backend/  vs src/ refactoring
❌ tagging-related files
❌ experiment-* files
```

### 3. Check for Problematic File Changes

```bash
git diff main..orchestration-tools --name-only | grep -E "taskmaster|bolt|experiment|tagging|backend-refactor"
```

**Expected output:** (empty = good)

**Red flag output:**
```
❌ Changes to .taskmaster/ files
❌ Changes to bolt-related files
❌ Experimental feature files
```

---

## Detailed Verification (10 minutes)

### Step 1: Verify Branch Origin

```bash
git log --oneline orchestration-tools | tail -5
```

Should show commits that are related to:
- Alignment framework development
- Task 079, 080, 083
- Phase 3 specification work

### Step 2: Check Commit Messages

```bash
git log --oneline orchestration-tools | grep -v "alignment\|orchestr\|validat\|e2e\|phase 3"
```

If this returns any commits, they might be suspicious. Investigate:
```bash
git show <commit-hash>
```

### Step 3: Look for Merge Commits

```bash
git log --oneline orchestration-tools | grep "Merge\|merge"
```

Check what was merged:
```bash
git log --oneline orchestration-tools --graph | head -30
```

**Verify:**
- ✅ Only alignment-related merges
- ❌ No merges from taskmaster, bolt-*, 001/002/003 branches

### Step 4: Compare File Structure

```bash
git diff main..orchestration-tools --name-status | head -50
```

Examine files changed. They should be in:
```
✅ src/orchestration/
✅ src/alignment/
✅ src/validation/
✅ src/e2e_testing/
✅ tests/alignment/
✅ docs/alignment/
✅ config/alignment/

❌ NOT in:
❌ .taskmaster/
❌ bolt_experiments/
❌ experimental/
❌ archive/
```

### Step 5: Check for Large Commits

```bash
git log --oneline orchestration-tools --reverse | head -20
```

Then check if any commit seems unusually large:
```bash
git show <commit-hash> --stat
```

**Red flags:**
- ❌ 100+ files changed in single commit
- ❌ Random file deletions/additions
- ❌ Unrelated code mixed in

---

## Automated Verification Script

Save this as `verify_orchestration_tools.sh`:

```bash
#!/bin/bash
set -e

echo "Verifying orchestration-tools branch is clean..."
echo ""

# 1. Ensure we're in the right directory
if [ ! -d ".git" ]; then
  echo "❌ ERROR: Not in a git repository"
  exit 1
fi

# 2. Fetch latest
echo "Fetching latest..."
git fetch origin

# 3. Check if orchestration-tools exists
if ! git rev-parse orchestration-tools >/dev/null 2>&1; then
  echo "❌ ERROR: orchestration-tools branch not found"
  exit 1
fi

# 4. Switch to orchestration-tools
echo "Checking out orchestration-tools..."
git checkout orchestration-tools

# 5. Check for problematic files
echo ""
echo "Checking for problematic files..."

TASKMASTER_FILES=$(git diff main..orchestration-tools --name-only | grep -c "\.taskmaster\/" || true)
BOLT_FILES=$(git diff main..orchestration-tools --name-only | grep -c "bolt-" || true)
EXPERIMENT_FILES=$(git diff main..orchestration-tools --name-only | grep -c "experiment\|tagging\|backend-refactor" || true)

if [ "$TASKMASTER_FILES" -gt 0 ]; then
  echo "❌ FAIL: Found $TASKMASTER_FILES .taskmaster/ files"
  exit 1
fi

if [ "$BOLT_FILES" -gt 0 ]; then
  echo "❌ FAIL: Found $BOLT_FILES bolt-related files"
  exit 1
fi

if [ "$EXPERIMENT_FILES" -gt 0 ]; then
  echo "❌ FAIL: Found $EXPERIMENT_FILES experimental files"
  exit 1
fi

# 6. Check for problematic commits
echo "Checking commit messages for red flags..."

BAD_COMMITS=$(git log --oneline main..orchestration-tools | grep -i "taskmaster\|bolt\|experiment\|tagging" | wc -l || true)

if [ "$BAD_COMMITS" -gt 0 ]; then
  echo "❌ FAIL: Found $BAD_COMMITS commits with suspicious messages"
  echo ""
  git log --oneline main..orchestration-tools | grep -i "taskmaster\|bolt\|experiment\|tagging"
  exit 1
fi

# 7. Success
echo "✅ SUCCESS: orchestration-tools branch is clean!"
echo ""
echo "Summary:"
echo "  - No .taskmaster/ files: ✅"
echo "  - No bolt-* files: ✅"
echo "  - No experimental files: ✅"
echo "  - No suspicious commits: ✅"
echo ""
echo "Safe to merge to scientific branch."
```

**Run verification:**
```bash
chmod +x verify_orchestration_tools.sh
./verify_orchestration_tools.sh
```

---

## Visual Inspection Checklist

### Before Merging to scientific:

- [ ] Branch exists: `orchestration-tools`
- [ ] Last 20 commits are alignment-related
- [ ] No taskmaster files changed
- [ ] No bolt-* files in diff
- [ ] No experimental features merged
- [ ] No 001/002/003 branch merges
- [ ] File structure is clean
- [ ] No merge conflicts with scientific
- [ ] No huge unexplained commits
- [ ] All tests pass (if available)

### If ANY check fails:

1. ❌ STOP - Do not merge
2. 🔍 Investigate the problematic commit
3. 🔧 Consider:
   - Creating clean orchestration-tools from main
   - Cherry-picking only alignment commits
   - Asking: "Is this commit part of Phase 3 alignment?"
4. ✅ Re-run verification
5. ✅ Then proceed with merge

---

## Recovery: If orchestration-tools is Contaminated

### Option 1: Rebase to Remove Bad Commits

```bash
# Find the bad commit
git log --oneline orchestration-tools | grep "<bad-commit-message>"

# Find the commit before it
GOOD_COMMIT="<hash-of-commit-before-bad>"

# Rebase from there
git rebase -i $GOOD_COMMIT
# Remove bad commits in interactive editor

# Force push (⚠️ only if you're sure)
git push origin orchestration-tools --force-with-lease
```

### Option 2: Create Clean Branch from main

```bash
# Create clean orchestration-tools
git checkout main
git pull origin main
git checkout -b orchestration-tools-clean
git cherry-pick <alignment-commit-1>
git cherry-pick <alignment-commit-2>
git cherry-pick <alignment-commit-3>
# ... repeat for all alignment commits

# Verify it's clean
./verify_orchestration_tools.sh

# Replace old branch
git push origin orchestration-tools-clean:orchestration-tools --force-with-lease
```

### Option 3: Start Fresh

```bash
# If orchestration-tools is too contaminated:
git checkout main
git pull origin main
git checkout -b orchestration-tools
# Copy clean alignment code into src/
git add .
git commit -m "feat: clean orchestration-tools branch for Phase 3"
git push origin orchestration-tools --force-with-lease
```

---

## Sign-Off Checklist

### When orchestration-tools is verified clean:

```
✅ Recent commits are alignment-related
✅ No .taskmaster/ files in diff
✅ No bolt-* files in diff
✅ No experimental code
✅ No 001/002/003 branch merges
✅ File structure is alignment-focused
✅ Verification script passes
✅ Manual inspection complete

CLEARANCE: orchestration-tools is safe to merge to scientific
```

---

## Document This Verification

When you merge, document your verification:

```bash
git checkout scientific
git merge orchestration-tools -m "feat: merge Phase 3 alignment framework

Verified:
- ✅ orchestration-tools branch is clean (verified 2026-01-06)
- ✅ No taskmaster code
- ✅ No bolt experiments
- ✅ No experimental features
- ✅ Only alignment framework code
- ✅ Ready for Phase 3 implementation

Reference: VERIFY_ORCHESTRATION_TOOLS_CLEAN.md"
```

---

## Summary

Before merging orchestration-tools to scientific:

1. **Quick check (5 min):** Run the 3-step quick verification
2. **Detailed check (10 min):** Run all 5 detailed verification steps
3. **Script check:** Run the automated verification script
4. **Manual review:** Check commit messages and file list
5. **Sign-off:** Only merge if all checks pass ✅

**If anything looks wrong:** STOP and remediate before merging.

---

**Reference:** BRANCHES_TO_NEVER_MERGE.md for list of bad branches to avoid
