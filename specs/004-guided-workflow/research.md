# Research: Guided CLI Workflows & Unified Integration

**Feature**: 004-guided-workflow
**Status**: Consolidated

## 1. Unified CLI Architecture (`dev.py`)

### Decision: Sidecar Entry Point
- **Context**: `launch.py` is complex and pending refactor.
- **Choice**: Create `dev.py` as a lightweight, independent entry point.
- **Rationale**: Decouples new developer tools from legacy infrastructure. Allows "Phase 2" implementation without regression risk.
- **Pattern**: `dev.py` imports standalone modules from `src/cli/guides/`.

## 2. Git Worktree Isolation (`GitWorktreeRunner`)

### Decision: Python Context Manager
- **Context**: Need safe, ephemeral environments for conflict analysis.
- **Inspiration**: [git-worktree-runner](https://github.com/coderabbitai/git-worktree-runner)
- **Implementation**:
  ```python
  with GitWorktreeRunner(branch="feature/x") as worktree:
      # worktree.path is now a clean directory
      engine.analyze(worktree.path)
  # auto-cleanup on exit
  ```
- **Rationale**: Provides the safety of the external tool without the binary dependency/shelling-out overhead.

## 3. Scientific Engine Integration

### Decision: Direct Import
- **Context**: Scientific code (`ConstitutionalEngine`, `GitConflictDetector`) is now merged into `src/`.
- **Choice**: `dev.py` commands (`analyze`, `resolve`) will directly import these classes.
- **Gap**: Requires `requirements-guides.txt` to ensure AI dependencies (like `PyYAML`, `networkx`) are present.

## 4. State Management

### Decision: `WorkflowContextManager`
- **Context**: Interactive guides need to remember user intent across steps.
- **Choice**: A simple state machine class (already prototyped in Phase 1).
- **Persistence**: In-memory for now. Future: `.dev_state.json` for resuming interrupted sessions.