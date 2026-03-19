# Shell Script Organization

This directory contains all shell scripts for the EmailIntelligence project, organized by functional domain.

## Folder Structure

| Directory | Category | Description |
| :--- | :--- | :--- |
| **`setup/`** | Installation | Environment setup, dependency installation, and clean installs. |
| **`git/`** | Repository | Git hooks, subtree integration, and merge drivers. |
| **`ops/`** | Operations | Deployment, backup, and application launching. |
| **`orchestration/`** | Orchestration | Branch synchronization, worktree management, and status tracking. |
| **`dev/`** | Development | Code formatting, automation setup, and validation tools. |

## Usage

Scripts should be executed from the project root whenever possible. Many scripts have been updated to support root-relative execution.

### Example
```bash
bash scripts/shell/ops/launch.sh
```

## Maintenance Note
When adding a new shell script, place it in the appropriate functional sub-directory instead of the project root or the generic `scripts/` folder.
