# Research Summary: Git Topology & Conflict Tools

## 1. Discovered Script Logic (.taskmaster)

### Investigative Tools
- `.taskmaster/scripts/analyze_git_history.py`: Categorizes git commit history and filters "orchestration noise".
- `.taskmaster/scripts/partial_cherry_pick.py`: Selective cherry-picking tool.
- `.taskmaster/scripts/inject_markers.py`: Manual conflict marker injection.

### Resolution Framework
- `.taskmaster/src/resolution/auto_resolver.py`: Orchestrates automatic conflict resolution.
- `.taskmaster/src/resolution/semantic_merger.py`: AST-aware merging logic.
- `.taskmaster/src/strategy/generator.py`: Generates resolution strategies based on conflict patterns.
- `.taskmaster/src/core/conflict_models.py`: Rich data models for representing Semantic, Logical, and Architectural conflicts.

## 2. Graph Analysis Integration (NetworkX & GraphQL)

### NetworkX
- **Existing Usage**: Already integrated into `src/backend/node_engine/node_base.py` for workflow graph operations and topological sorting.
- **Potential**: Can be extended to model git commit topology as a Directed Acyclic Graph (DAG) to find merge bases, detect complex divergence patterns, and calculate "Distance" between branches.

### Git GraphQL
- **Purpose**: To fetch rich commit metadata (PR descriptions, reviews, labels) directly from GitHub without cloning entire histories if not needed.
- **Integration**: Can be used to populate the `ConflictBlock` and `Conflict` models with "Intent" data from PR discussions.

## 3. Recommended Tool Extensions

- **TopologyMapper Command**: A new CLI command that uses NetworkX to visualize and analyze the commit graph.
- **LogicDriftAnalyzer**: A wrapper around `logic-compare` that specifically looks for semantic drift in diverged branches.
- **Disentanglement Engine**: Porting the `auto_resolver.py` logic into the unified CLI to handle multi-branch synchronization.
