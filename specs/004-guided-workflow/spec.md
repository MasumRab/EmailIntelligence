# Feature Specification: Orchestration Core

**Feature Branch**: `004-guided-workflow`  
**Created**: 2026-01-13  
**Status**: Draft  
**Input**: User description: "Implement the Orchestration Core (dev.py). Unify branching, conflict analysis, rebase planning, and task execution into a single cockpit. SEPARATION: dev.py is the exclusive entry point for dev-tools. launch.py is forbidden for this scope and remains App Runtime only. NO STUBS: Functional implementation is mandatory. Identify and replace all placeholders in src/cli/commands and src/services with real logic. PLUMBING: Use git merge-tree for in-memory conflict detection and git rev-list for history analysis. Avoid modifying the working tree during analysis. ALGORITHMS: Rebase planning must use Directed Acyclic Graph (DAG) analysis and Topological Sorting. ENFORCEMENT: Implement AST-based scanning to enforce constitution.md rules (e.g. 'No logic in scripts/'). DATA FLOW: All internal communication between src/core and dev.py must use Pydantic models. TESTING: 100% of log engines must be verified via side-effect tests using ephemeral (temporary) Git repositories."

## 1. Overview
This feature implements `dev.py`, the unified entry point for the "Orchestration Core". It replaces existing stubs with high-rigor logic engines for Git analysis, conflict resolution, and task execution. SEPARATION: `dev.py` is the exclusive entry point for dev-tools. `launch.py` is forbidden for this scope and remains App Runtime only.

## Clarifications

### Session 2026-01-14
- Q: Synchronization mechanism? → A: Strict Hash-based comparison (SHA-256).
- Q: Synchronization resolution strategy? → A: Interactive: Multi-select which files to overwrite.
- Q: Constitutional Rule Definition? → A: Config-Driven: Parse rules dynamically from constitution.md or a structured governance.yml.
- Q: Violation Report Delivery? → A: Stdout: Stream the JSON payload directly to standard output.
- Q: Canonical Orchestration Source? → A: Remote Branch: Use origin/orchestration-tools as the canonical source of truth for synchronization.
- Q: Rebase Strategy? → A: Interactive: Generate plan and provide a `dev.py rebase --apply` command to execute it.
- Q: Session Persistence Location? → A: Local Hidden: Store atomic state in `.dev_state.json` (gitignored) in the repository root.
- Q: Hook Installation Strategy? → A: Backup & Overwrite: Rename existing hooks to `.bak` and install new ones.
- Q: Supported IDEs for init? → A: Multi-IDE: VSCode, Antigravity, and Windsurf.

## 2. User Scenarios & Testing

### User Story 1 - Unified Development Cockpit (Priority: P1)

As a developer, I want a single entry point `dev.py` to manage all my development workflows (branching, analysis, resolution, tasks), so that I have a consistent and powerful interface for repository orchestration that is separate from the application runtime.

**Why this priority**: Core architectural requirement to separate developer tools from the application code and provide a cohesive experience.

**Independent Test**: Can be fully tested by running `python dev.py --help` and verifying that all core orchestration subcommands are present and functional.

**Acceptance Scenarios**:

1. **Given** the repository root, **When** I run `python dev.py`, **Then** I see a unified CLI interface with subcommands for orchestration.
2. **Given** a development task (e.g., rebase), **When** I use `dev.py`, **Then** the system guides me through the high-rigor logic engine instead of generic placeholders.

---

### User Story 2 - In-Memory Conflict Analysis (Priority: P1)

As a developer, I want to analyze merge conflicts between branches without modifying my current working tree, so that I can evaluate merge safety and resolution strategies purely in memory.

**Why this priority**: Essential for implementing the "Plumbing over Porcelain" principle and ensuring that analysis doesn't disrupt ongoing work.

**Independent Test**: Create two conflicting branches. Run `dev.py analyze`. Verify that all conflicts are identified correctly matching `git merge` results, but the working tree remains `clean`.

**Acceptance Scenarios**:

1. **Given** branch A and branch B have content conflicts, **When** I run `dev.py analyze A B`, **Then** the system reports all conflicting files and hunks using `git merge-tree`.

---

### User Story 3 - Algorithmic Rebase Planning (Priority: P2)

As a developer, I want the system to automatically reorder my commits logically (e.g., dependencies before features) using topological sorting, so that my commit history remains clean and linear.

**Why this priority**: Implements the "Algorithmic Rigor" requirement and automates complex history management.

**Independent Test**: Create a set of commits with clear dependencies (e.g., commit 2 fixes commit 1). Run rebase planner. Verify the output plan reorders them correctly using DAG analysis.

**Acceptance Scenarios**:

1. **Given** a branch with complex history, **When** I run `dev.py plan-rebase`, **Then** the system outputs a topologically sorted plan where dependent commits are correctly sequenced.
2. **Given** a generated rebase plan, **When** I run `dev.py rebase --apply`, **Then** the system executes the rebase using the planned order.

---

### User Story 4 - Constitutional Rule Enforcement (Priority: P2)
As a project maintainer, I want the system to scan my code changes against `constitution.md` rules using AST analysis, so that architectural violations (like logic in scripts/) are blocked before they are committed.

### User Story 5 - Automated Onboarding & Sync (Priority: P2)
As a developer switching to an old feature branch, I want the system to detect divergence from the canonical `orchestration-tools` and provide an interactive multi-select interface to sync environment scripts, ensuring I always use the latest validated tools while maintaining control over local changes.
- **Requirement**: Use SHA-256 hash comparison to verify toolset identity against the canonical branch.

### User Story 6 - Headless CI Governance (Priority: P1)

As a CI pipeline runner, I want to execute the Orchestration Core in a non-interactive mode using JSON payloads, allowing automated enforcement of the project constitution via a structured violation report.



### User Story 7 - Resilient Session Recovery (Priority: P3)

As a developer performing a complex 20-commit rebase, I want the system to persist my progress atomically after every step so that if the process is interrupted, I can resume from the exact point of failure without losing previous resolutions.



---



### Edge Cases



- **Binary Conflict Handling**: System MUST handle `merge-tree` output for binary files without crashing and report them clearly.

- **Malformed `tasks.md`**: The task runner MUST provide clear error messages with line numbers if the markdown task syntax is invalid.

- **Diverged Remotes**: If analysis involves branches that have diverged from their remotes, the system MUST warn the user or perform a fetch.



## Requirements *(mandatory)*



### Functional Requirements



- **FR-001**: System MUST provide a unified CLI entry point `dev.py` using the `typer` framework.

- **FR-002**: System MUST use `git merge-tree --real-merge` for conflict detection to ensure zero working-tree side effects.

- **FR-003**: System MUST implement a `HistoryService` that builds a DAG of commits and performs topological sorting for rebase planning.

- **FR-004**: System MUST implement an `ASTScanner` using the Python `ast` module to verify compliance with rules dynamically parsed from `constitution.md`.

- **FR-005**: System MUST use Pydantic models for all internal data exchange (Conflicts, CommitNodes, ExecutionPlans).

- **FR-006**: System MUST replace existing placeholders in `src/cli/commands/` and `src/services/` with these functional implementations.

- **FR-007**: System MUST support a `--dry-run` flag for all Git-mutating operations.

- **FR-008**: System MUST parse and execute `tasks.md` files, providing real-time status updates and logging.

- **FR-009**: System MUST support a `--json` (headless) mode for all subcommands to allow agentic orchestration without interactive prompts.

- **FR-010**: System MUST provide an `ide-init` command to generate IDE-specific configurations for VSCode, Antigravity, and Windsurf, mapping `tasks.md` to IDE task runners.

- **FR-011**: System MUST implement a "Token-Saver" mode that suppresses all non-essential terminal styling (Rich panels, colors) when `--json` or `--quiet` is active.

- **FR-012**: System MUST allow pre-answering interactive prompts via a `--answers` JSON input to enable fully non-interactive agentic flows.

- **FR-013**: System MUST use SHA-256 hash comparison to detect divergence between local environment files and the `origin/orchestration-tools` remote branch.

- **FR-014**: System MUST persist session state atomically to `.dev_state.json` after every successful action/step to maximize crash recovery resilience.

- **FR-015**: System MUST generate a structured JSON violation report (Rule, File, Line, Snippet) delivered via stdout for constitutional violations detected by the AST scanner.

- **FR-016**: System MUST provide an interactive multi-select interface for `dev.py sync` to allow users to choose which diverged files to overwrite from the canonical source.

- **FR-017**: System MUST implement `dev.py install-hooks` to automatically configure git pre-commit hooks that enforce constitutional rules, renaming existing hooks to `.bak` if they exist.

- **FR-018**: System MUST implement `dev.py schema` to output JSON schemas for all internal Pydantic models to support CI integration.



### Key Entities *(include if feature involves data)*

- **Conflict**: File path, conflict type, OIDs, conflicting hunks.
- **CommitNode**: Commit SHA, parent SHAs, dependencies, classification (feature/fix/chore).
- **ExecutionPlan**: Ordered list of `Action` objects (ShellCommand, GitPlumbing, FileEdit).
- **ConstitutionalRule**: Rule name, target paths (glob), prohibited patterns (AST/Regex).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of conflict analysis matches `git merge` results in a test suite of 50 edge-case merges.
- **SC-002**: Analysis of a 100-commit history completes in under 5 seconds.
- **SC-003**: 0% working tree modification during the `analyze` and `plan` phases.
- **SC-004**: 100% of logic engines pass side-effect tests in ephemeral Git repositories.
- **SC-005**: All code violations defined in `constitution.md` are detected with 95% accuracy by the AST scanner.

## Assumptions
- The environment has `git` version >= 2.38 (for `merge-tree --real-merge`).
- `constitution.md` exists and is formatted according to project standards.