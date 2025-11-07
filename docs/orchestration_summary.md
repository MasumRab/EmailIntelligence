# Orchestration Workflow Summary

## 1. Purpose of `orchestration-tools` Branch

⚠️ **SEE ALSO**: [Orchestration Branch Scope Definition](orchestration_branch_scope.md) for a clear understanding of what belongs in this branch.

The `orchestration-tools` branch serves as the **central source of truth** for:
*   Development environment tooling.
*   Configuration management.
*   Scripts and Git hooks that ensure consistency across all project branches.

Its primary goal is to keep the core email intelligence codebase clean by separating orchestration concerns.

**IMPORTANT**: This branch will NOT be merged with other branches. It exists solely to provide environment tools and configurations that are synchronized to other branches.

## 2. File Ownership and Synchronization

### Files ONLY in `orchestration-tools` branch:
*   `scripts/` (all orchestration scripts and utilities, including `install-hooks.sh` and `cleanup_orchestration.sh`)
*   `scripts/lib/` (shared utility libraries)
*   `scripts/hooks/` (source files for Git hooks)

### Files synced TO other branches (orchestration-managed):
These files are considered "essentials" and are synchronized from `orchestration-tools` to other branches (e.g., `main`, `scientific`, feature branches).
*   `setup/` (launch scripts and environment setup)
*   `docs/orchestration-workflow.md` (this documentation)
*   `.flake8`, `.pylintrc` (Python linting configuration)
*   `.gitignore`, `.gitattributes` (Git configuration)
*   `launch.py` (and its associated configuration files like `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`)
*   `.env.example` (environment template)
*   `scripts/install-hooks.sh`, `scripts/manage_orchestration_changes.sh`, `scripts/reverse_sync_orchestration.sh`, `scripts/cleanup_orchestration.sh` (key orchestration scripts)

### Files that remain BRANCH-SPECIFIC (not orchestration-managed):
These files are *not* synced by the orchestration process and are managed independently within each branch.
*   `tsconfig.json`
*   `package.json`
*   `tailwind.config.ts`
*   `vite.config.ts`
*   `drizzle.config.ts`
*   `components.json`
*   All application source code

## 3. Git Hook Behavior

### `pre-commit` Hook
*   **Purpose:** Prevent accidental changes to orchestration-managed files on non-`orchestration-tools` branches.
*   **Behavior:**
    *   If on `orchestration-tools`: Allows all changes.
    *   If on other branches: Warns about changes to `setup/`, orchestration scripts, or shared configs, requiring a PR to `orchestration-tools`. Allows project-specific changes.

### `post-commit` Hook
*   **Purpose:** Trigger synchronization after orchestration changes.
*   **Behavior:**
    *   If on `orchestration-tools`: Offers to run worktree sync.
    *   If on other branches: No action.

### `post-merge` Hook
*   **Purpose:** Ensure environment consistency after merges.
*   **Behavior:**
    *   Syncs `setup/` directory.
    *   Syncs orchestration scripts (for reference).
    *   **Installs/updates Git hooks.**
    *   Cleans up temporary worktrees.

### `post-push` Hook
*   **Purpose:** Detect orchestration changes and create PRs.
*   **Behavior:**
    *   If `orchestration-tools` is pushed: Logs completion.
    *   If other branch is pushed and orchestration-managed files have changed: Creates an automatic draft PR to `orchestration-tools`.

### `post-checkout` Hook
*   **Purpose:** Sync essential files and install/update hooks when switching branches.
*   **Behavior:**
    *   **Crucially, it calls `scripts/install-hooks.sh` to install/update Git hooks.**
    *   Syncs `setup/` directory.
    *   Syncs `deployment/` directory.
    *   Syncs shared configuration files (e.g., `.flake8`, `.pylintrc`).
    *   Syncs orchestration documentation.
    *   **Does NOT sync orchestration tooling (e.g., `scripts/`) itself.**
    *   Skips all actions if switching *to* `orchestration-tools`.

## 4. `install-hooks.sh` Script

*   **Purpose:** Installs Git hooks from the canonical `orchestration-tools` branch to ensure consistent hook versions across all branches and worktrees.
*   **Mechanism (Remote-First Installation):**
    *   Fetches the latest from the remote `orchestration-tools` branch.
    *   Installs hooks directly from the *remote* `orchestration-tools` branch into the local `.git/hooks/` directory.
    *   Includes logic to compare local installed hooks with the remote version and only updates if necessary (unless `--force` is used).
*   **Benefit:** Prevents "hook version mismatch" issues by ensuring all environments use identical, up-to-date hook versions from the designated source of truth.

## 5. The "Stale Branches" Issue and Solution

*   **Problem:** Previously, hooks were copied from the *local* branch's `scripts/hooks/` directory. This led to inconsistencies when developers modified hooks locally, switched branches, or had unpushed commits, resulting in different hook versions across environments.
*   **Solution (`install-hooks.sh`'s Remote-First Approach):** By always installing hooks from the *remote* `orchestration-tools` branch, the system guarantees consistency and prevents local, unpushed, or branch-specific hook versions from causing issues.

## 6. Development Workflow Summary

1.  **Orchestration-tools is the source of truth** for shared configurations and tooling.
2.  **Main/other branches receive synced essentials** (like `launch.py`, `setup/`, shared configs, and *installed hooks*) but not the raw orchestration tooling scripts.
3.  **Hooks enforce a PR process** for changes to orchestration-managed files when made on non-`orchestration-tools` branches.
4.  **`post-checkout` ensures consistency** by syncing essentials and installing hooks from `orchestration-tools` upon branch switching.
5.  **`install-hooks.sh` is the mechanism** for reliably installing consistent hook versions from the remote `orchestration-tools` branch.
