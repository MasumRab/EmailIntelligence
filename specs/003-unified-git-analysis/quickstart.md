# Quickstart: Unified Git Analysis and Verification Tool

**Feature**: `003-unified-git-analysis`
**Date**: 2025-11-11

This guide provides instructions for installing and using the `git-verifier` tool.

## Installation

1.  **Prerequisites**: Ensure you have Python 3.11+ and Git 2.0+ installed.
2.  **Installation**: The tool will be installed as a package.
    ```bash
    pip install .
    ```
    *(This assumes a `pyproject.toml` or `setup.py` will be created for installation).*

## Common Workflow

Here is a typical workflow for using the tool to ensure a clean merge of a rebased branch.

### 1. On your feature branch, before merging

You've finished your work on `my-feature` and have rebased it onto `main`. Before creating a pull request, generate an "Intent Report".

```bash
# Generate the report for your current branch
git-verifier analyze --report --output-file my-feature-intent.json
```
This creates a `my-feature-intent.json` file that captures the synthesized intent of all your commits. You can attach this report to your pull request.

### 2. After your feature branch is merged into `main`

A reviewer or an automated CI process can now verify that the merge was successful and no changes were accidentally lost.

```bash
# Switch to the main branch
git checkout main
git pull

# Run the verification
git-verifier verify --report my-feature-intent.json --merged-branch main
```

**Example Success Output**:
```json
{
  "branch_name": "my-feature",
  "verified_at": "2025-11-11T10:00:00Z",
  "is_fully_consistent": true,
  "missing_changes": [],
  "unexpected_changes": []
}
```

**Example Failure Output**:
```json
{
  "branch_name": "my-feature",
  "verified_at": "2025-11-11T10:05:00Z",
  "is_fully_consistent": false,
  "missing_changes": [
    {
      "commit_hexsha": "bada55c0de...",
      "synthesized_narrative": "Refactored the user model to include a 'last_login' field."
    }
  ],
  "unexpected_changes": []
}
```

### Other Commands

#### Detecting Rebased Branches

To see which local branches have been rebased recently:

```bash
git-verifier detect-rebased
```

#### Analyzing a Single Commit

To quickly get a synthesized narrative for the very last commit:

```bash
git-verifier analyze HEAD~1..HEAD
```
