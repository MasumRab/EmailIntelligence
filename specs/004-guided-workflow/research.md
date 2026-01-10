# Phase 0 Research: Guided CLI Workflows

**Feature**: `004-guided-workflow`
**Date**: 2026-01-09

## 1. Unknowns & Clarifications

### 1.1 `launch.py` Missing from Root
-   **Context**: The spec assumes `python launch.py ...` works, but `launch.py` is not in the root.
-   **Finding**: `setup/launch.py` exists and appears to be the main entry point logic.
-   **Resolution**: Create a root `launch.py` that delegates to `setup.launch.main()`.

### 1.2 Missing Documentation Reference
-   **Context**: Spec refers to `docs/final_merge_approach.md`, which does not exist.
-   **Finding**: `docs/orchestration-workflow.md` contains relevant workflow information.
-   **Resolution**: Update the guidance text to refer to `docs/orchestration-workflow.md`.

### 1.3 Git Integration
-   **Context**: Need to check the current branch.
-   **Finding**: `src/lib/git_wrapper.py` exists and uses `GitPython`.
-   **Resolution**: Use `src.lib.git_wrapper.GitWrapper` to query the current branch.

## 2. Technology Choices

### 2.1 CLI Framework
-   **Choice**: `argparse` (via `setup/launch.py`).
-   **Rationale**: `setup/launch.py` already uses `argparse`. We should extend the existing `main()` function or the `_execute_command` pattern if available.
-   **Pattern**: `setup/launch.py` uses a command pattern (`setup.commands`). We should verify if we can add new commands there or if we need to add them to the parser directly.

### 2.2 State Management
-   **Choice**: `src.lib.workflow_context.WorkflowContextManager`.
-   **Rationale**: Defined in spec and tasks. Simple class to track state.

## 3. Implementation Strategy

1.  **Modify `setup/launch.py`**:
    *   Add `guide-dev` and `guide-pr` subparsers.
    *   Implement handlers that use `WorkflowContextManager`.
2.  **Create Root `launch.py`**:
    *   Simple wrapper to import and run `setup.launch.main`.
3.  **Update `src/lib/workflow_context.py`**:
    *   Ensure it has `__enter__`/`__exit__` and state tracking (already done in preparation).
