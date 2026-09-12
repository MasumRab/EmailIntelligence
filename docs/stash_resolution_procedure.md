# Stash Resolution Procedure

## Overview

This document describes the procedure for resolving uncommitted work stored in Git stashes. The procedure ensures that each stash is applied to the correct branch from which it originated.

## The Problem

The repository currently has 17 stashes containing work from various branches:
- Multiple stashes on `orchestration-tools` branch
- Stashes on `scientific`, `002-validate-orchestration-tools`, `feature/backend-to-src-migration`, and other branches
- These stashes contain important work that needs to be either committed or discarded

## The Solution

The `handle_stashes.sh` script automates the process of:
1. Identifying the correct branch for each stash
2. Switching to that branch
3. Applying the stash
4. Allowing the user to decide whether to commit or discard the changes

## How It Works

### 1. Stash Analysis
The script analyzes each stash message to extract the branch name:
- For stashes created with `git stash` (WIP stashes), it looks for "WIP on branch_name:"
- For stashes created with `git stash save` (named stashes), it looks for "On branch_name:"

### 2. Branch Validation
The script checks if the identified branch exists:
- If it exists, it switches to that branch
- If it doesn't exist, it offers to create the branch or select a similar existing branch

### 3. Stash Application
The script applies each stash to its correct branch:
- Uses `git stash apply` to preserve the stash
- Falls back to `git stash pop` if apply fails
- Shows what files were changed after applying the stash

## Running the Procedure

### Prerequisites
1. Make sure you're in the repository root directory
2. Ensure you have a clean working directory (no uncommitted changes)

### Execution
```bash
cd /home/masum/github/EmailIntelligence
./scripts/handle_stashes.sh
```

### Process
1. The script will show a summary of all stashes and their target branches
2. You'll be prompted to confirm before proceeding
3. For each stash, the script will:
   - Identify the correct branch
   - Switch to that branch
   - Apply the stash
   - Show what files were changed
4. After all stashes are processed, you'll need to:
   - Review changes on each branch
   - Decide whether to commit or discard the changes
   - Clean up resolved stashes

## After Processing Stashes

### For Each Branch With Applied Changes
1. Switch to the branch:
   ```bash
   git checkout branch_name
   ```

2. Review the changes:
   ```bash
   git status
   git diff
   ```

3. Decide whether to commit or discard:
   - To commit:
     ```bash
     git add .
     git commit -m "Apply stashed changes: brief description"
     ```
   - To discard:
     ```bash
     git checkout -- .
     ```

### Clean Up Resolved Stashes
After confirming all stashes have been properly handled:
```bash
# Drop a specific stash
git stash drop stash@{index}

# Or drop all resolved stashes
git stash clear
```

## Common Scenarios

### Scenario 1: Branch No Longer Exists
If a stash was created from a branch that has been deleted:
- The script will offer to create a new branch with that name
- Or allow you to select a similar existing branch

### Scenario 2: Merge Conflicts
If applying a stash causes merge conflicts:
- The script will show the conflict
- You'll need to resolve conflicts manually
- Then decide whether to commit or discard

### Scenario 3: No Changes After Apply
If applying a stash results in no changes:
- The stash may have been applied previously
- Or the changes may already exist in the branch

## Best Practices

1. **Always review changes** before committing after applying a stash
2. **Keep a log** of which stashes you've processed
3. **Don't rush** - take time to understand each set of changes
4. **Backup important work** before starting the procedure
5. **Test functionality** after applying significant code changes
6. **Update documentation** if the stashed changes affect it

## Troubleshooting

### Script Fails
- Ensure you're in the repository root
- Check that you have a clean working directory
- Verify Git is working properly

### Branch Creation Issues
- Manually create the branch if the script can't
- Use an existing similar branch if the original is truly obsolete

### Stash Application Failures
- Try applying manually with `git stash apply stash@{index}`
- Check if the stash is corrupted with `git fsck`

## Example Workflow

```bash
# 1. Run the script
./scripts/handle_stashes.sh

# 2. Process each stash (script will guide you)

# 3. After processing, review changes on each branch
git checkout orchestration-tools
git status
git diff
git add .
git commit -m "Apply stashed changes for orchestration tools"

# 4. Clean up resolved stashes
git stash drop stash@{0}
# Repeat for each resolved stash
```

## Conclusion

This procedure ensures that no important work is lost from stashes and that each change is applied to the correct branch. Take your time with each stash to properly evaluate and handle the changes.