# Quickstart: Guided Developer Workflows

## Overview
The `dev.py` CLI provides interactive guidance for common development tasks and advanced conflict resolution.

## Installation
1.  Ensure you have the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  (Optional) Install guide-specific dependencies:
    ```bash
    pip install -r src/cli/guides/requirements.txt
    ```

## Usage

### 1. General Development
Unsure where to start or which branch to use?
```bash
python dev.py guide-dev
```
*   **What it does**: Asks about your intent, checks your branch, and warns if you are about to edit shared configuration files in the wrong place.

### 2. PR Resolution
Need to merge a complex feature or orchestration change?
```bash
python dev.py guide-pr
```
*   **What it does**: Routes you to the correct script (`manage_orchestration_changes.sh`) or the Advanced Resolution Engine based on the PR type.

### 3. Advanced Analysis (Scientific Engine)
Run deep conflict analysis using the integrated AI engine:
```bash
python dev.py analyze --pr 123
```

## Troubleshooting
*   **"Module not found"**: Ensure you are in the repo root and `src` is in your PYTHONPATH (dev.py handles this automatically).
*   **"Worktree error"**: Ensure you have a clean working directory before running analysis commands that use ephemeral worktrees.
