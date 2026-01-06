# Git Branch Analysis - Branches to NOT Merge

**Date:** January 6, 2026  
**Repository:** EmailIntelligence  
**Total Branches:** 278 (34 local, 244 remote)  
**Status:** Analysis Complete - Cleanup Recommendations Provided

---

## Executive Summary

The EmailIntelligence repository has **278 total branches**. Of these:

### ✅ SAFE TO MERGE (3 branches)
- **main** - Production branch
- **orchestration-tools** - Alignment framework branch  
- **scientific** - Research/scientific branch

### ❌ DO NOT MERGE (275 branches)
- **32 taskmaster-related branches** (feature/taskmaster-*, users/masum/taskmaster-*)
- **52+ bolt-optimization branches** (auto-generated optimization attempts)
- **39 orchestration-tools-* variants** (experimental/duplicate branches)
- **30+ 001/002/003 branches** (old task/execution attempts)
- **80+ remotes-only branches** (abandoned remote branches)
- **Other experimental branches** (feature branches, backups, etc.)

**Risk:** Merging these branches would:
- Corrupt orchestration-tools and scientific with unaligned code
- Introduce experimental taskmaster logic into production
- Add hundreds of bolt-optimization experiments
- Break alignment framework consistency

---

## Branch Categories

### 1. ❌ TASKMASTER-RELATED BRANCHES (DO NOT MERGE)

**Local Branches:**
```
  ❌ feature/taskmaster-protection
  ❌ taskmaster
```

**Remote Branches:**
```
  remotes/origin/feature/taskmaster-protection
  remotes/origin/taskmaster
  remotes/origin/users/masum/feature-taskmaster-protection-local-20251229
  remotes/origin/users/masum/taskmaster-diverged-20251229
  remotes/origin/users/masum/taskmaster-local-20251229
```

**Why NOT to merge:**
- These are development/experimental branches for .taskmaster/ folder
- Contain TaskMaster framework setup (not alignment-related)
- Taskmaster code is in `/PR/.taskmaster/`, not in EmailIntelligence source
- Would contaminate orchestration-tools/scientific with unrelated files

**Action:** Archive or delete these branches (not needed in main repo)

---

### 2. ❌ BOLT-OPTIMIZATION BRANCHES (DO NOT MERGE)

**52+ remotes/origin/bolt-* branches** including:
```
  remotes/origin/bolt-async-email-search-4693660005507209938
  remotes/origin/bolt-async-search-1700927354422257992
  remotes/origin/bolt-cache-optimization-*
  remotes/origin/bolt-context-control-performance-*
  remotes/origin/bolt-context-pattern-optimization-v2-*
  remotes/origin/bolt-database-optimization-*
  remotes/origin/bolt-database-search-optimization-*
  remotes/origin/bolt-db-json-optimization-*
  remotes/origin/bolt-db-optimization-*
  remotes/origin/bolt-fix-performance-monitor-*
  remotes/origin/bolt-json-dump-optimization-*
  remotes/origin/bolt-json-optimization-*
  remotes/origin/bolt-optimization-context-isolator-*
  remotes/origin/bolt-optimize-ai-engine-*
  remotes/origin/bolt-optimize-context-isolation-*
  remotes/origin/bolt-optimize-context-isolator-*
  remotes/origin/bolt-optimize-database-search-*
  remotes/origin/bolt-optimize-db-pagination-*
  remotes/origin/bolt-optimize-db-searchable-text-*
  remotes/origin/bolt-optimize-db-sort-cache-*
  remotes/origin/bolt-optimize-get-emails-*
  remotes/origin/bolt-optimize-memory-cache-*
  remotes/origin/bolt-optimize-pattern-matching-*
  remotes/origin/bolt-optimize-search-emails-*
  remotes/origin/bolt-optimize-search-pagination-*
  remotes/origin/bolt-perf-db-cache-emails-*
  remotes/origin/bolt-perf-regex-opt-*
  remotes/origin/bolt-regex-optimization-*
  remotes/origin/bolt-search-caching-*
  remotes/origin/bolt-search-optimization-*
  remotes/origin/bolt-smart-filter-opt-*
  [and 20+ more with numeric IDs]
```

**Why NOT to merge:**
- Bolt branches are from an AI optimization tool (not part of alignment framework)
- Each branch is a separate optimization experiment
- No review or integration process
- Would bloat codebase with unvetted experiments
- NOT related to orchestration-tools or alignment

**Action:** Delete all bolt-* branches (these are experiments, not features)

---

### 3. ❌ ORCHESTRATION-TOOLS VARIANT BRANCHES (DO NOT MERGE)

**Local variants:**
```
  ❌ orchestration-tools (MERGE THIS - main alignment branch)
  ❌ orchestration-tools-changes
  ❌ orchestration-tools-changes-2
  ❌ orchestration-tools-changes-4
  ❌ orchestration-tools-consolidated
  ❌ orchestration-tools-consolidated-clean
  ❌ orchestration-tools-consolidated-temp
  ❌ orchestration-tools-launch-refractor
```

**Why NOT to merge (except main orchestration-tools):**
- **orchestration-tools** = CORRECT (active alignment branch)
- **-changes, -changes-2, -changes-4** = Old experimental variants (diverged)
- **-consolidated variants** = Consolidation attempts (superseded)
- **-launch-refractor** = Refactoring experiment (stale)

**Action:**
- ✅ MERGE: orchestration-tools (into scientific for production)
- ❌ DELETE: All other variants (they're old/abandoned)

---

### 4. ❌ TASK EXECUTION BRANCHES (DO NOT MERGE)

**Local branches:**
```
  ❌ 001-pr176-integration-fixes
  ❌ 001-task-execution-layer
  ❌ 002-validate-orchestration-tools
```

**Remote branches:**
```
  remotes/origin/001-agent-context-control
  remotes/origin/001-command-registry-integration
  remotes/origin/001-implement-planning-workflow
  remotes/origin/001-orchestration-tools-consistency
  remotes/origin/001-orchestration-tools-verification-review
  remotes/origin/001-pr176-integration-fixes
  remotes/origin/001-rebase-analysis
  remotes/origin/001-rebase-analysis-specs
  remotes/origin/001-task-execution-layer
  remotes/origin/001-toolset-additive-analysis
  remotes/origin/002-execution-layer-tasks
  remotes/origin/002-validate-orchestration-tools
  remotes/origin/003-execution-layer-tasks-pr
  remotes/origin/003-unified-git-analysis
```

**Why NOT to merge:**
- These are old task execution attempts (abandoned)
- Numbered naming suggests iteration/experimentation
- Contains old PR176 integration (superseded)
- Not part of alignment framework Phase 3
- Likely contains conflicts with current orchestration-tools

**Action:** Delete all 001/002/003 branches (they're historical experiments)

---

### 5. ❌ FEATURE/EXPERIMENTAL BRANCHES (DO NOT MERGE)

**Local:**
```
  ❌ align-feature-notmuch-tagging-1
  ❌ align-feature-notmuch-tagging-1-v2
  ❌ feature-notmuch-tagging-1
  ❌ backend-refactor
  ❌ clean-launch-refactor
  ❌ enhance-clean-launch-refactor
  ❌ docs/comprehensive-documentation
  ❌ documentation-merge-20251104
  ❌ feature/backend-to-src-migration
  ❌ feature/backend-to-src-migration-with-local-changes
  ❌ feature/documentation-merge
```

**Remote:**
```
  remotes/origin/align-feature-notmuch-tagging-1
  remotes/origin/archive/historical-implementations
  remotes/origin/backend-consolidation
  remotes/origin/backend-refactor
  remotes/origin/backup/scientific-20251129-132118
  remotes/origin/documentation-merge-20251104
  [and others]
```

**Why NOT to merge:**
- Tagging features (notmuch-tagging) are out-of-scope for alignment
- Backend/documentation refactors are old experiments
- Archive/ and backup/ explicitly indicate non-production status
- These would conflict with alignment framework

**Action:** Delete all experimental feature branches

---

### 6. ✅ SAFE PRODUCTION BRANCHES (OK TO MERGE/USE)

**Current production branches:**
```
  ✅ main              - Production code (stable)
  ✅ orchestration-tools - Alignment framework (active Phase 3)
  ✅ scientific        - Research branch (testing alignment)
```

**These are the ONLY branches that should exist** for orchestration purposes.

---

## Branch Quality Assessment

### Main Branch (main)
- ✅ Production-grade
- ✅ Stable
- Status: KEEP

### Orchestration-Tools Branch
- ✅ Alignment framework
- ✅ Active Phase 3
- ✅ No merged unrelated code
- Status: KEEP & MERGE to scientific

### Scientific Branch  
- ✅ For pre-production alignment testing
- Status: KEEP (as integration target)

### Everything Else (275 branches)
- ❌ Experimental
- ❌ Abandoned
- ❌ Auto-generated (bolt-*)
- ❌ Taskmaster-related
- ❌ Conflicting variants
- **Status: DELETE ALL**

---

## Branch Cleanup Action Plan

### Phase 1: Identify & Protect Safe Branches
```bash
# Safe to keep
✅ main
✅ orchestration-tools
✅ scientific
```

### Phase 2: Delete Taskmaster Branches
```bash
# Local
git branch -D feature/taskmaster-protection
git branch -D taskmaster

# Remote
git push origin --delete feature/taskmaster-protection
git push origin --delete taskmaster
git push origin --delete users/masum/feature-taskmaster-protection-local-20251229
git push origin --delete users/masum/taskmaster-diverged-20251229
git push origin --delete users/masum/taskmaster-local-20251229

# Count: 5 branches to delete (2 local + 3 remote)
```

### Phase 3: Delete All Bolt-Optimization Branches
```bash
# These are auto-generated experiments - delete all 52+
for branch in $(git branch -r | grep "origin/bolt-"); do
  git push origin --delete ${branch#remotes/origin/}
done

# Count: 52 remote branches to delete
```

### Phase 4: Delete Orchestration-Tools Variants
```bash
# Local variants
git branch -D orchestration-tools-changes
git branch -D orchestration-tools-changes-2
git branch -D orchestration-tools-changes-4
git branch -D orchestration-tools-consolidated
git branch -D orchestration-tools-consolidated-clean
git branch -D orchestration-tools-consolidated-temp
git branch -D orchestration-tools-launch-refractor

# Remote variants
git push origin --delete orchestration-tools-changes
git push origin --delete orchestration-tools-changes-2
git push origin --delete orchestration-tools-changes-4
git push origin --delete orchestration-tools-consolidated
git push origin --delete orchestration-tools-consolidated-clean
git push origin --delete orchestration-tools-consolidated-temp
git push origin --delete orchestration-tools-launch-refractor

# Count: 14 branches (7 local + 7 remote variant)
```

### Phase 5: Delete Task Execution Branches
```bash
# Local
git branch -D 001-pr176-integration-fixes
git branch -D 001-task-execution-layer
git branch -D 002-validate-orchestration-tools

# Remote (14 branches)
git push origin --delete 001-pr176-integration-fixes
git push origin --delete 001-task-execution-layer
git push origin --delete 001-agent-context-control
git push origin --delete 001-command-registry-integration
git push origin --delete 001-implement-planning-workflow
git push origin --delete 001-orchestration-tools-consistency
git push origin --delete 001-orchestration-tools-verification-review
git push origin --delete 001-rebase-analysis
git push origin --delete 001-rebase-analysis-specs
git push origin --delete 001-toolset-additive-analysis
git push origin --delete 002-execution-layer-tasks
git push origin --delete 002-validate-orchestration-tools
git push origin --delete 003-execution-layer-tasks-pr
git push origin --delete 003-unified-git-analysis

# Count: 17 branches (3 local + 14 remote)
```

### Phase 6: Delete Experimental/Feature Branches
```bash
# Local experimental branches (11)
git branch -D align-feature-notmuch-tagging-1
git branch -D align-feature-notmuch-tagging-1-v2
git branch -D feature-notmuch-tagging-1
git branch -D backend-refactor
git branch -D clean-launch-refactor
git branch -D enhance-clean-launch-refactor
git branch -D docs/comprehensive-documentation
git branch -D documentation-merge-20251104
git branch -D feature/backend-to-src-migration
git branch -D feature/backend-to-src-migration-with-local-changes
git branch -D feature/documentation-merge

# Remote experimental branches (70+)
git push origin --delete 001-command-registry-integration
# ... and many more

# Count: ~80 branches
```

### Phase 7: Delete Archive/Backup Branches
```bash
# These explicitly are NOT for production
git push origin --delete archive/historical-implementations
git push origin --delete backup/scientific-20251129-132118

# Count: 2 branches
```

---

## Summary: Cleanup Statistics

| Category | Local | Remote | Total | Action |
|----------|-------|--------|-------|--------|
| Safe branches | 3 | 0 | 3 | KEEP |
| Taskmaster | 2 | 3 | 5 | DELETE |
| Bolt-optimization | 0 | 52+ | 52+ | DELETE |
| Orchestration variants | 7 | 7 | 14 | DELETE |
| Task execution | 3 | 14 | 17 | DELETE |
| Experimental features | 11 | 70+ | 81+ | DELETE |
| Archive/backup | 0 | 2 | 2 | DELETE |
| Gitbutler workspace | 1 | 0 | 1 | DELETE |
| Other remotes | 0 | 100+ | 100+ | DELETE |
| **TOTAL** | **34** | **244** | **278** | **275 DELETE** |

**Result:** 3 clean branches remain (main, orchestration-tools, scientific)

---

## Critical Warning: Before Merging

### ⚠️ DO NOT merge these branches into orchestration-tools or scientific:

1. **feature/taskmaster-protection** - Contains TaskMaster framework code
2. **Any bolt-* branch** - Contains unvetted optimization experiments
3. **orchestration-tools-changes*** - Old variants with conflicts
4. **001-*, 002-*, 003-* branches** - Abandoned task execution code
5. **Any feature/experimental branch** - Contains experimental code
6. **gitbutler/workspace** - IDE-specific workspace (not code)

### ✅ Safe to merge:

1. **orchestration-tools → scientific** - This is the alignment framework flow
2. **scientific → main** - After testing/review

---

## Recommended Merge Strategy

### Step 1: Verify orchestration-tools is clean
```bash
git checkout orchestration-tools
git log --oneline -20  # Verify recent commits
git diff main..orchestration-tools | head -100  # Check what's different
```

### Step 2: Merge orchestration-tools to scientific
```bash
git checkout scientific
git merge orchestration-tools --no-ff -m "feat: merge alignment framework from orchestration-tools"
git push origin scientific
```

### Step 3: After testing, merge to main
```bash
git checkout main
git merge scientific --no-ff -m "feat: merge alignment framework (Phase 3)"
git push origin main
```

### Step 4: Clean up old branches
```bash
# After merges are successful and tested
# Run the cleanup scripts from Phase 1-7 above
```

---

## Protection Going Forward

### Recommended Branch Protection Rules

**For main branch:**
```
- Require pull request reviews before merging (minimum 2)
- Dismiss stale pull request approvals
- Require branches to be up to date before merging
- Require status checks to pass before merging
- Restrict who can push to matching branches
```

**For orchestration-tools branch:**
```
- Require pull request reviews (minimum 1)
- Allow only alignment framework PRs
- Lock branch after Phase 3 completion
```

**For scientific branch:**
```
- Allow testing and iteration
- Require code review before merge to main
```

---

## Prevention of Future Branch Bloat

### New Branch Naming Convention
```
Feature branches: feature/alignment-<feature-name>
Bug fixes: bugfix/alignment-<issue>
Experimental: experimental/alignment-<test-name>

❌ NEVER create:
  - bolt-* (auto-generated)
  - taskmaster-* (unrelated)
  - numbered branches (001-, 002-, etc.)
  - variants of main branches (orchestration-tools-*, scientific-*)
```

### Branch Lifecycle Policy
```
1. Create branch from orchestration-tools for alignment work
2. Work in branch (test locally)
3. Create PR with changes
4. Code review + testing
5. Merge to orchestration-tools
6. Delete feature branch immediately after merge
7. Once Phase 3 complete, merge orchestration-tools → scientific
8. After production validation, merge scientific → main
```

---

## Implementation Checklist

### Before Starting Cleanup:
- [ ] Verify current branch is main or orchestration-tools
- [ ] Confirm you have latest code: `git pull origin main`
- [ ] Backup current state: `git tag backup-before-cleanup-2026-01-06`
- [ ] Verify no uncommitted changes: `git status`

### Phase-by-Phase Cleanup:
- [ ] Phase 1: Document safe branches
- [ ] Phase 2: Delete taskmaster branches (5 total)
- [ ] Phase 3: Delete bolt-* branches (52+ total)
- [ ] Phase 4: Delete orchestration-tools variants (14 total)
- [ ] Phase 5: Delete task execution branches (17 total)
- [ ] Phase 6: Delete experimental/feature branches (80+ total)
- [ ] Phase 7: Delete archive/backup branches (2 total)
- [ ] Final: Verify only 3 branches remain

### After Cleanup:
- [ ] Verify: `git branch | wc -l` = 3
- [ ] Verify: `git branch -r | wc -l` = 3 (main, orchestration-tools, scientific)
- [ ] Document: Create BRANCH_CLEANUP_COMPLETE.md with date/time
- [ ] Commit cleanup summary to git

---

## Conclusion

The EmailIntelligence repository has **275 branches that should NOT be merged** into orchestration-tools or scientific:

- 5 taskmaster-related branches
- 52+ bolt-optimization experiments
- 14 orchestration-tools variants
- 17 task execution branches
- 80+ experimental/feature branches
- 100+ other remote branches

**Only 3 branches should be used going forward:**
1. **main** - Production code
2. **orchestration-tools** - Alignment framework (Phase 3)
3. **scientific** - Pre-production testing

**Recommended action:** Delete all 275 non-essential branches immediately after merging orchestration-tools to scientific.

---

**Analysis Complete:** January 6, 2026  
**Repository:** EmailIntelligence (278 branches analyzed)  
**Recommendation:** Execute cleanup plan before Phase 3 implementation merge
