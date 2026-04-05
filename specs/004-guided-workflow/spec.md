# Feature Specification: Orchestration Core

**Feature Branch**: `004-guided-workflow`  
**Created**: 2026-01-13  
**Updated**: 2026-03-15
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
This feature implements `dev.py`, the unified entry point for the "Orchestration Core". It replaces existing stubs with high-rigor logic engines for Git analysis, conflict resolution, and task execution.

### Layered Analysis Architecture
The Orchestration Core employs a dual-layer analysis strategy to enable autonomous repository alignment:

1.  **Micro Layer (Branch Classification)**: Focused on the intent and risk of a single branch. It utilizes `CommitClassifier` (US11) and `ArtifactScanner` (US10) to determine what was changed and why.
2.  **Macro Layer (Repository Clustering)**: Focused on the relationship between all active branches. It utilizes `AgglomerativeClustering` (FR-048) and `MergeSequencer` (FR-058) to identify thematic overlaps and optimal merge paths.

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

### Session 2026-03-17
- Q: Remote operation scope for dev.py? → A: Configurable: Orchestrate local branches by default; allow remote operations (e.g., push) only if `--enable-remote` is set.
- Q: Lifecycle of .dev_state.json? → A: Ephemeral: Automatically delete the state file upon successful command completion; persist only if a process is interrupted or fails.
- Q: Primary logging sink for orchestration? → A: Local File: Store structured logs in `.dev_state/logs/` (e.g., JSONL) for debugging and auditing.
- Q: CLI output color/accessibility? → A: Always Color: Use Rich styling for all terminal output to maintain visual consistency.
- Q: Local authorization strategy for dev.py? → A: User-Only: Assume the current system user's permissions and fail with an explicit "PERMISSION_DENIED" error if elevated privileges are required.

## 2. User Scenarios & Testing

### User Story 1 - Unified Development Cockpit (Priority: P1)

As a developer, I want a single entry point `dev.py` to manage all my development workflows (branching, analysis, resolution, tasks), so that I have a consistent and powerful interface for repository orchestration that is separate from the application runtime. This cockpit allows local-first orchestration with optional remote integration via a safety flag.

**Why this priority**: Core architectural requirement to separate developer tools from the application code and provide a cohesive experience.

**Independent Test**: Can be fully tested by running `python dev.py --help` and verifying that all core orchestration subcommands and the `--enable-remote` global flag are present.

**Agent Interaction Flow**: Agent executes `python dev.py --json` to discover available commands and global options. It then uses specific subcommands like `dev.py analyze` to gather repo state. For CI flows, it uses `--enable-remote` to push results.
**Failure Recovery Path**: If `dev.py` is missing or fails to execute, the agent checks for Python environment issues or missing dependencies and attempts to run `pip install -r requirements.txt`.

**Acceptance Scenarios**:

1. **Given** the repository root, **When** I run `python dev.py`, **Then** I see a unified CLI interface with subcommands for orchestration.
2. **Given** a development task (e.g., rebase), **When** I use `dev.py`, **Then** the system guides me through the high-rigor logic engine instead of generic placeholders.

---

### User Story 2 - In-Memory Conflict Analysis (Priority: P1)

As a developer, I want to analyze merge conflicts between branches without modifying my current working tree, so that I can evaluate merge safety and resolution strategies purely in memory.

**Why this priority**: Essential for implementing the "Plumbing over Porcelain" principle and ensuring that analysis doesn't disrupt ongoing work.

**Independent Test**: Create two conflicting branches. Run `dev.py analyze`. Verify that all conflicts are identified correctly matching `git merge` results, but the working tree remains `clean`.

**Agent Interaction Flow**: Agent runs `dev.py analyze <branch1> <branch2> --json`. It parses the resulting JSON to identify conflicting files and hunks without affecting the local environment.
**Failure Recovery Path**: If Git is not installed or the branches do not exist, the agent receives an error JSON and attempts to fetch from remote or suggests branch creation.

**Acceptance Scenarios**:

1. **Given** branch A and branch B have content conflicts, **When** I run `dev.py analyze A B`, **Then** the system reports all conflicting files and hunks using `git merge-tree`.

---

### User Story 3 - Algorithmic Rebase Planning (Priority: P2)

As a developer, I want the system to automatically reorder my commits logically (e.g., dependencies before features) using topological sorting, so that my commit history remains clean and linear.

**Why this priority**: Implements the "Algorithmic Rigor" requirement and automates complex history management.

**Independent Test**: Create a set of commits with clear dependencies (e.g., commit 2 fixes commit 1). Run rebase planner. Verify the output plan reorders them correctly using DAG analysis.

**Agent Interaction Flow**: Agent triggers `dev.py plan-rebase --json` to get a structured sequence of commits. It then executes the plan via `dev.py rebase --apply --answers <json>`.
**Failure Recovery Path**: If the DAG analysis detects a cycle or missing parent, the agent receives a "TOPOLOGY_ERROR" and prompts the user for manual intervention or a conflict resolution strategy.

**Acceptance Scenarios**:

1. **Given** a branch with complex history, **When** I run `dev.py plan-rebase`, **Then** the system outputs a topologically sorted plan where dependent commits are correctly sequenced.
2. **Given** a generated rebase plan, **When** I run `dev.py rebase --apply`, **Then** the system executes the rebase using the planned order.

---

### User Story 4 - Constitutional Rule Enforcement (Priority: P2)
As a project maintainer, I want the system to scan my code changes against `constitution.md` rules using AST analysis, so that architectural violations (like logic in scripts/) are blocked before they are committed.

**Agent Interaction Flow**: Agent runs `dev.py analyze --const --json`. It processes the `violations` array in the JSON output to identify specific code lines that need refactoring to meet constitutional standards.
**Failure Recovery Path**: If `constitution.md` is malformed or missing, the scanner defaults to a strict "safe-only" mode and alerts the agent to restore the constitution file.

### User Story 5 - Automated Onboarding & Sync (Priority: P2)
As a developer switching to an old feature branch, I want the system to detect divergence from the canonical `orchestration-tools` and provide an interactive multi-select interface to sync environment scripts, ensuring I always use the latest validated tools while maintaining control over local changes.
- **Requirement**: Use SHA-256 hash comparison to verify toolset identity against the canonical branch.

**Agent Interaction Flow**: Agent executes `dev.py sync --json`. If divergence is detected, it selects all necessary updates automatically via `--answers '{"sync_all": true}'` to ensure the environment is ready.
**Failure Recovery Path**: If the remote `origin/orchestration-tools` is unreachable, the agent falls back to the last known-good local state and logs a "NETWORK_SYNC_WARNING".

### User Story 6 - Headless CI Governance (Priority: P1)

As a CI pipeline runner, I want to execute the Orchestration Core in a non-interactive mode using JSON payloads, allowing automated enforcement of the project constitution via a structured violation report.

**Agent Interaction Flow**: CI Agent runs `dev.py analyze --json --quiet`. It pipes the output to a security/governance gate that fails the build if the `risk_score` exceeds the threshold.
**Failure Recovery Path**: If the JSON output is truncated or invalid, the CI agent fails with a "MALFORMED_PAYLOAD" exit code 1 to prevent unsafe code from being merged.

### User Story 7 - Resilient Session Recovery (Priority: P3)

As a developer performing a complex 20-commit rebase, I want the system to persist my progress atomically after every step so that if the process is interrupted, I can resume from the exact point of failure without losing previous resolutions. The session state is temporary and is cleaned up automatically once the operation succeeds.

**Agent Interaction Flow**: Agent checks for `.dev_state.json` on startup. If found, it reads the `last_successful_step` and calls `dev.py resume --json` to continue the workflow.
**Failure Recovery Path**: If the state file is corrupted, the agent attempts to reconstruct the state from the Git history (e.g., current HEAD vs target branch) and notifies the user of the partial recovery.

**Acceptance Scenarios**:
1. **Given** a rebase in progress is killed, **When** I run `dev.py`, **Then** it detects the `.dev_state.json` and offers to resume.
2. **Given** a command finishes successfully, **When** I check the repository root, **Then** the `.dev_state.json` file has been deleted.



---

### User Story 8 - Branch Dependency Mapping (Priority: P2)

As a developer, I want to extract and compare the dependency graph (imports, function calls) between branches, so I can understand what refactoring was attempted and salvage incomplete work from outdated branches.

**Why this priority**: Critical for branch alignment — understanding architectural intent across branches enables informed merge decisions.

**Independent Test**: Create two branches with different import structures. Run `dev.py deps compare branch-a branch-b`. Verify the output shows added, removed, and moved dependencies.

**Agent Interaction Flow**: Agent runs `dev.py deps compare branch-a branch-b --json` to map relationships. It uses this to identify if a feature move was a simple relocation or a complex logic change.
**Failure Recovery Path**: If one branch has un-parseable Python files (syntax error), the agent receives a `SYNTAX_ERROR` in the `errors` array of the JSON report.

**Acceptance Scenarios**:
1. **Given** two branches, **When** I run `dev.py deps compare`, **Then** the system outputs a JSON report showing: {added: [...], removed: [...], moved: [...]}
2. **Given** a refactoring in progress (functions moved between modules), **When** I compare branches, **Then** the system identifies the refactoring pattern (move vs delete+create)

---

### User Story 9 - Commit Intent Analysis (Priority: P2)

As a developer, I want to understand what each commit was INTENDED to do vs what it ACTUALLY changed, so I can make informed decisions during branch alignment and identify commits that may have introduced issues.

**Why this priority**: Enables historical analysis of code changes — critical for debugging issues introduced in past merges.

**Independent Test**: Analyze a branch with 10 commits. Verify each commit is classified with: {intent: "...", actual_change_type: "...", risk_level: "low|medium|high"}.

**Agent Interaction Flow**: Agent runs `dev.py commit-classify --branch feat-x --json`. It iterates through the results to find commits tagged as "architectural_change" or "regression".
**Failure Recovery Path**: If a commit message is empty or "fixed", the agent uses the diff content to infer intent and tags it as "INFERRED_INTENT_LOW_CONFIDENCE".

**Acceptance Scenarios**:
1. **Given** a commit with message "fix bug", **When** analyzed, **Then** system identifies actual change type (e.g., "refactor", "new_feature", "bug_fix", "docs")
2. **Given** a commit that changed architecture (file moves, module restructure), **Then** system flags as "architectural_change"
3. **Given** a commit that deleted significant code without corresponding feature removal, **Then** system flags as potential "regression" or "incorrect_deletion"

---

### User Story 10 - Merge Artifact Detection (Priority: P1)

As a developer, I want the system to detect incomplete merges, conflict markers, and broken references, so I can clean them up before integration.

**Why this priority**: Core requirement for branch alignment — prevents merging broken code.

**Independent Test**: Create a file with `<<<<<<<`, `=======`, `>>>>>>>`. Run `dev.py scan --artifacts`. Verify all markers are detected with file:line.

**Agent Interaction Flow**: Agent runs `dev.py analyze --artifacts --json`. It parses the results and automatically applies fixes for trivial artifacts or requests user input for complex ones.
**Failure Recovery Path**: If artifact detection fails due to binary files, the system reports the binary files as "UNSCANNABLE" and suggests manual verification.

**Acceptance Scenarios**:
1. **Given** unmerged conflict markers in code, **When** scanned, **Then** report includes: {type: "conflict_marker", file, line, marker_type}
2. **Given** import from moved/renamed file, **When** scanned, **Then** report includes: {type: "broken_import", file, line, missing_module}
3. **Given** duplicate function/class definitions, **When** scanned, **Then** report includes: {type: "duplicate_def", file, line, symbol_name}

---

### User Story 11 - Change Classification (Priority: P2)

As a developer, I want each commit's changes classified as (architectural|docs|regression|error|merge_artifact|deletion), so I can identify problematic commits during integration.

**Why this priority**: Enables selective integration — skip or review specific commit types.

**Independent Test**: Run classification on a branch. Verify output groups commits by type with confidence scores.

**Agent Interaction Flow**: Agent executes `dev.py align --json` and uses the `commit_classification` section to filter out "documentation" changes from the rebase plan.
**Failure Recovery Path**: If a classification is ambiguous (confidence < 0.5), the agent marks it as "NEEDS_HUMAN_REVIEW" in its internal log.

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

**Agent Interaction Flow**: Agent runs `dev.py align branch-a main --json` to evaluate if a PR is ready to merge. It blocks the PR if `risk_score` is "high".
**Failure Recovery Path**: If alignment report generation takes too long (>30s), the system enters "timeout awareness" mode (FR-057) and provides a partial report.

**Acceptance Scenarios**:
1. **Given** two branches with minor differences, **Then** risk_score is "low" with "safe to merge" recommendation
2. **Given** branches with conflicting architectural changes, **Then** risk_score is "high" with specific conflict points listed
3. **Given** branch with outdated dependencies, **Then** report warns about "integration_issues"

---

### User Story 13 - Strategic Multi-Branch Orchestration (Multi-Branch Chess) (Priority: P1)

As a repository architect, I want to analyze all active feature branches simultaneously to identify redundant work, group related features, and determine the optimal sequence for merging PRs, so that I can minimize total conflict resolution effort and maintain architectural integrity across the entire project.

**Why this priority**: This is the "End Game" of repository orchestration. It enables high-velocity development by turning a chaotic set of branches into a structured merge pipeline.

**Independent Test**: Use a set of 5 divergent branches with known dependencies and overlaps. Run `dev.py align --batch`. Verify that the output includes a valid `MergeSchedule` where foundational dependencies merge before features, and redundant branches are flagged.

**Agent Interaction Flow**: Agent executes `dev.py align --batch --json`. It parses the `redundancy_alerts` to suggest branch consolidation and uses the `merge_sequence` to create a phased implementation plan for the user.
**Failure Recovery Path**: If circular dependencies are found between branches (Chess Stalemate), the agent receives a `CIRCULAR_DEPENDENCY` error with a list of the offending branches and suggestions for where to perform an "Atomic Decomposition" (FR-050) to break the loop.

**Acceptance Scenarios**:
1. **Given** N branches, **When** I run batch alignment, **Then** the system outputs a topologically sorted merge order and categorizes each branch by its primary target (main, scientific, tools).
2. **Given** two branches with 90% logic overlap, **When** I run batch alignment, **Then** the system flags them as "Duplicate Work" and suggests consolidation.

---

### User Story 16 - Targeted vs Untargeted Clustering (Priority: P2)

As a repository manager, I want to perform both targeted clustering (against a specific branch like `main`) and untargeted clustering (between all active branches), so that I can both plan specific merges and discover redundant feature development across the entire project.

**Independent Test**: Run `dev.py cluster --target scientific`. Verify output only shows clusters relevant to the scientific branch. Run `dev.py cluster --all`. Verify it identifies thematic groups across the whole repo.

**Agent Interaction Flow**: Agent runs `dev.py cluster --all --json` to identify intent clusters. It then runs `dev.py cluster --target main --json` to refine the merge schedule for the next release.

---

### User Story 14 - History Loop Detection & Fix Suggestion (Priority: P2)

As a developer, I want the system to identify "undo/redo" loops and recurring problematic commits (like incorrect folder moves), so that I can apply a "Clean Simple Fix" based on previously successful resolutions instead of manually untangling the history.

**Independent Test**: Create a branch where a folder is moved, then moved back, then modified. Run `dev.py analyze --history`. Verify the report identifies the "Move Loop" and suggests a single atomic move commit as the fix.

**Agent Interaction Flow**: Agent runs `dev.py analyze --patterns --json`. It checks the `resolution_templates` array. If a match is found for a `gitignore_leak`, it calls `dev.py resolve --template <id>` to apply the pre-validated fix.

**Acceptance Scenarios**:
1. **Given** a branch with redundant "flip-flop" commits, **When** analyzed, **Then** system flags the "Change Loop."
2. **Given** a known problematic commit pattern (e.g., destructive merge), **When** detected, **Then** system suggests a "Resolution Template" with a high confidence score.

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
  - **JSON Output**: `{"version": "1.0.0", "commands": ["analyze", "plan-rebase", ...], "global_options": ["--json", "--dry-run", "--enable-remote", ...]}`
  - **Exit Codes**: 0 (Success), 1 (Runtime Error), 2 (CLI/Usage Error)
  - **Error Format**: `{"code": "CLI_INIT_FAILED", "message": "Failed to initialize Typer app", "details": "...", "hint": "Check if typer is installed"}`
  - **Agent Prompt**: "List all available orchestration commands in dev.py in JSON format."

- **FR-002**: System MUST use `git merge-tree --real-merge` for conflict detection to ensure zero working-tree side effects.
  - **JSON Output**: `{"conflicts": [{"file": "src/main.py", "type": "content", "hunks": [...]}]}`
  - **Exit Codes**: 0 (No conflicts), 1 (Conflicts found), 2 (Git error)
  - **Error Format**: `{"code": "GIT_PLUMBING_ERROR", "message": "merge-tree failed", "details": "...", "hint": "Ensure git >= 2.38 is installed"}`
  - **Agent Prompt**: "Analyze merge conflicts between branch-a and branch-b using git merge-tree logic and return JSON."

- **FR-003**: System MUST implement a `HistoryService` that builds a DAG of commits and performs topological sorting for rebase planning.
  - **JSON Output**: `{"plan": [{"sha": "abc...", "action": "pick", "dependencies": [...]}]}`
  - **Exit Codes**: 0 (Success), 1 (DAG Error), 2 (Usage Error)
  - **Error Format**: `{"code": "CYCLE_DETECTED", "message": "Commit graph contains cycles", "details": "...", "hint": "Check for merge-rebase loops"}`
  - **Agent Prompt**: "Generate a topologically sorted rebase plan for the current branch in JSON."

- **FR-004**: System MUST implement an `ASTScanner` using the Python `ast` module to verify compliance with rules dynamically parsed from `constitution.md`.
  - **JSON Output**: `{"violations": [{"rule": "NO_LOGIC_IN_SCRIPTS", "file": "scripts/run.py", "line": 10}]}`
  - **Exit Codes**: 0 (No violations), 1 (Violations found), 2 (Scan error)
  - **Error Format**: `{"code": "SCAN_FAILED", "message": "AST parsing failed", "details": "...", "hint": "Check for syntax errors in source files"}`
  - **Agent Prompt**: "Scan the codebase for constitutional violations and return a JSON report."

- **FR-005**: System MUST use Pydantic models for all internal data exchange (Conflicts, CommitNodes, ExecutionPlans).
  - **JSON Output**: `{"model_schema": {...}, "data": {...}}`
  - **Exit Codes**: 0 (Success), 1 (Validation Error)
  - **Error Format**: `{"code": "VALIDATION_ERROR", "message": "Pydantic validation failed", "details": "...", "hint": "Ensure input matches model schema"}`
  - **Agent Prompt**: "Return the Pydantic schema for ConflictModel in JSON format."

- **FR-006**: System MUST replace existing placeholders in `src/cli/commands/` and `src/services/` with these functional implementations.
  - **JSON Output**: `{"audit": {"files_updated": 12, "placeholders_remaining": 0}}`
  - **Exit Codes**: 0 (Success), 1 (Audit failure)
  - **Error Format**: `{"code": "STUB_DETECTED", "message": "Placeholder remains in core logic", "details": "...", "hint": "Implement real logic in src/services/..."}`
  - **Agent Prompt**: "Audit the codebase for remaining stubs and report status in JSON."

- **FR-007**: System MUST support a `--dry-run` flag for all Git-mutating operations.
  - **JSON Output**: `{"dry_run": true, "intended_actions": [{"cmd": "git rebase...", "impact": "safe"}]}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "DRY_RUN_FAILED", "message": "Simulation failed", "details": "...", "hint": "Check permissions or branch existence"}`
  - **Agent Prompt**: "Run rebase with --dry-run and return the intended actions in JSON."

- **FR-008**: System MUST parse and execute `tasks.md` files, providing real-time status updates and logging.
  - **JSON Output**: `{"task_id": "T001", "status": "completed", "duration": "2.5s"}`
  - **Exit Codes**: 0 (All tasks pass), 1 (Task failed)
  - **Error Format**: `{"code": "TASK_EXEC_ERROR", "message": "Command exit code 127", "details": "...", "hint": "Check command path in tasks.md"}`
  - **Agent Prompt**: "Execute task T001 from tasks.md and return JSON status."

- **FR-009**: System MUST support a `--json` (headless) mode for all subcommands to allow agentic orchestration without interactive prompts.
  - **JSON Output**: `{"mode": "headless", "result": {...}}`
  - **Exit Codes**: Standard codes (0, 1, 2)
  - **Error Format**: `{"code": "HEADLESS_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Execute 'dev.py analyze' in JSON mode."

- **FR-010**: System MUST provide an `ide-init` command to generate IDE-specific configurations for VSCode, Antigravity, and Windsurf, mapping `tasks.md` to IDE task runners.
  - **JSON Output**: `{"files_generated": [".vscode/tasks.json", ...], "status": "success"}`
  - **Exit Codes**: 0 (Success), 1 (Template error)
  - **Error Format**: `{"code": "IDE_CONFIG_ERROR", "message": "Template rendering failed", "details": "...", "hint": "Check Jinja2 templates in src/core/templates/"}`
  - **Agent Prompt**: "Initialize IDE configurations for Windsurf based on tasks.md in JSON."

- **FR-011**: System MUST implement progressive disclosure output with four modes: (a) `--quiet` (minimal output, suppresses Rich styling/Token-Saver), (b) `--normal` (default), (c) `--verbose` (debug logs), (d) `--json` (structured machine-parseable output).
  - **JSON Output**: `{"output_mode": "json", "data": {...}}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "OUTPUT_ERROR", "message": "Failed to format output", "details": "...", "hint": "Check if output is redirectable"}`
  - **Agent Prompt**: "Run dev.py with --quiet to minimize token usage."

- **FR-012**: System MUST allow pre-answering interactive prompts via a `--answers` JSON input to enable fully non-interactive agentic flows.
  - **JSON Output**: `{"answers_applied": ["sync_all", "overwrite_config"], "status": "success"}`
  - **Exit Codes**: 0 (Success), 1 (Invalid answers)
  - **Error Format**: `{"code": "INVALID_ANSWERS", "message": "Missing required answer: 'branch_name'", "details": "...", "hint": "Provide all required answers in the JSON input"}`
  - **Agent Prompt**: "Execute sync command with pre-provided answers for all prompts in JSON."

- **FR-013**: System MUST use SHA-256 hash comparison to detect divergence between local environment files and the `origin/orchestration-tools` remote branch.
  - **JSON Output**: `{"divergence": [{"file": "scripts/setup.sh", "local_sha": "abc...", "remote_sha": "def...", "status": "diverged"}]}`
  - **Exit Codes**: 0 (In sync), 1 (Diverged), 2 (Remote error)
  - **Error Format**: `{"code": "REMOTE_UNREACHABLE", "message": "Failed to fetch origin/orchestration-tools", "details": "...", "hint": "Check network connection or git remote config"}`
  - **Agent Prompt**: "Check for toolset divergence against the canonical branch in JSON."

- **FR-014**: System MUST persist session state atomically to `.dev_state.json` after every successful action/step to maximize crash recovery resilience. The file MUST be deleted upon successful completion of the entire command/workflow.
  - **JSON Output**: `{"session_id": "uuid-...", "last_step": 5, "state": "saved"}`
  - **Exit Codes**: 0 (Success), 1 (IO Error)
  - **Error Format**: `{"code": "STATE_SAVE_FAILED", "message": "Disk full or permission denied", "details": "...", "hint": "Check write permissions in repo root"}`
  - **Agent Prompt**: "Retrieve the current session state from .dev_state.json in JSON."

- **FR-015**: System MUST generate a structured JSON violation report (Rule, File, Line, Snippet) delivered via stdout for constitutional violations detected by the AST scanner.
  - **JSON Output**: `{"violations": [{"rule": "X", "file": "Y", "line": 1, "snippet": "...", "severity": "error"}]}`
  - **Exit Codes**: 0 (Clean), 1 (Violations)
  - **Error Format**: `{"code": "REPORT_GEN_FAILED", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Generate a detailed violation report for the latest scan in JSON."

- **FR-016**: System MUST provide an interactive multi-select interface for `dev.py sync` to allow users to choose which diverged files to overwrite from the canonical source.
  - **JSON Output**: `{"selected_files": ["scripts/A.sh", "scripts/B.sh"], "action": "overwrite"}`
  - **Exit Codes**: 0 (Success), 1 (Cancel)
  - **Error Format**: `{"code": "SYNC_SELECTION_ERROR", "message": "No files selected", "details": "...", "hint": "Select at least one file or use --answers to automate"}`
  - **Agent Prompt**: "Perform a tool sync and select all diverged files for update in JSON."

- **FR-017**: System MUST implement `dev.py install-hooks` to automatically configure git pre-commit hooks that enforce constitutional rules, renaming existing hooks to `.bak` if they exist.
  - **JSON Output**: `{"hooks_installed": ["pre-commit"], "backups_created": [".git/hooks/pre-commit.bak"]}`
  - **Exit Codes**: 0 (Success), 1 (Permission Error)
  - **Error Format**: `{"code": "HOOK_INSTALL_FAILED", "message": "Cannot write to .git/hooks", "details": "...", "hint": "Run with appropriate permissions"}`
  - **Agent Prompt**: "Install constitutional git hooks and report backups in JSON."

- **FR-018**: System MUST implement `dev.py schema` to output JSON schemas for all internal Pydantic models to support CI integration.
  - **JSON Output**: `{"schemas": {"ConflictModel": {...}, "CommitNode": {...}}}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "SCHEMA_GEN_FAILED", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Output JSON schemas for all core data models."

- **FR-019**: System MUST implement `dev.py deps extract` to build a dependency graph (imports, function calls) from the codebase using AST analysis.
  - **JSON Output**: `{"graph": {"nodes": [{"id": "mod1", "type": "module"}], "edges": [{"source": "mod1", "target": "mod2", "type": "import"}]}}`
  - **Exit Codes**: 0 (Success), 1 (Analysis Error)
  - **Error Format**: `{"code": "DEPS_EXTRACT_FAILED", "message": "Cyclic dependency or malformed code", "details": "...", "hint": "Check for circular imports"}`
  - **Agent Prompt**: "Extract the codebase dependency graph in JSON format."

- **FR-020**: System MUST implement `dev.py deps compare <branch-a> <branch-b>` to output JSON report showing {added: [...], removed: [...], moved: [...], refactored: [...]} between branches.
  - **JSON Output**: `{"comparison": {"added": ["new_func"], "removed": [], "moved": [{"from": "old", "to": "new"}]}}`
  - **Exit Codes**: 0 (Success), 1 (Branch missing)
  - **Error Format**: `{"code": "BRANCH_NOT_FOUND", "message": "Branch 'branch-b' does not exist", "details": "...", "hint": "Ensure both branches are fetched"}`
  - **Agent Prompt**: "Compare dependencies between branch-a and branch-b and return JSON."

- **FR-021**: System MUST implement `dev.py analyze --artifacts` to detect merge artifacts including: conflict markers, broken imports, duplicate definitions, orphaned exports.
  - **JSON Output**: `{"artifacts": [{"type": "conflict_marker", "file": "src/app.py", "line": 42}]}`
  - **Exit Codes**: 0 (Clean), 1 (Artifacts found)
  - **Error Format**: `{"code": "SCAN_ERROR", "message": "Failed to scan artifacts", "details": "...", "hint": "Check file permissions"}`
  - **Agent Prompt**: "Scan for merge artifacts in the current branch and return JSON."

- **FR-022**: System MUST implement `dev.py commit-classify` to analyze each commit and classify change type: (architectural|refactor|bug_fix|docs|regression|merge_artifact|deletion).
  - **JSON Output**: `{"commits": [{"sha": "abc", "classification": "bug_fix", "confidence": 0.95}]}`
  - **Exit Codes**: 0 (Success), 1 (Classification failed)
  - **Error Format**: `{"code": "CLASSIFY_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Classify the latest 10 commits on the current branch in JSON."

- **FR-023**: System MUST implement `dev.py align <branch-a> <branch-b>` to generate comprehensive alignment report including: divergence summary, dependency diff, commit classifications, risk score (low/medium/high), and merge recommendations.
  - **JSON Output**: `{"alignment_report": {"risk_score": "medium", "recommendation": "merge with review", "divergence": {...}}}`
  - **Exit Codes**: 0 (Success), 1 (Alignment failed)
  - **Error Format**: `{"code": "ALIGN_FAILED", "message": "Branches are too divergent", "details": "...", "hint": "Manual merge required"}`
  - **Agent Prompt**: "Generate a branch alignment report between feat-x and main in JSON."

- **FR-024**: System MUST use ast-grep (via Python API or CLI) for structural dependency extraction to accurately identify function calls, class definitions, and import relationships.
  - **JSON Output**: `{"structural_deps": [{"symbol": "User", "type": "class", "references": [...]}]}`
  - **Exit Codes**: 0 (Success), 1 (ast-grep error)
  - **Error Format**: `{"code": "AST_GREP_ERROR", "message": "ast-grep binary not found", "details": "...", "hint": "Install ast-grep CLI"}`
  - **Agent Prompt**: "Extract structural dependencies using ast-grep and return JSON."

- **FR-025**: System MUST implement CLI architecture using CommandFactory + CommandRegistry pattern for modular, extensible command registration with dependency injection support (cherry-picked from consolidate/cli-unification).
  - **JSON Output**: `{"registry": {"commands": ["analyze", "sync"], "factories": ["GitFactory", ...]}}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "REGISTRY_ERROR", "message": "Command collision", "details": "...", "hint": "Ensure unique command names"}`
  - **Agent Prompt**: "List registered CLI commands and their factories in JSON."

- **FR-026**: System MUST implement GitLogParser to parse git log output into structured Commit objects (cherry-picked from feat-emailintelligence-cli-v2.0).
  - **JSON Output**: `{"commits": [{"sha": "abc", "author": "...", "message": "...", "files_changed": [...]}]}`
  - **Exit Codes**: 0 (Success), 1 (Git error)
  - **Error Format**: `{"code": "LOG_PARSE_ERROR", "message": "Malformed git log output", "details": "...", "hint": "Verify git log format"}`
  - **Agent Prompt**: "Parse the git log into structured JSON objects."

- **FR-027**: System MUST implement CommitClassifier with conventional commit parsing and risk keyword detection (cherry-picked from feat-emailintelligence-cli-v2.0).
  - **JSON Output**: `{"classification": {"sha": "abc", "is_conventional": true, "risk_keywords": ["TODO", "FIXME"]}}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "CONVENTIONAL_PARSE_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Analyze the risk level of the current commit history in JSON."

- **FR-028**: System MUST implement RebasePlanner with topological sorting and priority-based commit reordering (cherry-picked from feat-emailintelligence-cli-v2.0).
  - **JSON Output**: `{"rebase_plan": {"ordered_shas": ["abc", "def"], "conflicts_predicted": []}}`
  - **Exit Codes**: 0 (Success), 1 (Planning error)
  - **Error Format**: `{"code": "PLAN_REBASE_ERROR", "message": "Dependency cycle in commits", "details": "...", "hint": "Check for cross-branch dependencies"}`
  - **Agent Prompt**: "Create a priority-based rebase plan in JSON."

- **FR-029**: System MUST implement cross-branch commit analysis to identify shared problematic commits (same SHA or similar change pattern) across multiple branches, with deduplication and merge/rebase recommendations.
  - **JSON Output**: `{"shared_problematic_commits": [{"sha": "abc", "branches": ["feat-1", "feat-2"], "reason": "broken_test"}]}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "CROSS_BRANCH_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Identify shared problematic commits across all active feature branches in JSON."

- **FR-030**: System MUST provide fix/avoidance options for identified problematic commits including: (a) skip commit during rebase, (b) squash into parent, (c) cherry-pick only safe commits, (d) mark for review before merge.
  - **JSON Output**: `{"commit_options": {"abc": ["skip", "squash", "cherry-pick"]}}`
  - **Exit Codes**: 0 (Success), 1 (Invalid option)
  - **Error Format**: `{"code": "FIX_OPTION_ERROR", "message": "Option 'squash' not available for merge commits", "details": "...", "hint": "Use 'skip' or manual resolution"}`
  - **Agent Prompt**: "List avoidance options for problematic commit 'abc' in JSON."

- **FR-031**: System MUST implement directory structure comparison between branches to calculate structural similarity percentage.
  - **JSON Output**: `{"structural_similarity": {"percentage": 85.5, "major_changes": ["/src/new_module"]}}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "DIR_COMP_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Compare directory structures between branches and return similarity score in JSON."

- **FR-032**: System MUST implement filename similarity detection using fuzzy matching to identify renamed files across branches.
  - **JSON Output**: `{"renames": [{"from": "old_name.py", "to": "new_name.py", "confidence": 0.92}]}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "FUZZY_MATCH_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Detect renamed files between branches using fuzzy matching and return JSON."

- **FR-033**: System MUST implement content-level diff analysis to identify added, removed, and modified files.
  - **JSON Output**: `{"diff_summary": {"added": 5, "removed": 2, "modified": 10}}`
  - **Exit Codes**: 0 (Success), 1 (Diff failed)
  - **Error Format**: `{"code": "DIFF_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Get a content-level diff summary between branches in JSON."

- **FR-034**: System MUST use pyastsim library for AST-based structural similarity detection between Python files.
  - **JSON Output**: `{"ast_similarity": {"file_a": "mod1.py", "file_b": "mod2.py", "score": 0.88}}`
  - **Exit Codes**: 0 (Success), 1 (Library missing)
  - **Error Format**: `{"code": "PYASTSIM_ERROR", "message": "pyastsim not installed", "details": "...", "hint": "Run pip install pyastsim"}`
  - **Agent Prompt**: "Calculate AST structural similarity between two files and return JSON."

- **FR-035**: System MUST integrate with gkg (git knowledge graph) for code structure analysis and generate parquet-based dependency graphs for branch comparison.
  - **JSON Output**: `{"gkg_report": {"graph_path": ".dev_state/deps.parquet", "node_count": 150}}`
  - **Exit Codes**: 0 (Success), 1 (gkg error)
  - **Error Format**: `{"code": "GKG_INTEGRATION_ERROR", "message": "gkg failed to generate graph", "details": "...", "hint": "Ensure gkg is in PATH"}`
  - **Agent Prompt**: "Generate a gkg dependency graph for the current repository in JSON."

- **FR-036**: System SHOULD implement BM25-based text similarity scoring for comparing code comments, docstrings, and commit messages between branches.
  - **JSON Output**: `{"bm25_scores": [{"item": "docstring_x", "similarity": 0.75}]}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "BM25_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Compare docstrings between branches using BM25 and return JSON scores."

- **FR-037**: System SHOULD implement sentence embedding-based semantic search for code documentation analysis between branches, using lightweight embeddings (e.g., sentence-transformers with a small model).
  - **JSON Output**: `{"semantic_search": {"query": "...", "matches": [{"file": "...", "score": 0.9}]}}`
  - **Exit Codes**: 0 (Success), 1 (Model error)
  - **Error Format**: `{"code": "EMBEDDING_ERROR", "message": "Model not loaded", "details": "...", "hint": "Check sentence-transformers installation"}`
  - **Agent Prompt**: "Perform semantic search for documentation across branches and return JSON."

- **FR-038**: System MUST implement dynamic rule parsing from `constitution.md` by identifying sections marked with "## Rule:" or "### Forbidden:" followed by pattern definitions (regex or AST patterns).
  - **JSON Output**: `{"parsed_rules": [{"id": "RULE_01", "pattern": "...", "type": "ast"}]}`
  - **Exit Codes**: 0 (Success), 1 (Parse error)
  - **Error Format**: `{"code": "RULE_PARSE_ERROR", "message": "Invalid rule syntax in constitution.md", "details": "...", "hint": "Follow the '## Rule: ID' format"}`
  - **Agent Prompt**: "Parse dynamic rules from constitution.md and return JSON."

- **FR-039**: System MUST use ast-grep CLI via subprocess for structural pattern matching when enforcing constitutional rules, with JSON output parsing for violation reporting.
  - **JSON Output**: `{"ast_grep_violations": [{"rule": "X", "matches": [...]}]}`
  - **Exit Codes**: 0 (Success), 1 (ast-grep error)
  - **Error Format**: `{"code": "AST_GREP_EXEC_ERROR", "message": "ast-grep crashed", "details": "...", "hint": "Check ast-grep version"}`
  - **Agent Prompt**: "Run ast-grep structural matching for constitutional rules and return JSON."

- **FR-040**: System MUST implement task execution engine that parses `tasks.md` checkbox format and supports: (a) shell command execution, (b) file edit operations, (c) git operations, (d) conditional branching based on exit codes.
  - **JSON Output**: `{"task_engine": {"task_id": "T001", "operations": ["shell", "git"], "status": "running"}}`
  - **Exit Codes**: 0 (Success), 1 (Task failure)
  - **Error Format**: `{"code": "TASK_ENGINE_ERROR", "message": "Operation 'file_edit' failed", "details": "...", "hint": "Check file path and permissions"}`
  - **Agent Prompt**: "Run the task engine for the current tasks.md and return JSON progress."

- **FR-041**: System MUST implement IDE task file generation that maps `tasks.md` entries to VSCode `.vscode/tasks.json`, Antigravity `antigravity.tasks.json`, and Windsurf `.windsurf/tasks.json` formats.
  - **JSON Output**: `{"ide_tasks": {"vscode": true, "antigravity": true, "windsurf": true}}`
  - **Exit Codes**: 0 (Success), 1 (Write error)
  - **Error Format**: `{"code": "IDE_WRITE_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Generate IDE task configurations for all supported IDEs in JSON."

- **FR-042**: System MUST implement interactive resolution UX for FR-030 fix options using a numbered list selection interface (1-4) with preview of each option's impact before execution.
  - **JSON Output**: `{"resolution_preview": {"option": 1, "impact": "Commit abc will be skipped"}}`
  - **Exit Codes**: 0 (Success), 1 (Selection error)
  - **Error Format**: `{"code": "PREVIEW_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Preview the impact of rebase resolution option 1 in JSON."

- **FR-043**: System MUST integrate pydriller library for commit topology analysis, enabling DAG traversal, reachability checks, and commit relationship mapping.
  - **JSON Output**: `{"topology": {"reachable": true, "distance": 5, "is_ancestor": true}}`
  - **Exit Codes**: 0 (Success), 1 (Library error)
  - **Error Format**: `{"code": "PYDRILLER_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Analyze commit topology between HEAD and main using pydriller in JSON."

- **FR-044**: System MUST implement problematic commit detection including: WIP commits (starts with WIP, draft, temp), large diffs (>1000 lines), many files (>10), merge commits, revert commits, and breaking changes.
  - **JSON Output**: `{"problematic_commits": [{"sha": "abc", "reasons": ["WIP", "large_diff"]}]}`
  - **Exit Codes**: 0 (Clean), 1 (Issues found)
  - **Error Format**: `{"code": "DETECTION_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Detect problematic commits in the current PR branch and return JSON."

- **FR-045**: System MUST generate topology risk assessment report showing commit risk scores, conflict probability, and rebase complexity estimation based on commit graph analysis.
  - **JSON Output**: `{"risk_assessment": {"complexity": "high", "conflict_prob": 0.8, "risk_score": 75}}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "ASSESSMENT_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Generate a topology risk assessment for the upcoming rebase in JSON."

- **FR-046**: System SHOULD integrate git-graphable for hygiene analysis including direct pushes to protected branches, back-merge detection, and contributor patterns.
  - **JSON Output**: `{"hygiene_report": {"direct_pushes": 0, "back_merges": 2, "hygiene_score": 90}}`
  - **Exit Codes**: 0 (Success), 1 (Tool missing)
  - **Error Format**: `{"code": "GIT_GRAPHABLE_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Analyze repository hygiene using git-graphable and return JSON report."

- **FR-047**: System MUST implement analysis cache with SHA-based validation. Cache branch analysis results to `.dev_state/analysis_cache/{branch}__{sha}.json` to enable fast cross-branch comparison without re-analysis. Cache must invalidate when branch SHA changes.
  - **JSON Output**: `{"cache_status": "hit", "cache_file": "..."}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "CACHE_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Check analysis cache status for branch-x in JSON."

- **FR-048**: System MUST implement ML-based branch clustering using AgglomerativeClustering with Ward linkage to categorize branches by similarity (name patterns, commit history, dependency graphs). This enables intelligent branch grouping and identification of related feature branches for batch operations.
  - **JSON Output**: `{"clusters": [{"id": 0, "branches": ["feat-a", "feat-b"], "centroid_summary": "..."}]}`
  - **Exit Codes**: 0 (Success), 1 (ML Error)
  - **Error Format**: `{"code": "CLUSTERING_ERROR", "message": "Insufficient data for clustering", "details": "...", "hint": "Analyze more branches first"}`
  - **Agent Prompt**: "Cluster active feature branches by similarity and return JSON."

- **FR-049**: System MUST implement coarse-level alignment analysis comparing git histories between two branches. For each divergence point, the system MUST identify changes as either: (a) Simple changes: path renames, import updates, test updates, documentation reorg, deletion with clear justification; or (b) Complex changes: logic modifications requiring full topology comparison. Output MUST include a classification for each changed file.
  - **JSON Output**: `{"alignment_analysis": [{"file": "src/old.py", "classification": "simple", "reason": "rename"}]}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "ALIGN_ANALYSIS_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Perform coarse-level alignment analysis between branch-a and branch-b in JSON."

- **FR-050**: System MUST implement atomic change decomposition for complex alignments. When a complex alignment is detected (e.g., feature moved from one location to another), the system MUST decompose it into smaller, atomic steps: (1) copy/move source to destination, (2) update all import references, (3) add redirect or delete source, (4) update dependent tests, (5) update documentation. Each atomic step MUST be a separate, replayable rebase commit.
  - **JSON Output**: `{"atomic_steps": [{"step": 1, "description": "move src to dest", "cmd": "mv ..."}]}`
  - **Exit Codes**: 0 (Success), 1 (Decomposition failed)
  - **Error Format**: `{"code": "DECOMP_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Decompose complex alignment between branch-a and branch-b into atomic steps in JSON."

- **FR-051**: System MUST implement justification tracking for deletions and path changes, similar to git rerere but enhanced with intent reasoning. For each deletion: record why it was deleted (refactored to X, obsolete, merged). For each path change: record the reason (consistency, module reorg). The system SHOULD learn from commit messages and code patterns to auto-suggest justifications for future alignments.
  - **JSON Output**: `{"justification": {"path": "...", "reason": "refactor", "confidence": 0.85}}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "JUSTIFY_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Provide justification for the deleted file 'src/old.py' in JSON."

- **FR-052**: System MUST implement shell completion support using typer's built-in completion system for bash, zsh, fish, and PowerShell shells. The command `dev.py --install-completion [shell]` MUST auto-detect the current shell if no argument is provided and install the appropriate completion script to the standard completion directory.
  - **JSON Output**: `{"completion": {"shell": "zsh", "path": "/usr/local/share/zsh/site-functions/_dev.py"}}`
  - **Exit Codes**: 0 (Success), 1 (Unsupported shell)
  - **Error Format**: `{"code": "SHELL_NOT_SUPPORTED", "message": "Shell 'ksh' not supported", "details": "...", "hint": "Use bash, zsh, fish, or powershell"}`
  - **Agent Prompt**: "Install shell completion for zsh in JSON."

- **FR-053**: System MUST implement interactive wizard patterns using InquirerPy for guided workflows. Commands that benefit from step-by-step guidance (e.g., first-time setup, branch selection) MUST support a `--wizard` flag that launches an interactive multi-step wizard. Example: `dev.py init --wizard` for first-time repository setup.
  - **JSON Output**: `{"wizard_state": {"step": 2, "total_steps": 5, "current_input": "branch_a"}}`
  - **Exit Codes**: 0 (Success), 1 (Aborted)
  - **Error Format**: `{"code": "WIZARD_ABORTED", "message": "User cancelled wizard", "details": "...", "hint": "Run without --wizard for non-interactive mode"}`
  - **Agent Prompt**: "Start the repository initialization wizard in JSON."

- **FR-054**: System MUST implement command aliases for frequently used commands. Aliases MUST be documented in `--help` output under an "Aliases" section. Examples: `dev.py br` → `dev.py branch`, `dev.py an` → `dev.py analyze`. The system MUST validate that aliases do not conflict with existing commands or other aliases.
  - **JSON Output**: `{"aliases": {"br": "branch", "an": "analyze"}}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "ALIAS_CONFLICT", "message": "Alias 'br' conflicts with existing command", "details": "...", "hint": "Choose a different alias name"}`
  - **Agent Prompt**: "List all available command aliases in JSON."

- **FR-055**: [Merged into FR-011]

- **FR-056**: System MUST implement environment variable overrides for output modes. Supported env vars: `DEV_JSON=1` enables JSON output mode, `DEV_QUIET=1` enables quiet mode, `DEV_VERBOSE=1` enables verbose mode. Priority order: CLI flag > environment variable > config file > defaults.
  - **JSON Output**: `{"env_overrides": {"DEV_JSON": "1", "active_mode": "json"}}`
  - **Exit Codes**: 0 (Success)
  - **Error Format**: `{"code": "ENV_PARSE_ERROR", "message": "...", "details": "...", "hint": "..."}`
  - **Agent Prompt**: "Check active environment variable overrides for output modes in JSON."

- **FR-057**: System MUST implement time estimation and timeout awareness for all analysis operations.
  - **JSON Output**: `{"estimation": {"estimated_seconds": 45, "complexity": "O(N*M)", "timeout_threshold": 60}}`
  - **Exit Codes**: 0 (Success), 1 (Timeout)
  - **Error Format**: `{"code": "TIMEOUT_EXCEEDED", "message": "Analysis exceeded 60s", "details": "...", "hint": "Use --quiet or cached results"}`
  - **Agent Prompt**: "Get a time estimation for analyzing 500 commits in JSON."

- **FR-058**: System MUST implement an **Optimal Merge Sequencer** that analyzes a set of N branches/PRs and outputs a topological merge order that minimizes total conflict resolution effort based on cross-branch dependency and conflict matrices.
  - **JSON Output**: `{"merge_sequence": ["feat-foundational", "feat-implementation", "feat-ui"], "conflict_matrix": {...}, "blockers": []}`
  - **Exit Codes**: 0 (Sequence found), 1 (Circular dependency), 2 (Analysis error)
  - **Agent Prompt**: "Determine the optimal merge order for the following 5 PR branches in JSON."

- **FR-059**: System MUST implement an **Intent Overlap Detector** using BM25 and AST similarity to identify potentially redundant or duplicate work across divergent feature branches.
  - **JSON Output**: `{"redundancy_alerts": [{"branches": ["feat-a", "feat-b"], "overlap_score": 0.88, "common_logic": ["auth_service.py"]}]}`
  - **Exit Codes**: 0 (Clean), 1 (Overlap detected)
  - **Agent Prompt**: "Scan all active feature branches for duplicate or overlapping work in JSON."

### External Tools (Required)
| Tool | Purpose | FR |
|------|---------|-----|
| `gkg` | Git knowledge graph | FR-035 |
| `ast-grep` | Structural pattern matching | FR-039 |
| `pydriller` | Commit topology analysis | FR-043 |


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
- **SC-005**: All code violations defined in `constitution.md` are detected with 95% accuracy by the AST scanner, measured against a gold-standard set of 100 violation fixtures.
- **SC-006**: BM25 similarity scoring completes for 1000 document pairs in under 2 seconds.
- **SC-007**: AST similarity detection using pyastsim returns results within 500ms per file pair.
- **SC-008**: gkg dependency graph generation completes for repositories up to 10,000 files in under 30 seconds.
- **SC-009**: Batch alignment for up to 10 branches produces a valid, conflict-minimized `MergeSchedule` in under 60 seconds.

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
| `networkx` | DAG analysis and Multi-Branch Chess engine | FR-003, FR-058 |
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