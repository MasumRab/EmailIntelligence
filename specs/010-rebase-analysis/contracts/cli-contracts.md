# CLI Contracts for Rebase Analysis and Intent Verification

This document outlines the command-line interface (CLI) contracts for the Rebase Analysis and Intent Verification tool.

## Commands

### `analyze <branch_name>`
- **Description**: Analyzes the commit history of a specified rebased branch to reconstruct a chronological story of changes and identify original intentions.
- **Arguments**:
    - `<branch_name>` (required): The name of the rebased branch to analyze.
- **Output**: A clear, chronological story of the commit history with identified intentions.

### `verify <merged_branch_name>`
- **Description**: Verifies that the actual changes made in a rebased branch, once merged, reflect the original intentions identified during analysis.
- **Arguments**:
    - `<merged_branch_name>` (required): The name of the branch where the rebased branch was merged.
- **Output**: A report confirming alignment or highlighting discrepancies between merged changes and original intentions.

### `identify-rebased-branches`
- **Description**: Identifies branches that have recently undergone a rebase operation and are candidates for analysis.
- **Arguments**: None
- **Output**: A list of branches identified as having undergone rebase operations.

### `install`
- **Description**: Installs and sets up the rebase analysis and intent verification tools on the current development branch.
- **Arguments**: None
- **Output**: Confirmation of successful installation and setup.

### `ci-check <branch_name>`
- **Description**: Integrates with CI/CD pipelines to automate rebase analysis on relevant branches.
- **Arguments**:
    - `<branch_name>` (required): The name of the branch to perform CI checks on.
- **Output**: Results of the CI rebase analysis.