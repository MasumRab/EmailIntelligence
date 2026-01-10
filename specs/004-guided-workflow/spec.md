# Feature Specification: Guided CLI Workflows

**Feature Branch**: `004-guided-workflow`
**Created**: 2025-11-14
**Status**: Draft

## 1. Overview

This feature introduces a guided workflow system, accessible via the main `launch.py` script. Its purpose is to provide clear, contextual guidance to developers and AI agents, preventing common errors and ensuring adherence to the repository's established orchestration and PR resolution processes.

The system will be built around a `WorkflowContextManager` and will provide two initial guides: `guide-dev` for general development tasks and `guide-pr` for pull request resolution.

## 2. User Stories

### User Story 1: General Development Guidance
As a developer, I want to run a simple command that tells me which workflow to follow based on my intent (working on application code vs. orchestration tools/agent configs), so that I don't have to remember the complex rules of the orchestration system.

### User Story 2: PR Resolution Guidance
As a developer, I want a tool that guides me through the correct process for merging a pull request, so that I know whether to use a standard `git merge` or the special `reverse_sync_orchestration.sh` script.

## 3. Functional Requirements

### `guide-dev` Workflow
- **FR-001**: The system MUST provide a `guide-dev` command accessible via `python launch.py guide-dev`.
- **FR-002**: The guide MUST ask the user to choose (interactively or via CLI argument) between "working on application code" and "modifying orchestration tools (scripts, CLI tools, launch system, agent configs)".
- **FR-003**: If "application code" is chosen, the guide MUST inform the user that no special workflow is needed and that they can develop on their feature branch as usual.
- **FR-004**: If "orchestration tools" is chosen, the guide MUST check the user's current Git branch and repository status (dirty/clean).
- **FR-005**: If the user is on the `orchestration-tools` branch, the guide MUST inform them it is safe to proceed with edits.
- **FR-006**: If the user is NOT on the `orchestration-tools` branch, the guide MUST warn them that their changes will be overwritten and advise them to switch to the `orchestration-tools` branch first (stashing or committing any uncommitted changes if the repo is dirty).

### `guide-pr` Workflow
- **FR-007**: The system MUST provide a `guide-pr` command accessible via `python launch.py guide-pr`.
- **FR-008**: The guide MUST ask the user to choose (interactively or via CLI argument) between resolving a "daily orchestration change" and a "major feature branch merge".
- **FR-009**: If "orchestration change" is chosen, the guide MUST instruct the user to use the `scripts/reverse_sync_orchestration.sh` script and warn them against using a direct `git merge`.
- **FR-10**: If "major feature merge" is chosen, the guide MUST recommend a standard `git merge` and proactively list the critical validation steps (e.g., running tests, verifying sync) from `docs/orchestration-workflow.md` directly in the CLI.

### `WorkflowContextManager`
- **FR-011**: A `WorkflowContextManager` MUST be implemented in `src/lib/workflow_context.py`.
- **FR-012**: The context manager MUST maintain and persist the state of the user's current workflow (e.g., which guide they are in, what step they are on) to disk (`.taskmaster/workflow_state.json`) to allow state recovery between runs.
- **FR-013**: The context manager MUST be used by the `guide-dev` and `guide-pr` commands to provide stateful guidance.
- **FR-014**: Both commands MUST support non-interactive usage via CLI arguments (e.g., `--intent`, `--type`) to support automation and AI agents.

[...] 

## Clarifications
### Session 2026-01-09
- Q: To support "AI agents" and automation, should the `guide-dev` and `guide-pr` commands support non-interactive CLI arguments for intent selection? → A: Yes, add CLI arguments for non-interactive mode.
- Q: Does the `WorkflowContextManager` need to persist state across command executions (e.g., to disk), or is it sufficient for the state to be transient (in-memory only)? → A: Persistent (Save state to file between runs).
- Q: For FR-004 (Git branch check), should the guide also check for uncommitted changes or a dirty repository before advising the user to proceed or switch branches? → A: Yes, check for uncommitted changes/dirty repo (Ensures safer branch transitions).
- Q: Where should the `WorkflowContextManager` persist its state file? → A: `.taskmaster/workflow_state.json`.
- Q: In guide-pr (FR-010), when a "major feature merge" is chosen, should the guide merely remind the user to check docs/orchestration-workflow.md, or should it proactively list the critical validation steps directly in the CLI output? → A: Proactively list critical validation steps in CLI.

## 4. Non-Functional Requirements
- **NFR-001**: The guidance provided MUST be clear, concise, and unambiguous.
- **NFR-002**: The system MUST NOT modify any files or Git state directly; it should only provide information and recommend commands for the user to run.
- **NFR-003**: The guided workflow system MUST be optional to use; experienced developers MAY bypass it and perform git operations directly if they follow the correct procedures.

## 5. Assumptions
- The user is running the `launch.py` script from the root of the repository.
- The user has a basic understanding of Git and pull requests.
