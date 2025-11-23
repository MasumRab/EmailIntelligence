# Fast-Forward Eligible Branches

## Summary
- **Branches can FF locally** (behind only): 10
- **Branches can FF to remote** (ahead only): 3
- **Branches that cannot FF** (diverged): 8

---

## Branches That Can Fast-Forward Locally (Pull)

These branches are behind remote and have no local commits ahead - can safely `git pull` for FF merge.

### EmailIntelligenceQwen (3 branches)
```bash
cd /home/masum/github/EmailIntelligenceQwen

# 1. main - behind 4 commits
git checkout main && git pull origin main

# 2. orchestration-tools - behind 13 commits  
git checkout orchestration-tools && git pull origin orchestration-tools

# 3. scientific - behind 8 commits
git checkout scientific && git pull origin scientific
```

### EmailIntelligence (3 branches)
```bash
cd /home/masum/github/EmailIntelligence

# 1. main - behind 10 commits
git checkout main && git pull origin main

# 2. orchestration-tools - behind 59 commits (CRITICAL)
git checkout orchestration-tools && git pull origin orchestration-tools

# 3. taskmaster - behind 9 commits
git checkout taskmaster && git pull origin taskmaster
```

### EmailIntelligenceGem (1 branch)
```bash
cd /home/masum/github/EmailIntelligenceGem

# 1. taskmaster - behind 10 commits
git checkout taskmaster && git pull origin taskmaster
```

### EmailIntelligenceAider (1 branch)
```bash
cd /home/masum/github/EmailIntelligenceAider

# 1. main - behind 1 commit
git checkout main && git pull origin main
```

---

## Branches That Can Fast-Forward to Remote (Push)

These branches are ahead of remote and have no divergence - can safely `git push` for FF merge.

### PR/EmailIntelligence (3 branches)
```bash
cd /home/masum/github/PR/EmailIntelligence

# 1. 001-implement-planning-workflow - ahead 1 commit
git checkout 001-implement-planning-workflow && git push origin 001-implement-planning-workflow

# 2. docs-cleanup - ahead 1 commit
git checkout docs-cleanup && git push origin docs-cleanup

# 3. main - ahead 1 commit
git checkout main && git push origin main
```

---

## Branches That Cannot FF (Diverged)

These branches have commits both locally and on remote - require merge, rebase, or force push.

| Repo | Branch | Status | Action Needed |
|------|--------|--------|---------------|
| EmailIntelligenceQwen | feature-notmuch-tagging-1 | ahead 1, behind 1 | Rebase or merge |
| EmailIntelligenceQwen | orchestration-tools-temp | ahead 2, behind 11 | Rebase or merge |
| EmailIntelligenceQwen | taskmaster | ahead 6, behind 5 | Rebase or merge |
| EmailIntelligence | scientific | ahead 2, behind 3 | Rebase or merge |
| EmailIntelligenceGem | orchestration-tools | ahead 57, behind 28 | Major divergence - investigate |
| EmailIntelligenceGem | scientific | ahead 9, behind 3 | Rebase or merge |
| PR/EmailIntelligence | scientific | ahead 11, behind 3 | Rebase or merge |
| PR/EmailIntelligence | taskmaster | ahead 2, behind 8 | Rebase or merge |

---

## Automated Fast-Forward Script

Run all FF-eligible updates:

```bash
#!/bin/bash

echo "=== Fast-forwarding all eligible branches ==="

# EmailIntelligenceQwen
cd /home/masum/github/EmailIntelligenceQwen
for branch in main orchestration-tools scientific; do
  echo "Pulling $branch in EmailIntelligenceQwen..."
  git checkout $branch && git pull origin $branch
done

# EmailIntelligence
cd /home/masum/github/EmailIntelligence
for branch in main orchestration-tools taskmaster; do
  echo "Pulling $branch in EmailIntelligence..."
  git checkout $branch && git pull origin $branch
done

# EmailIntelligenceGem
cd /home/masum/github/EmailIntelligenceGem
echo "Pulling taskmaster in EmailIntelligenceGem..."
git checkout taskmaster && git pull origin taskmaster

# EmailIntelligenceAider
cd /home/masum/github/EmailIntelligenceAider
echo "Pulling main in EmailIntelligenceAider..."
git checkout main && git pull origin main

# PR/EmailIntelligence
cd /home/masum/github/PR/EmailIntelligence
for branch in 001-implement-planning-workflow docs-cleanup main; do
  echo "Pushing $branch in PR/EmailIntelligence..."
  git checkout $branch && git push origin $branch
done

echo "=== Fast-forward operations complete ==="
```

---

## Recommended Execution Order

1. **First:** Push PR/EmailIntelligence branches (3 branches, 1 commit each)
2. **Second:** Pull EmailIntelligenceAider/main (1 branch, 1 commit - lowest risk)
3. **Third:** Pull EmailIntelligenceGem/taskmaster (1 branch, 10 commits)
4. **Fourth:** Pull EmailIntelligence (3 branches, including critical 59-commit pull)
5. **Fifth:** Pull EmailIntelligenceQwen (3 branches)

**Time estimate:** 5-10 minutes for all operations

---

*Generated: 2025-11-10*
