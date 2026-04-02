# Disable Orchestration Workflows - Implementation Guide

## Overview

This guide explains how to create a flag to disable all orchestration workflows and integrations. There are multiple approaches depending on your needs.

---

## Option 1: Environment Variable (Simplest)

### Quick Implementation

Add to your `.env` file or shell environment:

```bash
export ORCHESTRATION_DISABLED=true
```

### Configuration Setup (settings.py)

Edit `setup/settings.py`:

```python
class Settings(BaseSettings):
    # ... existing settings ...
    
    # Orchestration control
    orchestration_disabled: bool = Field(
        default=False, 
        env="ORCHESTRATION_DISABLED",
        description="Disable all orchestration workflows and integrations"
    )
    max_concurrent_workflows: int = 10
```

### Usage in Code

```python
from setup.settings import Settings

settings = Settings()

if settings.orchestration_disabled:
    logger.info("Orchestration workflows are disabled")
    # Skip orchestration code
else:
    # Run orchestration code
    run_orchestration()
```

---

## Option 2: Command-Line Flag (Recommended)

### Modify launch.py

Edit `setup/launch.py` to add orchestration control:

```python
def main():
    parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher")
    
    # Existing arguments...
    parser.add_argument(
        '--disable-orchestration',
        action='store_true',
        help='Disable all orchestration workflows and integrations'
    )
    parser.add_argument(
        '--disable-hooks',
        action='store_true',
        help='Disable git hooks temporarily'
    )
    
    args = parser.parse_args()
    
    # Set environment variable based on flag
    if args.disable_orchestration:
        os.environ['ORCHESTRATION_DISABLED'] = 'true'
        logger.warning("Orchestration workflows disabled")
    
    if args.disable_hooks:
        disable_git_hooks()
        logger.warning("Git hooks disabled")
    
    # Continue with rest of launch logic...
```

### Usage

```bash
# Disable orchestration workflows
python launch.py setup --disable-orchestration

python launch.py run --disable-orchestration

# Disable both orchestration and git hooks
python launch.py --disable-orchestration --disable-hooks
```

---

## Option 3: Hook Control (Git-Level)

### Disable Git Hooks Script

Create `scripts/disable-orchestration-hooks.sh`:

```bash
#!/bin/bash
# Temporarily disable orchestration hooks

set -e

HOOKS_DIR=".git/hooks"
BACKUP_DIR=".git/hooks.backup-$(date +%s)"

if [[ ! -d "$HOOKS_DIR" ]]; then
    echo "No hooks directory found"
    exit 1
fi

# Backup existing hooks
mkdir -p "$BACKUP_DIR"
cp -r "$HOOKS_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true

# Disable by renaming
for hook in "$HOOKS_DIR"/*; do
    if [[ -f "$hook" ]] && [[ -x "$hook" ]]; then
        mv "$hook" "$hook.disabled"
        echo "Disabled: $(basename "$hook")"
    fi
done

echo "Orchestration hooks disabled"
echo "Backup saved to: $BACKUP_DIR"
echo "To restore, run: scripts/restore-orchestration-hooks.sh"
```

Create `scripts/restore-orchestration-hooks.sh`:

```bash
#!/bin/bash
# Restore orchestration hooks

set -e

HOOKS_DIR=".git/hooks"

# Find most recent backup
LATEST_BACKUP=$(ls -d ".git/hooks.backup-"* 2>/dev/null | sort -V | tail -1)

if [[ -z "$LATEST_BACKUP" ]]; then
    echo "No backup found"
    exit 1
fi

# Restore from backup
for hook in "$LATEST_BACKUP"/*; do
    if [[ -f "$hook" ]]; then
        cp "$hook" "$HOOKS_DIR/" || true
        chmod +x "$HOOKS_DIR/$(basename "$hook")" || true
        echo "Restored: $(basename "$hook")"
    fi
done

echo "Orchestration hooks restored from: $LATEST_BACKUP"
```

### Usage

```bash
# Disable hooks
./scripts/disable-orchestration-hooks.sh

# Enable hooks
./scripts/restore-orchestration-hooks.sh
```

---

## Option 4: Configuration File (Most Flexible)

### Create orchestration-config.json

Create `config/orchestration-config.json`:

```json
{
  "enabled": false,
  "workflows": {
    "pre_commit": true,
    "post_commit": true,
    "post_merge": true,
    "post_checkout": true,
    "post_push": true
  },
  "integrations": {
    "setup_sync": true,
    "branch_propagation": true,
    "validation": true,
    "cleanup": false
  },
  "features": {
    "auto_sync": true,
    "conflict_detection": true,
    "hook_validation": true,
    "worktree_sync": false
  }
}
```

### Load Configuration in Code

```python
import json
from pathlib import Path

def load_orchestration_config():
    config_path = Path("config/orchestration-config.json")
    if not config_path.exists():
        return {"enabled": True}  # Default: enabled
    
    with open(config_path) as f:
        return json.load(f)

class OrchestrationManager:
    def __init__(self):
        self.config = load_orchestration_config()
        self.enabled = self.config.get("enabled", True)
    
    def is_workflow_enabled(self, workflow_name):
        return self.enabled and self.config["workflows"].get(workflow_name, True)
    
    def is_integration_enabled(self, integration_name):
        return self.enabled and self.config["integrations"].get(integration_name, True)
```

---

## Option 5: Hook Wrapper Pattern (Most Robust)

### Create Hook Wrapper

Create `scripts/lib/orchestration-check.sh`:

```bash
#!/bin/bash
# Check if orchestration is enabled before running hooks

# Check environment variable
if [[ "${ORCHESTRATION_DISABLED}" == "true" ]]; then
    return 0  # Skip orchestration
fi

# Check config file
if [[ -f "config/orchestration-config.json" ]]; then
    enabled=$(jq -r '.enabled' config/orchestration-config.json 2>/dev/null || echo "true")
    if [[ "$enabled" != "true" ]]; then
        return 0  # Skip orchestration
    fi
fi

# Check for .orchestration-disabled marker file
if [[ -f ".orchestration-disabled" ]]; then
    return 0  # Skip orchestration
fi

return 1  # Orchestration is enabled
```

### Wrap Hooks

Modify `.git/hooks/post-commit`:

```bash
#!/bin/bash
# Post-commit orchestration hook

# Source orchestration check
source "scripts/lib/orchestration-check.sh"
if [[ $? -eq 0 ]]; then
    exit 0  # Skip
fi

# Run orchestration logic
# ... rest of hook code ...
```

---

## Complete Implementation Checklist

### Step 1: Add Environment Variable Support
```bash
# Edit setup/settings.py
# Add: orchestration_disabled: bool = Field(default=False, env="ORCHESTRATION_DISABLED")
```

### Step 2: Add Command-Line Flag
```bash
# Edit setup/launch.py
# Add: --disable-orchestration flag
# Set ORCHESTRATION_DISABLED=true if flag used
```

### Step 3: Check in Key Integration Points

#### In container.py:
```python
if os.getenv('ORCHESTRATION_DISABLED') == 'true':
    logger.info("Skipping orchestration service initialization")
    return  # Skip service initialization
```

#### In command handlers:
```python
def execute(self):
    if os.getenv('ORCHESTRATION_DISABLED') == 'true':
        logger.warning("Command execution skipped (orchestration disabled)")
        return 0
    # Execute command
```

#### In hooks (pre-commit, post-commit, etc.):
```bash
#!/bin/bash
if [[ "${ORCHESTRATION_DISABLED}" == "true" ]]; then
    exit 0  # Skip hook
fi
# Hook logic
```

### Step 4: Create Helper Scripts

```bash
# Create disable script
cat > scripts/disable-all-orchestration.sh << 'EOF'
#!/bin/bash
export ORCHESTRATION_DISABLED=true
echo "ORCHESTRATION_DISABLED=true" >> .env.local
./scripts/disable-orchestration-hooks.sh
echo ".orchestration-disabled" >> .gitignore
touch .orchestration-disabled
echo "All orchestration disabled"
EOF

# Create enable script
cat > scripts/enable-all-orchestration.sh << 'EOF'
#!/bin/bash
export ORCHESTRATION_DISABLED=false
sed -i '/ORCHESTRATION_DISABLED/d' .env.local
./scripts/restore-orchestration-hooks.sh
rm -f .orchestration-disabled
echo "All orchestration enabled"
EOF

chmod +x scripts/disable-all-orchestration.sh
chmod +x scripts/enable-all-orchestration.sh
```

### Step 5: Document in README

```markdown
## Disabling Orchestration

If you need to work independently without orchestration:

### Option A: Environment Variable
```bash
export ORCHESTRATION_DISABLED=true
```

### Option B: Command-line Flag
```bash
python launch.py run --disable-orchestration
```

### Option C: Git Hooks Only
```bash
./scripts/disable-orchestration-hooks.sh
```

### Option D: Complete Disable
```bash
./scripts/disable-all-orchestration.sh
```

### Re-enable
```bash
./scripts/enable-all-orchestration.sh
```
```

---

## Implementation Priority

1. **Immediate (5 min):** Add environment variable to settings.py
2. **Short-term (15 min):** Add flag to launch.py
3. **Medium-term (30 min):** Check orchestration_disabled in 3-5 critical integration points
4. **Nice-to-have (1 hour):** Create helper scripts and config file

---

## Testing the Flag

```bash
# Test with environment variable
ORCHESTRATION_DISABLED=true python launch.py setup

# Test with command-line flag
python launch.py setup --disable-orchestration

# Test with hook disable
./scripts/disable-orchestration-hooks.sh
git commit -m "test"  # Should work without hooks
./scripts/restore-orchestration-hooks.sh

# Test restoration
python launch.py setup  # Should run with orchestration
```

---

## Integration Points to Update

Key files that check for orchestration:

1. `setup/launch.py` - Main launcher
2. `setup/container.py` - Service initialization
3. `setup/commands/*.py` - Command handlers
4. `scripts/hooks/*` - All git hooks
5. `setup/services.py` - Service startup

Each should have early return if `ORCHESTRATION_DISABLED=true`

---

## References

- `setup/settings.py` - Configuration management
- `setup/launch.py` - Main entry point
- `scripts/disable-hooks.sh` - Existing hook disable script
- `setup/container.py` - Service container
