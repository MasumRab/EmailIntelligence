# Git Branch Sync - Quick Reference Guide

## Command Quick Links

### View current branch status across repos:
```bash
for repo in EmailIntelligence EmailIntelligenceQwen EmailIntelligenceGem EmailIntelligenceAuto EmailIntelligenceAider rulesync PR/EmailIntelligence worktrees/taskmaster-worktree; do
  echo "=== $repo ===" && cd /home/masum/github/$repo && git branch -vv && echo ""
done
```

### Fix severely out-of-sync branch:
```bash
cd /home/masum/github/EmailIntelligence
git checkout orchestration-tools
git fetch origin
git log --oneline origin/orchestration-tools..HEAD  # local commits
git log --oneline HEAD..origin/orchestration-tools  # missing remote commits
git pull origin orchestration-tools  # or rebase: git rebase origin/orchestration-tools
```

### Sync all behind branches in one repo:
```bash
cd /home/masum/github/EmailIntelligenceQwen
git fetch origin
for branch in feature-notmuch-tagging-1 main orchestration-tools scientific; do
  git branch -D $branch
  git checkout --track origin/$branch
done
```

### Review stashes for a repo:
```bash
cd /home/masum/github/EmailIntelligence  # or other repo with stashes
git stash list  # see all
git stash show stash@{0}  # review specific stash
git stash pop stash@{0}  # recover stash
git stash drop stash@{0}  # discard stash
```

---

## Urgent Actions (Today)

| Action | Command | Impact |
|--------|---------|--------|
| Check orchestration-tools | `cd /home/masum/github/EmailIntelligence && git log --oneline HEAD..origin/orchestration-tools \| head` | Find missing 59 commits |
| Review high-stash repos | `for repo in EmailIntelligenceQwen EmailIntelligence EmailIntelligenceGem; do cd /home/masum/github/$repo && echo "=== $repo ===" && git stash list \| head -3; done` | Prevent work loss |
| Check uncommitted files | `cd /home/masum/github/EmailIntelligence && git status` | Resolve deleted hooks |

---

## Sync Status Legend

- ✅ **In Sync** - Branch matches remote (no action needed)
- ⚠️ **Behind** - Local is behind remote (needs pull/rebase)
- ⚠️⚠️ **Severely Behind** - More than 10 commits behind
- 🔴 **Diverged** - Both ahead and behind (needs resolve strategy)
- 🟡 **Ahead** - Local is ahead of remote

---

## Critical Findings Summary

### Branches Requiring Immediate Attention

1. **EmailIntelligence/orchestration-tools** - Behind 59 commits ⚠️⚠️
2. **EmailIntelligenceGem/orchestration-tools** - Ahead 57, Behind 28 🔴
3. **EmailIntelligenceQwen** - 11 stashes + 35 uncommitted changes
4. **EmailIntelligence** - 14 stashes + hook deletions

### Data Points
- **Total out-of-sync branches:** 19
- **Total stashes to review:** 51
- **Repos with 10+ stashes:** 3 (Qwen, Intelligence, Gem)
- **Repos needing action:** 6/8

---

## Next Actions (Priority Order)

### Week 1: Analysis & Critical Fixes
- [ ] Pull missing 59 commits for EmailIntelligence/orchestration-tools
- [ ] Review and process 51 stashes
- [ ] Commit or discard 35+ uncommitted changes in Qwen
- [ ] Resolve hook deletions in Intelligence repo

### Week 2: Sync & Cleanup
- [ ] Pull all branches that are behind
- [ ] Resolve diverged branches (scientific, taskmaster)
- [ ] Clean untracked configuration files
- [ ] Consolidate tool configs to workspace root

### Week 3: Documentation & Prevention
- [ ] Create BRANCH_STATUS.md for future reference
- [ ] Archive stale feature branches
- [ ] Update global gitignore rules
- [ ] Document active development branches

---

*Report generated: 2025-11-10*  
*Full details: See GIT_SCAN_REPORT.md*
