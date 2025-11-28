# Task ID: 77

**Title:** Create a Utility for Safe Integration of Primary Branch Changes into Feature Branches

**Status:** pending

**Dependencies:** 75, 76

**Priority:** high

**Description:** (ALIGNMENT PROCESS TASK - NOT FEATURE DEVELOPMENT) Develop a Python-based command-line utility that fetches the latest changes from a specified primary branch (main, scientific, or orchestration-tools) and integrates them into a target feature branch, ensuring changes flow 'from primary TO feature branches' as a default.

**Details:**

CRITICAL CLARIFICATION: This is an ALIGNMENT PROCESS TASK that defines procedures and tools for the alignment workflow, NOT a feature development task requiring its own feature branch. This task contributes to the core alignment framework that will be applied to other feature branches during the alignment process. Do NOT create a separate feature branch for this task. This task's output feeds into the alignment process for other branches, not the other way around.

This utility will automate the process of keeping feature branches up-to-date. It should accept the feature branch name and its determined primary target (from Task 75). The utility will perform the following steps:
1.  Checkout the feature branch.
2.  Fetch latest from `origin`.
3.  Perform a `git rebase` from the primary target branch onto the feature branch to maintain a clean history. (Or `git merge --no-ff` if rebase is not preferred, but `rebase` is generally cleaner for feature branches).
4.  If conflicts arise, prompt the single developer for manual resolution and provide instructions.
5.  After successful integration (rebase/merge), run the error detection scripts from Task 76.
6.  If no errors are detected, push the updated feature branch (force push if rebase was used, with caution).

```python
import subprocess
from typing import List

# Assume run_error_detection from Task 76 is available
# from .error_detection import run_error_detection 

def integrate_primary_changes(feature_branch: str, primary_branch: str) -> bool:
    print(f"Integrating {primary_branch} into {feature_branch}...")
    
    # 1. Checkout feature branch
    subprocess.run(['git', 'checkout', feature_branch], check=True)
    
    # 2. Fetch latest
    subprocess.run(['git', 'fetch', 'origin'], check=True)
    
    # 3. Rebase onto primary branch
    try:
        subprocess.run(['git', 'rebase', f'origin/{primary_branch}'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Merge/Rebase conflicts detected. Resolve manually and then run 'git rebase --continue'.")
        print(f"Or abort with 'git rebase --abort'. Error: {e}")
        return False # Indicate manual intervention needed

    # 4. Run error detection (using Task 76's functionality)
    # Placeholder for actual error detection call
    changed_files = subprocess.run(['git', 'diff', '--name-only', f'origin/{primary_branch}...{feature_branch}'], capture_output=True, text=True).stdout.splitlines()
    errors = [] # run_error_detection(changed_files, f'origin/{primary_branch}', feature_branch)
    
    if errors:
        print(f"Errors detected after integration: {errors}")
        return False

    # 5. Push updated feature branch (force with lease recommended after rebase)
    try:
        subprocess.run(['git', 'push', '--force-with-lease', 'origin', feature_branch], check=True)
        print(f"Successfully integrated {primary_branch} into {feature_branch} and pushed.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to push {feature_branch}. Error: {e}")
        return False

# Example usage:
# integrate_primary_changes('my-feature-branch', 'main')
```

**Test Strategy:**

Create a test repository with a `main` branch and several feature branches. Perform various scenarios: successful rebase with no conflicts, rebase with minor conflicts that can be resolved automatically (if implemented), rebase with major conflicts requiring manual intervention (verify utility gracefully handles this), rebase followed by introduced merge artifacts, missing imports, etc. Verify that `git log` shows a clean history after successful rebases and pushes. Test with different primary branch targets (`scientific`, `orchestration-tools`).

## Subtasks

### 77.1. Develop Core Utility with Pre-Integration Safeguards and Branch Validation

**Status:** pending  
**Dependencies:** None  

Implement the foundational utility structure, including command-line argument parsing for branch identification. Focus on implementing robust checks to validate target and primary branches, preventing accidental merges to incorrect branches. Incorporate mechanisms to create a temporary backup or restore point for the feature branch before initiating any git operations to safeguard against data loss.

**Details:**

This subtask involves setting up the command-line interface using `argparse` for `feature_branch` and `primary_branch` inputs. Implement checks using `git branch --list` and `git rev-parse --abbrev-ref HEAD` to ensure the branches exist and the current branch is the feature branch. Before any git operations, create a temporary backup branch (e.g., `git checkout -b <feature-branch-backup>`) to allow for easy rollback. Implement branch state validation to ensure the feature branch is clean (no uncommitted changes) before proceeding with integration. Design an initial user interface/command pattern for invoking the utility.

### 77.2. Implement Advanced Integration Strategies and Conflict Management

**Status:** pending  
**Dependencies:** 77.1  

Develop the core `git rebase` or `git merge --no-ff` logic, prioritizing primary branch changes while preserving feature branch work. Implement sophisticated conflict detection to identify and flag potential destructive merge patterns, not just simple line conflicts. Provide clear, actionable guidance to the developer for manual conflict resolution, including interactive prompts. Integrate verification checks that leverage error detection from Task 76 to validate the integration's outcome.

**Details:**

Enhance the `subprocess.run(['git', 'rebase', ...])` logic to handle rebase operations. Implement logic to detect and provide guidance for various conflict scenarios based on `git status` output, beyond just reporting conflicts (e.g., 'fast-forward', 'manual resolution required for file X'). Integrate the `run_error_detection` function from Task 76 after a successful rebase/merge to validate the integrated code. Develop safety protocols to analyze the integration result (e.g., checking for unexpected file deletions) before allowing a push. Implement performance safeguards like using `git pull --ff-only` when possible.

### 77.3. Establish Robust Error Handling, Rollback, Audit Logging, and Documentation

**Status:** pending  
**Dependencies:** 77.2  

Design and implement comprehensive error handling for all integration steps, gracefully managing failures during fetch, rebase/merge, or push operations. Create reliable rollback procedures to revert the branch to its pre-integration state in case of unresolvable conflicts or post-integration errors. Implement a detailed audit logging system to record all integration activities, including branch states, outcomes, and any interventions. Finally, create a comprehensive document outlining the utility's usage, safety protocols, and best practices.

**Details:**

Implement `try-except` blocks for all `subprocess.run` calls to catch `CalledProcessError` and other exceptions, providing informative error messages. Utilize the backup branch created in Subtask 1 to implement a robust rollback mechanism using `git reset --hard` or `git branch -D` followed by `git checkout <backup-branch>`. Develop an audit logging component that records start/end times, branch names, primary branch, integration method, success/failure status, and any manual interventions. Create a `docs/safe_integration_process.md` document covering utility usage, conflict resolution workflows, error handling, rollback procedures, and the purpose of each safety measure.
