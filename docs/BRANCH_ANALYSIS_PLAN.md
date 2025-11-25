# Branch Analysis and Migration Status Verification Plan

## Overview
Before proceeding with the core alignment tasks (74-83), this plan outlines the critical analysis and verification steps needed to ensure safe execution. This addresses the issues identified in the assessment regarding:

- Risk of destructive merges due to incomplete migrations
- Need to verify launch code functionality across branches
- Requirement to prioritize orchestration-tools branch alignment
- Need to identify and clean outdated directories

## Priority 1: Orchestration Tools Branch Verification

### 1.1 Verify Current Orchestration Branch Status
- Check current state of `orchestration-tools`, `orchestration-tools-changes`, `orchestration-tools-consolidated` branches
- Identify which branch contains the most advanced launch code functionality
- Verify functionality of launch.py and related orchestration tools
- Document any missing configurations or agent files

### 1.2 Launch Code Functionality Verification
- Test launch.py functionality on orchestration-tools branch
- Verify all command patterns and environment setup work correctly
- Confirm agent integration and context control functionality
- Document current state and any issues found

## Priority 2: Migration Status Verification

### 2.1 Backend → src/ Migration Analysis
- For each branch to be aligned, verify if backend modules were properly migrated to src/backend/
- Check for incomplete migrations where files were moved but import statements weren't updated
- Identify branches where imports still reference `from backend...` instead of `from src.backend...`
- Identify configuration files that may still reference old paths

### 2.2 Directory Structure Verification
- Check for temporary/backup directories that need cleanup
- Identify duplicate documentation in incorrect locations
- Verify proper placement of orchestrator tools, launch scripts, and agents modules
- Clean up outdated backlog directories

## Priority 3: Branch Similarity Analysis

### 3.1 Identify Branches with Similar Names but Divergent Content
- Use git commands to compare branches with similar naming patterns
- Flag branches where content doesn't match branch naming intent
- Identify potential incorrect merges that led to content divergence
- Document findings for alignment prioritization

## Phase 1: Pre-Alignment Verification Tasks

### Task 100: Orchestration Tools Branch Assessment
**Objective**: Identify the most advanced orchestration-tools branch and verify functionality
- **Steps**:
  1. List all orchestration-* branches: `git branch -a | grep -i orchestration`
  2. Check out each branch and run: `python launch.py --system-info`
  3. Document which branch has most advanced features
  4. Test basic functionality on the selected branch
  5. Flag for alignment first priority

### Task 101: Migration Status Assessment
**Objective**: Identify branches with incomplete backend → src/ migrations
- **Steps**:
  1. For each feature branch targeted for alignment:
  2. Check for import statements using old paths: `git grep -n \"from backend\" -- .`
  3. Check for configuration files referencing old paths
  4. Document branches with incomplete migrations
  5. Create remediation plan for each problematic branch

### Task 102: Directory Cleanup Verification
**Objective**: Identify and plan cleanup of outdated directories before alignment
- **Steps**:
  1. Check for temporary directories: `find . -name \"temp_*\" -o -name \"backlog_*\" -type d`
  2. Identify duplicate documentation in wrong locations: `find . -name \"*.md\" | grep -v \"/docs/\" | xargs grep -l \"Documentation\\|README\"`
  3. Document directories requiring cleanup
  4. Schedule cleanup before alignment begins

### Task 103: Branch Similarity Analysis
**Objective**: Identify branches with similar names but divergent content
- **Steps**:
  1. List all feature branches: `git branch -a | grep \"feature/\"`
  2. Compare changes between similarly named branches using `git diff`
  3. Flag branches with similar names but different content
  4. This indicates potential incorrect merges that need investigation

## Phase 2: Prioritized Alignment Execution

### Priority Tier 1: Orchestration Branches
1. Complete Task 100 (Orchestration branch assessment)
2. Align orchestration-tools with main/scientific as appropriate
3. Ensure launch code and orchestration tools remain functional

### Priority Tier 2: Migration-Critical Branches
1. Complete Task 101 (Migration status assessment)
2. Address any incomplete migrations
3. Verify import consistency across all branches

### Priority Tier 3: Cleanup Required Branches
1. Complete Task 102 (Directory cleanup)
2. Clean up identified directories and files
3. Verify branch stability after cleanup

### Priority Tier 4: Core Alignment Tasks (74-83)
1. After safety checks are complete, proceed with Tasks 74-83
2. Apply branch similarity analysis (Task 103) during alignment
3. Focus on safe alignment without introducing new issues

## Risk Mitigation Measures

### For Task 31 (Now Deferred):
- Task 31 remains deferred to prevent wrong-branch pushes
- Alternative verification methods for merge conflicts will be implemented
- Manual inspection of critical branches before alignment

### For Migration Issues:
- Complete migration verification before alignment begins
- Backup branches before attempting fixes
- Test functionality after any migration updates

### For Orchestration Functionality:
- Preserve advanced launch code functionality during alignment
- Ensure agent context control remains operational
- Verify all orchestration tools remain functional after each step

## Success Criteria

- [ ] Orchestration-tools branch identified and verified
- [ ] All incomplete migrations identified and addressed
- [ ] Outdated directories cleaned up
- [ ] Branch similarity analysis completed with potential issues flagged
- [ ] Task 31 remains deferred
- [ ] Core alignment tasks (74-83) can proceed safely with minimal risk

## Implementation Order
1. Execute Phase 1 tasks (100-103)
2. Address any issues found in Phase 1
3. Proceed with core alignment (74-83)
4. Defer Task 31 completely
5. Schedule cleanup tasks for later completion