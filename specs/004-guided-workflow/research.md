# Research: Orchestration Core & Guided Workflows

## High-Rigor Git Analysis

### Decision: in-memory conflict detection via `git merge-tree`
- **Decision**: Use `git merge-tree --real-merge` for conflict detection.
- **Rationale**: The core requirement (US2) is to analyze conflicts without modifying the working tree. `merge-tree` (available in Git 2.38+) allows calculating a merge result and identifying conflicts purely in the object database.
- **Alternatives considered**: 
    - `git checkout` to a temporary branch and merging: Rejected as it triggers hooks and disrupts user workflow.
    - `GitPython` high-level API: Rejected as it often relies on porcelain commands that touch the index.

### Decision: Topological Sorting via Kahn's Algorithm
- **Decision**: Implement topological sorting using Kahn's algorithm for rebase planning (US3).
- **Rationale**: Kahn's algorithm is efficient ($O(V+E)$) and easily allows for cycle detection, which is critical for identifying illegal commit dependencies.
- **Alternatives considered**: DFS-based topological sort.

## Constitutional Enforcement (AST Scanning)

### Decision: Structural Pattern Matching via `ast-grep` and Python `ast`
- **Decision**: Use `ast-grep` for high-speed structural searches and the standard Python `ast` module for fine-grained rule validation (e.g., US4).
- **Rationale**: `ast-grep` is exceptionally fast for project-wide scans, while Python's `ast` allows for complex logical checks (like class inheritance or decorator presence) that are difficult to express in simple patterns.
- **Alternatives considered**: Regex-based scanning (Rejected as too fragile).

## Machine Intelligence & Clustering

### Decision: Agglomerative Clustering for Branch Grouping
- **Decision**: Use `scikit-learn`'s `AgglomerativeClustering` with Ward linkage (FR-048).
- **Rationale**: Ward's method minimizes the variance within clusters, which is ideal for grouping branches that share similar commit histories or dependency changes. It doesn't require pre-specifying the number of clusters (via distance threshold).
- **Alternatives considered**: K-Means (Requires pre-defining $k$).

### Decision: BM25 for Text Similarity
- **Decision**: Use `rank-bm25` for comparing documentation and commit messages (FR-036).
- **Rationale**: BM25 is the industry standard for lightweight, non-vectorized text similarity. It is much faster than running LLM embeddings for thousands of document pairs and requires no external API.
- **Alternatives considered**: TF-IDF (less robust to document length variation).

## Resilience & Session Management

### Decision: Atomic JSON State with Ephemeral Lifecycle
- **Decision**: Store session state in `.dev_state.json` using atomic writes (tmp + rename). Automatically delete the file on successful completion.
- **Rationale**: Prevents partial state corruption during crashes. Auto-cleanup ensures the environment doesn't accumulate stale state files.
- **Alternatives considered**: SQLite (Too heavy for simple task state).
