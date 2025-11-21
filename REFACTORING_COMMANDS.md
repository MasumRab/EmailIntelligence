# Quick Command Reference for Refactoring Tasks

## View All Analysis Documents

```bash
# Executive Summary (Start here for management/decision makers)
cat REFACTORING_EXECUTIVE_SUMMARY.md

# Full technical findings report
cat REFACTORING_FINDINGS_REPORT.md

# Detailed technical analysis
cat REFACTORING_ANALYSIS.md

# Migration code examples
cat REFACTORING_QUICK_REFERENCE.md

# Task descriptions
cat REFACTORING_TASKS_SUMMARY.md
```

## Task Master Commands

### View Tasks
```bash
# List all refactoring tasks
task-master list | grep -E "32|33|34|35|36|37"

# View specific task details
task-master show 32   # Test suite
task-master show 33   # Deprecation wrappers
task-master show 34   # Migration guide
task-master show 35   # Config initialization
task-master show 36   # Circular imports
task-master show 37   # Storage API

# View next recommended task
task-master next
```

### Work on Tasks

```bash
# Start working on a task
task-master set-status --id=32 --status=in-progress

# Break task into subtasks
task-master expand --id=32

# Mark task complete
task-master set-status --id=32 --status=done

# View expanded subtasks
task-master show 32.1
task-master show 32.2
```

### Update Progress

```bash
# Add implementation notes to subtask
task-master update-subtask --id=32.1 --prompt="Implementation notes about what was done"

# View all pending tasks
task-master list | grep "pending"

# Get task status
task-master show 32
```

## Git Commands for Context

### View the Refactoring Commit
```bash
# See the full diff
git diff 0f799cc1b580785e45e001acd6f72652adb2b5c5..HEAD

# See just the stats
git diff 0f799cc1b580785e45e001acd6f72652adb2b5c5..HEAD --stat

# View specific file changes
git diff 0f799cc1b580785e45e001acd6f72652adb2b5c5..HEAD -- src/context_control/core.py
git diff 0f799cc1b580785e45e001acd6f72652adb2b5c5..HEAD -- src/context_control/storage.py
git diff 0f799cc1b580785e45e001acd6f72652adb2b5c5..HEAD -- src/context_control/validation.py

# See the commit message
git show 0f799cc1b580785e45e001acd6f72652adb2b5c5

# View before/after specific lines
git show 0f799cc1b580785e45e001acd6f72652adb2b5c5:src/context_control/core.py | head -100
git show HEAD:src/context_control/core.py | head -100
```

## Development Setup

### Create test file for Task #32
```bash
touch tests/core/test_context_control.py
```

### Check current test status
```bash
# Run existing tests (if any)
pytest tests/core/ -v

# Run with coverage
pytest tests/core/ --cov=src/context_control --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Check imports for Task #36
```bash
# Test imports in isolation
python -c "from src.context_control.core import ContextController; print('✅ Import works')"
python -c "from src.context_control.validation import ContextValidator; print('✅ Import works')"
python -c "from src.context_control.storage import ProfileStorage; print('✅ Import works')"

# Check for circular imports
python -m py_compile src/context_control/*.py
```

## Code Review Commands

### Find methods mentioned in breaking changes
```bash
# Find BranchMatcher
grep -n "class BranchMatcher" src/context_control/core.py

# Find EnvironmentTypeDetector
grep -n "class EnvironmentTypeDetector" src/context_control/core.py

# Find ContextFileResolver
grep -n "class ContextFileResolver" src/context_control/core.py

# Find all validators
grep -n "class.*Validator" src/context_control/validation.py

# Find ProfileStorage
grep -n "class ProfileStorage" src/context_control/storage.py
```

### Check for legacy classes (backward compat)
```bash
# Legacy compatibility layer
grep -n "Legacy" src/context_control/core.py
grep -n "Legacy" src/context_control/validation.py
grep -n "Legacy" src/context_control/storage.py
```

## Analysis & Verification

### Check module structure
```bash
# List all files
ls -la src/context_control/

# Check dependencies between files
grep -h "^from" src/context_control/*.py | sort | uniq

# Count lines of code
wc -l src/context_control/*.py
```

### Verify changes against report
```bash
# Check if test file exists (should be created for Task #32)
ls tests/core/test_context_control.py 2>/dev/null || echo "❌ Not created yet"

# Check if deprecation warnings exist (Task #33)
grep -r "DeprecationWarning" src/context_control/ || echo "❌ Not added yet"

# Check storage API compatibility (Task #37)
grep -n "export_profile_to_path\|import_profile_from_path" src/context_control/storage.py || echo "❌ Not added yet"
```

## Documentation

### Generate HTML reports (if tools available)
```bash
# Generate module documentation
pdoc src/context_control --html --output-dir docs/

# Generate test coverage report
coverage run -m pytest tests/core/
coverage html

# View reports
open docs/context_control/index.html
open htmlcov/index.html
```

## Commit Workflow for Tasks

### Work on Task #32 (Example)
```bash
# Create feature branch
git checkout -b feature/task-32-context-control-tests

# Make changes
echo "test_code" > tests/core/test_context_control.py

# Check what changed
git diff

# Commit
git add tests/core/test_context_control.py
git commit -m "task(#32): Create comprehensive test suite for context_control

- Add unit tests for BranchMatcher
- Add unit tests for EnvironmentTypeDetector
- Add unit tests for ContextValidator components
- Add DI pattern tests with mocks
- Add legacy compatibility tests
- Achieve 90%+ code coverage

Fixes #32"

# Push and create PR
git push origin feature/task-32-context-control-tests
```

## Integration Checklist (Before Merging)

```bash
# 1. Check all tests pass
pytest tests/core/test_context_control.py -v

# 2. Check coverage meets target
pytest tests/core/test_context_control.py --cov=src/context_control --cov-report=term-missing

# 3. Verify no new circular imports
python -c "from src.context_control import *; print('✅ All imports work')"

# 4. Run linting
flake8 src/context_control/
pylint src/context_control/

# 5. Check type hints
mypy src/context_control/

# 6. Verify backward compat layer
grep -c "DeprecationWarning" src/context_control/core.py  # Should be > 0

# 7. Create commit message
git log -1 --oneline  # Review before push
```

## Troubleshooting

### If tests fail
```bash
# See detailed error
pytest tests/core/test_context_control.py -v -s --tb=long

# Check imports
python -c "from src.context_control.core import *"

# Run with debugging
python -m pdb -m pytest tests/core/test_context_control.py
```

### If circular imports
```bash
# Test each module separately
python -c "from src.context_control import models"
python -c "from src.context_control import exceptions"
python -c "from src.context_control import config"
python -c "from src.context_control import logging_module"
python -c "from src.context_control import core"
python -c "from src.context_control import storage"
python -c "from src.context_control import validation"
```

### If config initialization fails
```bash
# Test config in isolation
python << 'PYEOF'
from src.context_control.config import get_current_config
config = get_current_config()
print(f"Config loaded: {config}")
print(f"Profiles dir: {config.profiles_dir}")
PYEOF
```

## Monitoring & Validation

### Watch for deprecation warnings during tests
```bash
# Run tests and show warnings
pytest tests/core/ -W default::DeprecationWarning -v

# Count deprecation warnings
pytest tests/core/ -W default::DeprecationWarning -v 2>&1 | grep -c DeprecationWarning
```

### Verify performance impact
```bash
# Benchmark old vs new (if you create benchmark tests)
pytest tests/core/test_performance.py -v

# Check memory usage
python -c "from src.context_control import *; print('Module loaded')" && \
  ps aux | grep python
```

## Document References

| Document | Purpose | Audience |
|----------|---------|----------|
| REFACTORING_EXECUTIVE_SUMMARY.md | Quick overview, decision-making | Managers, Tech Leads |
| REFACTORING_FINDINGS_REPORT.md | Detailed findings, all concerns | Technical Teams |
| REFACTORING_ANALYSIS.md | Deep technical analysis | Backend Developers |
| REFACTORING_QUICK_REFERENCE.md | Migration examples | Developers using module |
| REFACTORING_TASKS_SUMMARY.md | Task descriptions | Task assignees |
| REFACTORING_COMMANDS.md | Commands reference | All (this file) |

## Quick Status Check

```bash
#!/bin/bash
echo "=== Refactoring Status Check ==="
echo ""
echo "Test coverage:"
[ -f tests/core/test_context_control.py ] && echo "✅ Test file exists" || echo "❌ Test file missing"
echo ""
echo "Deprecation wrappers:"
grep -q "DeprecationWarning" src/context_control/core.py && \
  echo "✅ Deprecation warnings added" || echo "❌ Not added"
echo ""
echo "Storage API compatibility:"
grep -q "export_profile_to_path" src/context_control/storage.py && \
  echo "✅ Export/import methods added" || echo "❌ Not added"
echo ""
echo "Config initialization fix:"
grep -q "_lock" src/context_control/core.py && \
  echo "✅ Thread-safe pattern added" || echo "❌ Not added"
echo ""
echo "Task status:"
task-master list | grep -E "32|33|34|35|36|37" | awk '{print $2, $3}' 2>/dev/null || echo "Task Master not available"
```

Save this as `check_status.sh` and run: `bash check_status.sh`

