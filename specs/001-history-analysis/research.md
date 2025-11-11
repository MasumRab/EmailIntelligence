# Research: History Analysis

**Feature**: `001-history-analysis`
**Date**: 2025-11-11

## Decision: Use GitPython for Git Repository Interaction

**Rationale**: GitPython is a mature, widely-used library in the Python ecosystem for interacting with Git repositories. It provides a robust, object-oriented API to access commits, branches, diffs, and other Git objects, which directly maps to the needs of this feature. Its direct dependency on the `git` command-line executable ensures compatibility and leverages the performance of the core Git engine.

**Alternatives considered**:

- **Direct `subprocess` calls to `git`**: This would offer maximum control but would require manually parsing the output of Git commands, which is brittle and error-prone. It would significantly increase development time and complexity compared to using a dedicated library.
- **Other Git libraries**: While other libraries exist, GitPython is the most established and has the most extensive documentation and community support, making it the lowest-risk choice.

## Best Practices for GitPython Usage

1.  **Repository Object**: Always start by instantiating a `git.Repo` object. For performance, it's best to instantiate it once and reuse it rather than creating it for every operation.
    ```python
    from git import Repo
    repo = Repo('/path/to/repo')
    ```

2.  **Iterating Commits**: Use `repo.iter_commits()` for efficiently iterating through the commit history of a branch or a commit range. This is a generator and is memory-efficient, which is crucial for large repositories.
    ```python
    for commit in repo.iter_commits('main', max_count=50):
        print(commit.hexsha)
        print(commit.message)
    ```

3.  **Accessing Code Changes (Diffs)**: To get the changes for a specific commit, diff it against its parent(s). The `commit.diff()` method returns a `DiffIndex` object containing `Diff` objects for each changed file.
    ```python
    # Diff against the first parent
    parent = commit.parents[0]
    diffs = parent.diff(commit)

    for diff_item in diffs:
        # diff_item.a_path is the old path
        # diff_item.b_path is the new path
        # diff_item.change_type is 'A' (added), 'D' (deleted), 'M' (modified), etc.
        # To get the actual diff content:
        # diff_content = diff_item.diff.decode('utf-8')
    ```
    **Note**: Handling merge commits (with multiple parents) requires a specific strategy, such as diffing against each parent individually or using a combined diff.

4.  **Error Handling**: Wrap GitPython calls in `try...except` blocks to handle potential `git.exc.GitCommandError` exceptions, which can occur if the underlying Git command fails (e.g., repository not found, invalid revision).

5.  **Resource Management**: Ensure that GitPython processes are properly closed, although the library generally handles this well. When dealing with large amounts of data (like file contents from diffs), be mindful of memory usage.
