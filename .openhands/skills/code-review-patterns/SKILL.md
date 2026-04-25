---
name: code-review-patterns
description: Common code review patterns and fixes for this repository based on historical PR feedback.
---

# Code Review Patterns

This skill captures recurring patterns identified from code reviews in this repository.

## Error Handling

### Always Use Specific Exceptions

❌ Avoid catching bare `Exception`:
```python
except Exception:
    return ""
```

✅ Prefer specific exceptions:
```python
except (subprocess.SubprocessError, OSError):
    return ""
```

### Use Logging Instead of Print for Errors

❌ Avoid:
```python
except Exception as e:
    print(f"Error: {e}")
```

✅ Prefer:
```python
import logging
logger = logging.getLogger(__name__)

except Exception as e:
    logger.error(f"Failed to save data: {e}")
    raise  # Re-raise unexpected errors
```

### Use logging.exception() in Except Blocks

❌ Avoid:
```python
except Exception as e:
    logger.error(f"Scheduled sync failed: {e}")
```

✅ Prefer (preserves traceback):
```python
except Exception as e:
    logger.exception("Scheduled sync failed")
```

## Type Hints

### Make Optional Type Hints Explicit

❌ Avoid:
```python
def __init__(self, scheduler_file: Path = None):
```

✅ Prefer:
```python
from typing import Optional

def __init__(self, scheduler_file: Optional[Path] = None):
```

### Apply to All Optional Parameters

```python
def create_maintenance_task(
    self,
    task_type: str,
    document_id: str,
    description: str,
    priority: str = "normal",
    assigned_agents: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
```

## Code Quality

### Remove Unused Variables

❌ Avoid:
```python
task_id = self.create_maintenance_task(...)
```

✅ Prefer (or use `_` prefix to signal intent):
```python
self.create_maintenance_task(...)
# or
_task_id = self.create_maintenance_task(...)
```

### Remove Unnecessary f-string Prefixes

❌ Avoid:
```python
print(f"\nSystem Status")
```

✅ Prefer:
```python
print("\nSystem Status")
```

### Remove Redundant Code After return

❌ Avoid:
```python
if condition:
    return True
else:
    # This else is unnecessary
    do_something()
```

✅ Prefer:
```python
if condition:
    return True
do_something()
```

## Security

### Avoid Shell Injection

❌ Never use `shell=True` with string interpolation:
```python
subprocess.run(f"git branch -m {branch_name}", shell=True)
```

✅ Use shell=False with list arguments:
```python
subprocess.run(["git", "branch", "-m", branch_name], shell=False)
```

## Performance

### Use Calendar-Aware Time Calculations

❌ Avoid fixed day counts:
```python
return now + (30 * 86400)  # Doesn't account for month length
```

✅ Use dateutil for accurate scheduling:
```python
from dateutil.relativedelta import relativedelta
return (datetime.now() + relativedelta(months=1)).timestamp()
```

### Use `next(iter(set))` Instead of `list(set)[0]`

❌ Avoid:
```python
operations = list(operations)[0]
```

✅ Prefer:
```python
operations = next(iter(operations))
```

## Maintainability

### Refactor Complex Conditionals

❌ Avoid long compound conditionals:
```bash
if [[ "$file" == docs/* ]] || [[ "$file" == backlog/* ]] || [[ "$file" == worktrees/docs-main/docs/* ]] ...; then
```

✅ Use arrays and loops:
```bash
ALLOWED_PATHS=( "docs/" "backlog/" "worktrees/docs-main/docs/" )
for allowed_path in "${ALLOWED_PATHS[@]}"; do
    if [[ "$file" == $allowed_path* ]]; then
        continue
    fi
done
```

### Standardize Python Command

❌ Avoid hardcoded python/python3:
```bash
if command -v python3 &> /dev/null; then
    python3 script.py
fi
```

✅ Use a standardized approach:
```bash
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi
$PYTHON_CMD script.py
```

### Extract Shared Utilities

Duplicate functions across files should be extracted to a shared module:
- `get_current_branch()` appears in multiple scripts
- `_percentile()` duplicated in bottleneck_detector.py and resource_monitor.py

## Testing

### Add Assertions to Tests

❌ Avoid only printing results:
```python
print(f"Result: {result}")
# No verification!
```

✅ Prefer assertions:
```python
assert len(api_agents) == 1, "Expected 1 agent with API capability"
assert api_agents[0].agent_name == "api-writer"
```

### Use Proper Test Framework

❌ Avoid demo scripts without assertions:
```python
# test_conflict_predictor.py - runs but doesn't verify
```

✅ Use unittest or pytest:
```python
import unittest

class TestConflictPredictor(unittest.TestCase):
    def test_conflict_prediction(self):
        predictor = ConflictPredictor()
        conflicts = predictor.predict_conflicts(pending_changes)
        self.assertGreater(len(conflicts), 0)
```

## File Operations

### Handle File I/O Errors Explicitly

❌ Avoid silent failures:
```python
with open(self.registry_file, 'w') as f:
    json.dump(data, f)
# No error handling!
```

✅ Prefer explicit error handling:
```python
try:
    with open(self.registry_file, 'w') as f:
        json.dump(data, f, indent=2)
except (OSError, IOError) as e:
    logger.error(f"Error saving registry to {self.registry_file}: {e}")
    raise
```

### Move Imports to Module Scope

❌ Avoid inline imports:
```python
if preserve_custom:
    import shutil
# shutil used later but import may not execute!
```

✅ Always import at module level:
```python
import shutil

if preserve_custom:
    # shutil available here
```

## Common Bugs to Watch For

### Enum Conversion

If an enum is already assigned, don't call `.upper()` on it:
```python
# pattern_info['confidence'] is already a FixConfidence enum
confidence = FixConfidence[pattern_info['confidence'].upper()]  # FAILS!

# Fix: check type first
confidence_value = pattern_info['confidence']
resolved_confidence = (
    confidence_value
    if isinstance(confidence_value, FixConfidence)
    else FixConfidence[str(confidence_value).upper()]
)
```

### Case Sensitivity in File Checks

Don't lowercase file paths if filesystem is case-sensitive:
```python
# Drops file extension and case
file_mentions = re.findall(r'created?\s+([^,\n.]+)', notes.lower())

# Fix: preserve original
file_mentions = re.findall(r'created?\s+([\w./-]+)', notes_raw)
```

### Returning Only First Item of List

When splitting creates multiple tasks, don't return only the first:
```python
# Bug: silently drops remaining tasks
return tasks[0] if tasks else None

# Fix: return all tasks
return tasks if tasks else None
```

### Atomic Operations

When marking groups as failed, rollback partial changes:
```python
if success_count == len(group.worktrees):
    group.status = "completed"
else:
    group.status = "failed"
    # Add rollback for atomicity!
    self.rollback_commit_group(group_id)
```