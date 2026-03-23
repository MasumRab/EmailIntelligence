# Implementation Plan: Guided CLI Workflows

**Branch**: `004-guided-workflow` | **Date**: 2026-01-09 | **Spec**: `specs/004-guided-workflow/spec.md`
**Input**: Feature specification from `/specs/004-guided-workflow/spec.md`

## Summary

Implement a guided CLI workflow system (`guide-dev`, `guide-pr`) integrated into `launch.py`. This system uses a `WorkflowContextManager` to guide developers through repository-specific workflows (orchestration vs. app code) and PR resolution strategies, ensuring adherence to the project's orchestration rules.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `GitPython` (via `src/lib/git_wrapper.py`), Standard Library (`argparse`, `sys`, `subprocess`)
**Storage**: N/A (State is transient or file-based checks)
**Testing**: `pytest` (Unit and Integration)
**Target Platform**: Linux/Dev Environment
**Project Type**: CLI Tool / Dev Utility
**Performance Goals**: Instant response (<200ms) for CLI commands.
**Constraints**: Must rely on `src/lib/git_wrapper.py` for git operations. Must integrate with existing `setup/launch.py`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the Orchestration Tools Verification and Review Constitution:
- **Verification-First Development**: Integration tests defined for CLI guides.
- **Goal-Task Consistency**: Directly addresses "Guided CLI Workflows" feature.
- **Role-Based Access Control**: N/A (Local Dev Tool).
- **Extensibility & Integration**: Integrates with `launch.py` and `git`.
- **Context-Aware Verification**: explicit checks for `orchestration-tools` branch.
- **Token Optimization**: N/A.
- **Fail-Safe by Default**: Warns users but allows them to fix.
- **Security Requirements**: No sensitive data handling.
- **Observability**: Logs to console.
- **Performance & Efficiency**: Lightweight CLI checks.
- **Reliability Requirements**: robust error handling in `launch.py`.

## Project Structure

### Documentation (this feature)

```text
specs/004-guided-workflow/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI Args)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
├── lib/
│   └── workflow_context.py       # Context Manager
└── cli/
    └── guides.py                 # (New) Guide implementations
setup/
└── launch.py                     # (Modified) CLI Entry point
launch.py                         # (New) Root wrapper
docs/
└── cli_workflow_map.md           # Workflow documentation
```

## Phases

### Phase 0: Outline & Research
- [x] Analyze `setup/launch.py` and `git_wrapper.py`.
- [x] Identify missing `launch.py` in root.
- [x] Resolve missing `final_merge_approach.md` reference.

### Phase 1: Design & Contracts
- [ ] Define `data-model.md` (Workflow States).
- [ ] Define `contracts/cli-guides.md` (CLI Arguments/Output).
- [ ] Create `quickstart.md`.
- [ ] Update `tasks.md` with refined TDD tasks.

### Phase 2: Implementation
- [ ] Create root `launch.py`.
- [ ] Implement `src/lib/workflow_context.py` (Refine).
- [ ] Implement `src/cli/guides.py`.
- [ ] Integrate into `setup/launch.py`.
- [ ] Add Tests.