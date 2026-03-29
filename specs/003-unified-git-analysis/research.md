# Research: Unified Git Analysis and Verification

**Feature**: `003-unified-git-analysis`
**Date**: 2025-11-11

## Decision: Use GitPython for Git Repository Interaction

**Rationale**: This decision is carried over from the previous features. GitPython remains the best choice for its robust, object-oriented API and reliance on the core Git engine.

**Alternatives considered**: See `specs/001-history-analysis/research.md`.

## Research Area: Detecting Rebased Branches

**Requirement**: The tool must be able to identify branches that have been rebased (FR-002). The specification assumes this can be done by accessing the repository's reflog.

**Investigation**:
The `git reflog` command tracks the history of where heads of branches and other references have been. When a rebase occurs, the reflog will show the old and new HEADs of the branch. A typical rebase entry looks like `HEAD@{1}: rebase (finish): returning to refs/heads/my-feature-branch`.

**Method using GitPython**:
GitPython does not have a high-level API for directly parsing complex reflog semantics like "rebase finished". However, it provides access to the raw reflog entries for any given reference.

1.  **Accessing the Reflog**: The reflog for a specific head (like a branch) can be accessed via `repo.head.ref.log()`. Each entry in the log is a `RefLogEntry` object.

    ```python
    from git import Repo
    repo = Repo('.')
    reflog = repo.head.ref.log()
    for entry in reflog:
        print(entry.oldhexsha, entry.newhexsha, entry.message)
    ```

2.  **Identifying Rebase Operations**: The most reliable way to detect a rebase is to look for the characteristic `rebase:` prefix in the reflog entry message. We can iterate through the reflogs of all local branches and check their messages.

    ```python
    rebased_branches = set()
    for branch in repo.branches:
        try:
            for entry in branch.log():
                if 'rebase:' in entry.message:
                    rebased_branches.add(branch.name)
                    break # Move to the next branch
        except Exception:
            # Some refs may not have a log
            continue
    ```

**Decision**: The rebase detection mechanism will be implemented by iterating through the reflogs of all local branches and searching for entries containing the string `"rebase:"`. This is a reliable heuristic for identifying branches that have undergone a rebase operation. This approach avoids parsing complex `git` command output and contains the logic within the Python application.

**Risks**:
- This method relies on the reflog being available and not having been pruned. By default, reflog entries expire after 90 days. This is an acceptable constraint for the intended use case.
- It will only detect rebases on local branches that have a reflog. It cannot detect if a branch was rebased on a different machine and then force-pushed.
