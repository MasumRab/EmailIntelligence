# Merge/Rebase Task Guide: EmailIntelligenceQwen Repository

**Generated:** 2025-01-13
**Repository:** /home/masum/github/EmailIntelligenceQwen
**Guide Version:** 1.0

---

## Executive Summary

This guide provides instructions for synchronizing branches in the EmailIntelligenceQwen repository. This repository has several branches requiring attention, with one diverged branch needing careful merge strategy.

---

## Branch Status Overview

### Current Branch States

| Branch | Position | Status | Action Required |
|--------|----------|--------|-----------------|
| `orchestration-tools-launch-refractor` | ahead 1 | Ahead-only | Push or squash |
| `main` | Clean | No divergence | No action needed |
| `orchestration-tools` | behind origin by 3 | Behind-only | Pull with rebase |
| `scientific` | ahead 5, behind 5 | **Diverged** | Manual merge required |
| `taskmaster` | behind origin by 21 | Behind-only | Pull with rebase |

---

## Divergence Analysis

### Key Points

1. **orchestration-tools-launch-refractor** - Has 1 uncommitted/pending commit ahead
2. **main** - Clean, no action needed
3. **orchestration-tools** - Only 3 commits behind, simple sync
4. **scientific** - Diverged (5 ahead, 5 behind), needs manual merge
5. **taskmaster** - 21 commits behind, moderate sync

---

## Recommended Merge Strategies

### Branch 1: orchestration-tools (behind 3)

**Strategy:** Simple rebase

```bash
cd /home/masum/github/EmailIntelligenceQwen
git fetch origin

git checkout orchestration-tools
git branch orchestration-tools-backup-$(date +%Y%m%d)

git rebase origin/orchestration-tools
git push origin orchestration-tools --force-with-lease
```

### Branch 2: orchestration-tools-launch-refractor (ahead 1)

**Strategy:** Push or squash

```bash
cd /home/masum/github/EmailIntelligenceQwen
git checkout orchestration-tools-launch-refractor

# Option A: Push if ready
git push origin orchestration-tools-launch-refractor

# Option B: Squash if commit is incomplete
git rebase -i HEAD~1
git push origin orchestration-tools-launch-refractor --force-with-lease
```

### Branch 3: scientific (ahead 5, behind 5)

**Strategy:** Manual merge

```bash
cd /home/masum/github/EmailIntelligenceQwen
git fetch origin

git checkout scientific
git branch scientific-backup-$(date +%Y%m%d)

# Merge remote changes
git merge origin/scientific -m "Sync scientific with origin"

# Manual conflict resolution if needed
git mergetool

# Test
cd setup && python -m pytest

# Push
git push origin scientific
```

### Branch 4: taskmaster (behind 21)

**Strategy:** Rebase

```bash
cd /home/masum/github/EmailIntelligenceQwen
git checkout taskmaster
git branch taskmaster-backup-$(date +%Y%m%d)

git rebase origin/taskmaster
git push origin taskmaster --force-with-lease
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
git branch backup-orchestration-tools-launch-refractor-$(date +%Y%m%d)
git branch backup-scientific-$(date +%Y%m%d)
git branch backup-taskmaster-$(date +%Y%m%d)

# If issues occur
git checkout backup-branch-name
git reset --hard backup-branch-name
```

---

## Execution Sequence

1. **Backup all branches**
2. **Push/sync orchestration-tools-launch-refractor** (if ready)
3. **Sync orchestration-tools**
4. **Merge scientific** (complex)
5. **Sync taskmaster**
6. **Validate and push**

---

*This guide was generated based on git analysis performed on 2025-01-13.*
