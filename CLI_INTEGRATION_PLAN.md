# CLI Integration Plan: Completing the Transition to Real Implementations

**Date:** 2025-11-29
**Status:** In Progress
**Goal:** Replace all mock implementations in `emailintelligence_cli.py` with the real, modular implementations from `src/`.

## Overview
The `emailintelligence_cli.py` tool currently operates in a hybrid state. The **Constitutional Analysis** feature is fully functional and uses the real `src.resolution.ConstitutionalEngine`. However, other critical components (Conflict Detection, Strategy Generation, Validation) still rely on mock implementations using hash-based randomization.

This plan outlines the steps to integrate the remaining real modules into the CLI.

## Phase 1: Foundation (✅ Complete)
*   **Constitutional Engine**: Integrated and working.
*   **Module Structure**: `src/` directory populated with core modules.

## Phase 2: Git Operations Integration (Conflict Detection)
**Objective**: Replace the `git diff --name-only` mock in `_detect_conflicts` with the real `GitConflictDetector` that uses `git merge-tree`.

*   **Task 2.1**: Import `GitConflictDetector` in `emailintelligence_cli.py`.
*   **Task 2.2**: Update `_detect_conflicts` to use `GitConflictDetector.detect_conflicts`.
    *   *Note*: Ensure async methods are handled correctly (wrap in `asyncio.run` if needed).
*   **Task 2.3**: Verify that `Conflict` objects returned by the detector are correctly serialized for the metadata JSON.

## Phase 3: Strategy Integration
**Objective**: Replace the hash-based `_generate_spec_kit_strategy` with the real `StrategySelector` / `StrategyGenerator`.

*   **Task 3.1**: Import `StrategySelector` (and `StrategyGenerator` if available) in `emailintelligence_cli.py`.
*   **Task 3.2**: Update `develop_spec_kit_strategy` to use the real strategy modules.
    *   Pass the `AnalysisResult` from the constitutional analysis to the strategy selector.
*   **Task 3.3**: Ensure the generated strategy follows the Spec Kit format required by the CLI's display methods.
*   **Task 3.4**: Implement `EnhancementPreservation` module (currently missing in `src/`).
*   **Task 3.5**: Implement `AlignmentScorer` module (currently missing in `src/`).

## Phase 4: Validation Integration
**Objective**: Replace the hash-based `_perform_validation` with real test execution.

*   **Task 4.1**: Create a `TestRunner` class in `src/validation/test_runner.py` (if not exists) to handle `pytest`, `bandit`, etc.
*   **Task 4.2**: Update `_perform_validation` in `emailintelligence_cli.py` to use `TestRunner`.
    *   Implement `_run_actual_tests` logic.
*   **Task 4.3**: Add support for parsing test results (JUnit XML, JSON) into the CLI's reporting format.

## Phase 5: Cleanup & Optimization
**Objective**: Remove dead code and optimize performance.

*   **Task 5.1**: Remove all methods marked with `# WARNING: Mock ...`.
*   **Task 5.2**: Remove unused imports (e.g., `hashlib` might become less used).
*   **Task 5.3**: Standardize logging using `structlog` across the CLI (currently uses print/custom methods).

## Remaining Mocks to Address
| Component | Current State | Target Implementation |
|-----------|---------------|----------------------|
| **Conflict Detection** | `git diff` (Mock) | `src.git.conflict_detector.GitConflictDetector` |
| **Strategy Generation** | Hash-based (Mock) | `src.strategy.selector.StrategySelector` |
| **Validation** | Hash-based (Mock) | Real `pytest`/`bandit` execution (via `src.validation.test_runner`) |
| **Enhancement Preservation** | Mock file counting | **MISSING** (Need `src.analysis.enhancement`) |
| **Alignment Scoring** | Mock percentage | **MISSING** (Need `src.analysis.alignment`) |

## Next Steps
1.  Execute **Phase 2** (Git Operations Integration).
2.  Verify conflict detection with a real merge conflict scenario.
