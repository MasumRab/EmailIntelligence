# Implementation Plan: CLI Unification Completion

## Phase 1: Forensic Feature Discovery
- [x] Task 1.1: Execute semantic search (`mcp_ck-search_semantic_search`) across remote branches to match implemented features with project requirements.
- [x] Task 1.2: Identify any "Ghost Features" (implemented logic not currently registered in `CommandRegistry`).
- [x] Task 1.3: Document missing features and prepare wrapping commands.
- [x] Task: Conductor - User Manual Verification 'Forensic Discovery' (Protocol in workflow.md)

## Phase 2: Architectural Hardening & Cleanup
- [x] Task 2.1: Delete `src/speckit/*.py` and replace with `README.md` explaining the LLM-driven prompt workflow.
- [x] Task 2.2: Refactor `src/cli/services/nlp.py` to remove `NLPEngine` imports and add LLM intent requirements.
- [x] Task 2.3: Scan `src/cli/commands/` for any other naive text processing and mark for refactoring.
- [x] Task: Conductor - User Manual Verification 'Hardening & Cleanup' (Protocol in workflow.md)

## Phase 3: Feature Integration
- [x] Task 3.1: Wrap any missing features identified in Phase 1 into new `Command` classes.
- [x] Task 3.2: Register new commands in `src/cli/commands/__init__.py`.
- [x] Task 3.3: Run `logic-compare` to verify parity between wrapped features and original remote logic.
- [x] Task: Conductor - User Manual Verification 'Feature Integration' (Protocol in workflow.md)

## Phase 4: Final Validation
- [x] Task 4.1: Run `code-audit` to ensure all new/restored logic is gated by `SecurityValidator`.
- [x] Task 4.2: Execute `pytest` on all CLI-related tests.
- [x] Task 4.3: Final cross-branch sync to ensure 100% completion status.
- [x] Task: Conductor - User Manual Verification 'Final Validation' (Protocol in workflow.md)
