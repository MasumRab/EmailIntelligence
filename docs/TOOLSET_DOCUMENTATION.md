# Toolset Available in This Branch

**Generated On:** 2026-01-16 18:09:56

## Analysis Tools

### Task Complexity Analyzer
- **Script:** `analyze_task_complexity.py`
- **Purpose:** Analyzes complexity of tasks in tasks.json, creates metadata with research
- **Features:**
  - Extracts complexity scores from task metadata
  - Performs research on each task using simulated task-master research
  - Analyzes subtask states and completion percentages
  - Creates comprehensive metadata for each task

### Dependency Graph Builder
- **Script:** `build_dependency_graph.py` 
- **Purpose:** Creates dependency graphs and determines execution order
- **Features:**
  - Builds adjacency lists for task dependencies
  - Calculates topological order for execution sequence
  - Detects potential cycles in dependencies
  - Generates textual flow diagrams

### Branch Clustering Investigator
- **Script:** `investigate_clustering_potential.py`
- **Purpose:** Determines if hierarchical branch clustering could enable multi-stage alignment
- **Features:**
  - Identifies alignment and clustering related tasks
  - Analyzes potential factors for hierarchical approaches
  - Provides feasibility assessment for multi-stage alignment

### Research Simulator
- **Component:** Integrated research module
- **Purpose:** Simulates task-master research functionality
- **Features:**
  - Analyzes task content for technology relevance
  - Identifies implementation risks
  - Recommends implementation approaches

## Usage Examples

### Analyze All Tasks
```bash
python analyze_task_complexity.py --input tasks.json --output analysis_results.json
```

### Generate Dependency Graph
```bash
python build_dependency_graph.py --input tasks.json --output graph.dot
```

### Investigate Clustering Potential
```bash
python investigate_clustering_potential.py --input tasks.json
```

## Integration Points

These tools integrate with the existing task-master ecosystem:
- Compatible with tasks.json format
- Preserves existing metadata structures
- Adds enhanced analytical metadata
- Maintains backward compatibility

## Validation

All tools have been validated against the current task set and confirmed to:
- Preserve original task data
- Add valuable analytical insights
- Maintain JSON schema compatibility
- Provide actionable intelligence for task management
