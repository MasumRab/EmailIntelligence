# Feature Specification: Orchestration Core

**Feature Branch**: `004-guided-workflow`  
**Created**: 2026-01-13  
**Updated**: 2026-03-14
**Status**: Draft  
**Input**: User description: "Implement the Orchestration Core (dev.py). Unify branching, conflict analysis, rebase planning, and task execution into a single cockpit. SEPARATION: dev.py is the exclusive entry point for dev-tools. launch.py is forbidden for this scope and remains App Runtime only. NO STUBS: Functional implementation is mandatory. Identify and replace all placeholders in src/cli/commands and src/services with real logic. PLUMBING: Use git merge-tree for in-memory conflict detection and git rev-list for history analysis. Avoid modifying the working tree during analysis. ALGORITHMS: Rebase planning must use Directed Acyclic Graph (DAG) analysis and Topological Sorting. ENFORCEMENT: Implement AST-based scanning to enforce constitution.md rules (e.g. 'No logic in scripts/'). DATA FLOW: All internal communication between src/core and dev.py must use Pydantic models. TESTING: 100% of log engines must be verified via side-effect tests using ephemeral (temporary) Git repositories."

## Cherry-Picked Features (from other branches)

| Source Branch | Feature | Purpose |
|--------------|---------|---------|
| consolidate/cli-unification | CommandFactory + Registry | Modular, extensible command architecture |
| feat-emailintelligence-cli-v2.0 | GitLogParser | Parse git log into structured Commit objects |
| feat-emailintelligence-cli-v2.0 | CommitClassifier | Conventional commits + risk detection |
| feat-emailintelligence-cli-v2.0 | RebasePlanner | Topological sort + priority sorting |
| taskmaster (001-012) | Git Hooks | pre-commit, pre-push enforcement |
| taskmaster (001-012) | Error Detection | Conflict markers, broken imports |

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

### User Story 8 - Branch Dependency Mapping (Priority: P2)

As a developer, I want to extract and compare the dependency graph (imports, function calls) between branches, so I can understand what refactoring was attempted and salvage incomplete work from outdated branches.

**Why this priority**: Critical for branch alignment — understanding architectural intent across branches enables informed merge decisions.

**Independent Test**: Create two branches with different import structures. Run `dev.py deps compare branch-a branch-b`. Verify the output shows added, removed, and moved dependencies.

**Acceptance Scenarios**:
1. **Given** two branches, **When** I run `dev.py deps compare`, **Then** the system outputs a JSON report showing: {added: [...], removed: [...], moved: [...]}
2. **Given** a refactoring in progress (functions moved between modules), **When** I compare branches, **Then** the system identifies the refactoring pattern (move vs delete+create)

---

### User Story 9 - Commit Intent Analysis (Priority: P2)

As a developer, I want to understand what each commit was INTENDED to do vs what it ACTUALLY changed, so I can make informed decisions during branch alignment and identify commits that may have introduced issues.

**Why this priority**: Enables historical analysis of code changes — critical for debugging issues introduced in past merges.

**Independent Test**: Analyze a branch with 10 commits. Verify each commit is classified with: {intent: "...", actual_change_type: "...", risk_level: "low|medium|high"}.

**Acceptance Scenarios**:
1. **Given** a commit with message "fix bug", **When** analyzed, **Then** system identifies actual change type (e.g., "refactor", "new_feature", "bug_fix", "docs")
2. **Given** a commit that changed architecture (file moves, module restructure), **Then** system flags as "architectural_change"
3. **Given** a commit that deleted significant code without corresponding feature removal, **Then** system flags as potential "regression" or "incorrect_deletion"

---

### User Story 10 - Merge Artifact Detection (Priority: P1)

As a developer, I want the system to detect incomplete merges, conflict markers, and broken references, so I can clean them up before integration.

**Why this priority**: Core requirement for branch alignment — prevents merging broken code.

**Independent Test**: Create a file with `<<<<<<<`, `=======`, `>>>>>>>`. Run `dev.py scan --artifacts`. Verify all markers are detected with file:line.

**Acceptance Scenarios**:
1. **Given** unmerged conflict markers in code, **When** scanned, **Then** report includes: {type: "conflict_marker", file, line, marker_type}
2. **Given** import from moved/renamed file, **When** scanned, **Then** report includes: {type: "broken_import", file, line, missing_module}
3. **Given** duplicate function/class definitions, **When** scanned, **Then** report includes: {type: "duplicate_def", file, line, symbol_name}

---

### User Story 11 - Change Classification (Priority: P2)

As a developer, I want each commit's changes classified as (architectural|docs|regression|error|merge_artifact|deletion), so I can identify problematic commits during integration.

**Why this priority**: Enables selective integration — skip or review specific commit types.

**Independent Test**: Run classification on a branch. Verify output groups commits by type with confidence scores.

**Acceptance Scenarios**:
1. **Given** commits modifying only `.md` files, **Then** classified as "documentation"
2. **Given** commits moving files between directories, **Then** classified as "architectural" with "refactor" subtype
3. **Given** commits reverting previous changes, **Then** classified as "revert"
4. **Given** commits with merge conflicts resolved, **Then** classified as "merge_artifact"

---

### User Story 12 - Branch Alignment Report (Priority: P2)

As a developer, I want a comprehensive alignment report between two branches showing divergence analysis, dependency changes, and risk assessment, so I can make informed merge decisions.

**Why this priority**: Provides holistic view for merge decision-making.

**Independent Test**: Run `dev.py align branch-a branch-b --json`. Verify output includes: {summary, dependency_diff, commit_classification, risk_score, recommendations}.

**Acceptance Scenarios**:
1. **Given** two branches with minor differences, **Then** risk_score is "low" with "safe to merge" recommendation
2. **Given** branches with conflicting architectural changes, **Then** risk_score is "high" with specific conflict points listed
3. **Given** branch with outdated dependencies, **Then** report warns about "integration_issues"





---



### Edge Cases


- **Binary Conflict Handling**: System MUST handle `merge-tree` output for binary files without crashing and report them clearly.
  - **Acceptance Criteria**: 
    - Binary file conflicts are reported with file path and "binary" type marker
    - System exits with code 0 (not crash) when binary conflicts detected
    - Output clearly distinguishes binary conflicts from text conflicts

- **Malformed `tasks.md`**: The task runner MUST provide clear error messages with line numbers if the markdown task syntax is invalid.
  - **Acceptance Criteria**:
    - Invalid checkbox syntax (missing [ ] or [x]) reports line number
    - Missing task ID reports which line caused the error
    - Error message includes "tasks.md" and line number in first 80 chars

- **Diverged Remotes**: If analysis involves branches that have diverged from their remotes, the system MUST warn the user or perform a fetch.
  - **Acceptance Criteria**:
    - Warning message includes branch name and divergence count (e.g., "3 commits behind")
    - `--json` mode includes "diverged": true in branch metadata
    - System prompts or auto-fetches based on --answers flag



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

- **FR-019**: System MUST implement `dev.py deps extract` to build a dependency graph (imports, function calls) from the codebase using AST analysis.

- **FR-020**: System MUST implement `dev.py deps compare <branch-a> <branch-b>` to output JSON report showing {added: [...], removed: [...], moved: [...], refactored: [...]} between branches.

- **FR-021**: System MUST implement `dev.py analyze --artifacts` to detect merge artifacts including: conflict markers, broken imports, duplicate definitions, orphaned exports.

- **FR-022**: System MUST implement `dev.py commit-classify` to analyze each commit and classify change type: (architectural|refactor|bug_fix|docs|regression|merge_artifact|deletion).

- **FR-023**: System MUST implement `dev.py align <branch-a> <branch-b>` to generate comprehensive alignment report including: divergence summary, dependency diff, commit classifications, risk score (low/medium/high), and merge recommendations.

- **FR-024**: System MUST use ast-grep (via Python API or CLI) for structural dependency extraction to accurately identify function calls, class definitions, and import relationships.

- **FR-025**: System MUST implement CLI architecture using CommandFactory + CommandRegistry pattern for modular, extensible command registration with dependency injection support (cherry-picked from consolidate/cli-unification).

- **FR-026**: System MUST implement GitLogParser to parse git log output into structured Commit objects (cherry-picked from feat-emailintelligence-cli-v2.0).

- **FR-027**: System MUST implement CommitClassifier with conventional commit parsing and risk keyword detection (cherry-picked from feat-emailintelligence-cli-v2.0).

- **FR-028**: System MUST implement RebasePlanner with topological sorting and priority-based commit reordering (cherry-picked from feat-emailintelligence-cli-v2.0).

- **FR-029**: System MUST implement cross-branch commit analysis to identify shared problematic commits (same SHA or similar change pattern) across multiple branches, with deduplication and merge/rebase recommendations.

- **FR-030**: System MUST provide fix/avoidance options for identified problematic commits including: (a) skip commit during rebase, (b) squash into parent, (c) cherry-pick only safe commits, (d) mark for review before merge.

- **FR-031**: System MUST implement directory structure comparison between branches to calculate structural similarity percentage.

- **FR-032**: System MUST implement filename similarity detection using fuzzy matching to identify renamed files across branches.

- **FR-033**: System MUST implement content-level diff analysis to identify added, removed, and modified files.

- **FR-034**: System MUST use pyastsim library for AST-based structural similarity detection between Python files.

- **FR-035**: System MUST integrate with gkg (git knowledge graph) for code structure analysis and generate parquet-based dependency graphs for branch comparison.

- **FR-036**: System SHOULD implement BM25-based text similarity scoring for comparing code comments, docstrings, and commit messages between branches.

- **FR-037**: System SHOULD implement sentence embedding-based semantic search for code documentation analysis between branches, using lightweight embeddings (e.g., sentence-transformers with a small model).

- **FR-038**: System MUST implement dynamic rule parsing from `constitution.md` by identifying sections marked with "## Rule:" or "### Forbidden:" followed by pattern definitions (regex or AST patterns).

- **FR-039**: System MUST use ast-grep CLI via subprocess for structural pattern matching when enforcing constitutional rules, with JSON output parsing for violation reporting.

- **FR-040**: System MUST implement task execution engine that parses `tasks.md` checkbox format and supports: (a) shell command execution, (b) file edit operations, (c) git operations, (d) conditional branching based on exit codes.

- **FR-041**: System MUST implement IDE task file generation that maps `tasks.md` entries to VSCode `.vscode/tasks.json`, Antigravity `antigravity.tasks.json`, and Windsurf `.windsurf/tasks.json` formats.

- **FR-042**: System MUST implement interactive resolution UX for FR-030 fix options using a numbered list selection interface (1-4) with preview of each option's impact before execution.


### Key Entities *(include if feature involves data)*

- **Conflict**: File path, conflict type, OIDs, conflicting hunks.
- **CommitNode**: Commit SHA, parent SHAs, dependencies, classification (feature/fix/chore).
- **ExecutionPlan**: Ordered list of `Action` objects (ShellCommand, GitPlumbing, FileEdit).
- **ConstitutionalRule**: Rule name, target paths (glob), prohibited patterns (AST/Regex).
- **Violation**: Rule name, file path, line number, code snippet, severity (error/warning).
- **DependencyGraph**: Nodes (files/modules), edges (imports/calls), metadata (call counts, cyclic deps).
- **AlignmentReport**: Summary stats, dependency diff, commit classifications, risk score, recommendations.
- **TaskItem**: ID, title, status (pending/in_progress/completed), dependencies, commands.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of conflict analysis matches `git merge` results in a test suite of 50 edge-case merges.
- **SC-002**: Analysis of a 100-commit history completes in under 5 seconds.
- **SC-003**: 0% working tree modification during the `analyze` and `plan` phases.
- **SC-004**: 100% of logic engines pass side-effect tests in ephemeral Git repositories.
- **SC-005**: All code violations defined in `constitution.md` are detected with 95% accuracy by the AST scanner.
- **SC-006**: BM25 similarity scoring completes for 1000 document pairs in under 2 seconds.
- **SC-007**: AST similarity detection using pyastsim returns results within 500ms per file pair.
- **SC-008**: gkg dependency graph generation completes for repositories up to 10,000 files in under 30 seconds.

## Assumptions
- The environment has `git` version >= 2.38 (for `merge-tree --real-merge`).
- `constitution.md` exists and is formatted according to project standards.

## Dependencies

### Python Packages (Required)
| Package | Purpose | FR |
|---------|---------|-----|
| `typer[all]` | CLI framework | FR-001 |
| `pydantic` | Data validation | FR-005 |
| `rich` | Terminal styling | FR-011 |
| `jinja2` | IDE template rendering | FR-041 |
| `pyastsim` | AST similarity detection | FR-034 |
| `rank-bm25` | BM25 text similarity | FR-036 |

### External Tools (Required)
| Tool | Purpose | FR |
|------|---------|-----|
| `gkg` | Git knowledge graph | FR-035 |
| `ast-grep` | Structural pattern matching | FR-039 |

### Optional (Phase 2)
| Package | Purpose | FR |
|---------|---------|-----|
| `sentence-transformers` | Semantic embeddings | FR-037 |
| `InquirerPy` | Interactive prompts | FR-016 |

---

## Constitution Compliance (Section XII)

All commands MUST comply with Section XII of constitution.md:

- **JSON Output**: Every command MUST support `--json` flag
- **Exit Codes**: 0=success, 1=error, 2=usage error
- **Structured Errors**: `{code, message, details, hint}`
- **Idempotency**: Safe to re-run
- **Self-Documenting**: `--help` for agent prompting