# Merge/Rebase Task Guide: EmailIntelligenceAider Repository

**Generated:** 2025-01-13
**Repository:** /home/masum/github/EmailIntelligenceAider
**Guide Version:** 1.0

---

## Executive Summary

This guide provides instructions for synchronizing branches in the EmailIntelligenceAider repository. This repository has fewer divergence issues compared to the main EmailIntelligence repository, but still requires careful attention to branch alignment.

---

## Branch Status Overview

### Current Branch States

| Branch | Position | Status | Action Required |
|--------|----------|--------|-----------------|
| `orchestration-tools` | behind origin by 7 | Behind-only | Pull with rebase |
| `scientific` | ahead 3, behind 1445 | **Diverged** | Manual merge required |
| `main` | behind origin/main by 6 | Behind-only | Pull with rebase |

---

## Divergence Analysis

### Key Points

1. **orchestration-tools** is only 7 commits behind - simple rebase will resolve
2. **scientific** has massive divergence (behind 1445) - requires careful merge strategy
3. **main** is 6 commits behind - simple pull will resolve

### Scientific Branch Divergence

The scientific branch in this repository is 1445 commits behind origin/scientific. This indicates:
- Major parallel development in the main EmailIntelligence repository
- Need to decide which changes to incorporate
- Potential for significant merge conflicts

---

## Recommended Merge Strategies

### Branch 1: orchestration-tools (behind 7)

**Strategy:** Simple rebase

```bash
cd /home/masum/github/EmailIntelligenceAider
git fetch origin

git checkout orchestration-tools
git branch orchestration-tools-backup-$(date +%Y%m%d)

# Rebase on top of remote
git rebase origin/orchestration-tools

# If conflicts (unlikely with only 7 commits):
git add -A
git rebase --continue

# Push updates
git push origin orchestration-tools
```

### Branch 2: main (behind 6)

**Strategy:** Simple pull with rebase

```bash
cd /home/masum/github/EmailIntelligenceAider
git checkout main
git branch main-backup-$(date +%Y%m%d)

git pull --rebase origin main
git push origin main
```

### Branch 3: scientific (ahead 3, behind 1445)

**Strategy:** Manual merge with careful conflict resolution

```bash
cd /home/masum/github/EmailIntelligenceAider
git fetch origin

git checkout scientific
git branch scientific-backup-$(date +%Y%m%d)

# Option A: Merge (preserves history)
git merge origin/scientific -m "Sync scientific with origin"

# Option B: Rebase then merge (cleaner history)
git rebase origin/scientific
git merge --ff-only origin/scientific

# Manual conflict resolution
git mergetool

# Test thoroughly
cd setup && python -m pytest
```

**Critical Consideration:** With 1445 commits of divergence, this is essentially a major merge operation. Consider:
1. What changes in origin/scientific are essential?
2. What local changes (ahead 3) must be preserved?
3. Can some changes be deferred to later?

---

## Testing Requirements

### Pre-Merge
```bash
# Verify current state
git status
git log --oneline -5

# Check for uncommitted changes
git diff --stat
```

### Post-Merge
```bash
# Run tests
cd setup
python -m pytest tests/ -v --tb=short

# Verify imports
python -c "from src.core import *; print('Imports OK')"
```

---

## Rollback Plan

```bash
# Before operations
git branch backup-orchestration-tools-$(date +%Y%m%d)
git branch backup-main-$(date +%Y%m%d)
git branch backup-scientific-$(date +%Y%m%d)

# If issues occur
git checkout backup-branch-name
git reset --hard backup-branch-name
```

---

## Execution Sequence

1. **Backup all branches**
2. **Sync orchestration-tools** (simple, low risk)
3. **Sync main** (simple, low risk)
4. **Merge scientific** (complex, high risk - may need team review)
5. **Validate and push**

---

*This guide was generated based on git analysis performed on 2025-01-13.*
