# Branch Rename Plan

## Overview
This document outlines the plan to rename branches that don't follow the standardized naming convention.

## Standardized Naming Conventions
- `feature/short-description` - New features and enhancements
- `bugfix/short-description` - Bug fixes and patches
- `hotfix/short-description` - Urgent production fixes
- `refactor/short-description` - Code refactoring and restructuring
- `docs/short-description` - Documentation updates

## Branches to Rename

### Local Branches
| Current Name | Proposed New Name | Reason |
|--------------|-------------------|--------|
| backup-branch | (to be deleted) | Old backup branch, no longer needed |
| branch-alignment | (to be deleted) | Old branch, no longer needed |
| docs-cleanup | docs/cleanup | Follow standard docs/ prefix |
| scientific-consolidated | (to be deleted) | Old branch, no longer needed |
| scientific-minimal-rebased | (to be deleted) | Old branch, no longer needed |

### Remote Branches (to be deleted)
| Branch Name | Reason |
|-------------|--------|
| origin/backup-branch | Old backup branch, no longer needed |
| origin/backup-scientific-before-rebase-50 | Old backup branch, no longer needed |
| origin/backup/20251027_120805_audit_branch | Old backup branch, no longer needed |
| origin/branch-alignment | Old branch, no longer needed |
| origin/coderabbitai/utg/f31e8bd | External tool branch, no longer needed |
| origin/docs-cleanup | docs/cleanup | Should follow standard docs/ prefix |
| origin/feat/modular-ai-platform | feature/modular-ai-platform | Use feature/ prefix instead of feat/ |
| origin/jules/audit-sqlite-branch | Old branch, no longer needed |
| origin/replit-agent | External tool branch, no longer needed |
| origin/scientific-consolidated | Old branch, no longer needed |
| origin/scientific-minimal-rebased | Old branch, no longer needed |

### Branches Already Following Standard (No Changes Needed)
| Branch Name |
|-------------|
| docs/comprehensive-documentation |
| docs/merge-docs-cleanup |
| docs/merge-docs-cleanup-to-comprehensive |
| feature/search-in-category |
| feature/syntax-error-fixes-from-stable |
| main |
| scientific |
| origin/bugfix/backend-fixes-and-test-suite-stabilization |
| origin/docs/clean-inheritance-base |
| origin/docs/comprehensive-documentation |
| origin/docs/merge-docs-cleanup |
| origin/docs/merge-docs-cleanup-to-comprehensive |
| origin/feature/backlog-ac-updates |
| origin/feature/code-quality-and-conflict-resolution |
| origin/feature/merge-clean |
| origin/feature/merge-setup-improvements |
| origin/feature/search-in-category |
| origin/feature/syntax-error-fixes-from-stable |
| origin/feature/work-in-progress-extensions |
| origin/fix-gitignore-version-files |
| origin/fix-launch-issues |
| origin/fix-launcher-merge-conflict |
| origin/fix-test-suite |
| origin/launch-setup-fixes |
| origin/main |
| origin/scientific |
| origin/shared-docs-only |
| origin/worktree-workflow-system |

## Action Plan

1. Delete obsolete local branches:
   - backup-branch
   - branch-alignment
   - scientific-consolidated
   - scientific-minimal-rebased

2. Rename local branch:
   - docs-cleanup → docs/cleanup

3. Delete obsolete remote branches:
   - git push origin --delete backup-branch
   - git push origin --delete backup-scientific-before-rebase-50
   - git push origin --delete backup/20251027_120805_audit_branch
   - git push origin --delete branch-alignment
   - git push origin --delete coderabbitai/utg/f31e8bd
   - git push origin --delete jules/audit-sqlite-branch
   - git push origin --delete replit-agent
   - git push origin --delete scientific-consolidated
   - git push origin --delete scientific-minimal-rebased

4. Rename remote branch:
   - git push origin --delete docs-cleanup
   - git push origin docs/cleanup

5. Rename remote branch with wrong prefix:
   - git push origin --delete feat/modular-ai-platform
   - git push origin feature/modular-ai-platform

## Commands to Execute

```bash
# Delete obsolete local branches
git branch -d backup-branch
git branch -d branch-alignment
git branch -d scientific-consolidated
git branch -d scientific-minimal-rebased

# Rename local branch
git branch -m docs-cleanup docs/cleanup

# Delete obsolete remote branches
git push origin --delete backup-branch
git push origin --delete backup-scientific-before-rebase-50
git push origin --delete backup/20251027_120805_audit_branch
git push origin --delete branch-alignment
git push origin --delete coderabbitai/utg/f31e8bd
git push origin --delete jules/audit-sqlite-branch
git push origin --delete replit-agent
git push origin --delete scientific-consolidated
git push origin --delete scientific-minimal-rebased

# Rename remote branch (delete old, push new)
git push origin --delete docs-cleanup
git push origin docs/cleanup

# Rename remote branch with wrong prefix
git push origin --delete feat/modular-ai-platform
git push origin feature/modular-ai-platform
```