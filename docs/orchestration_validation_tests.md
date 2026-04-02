# Orchestration Workflow Validation Tests

This document outlines a series of tests to validate the correct functioning of the orchestration workflow, Git hooks, and file synchronization mechanisms. These tests cover common scenarios and aim to confirm that the system behaves as described in `orchestration_summary.md`.

## General Best Practices for Testing

To avoid common pitfalls and ensure accurate test results:

*   **Understand the Current Git State:** Before starting any test, always use `git status`, `git branch`, and `git log --oneline` to understand your current branch, committed changes, and overall history.
*   **Clean Working Directory:** Aim to have a clean working directory (`git status` shows "nothing to commit, working tree clean") before beginning a new test scenario, unless the test explicitly requires uncommitted changes.
*   **Stash or Commit:** If you have uncommitted changes that are not part of the current test, either `git stash` them or commit them. For untracked files, use `git clean -fd` cautiously, or `git stash --include-untracked`.
*   **Verify Branch:** Always double-check you are on the correct branch before making changes or running commands.
*   **Read Output Carefully:** Pay close attention to the output of every Git command and hook execution. Error messages or unexpected output can provide crucial debugging information.

## Prerequisites

Before running these tests, ensure the following:

1.  **Git Repository:** You are in a Git repository with at least an `orchestration-tools` and a `main` branch.
2.  **Latest `orchestration-tools`:** The `orchestration-tools` branch contains the *latest committed versions* of all orchestration scripts and hooks (i.e., `scripts/install-hooks.sh`, `scripts/hooks/*`, `scripts/cleanup_orchestration.sh`).
3.  **Clean `orchestration-tools` Branch:** Your `orchestration-tools` branch should have a clean working directory (`git status` and `git diff` show nothing) and all recent changes pushed to the remote.
    ```bash
    git checkout orchestration-tools
    git status # Should be clean
    git push origin orchestration-tools # To ensure remote is updated
    ```
4.  **Updated `main` Branch (Initial Sync):** To ensure `main` has the latest non-hook orchestration files and a clean `.git/hooks/` state from `orchestration-tools`, perform an initial sync:
    a.  Ensure `main` is up to date with `origin/main`:
        ```bash
        git checkout main
        git pull
        ```
    b.  Explicitly update `main`'s `scripts/install-hooks.sh` to the latest version from `orchestration-tools` and then run it to ensure `main`'s `.git/hooks/` are in a clean state (empty or default).
        *   Checkout the `install-hooks.sh` from `orchestration-tools` into your current `main` branch:
            ```bash
            git checkout orchestration-tools -- scripts/install-hooks.sh
            ```
        *   Now run this newly checked-out `install-hooks.sh` (which *will* install hooks temporarily to main):
            ```bash
            bash scripts/install-hooks.sh --force
            ```
        *   Then immediately switch back to `main` (or any other non-orchestration branch) to trigger the `post-checkout` hook, which will *remove* the hooks installed in the previous step.
            ```bash
            git checkout main # This will trigger post-checkout
            ```
        *   Verify `.git/hooks/` is clean:
            ```bash
            ls -l .git/hooks/
            ```
    c.  Clean up any stashed changes on `main` (if applicable) and remove the checked out `install-hooks.sh`:
        ```bash
        git stash pop # If you stashed changes earlier
        git restore scripts/install-hooks.sh # To remove the temporarily checked out version
        ```
5.  **Understanding File Ownership:** You have a clear understanding of which files are orchestration-managed vs. project-specific (refer to `orchestration_summary.md`).

## Test Scenarios

---

### Test 1: Basic Branch Switch & Hook Removal (New Strategy)

**Goal:** Verify that `post-checkout` correctly synchronizes orchestration-managed files and *removes* Git hooks when switching to `main` (a non-orchestration branch).

**Diagram:**

```
[orchestration-tools] --(checkout)--> [main]
    |                           |
    |                           V
    |                     [post-checkout]
    |                      (removes hooks)
    V
[launch.py (synced), .git/hooks/ (empty)]
```

**Steps:**

1.  Ensure you are on a clean `orchestration-tools` branch.
    ```bash
    git checkout orchestration-tools
    git status # Should be clean
    ```
2.  Manually install hooks on `orchestration-tools` to ensure `.git/hooks/` is populated for this branch (this step only applies to the `orchestration-tools` branch):
    ```bash
    bash scripts/install-hooks.sh --force
    ls -l .git/hooks/ # Verify hooks are present
    ```
3.  Switch to the `main` branch:
    ```bash
    git checkout main
    ```
4.  **Verification:**
    *   Observe the output of the `post-checkout` hook. It should indicate that hooks are being removed.
    *   Verify that `launch.py` has been correctly synchronized from `orchestration-tools` (this requires `launch.py` to be updated in `orchestration-tools` and then synced).
        ```bash
        diff launch.py $(git rev-parse --show-toplevel)/launch.py
        # Expected: No difference (or minimal if main has local changes not affected by orchestration)
        ```
    *   Verify that the `.git/hooks/` directory on `main` is empty or contains only non-orchestration hooks (e.g., sample hooks).
        ```bash
        ls -l .git/hooks/
        # Expected: Output should show no orchestration-managed hooks like pre-commit, post-checkout, etc.
        ```

---

### Test 2: Modifying Orchestration-Managed File on Feature Branch (No Active Pre-Commit)

**Goal:** Verify that, as orchestration hooks are removed from feature branches, a commit to an orchestration-managed file on a non-`orchestration-tools` branch will *not* be blocked by a `pre-commit` hook.

**Diagram:**

```
[feature-branch] --(modify launch.py)--> [attempt commit]
    |
    V
[No pre-commit hook] --(ALLOW)--> [Commit Successful (no blocking)]
```

**Steps:**

1.  Ensure you are on a non-`orchestration-tools` branch (e.g., `main` or a feature branch) and that hooks have been removed from `.git/hooks/` (from Test 1 or initial sync).
    ```bash
    git checkout main # Example
    ls -l .git/hooks/ # Should be empty or clean
    ```
2.  Create and switch to a new feature branch from `main` (if not already on one):
    ```bash
    git checkout -b feature/test-orchestration-file-no-hook
    ```
3.  Make a small, identifiable change to an orchestration-managed file, e.g., `launch.py`:
    ```bash
    echo "# Test change for launch.py" >> launch.py
    ```
4.  Stage the change:
    ```bash
    git add launch.py
    ```
5.  **Attempt to commit the change:**
    ```bash
    git commit -m "Attempt to commit orchestration-managed file change without hooks"
    ```
6.  **Verification:**
    *   The commit should be **successful**.
    *   **IMPORTANT:** There should be *no* blocking message from a `pre-commit` hook related to orchestration files. This test explicitly confirms that the `pre-commit` hook is *not active* on feature branches, aligning with the "single point of control" strategy.
    *   Cleanup: `git reset --hard HEAD~1` to undo the commit.


---

### Test 3: Modifying Project-Specific File on Feature Branch (and no active pre-commit hook)

**Goal:** Verify that, with no active `pre-commit` hook, project-specific file changes can be committed without interference.

**Diagram:**

```
[feature-branch] --(modify src/main.py)--> [attempt commit]
    |
    V
[No pre-commit hook] --(ALLOW)--> [Commit Successful]
```

**Steps:**

1.  Ensure you are on a feature branch (e.g., `feature/test-orchestration-file-no-hook`) and that hooks have been removed from `.git/hooks/`.
    ```bash
    git checkout feature/test-orchestration-file-no-hook # Or your current feature branch
    ls -l .git/hooks/ # Should be empty or clean
    ```
2.  Make a small, identifiable change to a project-specific file, e.g., `src/main.py`:
    ```bash
    echo "# Project specific test change" >> src/main.py
    ```
3.  Stage the change:
    ```bash
    git add src/main.py
    ```
4.  **Attempt to commit the change:**
    ```bash
    git commit -m "Commit project-specific file change"
    ```
5.  **Verification:**
    *   The commit should be **successful**.
    *   No messages from `pre-commit` should appear.
    *   Cleanup: `git reset --hard HEAD~1` to undo the commit.

---

### Test 4: Updating Hooks in `orchestration-tools` and Manual Installation on `orchestration-tools`

**Goal:** Verify that changes made to hook source files on the `orchestration-tools` branch are correctly installed by manually running `install-hooks.sh` on that branch.

**Diagram:**

```
[orchestration-tools] --(modify scripts/hooks/pre-commit)--> [Commit]
    |
    V
[orchestration-tools] --(manually run install-hooks.sh)--> [local .git/hooks/ updated]
```

**Steps:**

1.  Ensure you are on a clean `orchestration-tools` branch.
    ```bash
    git checkout orchestration-tools
    git status # Should be clean
    ```
2.  Make a minor, identifiable change to a hook source file, e.g., `scripts/hooks/pre-commit`. Add a comment or a unique `echo` statement. For example:
    ```bash
    echo "# Orchestration hook test change - $(date)" >> scripts/hooks/pre-commit
    ```
3.  Stage and commit the change:
    ```bash
    git add scripts/hooks/pre-commit
    git commit -m "feat: Add identifiable test change to pre-commit hook"
    ```
4.  Manually run `install-hooks.sh` on the `orchestration-tools` branch.
    ```bash
    bash scripts/install-hooks.sh --force
    ```
5.  **Verification:**
    *   Observe the output of `install-hooks.sh`. It should indicate that it's installing/updating hooks.
    *   Check the content of the installed `pre-commit` hook in `.git/hooks/pre-commit` on the `orchestration-tools` branch.
    *   It should contain the identifiable change you made in step 2.
        ```bash
        grep "# Orchestration hook test change" .git/hooks/pre-commit
        # Expected: The line should be found
        ```

---

### Test 5: Simulating a Branch Switch that Triggers Hook Removal

**Goal:** Verify that if hooks are temporarily present on a non-`orchestration-tools` branch (e.g., after a manual `install-hooks.sh` run), they are correctly removed upon the *next* `git checkout` to another non-orchestration branch.

**Diagram:**

```
[main] --(manually run install-hooks.sh)--> [main/.git/hooks/ populated]
    |
    V
[main] --(checkout feature-branch)--> [post-checkout cleans hooks]
```

**Steps:**

1.  Ensure you are on the `main` branch.
    ```bash
    git checkout main
    ```
2.  **Temporarily populate hooks on `main`** by running `install-hooks.sh`. This simulates a user manually installing them on a non-orchestration branch.
    ```bash
    # Assuming scripts/install-hooks.sh is present and updated on main (or you checked it out from orchestration-tools)
    bash scripts/install-hooks.sh --force
    ls -l .git/hooks/ # Verify hooks are now present
    ```
3.  Now, switch to a *different* non-orchestration branch (e.g., `feature/temp-branch`). This will trigger `post-checkout` on `main` (cleaning it) and then again on `feature/temp-branch` (cleaning it if any local hooks).
    ```bash
    git checkout -b feature/temp-branch # Or any other non-orchestration branch
    ```
4.  **Verification:**
    *   Observe the output of the `post-checkout` hook during the switch. It should explicitly state that hooks are being removed (`Removing Git hooks from .git/hooks/ for non-orchestration-tools branch...`).
    *   Verify that the `.git/hooks/` directory on `feature/temp-branch` is now empty or contains only non-orchestration hooks.
        ```bash
        ls -l .git/hooks/
        # Expected: Output should show no orchestration-managed hooks like pre-commit, post-checkout, etc.
        ```
    *   Cleanup: Delete the temporary branch: `git checkout main && git branch -D feature/temp-branch`.

---

## Troubleshooting Common Git Issues During Testing

*   **`error: Your local changes to the following files would be overwritten by checkout`**
    *   **Cause:** You have uncommitted changes in your working directory that conflict with the branch you're trying to checkout.
    *   **Fix:**
        1.  **Commit:** If the changes are meant to be kept, `git add . && git commit -m "WIP: temporary changes"`
        2.  **Stash:** If the changes are temporary and you want to reapply them later, `git stash push` (for tracked files) or `git stash push --include-untracked` (for tracked and untracked files).
        3.  **Discard:** If the changes are unwanted, `git reset --hard HEAD` (to discard changes to tracked files) and `git clean -fd` (to remove untracked files and directories - use with caution!).

*   **`error: The following untracked working tree files would be overwritten by checkout`**
    *   **Cause:** Untracked files exist that would be clobbered by the checkout. These are files Git doesn't know about yet.
    *   **Fix:** `git stash push --include-untracked` to temporarily store them, or `git clean -f` to delete them (use with caution).

*   **`scripts/lib/common.sh: No such file or directory` / `command not found`**
    *   **Cause:** The script trying to be executed either doesn't exist at the specified path, or it's not executable. This often happens if `install-hooks.sh` or a hook script is outdated or not properly synced from `orchestration-tools`.
    *   **Fix:**
        1.  Ensure you are on the `orchestration-tools` branch and `git push origin orchestration-tools` to ensure remote is up-to-date.
        2.  On the target branch (`main` or feature branch), manually get the latest `install-hooks.sh`:
            ```bash
            git checkout orchestration-tools -- scripts/install-hooks.sh
            ```
        3.  Then run `bash scripts/install-hooks.sh --force`.
        4.  Verify executability: `chmod +x path/to/script_name` if needed.

*   **Hooks not executing / Unexpected hook behavior**
    *   **Cause:** The hooks in `.git/hooks/` might not be the correct version, might not be executable, or there's an issue with the script logic.
    *   **Fix:**
        1.  Verify script content: `cat .git/hooks/hook_name`.
        2.  Verify executability: `ls -l .git/hooks/hook_name` (should have `x` permission).
        3.  On `orchestration-tools`, ensure `bash scripts/install-hooks.sh --force` has been run after any changes to `scripts/hooks/*`.
        4.  On non-orchestration branches, remember that hooks are *not* active. If you temporarily need them, install manually and be aware they will be cleaned on next checkout. 

## Conclusion

Successfully passing these updated tests indicates that the orchestration workflow, including Git hook management and file synchronization, is functioning as intended, ensuring consistency and adhering to the "single point of control" strategy. If any test fails, it points to a specific area that requires further investigation and debugging.