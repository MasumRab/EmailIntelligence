# Plan: Intelligent Git Conflict Resolution

## Background & Motivation
Recent manual merge conflict resolutions resulted in the accidental deletion of code and intent, circumventing the sophisticated conflict resolution tools built into the EmailIntelligence project. To ensure the integrity of the codebase, structural alignment, and adherence to project constitutional rules, all conflict resolution must be performed using the project's native CLI tools (`dev.py` and `emailintelligence_cli.py`).

## Scope & Impact
This plan affects all files currently containing Git merge conflict markers (e.g., `<<<<<<< HEAD`, `=======`, `>>>>>>>`). The impact is high, as the codebase must be correctly aligned to preserve both the architectural improvements from the main branch and the feature-specific functionality from the merging branch.

## Proposed Solution
Instead of manual text editing, the system will execute a proper analysis of the merge conflicts using the unified CLI and the `EmailIntelligenceCLI`. This involves mapping the git topology, assessing the constitutional compliance of the conflicts, and using intelligent, semantic-aware 3-way merging commands (`auto-resolve` or `merge-smart`) to properly disentangle and resolve the code.

## Implementation Steps

1. **Topology Mapping & Discovery**:
   - Run `python dev.py git-topology` or `python dev.py git-discover` to map the commit topology causing the conflicts and identify the precise nature of the drift.
   
2. **Conflict Analysis & Constitutional Check**:
   - Use `python emailintelligence_cli.py setup-resolution` and `analyze-constitutional` (or `python dev.py git-analyze`) to analyze the conflicting files against the project's constitutional rules.
   
3. **Strategy Generation**:
   - Execute `python emailintelligence_cli.py develop-spec-kit-strategy` to generate a safe resolution strategy that maximizes enhancement preservation.
   
4. **Intelligent Resolution Execution**:
   - Run `python emailintelligence_cli.py auto-resolve` (or `python dev.py git-auto-resolve` / `python dev.py merge-smart`) to execute the generated strategy and intelligently merge the files.
   - For remaining conflicts, use `python dev.py git-align` or `python dev.py git-merge-semantic`.

## Verification & Testing
- Run `python emailintelligence_cli.py validate-resolution` to comprehensively validate the resolved codebase against syntax checks, basic functionality, and constitutional compliance.
- Run `pytest` to ensure all unit and integration tests pass successfully without regressions.

## Migration & Rollback
- If the intelligent merger produces unexpected results, the git worktree can be reset (`git reset --hard HEAD` and `git clean -fd`) and the resolution process restarted with tweaked constitutional or alignment parameters.
