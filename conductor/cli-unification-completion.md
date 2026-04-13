# Plan: LLM-Driven CLI Intent Processing & Speckit Consolidation

## 1. Remove `src/speckit/` Redundancy
- **Action**: Archive the `src/speckit/` directory (move to `archive/src_speckit/` or delete the python files).
- **Documentation**: Create a `README.md` in `src/speckit/` explaining that Speckit features are now purely agent-driven via `.gemini/commands/speckit.*.toml` and `.specify/scripts/bash/`. Native python text-processing for user feedback is strictly prohibited as it produces rigid and inferior results compared to an LLM.

## 2. Refactor `src/cli/services/nlp.py`
- **Action**: Remove the direct initialization of `NLPEngine` from the backend. 
- **Requirement Update**: Add comprehensive docstrings stating that any operation requiring the understanding of "user feedback," "intent," or "purpose" MUST be delegated to an LLM (via agent prompt workflows). 
- **Internal Matching**: The service will retain basic structural/lexical matching (like `difflib`) *only* for internal, rigid comparisons (e.g., finding typos in branch names), not for semantic intent.

## 3. Review & Update CLI Implementations
- **Action**: Scan the `src/cli/` implementations to identify any commands that prompt for open-ended "user feedback" or "intent" and route it through naive local text processing.
- **Enforcement**: Document inline that if a unified CLI command needs to understand complex user input, it must bridge out to the agent workflow instead of trying to parse it with regex or hardcoded keyword lists.