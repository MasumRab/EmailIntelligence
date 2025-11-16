# Safe Action Plan - Orchestration Workflow Implementation

## ⚠️ BRANCH SAFETY RULES

### Current State
- **Current Branch**: `orchestration-tools-changes` (local ahead by 1 commit)
- **Staged Changes**: 
  - New: `docs/GITHUB_WORKFLOWS_ROADMAP.md`, `docs/WORK_IN_PROGRESS_SUMMARY.md`
  - Deleted: 6 hook files from `scripts/hooks/`
  - Untracked: `scripts/hooks/` directory

### Branch Strategy
1. **orchestration-tools-changes** ← CURRENT (safe to commit/push)
   - Purpose: Experimental branch for orchestration workflow changes
   - Safe to push to: `origin/orchestration-tools-changes`
   - Should NOT push to: main, scientific, feature branches

2. **main** (protected branch - requires PR)
   - Purpose: Production-ready stable codebase
   - Safe action: Create PR from tested branches only
   - NEVER push directly

3. **scientific** (release branch - requires PR)
   - Purpose: Scientific computing features
   - Safe action: Create PR from tested branches only
   - NEVER push directly

4. **Feature branches** (topic branches - local changes ok)
   - Purpose: Experimental features
   - Safe action: Push to specific feature branch only
   - NEVER rebase/push others' work

---

## PHASE 1: Complete Documentation & Hooks (This Session)

### Step 1: Verify Staged Changes ✓
```bash
git status  # Shows: 2 files new, 6 files deleted, 1 untracked dir
```
**SAFE**: These are infrastructure/docs changes for orchestration-tools-changes only

### Step 2: Review & Commit Staged Changes
**ACTION**: Review changes before commit
```bash
git diff --cached  # Review what's being committed
```

**SAFE COMMIT**:
```bash
git commit -m "feat: add orchestration workflow documentation and hook cleanup"
```
**Target**: orchestration-tools-changes only

### Step 3: Push to orchestration-tools-changes
**SAFE PUSH**:
```bash
git push origin orchestration-tools-changes
```
**Verify**: Check GitHub that it pushed to `orchestration-tools-changes` branch, NOT main/scientific

---

## PHASE 2: P0 Workflows (test.yml, lint.yml)

### Files to Create
- `.github/workflows/test.yml` (NEW)
- `.github/workflows/lint.yml` (NEW)

### Branch Rule
- **Create on**: `orchestration-tools-changes`
- **Push to**: `orchestration-tools-changes` (via PR to orchestration-tools first)
- **DO NOT**: Create directly on main/scientific

### Process
1. Create workflows on orchestration-tools-changes
2. Commit and push to orchestration-tools-changes
3. Create PR: orchestration-tools-changes → orchestration-tools
4. After merge to orchestration-tools, other branches receive via sync

---

## PHASE 3: Task-Specific Work

### Task 3 (Email Pipeline) & Task 7.1 (Validation Criteria)
**WHERE**: Create on appropriate task branches (NOT orchestration-tools)

**RECOMMENDATION**:
1. Create `feature/task-7-merge-validation` branch from `scientific`
2. Work on validation criteria in that branch
3. Create PR when ready

**SAFE PROCESS**:
```bash
# Only after orchestration-tools-changes is pushed:
git checkout scientific
git pull origin scientific
git checkout -b feature/task-7-merge-validation
# Make changes...
git push origin feature/task-7-merge-validation
# Create PR in GitHub
```

---

## SAFETY CHECKLIST (Before Each Push)

- [ ] **Verify branch**: `git branch` shows correct branch name (✓ orchestration-tools-changes)
- [ ] **Verify remote**: `git remote -v` shows correct upstream
- [ ] **Verify commit message**: Describes changes accurately
- [ ] **Verify files changed**: Only expected files in `git status`
- [ ] **Test locally**: Can run basic validation
- [ ] **Check PR target**: If creating PR, verify target branch is correct
- [ ] **NO direct pushes to**: main, scientific, taskmaster, or other protected branches

---

## Current Staged Changes Summary

### NEW FILES (safe to add)
- `docs/GITHUB_WORKFLOWS_ROADMAP.md` - Comprehensive workflow planning
- `docs/WORK_IN_PROGRESS_SUMMARY.md` - Status tracking

### DELETED FILES (review carefully)
- `scripts/hooks/post-checkout`
- `scripts/hooks/post-commit`
- `scripts/hooks/post-commit-setup-sync`
- `scripts/hooks/post-merge`
- `scripts/hooks/post-push`
- `scripts/hooks/pre-commit`

### UNTRACKED
- `scripts/hooks/` directory (new files)

**Question**: Are the hook files being REORGANIZED or REMOVED? Need to verify before committing.

---

## RECOMMENDED NEXT STEPS

1. **STOP**: Don't commit yet
2. **VERIFY**: Check what's in the untracked `scripts/hooks/` directory
3. **CLARIFY**: Are hooks being reorganized or removed?
4. **PROCEED SAFELY**: Once clarified, commit with clear message

---

## Once Confirmed Safe:

1. Commit staged changes to orchestration-tools-changes
2. Push to origin/orchestration-tools-changes
3. Create phase-by-phase action items in todos
4. Execute P0 workflows on appropriate branch
5. Create feature branches for Task 3 & Task 7 work

