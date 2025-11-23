# Git Repository Cleanup and Push Instructions

This guide provides step-by-step instructions to clean up and push changes in the identified git repositories with unpushed commits and local-only branches.

## Identified Repositories

The following repositories were found with issues:
- `/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligenceQwen.taskmaster`
- `/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligenceGem.taskmaster`
- `/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligenceAuto.taskmaster`
- `/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligenceAider.taskmaster`
- `/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligence.taskmaster`

## Step-by-Step Instructions

### Step 1: Check Current Status

First, check the current git status for each repository:

```bash
# For each repository, run:
cd /path/to/repository
git status
git log --oneline --branches --not --remotes  # Check unpushed commits
git branch --no-merged origin/main           # Check local-only branches
```

### Step 2: Stash Working Directory Changes

If there are unstaged changes, stash them before pulling:

```bash
# For each repository with changes:
cd /path/to/repository
git stash push -m "Auto-stash before cleanup"
```

### Step 3: Pull Latest Changes

Update the repository with the latest changes from remote:

```bash
# For each repository:
cd /path/to/repository
git pull --rebase
```

If there are merge conflicts during pull, resolve them manually:

```bash
# After resolving conflicts in files:
git add <resolved_files>
git rebase --continue
```

### Step 4: Restore Stashed Changes

If you stashed changes in Step 2, restore them:

```bash
# For each repository where you stashed:
cd /path/to/repository
git stash pop
```

If there are conflicts when popping the stash, resolve them:

```bash
# Resolve conflicts in files, then:
git add <resolved_files>
git commit -m "Resolve stash conflicts"
```

### Step 5: Stage and Commit Changes

If you have new changes after restoring stash, stage and commit them:

```bash
# For each repository with changes:
cd /path/to/repository
git add .
git commit -m "Cleanup and update changes"
```

### Step 6: Push Unpushed Commits

Push any local commits that haven't been pushed:

```bash
# For each repository:
cd /path/to/repository
git push
```

### Step 7: Push Local-Only Branches

Push branches that exist only locally:

```bash
# For each repository, check local branches:
cd /path/to/repository
LOCAL_BRANCHES=$(git branch --no-merged origin/main | sed 's/*//')

# Push each local branch:
for branch in $LOCAL_BRANCHES; do
    git push -u origin "$branch"
done
```

### Step 8: Verify Cleanup

Check that everything is clean:

```bash
# For each repository:
cd /path/to/repository
git status
git log --oneline --branches --not --remotes  # Should be empty
git branch -a  # Check all branches are pushed
```

## Automated Script

For convenience, you can use this automated script to process all repositories:

```bash
#!/bin/bash
set -e

REPOS=(
    "/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligenceQwen.taskmaster"
    "/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligenceGem.taskmaster"
    "/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligenceAuto.taskmaster"
    "/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligenceAider.taskmaster"
    "/home/masum/github/taskmaster-backups/20251109_232215/EmailIntelligence.taskmaster"
)

for repo in "${REPOS[@]}"; do
    echo "Processing $repo"
    cd "$repo"
    
    # Check for changes
    if [[ -n $(git status --porcelain) ]]; then
        echo "Stashing changes..."
        git stash push -m "Auto-stash before update"
        STASHED=true
    else
        STASHED=false
    fi
    
    # Pull latest changes
    echo "Pulling latest changes..."
    git pull --rebase || {
        echo "Pull failed, please resolve conflicts manually"
        continue
    }
    
    # Restore stashed changes
    if [[ "$STASHED" == "true" ]]; then
        echo "Restoring stashed changes..."
        git stash pop || {
            echo "Stash pop failed, please resolve conflicts manually"
            continue
        }
    fi
    
    # Commit any new changes
    if [[ -n $(git status --porcelain) ]]; then
        echo "Committing changes..."
        git add .
        git commit -m "Cleanup and update changes"
    fi
    
    # Push unpushed commits
    if [[ -n $(git log --oneline --branches --not --remotes) ]]; then
        echo "Pushing unpushed commits..."
        git push
    fi
    
    # Handle local-only branches
    LOCAL_BRANCHES=$(git branch --no-merged origin/main | sed 's/*//')
    for branch in $LOCAL_BRANCHES; do
        echo "Pushing local branch $branch..."
        git push -u origin "$branch"
    done
    
    echo "Done with $repo"
    echo "---"
done
```

## Important Notes

- Always backup your repositories before running automated scripts
- If conflicts occur, manual resolution may be required
- Some repositories may have complex branch structures that need careful handling
- The `EmailIntelligenceAuto/.taskmaster` repository was not accessible and may need separate handling
- Test the script on a single repository first before running on all

## Troubleshooting

### Merge Conflicts
If you encounter merge conflicts:
1. Edit the conflicting files to resolve conflicts
2. Stage the resolved files: `git add <file>`
3. Continue the rebase: `git rebase --continue`

### Stash Conflicts
If stash pop fails:
1. Resolve conflicts in files
2. Stage resolved files: `git add <file>`
3. Run: `git commit -m "Resolve stash conflicts"`

### Permission Issues
If you encounter permission errors:
1. Check repository permissions
2. Ensure you have push access to the remote repository
3. Verify SSH keys or credentials are configured correctly