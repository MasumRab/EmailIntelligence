# Core Modules Porting Plan to orchestration-tools

## Overview

This document outlines the plan to port core modules from the current consolidated branch (`consolidate/cli-unification`) to the `orchestration-tools` branch, enabling architectural alignment with both `main` and `scientific` branches.

## Target: orchestration-tools Branch

Current state of `src/core/` in orchestration-tools:
- `commands/setup_command.py`
- `conflict_models.py`
- `exceptions.py`
- `factory.py`
- `interfaces.py`

Missing modules needed:
- `database.py`
- `security.py`
- `performance_monitor.py`
- `enhanced_caching.py`
- `enhanced_error_reporting.py`
- `constants.py`
- `data/data_source.py`
- `data/database_source.py`

---

## Module 1: database.py

### Dependencies to Port
```
src/core/database.py requires:
├── src/core/performance_monitor.py     (log_performance)
├── src/core/enhanced_caching.py       (EnhancedCachingManager)
├── src/core/enhanced_error_reporting.py (log_error, ErrorSeverity, etc.)
├── src/core/constants.py             (DEFAULT_CATEGORY_COLOR, DEFAULT_CATEGORIES)
├── src/core/security.py             (validate_path_safety, sanitize_path)
└── src/core/data/data_source.py     (DataSource)
```

### Porting Dependencies (Must port in order)
1. **constants.py** - No dependencies (create if missing)
2. **security.py** - No local dependencies
3. **performance_monitor.py** - No dependencies  
4. **enhanced_error_reporting.py** - No dependencies
5. **enhanced_caching.py** - No dependencies
6. **data/data_source.py** - No dependencies
7. **database.py** - Has all above dependencies

### Predicted Issues

| Issue | Severity | Description | Solution |
|-------|----------|-------------|----------|
| Import path mismatch | HIGH | `from .security` vs `from src.core.security` | Adjust imports to local: `from .security import ...` |
| Global state (DATA_DIR) | MEDIUM | Uses `data/` directory which may not exist | Create data directory or make configurable |
| Circular import | MEDIUM | security imports DatabaseManager potentially | Use lazy imports or TYPE_CHECKING |
| gzip dependency | LOW | Module uses `gzip` standard library | Should work - Python built-in |
| DataSource Protocol | HIGH | `src/core/data/data_source.py` needed | Must also port DataSource class |

### Specific Code Changes Needed

```python
# Before (current)
from .performance_monitor import log_performance
from .security import validate_path_safety

# After (orchestration-tools)
from .performance_monitor import log_performance
from .security import validate_path_safety
# OR use absolute if src/core is in path
import src.core.security as security_module
```

---

## Module 2: security.py

### Dependencies to Port
```
src/core/security.py has NO local dependencies
```

This module is self-contained and should port cleanly.

### Predicted Issues

| Issue | Severity | Description | Solution |
|-------|----------|-------------|----------|
| Path resolution | MEDIUM | Uses `pathlib.Path.is_relative_to()` (Python 3.9+) | Check Python version requirement |
| Html escape | LOW | Uses `html` module | Should work - standard library |
| Logging setup | LOW | May need logger configuration | Add logging config in orchestration-tools |

### Specific Considerations

- **SecureFileSystemProxy** (line 290+): May conflict if orchestration-tools has file operations
- **PathValidator**: Should port cleanly
- **SecurityManager**: Should port cleanly

---

## Module 3: Supporting Modules

### performance_monitor.py
- **Dependencies**: None self-contained
- **Issues**: None predicted

### enhanced_caching.py  
- **Dependencies**: `logging`, `asyncio`
- **Issues**: None predicted

### enhanced_error_reporting.py
- **Dependencies**: None self-contained
- **Issues**: None predicted

### constants.py
- **Dependencies**: None
- **Issues**: None

### data/data_source.py
- **Dependencies**: `typing`
- **Issues**: None

---

## Porting Order (Safe Sequence)

```
1. constants.py                    (foundation)
2. security.py                     (no deps)
3. performance_monitor.py          (no deps)
4. enhanced_error_reporting.py     (no deps)
5. enhanced_caching.py            (no deps)
6. data/data_source.py           (no deps)
7. data/factory.py               (depends on DataSource)
8. data/database_source.py       (depends on DataSource, DatabaseManager)
9. database.py                   (depends on all above)
10. audit_logger.py              (may be needed by security)
```

---

## Potential Conflicts with orchestration-tools

| Module | Conflict With | Severity | Resolution |
|--------|--------------|----------|-------------|
| `database.py` | Existing `factory.py` | MEDIUM | Merge: Keep both, distinguish by name |
| `exceptions.py` | Custom exceptions | LOW | Merge: Add missing to existing |
| `factory.py` | Different Factory | **HIGH** | Rename: `database_factory.py` vs `orchestration_factory.py` |
| `conflict_models.py` | May have overlaps | LOW | Merge attributes |

---

## Testing Recommendations

After porting, verify:

```bash
# 1. Basic imports
python -c "from src.core.database import DatabaseManager; print('database: OK')"
python -c "from src.core.security import SecurityValidator; print('security: OK')"

# 2. Integration
python -m pytest tests/ -x -v --tb=short

# 3. Specific module tests
python -m pytest tests/test_database.py -v
python -m pytest tests/test_security.py -v
```

---

## Estimated Complexity

| Module | Lines | Dependencies | Porting Effort |
|--------|-------|--------------|---------------|
| database.py | 998 | 6 + DataSource | **HIGH** (4-6 hours) |
| security.py | 462 | 0 | **MEDIUM** (2-3 hours) |
| Supporting | ~500 | minimal | **LOW** (1-2 hours) |
| **Total** | ~2000 | - | **~8-12 hours** |

---

## Alternative: Quick Start (Minimal Port)

If full port is too complex, start with minimal working set:

```python
# minimal_core.py - Quick port package
from .constants import *
from .security import SecurityValidator, PathValidator, validate_path_safety
# Skip full database - use simple JSON for now
```

This provides basic security without full database complexity.

---

## Summary

**Recommended Path**: Port in dependency order starting with `constants.py` and `security.py`, then address `database.py`. Watch for import path conflicts and `DataSource` protocol requirement.