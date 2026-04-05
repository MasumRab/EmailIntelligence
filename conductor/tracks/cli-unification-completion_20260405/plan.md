# Implementation Plan: CLI Unification Completion

## Phase 1: Forensic Feature Discovery
- [ ] Task 1.1: Execute semantic search (`mcp_ck-search_semantic_search`) across remote branches to match implemented features with project requirements.
- [ ] Task 1.2: Identify any "Ghost Features" (implemented logic not currently registered in `CommandRegistry`).
- [ ] Task 1.3: Document missing features and prepare wrapping commands.
- [ ] Task: Conductor - User Manual Verification 'Forensic Discovery' (Protocol in workflow.md)

## Phase 2: Architectural Hardening & Cleanup
- [ ] Task 2.1: Delete `src/speckit/*.py` and replace with `README.md` explaining the LLM-driven prompt workflow.
- [ ] Task 2.2: Refactor `src/cli/services/nlp.py` to remove `NLPEngine` imports and add LLM intent requirements.
- [ ] Task 2.3: Scan `src/cli/commands/` for any other naive text processing and mark for refactoring.
- [ ] Task: Conductor - User Manual Verification 'Hardening & Cleanup' (Protocol in workflow.md)

## Phase 3: Feature Integration
- [ ] Task 3.1: Wrap any missing features identified in Phase 1 into new `Command` classes.
- [ ] Task 3.2: Register new commands in `src/cli/commands/__init__.py`.
- [ ] Task 3.3: Run `logic-compare` to verify parity between wrapped features and original remote logic.
- [ ] Task: Conductor - User Manual Verification 'Feature Integration' (Protocol in workflow.md)

## Phase 4: Final Validation
- [ ] Task 4.1: Run `code-audit` to ensure all new/restored logic is gated by `SecurityValidator`.
- [ ] Task 4.2: Execute `pytest` on all CLI-related tests.
- [ ] Task 4.3: Final cross-branch sync to ensure 100% completion status.
- [ ] Task: Conductor - User Manual Verification 'Final Validation' (Protocol in workflow.md)
