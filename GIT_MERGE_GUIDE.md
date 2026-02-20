# Merge/Rebase Task Guide: Email Intelligence Repository

**Generated:** 2025-01-13
**Repository:** /home/masum/github/EmailIntelligenceGem
**Guide Version:** 1.0

---

## Executive Summary

This guide provides instructions for synchronizing branches in the Email Intelligence repository. This repository is in relatively good shape with most branches either clean or requiring simple synchronization.

---

## Branch Status Overview

### Current Branch States

| Branch | Position | Status | Action Required |
|--------|----------|--------|-----------------|
| `004-guided-workflow` | Current | **Clean** | No action needed |
| `main` | Clean | No commits behind | No action needed |
| `taskmaster` | Clean | No divergence | No action needed |
| `orchestration-tools` | behind origin by 5 | Behind-only | Pull with rebase |
| `scientific` | behind origin by 4 | Behind-only | Pull with rebase |

---

## Divergence Analysis

### Key Points

1. **004-guided-workflow** - Current working branch, clean state
2. **main** - Already synchronized with origin
3. **taskmaster** - Clean, no action needed
4. **orchestration-tools** - Only 5 commits behind, simple sync
5. **scientific** - Only 4 commits behind, simple sync

This repository requires minimal intervention compared to others.

---

## Recommended Merge Strategies

### Branch 1: orchestration-tools (behind 5)

**Strategy:** Simple rebase

```bash
cd /home/masum/github/EmailIntelligenceGem
git fetch origin

git checkout orchestration-tools
git branch orchestration-tools-backup-$(date +%Y%m%d)

git rebase origin/orchestration-tools

# If conflicts (unlikely with only 5 commits):
git add -A
git rebase --continue

git push origin orchestration-tools --force-with-lease
```

### Branch 2: scientific (behind 4)

**Strategy:** Simple rebase

```bash
cd /home/masum/github/EmailIntelligenceGem
git checkout scientific
git branch scientific-backup-$(date +%Y%m%d)

git rebase origin/scientific

# If conflicts (unlikely with only 4 commits):
git add -A
git rebase --continue

git push origin scientific --force-with-lease
```

---

## Testing Requirements

```bash
# Run tests after sync
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
git branch backup-scientific-$(date +%Y%m%d)

# If issues occur
git checkout backup-branch-name
git reset --hard backup-branch-name
```

---

## Execution Sequence

1. **Backup orchestration-tools**
2. **Sync orchestration-tools**
3. **Backup scientific**
4. **Sync scientific**
5. **Validate and push**

---

*This guide was generated based on git analysis performed on 2025-01-13.*
