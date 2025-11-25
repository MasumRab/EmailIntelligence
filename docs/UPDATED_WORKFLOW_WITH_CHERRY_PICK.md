# Updated Branch Alignment Workflow with Cherry-Pick Process

## Overview
This document describes the updated workflow for branch alignment that includes cherry-picking essential scripts at the start of each alignment task to ensure consistent environments and tools across all branches during the alignment process.

## Updated Workflow Phases

### Phase 1: Script Distribution & Cherry-Picking
Before any alignment work begins on a branch, essential scripts need to be made available on that branch:

1. **Identify Critical Scripts**
   - `scripts/monitor_orchestration_changes.sh` - Orchestration integrity checker
   - `scripts/branch_analysis_check.sh` - Branch analysis and verification tool
   - Any other utility scripts that aid in alignment safety

2. **Cherry-Pick Process for Each Target Branch**:
   - **Step 1**: Create a temporary alignment-tools branch from the target feature branch
   - **Step 2**: Cherry-pick the necessary script commits from the scientific/main branch 
   - **Step 3**: Run verification to ensure scripts work on the target branch
   - **Step 4**: Merge the temporary branch back to the feature branch
   - **Step 5**: Verify that cherry-picked scripts don't conflict with branch-specific functionality

3. **Branch-Specific Verification**:
   - Confirm all cherry-picked scripts execute properly on the target branch
   - Test that orchestration monitoring works with the target branch's code structure
   - Verify branch analysis tools work with the target branch's file structure

### Phase 2: Pre-Alignment Safety Checks (Updated)
With scripts now available on the target branch, run comprehensive safety checks:

1. **Run Orchestration Monitoring Script**
   ```bash
   bash scripts/monitor_orchestration_changes.sh
   ```

2. **Run Branch Analysis Script** 
   ```bash
   bash scripts/branch_analysis_check.sh
   ```

3. **Migration Status Verification on Target Branch**
   - Check for incomplete backend→src migrations on the target branch
   - Verify all import statements match the current directory structure
   - Identify any branch-specific structural inconsistencies

4. **Directory Cleanup Verification on Target Branch**
   - Remove any outdated backlog/temp directories specific to this branch
   - Clean up any duplicate documentation files in incorrect locations
   - Verify proper documentation structure for this branch

### Phase 3: Core Alignment Execution
After scripts are available and safety checks pass, execute the core alignment tasks:

1. **Execute Tasks 74-83** with confidence that monitoring tools are available
2. **Run verification scripts** after each major alignment step
3. **Monitor orchestration integrity** throughout the process

### Phase 4: Post-Alignment Verification
1. **Run final orchestration verification** with updated scripts
2. **Confirm cherry-picked scripts still work** after alignment
3. **Clean up temporary branches** created during cherry-pick process

## Implementation Steps

### For Each Feature Branch to be Aligned:

#### Step 1: Script Availability Check
```bash
# Check if critical scripts exist on the feature branch
if [ ! -f "scripts/monitor_orchestration_changes.sh" ]; then
    echo "Critical scripts not found on feature branch, initiating cherry-pick process"
    # Go to Step 2
else
    echo "Scripts already available on feature branch"
    # Go to Phase 2: Pre-Alignment Safety Checks
fi
```

#### Step 2: Cherry-Pick Script Commits
```bash
# Get the current feature branch name
FEATURE_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Create temporary branch for cherry-picking
git checkout -b temp-align-scripts-$FEATURE_BRANCH

# Cherry-pick the latest script commits from scientific branch
# (assuming the scripts were committed in a recent commit)
git cherry-pick <commit-hash-containing-scripts>

# If cherry-pick fails due to conflicts:
if [ $? -ne 0 ]; then
    echo "Cherry-pick conflicts detected, manual resolution required"
    # Resolve conflicts manually, ensuring scripts are properly integrated
    # without breaking branch-specific functionality
    git add .
    git commit -m "Resolve conflicts: Integrate alignment monitoring scripts"
fi

# Verify scripts work on this branch
bash scripts/monitor_orchestration_changes.sh
if [ $? -eq 0 ]; then
    echo "Scripts verified on $FEATURE_BRANCH, proceeding with merge"
    git checkout $FEATURE_BRANCH
    git merge temp-align-scripts-$FEATURE_BRANCH
    git branch -D temp-align-scripts-$FEATURE_BRANCH
else
    echo "Script verification failed on $FEATURE_BRANCH, aborting alignment"
    git checkout $FEATURE_BRANCH
    git branch -D temp-align-scripts-$FEATURE_BRANCH
    exit 1
fi
```

#### Step 3: Execute Pre-Alignment Safety Checks
Run the safety verification procedures as outlined in Phase 2.

#### Step 4: Execute Core Alignment Tasks (74-83)
With scripts available and safety checks passed, proceed with the core alignment framework.

## Benefits of This Approach

1. **Consistent Tooling**: All branches have the same monitoring and analysis tools available
2. **Reduced Risk**: Branches being aligned have proper verification tools to catch issues
3. **Standardized Process**: Cherry-picking ensures the same tools are available across all branches
4. **Safer Operations**: Each branch has the tools to verify its own integrity during alignment
5. **Traceability**: Clear record of when scripts were added to each branch

## Cherry-Pick Commit Tracking

For record keeping, maintain a log of which branches received which script updates:

```
Cherry-Pick Log:
- Branch: feature/X, Scripts added: monitor_orchestration_changes.sh, commit: abc123, date: 2025-11-25
- Branch: feature/Y, Scripts added: monitor_orchestration_changes.sh, branch_analysis_check.sh, commit: def456, date: 2025-11-25
```

This ensures that all branches have access to the same safety and verification tools during the alignment process, reducing the risk of destructive operations and allowing for consistent monitoring of critical orchestration functionality across the entire alignment process.