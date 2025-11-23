# Diverged Branches Detailed Analysis

**8 branches have diverged** - both local and remote have unique commits. Resolution strategy varies by severity.

---

## 🔴 CRITICAL DIVERGENCE

### EmailIntelligenceGem / orchestration-tools
**Status:** ahead 57, behind 28 commits | **Severity:** CRITICAL

**Issue:** Heavily diverged in opposite directions. Local is 57 commits ahead but also 28 commits behind.

**Local-only commits (57):**
```
fe220f6 docs: amend constitution to v0.2.1 (principle refinements + TDD update)
40bec18 feat: Resolve static analysis errors in launch.py and configure pylint
2609115 fix: Update .gitignore for centralized agent markdown files
cf1fab3 feat: Centralize agent markdown files and update content
ec01c3b test: Temporary commit to diagnose commit errors
8a2592b feat: Apply setup and orchestration changes from stash@{11}
f9f8654 feat: Apply Backlog.md MCP Guidelines from stash@{7}
72941ee feat: Add disable-hooks.sh and enable-hooks.sh scripts
c0a8b11 Resolve merge conflicts and commit orchestration-related files
825df8a Update MANAGED_FILES to include new setup/ files and scripts
[+ 47 more local commits]
```

**Remote-only commits (28):**
```
982bfbc docs
e374183 docs: add quick start guide for branch update procedure
b5c1b22 feat: add automated branch update system for script propagation
4f221f1 docs: add comprehensive branch propagation implementation summary
1d28f84c feat: implement branch propagation policy and enforcement hooks
b77b40f merge: orchestration-tools-changes → orchestration-tools
6c17b72 docs(MODEL_CONTEXT_STRATEGY): add comprehensive model context distribution guide
bc676d2 docs: create standardized model-specific context guidelines
2b30816 docs(IMPROVED_PROMPT_ANSWERS): add Strategy 5 comprehensive answer (92% quality)
[+ 19 more remote commits]
```

**Root cause:** Parallel development on local and remote without synchronization. Local has worktree/AI setup improvements; remote has orchestration framework improvements.

**Resolution options:**
1. **Rebase local onto remote** (keep local workflow improvements):
   ```bash
   cd /home/masum/github/EmailIntelligenceGem
   git checkout orchestration-tools
   git rebase origin/orchestration-tools
   # Resolve conflicts, then force push (after review)
   ```

2. **Merge remote into local** (preserve both histories):
   ```bash
   cd /home/masum/github/EmailIntelligenceGem
   git checkout orchestration-tools
   git merge origin/orchestration-tools
   # Resolve conflicts, commit merge
   ```

3. **Force reset to remote** (discard local changes - NOT recommended without review):
   ```bash
   git reset --hard origin/orchestration-tools
   ```

**Recommendation:** Option 1 (rebase) - review what's worth keeping locally vs remote

---

## ⚠️ HIGH DIVERGENCE

### EmailIntelligenceQwen / orchestration-tools-temp
**Status:** ahead 2, behind 11 commits | **Severity:** HIGH

**Issue:** Local has 2 unique commits (merge conflict resolutions), remote has 11 newer commits (major features).

**Local-only commits (2):**
```
6ccb0c4 Resolve merge conflict: accept remote's version of scripts/hooks/post-checkout
932527b Commit staged changes related to orchestration hook management and cleanup script
```

**Remote-only commits (11):**
```
f63324d Merge pull request #201 from MasumRab/orchestration-tools-changes
e58be0e feat: add P0 CI/CD workflows (test and lint)
1f006c7 feat: add orchestration workflow documentation and hook cleanup
c545f0c docs: add comprehensive orchestration workflows and implementation roadmap
d4f60e0 docs: add sync framework review and updated single-branch options
4c3c466 feat: add orchestration file extraction and simplified documentation
a5107c1 docs: add simplified orchestration guide
2dfdbd7 docs: add orchestration quick reference guide
c8c6539 docs: add comprehensive orchestration push workflow documentation and PR template
c30db51 feat: add disable/enable hooks scripts for independent setup development
[+ 1 more remote commits]
```

**Root cause:** Local was created for temporary merge conflict resolution but remote evolved with major feature additions. This appears to be a throwaway/temp branch.

**Recommendation:** Either delete local and checkout from remote, or pull and discard local commits:
```bash
cd /home/masum/github/EmailIntelligenceQwen
git checkout orchestration-tools-temp
git reset --hard origin/orchestration-tools
# Prefer: Consider if this branch is still needed
```

---

### EmailIntelligenceGem / scientific
**Status:** ahead 9, behind 3 commits | **Severity:** MEDIUM-HIGH

**Issue:** Local has 9 merge/setup commits, remote has 3 config commits.

**Local-only commits (9):**
```
38ff3fc Complete merge on scientific branch
34de9c6 Merge remote-tracking branch 'origin/scientific' into scientific
e114296 fix: Update managed files lists to include launch.py and test files
2b2a506 Merge remote-tracking branch 'origin/scientific' into scientific
1d3f3c9 feat: Complete Git hook loop prevention and worktree/subtree detection
e5555df Apply stashed changes from scientific branch, excluding orchestration-specific files
141819b feat: Update jules_mcp_schedule.json and task status
79a4dce Fix merge artifacts in Git hooks
b4e2c57 Fix subprocess security vulnerabilities in setup modules
```

**Remote-only commits (3):**
```
3133f1f agent guidance
66bdc08 docs: Update AGENTS.md with correct worktree behavior
8a4fc2e Update AI configs from centralized .aiglobal
```

**Root cause:** Local has setup/security fixes; remote has config updates. Both worth keeping.

**Recommendation:** Merge remote into local (simplest since remote is older):
```bash
cd /home/masum/github/EmailIntelligenceGem
git checkout scientific
git merge origin/scientific
# Resolve any conflicts
```

---

### PR/EmailIntelligence / scientific
**Status:** ahead 11, behind 3 commits | **Severity:** MEDIUM-HIGH

**Issue:** Local has 11 docs/plan commits; remote has 3 config commits.

**Local-only commits (11):**
```
42275c9 docs: distribute .github/instructions to scientific branch
b5753ab Save changes before switching to orchestration-tools
383c7863 Add backlog tasks to scientific branch
d355155 docs: Update staged development plan with latest PR CI status
959e92e docs: Create comprehensive required code changes analysis
6ef77cc docs: Create detailed execution plan with daily tasks and timelines
b567423 docs: Create comprehensive staged development plan
f93d6f1 docs: Create comprehensive AGENTS.md for agentic coding tools
d202501 fix: Resolve PR CI failures and merge conflicts
79a4dce Fix merge artifacts in Git hooks
[+ 1 more local]
```

**Remote-only commits (3):**
```
3133f1f agent guidance
66bdc08 docs: Update AGENTS.md with correct worktree behavior
8a4fc2e Update AI configs from centralized .aiglobal
```

**Root cause:** This is a PR-specific branch with local documentation work; remote is parent branch updates.

**Recommendation:** Merge remote into local to get config updates:
```bash
cd /home/masum/github/PR/EmailIntelligence
git checkout scientific
git merge origin/scientific
```

---

### PR/EmailIntelligence / taskmaster
**Status:** ahead 2, behind 8 commits | **Severity:** MEDIUM-HIGH

**Issue:** Local has 2 task cleanup commits; remote has 8 sync commits.

**Local-only commits (2):**
```
584814a refactor: Consolidate and clean task database
a674c25 fix: Restore and clean task database from corrupted tasks_new.json
```

**Remote-only commits (8):**
```
efd2244 fix: correct corrupted task JSON files
beccf24 feat: synchronize orchestration changes
827d3cd feat: synchronize orchestration changes
8a600d5 feat: complete taskmaster synchronization
ea2244e feat: complete taskmaster synchronization
24627bd feat: synchronize taskmaster config and clean up task files
0b90033 feat: synchronize taskmaster config and resolve merge
e1cd633 feat: synchronize taskmaster config and clean up task files
```

**Root cause:** Both sides attempting task cleanup independently. Remote is official source.

**Recommendation:** Rebase local onto remote (local cleanup work may be redundant):
```bash
cd /home/masum/github/PR/EmailIntelligence
git checkout taskmaster
git rebase origin/taskmaster
# Or reset if cleanup is already covered:
git reset --hard origin/taskmaster
```

---

## ⚠️ MINOR DIVERGENCE

### EmailIntelligenceQwen / feature-notmuch-tagging-1
**Status:** ahead 1, behind 1 commit | **Severity:** LOW

**Issue:** Single-commit divergence, likely conflicting work.

**Local commit:**
```
7f94dac Add orchestration tools and sync scripts from align-feature-notmuch-tagging-1-v2
```

**Remote commit:**
```
cefe368 Save current changes
```

**Root cause:** Parallel commits to same feature branch without coordination.

**Recommendation:** Merge or rebase (either works for single commit):
```bash
cd /home/masum/github/EmailIntelligenceQwen
git checkout feature-notmuch-tagging-1
git merge origin/feature-notmuch-tagging-1
# or: git rebase origin/feature-notmuch-tagging-1
```

---

### EmailIntelligenceQwen / taskmaster
**Status:** ahead 6, behind 5 commits | **Severity:** LOW

**Issue:** Parallel cleanup work - similar commits on both sides.

**Local commits (6):**
```
a5b6cf7 Flatten structure: move .taskmaster contents to root
cc7b729 Remove .env from taskmaster worktree
840cd40 Remove non-core taskmaster AI files
4410cd9 Clean up non-taskmaster files from worktree
75aeb18 Move opencode.json to ~/central
cd1c8ab 1
```

**Remote commits (5):**
```
dd61677 Remove .env from taskmaster worktree
3df0017 Remove non-core taskmaster AI files
89e089e Clean up non-taskmaster files from worktree
543a8ac Move opencode.json to ~/central
a4849ce 1
```

**Root cause:** Nearly identical commits (probably stashed work applied twice). Local has extra "Flatten structure" commit.

**Recommendation:** Rebase local onto remote to clean up duplicates:
```bash
cd /home/masum/github/EmailIntelligenceQwen
git checkout taskmaster
git rebase origin/taskmaster
# Will likely have conflicts/duplicates to resolve
```

---

### EmailIntelligence / scientific
**Status:** ahead 2, behind 3 commits | **Severity:** LOW

**Issue:** Small divergence in security/setup fixes vs config updates.

**Local commits (2):**
```
79a4dce Fix merge artifacts in Git hooks
b4e2c57 Fix subprocess security vulnerabilities in setup modules
```

**Remote commits (3):**
```
3133f1f agent guidance
66bdc08 docs: Update AGENTS.md with correct worktree behavior
8a4fc2e Update AI configs from centralized .aiglobal
```

**Root cause:** Both fixing/updating the scientific branch independently.

**Recommendation:** Merge remote into local (both seem valuable):
```bash
cd /home/masum/github/EmailIntelligence
git checkout scientific
git merge origin/scientific
```

---

## Summary Table

| Repo | Branch | Status | Complexity | Recommendation |
|------|--------|--------|-----------|-----------------|
| EmailIntelligenceGem | orchestration-tools | +57/-28 | CRITICAL | Review then rebase |
| EmailIntelligenceQwen | orchestration-tools-temp | +2/-11 | HIGH | Reset to remote (temp branch) |
| EmailIntelligenceGem | scientific | +9/-3 | MEDIUM | Merge origin into local |
| PR/EmailIntelligence | scientific | +11/-3 | MEDIUM | Merge origin into local |
| PR/EmailIntelligence | taskmaster | +2/-8 | MEDIUM | Rebase or reset to origin |
| EmailIntelligence | scientific | +2/-3 | LOW | Merge origin into local |
| EmailIntelligenceQwen | feature-notmuch-tagging-1 | +1/-1 | LOW | Merge or rebase |
| EmailIntelligenceQwen | taskmaster | +6/-5 | LOW | Rebase to clean duplicates |

---

## Quick Resolution Script

```bash
#!/bin/bash

echo "=== Resolving Diverged Branches ==="

# CRITICAL: EmailIntelligenceGem/orchestration-tools - needs manual review
echo "1. EmailIntelligenceGem/orchestration-tools - REQUIRES MANUAL REVIEW"
echo "   Run: cd /home/masum/github/EmailIntelligenceGem && git log --oneline orchestration-tools..origin/orchestration-tools | head -20"

# HIGH: orchestration-tools-temp - reset to remote (temp branch)
cd /home/masum/github/EmailIntelligenceQwen
git checkout orchestration-tools-temp
git reset --hard origin/orchestration-tools
echo "✓ Reset orchestration-tools-temp"

# MEDIUM: Various scientific/taskmaster - merge or rebase
for repo_branch in \
  "/home/masum/github/EmailIntelligenceGem:scientific" \
  "/home/masum/github/PR/EmailIntelligence:scientific" \
  "/home/masum/github/EmailIntelligence:scientific"
do
  repo="${repo_branch%:*}"
  branch="${repo_branch#*:}"
  cd "$repo"
  git checkout $branch
  git merge origin/$branch
  echo "✓ Merged origin/$branch in $(basename $repo)"
done

# LOW: Merge/rebase small divergences
cd /home/masum/github/EmailIntelligenceQwen
git checkout feature-notmuch-tagging-1
git merge origin/feature-notmuch-tagging-1
echo "✓ Merged feature-notmuch-tagging-1"

echo "=== Done. Review results and push if needed ==="
```

---

*Generated: 2025-11-10*
