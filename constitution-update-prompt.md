# Constitution Update Prompt

## Context

The project has evolved to focus on creating CLI/TUI tools primarily for AI agent consumption. The current constitution (v1.3.0) lacks explicit guidance on designing tools for agentic workflows. This update adds Section XII to address this gap.

## Current Constitution Status

- **Location**: `.specify/memory/constitution.md`
- **Current Version**: 1.3.0
- **Last Amended**: 2025-11-10

## Proposed Changes

### Section XII: Agentic-First Tool Design (NEW)

Add a new NON-NEGOTIABLE section that mandates all CLI/TUI tools be designed for AI agent consumption:

**Core Requirements:**
1. **Machine-Parseable Output**: Every command MUST support `--json` output
2. **Explicit Exit Codes**: 0=success, 1=error, 2=usage error
3. **Structured Error Handling**: JSON errors with `{code, message, details, hint}`
4. **Composability**: Commands designed for piping between agents
5. **Idempotency**: Safe to re-run without side effects
6. **Self-Documenting**: `--help` provides complete usage for agent prompting

**Rationale:**
- Current constitution mentions "CLI tools" in Extension A but doesn't mandate agentic-first design
- Specs created without this principle result in tools that work for humans but not for agents
- Alignment with spec-driven development best practices (Agent Factory, spec-kit)

## Implementation Notes

- This section applies to: `dev.py`, `launch.py`, orchestration scripts, and all CLI utilities
- Every FR in spec.md should include JSON output schema
- Exit code definitions must be documented per command
- Error response format: `{code: string, message: string, details?: object, hint?: string}`

## Version Update

- Update version from 1.3.0 to 1.4.0
- Add amendment log entry with date (2026-03-15)

## Files to Modify

1. `.specify/memory/constitution.md` - Add Section XII
2. `specs/004-guided-workflow/spec.md` - Add Constitution Compliance section
3. `specs/004-guided-workflow/GAP_ANALYSIS.md` - Document constitution update

## Success Criteria

- [ ] Section XII added with all 6 requirements
- [ ] Version bumped to 1.4.0
- [ ] Amendment log updated
- [ ] spec.md includes Constitution Compliance section
- [ ] GAP_ANALYSIS reflects new requirements
