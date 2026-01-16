# Complete Stash Resolution Procedure

## Overview

This document provides a complete procedure for resolving uncommitted work stored in Git stashes. The procedure ensures that each stash is applied to the correct branch from which it originated, with proper validation and error handling.

## Files Created

1. **`scripts/handle_stashes.sh`** - Main automation script for processing stashes
2. **`scripts/stash_analysis.sh`** - Analysis script to prioritize stash processing
3. **`scripts/stash_details.sh`** - Detailed information script for understanding stash contents
4. **`docs/stash_resolution_procedure.md`** - Comprehensive documentation

## Procedure Steps

### 1. Analyze Stashes
First, understand what stashes exist and their priority:

```bash
cd /home/masum/github/EmailIntelligence
./scripts/stash_analysis.sh
```

This shows:
- All stashes with their target branches
- Priority order for processing
- Important notes about critical branches

### 2. Examine Stash Details
Get detailed information about what changes each stash contains:

```bash
./scripts/stash_details.sh
```

This shows for each stash:
- Reference and message
- Target branch
- Files changed
- Summary of changes

### 3. Process Stashes Systematically
Run the main automation script:

```bash
./scripts/handle_stashes.sh
```

The script will:
1. Show a summary of all stashes and their target branches
2. Ask for confirmation before proceeding
3. Process each stash in order:
   - Identify the correct branch
   - Switch to that branch
   - Apply the stash
   - Show what files were changed
4. Provide instructions for next steps

### 4. Review and Commit Changes
After applying stashes, review changes on each branch:

```bash
# Switch to a branch with applied changes
git checkout branch_name

# Review changes
git status
git diff

# Commit if changes are good
git add .
git commit -m "Apply stashed changes: description of changes"

# Or discard if changes are not needed
git checkout -- .
```

### 5. Clean Up Resolved Stashes
After confirming all stashes have been properly handled:

```bash
# Check current stash status
git stash list

# Drop specific resolved stashes
git stash drop stash@{index}

# Or clear all stashes if all have been processed
git stash clear
```

## Priority Order for Processing

Based on the analysis, stashes should be processed in this order:

1. **orchestration-tools** (6 stashes, critical branch, 61 commits behind remote)
2. **scientific** (3 stashes, 2 commits ahead of remote)
3. **002-validate-orchestration-tools** (3 stashes, orchestration related)
4. **feature/backend-to-src-migration** (2 stashes, migration work)
5. **Other branches** in order of appearance

## Important Considerations

### Before Processing
1. Ensure you're in the repository root directory
2. Make sure you have a clean working directory (no uncommitted changes)
3. Consider pulling latest changes on branches before applying stashes to avoid conflicts

### During Processing
1. The script will prompt you if a branch doesn't exist
2. You can choose to create the branch or select a similar existing branch
3. Pay attention to any merge conflicts that may arise

### After Processing
1. Review all changes carefully before committing
2. Test functionality if the stashed changes affect code
3. Update documentation if needed
4. Clean up resolved stashes to avoid confusion

## Common Issues and Solutions

### Branch Doesn't Exist
- Let the script create the branch
- Or select a similar existing branch
- Or manually create the branch before running the script

### Merge Conflicts
- Resolve conflicts manually
- Decide whether to keep stash changes, existing changes, or merge them
- Commit the resolved changes

### Stash Already Applied
- The script will show if no changes result from applying a stash
- You can safely drop these stashes

### Script Errors
- Ensure you're in the repository root
- Check that Git is working properly
- Run scripts with appropriate permissions

## Best Practices

1. **Take your time** - Don't rush through the process
2. **Backup important work** before starting
3. **Document your actions** as you process each stash
4. **Test functionality** after applying code changes
5. **Update documentation** when applying documentation changes
6. **Keep a clean workspace** between processing different stashes
7. **Communicate with team** if working in a shared repository

## Expected Outcomes

After completing this procedure:

1. All stashed work will be either:
   - Applied to the correct branch and ready for commit
   - Discarded if no longer needed
2. No important work will be lost
3. The stash list will be clean
4. Each branch will contain its appropriate changes
5. The repository will be in a more organized state

## Next Steps

1. Run `./scripts/stash_analysis.sh` to understand the priority order
2. Run `./scripts/stash_details.sh` to examine what changes each stash contains
3. Run `./scripts/handle_stashes.sh` to process the stashes systematically
4. Review and commit changes on each affected branch
5. Clean up resolved stashes
6. Update any documentation as needed

This procedure should resolve all 17 stashes in the repository and ensure that each piece of work is in the correct place for proper version control management.