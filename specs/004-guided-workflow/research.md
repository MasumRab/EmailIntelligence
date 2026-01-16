# Research: Unified Launch System (Scientific Integration)

**Feature**: 004-guided-workflow
**Status**: Revised (Unified Strategy)

## 1. Integration Strategy

### Discovery
The `scientific` branch contains a mature `EmailIntelligenceCLI` (`eai`) with advanced capabilities:
- **Semantic Conflict Detection**: `GitConflictDetector`
- **Constitutional Analysis**: `ConstitutionalEngine`
- **AI Resolution**: `AutoResolver`

### Decision: Full Integration (Unified CLI)
Instead of maintaining two CLIs (`launch.py` and `emailintelligence_cli.py`), we will **merge** the Scientific capabilities into the Orchestration `launch.py` framework.
- **Goal**: One entry point for all developers (`python launch.py`).
- **Mechanism**: Port `eai` commands to `setup/commands/*.py` using the `Command` pattern.
- **Architecture**: Move Scientific Engines to `src/core/` and `src/resolution/` as shared libraries.

## 2. Data Model Alignment

### Decision: Shared Schema
The Orchestration tools must adopt the `Conflict` and `Violation` schemas defined in `src.core.conflict_models` (Scientific) to allow seamless data exchange.
- **Conflict**: Represents semantic conflicts.
- **ResolutionPlan**: Tracks the strategy for resolving them.

## 3. Git Plumbing Strategy

### Decision: `git worktree` (Scientific Approach)
The `scientific` CLI uses ephemeral worktrees for isolation. The Unified `guide-pr` command will adopt this pattern:
- **Isolate**: Complex merges happen in `resolution-workspace` worktrees.
- **Protect**: The user's main worktree remains untouched until validation passes.

## 4. AST Scanning Strategy

### Decision: `ConstitutionalEngine`
We will migrate the `ConstitutionalEngine` class to `src/resolution/` and expose it via `launch.py analyze`.
- **Config**: It will continue to use the YAML-based "Constitutions" found in `.emailintelligence/constitutions/`.