# Specification: CLI Unification Completion & LLM Intent Migration

## Overview
This track focuses on finishing the CLI unification process by ensuring all functional features from remote branches are consolidated into the unified SOLID architecture. It also mandates a shift away from rigid, code-based text processing (naive NLP) towards a flexible, context-aware LLM-driven intent processing model.

## Functional Requirements
- **Forensic Feature Retrieval**: Use fuzzy and semantic search across all remote branches to identify features that have been implemented but not yet pulled into the unified CLI.
- **Redundancy Removal**: Remove the `src/speckit/` Python implementation as it overlaps with the more effective agent-based prompts in `.gemini/` and `.specify/`.
- **NLP Service Refactoring**: Remove direct `NLPEngine` piping from the CLI and enforce LLM-based processing for all "intent" and "purpose" understanding.
- **Agent Workflow Enforcement**: Standardize the use of `.gemini/commands/` for complex developer workflows like specification analysis and planning.

## Acceptance Criteria
- `src/speckit/` directory removed (archived) and replaced with documentation of the LLM-based workflow.
- `src/cli/services/nlp.py` refactored to remove backend ML dependencies and specify LLM requirements.
- Zero functional loss: All identified unique features from remote branches are wrapped into the unified CLI.
- All 26+ unified commands remain functional and pass security validation.

## Out of Scope
- Performance optimization of the LLM itself.
- Merging the final consolidated code into `main` (this is a completion track for the implementation).
