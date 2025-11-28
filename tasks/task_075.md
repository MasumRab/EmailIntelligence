# Task ID: 75

**Title:** Develop a Script to Identify and Categorize Feature Branches

**Status:** pending

**Dependencies:** None

**Priority:** high

**Description:** (ALIGNMENT PROCESS TASK - NOT FEATURE DEVELOPMENT) Create a Python script that identifies all active feature branches in the repository and categorizes them based on their intended primary integration target (main, scientific, or orchestration-tools) using Git history analysis and codebase similarity heuristics.

**Details:**

CRITICAL CLARIFICATION: This is an ALIGNMENT PROCESS TASK that defines procedures and tools for the alignment workflow, NOT a feature development task requiring its own feature branch. This task contributes to the core alignment framework that will be applied to other feature branches during the alignment process. Do NOT create a separate feature branch for this task. This task's output feeds into the alignment process for other branches, not the other way around.

This script will utilize `git` commands (e.g., `git branch --remote`, `git log`) to list all remote feature branches. For each feature branch, it will analyze its commit history and potentially its file changes to infer its primary target. A simple heuristic could involve checking common files or directories modified in the feature branch against known patterns for `main`, `scientific`, or `orchestration-tools` related development (e.g., `scientific/` folder for `scientific` branch, `orchestration/` for `orchestration-tools`). The script should output a structured list (e.g., JSON) of branches and their determined target.

```python
import subprocess
import json

def get_remote_feature_branches():
    # Example: List all remote branches excluding primary ones
    result = subprocess.run(['git', 'branch', '-r'], capture_output=True, text=True)
    branches = []
    for line in result.stdout.splitlines():
        branch_name = line.strip().replace('origin/', '')
        if not any(b in branch_name for b in ['main', 'scientific', 'orchestration-tools', 'HEAD -> main']):
            branches.append(branch_name)
    return branches

def categorize_branch(branch_name):
    # Heuristic: Check for common ancestor, or changed files
    # For simplicity, let's assume a basic keyword matching for now
    # A more advanced approach would involve git merge-base, git diff --name-only, etc.
    if 'scientific' in branch_name or any(f.startswith('scientific/') for f in get_changed_files(branch_name)):
        return 'scientific'
    elif 'orchestration' in branch_name or any(f.startswith('orchestration/') for f in get_changed_files(branch_name)):
        return 'orchestration-tools'
    else:
        return 'main'

def get_changed_files(branch_name):
    # dummy function for illustration, actual implementation would compare with main/base
    # e.g., git diff --name-only origin/main..origin/{branch_name}
    return [] # Placeholder

def main():
    feature_branches = get_remote_feature_branches()
    categorized_branches = []
    for branch in feature_branches:
        target = categorize_branch(branch)
        categorized_branches.append({'branch': branch, 'target': target})
    
    with open('categorized_branches.json', 'w') as f:
        json.dump(categorized_branches, f, indent=4)
    print('Branches categorized and saved to categorized_branches.json')

if __name__ == '__main__':
    main()
```

**Test Strategy:**

Run the script against a test repository with various feature branches (some clearly targeting 'main', others 'scientific' or 'orchestration-tools' through their names or file changes). Manually verify that the categorization output is accurate for at least 80% of the branches. Ensure the script handles branches with large shared history effectively. Verify the output JSON format.

## Subtasks

### 75.1. Implement logic to identify all active feature branches using git commands

**Status:** pending  
**Dependencies:** None  

Develop and implement Python code to execute Git commands (e.g., 'git branch -r') to list all remote branches. This subtask includes filtering out known primary branches (main, scientific, orchestration-tools) and other non-feature branches (e.g., release, hotfix branches based on established conventions) to accurately identify only active feature branches.

**Details:**

Utilize `subprocess` to run `git branch -r` and parse its output. Implement robust filtering logic based on common primary branch names and patterns. Consider potential edge cases like detached HEAD or atypical branch names.

### 75.2. Create branch analysis algorithm to determine optimal target branch (main, scientific, orchestration-tools) based on codebase similarity

**Status:** pending  
**Dependencies:** 75.1, 75.3  

Design and implement a core algorithm that orchestrates various analysis components (Git history, file change patterns, content similarity) to determine the most suitable primary integration target (main, scientific, or orchestration-tools) for each feature branch.

**Details:**

Define a weighted scoring mechanism or a decision tree approach to combine signals from history analysis, file path heuristics, and future content similarity. The algorithm should output a primary target and a confidence score.

### 75.3. Implement Git history analysis to identify shared history between branches

**Status:** pending  
**Dependencies:** 75.1  

Develop Python functions to analyze the Git history of feature branches against potential primary targets (main, scientific, orchestration-tools) to identify common ancestors and measure the depth of shared and divergent history.

**Details:**

Use `git merge-base <branch1> <branch2>` to find the common ancestor. Then, use `git log <common_ancestor>..<feature_branch>` and `git log <common_ancestor>..<target_branch>` to count divergent commits and analyze their characteristics.

### 75.4. Create categorization system to group branches by target and similarity

**Status:** pending  
**Dependencies:** 75.2  

Define and implement a structured output format (e.g., JSON) to represent the categorized feature branches. The system should group branches based on their determined primary integration target and further by a measure of their similarity or relatedness.

**Details:**

The output structure should include branch name, identified primary target, a confidence score, and potentially secondary target suggestions or other relevant metadata. Implement Python logic to serialize this data into a human-readable and machine-parseable format.

### 75.5. Implement similarity analysis between branches to identify potential conflicts or duplication

**Status:** pending  
**Dependencies:** 75.1, 75.3  

Develop functionality to compare the changes introduced in a feature branch against its potential target branches and other active feature branches to detect overlapping modifications, potential merge conflicts, or duplicated effort.

**Details:**

Utilize `git diff --name-only <branch1> <branch2>` to identify common files modified. Consider using `git diff --stat` or parsing full diffs to analyze the content overlap. This can help identify potential `main`, `scientific`, or `orchestration-tools` conflicts.

### 75.6. Develop logic to prioritize branches based on importance and complexity of divergence

**Status:** pending  
**Dependencies:** 75.3, 75.10  

Implement a system to assign a priority score to each feature branch. This score should reflect the branch's importance (e.g., activity, linked work items) and the complexity of its divergence from primary targets.

**Details:**

Define quantifiable metrics for importance (e.g., number of commits, last commit date, number of contributors) and complexity (e.g., lines changed, number of files, depth of divergent history). Implement a configurable scoring model to combine these metrics into a single priority score.

### 75.7. Create detailed branch assessment reports with recommendations for target branch

**Status:** pending  
**Dependencies:** 75.4, 75.5, 75.6, 75.9, 75.10  

Generate comprehensive reports for each feature branch that include its determined target, confidence level, rationale for categorization, identified conflicts, age, prioritization score, and clear recommendations for integration actions.

**Details:**

Design a template for the branch assessment report (e.g., Markdown or structured text). Populate this template with data gathered from previous subtasks. The report should be easily readable and provide actionable insights for developers.

### 75.8. Implement branch naming convention checks to identify improperly named branches

**Status:** pending  
**Dependencies:** 75.1  

Develop a module to validate feature branch names against predefined naming conventions (e.g., using regular expressions or specific prefixes). The module should report any non-compliant branch names.

**Details:**

Define a configurable set of regular expressions (e.g., `^(feature|bugfix|chore)\/[A-Z]+-\d+-.+$`) or specific patterns for acceptable branch names. Implement a function that takes a branch name and returns `True` if compliant, `False` otherwise, along with a reason for non-compliance.

### 75.9. Create branch age analysis to identify long-running feature branches

**Status:** pending  
**Dependencies:** 75.1  

Implement functionality to calculate the age of each feature branch from its creation date (first commit) and identify branches that have been active for an unusually long period, potentially indicating stalled development or integration challenges.

**Details:**

Use `git log --reverse --format=%ai <branch_name> | head -1` to find the first commit date. Calculate the duration from this date to the current date. Define a configurable threshold (e.g., 30, 60, 90 days) for flagging long-running branches.

### 75.10. Implement code change assessment to determine scope and risk of alignment

**Status:** pending  
**Dependencies:** 75.1, 75.3  

Analyze the size and nature of code changes within each feature branch to quantify the scope and potential risk associated with integrating those changes into a primary target branch.

**Details:**

Use `git diff --numstat <common_ancestor> <feature_branch>` to get lines added/deleted and files changed. Categorize changes by file type and directory (e.g., `src/scientific/`, `src/orchestration/`, `tests/`) to infer impact on different system components. Assign a risk score based on these metrics.

### 75.11. Develop branch dependency mapping to understand inter-branch relationships

**Status:** pending  
**Dependencies:** 75.1, 75.3  

Identify and map dependencies between feature branches, determining if one feature branch is directly based on, or has merged changes from, another feature branch. This helps understand complex development flows.

**Details:**

Utilize `git log --graph --decorate --all` to visualize the branch topology or programmatically use `git merge-base --is-ancestor <potential_parent_branch> <feature_branch>` to check for direct ancestry relationships between feature branches.

### 75.12. Create visualization tools to display branch relationships and suggested alignment paths

**Status:** pending  
**Dependencies:** 75.4, 75.11  

Develop functionality to generate visual representations of the identified branch relationships, suggested target integrations, and overall branch hierarchy, aiding in quick comprehension and decision-making.

**Details:**

Integrate with a Python graphing library (e.g., `NetworkX` to model relationships, `pyvis` or `graphviz` to render interactive/static graphs) or generate data for external visualization tools (e.g., Mermaid JS syntax). The visualization should highlight target branches and problematic areas.

### 75.13. Implement automated branch status monitoring for the alignment process

**Status:** pending  
**Dependencies:** 75.4  

Configure the categorization script to run periodically and implement a mechanism to monitor changes in branch status, new branch creations, deletions, and categorization updates. This allows for continuous tracking of the alignment process.

**Details:**

Develop a persistent storage mechanism (e.g., a simple database, JSON file) to store the last known state of branches and their categorization. Implement logic to compare the current run's output with the stored state and report any significant changes. Integrate with system scheduling tools like `cron` or CI/CD pipelines.

### 75.14. Establish branch categorization validation to confirm accuracy of target assignments

**Status:** pending  
**Dependencies:** 75.2, 75.4  

Develop a comprehensive validation framework, including unit and integration tests, to systematically confirm the accuracy of the script's branch categorization and target assignments against known ground truth.

**Details:**

Create a dedicated test Git repository with various feature branches whose correct target branches are predetermined. Implement Python test cases (e.g., using `pytest`) that execute the categorization script on this test repository and assert that the output matches the expected classifications.

### 75.15. Document the branch identification and categorization methodology for future reference

**Status:** pending  
**Dependencies:** 75.1, 75.2, 75.3, 75.4, 75.5, 75.6, 75.7, 75.8, 75.9, 75.10, 75.11, 75.12  

Create comprehensive documentation detailing the entire methodology, including how feature branches are identified, the algorithms and heuristics used for categorization, confidence scoring, prioritization, risk assessment, and interpretation of reports and visualizations.

**Details:**

Write clear, concise documentation (e.g., in Markdown or Sphinx) in a designated `docs/` folder. Include sections on script usage, configuration options, underlying Git commands, interpretation of output, and guidelines for manual override or refinement of categorization. Provide examples.
