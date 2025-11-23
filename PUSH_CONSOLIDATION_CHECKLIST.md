# Email Consolidation Push - Quick Reference Checklist

## Phase 1: PRESERVE (Mandatory) ✓ DO THIS FIRST

### Pre-Flight Checks
- [ ] All repos accessible and on main/stable branches
- [ ] No uncommitted changes that need saving
- [ ] Internet connection stable (large push operation)
- [ ] Sufficient disk space available

### Step 1: Disable Orchestration

```bash
# Run this script to disable orchestration globally
cat > /tmp/disable_orch.sh << 'SCPT'
#!/bin/bash
for repo in \
  /home/masum/github/EmailIntelligence \
  /home/masum/github/EmailIntelligenceAider \
  /home/masum/github/EmailIntelligenceAuto \
  /home/masum/github/EmailIntelligenceGem \
  /home/masum/github/EmailIntelligenceQwen \
  /home/masum/github/PR/EmailIntelligence
do
  echo "=== $(basename $repo) ==="
  cd "$repo"
  
  # Disable in shell scripts
  find . -name "*.sh" -type f 2>/dev/null | \
    xargs grep -l "ORCHESTRATION_ENABLED" 2>/dev/null | \
    while read script; do
      sed -i 's/ORCHESTRATION_ENABLED=true/ORCHESTRATION_ENABLED=false/g' "$script"
      echo "  ✓ Disabled: $script"
    done
  
  # Disable in Python files
  find . -name "*.py" -type f 2>/dev/null | \
    xargs grep -l "ORCHESTRATION.*=.*True" 2>/dev/null | \
    while read script; do
      sed -i 's/ORCHESTRATION\s*=\s*True/ORCHESTRATION = False/g' "$script"
      echo "  ✓ Disabled: $script"
    done
  
  # Disable in .env
  if [ -f ".env" ]; then
    if grep -q "ORCHESTRATION" ".env"; then
      sed -i 's/ORCHESTRATION=.*/ORCHESTRATION=0/' ".env"
      echo "  ✓ Disabled: .env"
    fi
  fi
done
SCPT

bash /tmp/disable_orch.sh
```

**Completion Check:**
```bash
grep -r "ORCHESTRATION_ENABLED=true" /home/masum/github/EmailIntelligence*
# Should return: (no results)
```

- [ ] Orchestration disabled across all repos
- [ ] No "ORCHESTRATION_ENABLED=true" found in grep

### Step 2: Commit Orchestration Changes

```bash
cat > /tmp/commit_orch.sh << 'SCPT'
#!/bin/bash
for repo in \
  /home/masum/github/EmailIntelligence \
  /home/masum/github/EmailIntelligenceAider \
  /home/masum/github/EmailIntelligenceAuto \
  /home/masum/github/EmailIntelligenceGem \
  /home/masum/github/EmailIntelligenceQwen \
  /home/masum/github/PR/EmailIntelligence
do
  cd "$repo"
  echo "=== $(basename $repo) ==="
  
  if git status | grep -q "modified"; then
    git add -A
    git commit -m "chore: disable orchestration before consolidation push"
    echo "  ✓ Committed"
  else
    echo "  ✓ No changes needed"
  fi
done
SCPT

bash /tmp/commit_orch.sh
```

- [ ] All orchestration commits created

### Step 3: Push All Branches (EmailIntelligenceAuto Priority)

**⚠️ CRITICAL: This is the key operation - pushes all 900+ commits**

```bash
# Start with critical repo
cd /home/masum/github/EmailIntelligenceAuto
echo "Starting push of 889 unpushed commits..."
git push --all origin 2>&1 | tee /tmp/push_auto.log

# Check for errors
if grep -E "error|failed|rejected" /tmp/push_auto.log; then
  echo "⚠️  ERRORS DETECTED - See CONFLICT RESOLUTION section"
  exit 1
else
  echo "✓ EmailIntelligenceAuto push successful"
fi
```

- [ ] EmailIntelligenceAuto: All branches pushed
- [ ] Monitor output for conflicts (see below if errors occur)

**If Conflicts During Push:**

See "CONFLICT RESOLUTION PROCEDURES" in main report. Most common:

```bash
# Error: "non-fast-forward"
# Solution:
cd /home/masum/github/EmailIntelligenceAuto
git pull --rebase origin <branch>
# Resolve any conflicts (same process as below)
git push origin <branch>
```

### Step 4: Push Remaining Repos

```bash
cat > /tmp/push_all.sh << 'SCPT'
#!/bin/bash
for repo in \
  /home/masum/github/EmailIntelligence \
  /home/masum/github/EmailIntelligenceAider \
  /home/masum/github/EmailIntelligenceGem \
  /home/masum/github/EmailIntelligenceQwen \
  /home/masum/github/PR/EmailIntelligence
do
  cd "$repo"
  echo "=== $(basename $repo) ==="
  git push --all origin 2>&1 | tail -3
  echo ""
done
SCPT

bash /tmp/push_all.sh
```

- [ ] EmailIntelligence: All branches pushed
- [ ] EmailIntelligenceAider: All branches pushed
- [ ] EmailIntelligenceGem: All branches pushed
- [ ] EmailIntelligenceQwen: All branches pushed
- [ ] PR/EmailIntelligence: All branches pushed

### Step 5: Verify All Commits Saved

```bash
cat > /tmp/verify_push.sh << 'SCPT'
#!/bin/bash
echo "VERIFICATION: All commits pushed?"
echo "================================"
all_ok=true

for repo in \
  /home/masum/github/EmailIntelligence \
  /home/masum/github/EmailIntelligenceAider \
  /home/masum/github/EmailIntelligenceAuto \
  /home/masum/github/EmailIntelligenceGem \
  /home/masum/github/EmailIntelligenceQwen \
  /home/masum/github/PR/EmailIntelligence
do
  cd "$repo"
  unpushed=$(git log --branches --not --remotes --oneline 2>/dev/null | wc -l)
  repo_name=$(basename "$repo")
  
  if [ "$unpushed" -eq 0 ]; then
    echo "✓ $repo_name: All commits pushed"
  else
    echo "⚠️  $repo_name: $unpushed commits still unpushed!"
    all_ok=false
  fi
done

echo ""
if [ "$all_ok" = true ]; then
  echo "✅ SUCCESS: All commits safely on GitHub"
else
  echo "❌ FAILURE: Some commits still unpushed - re-run push"
  exit 1
fi
SCPT

bash /tmp/verify_push.sh
```

- [ ] All 6 repos show "✓ All commits pushed"
- [ ] No unpushed commits remain

### Phase 1 Complete ✅

**Milestone:** All 900+ commits are now on GitHub - fully recoverable

---

## Phase 2: ANALYZE (Optional - When Ready)

### Decision: What to Do with Each Branch?

**For each local branch, decide:**

- [ ] **DELETE** - Already merged or temporary
- [ ] **MERGE INTO MAIN** - Active feature that should be integrated
- [ ] **KEEP SEPARATE** - Experimental or long-term feature work
- [ ] **ARCHIVE** - Document and keep for historical reference

**Branches Safe to DELETE (Already Merged):**
```
- main-patch (EmailIntelligenceAuto)
- refactor-ai-modules-di (EmailIntelligenceAuto)
- remove-deprecated-markers (EmailIntelligenceAuto)
- sourcery-ai-fixes-main-2 (EmailIntelligenceAuto)
- pr-179-patch-* (temporary patches)
- *-temp (temporary worktrees)
- kilo-* (temporary worktrees)
```

**Branches to KEEP (Core Development):**
```
- main (primary branch)
- orchestration-tools (active development)
- scientific (experimental/scientific track)
- feature/* (active features in progress)
```

---

## Phase 3: MERGE (Optional - If Consolidating)

### Merge Strategy Decision Matrix

| Branch | Status | Decision | Rationale |
|--------|--------|----------|-----------|
| feature/syntax-error-fixes | 705 commits | MERGE INTO MAIN | Important fixes needed |
| scientific | Parallel track | KEEP SEPARATE | Different development stream |
| orchestration-tools | Active | KEEP SEPARATE | Intentional experimental area |
| docs/* | Documentation | CONSOLIDATE | Could merge all docs into main-docs |
| recovery-* | Backup | DELETE | Once main is verified stable |

### Pre-Merge Testing

```bash
# Before merging a branch, test it safely:
cd /home/masum/github/EmailIntelligenceAuto

# Test merge without committing
git checkout main
git merge --no-commit --no-ff feature/syntax-error-fixes

# Check if there are conflicts
git status

# If problems, abort
git merge --abort

# If OK, complete merge
git merge --continue
git push origin main
```

---

## Phase 4: CLEAN (Optional - Workspace Cleanup)

### Safe Deletion Procedure

```bash
# ONLY do this after Phase 1 (push) is complete!

cd /home/masum/github/EmailIntelligenceAuto

# 1. Delete locally
git branch -D <branch_name>

# 2. Clean up remote references
git fetch --prune origin
git remote prune origin

# 3. Verify deletion
git branch -vv | grep <branch_name>
# Should show nothing
```

**Before deletion, verify:**
- [ ] Branch has been pushed to GitHub
- [ ] Branch is not needed for active development
- [ ] Commits from branch are merged into main or other branches

---

## CONFLICT RESOLUTION PROCEDURES

### Scenario 1: Push Rejected (Non-Fast-Forward)

**Error Message:**
```
 ! [rejected]        feature/X -> feature/X (non-fast-forward)
error: failed to push some refs to 'https://github.com/MasumRab/EmailIntelligence.git'
hint: Updates were rejected because the tip of your current branch is behind
```

**Solution:**

```bash
# Rebase approach (cleaner history)
git pull --rebase origin feature/X
# Resolve conflicts (see Scenario 2)
git rebase --continue
git push origin feature/X

# OR merge approach (preserves history)
git pull origin feature/X
# Resolve conflicts (see Scenario 2)
git commit
git push origin feature/X
```

- [ ] Conflict resolved using rebase or merge
- [ ] Branch successfully pushed

### Scenario 2: Merge Conflicts During Rebase/Merge

**Signs of Conflict:**
```
# git status shows:
both modified:   path/to/file.py

# File contains markers:
<<<<<<< HEAD
  content from local branch
=======
  content from remote branch
>>>>>>> origin/feature-X
```

**Resolution Steps:**

```bash
# 1. Open file and find conflict markers
vim path/to/file.py

# 2. Edit to resolve - choose which version to keep:
# Option A: Keep local (everything before =======)
# Option B: Keep remote (everything after =======)
# Option C: Keep both (manually combine)
# Option D: Keep neither (delete both)

# 3. Remove conflict markers completely

# 4. Stage the resolved file
git add path/to/file.py

# 5. Continue the operation
git rebase --continue
# OR
git commit

# 6. If more conflicts, repeat steps 1-4

# 7. Finally, push
git push origin <branch>
```

- [ ] All conflict markers removed
- [ ] File compiles/runs without errors
- [ ] Rebase/merge completed
- [ ] Branch pushed successfully

### Scenario 3: Large Diverged Branch

**Symptom:** 700+ commits ahead of remote (like align-feature-notmuch-tagging-1-v2)

**Check Before Acting:**

```bash
cd /home/masum/github/EmailIntelligenceAuto

# See what changed
git log --oneline origin/align-feature-notmuch-tagging-1-v2..align-feature-notmuch-tagging-1-v2 | head -20

# See file changes
git diff --stat origin/align-feature-notmuch-tagging-1-v2..align-feature-notmuch-tagging-1-v2 | head -10

# Test merge without committing
git merge --no-commit --no-ff origin/align-feature-notmuch-tagging-1-v2
# Review conflicts
git status
# Abort if too many
git merge --abort
```

**Options:**

1. **Force Push** (if you control this branch):
   ```bash
   git push origin align-feature-notmuch-tagging-1-v2 --force
   # ⚠️  Only if you're sure about the divergence
   ```

2. **Rebase** (cleaner history):
   ```bash
   git rebase origin/align-feature-notmuch-tagging-1-v2
   # Resolve conflicts as they appear
   ```

3. **Keep Separate** (preserve divergence):
   ```bash
   git push origin align-feature-notmuch-tagging-1-v2
   # Don't merge with remote - keep experimental
   ```

- [ ] Decision made on how to handle divergence
- [ ] Action taken (force push, rebase, or keep separate)

---

## MONITORING & LOGGING

### Create Push Log

```bash
# Capture all push operations
git push --all origin 2>&1 | tee /tmp/email_push_log_$(date +%Y%m%d_%H%M%S).txt

# Check for errors
grep -E "error|rejected|fatal" /tmp/email_push_log_*.txt
```

- [ ] Push log created and saved
- [ ] No fatal errors in log

### GitHub Verification

After push, verify on GitHub:

1. Visit: https://github.com/MasumRab/EmailIntelligence
2. Check "Network" tab to see branch graph
3. Verify commits show up on each branch
4. Confirm no older remote branches are missing

- [ ] GitHub shows all pushed branches
- [ ] No commits lost in network graph

---

## SUCCESS CRITERIA - Phase 1

Once complete, all of these should be true:

- [ ] ✅ 900+ unpushed commits now visible on GitHub
- [ ] ✅ All 6 repos show "All commits pushed"
- [ ] ✅ No commits lost in process
- [ ] ✅ Orchestration disabled across all repos
- [ ] ✅ Local branches still exist (not deleted yet)
- [ ] ✅ Can recover any branch from GitHub if needed

---

## ROLLBACK / RECOVERY

### If Something Goes Wrong (Before pushing):
```bash
# Don't push
# Commits are still in local git
git reflog
git reset --hard <safe_point>
```

### If Something Goes Wrong (After pushing):
```bash
# Commits are on GitHub - check branch there
git fetch origin
git checkout <branch>
git pull origin <branch>

# GitHub branch is now restored locally
```

---

## NEXT STEPS

### After Phase 1 Completes:

1. **Take a break** - Large operation completed
2. **Verify on GitHub** - Confirm all commits visible
3. **Decide on Phase 2-4** - Do we want to consolidate/clean?
4. **Document decisions** - Which branches keep/delete/merge

---

## Support

### For Merge Conflicts:
See "CONFLICT RESOLUTION PROCEDURES" above, or check main report

### For Push Failures:
```bash
# Check git status
git status

# Check if origin is reachable
git remote -v

# Test connection
git fetch origin

# If still stuck, see specific scenario in main report
```

### Questions?
Refer to: `/home/masum/github/EMAIL_CONSOLIDATION_PUSH_REPORT.md`

---

## Checklist Status

- [ ] Phase 1: PRESERVE - Mandatory
  - [ ] Step 1: Disable Orchestration
  - [ ] Step 2: Commit Changes
  - [ ] Step 3: Push EmailIntelligenceAuto
  - [ ] Step 4: Push Other Repos
  - [ ] Step 5: Verify All Pushed
  
- [ ] Phase 2: ANALYZE - Optional (later)
  
- [ ] Phase 3: MERGE - Optional (later)
  
- [ ] Phase 4: CLEAN - Optional (later)

**Current Status:** Ready to Execute Phase 1 ✓
