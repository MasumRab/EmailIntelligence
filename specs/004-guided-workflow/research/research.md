# Research: Orchestration Core & Guided Workflows (EVOLVED)

**Feature**: `004-guided-workflow`
**Date**: 2026-01-13

## Conflict Detection Plumbing
- **Decision**: `git merge-tree --real-merge`
- **Rationale**: Mandated by Spec (FR-002) and Constitution (Section VIII). It allows for full 3-way merge analysis in-memory, producing OIDs for merged results or conflict markers without touching the worktree.
- **Plumbing Details**: We will parse the output of `git merge-tree <base> <branch1> <branch2>` which provides a tree OID if successful, or lists conflict hunks.

## Rebase Algorithms
- **Decision**: DAG builder with Topological Sort
- **Rationale**: Required for high-rigor rebase planning (US-3).
- **Implementation**: Use `git rev-list --parents` to gather the graph edges. Implement Kahn's algorithm or a DFS-based topological sort to reorder commits while respecting dependencies.

## AST Analysis for Rule Enforcement
- **Decision**: Python `ast` module
- **Rationale**: Mandated by Spec (FR-004) and Constitution (Section IX).
- **Patterns**: We will look for `FunctionDef` and `ClassDef` in prohibited directories (e.g. `scripts/`). We will also check for specific imports to ensure logic is kept in `src/core/`.

## Data Interchange & Machine Protocol
- **Decision**: Pydantic v2 + Stable IDs + Schema Versioning
- **Rationale**: Mandated by Spec (FR-005, FR-009) and Constitution (Section IX). Provides type-safety and validation for complex Git metadata structures.
- **Agentic Efficiency**: Implement a "Token-Saver" mode that strips ANSI escapes and Rich panels when `--json` is detected.

## Synchronization Service (US5)
- **Decision**: Hash-based comparison with `orchestration-tools`.
- **Rationale**: To ensure environment scripts are canonical across branches.
- **Implementation**: Identify managed files via `docs/orchestration_summary.md` (or a manifest). Compare local hashes against the same paths in the `orchestration-tools` remote ref.

## Session Recovery & Persistence (US7)
- **Decision**: Atomically-written JSON state (`.dev_state.json`).
- **Rationale**: To handle resilient recovery of long-running operations.
- **Payload**: Must store the `ExecutionPlan`, the index of the last successful `Action`, and the accumulated `ConflictModel` results.