# Quick Reference Card: Refactoring Implementation

**Date:** 2026-01-04  
**Refactoring ID:** i2t4-into-756  
**Status:** Ready for Implementation

---

## TL;DR Summary

**Goal:** Integrate I2.T4's migration analysis into 75.6's clustering framework  
**Effort:** 18-24 hours (3-4 days)  
**Files:** 3 files modified, ~870 lines changed  
**New Features:** 3 execution modes, migration analysis, multiple output formats

---

## Five Key Changes

1. **Add MigrationAnalyzer** - Detects backend → src migration patterns
2. **Add 3 Execution Modes** - identification, clustering, hybrid
3. **Add OutputGenerator** - Supports simple/detailed/all output formats
4. **Update Configuration** - Add mode, migration, and output format options
5. **Add Tests** - 10 new test cases for new features

---

## File Changes at a Glance

```
task_data/branch_clustering_implementation.py
├── Line 80:  ADD MigrationMetrics dataclass
├── Line 72:  MODIFY BranchMetrics (add migration_metrics)
├── Line 590: ADD MigrationAnalyzer class (~140 lines)
├── Line 814: MODIFY BranchClusteringEngine.__init__
├── Line 821: ADD _validate_mode method
├── Line 828: ADD execute method
├── Line 838: ADD execute_identification_pipeline method
├── Line 885: ADD execute_hybrid_pipeline method
├── Line 914: ADD OutputGenerator class (~120 lines)
└── Line 748: MODIFY _generate_tags (add migration tags)

task_data/task-75.6.md
├── Line 400: MODIFY Configuration schema
└── Line 350: ADD 10 new test cases

task_data/QUICK_START.md
└── Line -: ADD Usage examples for all modes
```

---

## Execution Modes

### Mode 1: Identification (I2.T4 Style)
```python
engine = BranchClusteringEngine(mode="identification")
results = engine.execute(branches)
# Returns: Simple JSON output
# Performance: <30s for 13 branches
# Memory: <50MB
```

### Mode 2: Clustering (75.6 Style)
```python
engine = BranchClusteringEngine(mode="clustering")
results = engine.execute(branches)
# Returns: Detailed JSON output with clustering
# Performance: <120s for 13 branches
# Memory: <100MB
```

### Mode 3: Hybrid (Combined)
```python
engine = BranchClusteringEngine(mode="hybrid")
results = engine.execute(branches)
# Returns: Both simple and detailed outputs
# Performance: <90s for 13 branches
# Memory: <75MB
```

---

## Configuration Options

```yaml
execution:
  mode: clustering  # identification | clustering | hybrid
  enable_migration_analysis: true
  enable_clustering_in_hybrid: true
  output_format: detailed  # simple | detailed | all
```

---

## Implementation Checklist

### Phase 2: Implementation (14 tasks)
- [ ] Add MigrationMetrics dataclass (line 80)
- [ ] Update BranchMetrics dataclass (line 72)
- [ ] Add MigrationAnalyzer class (line 590)
- [ ] Add Path import (line 13)
- [ ] Update BranchClusteringEngine.__init__ (line 814)
- [ ] Add _validate_mode method (line 821)
- [ ] Add execute method (line 828)
- [ ] Add execute_identification_pipeline method (line 838)
- [ ] Add execute_hybrid_pipeline method (line 885)
- [ ] Update execute_full_pipeline (line 840, 842, 876)
- [ ] Add OutputGenerator class (line 914)
- [ ] Update _generate_tags method (line 748)

### Phase 3: Configuration (1 task)
- [ ] Update configuration schema (task-75.6.md line 400)

### Phase 4: Testing & Documentation (2 tasks)
- [ ] Add 10 new test cases (task-75.6.md line 350)
- [ ] Add usage examples (QUICK_START.md)

---

## Critical Path (Must be sequential)

1. Add MigrationMetrics → Update BranchMetrics
2. Add MigrationAnalyzer → Update Engine.__init__
3. Add mode validation → Add execute method
4. Add identification pipeline → Add hybrid pipeline
5. Update existing pipeline → Add OutputGenerator
6. Update tags → Update configuration → Add tests

---

## Quick Test Commands

```bash
# Test identification mode
python -c "
from task_data.branch_clustering_implementation import BranchClusteringEngine
engine = BranchClusteringEngine(mode='identification')
results = engine.execute(['feature-branch-1'])
print(results)
"

# Test clustering mode
python -c "
from task_data.branch_clustering_implementation import BranchClusteringEngine
engine = BranchClusteringEngine(mode='clustering')
results = engine.execute(['feature-branch-1'])
print(results)
"

# Test hybrid mode
python -c "
from task_data.branch_clustering_implementation import BranchClusteringEngine
engine = BranchClusteringEngine(mode='hybrid')
results = engine.execute(['feature-branch-1'])
print(results)
"
```

---

## Performance Targets

| Mode | Target | Memory |
|------|--------|--------|
| Identification | <30s | <50MB |
| Clustering | <120s | <100MB |
| Hybrid | <90s | <75MB |

---

## Key Benefits

✅ **Unified Architecture** - Single codebase for both workflows  
✅ **Preserved Functionality** - All I2.T4 features maintained  
✅ **Performance Gains** - I2.T4 gets caching and parallelization  
✅ **Maintainability** - Reduced code duplication  
✅ **Extensibility** - Easy to add new analyzers  

---

## Common Issues & Solutions

### Issue: Mode validation error
**Solution:** Ensure mode is one of: identification, clustering, hybrid

### Issue: Migration analysis not working
**Solution:** Check that MigrationAnalyzer is initialized in __init__

### Issue: Output format not recognized
**Solution:** Ensure output_format is one of: simple, detailed, all

### Issue: Performance regression
**Solution:** Check caching is enabled, verify parallelization settings

---

## Documentation Files

- **IMPLEMENTATION_GUIDE.md** - Detailed implementation instructions with line numbers
- **CHANGE_SUMMARY.md** - Complete change breakdown table
- **plan.md** - Original refactoring plan
- **state.json** - Progress tracking

---

## Next Steps

1. Review IMPLEMENTATION_GUIDE.md for detailed instructions
2. Review CHANGE_SUMMARY.md for complete change breakdown
3. Create feature branch: `refactor/i2t4-into-756`
4. Implement changes following the checklist
5. Test each phase before proceeding
6. Update documentation as you go

---

## Success Criteria

- [ ] All 17 implementation tasks complete
- [ ] All 10 new test cases pass
- [ ] Performance targets met for all modes
- [ ] Code coverage >90%
- [ ] PEP 8 compliant
- [ ] Ready for integration with Tasks 75.7, 75.8

---

**Quick Reference Version:** 1.0  
**Last Updated:** 2026-01-04  
**Maintained By:** Refactoring Team