# Feature Specification: Unified Git Analysis and Verification

**Feature Branch**: `003-unified-git-analysis`
**Created**: 2025-11-11
**Status**: Draft
**Input**: User description: "A unified tool to analyze Git history, generate a synthesized description of intent, and verify the integrity of the code after merges or rebases."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Action Narrative (Priority: P1)

As a developer, I want to analyze any branch or commit range to generate a clear, synthesized narrative of the actions taken, based on both commit messages and the associated code changes.

**Why this priority**: This is the foundational capability, providing a high-quality "intent" that powers all other features.

**Independent Test**: Can be tested by providing a repository with known history and verifying that the generated narrative is accurate and more descriptive than the commit messages alone.

**Acceptance Scenarios**:

1. **Given** a Git repository and a specified branch, **When** the `analyze` command is run, **Then** a synthesized narrative for each commit is produced.
2. **Given** a commit with a vague message but significant code changes, **When** the `analyze` command is run, **Then** the narrative accurately describes the actions reflected in the code.

---

### User Story 2 - Identify Rebased Branches & Generate Intent Report (Priority: P2)

As a developer, I want the tool to automatically identify branches that have been rebased and require review, and to generate a pre-merge "Intent Report" for them.

**Why this priority**: Automates a manual and error-prone part of the code review process, ensuring that rebased branches get proper scrutiny.

**Independent Test**: Can be tested by creating and rebasing a branch, then running a `detect-rebased` command and verifying the branch is identified and an Intent Report is generated.

**Acceptance Scenarios**:

1. **Given** a feature branch that has been rebased onto `main`, **When** the `detect-rebased` command is run, **Then** the feature branch is listed as a candidate for verification.
2. **Given** a rebased branch, **When** the `analyze --rebased` command is run, **Then** a comprehensive "Intent Report" containing the synthesized narrative for all its commits is generated.

---

### User Story 3 - Verify Post-Merge Integrity (Priority: P2)

As a reviewer, after a rebased branch is merged, I want to run a verification check that compares the final merged state against the pre-merge "Intent Report" to ensure no changes were lost or altered.

**Why this priority**: Provides the ultimate safeguard, ensuring that complex rebases and merges do not silently introduce errors or discard work.

**Independent Test**: Can be tested by generating an Intent Report, merging the branch, and running a `verify` command to check for discrepancies.

**Acceptance Scenarios**:

1. **Given** a merged branch and its corresponding pre-merge Intent Report, **When** the `verify` command is run, **Then** a report is produced confirming that all intended changes are present in the target branch.
2. **Given** a merged branch where a change was accidentally dropped during the rebase, **When** the `verify` command is run, **Then** the report highlights the specific discrepancy.

---

### User Story 4 - Unified Tool Access (Priority: P1)

As a developer, I want a single, unified tool that is easily accessible on any branch to perform analysis and verification.

**Why this priority**: Ensures the tool is easy to adopt and integrate into any developer's workflow.

**Independent Test**: Can be tested by installing the tool and running it from different branches within the repository.

**Acceptance Scenarios**:

1. **Given** the tool is installed, **When** I switch to any branch, **Then** the `git-verifier` command is available and executes successfully.

---

### Edge Cases

- How does verification handle intentional changes made during a rebase (e.g., fixing a typo in a previous commit)? The tool will treat these as discrepancies unless explicitly marked/ignored by the user.
- What is the performance on very large repositories with tens of thousands of commits?
- How are merge commits handled during narrative generation and verification?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST synthesize a narrative description by prioritizing code changes, inferring intent from them, and cross-referencing with the commit message, AND using an LLM to generate a human-like summary of both.
- **FR-002**: The system MUST provide a mechanism to detect rebased branches by looking for "rebase (finish)" messages in the reflog.
- **FR-003**: The system MUST generate a consolidated "Intent Report" for a given branch.
- **FR-004**: The system MUST compare a merged branch's state against an Intent Report and identify discrepancies, defined as any difference in file content between the Intent Report's expected state and the merged branch's actual state.
- **FR-005**: The system MUST be accessible as a single CLI tool (`git-verifier`).
- **FR-006**: The system MUST allow analysis of any arbitrary commit range, not just rebased branches.
- **FR-007**: The system MUST detect and anonymize common secret formats and personally identifiable information (PII) from code changes before sending any data to an external LLM for analysis.
- **FR-008**: The `analyze` command MUST output the generated `IntentReport` to a specified file path, and the `verify` command MUST accept an `IntentReport` file path as an input argument.

### Non-Functional Requirements

#### Security & Privacy
- **NFR-SEC-001**: All source code sent to external LLMs MUST be anonymized to remove secrets and PII.

#### Error Handling
- **NFR-ERR-001**: The system MUST attempt to recover from transient errors (e.g., network issues, temporary API unavailability) gracefully. If recovery is not possible, it MUST print a descriptive error message to stderr, suggest potential solutions, and exit with a non-zero status code.

### Key Entities *(include if feature involves data)*

- **ActionNarrative**: A synthesized description of a single commit's intent and actions.
- **IntentReport**: A collection of `ActionNarrative`s for all commits in a branch, representing the total intended change.
- **VerificationResult**: The output of the verification process, indicating consistency or listing discrepancies between an `IntentReport` and the final merged state.
  - `missing_changes`: `list[object]` where each object contains `commit_hexsha` (string), `file_path` (string), `change_type` (string: add/delete/modify).
  - `unexpected_changes`: `list[object]` where each object contains `commit_hexsha` (string), `file_path` (string), `change_type` (string: add/delete/modify).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The tool MUST correctly identify 95% of rebased branches in a test suite.
- **SC-002**: The verification process MUST detect 99% of content-altering discrepancies introduced during a rebase.
- **SC-003**: A developer using the tool MUST be able to review and verify a complex rebased branch 50% faster than with manual review.
- **SC-004**: The tool MUST generate a complete Intent Report for a branch with 50 commits in under 20 seconds.
- **SC-005**: The tool MUST generate a complete Intent Report for a branch with 1,000 commits in under 5 minutes, with performance degradation being acceptable beyond this point.

## Out of Scope

- **OOS-001**: Support for Source Code Management (SCM) systems other than Git (e.g., Mercurial, SVN) is explicitly out of scope for the initial version.

## Assumptions

- The system has access to the Git repository's reflog to help identify rebased branches.
- The primary value is in verifying that the *content* of the final merge is consistent with the intent of the individual commits, not that the commit hashes themselves are identical.

## Clarifications

### Session 2025-11-11
- Q: How should the "synthesized narrative" be generated? → A: Prioritize code changes, inferring intent from them, and cross-referencing with the commit message, AND use an LLM to generate a human-like summary of both.
- Q: What specific reflog patterns or heuristics define a "rebased branch" for detection? → A: Look for "rebase (finish)" messages in the reflog.
- Q: What defines a "discrepancy" during verification? → A: Any difference in file content between the Intent Report's expected state and the merged branch's actual state.
- Q: What information should be included in the `missing_changes` and `unexpected_changes` objects within `VerificationResult`? → A: Commit SHA, file path, and type of change (add/delete/modify).
- Q: How should the tool handle "intentional changes" made during a rebase (e.g., fixing a typo in a previous commit) during verification? → A: Treat them as discrepancies unless explicitly marked/ignored by the user.
- Q: How should the tool handle potentially sensitive information within the source code to ensure privacy and security? → A: Anonymize secrets/PII before sending to the LLM, but send the rest of the code.
- Q: How should the Intent Report be stored and passed between the `analyze` and `verify` commands? → A: The `analyze` command saves the Intent Report to a file (e.g., `intent-report.json`). The `verify` command then requires the path to this file as an argument.
- Q: How should errors be communicated to the user? → A: Attempt to recover gracefully where possible (e.g., retry a failed API call). If recovery fails, print a descriptive error to stderr and exit with a non-zero status code.
- Q: What is the maximum number of commits the tool should be designed to handle in a single analysis run before performance degradation is acceptable? → A: 1,000 commits.
- Q: Which functionalities should be explicitly considered out of scope for the initial version of this tool? → A: Support for other Source Code Management (SCM) systems (e.g., Mercurial, SVN).