# Orchestration Workflow Validation Tests

This document outlines a series of tests to validate the correct functioning of the orchestration workflow, Git hooks, and file synchronization mechanisms. These tests cover common scenarios and aim to confirm that the system behaves as described in `orchestration_summary.md`.

## Prerequisites

Before running these tests, ensure the following:

1.  You are in a Git repository with `orchestration-tools` and `main` branches.
2.  The `orchestration-tools` branch contains the latest version of all orchestration scripts and hooks.
3.  The `main` branch is up-to-date with `orchestration-tools` (i.e., `post-checkout` has run at least once after a switch to `main`).
4.  All Git hooks in `.git/hooks/` are executable.
5.  You have a clear understanding of which files are orchestration-managed vs. project-specific (refer to `orchestration_summary.md`).

## Test Scenarios

---

### Test 1: Basic Branch Switch & Hook Installation

**Goal:** Verify that `post-checkout` correctly synchronizes orchestration-managed files and installs/updates Git hooks when switching from `orchestration-tools` to `main`.

**Diagram:**

```
[orchestration-tools] --(checkout)--> [main]
    |                           |
    |                           V
    |                     [post-checkout]
    |                           |
    |                           V
    |                     Sync files & Install hooks
    V
[launch.py, .git/hooks/pre-commit] (from orchestration-tools)
```

**Steps:**

1.  Ensure you are on the `orchestration-tools` branch:
    ```bash
    git checkout orchestration-tools
    ```
2.  Switch to the `main` branch:
    ```bash
    git checkout main
    ```
3.  **Verification:**
    *   Check the content of `launch.py` on `main`. It should match the version in `orchestration-tools`.
        ```bash
        diff launch.py $(git rev-parse --show-toplevel)/launch.py
        # Expected: No difference, or only expected differences if main has local changes
        ```
    *   Check the content of a sample hook, e.g., `.git/hooks/pre-commit`. It should match the version in `orchestration-tools`.
        ```bash
        diff .git/hooks/pre-commit $(git rev-parse --show-toplevel)/scripts/hooks/pre-commit
        # Expected: No difference
        ```
    *   (Optional) Observe the output of the `post-checkout` hook during the branch switch for messages indicating file synchronization and hook installation.

---

### Test 2: Modifying Orchestration-Managed File on Feature Branch

**Goal:** Verify that the `pre-commit` hook prevents accidental commits of changes to orchestration-managed files on a non-`orchestration-tools` branch and provides appropriate instructions.

**Diagram:**

```
[feature-branch] --(modify launch.py)--> [attempt commit]
    |
    V
[pre-commit hook] --(BLOCK)--> [Warning: changes require PR to orchestration-tools]
```

**Steps:**

1.  Create and switch to a new feature branch from `main`:
    ```bash
    git checkout main
    git checkout -b feature/test-orchestration-file
    ```
2.  Make a small, identifiable change to an orchestration-managed file, e.g., `launch.py`:
    ```bash
    echo "# Test change" >> launch.py
    ```
3.  Stage the change:
    ```bash
    git add launch.py
    ```
4.  **Attempt to commit the change:**
    ```bash
    git commit -m "Attempt to commit orchestration-managed file change"
    ```
5.  **Verification:**
    *   The commit should be **blocked** by the `pre-commit` hook.
    *   You should see a warning message similar to: "WARNING: setup/ changes require PR to orchestration-tools" or similar text indicating that changes to orchestration-managed files should be done via a PR to `orchestration-tools`.
    *   The file `launch.py` should remain unstaged or the commit should not have been created.

---

### Test 3: Modifying Project-Specific File on Feature Branch

**Goal:** Verify that the `pre-commit` hook allows changes to project-specific files on a non-`orchestration-tools` branch without interference.

**Diagram:**

```
[feature-branch] --(modify src/main.py)--> [attempt commit]
    |
    V
[pre-commit hook] --(ALLOW)--> [Commit Successful]
```

**Steps:**

1.  Ensure you are on the `feature/test-orchestration-file` branch (or any non-`orchestration-tools` branch).
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
    *   No warnings or blocks from the `pre-commit` hook related to orchestration files should appear.

---

### Test 4: Updating Hooks on `orchestration-tools` and Syncing

**Goal:** Verify that changes made to hook source files on the `orchestration-tools` branch are correctly propagated and installed into other branches via `post-checkout`.

**Diagram:**

```
[orchestration-tools] --(modify scripts/hooks/pre-commit)--> [Commit & Push]
    |
    V
[remote orchestration-tools] --(checkout main)--> [main]
                                    |
                                    V
                              [post-checkout]
                                    |
                                    V
                              Install updated hooks
```

**Steps:**

1.  Ensure you are on the `orchestration-tools` branch:
    ```bash
    git checkout orchestration-tools
    ```
2.  Make a minor, identifiable change to a hook source file, e.g., `scripts/hooks/pre-commit`. Add a comment or a unique `echo` statement.
    ```bash
    echo "# Orchestration hook test change" >> scripts/hooks/pre-commit
    ```
3.  Stage and commit the change:
    ```bash
    git add scripts/hooks/pre-commit
    git commit -m "feat: Add test change to pre-commit hook"
    ```
4.  **Push the change to the remote `orchestration-tools` branch.** (This step is crucial for `install-hooks.sh`'s remote-first mechanism).
    ```bash
    git push origin orchestration-tools
    ```
5.  Switch to the `main` branch:
    ```bash
    git checkout main
    ```
6.  **Verification:**
    *   Check the content of the installed `pre-commit` hook in `.git/hooks/pre-commit` on the `main` branch.
    *   It should contain the identifiable change you made in step 2.
        ```bash
        grep "# Orchestration hook test change" .git/hooks/pre-commit
        # Expected: The line should be found
        ```
    *   This confirms that `post-checkout` (which calls `install-hooks.sh`) correctly pulled the updated hook from the remote `orchestration-tools`.

---

### Test 5: Accidental `install-hooks.sh` Call on Feature Branch

**Goal:** Verify that manually running `scripts/install-hooks.sh` on a non-`orchestration-tools` branch correctly updates hooks from the remote `orchestration-tools` without causing issues, demonstrating its robustness.

**Diagram:**

```
[feature-branch] --(manually run scripts/install-hooks.sh)--> [Install hooks from remote orchestration-tools]
```

**Steps:**

1.  Ensure you are on a non-`orchestration-tools` branch (e.g., `main` or `feature/test-orchestration-file`).
2.  (Optional) Make a temporary, local modification to `.git/hooks/pre-commit` to ensure it's different from the remote `orchestration-tools` version. This will confirm `install-hooks.sh` actually updates it.
    ```bash
    echo "# Temporary local change" >> .git/hooks/pre-commit
    ```
3.  **Manually run the `install-hooks.sh` script:**
    ```bash
    bash scripts/install-hooks.sh --verbose
    ```
4.  **Verification:**
    *   Observe the output of `install-hooks.sh`. It should indicate that it's installing/updating hooks from the remote `orchestration-tools` branch.
    *   Check the content of `.git/hooks/pre-commit`. It should now match the version from the remote `orchestration-tools` branch (i.e., the temporary local change from step 2 should be gone, and the change from Test 4 should be present).
        ```bash
        grep "# Orchestration hook test change" .git/hooks/pre-commit
        # Expected: The line should be found
        ```
        ```bash
        grep "# Temporary local change" .git/hooks/pre-commit
        # Expected: The line should NOT be found
        ```

---

## Conclusion

Successfully passing these tests indicates that the orchestration workflow, including Git hook management and file synchronization, is functioning as intended, ensuring consistency and preventing common issues related to version mismatches and accidental modifications. If any test fails, it points to a specific area that requires further investigation and debugging.
