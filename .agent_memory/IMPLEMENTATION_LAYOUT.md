# Implementation Directory Layout

## Current State (Logging & Tracking Complete)

```
.taskmaster/
├── .agent_memory/              ✅ COMPLETE
│   ├── session_log.json        # Current session state
│   ├── memory_api.py           # Query API
│   ├── *.md                    # Documentation
│   └── example_usage.py        # Examples
│
└── task_data/                  ✅ READY
    ├── task-75.1.md            # CommitHistoryAnalyzer spec
    ├── task-75.2.md            # CodebaseStructureAnalyzer spec
    └── task-75.3.md            # DiffDistanceCalculator spec
```

## Next Phase (Task Implementation)

When Task 75.1-75.3 implementation begins, create:

```
.taskmaster/
├── .agent_memory/              (tracking progress)
│   └── session_log.json        (updated with implementation logs)
│
└── src/                        ← CREATE THIS
    ├── __init__.py
    └── analyzers/
        ├── __init__.py
        ├── commit_history_analyzer.py     # Task 75.1
        ├── codebase_structure_analyzer.py # Task 75.2
        └── diff_distance_calculator.py    # Task 75.3
```

Also create:

```
.taskmaster/
├── config/                     ← CREATE THIS
│   ├── commit_history.yaml
│   ├── codebase_structure.yaml
│   └── diff_distance.yaml
│
├── tests/                      ← CREATE THIS
│   ├── __init__.py
│   └── test_analyzers.py
│
└── examples/                   ← CREATE THIS (optional)
    ├── analyze_example_repo.py
    └── batch_analysis.py
```

## File Organization Rules

### Memory System (`.agent_memory/`)
- ✅ Read-only after validation
- ✅ No code implementation
- ✅ Only logging/tracking

### Task Code (`src/`)
- Single class per file
- Externalized configuration
- Type hints required
- Docstrings required
- Pure functions where possible

### Configuration (`config/`)
- YAML format
- Externalized from code
- Validated on load
- Example defaults provided

### Tests (`tests/`)
- Unit tests per analyzer
- >90% code coverage target
- No external services mocked
- Performance benchmarks

### Task Data (`task_data/`)
- Task specifications
- Implementation guides
- Gotchas & solutions
- Integration handoff docs

## Separation Confirmed

✅ Logging/memory = tracking layer (this directory)  
✅ Task execution = implementation layer (to be created)  
✅ Configuration = externalized (to be created)  
✅ Tests = validation layer (to be created)  

**Memory system never calls analyzer code. Analyzer code calls memory API.**

This ensures clean separation of concerns.
