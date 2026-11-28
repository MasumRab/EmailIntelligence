# Task 003.1: Define Critical Files and Validation Criteria

**Status:** specified
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** None

---

## Overview/Purpose

Identify all critical files and directories whose absence or corruption would cause regressions, and define validation criteria for pre-merge checks.

## Success Criteria

- [ ] Complete list of critical files created
- [ ] Validation criteria defined for each file
- [ ] Documentation ready for script implementation
- [ ] List covers all regression-prone files

## Prerequisites & Dependencies

### Required Before Starting
- [ ] No external prerequisites

### Blocks (What This Task Unblocks)
- [ ] No specific blocks defined

### External Dependencies
- [ ] No external dependencies

## Sub-subtasks Breakdown


## Specification Details

### Task Interface
- **ID**: 003.1
- **Title**: Define Critical Files and Validation Criteria
- **Status**: specified
- **Priority**: high
- **Effort**: 2-3 hours
- **Complexity**: 4/10

### Requirements
1. A list of critical files exists with one entry per file, each naming what breaks if it disappears
   -- not merely that it is important.
2. Each critical file records a validation predicate: exists, parses, exports a named symbol, or
   matches a required pattern.
3. Validation criteria are executable, so the list can be applied by a script without interpretation.
4. Test files and CI configuration are included: a deleted test directory and a deleted workflow both
   pass every runtime check today.
5. The list is reviewed against what CI actually runs in `.github/workflows/ci.yml`, so a file that no
   job touches is not called critical without justification.

## Implementation Guide

Put the list in `config/critical-files.json`. Derive the first pass mechanically from CI:

```bash
grep -E 'pytest|ruff|bandit|uv run' .github/workflows/ci.yml
git ls-tree -r --name-only HEAD -- src/ modules/ tests/ pyproject.toml
```

Each entry: `{"path": ..., "kind": "exists|parses|exports|pattern", "predicate": ..., "breaks": ...}`.


## Purpose

Identify all critical files and directories whose absence or corruption would cause regressions, and define validation criteria for pre-merge checks.

---

## Details

Analyze the codebase to identify files critical to project functionality. Create a definitive list with specific validation rules.

### Steps

1. **Review project structure**
   - `setup/commands/` - Command modules
   - `setup/container/` - Container configuration
   - `AGENTS.md` - Agent documentation
   - `src/core/` - Core application files
   - `config/` - Configuration files
   - `data/` - Data files

2. **Identify critical files**
   - `setup/commands/__init__.py`
   - `setup/container/__init__.py`
   - `AGENTS.md`
   - Core JSON data schemas
   - Configuration files

3. **Define validation criteria**
   - Existence check for all files
   - Non-empty check for key files
   - JSON validity for data files
   - Schema validation where applicable

4. **Document findings**

---

## Test Strategy

- Verify list completeness against project structure
- Cross-reference with historical missing-file issues
- Validate criteria appropriateness

---

## Implementation Notes

### Critical File Categories

| Category | Files | Validation |
|----------|-------|------------|
| Setup modules | `setup/*/__init__.py` | Existence, non-empty |
| Documentation | `AGENTS.md`, `*.md` | Existence |
| Data files | `data/**/*.json` | Valid JSON |
| Config | `config/*.py`, `*.json` | Existence |

### Output Format

```python
CRITICAL_FILES = {
    "setup/commands/__init__.py": {
        "required": True,
        "check_exists": True,
        "check_empty": True,
        "check_json": False,
    },
    "data/processed/email_data.json": {
        "required": True,
        "check_exists": True,
        "check_empty": True,
        "check_json": True,
    },
}
```

---

## Progress Log

### 2026-01-06
- Subtask file created
- Ready for implementation

---

## Next Steps

After completion, proceed to **Task 003.2**: Develop Core Validation Script
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** None
**Created:** 2026-01-06
**Parent:** Task 003: Develop and Integrate Pre-merge Validation Scripts

---

## Configuration Parameters

- **Owner**: TBD
- **Initiative**: TBD
- **Scope**: TBD
- **Focus**: TBD

## Performance Targets

- **Effort Range**: TBD
- **Complexity Level**: TBD

## Testing Strategy

### Unit Tests
- [ ] Tests cover core functionality
- [ ] Edge cases handled appropriately
- [ ] Performance benchmarks met

### Integration Tests
- [ ] Integration with dependent components verified
- [ ] End-to-end workflow tested
- [ ] Error handling verified

### Test Strategy Notes
- Verify list completeness against project structure
- Cross-reference with historical missing-file issues
- Validate criteria appropriateness

## Common Gotchas & Solutions

- [ ] [Common issues and solutions to be documented]

## Integration Checkpoint

### Criteria for Moving Forward
- [ ] All success criteria met
- [ ] Code reviewed and approved
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No critical or high severity issues

## Done Definition

### Completion Criteria
- [ ] All success criteria checkboxes marked complete
- [ ] Code quality standards met (PEP 8, documentation)
- [ ] Performance targets achieved
- [ ] All subtasks completed
- [ ] Integration checkpoint criteria satisfied
