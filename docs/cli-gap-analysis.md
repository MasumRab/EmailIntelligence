# CLI Gap Analysis (Phase 1.5)

## Executive Summary
The goal of this analysis was to determine the current operational status of the CLI ecosystem on `consolidate/cli-unification` and identify gaps preventing it from being fully portable to `main` and `scientific`.

## Portability Principle
`consolidate/cli-unification` is intended to be a portable unified CLI framework. It must not hard-entangle with branch-specific backend modules (`src/resolution`, `src/analysis`, `src/backend`). All backend integrations must go through dependency injection via `create_default_dependencies` in `commands/integration.py`.

## Major Findings

### 1. Unified CLI Core (`src/cli/main.py`)
- **Status**: Framework is present (`CommandRegistry`, `CommandFactory`), but initial testing revealed runtime crashes.
- **Missing Dependencies**: `libcst`, `networkx`, `psutil` were missing from the environment setup.
- **Issue**: Argument collision (`-f` / `--format`) between different modules (`import_audit.py`, `topology.py`) crashed the global parser.

### 2. AI Conflict Resolution Workflow (`emailintelligence_cli.py`)
- **Status**: Fragmented & Degraded.
- **Analysis**: The monolithic `emailintelligence_cli.py` workflow is structurally broken. It attempts to load `ConstitutionalValidationResult` before `ComplianceResult` in `src.resolution.__init__.py` causing Python `NameError` crashes. Furthermore, the `ConstitutionalEngine` defaults to loading hardcoded dummy rules rather than dynamically traversing `.agent/rules/`.
- **Workflow Impact**: The AI resolution capability cannot execute its intended `setup -> analyze -> strategy -> align -> validate` sequence without being reimplemented securely within the modular `git-auto-resolve` wrapper.

### 3. Branch Orchestration (`scripts/orchestration/align/cli.py`)
- **Status**: Deprecated/Lost Workflow.
- **Analysis**: This script parses commands but does not actively execute Git rollback/planning hooks. It operates on static JSON inputs. Its capabilities have been partially superseded by `git-topology.py` (which hooks successfully into GitHub GraphQL).

### 4. State Persistence (`src/cli/state.py`)
- **Status**: Present, but unintegrated.
- **Analysis**: A `CLIState` manager successfully saves execution history to `~/.cli_state.json`. However, no major workflows actively consume this state to context-switch efficiently between command chains.

## Dependency Mapping & Impact
| Dependency | Used By | Capability Enabled | Replacement Possible? |
| ---------- | ------- | ------------------ | --------------------- |
| `libcst` | `import_audit.py` | High-fidelity AST refactoring | No, switching to standard `ast` destroys whitespace and comments. |
| `networkx` | `topology.py` | GitHub PR topology dependency graphing | Possible but difficult. Standard for graph theory. |
| `psutil` | `monitor.py` | Agent system monitoring | Possible via `/proc`, but `psutil` is cross-platform. |

These dependencies must be included optionally or lazily to ensure the unified CLI remains lightweight and importable into `main` without forcing ML/data downloads.
