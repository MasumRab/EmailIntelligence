# Task ID: 31

**Title:** Scan and Resolve Unresolved Merge Conflicts Across All Remote Branches

**Status:** deferred

**Dependencies:** None

**Priority:** medium

**Description:** Scan all remote branches to identify and resolve any lingering merge conflict markers (<<<<<<< HEAD, =======, >>>>>>>), ensuring a clean and functional codebase.

**Details:**

This task involves a systematic audit and cleanup of merge conflict artifacts across all remote branches. The goal is to eliminate any `<<<<<<<`, `=======`, and `>>>>>>>` markers that indicate unresolved conflicts, which can cause subtle bugs or compilation issues.

1.  **Preparation**: Ensure local repository is up-to-date by running `git fetch --all --prune`. This fetches all remote branches and removes any stale local tracking branches.
2.  **Branch Iteration**: Programmatically (e.g., using a shell script or Python script) or manually, iterate through every remote-tracking branch (e.g., `origin/main`, `origin/develop`, `origin/feature-X`). For each remote branch:
    a.  Checkout a new local branch based on the remote branch: `git checkout -b fix/resolve-conflicts-<branch_name> <remote>/<branch_name>`.
    b.  **Conflict Identification**: Use `git grep -l '<<<<<<<\|=======\|>>>>>>>'` across all tracked files to pinpoint files containing merge conflict markers. Focus on all text-based files, including but not limited to: Python files (`src/**/*.py`, `setup/**/*.py`, `scripts/**/*.py`, `tests/**/*.py`), JSON files (e.g., `data/processed/email_data.json`), Markdown documentation (`*.md` files like `AGENTS.md`, `docs/**/*.md`), configuration files (`.github/workflows/*.yml`).
    c.  **Resolution**: For each identified file, manually inspect and carefully resolve the merge conflict. This requires understanding the context of the conflict and making the correct decision to preserve desired code/data.
        *   **Python files**: Ensure correct syntax and logical flow after resolution.
        *   **JSON files**: Validate the JSON structure after resolution. If `data/processed/email_data.json` is affected, pay special attention to data integrity; consider leveraging insights or tooling related to `scripts/restore_json_data.sh` if data corruption is a risk.
        *   **Documentation files**: Ensure the intended content is preserved and formatting remains consistent.
    d.  **Commit**: Once conflicts in a branch are resolved, commit the changes with a clear message: `git commit -am 'FIX: Resolved merge conflicts on <branch_name>'`.
    e.  **Push and PR**: Push the `fix/resolve-conflicts-<branch_name>` branch to remote and, if applicable, open a Pull Request against the original remote branch, requesting review and merge.
3.  **Documentation**: Maintain a log of all branches where conflicts were found, the files affected, and a brief description of the resolution applied. This log should be stored in `docs/maintenance/merge_conflict_resolutions.md`.
4.  **Verification**: After each resolution and merge, perform a quick spot-check on the original branch to ensure the conflicts are indeed gone and no new issues were introduced.

### Tags:
- `work_type:maintenance`
- `work_type:conflict-resolution`
- `component:git-workflow`
- `scope:codebase-wide`
- `scope:branch-management`
- `purpose:code-consistency`
- `purpose:stability`

**Test Strategy:**

1.  **Pre-Resolution State Verification**: Before initiating fixes on a branch, document the specific lines and files containing conflict markers using `git grep` output. This serves as a baseline.
2.  **Post-Resolution Content Review**: After resolving conflicts in a file, perform a line-by-line review of the changes to ensure the correct code or data has been retained or integrated and no new issues (syntax errors, logical flaws) have been introduced. This is especially critical for files like `src/agents/core.py` or `data/processed/email_data.json`.
3.  **No New Conflict Markers**: After committing resolutions for a branch, run `git grep -l '<<<<<<<\|=======\|>>>>>>>'` again on the cleaned branch to confirm that all conflict markers have been successfully removed.
4.  **Local Functional Test**: For branches affecting application logic, perform basic functional tests (e.g., run relevant unit tests, execute common commands using `python -m src.main`) to ensure core functionalities are still working as expected.
5.  **Codebase-wide Search (Final)**: After all resolution branches have been merged back to their respective targets, perform a final `git grep -l '<<<<<<<\|=======\|>>>>>>>'` across the entire (locally updated) repository to confirm a clean state.

## Subtasks

### 31.1. Initialize Repository State and List Remote Branches

**Status:** pending  
**Dependencies:** None  

Perform an initial `git fetch --all --prune` to update the local repository with all remote branches and prune any stale local tracking branches. Subsequently, identify and list all remote-tracking branches (e.g., `origin/main`, `origin/develop`) that need to be scanned for merge conflicts.

**Details:**

Execute `git fetch --all --prune` to ensure the local repository has the most current view of all remote branches. After fetching, use a command like `git branch -r` to generate a comprehensive list of all remote-tracking branches. This list will be the primary input for subsequent subtasks, ensuring no remote branch is missed during the conflict scan.

### 31.2. Develop and Execute Conflict Detection Script

**Status:** pending  
**Dependencies:** 31.1  

Create and execute a script (e.g., shell or Python) that iterates through each remote-tracking branch identified in Subtask 1. For each remote branch, the script will check it out into a temporary local branch and then use `git grep` to identify files containing merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`). The script should log or output the branch names and specific files where conflicts are found.

**Details:**

The script should: 1. Read the list of remote branches from Subtask 1. 2. For each remote branch `<remote>/<branch_name>`, create and checkout a new local branch like `fix/resolve-conflicts-<branch_name>` from the remote branch. 3. Run `git grep -l '<<<<<<<\|=======\|>>>>>>>'` across all tracked files. 4. Record the `<branch_name>` and the list of affected files for later manual resolution. 5. The script should be robust to handle branches with no conflicts gracefully.

### 31.3. Manually Resolve Detected Merge Conflicts

**Status:** pending  
**Dependencies:** None  

For each branch and file identified by the script in Subtask 2 as containing merge conflict markers, manually inspect and carefully resolve the conflicts directly on the local `fix/resolve-conflicts-<branch_name>` branch. This involves understanding the context of the conflicting changes and making appropriate decisions for Python, JSON, and Markdown files, then committing the resolutions.

**Details:**

For each `fix/resolve-conflicts-<branch_name>` branch where conflicts were detected: 1. Checkout the branch. 2. Open each identified file. 3. Manually remove `<<<<<<<`, `=======`, `>>>>>>>` markers, integrating the correct code/data. 4. For Python files, ensure correct syntax and logic. 5. For JSON files, validate the structure post-resolution. 6. For Markdown, preserve intended content and formatting. 7. Once resolved for a branch, commit with a message like 'FIX: Resolved merge conflicts on <branch_name>'. All work must be done directly on the local `fix/resolve-conflicts-<branch_name>` branch.

### 31.4. Push Resolved Branches and Create Pull Requests

**Status:** pending  
**Dependencies:** None  

After successfully resolving conflicts and committing changes on each `fix/resolve-conflicts-<branch_name>` branch, push these branches to the remote repository. Subsequently, create a Pull Request (PR) for each resolved branch, targeting its original remote branch (e.g., `origin/main`).

**Details:**

For each `fix/resolve-conflicts-<branch_name>` branch where conflicts were resolved: 1. Push the branch to the remote repository using `git push origin fix/resolve-conflicts-<branch_name>`. 2. Navigate to the repository's web interface (e.g., GitHub, GitLab). 3. Create a Pull Request from `fix/resolve-conflicts-<branch_name>` to the original target branch (e.g., `main`, `develop`, `feature-X`). 4. Ensure the PR title and description clearly indicate that it's for resolving merge conflicts.

### 31.5. Document Resolutions and Verify Final Codebase Cleanliness

**Status:** pending  
**Dependencies:** 31.4  

Maintain a comprehensive log of all branches where conflicts were found, the files affected, and a brief description of the resolution applied, storing this information in `docs/maintenance/merge_conflict_resolutions.md`. After each Pull Request is merged into its target branch, perform a final verification to ensure all conflict markers are removed and no new issues were introduced.

**Details:**

1. Update `docs/maintenance/merge_conflict_resolutions.md` with entries detailing each resolved branch, affected files, and a concise summary of the resolution. 2. After all PRs from Subtask 4 are merged, perform a final `git fetch --all --prune`. 3. Re-run the conflict detection script (or manual `git grep`) from Subtask 2 on the original remote branches to confirm the complete absence of `<<<<<<<`, `=======`, and `>>>>>>>` markers. 4. Conduct quick spot-checks or run critical integration tests on the 'cleaned' branches to ensure no new issues arose.
