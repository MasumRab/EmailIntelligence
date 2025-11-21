# Agentic LLM Tool Contamination Analysis

**Date**: Nov 16, 2025  
**Status**: Documentation of root causes and patterns observed in agentic commits  
**Scope**: TaskMaster branch contamination and misplaced commits

## Executive Summary

Multiple commits made by agentic LLM tools (Amp and Claude Code via Task Master CLI) were placed on incorrect branches or deleted critical task files. Root cause analysis identifies systematic failures in branch context understanding and file ownership validation.

### Key Findings

- **Total contaminating commits identified**: 6+ major incidents
- **Branches affected**: taskmaster, orchestration-tools-changes, feature/taskmaster-protection, scientific branches
- **Root cause pattern**: Lack of semantic understanding of branch purpose vs. file ownership
- **Impact severity**: High - critical task data loss and branch policy violations

---

## Incident 1: Misplaced .taskmaster Protection Commit

### Commit Details
- **Commit Hash**: 9cd5a74c (Nov 13, 04:24:44)
- **Original Branch**: feature/taskmaster-protection (incorrect)
- **Should Be On**: orchestration-tools-changes
- **Duplicate Instances**: 
  - af033351 on scientific-merge-pr
  - 61276b27 (amended) on orchestration-tools-changes

### Changes Made
```
- scripts/sync_setup_worktrees.sh: Add comment protecting .taskmaster
- .gitignore: Add .taskmaster/ entry (LATER REMOVED AS PROBLEMATIC)
```

### Root Cause: Context Contamination Type 1 - Branch Purpose Misunderstanding

**Why it happened**:
1. **Agentic tool was on wrong branch context** - Created feature branch when should have routed to orchestration-tools-changes
2. **No semantic validation** - Tool didn't check if file changes (orchestration scripts) belonged to orchestration branch
3. **Feature branch bias** - Tool defaulted to creating new feature branches instead of routing to appropriate infrastructure branch
4. **Missing branch policy check** - No validation against BRANCH_PROPAGATION_POLICY before committing

**Prevention**:
- Require branch policy validation before creating commits on any branch
- Route orchestration-specific changes to orchestration-tools-changes automatically
- Implement pre-commit hooks that verify file ownership matches target branch

---

## Incident 2: Task Files Deletion - e1cd6333

### Commit Details
- **Commit Hash**: e1cd6333 (Nov 9, 23:49:31)
- **Branch**: taskmaster (correct)
- **Action**: DELETED 1404 lines from tasks.json + complexity reports

### Changes Made
```
- tasks/tasks.json: DELETED (1404 insertions removed)
- reports/task-complexity-report.json: DELETED
- state.json: MODIFIED
```

### Root Cause: Context Contamination Type 2 - Accidental Workspace Cleanup

**Why it happened**:
1. **Unintended deletion** - Tool attempted "synchronization" cleanup that removed task definitions
2. **No safety check** - No verification that tasks.json should be preserved
3. **Workspace confusion** - Tool may have confused .taskmaster worktree with temporary workspace
4. **No rollback validation** - Didn't verify that tasks could be recovered before deletion

**Pattern**: Similar to "Clean up non-taskmaster files from worktree" (0c32a3d7)

**Prevention**:
- Never auto-delete tasks.json without explicit user confirmation
- Add pre-deletion hooks that validate critical files are backed up
- Implement file whitelist for safety-critical files that should never be deleted
- Require multiple confirmations for bulk file deletions

---

## Incident 3: Nested .taskmaster Directory Creation

### Commit Details
- **Commit Hashes**: 5af0da32 ("Add .taskmaster as submodule"), d8ab50d4 (duplicate)
- **Branch**: taskmaster
- **Action**: Attempted to track .taskmaster as submodule/nested structure

### Root Cause: Context Contamination Type 3 - Misunderstanding Worktree Semantics

**Why it happened**:
1. **Tool didn't understand worktree isolation** - Created nested .taskmaster when worktree is already isolated
2. **Git submodule confusion** - Treated taskmaster directory as a dependency rather than a worktree
3. **Double-tracking attempt** - Tried to track .taskmaster content in both parent and child repos
4. **Structural misunderstanding** - Didn't grasp that .taskmaster is a separate git working directory

**Pattern**: Recurring attempts to reorganize taskmaster structure incorrectly:
- 5af0da32: Add .taskmaster as submodule
- 5d07a5e6: Remove .taskmaster from index
- 25ecb35c: Flatten structure - move .taskmaster contents to root
- b6fb75b4: Copy taskmaster-worktree files to root
- 8774fb87: Remove non-core taskmaster AI files

**Prevention**:
- Add git worktree detection to agentic tools
- Prevent modifications to worktree parent references
- Document worktree structure clearly in AGENTS.md/CLAUDE.md with warnings
- Add pre-commit validation that prevents attempting to track worktree files

---

## Incident 4: Mass Deletion on orchestration-tools - 2b17d13a

### Commit Details
- **Commit Hash**: 2b17d13a (Nov 7, 15:18:44)
- **Branch**: orchestration-tools (but should have been scoped differently)
- **Branches Affected**: Multiple remote branches reference this

### Changes Made
```
- DELETED: 22 files including task definitions and documentation
- config.json: DELETED
- tasks/tasks.json: DELETED (1232 lines)
- docs/: Multiple .md files DELETED
```

### Root Cause: Context Contamination Type 4 - Branch Scope Violation + Agentic Cleanup

**Why it happened**:
1. **Branch cleanup overreach** - Tool deleted taskmaster files from orchestration-tools branch
2. **No scope understanding** - Didn't understand taskmaster files should never be on orchestration-tools branch
3. **Aggressive pruning** - Performed broad deletions based on "cleanup orchestration-tools" instruction
4. **Missing validation** - No check that files to delete were actually orchestration-specific

**Pattern**: Misunderstanding of what "keep only orchestration essentials" means - deleted task management files that should never have been there in first place

**Prevention**:
- Define explicit whitelist of files safe to delete per branch
- Require manual review of bulk deletions
- Validate that files to delete are in fact duplicates/misplaced (not primary copies)
- Add audit trail for all file deletions

---

## Incident 5: Multiple Flatten/Restructure Attempts

### Commit Sequence
- 25ecb35c (Nov 7, 04:09): Flatten structure - move .taskmaster contents to root
- 8774fb87 (Nov 7): Remove non-core taskmaster AI files
- 0c32a3d7: Clean up non-taskmaster files from worktree
- b6fb75b4: Copy taskmaster-worktree files to root

### Root Cause: Context Contamination Type 5 - Unclear Architecture Understanding

**Why it happened**:
1. **Confusion about intended structure** - Tool didn't understand whether .taskmaster should be:
   - A git worktree (correct)
   - A nested directory with synced content (incorrect)
   - A root-level structure (incorrect)
2. **Iterative "corrections"** - Each commit attempted to fix previous commit's structural choice
3. **No architecture documentation** - Tools lacked clear reference for proper structure
4. **Lack of convergence** - Multiple commits showing tool "exploring" different approaches

**Pattern**: Repeated restructuring indicates tool didn't have clear architectural constraints

**Prevention**:
- Document architecture in AGENTS.md with explicit warnings about worktree semantics
- Add architecture validation in pre-commit hooks
- Prevent consecutive restructuring commits without human review
- Require explicit architectural decision documentation before structural changes

---

## Root Cause Categories

### Type 1: Branch Purpose Misunderstanding
- **Examples**: 9cd5a74c (taskmaster protection on feature branch)
- **Cause**: No semantic mapping between file changes and target branch
- **Fix**: Pre-commit branch policy validation

### Type 2: Accidental Workspace Cleanup
- **Examples**: e1cd6333 (task file deletion), 0c32a3d7 (worktree cleanup)
- **Cause**: Overly aggressive deletion without critical file protection
- **Fix**: Whitelist critical files, require confirmation for bulk deletions

### Type 3: Worktree Semantics Misunderstanding
- **Examples**: 5af0da32, 5d07a5e6, 25ecb35c (nested structure attempts)
- **Cause**: Tool treated worktree as normal git directories
- **Fix**: Explicit worktree documentation, architecture validation

### Type 4: Branch Scope Violation
- **Examples**: 2b17d13a (task files deleted from orchestration-tools)
- **Cause**: Unclear which files belong on which branch
- **Fix**: Explicit branch ownership rules, scope validation

### Type 5: Architecture Understanding Failure
- **Examples**: Multiple restructuring attempts (25ecb35c, 8774fb87, 0c32a3d7, b6fb75b4)
- **Cause**: Lack of clear architectural decision documentation
- **Fix**: Architecture guide with constraints and warnings

---

## Validation Framework

### Pre-Commit Checks Required

```bash
# 1. Branch Policy Validation
- Verify files being committed belong to target branch
- Check against BRANCH_PROPAGATION_POLICY
- Flag orchestration-specific changes attempting to go to non-orchestration branches

# 2. Critical File Protection
- Prevent deletion of tasks.json without explicit confirmation
- Protect .taskmaster directory from being tracked in parent repo
- Validate state.json modifications

# 3. Worktree Integrity Checks
- Detect when operating in .taskmaster worktree
- Prevent modifications to worktree parent references
- Ensure worktree files stay independent

# 4. Architecture Validation
- Validate directory structure matches documented architecture
- Prevent nested .taskmaster creations
- Ensure no flattening/restructuring without review

# 5. Bulk Operation Safeguards
- Require explicit confirmation for bulk file deletions
- Log all deletions with justification
- Implement rollback capability for destructive operations
```

---

## Recommendations for Agentic Tool Configuration

### 1. Update AGENTS.md with Critical Warnings

Add explicit section:
```markdown
## CRITICAL: Worktree Architecture

The .taskmaster directory is a git worktree, NOT a nested directory or submodule.

- NEVER attempt to track .taskmaster files in parent repository
- NEVER create nested .taskmaster structures
- NEVER flatten or reorganize taskmaster directory
- NEVER delete .taskmaster from index
- ALWAYS keep .taskmaster independent with own git tracking

Any modification to this architecture must have explicit user review.
```

### 2. Implement Pre-Commit Validation

- Add git hook that validates branch policy before commits
- Check file ownership against BRANCH_PROPAGATION_POLICY
- Require confirmation for any operations on task files
- Log all agentic operations for audit trail

### 3. Define File Ownership Rules

```
Branch: orchestration-tools-changes
OWNS: scripts/*, .gitignore (orchestration entries only), post-merge hooks
NEVER: task files, task configuration, report files

Branch: taskmaster
OWNS: tasks/*.json, state.json, config.json, docs/prd.txt, reports/
NEVER: orchestration scripts, application code

Branch: main
OWNS: Application code, documentation (non-orchestration)
NEVER: task files, orchestration scripts
```

### 4. Add Architecture Guards

- Prevent modifications to git worktree structure
- Block attempts to create nested .taskmaster directories
- Validate that .taskmaster stays in .gitignore of parent repo
- Ensure no duplicate tracking of taskmaster files

### 5. Enhanced Logging for Agentic Operations

- Log all branch changes by agentic tools
- Record file deletion operations with justification
- Capture architectural changes with reasoning
- Enable audit trail for review of agentic decisions

---

## Remediation Status

### Completed
- ✅ Moved commit 9cd5a74c to orchestration-tools-changes (now 61276b27)
- ✅ Amended to remove problematic .gitignore entry
- ✅ Taskmaster branch cleaned up with hard reset to origin/taskmaster
- ✅ Verified task files restored in current taskmaster state

### Pending
- ⏳ Review all branches for orphaned/misplaced task files
- ⏳ Update AGENTS.md with worktree architecture warnings
- ⏳ Implement pre-commit validation framework
- ⏳ Audit other nested .taskmaster instances (5af0da32, d8ab50d4)
- ⏳ Review and remediate mass deletions (2b17d13a)

---

## Conclusion

The contamination incidents reveal systematic gaps in agentic tool understanding of:
1. Repository architecture (worktree semantics)
2. Branch policies and file ownership
3. Critical file protection during cleanup operations
4. Architectural decision documentation

Resolution requires not just fixing individual commits, but implementing validation frameworks that prevent these patterns from recurring. The root cause is not malicious intent, but rather insufficient context provided to agentic tools about repository structure and constraints.
