# Task 003.1: Define Critical Files and Validation Criteria

**Status:** pending
**Priority:** high
**Effort:** 2-3 hours
**Complexity:** 4/10
**Dependencies:** None
**Created:** 2026-01-06
**Parent:** Task 003: Develop and Integrate Pre-merge Validation Scripts

---

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

## Success Criteria

- [ ] Complete list of critical files created
- [ ] Validation criteria defined for each file
- [ ] Documentation ready for script implementation
- [ ] List covers all regression-prone files

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
