# Data Model: Rebase Analysis and Intent Verification

**Purpose**: Define the key entities and their relationships for the Rebase Analysis and Intent Verification feature.
**Created**: 2025-11-19
**Feature**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Entities

### 1. Commit

-   **Description**: Represents a change in the repository history.
-   **Attributes**:
    *   `hash` (string): Unique identifier for the commit (SHA-1).
    *   `author` (string): Name and email of the commit author.
    *   `date` (timestamp): When the commit was authored.
    *   `message` (string): Full commit message.
    *   `changes` (list of strings): Summary of file changes (e.g., file paths, type of change).
    *   `timestamp` (timestamp): From clarification (Session 2025-11-10)
    *   `parent_shas` (list of strings): SHA-1 hashes of parent commits. From clarification (Session 2025-11-10)
    *   `file_changes_summary` (string): Summarized description of file changes. From clarification (Session 2025-11-10)
    *   `inferred_intent` (string): The purpose or goal behind the change, inferred by the system.
    *   `is_ambiguous_intent` (boolean): Flag indicating if intent inference was ambiguous and requires manual review.
    *   `is_rebase_conflict_resolution` (boolean): Flag indicating if this commit resolved a merge conflict during rebase.

### 2. Branch

-   **Description**: A line of development in the repository.
-   **Attributes**:
    *   `name` (string): Name of the branch (e.g., `main`, `feature/xyz`).
    *   `head_commit_hash` (string): SHA-1 hash of the latest commit on the branch.
    *   `is_rebased` (boolean): Flag indicating if the branch's history has been rewritten (detected via heuristic).
    *   `tracking_remote_hash` (string): The hash of the remote tracking branch's head commit, used for rebase detection.

### 3. Rebase Operation

-   **Description**: The act of moving or combining a sequence of commits to a new base commit, resulting in rewritten history.
-   **Attributes**:
    *   `original_base_commit` (string): SHA-1 hash of the commit the branch was originally based on.
    *   `new_base_commit` (string): SHA-1 hash of the commit the branch is now based on.
    *   `rebased_commits` (list of Commit objects): The sequence of commits that were rebased.
    *   `occurrences` (integer): Number of times a branch has been rebased.

### 4. Analysis Report

-   **Description**: A summary of the rebase analysis and verification results.
-   **Attributes**:
    *   `summary_stats` (object): High-level statistics (e.g., total commits analyzed, commits with ambiguous intent).
    *   `chronological_story` (list of Commit objects): The structured list of commits with inferred intent.
    *   `action_items` (list of Commit objects): Commits flagged for mandatory manual review due to ambiguous intent or resolved conflicts.
    *   `report_format` (string): Type of report (e.g., Markdown).
