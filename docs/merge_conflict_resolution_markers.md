# Handling Residual Merge Conflict Markers

During complex merge or rebase operations, it is common for Git's merge conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) to be accidentally left behind in files, even after attempting manual resolution. These lingering markers can lead to compilation errors, runtime bugs, and prevent automated tooling from functioning correctly.

This document outlines the strategy to ensure all merge markers are properly resolved.

---

## 1. The Most Reliable Method: Thorough Manual Resolution

The safest and most recommended way to prevent residual markers is to meticulously resolve each conflict manually, ensuring all markers are removed as part of the resolution process.

**Steps for Manual Resolution (Recap):**

1.  **Identify Conflicting Files:** After a `git merge` or `git rebase` results in conflicts, use `git status` to list all files with unmerged changes.
2.  **Open Each File:** Open one of the conflicting files in your preferred code editor.
3.  **Locate Markers:** Search for the specific conflict marker strings: `<<<<<<<`, `=======`, `>>>>>>>`.
4.  **Resolve Content:**
    *   Carefully review the code sections delimited by these markers.
    *   Based on the intended outcome (e.g., prioritizing changes from `pr176-integration-fixes` as per our merge strategy), decide which version of the code to keep, how to combine logic, or what new code to write.
    *   **Crucially, delete *all* `<<<<<<<`, `=======`, and `>>>>>>>` lines.** Ensure no partial markers or extra lines are left.
5.  **Stage the File:** Once you are confident the file is correctly resolved and all markers are removed, stage it: `git add <file-path>`.
6.  **Repeat:** Continue this process for all conflicting files listed by `git status`.
7.  **Final Commit:** Once `git status` shows "nothing to commit, working tree clean", you can safely finalize the merge with `git commit`.

---

## 2. Detecting Lingering Merge Markers (Verification Step)

After attempting to resolve all conflicts, it is highly recommended to perform a comprehensive check for any missed markers. The `git grep` command is ideal for this.

**Command to detect merge markers in the entire repository:**

```bash
git grep -E '^(<<<<<<<|=======|>>>>>>>)'
```

**How to Use:**
*   Run this command from your project's root directory.
*   If the command returns any output, it means there are still files containing merge markers.
*   For each file listed in the output, go back to step 2 of "Manual Resolution" above, open the file, locate the markers, resolve them, and stage the file.
*   Continue running the `git grep` command iteratively until it returns no output. This confirms your repository is free of merge markers.

---

By following these steps, you can ensure a clean and functional codebase post-merge, preventing unexpected issues from residual conflict markers.