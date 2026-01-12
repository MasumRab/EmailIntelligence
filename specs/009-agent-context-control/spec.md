# Feature Specification: Agent Context Control

**Feature Branch**: `009-agent-context-control`
**Created**: 2026-01-13
**Status**: Draft

## User Scenarios

### US1: Branch-Aware Context Switching
As an AI Agent, I need my context (rules, prompts, memory) to automatically switch when the git branch changes, so that I don't use "scientific" rules on "orchestration" code.

**Independent Test**:
1. Start on `main`. Verify context loaded is "General".
2. Switch to `scientific`. Verify context loaded is "Scientific".
3. Switch to `orchestration-tools`. Verify context loaded is "Orchestration".

### US2: Context Isolation
As a Project Maintainer, I want to ensure that experimental rules in a feature branch do not leak into other branches.

## Requirements

- **FR-001**: System MUST detect current git branch and map it to a Context Profile.
- **FR-002**: System MUST enforce strict isolation (no cross-loading of rules).
- **FR-003**: System MUST support project-specific configuration overrides.
- **FR-004**: Performance: Context switch MUST happen in < 2 seconds.

## Success Criteria
- **SC-001**: Zero context contamination incidents in 100 manual switch tests.
- **SC-002**: Context switch latency < 500ms (average).
