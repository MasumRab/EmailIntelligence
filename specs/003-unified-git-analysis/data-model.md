# Data Model for Unified Git Analysis and Verification

This document defines the core data entities and their structures for the
Unified Git Analysis and Verification feature, as derived from `spec.md`.
These models will primarily be implemented using Python dataclasses or Pydantic
models in `src/models/unified_analysis.py`.

## 1. ActionNarrative

A synthesized description of a single commit's intent and actions.

### Fields:
-   `commit_hexsha` (string): The full SHA-1 hash of the commit.
-   `author_name` (string): The name of the commit author.
-   `authored_date` (datetime): The timestamp when the commit was authored.
-   `commit_message` (string): The original commit message.
-   `synthesized_narrative` (string): The LLM-generated human-like summary of the commit's intent and actions, based on commit message and prioritized code changes.
-   `is_consistent` (boolean): Indicates if the synthesized narrative is consistent with the original commit message and inferred intent.
-   `discrepancy_notes` (string, optional): Notes on any inconsistencies found during narrative synthesis.

### Relationships:
-   Contained within `IntentReport`.

## 2. IntentReport

A collection of `ActionNarrative`s for all commits in a branch, representing
the total intended change.

### Fields:
-   `branch_name` (string): The name of the branch for which the report was generated.
-   `generated_at` (datetime): The timestamp when the report was generated.
-   `commit_narratives` (list of `ActionNarrative`): A list of all `ActionNarrative`s for the commits in the branch.

### Relationships:
-   Contains multiple `ActionNarrative` instances.
-   Used as input for `VerificationResult`.

## 3. VerificationResult

The output of the verification process, indicating consistency or listing
discrepancies between an `IntentReport` and the final merged state.

### Fields:
-   `branch_name` (string): The name of the merged branch that was verified.
-   `verified_at` (datetime): The timestamp when the verification was performed.
-   `is_fully_consistent` (boolean): True if no discrepancies were found, False otherwise.
-   `missing_changes` (list of `ChangeDetail`): A list of changes that were expected based on the `IntentReport` but are missing in the merged branch.
-   `unexpected_changes` (list of `ChangeDetail`): A list of changes found in the merged branch that were not expected based on the `IntentReport`.

### Nested Entity: ChangeDetail

Represents a specific file change identified as missing or unexpected.

### Fields:
-   `commit_hexsha` (string): The SHA-1 hash of the commit associated with the change.
-   `file_path` (string): The path to the file where the change occurred.
-   `change_type` (string): Indicates whether the change was an "add", "delete", or "modify".

### Validation Rules:
-   `commit_hexsha` must be a valid Git SHA-1 hash.
-   `file_path` must be a valid relative file path within the repository.
-   `change_type` must be one of "add", "delete", or "modify".