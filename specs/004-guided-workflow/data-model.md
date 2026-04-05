# Data Model: Orchestration Core

## Commit & History Entities

### `CommitNode`
Represents a single commit in the repository DAG.
- `sha`: string (Unique ID)
- `parents`: list[string] (Parent SHAs)
- `author`: string
- `message`: string
- `classification`: enum (feature, bug_fix, refactor, docs, regression, merge_artifact, deletion)
- `confidence`: float (0.0 to 1.0)
- `dependencies`: list[string] (SHAs this commit depends on based on AST analysis)
- `logic_signature`: string (Hash of the AST structure for move detection)

### `HistoryPlan`
The result of a rebase planning operation.
- `ordered_shas`: list[string] (Topologically sorted commits)
- `risk_score`: float
- `conflicts_predicted`: list[ConflictModel]

## Conflict & Analysis Entities

### `ConflictModel`
Represents a detected merge conflict.
- `file_path`: string
- `type`: enum (content, delete_modify, rename_add)
- `hunks`: list[HunkModel]
- `base_oid`: string
- `our_oid`: string
- `their_oid`: string

### `DependencyGraph`
The codebase relationship map.
- `nodes`: list[ModuleNode]
- `edges`: list[DependencyEdge]
- `metadata`: dict (Analysis duration, timestamp)

## Macro Orchestration Entities (Multi-Branch Chess)

### `SimilarityMatrix`
Stores the N x N relationship scores between a set of branches.
- `branches`: list[string] (Ordered list of branch names)
- `scores`: list[list[float]] (Similarity matrix)
- `metrics`: list[string] (Metrics used: AST, BM25, Path, etc.)

### `BranchCluster`
Represents a thematic group of branches identified by ML.
- `cluster_id`: int
- `members`: list[string] (Branch names)
- `centroid_description`: string (Thematic summary of the group)
- `silhouette_score`: float (Quality of the clustering)

### `MergeSchedule`
The topologically sorted sequence for merging multiple PRs.
- `sequence`: list[string] (Ordered branch names)
- `blockers`: list[dict] (Dependencies preventing earlier merge)
- `total_conflict_risk`: float
- `graph_metadata`: dict (Centrality and reachability metrics from NetworkX)

## Problematic Pattern & Resolution Entities

### `ProblematicPattern`
Represents a recurring architectural or history error (e.g., Undo/Redo loops).
- `pattern_id`: string
- `type`: enum (undo_redo_loop, incorrect_move, destructive_merge, gitignore_leak)
- `topological_signature`: string (Graph hash of the offending commits)
- `affected_paths`: list[string]

### `ResolutionTemplate`
A "Clean Simple Fix" mapped to a known problematic pattern.
- `template_id`: string
- `pattern_id`: string (Link to ProblematicPattern)
- `strategy`: enum (squash_and_revert, path_realignment, dependency_fix)
- `success_count`: int
- `automated_apply_cmd`: string (The dev.py command to fix it)

## Constitutional Governance Entities

### `ConstitutionalRule`
A rule parsed from `constitution.md`.
- `id`: string
- `description`: string
- `target_paths`: list[string] (Globs)
- `prohibited_patterns`: list[string] (AST or Regex)
- `severity`: enum (error, warning)

### `Violation`
A detected violation of a constitutional rule.
- `rule_id`: string
- `file_path`: string
- `line_number`: int
- `snippet`: string
- `message`: string

## Orchestration & Session Entities

### `Session`
The atomic state of a long-running command.
- `session_id`: uuid
- `command`: string
- `args`: list[string]
- `start_time`: datetime
- `last_step_index`: int
- `status`: enum (running, paused, completed, failed)
- `data`: dict (Command-specific context)

### `TaskItem`
A single entry from `tasks.md`.
- `id`: string (e.g., T001)
- `title`: string
- `status`: enum (pending, in_progress, completed, failed)
- `commands`: list[string]
- `exit_code`: int (optional)
- `logs`: list[string] (Paths to log files)
