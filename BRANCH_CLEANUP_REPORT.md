# Branch Cleanup Report

## Overview
This report identifies branches that can be cleaned up to maintain a tidy repository. Branch cleanup helps reduce clutter and improves navigation.

## Merged Branches (Ready for Deletion)
The following branches have been merged and can be safely deleted:

1. `fix-search-in-category` - Merged branch with legacy naming pattern

## Unmerged Branches with Legacy Naming
The following branches are unmerged but use legacy naming patterns that should be updated:

1. `feature-notmuch-integration` - Should be renamed to `feature/notmuch-integration`
2. `feature/search-in-category` - Should be renamed to `feature/search-in-category` (already correct format)
3. `feature/setup-environment-optimization` - Should be renamed to `feature/setup-environment-optimization` (already correct format)
4. `feature/setup-environment-optimization-from-stable` - Should be renamed to `feature/setup-environment-optimization-from-stable` (already correct format)
5. `feature/syntax-error-fixes-from-stable` - Should be renamed to `feature/syntax-error-fixes-from-stable` (already correct format)

Note: Some branches already follow the correct format with forward slashes.

## Old Branches (Inactive)
The following branches haven't been updated in a long time and should be reviewed for deletion:

1. `fix-search-in-category` - Last updated 5 weeks ago (merged, can delete)
2. `feature-notmuch-integration` - Last updated 4 days ago
3. `feature/search-in-category` - Last updated 15 hours ago (active)

## Recommendations

1. **Immediate Action**:
   - Delete `fix-search-in-category` as it's merged and no longer needed

2. **Short-term Actions**:
   - Rename branches with legacy naming patterns using the migration script:
     ```bash
     python scripts/branch_rename_migration.py --execute
     ```

3. **Long-term Maintenance**:
   - Regular cleanup of merged branches
   - Periodic review of old branches for relevance
   - Enforce naming standards through CI/CD validation

## Cleanup Commands

To delete merged branches:
```bash
# Delete specific merged branch
git branch -d fix-search-in-category

# Delete all merged branches (use with caution)
git branch --merged | grep -v "\*\|main\|scientific\|develop" | xargs -n 1 git branch -d
```

To rename branches with legacy patterns:
```bash
# Dry run first
python scripts/branch_rename_migration.py --dry-run

# Execute renaming
python scripts/branch_rename_migration.py --execute
```

## Validation

Use the branch validation script to ensure branches follow naming conventions:
```bash
# Validate current branch
python scripts/validate_branch_name.py

# Validate specific branch
python scripts/validate_branch_name.py feature/new-feature
```