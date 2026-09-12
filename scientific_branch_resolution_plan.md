# Scientific Branch Resolution Plan

## Problem Analysis
- **Current State**: Scientific branch has 1192 local commits, 85 remote commits
- **Issue**: Complex divergence from merge commits in remote branch
- **Risk**: High - contains extensive history and potential conflicts

## Solution Strategy

### Option 1: Skip Problematic Commits (RECOMMENDED)
```bash
# List problematic commits
git log --oneline origin/scientific ^scientific | head -5

# Skip problematic commits
git rebase --skip  # For each problematic commit

# OR: Single rebase command with skipping
for commit in $(git log --oneline origin/scientific ^scientific | awk '{print $1}'); do
    git rebase --onto origin/scientific ^$commit scientific
    if [ $? -eq 1 ]; then
        git rebase --skip
    fi
done
```

### Option 2: Manual Resolution (TIME-CONSUMING)
```bash
# Step 1: Checkout new branch from current position
git checkout -b scientific-merge-rescue

# Step 2: Cherry-pick only non-conflicting commits
git cherry-pick <first_good_commit>..<last_good_commit>

# Step 3: Manually resolve conflicts
# Use CONFLICT_RESOLUTION guide from plan
```

### Option 3: Preserve Local Work (SAFEST)
```bash
# Create backup
git checkout -b scientific-backup

# Reset to tracking remote
git fetch origin scientific
git reset --hard origin/scientific

# Locate and apply specific changes manually
```

## Recommended Action

### STEP 1: Backup Current Work
```bash
git checkout -b scientific-backup-preserve-local
git branch -f scientific-backup-preserve-local HEAD
```

### STEP 2: Sync with Remote
```bash
git fetch origin scientific
git checkout scientific
git reset --hard origin/scientific
```

### STEP 3: Apply Local Changes (Optional)
```bash
# Manually identify and apply key changes from backup
# Use CLI tool to review what's been lost
git diff --name-only scientific-backup-preserve-local
```

## Verification
```bash
# Verify clean state
python -m src.cli.main branch-health scientific --post-resolution
python -m src.cli.main verify-merge --base origin/scientific --target scientific
```

## Rollback Plan
```bash
# If any issues arise
git checkout scientific-backup-preserve-local
```
