# TaskMaster Contamination Incidents - Quick Reference

## All Identified Contaminating Commits

| Hash | Date | Branch | Action | Root Cause Type | Severity |
|------|------|--------|--------|-----------------|----------|
| 9cd5a74c | Nov 13, 04:24 | feature/taskmaster-protection | Added .taskmaster protection code to wrong branch | Type 1: Branch Purpose Misunderstanding | MEDIUM |
| af033351 | Nov 13, 04:24 | scientific-merge-pr | Duplicate of 9cd5a74c on wrong branch | Type 1: Branch Purpose Misunderstanding | MEDIUM |
| e1cd6333 | Nov 9, 23:49 | taskmaster | Deleted tasks.json (1404 lines) | Type 2: Accidental Workspace Cleanup | **HIGH** |
| 5af0da32 | Nov 7 | taskmaster | Added .taskmaster as submodule (incorrect) | Type 3: Worktree Semantics Misunderstanding | MEDIUM |
| 5d07a5e6 | Nov 7, 02:57 | orchestration-tools* | Removed .taskmaster from index | Type 3: Worktree Semantics Misunderstanding | MEDIUM |
| 25ecb35c | Nov 7, 04:09 | taskmaster | Flattened .taskmaster structure (moved to root) | Type 3+5: Worktree + Architecture Misunderstanding | MEDIUM |
| 2b17d13a | Nov 7, 15:18 | orchestration-tools | Deleted 22 files including tasks.json from orchestration-tools | Type 4: Branch Scope Violation | **HIGH** |
| 8774fb87 | Nov 7 | taskmaster | Removed non-core taskmaster AI files | Type 2: Accidental Workspace Cleanup | MEDIUM |
| 0c32a3d7 | Nov 6 | taskmaster | Clean up non-taskmaster files from worktree | Type 2: Accidental Workspace Cleanup | MEDIUM |
| b6fb75b4 | Nov 10 | orchestration-tools-changes | Copy taskmaster-worktree files to root | Type 3: Worktree Semantics Misunderstanding | MEDIUM |
| d8ab50d4 | Nov 6 | taskmaster | Add .taskmaster as submodule (duplicate of 5af0da32) | Type 3: Worktree Semantics Misunderstanding | MEDIUM |
| 73679231 | Nov 6 | taskmaster | Add shared .taskmaster setup as submodule | Type 3: Worktree Semantics Misunderstanding | MEDIUM |

## Restructuring Commit Sequence (Shows Tool "Exploring")

This sequence shows the tool repeatedly trying to restructure taskmaster without understanding the correct architecture:

```
Nov 7, 04:09 - 25ecb35c: Flatten structure: move .taskmaster contents to root
Nov 7, later  - 8774fb87: Remove non-core taskmaster AI files  
Nov 6-7 ???   - 0c32a3d7: Clean up non-taskmaster files from worktree
Nov 10        - b6fb75b4: Copy taskmaster-worktree files to root
```

**Pattern**: Multiple iterations trying different structural approaches, indicating lack of clear architectural guidance.

## Root Cause Breakdown

### Type 1: Branch Purpose Misunderstanding (2 commits)
- 9cd5a74c, af033351
- **Pattern**: Commits routed to feature branches that should go to orchestration-tools-changes
- **Fix**: Pre-commit branch policy validation

### Type 2: Accidental Workspace Cleanup (3 commits)
- e1cd6333, 8774fb87, 0c32a3d7
- **Pattern**: Over-aggressive deletion without protecting critical files
- **Fix**: File whitelist, confirmation requirements

### Type 3: Worktree Semantics Misunderstanding (4 commits)
- 5af0da32, 5d07a5e6, 25ecb35c, b6fb75b4, d8ab50d4, 73679231
- **Pattern**: Treating worktree as normal git directory, attempting nesting/flattening
- **Fix**: Architecture documentation, worktree validation

### Type 4: Branch Scope Violation (1 commit)
- 2b17d13a
- **Pattern**: Deleting taskmaster files from orchestration-tools branch
- **Fix**: File ownership rules, scope validation

### Type 5: Architecture Understanding Failure (Multiple)
- Combined with Type 3 - shows in restructuring sequence
- **Fix**: Clear architecture guide with constraints

## Contamination Impact

### Critical (Task Data Loss)
- e1cd6333: Deleted tasks.json - recovered via earlier commits
- 2b17d13a: Mass deletion of 22 files including task definitions

### High (Branch Corruption)
- 5af0da32, 5d07a5e6, 25ecb35c, b6fb75b4: Nested .taskmaster structure attempts
- Restructuring sequence showing tool confusion

### Medium (Misplaced But Functional)
- 9cd5a74c: Correct changes, wrong branch (remediated)
- 8774fb87, 0c32a3d7: Cleanup actions with collateral damage

## Detection Patterns

### Pattern 1: Commits Appear on Multiple Branches
- Same commit hash on feature/taskmaster-protection and scientific-merge-pr (9cd5a74c, af033351)
- Indicates branching confusion

### Pattern 2: Restructuring Sequence Without Convergence
- Multiple consecutive commits trying different structures
- Indicates lack of architectural understanding

### Pattern 3: Bulk File Deletions Without Justification
- e1cd6333, 2b17d13a: Large file counts deleted
- No clear separation of task files from application files

### Pattern 4: Git Worktree as Normal Directory
- Attempts to treat .taskmaster as submodule, flatten it, copy contents
- Indicates tool doesn't understand worktree isolation

## Remediation Timeline

- **Nov 16, 10:00**: Identified 9cd5a74c misplacement, moved to orchestration-tools-changes
- **Nov 16, 15:00**: Cleaned taskmaster branch hard reset
- **Nov 16, 17:00**: Created comprehensive contamination analysis
- **Ongoing**: Audit other branches for additional contamination

## Lessons Learned

1. **Agentic tools need explicit architectural constraints** - Documenting "don't do X" after the fact is insufficient
2. **Pre-commit validation is critical** - No amount of post-hoc documentation prevents these issues
3. **Worktree semantics must be explicitly taught** - Tools default to treating them as normal directories
4. **File ownership rules need enforcement** - Suggesting file ownership isn't enough; validation hooks are needed
5. **Critical files need protection** - tasks.json shouldn't be deletable without explicit confirmation and rollback capability

## Prevention Checklist

- [ ] Update AGENTS.md with explicit worktree warnings
- [ ] Implement pre-commit branch policy validation hook
- [ ] Create file ownership whitelist per branch
- [ ] Add critical file protection (tasks.json, state.json)
- [ ] Audit all branches for additional contamination
- [ ] Review commits from Nov 6-13 for other issues
- [ ] Implement audit logging for agentic file operations
- [ ] Add architecture validation to prevent restructuring
