# Implementation Plan: Task Execution Layer

**Branch**: `013-task-execution-layer` | **Date**: 2026-03-17 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/013-task-execution-layer/spec.md`
**Consolidated from**: Previous specs 007 and 011

## Summary

Implement a robust task execution layer that parses `tasks.md` files, executes defined tasks sequentially with state tracking, supports crash recovery via session persistence, and generates execution reports. This builds on the foundational execution modules already scaffolded in `src/core/execution/` during 004-guided-workflow (TaskRunner, ActionExecutor, SessionManager).

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- `pydantic` (Data Models) - ✅ Installed
- `typer[all]` (CLI integration) - ✅ Installed
- `rich` (UI/progress) - ✅ Installed
- `src/core/execution/session.py` (SessionManager) - ✅ Exists (from 004)
- `src/core/execution/executor.py` (ActionExecutor) - ✅ Exists (from 004, stub)
- `src/core/execution/task_runner.py` (TaskRunner) - ✅ Exists (from 004, stub)
- `src/core/models/execution.py` (ExecutionPlan, Action) - ✅ Exists (from 004)

**Storage**: Atomic JSON (`.dev_state.json`) for session/execution state persistence (Gitignored).
**Testing**: `pytest` with functional side-effect verification.
**Target Platform**: Developer Workstation (Linux/macOS).
**Performance Goals**: Report generation < 1s after execution completes.
**Constraints**: Must integrate with 004's existing session and model infrastructure.

## Constitution Check

- (PASS) Agentic-First: All execution commands support `--json` output
- (PASS) TDD: Ephemeral test fixtures for execution verification
- (PASS) No logic in `scripts/` — all execution logic in `src/core/execution/`

## Existing Infrastructure (from 004-guided-workflow)

The following modules exist but need enhancement for full 013 scope:

| Module | Current State | 013 Enhancement Needed |
|--------|--------------|----------------------|
| `task_runner.py` | Basic markdown parsing, marks tasks done | Full parser with metadata, dependencies, commands |
| `executor.py` | Shell execution with dry-run | Timeout support, parallel mode, stderr capture |
| `session.py` | Atomic JSON load/save/clear | Per-task checkpointing, resume index |
| `models/execution.py` | ExecutionPlan, Action models | Task model with dependencies, ExecutionLog, ExecutionReport |

## Phases

### Phase 1: Task Parser Enhancement

Upgrade `TaskRunner` from simple line-matching to a structured parser that extracts Task ID, description, command, status, dependencies, and metadata from `tasks.md` format.

1. **FR-001**: Implement structured `tasks.md` parser
   - Parse task ID (T001), description, status (checkbox), metadata blocks
   - Support dependency declarations between tasks
   - Validate task IDs are unique and dependencies exist
   - Output: List of `Task` Pydantic models

### Phase 2: Execution Engine

Upgrade `ActionExecutor` to support configurable execution modes.

2. **FR-002/FR-003**: Implement full execution engine
   - Sequential execution with state tracking (Pending → In Progress → Done/Failed)
   - Configurable: stop-on-fail vs continue-on-fail
   - Per-task timeout support (configurable, default 300s)
   
3. **FR-005**: Implement execution logging
   - Capture stdout/stderr per task
   - Timestamped log entries in `ExecutionLog` model
   - Stream output to console via Rich

### Phase 3: Crash Recovery

Enhance `SessionManager` for per-task state persistence.

4. **FR-004**: Implement resume functionality
   - Save execution index after each task completion
   - On startup, detect stale session and prompt for resume
   - Resume from last failed/stopped task

### Phase 4: Reporting & Integration

5. **FR-006**: Implement execution report generation
   - Summary: total/passed/failed/skipped counts
   - Per-task: duration, status, output snippet
   - JSON and Rich table output modes
   - Link tasks to PR issues when metadata present (US2)

### Phase 5: Edge Cases & Polish

6. **Edge Cases**: Circular dependency detection, infinite loop prevention
   - DAG validation before execution
   - Timeout enforcement per task
   - Environment snapshot at start of run

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Shell command injection | Validate commands, support allowlist mode |
| Stale session corruption | Atomic writes (already implemented), schema version checks |
| Long-running tasks | Configurable timeout with SIGTERM → SIGKILL escalation |
