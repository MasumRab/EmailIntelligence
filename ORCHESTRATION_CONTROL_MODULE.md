# Orchestration Control Module

## Overview

The Orchestration Control Module provides a **single centralized location** for checking if orchestration is enabled or disabled. All other code remains completely agnostic to the disable/enable mechanism.

This architecture has several benefits:
- ✅ Branch code doesn't need to know about disable flags
- ✅ All orchestration control logic in 2 files only
- ✅ Easy to change disable mechanism without touching branch code
- ✅ Consistent across Python and Shell scripts
- ✅ Testable and maintainable

---

## Architecture

### Two Files, One Purpose

Only **2 files** handle orchestration control:

1. **`setup/orchestration_control.py`** - Python module
2. **`scripts/lib/orchestration-control.sh`** - Shell module

Both export the same interface and check the same disable signals.

### Disable Signals (Checked in Order)

1. **Environment Variable:** `ORCHESTRATION_DISABLED=true`
2. **Marker File:** `.orchestration-disabled` exists
3. **Config File:** `config/orchestration-config.json` with `enabled=false`

If **ANY** signal disables orchestration, it's disabled.

---

## Usage

### Python Code

All Python code (launch.py, commands, container, etc.) should use:

```python
from setup.orchestration_control import is_orchestration_enabled

def run_orchestration_workflow():
    if is_orchestration_enabled():
        # Run orchestration
        execute_workflow()
    else:
        logger.info("Orchestration disabled, skipping workflow")
```

### Shell Scripts

All shell scripts should use:

```bash
#!/bin/bash

source scripts/lib/orchestration-control.sh

if is_orchestration_enabled; then
    echo "Running orchestration hooks..."
    # Run orchestration
else
    echo "Orchestration disabled, skipping"
    exit 0
fi
```

---

## API Reference

### Python Module (`setup/orchestration_control.py`)

#### Main Function

```python
def is_orchestration_enabled() -> bool:
    """
    Check if orchestration workflows are enabled.
    
    Returns:
        bool: True if enabled, False if disabled
    """
```

#### Other Functions

```python
def reset_cache():
    """Reset the orchestration status cache."""

def get_orchestration_status_summary() -> dict:
    """Get detailed status of all disable signals."""
    # Returns:
    # {
    #     'enabled': True/False,
    #     'signals': {
    #         'environment_variable': True/False,
    #         'marker_file': True/False,
    #         'config_file': True/False,
    #     }
    # }
```

---

### Shell Module (`scripts/lib/orchestration-control.sh`)

#### Main Function

```bash
is_orchestration_enabled
# Returns 0 if enabled (true), 1 if disabled (false)
```

#### Other Functions

```bash
# Show status message
get_orchestration_status
# Output: "Orchestration: ENABLED ✓" or "Orchestration: DISABLED ✗"

# Assert orchestration is enabled (soft fail)
assert_orchestration_enabled || return 1

# Skip if disabled (cleaner syntax)
skip_if_orchestration_disabled || return 0

# Reset cache
reset_orchestration_cache

# Debug: show all signals
_show_all_signals  # Only when _ORCHESTRATION_DEBUG=1
```

---

## Examples

### Python Example 1: Simple Check

```python
from setup.orchestration_control import is_orchestration_enabled

if is_orchestration_enabled():
    logger.info("Starting orchestration workflows")
    # ... orchestration code ...
else:
    logger.info("Orchestration disabled, running standalone")
    # ... standalone code ...
```

### Python Example 2: Get Detailed Status

```python
from setup.orchestration_control import get_orchestration_status_summary

status = get_orchestration_status_summary()
if not status['enabled']:
    print("Orchestration disabled by:")
    for signal, active in status['signals'].items():
        if not active:
            print(f"  - {signal}")
```

### Shell Example 1: Simple Check

```bash
#!/bin/bash
source scripts/lib/orchestration-control.sh

if is_orchestration_enabled; then
    echo "Running orchestration..."
    ./scripts/complex-orchestration.sh
else
    echo "Skipping orchestration (disabled)"
fi
```

### Shell Example 2: Assert Enabled (Hard Fail)

```bash
#!/bin/bash
source scripts/lib/orchestration-control.sh

# This script requires orchestration
assert_orchestration_enabled || exit 1

# Continue knowing orchestration is enabled
./critical-orchestration-workflow.sh
```

### Shell Example 3: Optional Orchestration

```bash
#!/bin/bash
source scripts/lib/orchestration-control.sh

# If orchestration is disabled, skip and return success
skip_if_orchestration_disabled || return 0

# Rest of script runs only if orchestration is enabled
echo "Orchestration is enabled, proceeding..."
```

---

## Branch Code Changes

**MINIMAL changes needed** to existing branch code:

### For Git Hooks

Change from:
```bash
#!/bin/bash
if [[ "${ORCHESTRATION_DISABLED}" == "true" ]]; then
    exit 0
fi
# hook code
```

To:
```bash
#!/bin/bash
source scripts/lib/orchestration-control.sh
is_orchestration_enabled || exit 0

# hook code
```

### For Commands

Change from:
```python
def execute(self):
    if os.getenv('ORCHESTRATION_DISABLED') == 'true':
        return 0
    # command code
```

To:
```python
from setup.orchestration_control import is_orchestration_enabled

def execute(self):
    if not is_orchestration_enabled():
        return 0
    # command code
```

### For Services

Change from:
```python
def start(self):
    if os.getenv('ORCHESTRATION_DISABLED') == 'true':
        logger.info("Orchestration disabled")
        return
    # service code
```

To:
```python
from setup.orchestration_control import is_orchestration_enabled

def start(self):
    if not is_orchestration_enabled():
        logger.info("Orchestration disabled")
        return
    # service code
```

---

## How It Works

### Control Flow

```
Branch Code
    ↓
is_orchestration_enabled()  ← Single Point of Check
    ↓
    Checks 3 Disable Signals:
    1. ORCHESTRATION_DISABLED env var
    2. .orchestration-disabled marker file
    3. config/orchestration-config.json
    ↓
Returns True/False
```

### Caching

The module caches the result for performance:
- First call checks all signals
- Subsequent calls return cached value
- Cache can be reset with `reset_cache()` / `reset_orchestration_cache()`

---

## Testing

### Test Python Module

```bash
# Test if orchestration is enabled
python setup/orchestration_control.py

# Or programmatically
python -c "from setup.orchestration_control import is_orchestration_enabled; print(is_orchestration_enabled())"
```

### Test Shell Module

```bash
# Test if orchestration is enabled
bash scripts/lib/orchestration-control.sh

# Or source and use
source scripts/lib/orchestration-control.sh
is_orchestration_enabled && echo "Enabled" || echo "Disabled"
```

### Test With Disable Flags

```bash
# Test with environment variable
ORCHESTRATION_DISABLED=true python setup/orchestration_control.py

# Test with marker file
touch .orchestration-disabled
python setup/orchestration_control.py
rm .orchestration-disabled

# Test with shell
ORCHESTRATION_DISABLED=true bash scripts/lib/orchestration-control.sh
```

---

## Debugging

### Enable Debug Output (Shell)

```bash
export _ORCHESTRATION_DEBUG=1
source scripts/lib/orchestration-control.sh
is_orchestration_enabled
# Will show why orchestration is disabled
```

### Get Detailed Status (Python)

```python
from setup.orchestration_control import get_orchestration_status_summary
import json

status = get_orchestration_status_summary()
print(json.dumps(status, indent=2))
# Output:
# {
#   "enabled": false,
#   "signals": {
#     "environment_variable": true,
#     "marker_file": false,
#     "config_file": true
#   }
# }
```

---

## Integration Points

Update these files to use the control module:

### Python Files

- `setup/launch.py` - Main launcher
- `setup/container.py` - Service container
- `setup/commands/*.py` - All command implementations
- `setup/services.py` - Service startup
- Any orchestration-dependent code

### Shell Files

- All `.git/hooks/*` - Git hooks
- `scripts/handle_stashes*.sh` - Stash handlers
- `scripts/sync_setup_worktrees.sh` - Setup sync
- Any orchestration-dependent scripts

---

## Migration Path

1. ✅ Create control modules (DONE)
2. Update integration points (Optional)
3. Remove direct checks for `ORCHESTRATION_DISABLED` in other code
4. Update documentation
5. Test with disabled orchestration

---

## Files

- `setup/orchestration_control.py` - Python control module
- `scripts/lib/orchestration-control.sh` - Shell control module
- `scripts/disable-all-orchestration.sh` - Enable script (unchanged)
- `scripts/enable-all-orchestration.sh` - Disable script (unchanged)

---

## Summary

- **Single source of truth** for orchestration control
- **Branch code agnostic** to disable mechanism
- **Consistent** across Python and Shell
- **Testable** and **maintainable**
- **Minimal migration** needed for existing code

Just import/source the control module and call `is_orchestration_enabled()`.
