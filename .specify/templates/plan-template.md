# Implementation Plan: Orchestration Core & Guided Workflows

**Branch**: `004-guided-workflow` | **Date**: 2026-03-15 | **Spec**: ./spec.md
**Input**: Feature specification for `dev.py` (Orchestration Core) - Updated with constitution v1.6.0

## Summary

Implement `dev.py` as the unified developer cockpit, replacing scattered scripts with a high-rigor, API-first Python application. This system integrates Git plumbing (merge-tree), constitutional enforcement (AST scanning), and atomic session persistence to enable safe, guided development workflows.

**2026-03-15 Updates:**
- Constitution updated to v1.6.0 with Agentic-First Design (Principle 0)
- dev.py converted from argparse to typer (DONE)
- FR-036 to FR-042 added (BM25, task engine, IDE generation)
- pyastsim (v1.2.0) and gkg now available for integration

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: 
- `typer[all]` (CLI) - ✅ Installed
- `pydantic` (Data Models) - ✅ Installed
- `GitPython` or subprocess (Plumbing)
- `rich` (UI) - ✅ Installed
- `InquirerPy` (Interactive prompts)
- `pyastsim` (AST similarity) - ✅ Installed, NOT integrated
- `gkg` (code structure) - ✅ Available in PATH
- `rank-bm25` (BM25 text similarity) - ❌ Not installed

**Storage**: Atomic JSON (`.dev_state.json`) for session persistence (Gitignored).
**Testing**: `pytest` with functional Git side-effect verification (Ephemeral Repos).
**Target Platform**: Developer Workstation (Linux/macOS).
**Project Type**: Single Project (CLI Tool).
**Performance Goals**: <5s analysis for 100 commits; <200ms CLI startup.
**Constraints**: Zero working-tree modification during analysis; No logic in `scripts/`.
**Scale/Scope**: ~20 core modules, supporting 1000+ commits history analysis.
**IDE Integration**: Templates for VSCode, Antigravity, and Windsurf (US1/FR-010).

## Constitution Check (v1.6.0)

*GATE: Must pass before Phase 0 research.*

**New Requirements from v1.6.0:**

1. **Principle 0 (Agentic-First)**: All CLI tools designed for AI agent consumption
   - ✅ dev.py supports --json output (stub implementations)
   - ⚠️ Exit codes: 0/1/2 defined but not implemented
   - ⚠️ Error format: `{code, message, details, hint}` not implemented

2. **Rule Hierarchy**: MUST vs SHOULD clearly distinguished
   - (PASS) Existing rules use MUST appropriately

3. **Rationale Explanations**: Added to Sections I, II, VII
   - (PASS) Why TDD matters for AI validation
   - (PASS) Why API-first enables agent integration

**Pre-existing Checks:**
- **Principle VII (API-First)**: Core logic (git, analysis, resolution) isolated in `src/core/` and exposed via Pydantic APIs. `dev.py` is a thin CLI wrapper. (PASS)
- **Principle IX (Orchestration)**: `dev.py` respects the "File Ownership Matrix", managing only orchestration files. (PASS)
- **Principle II (TDD)**: All logic engines (merge-tree parser, AST scanner) testable via unit tests before integration. (PASS)
- **Extension B (Verification)**: "Context-Aware Verification" implemented via AST Scanner and Sync Service. (PASS)

## Phase Priorities (Based on Constitution v1.6.0)

### Phase 1: Core CLI Infrastructure (HIGHEST PRIORITY)

Per Constitution Section XII (Agentic-First):

1. **FR-001**: Implement JSON output for all dev.py commands
   - Add `--json` flag to all subcommands
   - Return structured JSON instead of echo()
   - Exit codes: 0=success, 1=error, 2=usage

2. **FR-005**: Implement Pydantic models for all data
   - Ensure JSON serialization works
   - Add --json output to existing commands

### Phase 2: Git Analysis Integration

3. **FR-031 to FR-033**: Branch comparison features
   - Directory structure comparison
   - Filename fuzzy matching
   - Content-level diff analysis

4. **FR-034**: pyastsim integration (library available)
   - Integrate for AST structural similarity
   - Add to deps command

5. **FR-035**: gkg integration (CLI available)
   - Integrate for code structure analysis
   - Parse parquet dependency graphs

### Phase 3: Advanced Features

6. **FR-036**: BM25 text similarity (requires rank-bm25)
7. **FR-040**: Task execution engine
8. **FR-041**: IDE task file generation

### Phase 4: Polish (Phase 2 - Deferred)

9. **FR-037**: Sentence embeddings (heavy dependency)

## Completed Items

| Item | Status | Notes |
|------|--------|-------|
| dev.py typer conversion | ✅ DONE | Converted from argparse |
| typer/click/rich installed | ✅ DONE | Dependencies installed |
| workspace imports fixed | ✅ DONE | Relative imports corrected |
| RiskLevel extracted | ✅ DONE | types.py reduced to 7 lines |
| workspace/ gitignored | ✅ DONE | Added to .gitignore |
| FR-036 to FR-042 | ✅ DONE | Added to spec.md |
| Constitution v1.6.0 | ✅ DONE | Agentic-First Design added |

## Gaps & Blockers

| Gap | Status | Resolution |
|-----|--------|------------|
| JSON output not implemented | BLOCKED | Add to Phase 1 |
| Exit codes not implemented | BLOCKED | Add to Phase 1 |
| Error format not implemented | BLOCKED | Add to Phase 1 |
| rank-bm25 not installed | BLOCKED | Install for FR-036 |
| ast-grep not installed | BLOCKED | Install for FR-039 |

## Project Structure

### Source Code (repository root)

```text
src/
├── core/                    # Pure Logic (API-First)
│   ├── git/                 # Plumbing wrappers (merge-tree, rev-list)
│   ├── analysis/            # AST Scanner, Sync Service
│   ├── resolution/         # Conflict Logic, Rebase Planner
│   ├── execution/           # Session Manager, Action Executor
│   └── models/              # Pydantic Definitions
├── cli/                     # Interface Layer
│   ├── commands/            # Typer subcommands (analyze, plan, etc.)
│   └── main.py              # dev.py entry point
└── utils/                   # Shared utilities (logging, hashing)

dev.py                       # Unified CLI entry point
workspace/                   # Extracted CLI patterns (gitignored)

tests/
├── unit/                    # Logic tests (AST, Parsing)
├── integration/             # Git side-effect tests (Ephemeral)
└── fixtures/                # Complex git history generators
```

**Structure Decision**: Standard "Single Project" layout, strictly separating `core` (Logic) from `cli` (Presentation) to satisfy Principle VII.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| In-Memory Git Analysis | "Plumbing over Porcelain" requirement (US2) | `git checkout` (Porcelain) disrupts user workflow and triggers hooks. |
| AST Scanning | "Constitution Enforcement" (US4) | Regex matching is too fragile for detecting logical violations (e.g. class structure). |
| Multi-IDE Support | "Unified Cockpit" (US1) | Restricting to VSCode alienates users of Windsurf/Antigravity; Template complexity is low. |
| Atomic Hook Backup | "Fail-Safe" (Design Principle 1) | Interactive prompts for every hook install create friction; Backup is safer. |
