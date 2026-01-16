# Feature Specification: Guided CLI Workflows

**Feature Branch**: `004-guided-workflow`
**Created**: 2025-11-14
**Status**: Implementation Phase (Unified Architecture)

## 1. Overview

This feature introduces a guided workflow system, accessible via a new `dev.py` script in the repository root. Its purpose is to provide clear, contextual guidance to developers and AI agents, utilizing the advanced conflict resolution engines from the `scientific` branch which have been integrated into `src/core/`.

The system uses a `WorkflowContextManager` to manage state and `dev.py` as a decoupled entry point, ensuring independence from the legacy `launch.py` system.

## 2. User Stories

### User Story 1: General Development Guidance
As a developer, I want to run `python dev.py guide-dev` to receive workflow guidance based on my intent, so that I don't have to remember the complex rules of the orchestration system.

### User Story 2: PR Resolution Guidance
As a developer, I want to run `python dev.py guide-pr` to be guided through the correct process for merging a pull request.

### User Story 3: Advanced Conflict Analysis
As a developer merging complex branches, I want the system to perform a deep analysis of potential conflicts (content vs. structural) and architectural violations (e.g., forbidden imports) *before* I attempt the merge, so I can plan my resolution strategy without breaking the build.

### User Story 4: Optimal Rebase Planning
As a developer with a divergent feature branch, I want the system to suggest an optimal rebase order based on the commit topology, minimizing repeated conflict resolution steps.

## 3. Functional Requirements

### `dev.py` Sidecar CLI
- **FR-001**: The system MUST provide a `dev.py` entry point at the repository root.
- **FR-019**: The `dev.py` script MUST route commands to standalone modules in `src/cli/guides/` or `src/core/`.

### `guide-dev` Workflow
- **FR-002**: The guide MUST first ask the user to choose between "working on application code" and "modifying a shared setup/config file".
- **FR-003**: If "application code" is chosen, the guide MUST inform the user that no special workflow is needed and that they can develop on their feature branch as usual.
- **FR-004**: If "shared setup/config" is chosen, the guide MUST check the user's current Git branch.
- **FR-005**: If the user is on the `orchestration-tools` branch, the guide MUST inform them it is safe to proceed with edits.
- **FR-006**: If the user is NOT on the `orchestration-tools` branch, the guide MUST warn them that their changes will be overwritten and advise them to switch to the `orchestration-tools` branch first.

### `guide-pr` Workflow
- **FR-007**: The `dev.py` script MUST provide a `guide-pr` command.
- **FR-008**: The guide MUST ask the user to choose between resolving a "daily orchestration change" and a "major feature branch merge".
- **FR-009**: If "orchestration change" is chosen, the guide MUST instruct the user to use `scripts/manage_orchestration_changes.sh`.
- **FR-010**: If "major feature merge" is chosen, the guide MUST invoke the **Integrated Resolution Engine**.

### Scientific Capabilities Integration (Unified Logic)
- **FR-014**: The standalone guides MUST import and utilize the capabilities of migrated engines from `src/core/` and `src/resolution/`.
- **FR-015**: The migrated engines include: `ConstitutionalEngine`, `GitConflictDetector`, and `AutoResolver`.
- **FR-016**: The `guide-pr` workflow MUST invoke these internal Python classes directly.
- **FR-017**: Dependencies for these engines MUST be documented in `src/cli/guides/requirements.txt` or similar.
- **FR-020**: The system MUST utilize a dedicated `GitWorktreeRunner` component (`src/core/git/worktree.py`) to manage ephemeral worktrees for conflict analysis, ensuring the user's main working directory remains untouched during "Safety Checks".

### `WorkflowContextManager`
- **FR-011**: A `WorkflowContextManager` MUST be implemented in `src/lib/workflow_context.py`.
- **FR-012**: The context manager MUST maintain the state of the user's current workflow (e.g., which guide they are in, what step they are on).
- **FR-013**: The context manager MUST be used by the `guide-dev` and `guide-pr` commands to provide stateful guidance.
- **FR-018**: The context manager MUST utilize `scripts/stash_manager_optimized.sh` to safely stash and restore changes during branch switching operations.

## 4. Non-Functional Requirements
- **NFR-001**: The guidance provided MUST be clear, concise, and unambiguous.
- **NFR-002**: The system MUST NOT modify any files or Git state directly; it should only provide information and recommend commands for the user to run.
- **NFR-003**: The implementation MUST be decoupled from `launch.py`. It should run as a standalone script/module to allow future integration via import/plugin without code changes.

## 5. Assumptions
- The user is running the `dev.py` script from the root of the repository.
- The user has a basic understanding of Git and pull requests.

