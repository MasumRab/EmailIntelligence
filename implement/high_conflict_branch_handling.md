# High-Conflict Branch Handling Report

## Analysis of scientific-merge-pr vs main

### Safe Commits for Cherry-Pick
1. **af033351** - "fix: protect .taskmaster from deletion by hooks and sync scripts"
   - Changes: .gitignore, scripts/sync_setup_worktrees.sh
   - Assessment: SAFE - Only affects orchestration tools, no application code
   - Files affected: Orchestration-only files that comply with branch policy

2. **0d20f4c6** - "docs: add command pattern and orchestration workflow docs, clean up old session files"
   - Assessment: NEEDS REVIEW - Check if documentation is orchestration-specific
   - Could be safe if it only affects approved doc files

### Unsafe Commits (Violate Branch Policy)
1. **26b1c98a** - "Add orchestration setup files from orchestration-tools branch"
   - Assessment: UNSAFE - This commit moves orchestration files to wrong branch
   - According to policy: Orchestration files belong in orchestration-tools branch only
   - Would cause contamination if merged to main

2. **Merge commits** - Contain conflicts between branches
   - 05764804 - Merge commit with unresolved conflicts in documentation
   - These should not be cherry-picked directly

### Feature Extraction Strategy

#### Safe Features to Extract
1. The TaskMaster protection fix (af033351) - can be cherry-picked
2. Select documentation updates that don't conflict with branch policies

#### High-Risk Features to Isolate
1. Orchestration tools - should remain in orchestration-tools branch
2. Application code - should remain separate from orchestration infrastructure
3. Merge commits with conflicts - require manual resolution

### Implementation Plan
1. Create topic branch from main: `feature/taskmaster-protection`
2. Cherry-pick only the safe commit: af033351
3. Push to remote for review
4. For other changes, create separate feature branches based on content type
5. Avoid cherry-picking any orchestration setup that belongs in orchestration-tools

### Risk Mitigation
- Validate each cherry-pick against branch propagation policy
- Use selective file cherry-picking where needed
- Test functionality after each cherry-pick
- Maintain separation between application code and orchestration tools