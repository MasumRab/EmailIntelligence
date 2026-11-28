# Scripts Directory

**Last Updated:** December 11, 2025  
**Purpose:** Project automation, utilities, and tooling  
**Total Scripts:** 100+

---

## Quick Navigation

| Need | Find It |
| --- | --- |
| **Complete script list** | [SCRIPTS_INVENTORY.md](./SCRIPTS_INVENTORY.md) |
| **Markdown tools** | [markdown/README.md](./markdown/README.md) |
| **Script dependencies** | [DEPENDENCIES.md](./DEPENDENCIES.md) |
| **Sync status** | [SCRIPTS_SYNC_STATUS.md](./SCRIPTS_SYNC_STATUS.md) |
| **Find a script** | See Categories below |

---

## Categories

### Core Infrastructure

**Git Hooks** (`hooks/`)
- Auto-run scripts on git events
- Pre-commit validation
- Post-merge synchronization
- Files: `post-checkout`, `post-commit`, `post-merge`, `pre-commit`, `post-push`

**Installation** (`install-hooks.sh`)
- Install all hooks
- Set up project environment
- Initialize git automation

### Development Tools

**Markdown** (`markdown/`)
- Format markdown with prettier
- Lint markdown with markdownlint-cli
- Standardize links to ./ prefix
- Files: `lint-and-format.sh`, `standardize-links.sh`, `README.md`

**Task Management** (`task_creation/`)
- Task decomposition
- Task tracking
- Completion validation
- Task-based automation

**Orchestration Management**
- Enable/disable hooks
- Branch synchronization
- Validate orchestration context
- Control hook execution

### Utilities

**Stash Management** (`stash_*.sh`)
- Analyze git stashes
- Interactive stash resolution
- Stash documentation
- Optimized stash operations

**Documentation** (`docs_*.py`)
- Merge strategies
- Content analysis
- Review management
- Workflow triggering
- Branch versioning

**Synchronization** (`sync_*.py`, `sync_*.sh`)
- Sync common documentation
- Script synchronization
- Parallel sync operations
- Auto-sync with monitoring

**Validation** (`*validator*.py`, `verify-*.py`)
- Dependency verification
- Parallel validation
- Incremental checks
- Validation caching

### Advanced

**Agents** (`agents/`)
- Agent registry
- Health monitoring
- Performance tracking
- Workflow integration

**Context Management** (`context_management/`)
- Context switching
- Environment management
- Worktree context detection
- Force sync operations

**Libraries** (`lib/`)
- Shared bash functions
- Git utilities
- Logging utilities
- Validation functions
- Error handling
- Stash utilities

---

## Quick Start

### Find a Script

```bash
# Search by name
find scripts -name "*script-name*"

# List all scripts in a category
ls scripts/markdown/        # Markdown scripts
ls scripts/hooks/           # Git hooks
ls scripts/agents/          # Agent scripts

# See complete registry
cat scripts/SCRIPTS_INVENTORY.md
```

### Get Help

```bash
# Most shell scripts support --help
bash scripts/markdown/lint-and-format.sh --help
bash scripts/stash_manager.sh --help

# For Python scripts
python scripts/verify-dependencies.py --help
```

### Common Tasks

#### Format Markdown

```bash
# Fix all markdown files
bash scripts/markdown/lint-and-format.sh --fix --all

# Check without modifying
bash scripts/markdown/lint-and-format.sh --check --all

# Standardize links
bash scripts/markdown/standardize-links.sh --fix --all
```

#### Install Git Hooks

```bash
# Set up automatic git hooks
bash scripts/install-hooks.sh

# Check hook status
bash scripts/orchestration_status.sh
```

#### Verify Dependencies

```bash
# Check all system and package dependencies
python scripts/verify-dependencies.py

# Check npm packages
npm list prettier markdownlint-cli

# Check Python packages
python -m pip list | grep -E "black|flake8|mypy|pylint"
```

#### Manage Stashes

```bash
# View all stashes
bash scripts/stash_details.sh

# Analyze stash contents
bash scripts/stash_analysis.sh

# Interactive stash manager
bash scripts/stash_manager_optimized.sh
```

#### Sync Documentation

```bash
# Sync common documentation across branches
bash scripts/sync-common-docs.sh

# Or with Python
python scripts/sync_common_docs.py
```

---

## File Organization

```
scripts/
├── hooks/                          # Git hooks (auto-execute)
│   ├── post-checkout
│   ├── post-commit
│   ├── post-merge
│   ├── pre-commit
│   └── post-push
│
├── markdown/                       # Markdown linting/formatting
│   ├── lint-and-format.sh
│   ├── standardize-links.sh
│   └── README.md
│
├── lib/                            # Shared libraries
│   ├── common.sh
│   ├── git_utils.sh
│   ├── logging.sh
│   ├── validation.sh
│   ├── stash_common.sh
│   └── error_handling.sh
│
├── agents/                         # Agent management
│   ├── agent_registry.py
│   ├── agent_health_monitor.py
│   ├── agent_performance_monitor.py
│   └── agent_workflow_integration.py
│
├── context_management/             # Context management
│   ├── orchestration.conf
│   └── [context utilities]
│
├── task_creation/                  # Task management
│   └── [task scripts]
│
├── SCRIPTS_INVENTORY.md            # Complete registry
├── SCRIPTS_SYNC_STATUS.md          # Sync tracking
├── DEPENDENCIES.md                 # Dependency documentation
├── README.md                       # This file
│
├── docs_*.py                       # Documentation utilities
├── sync_*.py                       # Synchronization scripts
├── validate_*.py                   # Validation scripts
├── stash_*.sh                      # Stash management
├── enable_*.sh                     # Orchestration control
├── disable_*.sh                    # Orchestration control
│
└── [other utilities and scripts]
```

---

## Dependencies

### System
- bash 4.0+
- python 3.8+
- git 2.20+
- npm 6.0+ (for markdown scripts)

### npm Packages
```bash
npm install --save-dev prettier markdownlint-cli
```

### Python Packages
See `requirements-dev.txt` for complete list

### Full Details
See [DEPENDENCIES.md](./DEPENDENCIES.md)

---

## Contributing

### Adding a New Script

1. **Choose directory** based on function
   - Infrastructure → root scripts/ or scripts/
   - Markdown → scripts/markdown/
   - Agents → scripts/agents/
   - Other → scripts/ or subdirectory

2. **Add script header documentation**
   ```bash
   #!/bin/bash
   ##
   # Script Name
   # Purpose: What it does
   # Usage: How to run it
   # Requirements: Dependencies
   ##
   ```

3. **Include help text**
   - All scripts should support `--help` flag
   - Document all options
   - Provide usage examples

4. **Update SCRIPTS_INVENTORY.md**
   - Add entry in appropriate category
   - Document purpose
   - List dependencies
   - Specify branch availability

5. **Test thoroughly**
   - Test on orchestration-tools first
   - Test on scientific branch
   - Test on main branch

6. **Document dependencies**
   - Update DEPENDENCIES.md if new deps
   - Note system/npm/Python requirements
   - Test in clean environment

7. **Commit with clear message**
   ```bash
   git add scripts/your-script.sh
   git commit -m "feat: add new utility script for [purpose]

   - Brief description
   - What it does
   - Where it goes
   - Dependencies"
   ```

### Script Guidelines

- **Naming:** Kebab-case for filenames (my-script.sh)
- **Shebang:** `#!/bin/bash` for bash, `#!/usr/bin/env python` for Python
- **Help:** Include `-h/--help` option
- **Errors:** Use meaningful error messages
- **Logging:** Use logging functions from scripts/lib/
- **Testing:** Include test cases if applicable
- **Compatibility:** Test on bash 4.0+ and Python 3.8+

### Script Template (Bash)

```bash
#!/bin/bash

##
# Script Name
#
# Purpose: What this script does
# Date: YYYY-MM-DD
# Requirements: bash, git, [other tools]
#
# Usage:
#   bash scripts/script-name.sh [options] [args]
#
# Options:
#   --help   Show this help message
#   --flag   Description of flag
##

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --help)
      head -20 "$0" | tail -18
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Main logic
main() {
  echo "Script executing..."
}

main "$@"
```

### Script Template (Python)

```python
#!/usr/bin/env python

"""
Script Name

Purpose: What this script does
Date: YYYY-MM-DD
Requirements: Python 3.8+
"""

import argparse
import sys

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("--help", help="Show help message")
    args = parser.parse_args()
    
    print("Script executing...")

if __name__ == "__main__":
    main()
```

---

## Synchronization

### Branch Strategy

- **orchestration-tools** - Source of truth for infrastructure
- **scientific** - Development branch
- **main** - Production branch

### Sync Mechanism

1. Changes committed to orchestration-tools
2. Post-commit hook offers propagation
3. Auto-merge to scientific and main
4. Verify on all branches before deployment

### Manual Sync (if needed)

```bash
# From orchestration-tools
git checkout scientific
git merge orchestration-tools

git checkout main
git merge orchestration-tools

git push origin scientific main
```

### Verify Sync

```bash
# Check which branches have a script
git show orchestration-tools:scripts/markdown/lint-and-format.sh
git show scientific:scripts/markdown/lint-and-format.sh
git show main:scripts/markdown/lint-and-format.sh
```

---

## Troubleshooting

### Script Not Found

```bash
# List all scripts
find scripts -type f -name "*.sh" -o -name "*.py"

# Search for script by name
find scripts -name "*pattern*"

# See inventory
cat SCRIPTS_INVENTORY.md
```

### Permission Denied

```bash
# Make script executable
chmod +x scripts/your-script.sh

# Batch fix
chmod +x scripts/**/*.sh
```

### Hook Not Running

```bash
# Check hooks installed
ls -la .git/hooks/

# Reinstall
bash scripts/install-hooks.sh

# Check hook status
bash scripts/orchestration_status.sh
```

### Dependency Missing

```bash
# Verify dependencies
python scripts/verify-dependencies.py

# Install npm packages
npm install --save-dev prettier markdownlint-cli

# Install Python packages
python launch.py --setup
```

---

## Related Documentation

- [SCRIPTS_INVENTORY.md](./SCRIPTS_INVENTORY.md) - Complete script registry
- [SCRIPTS_SYNC_STATUS.md](./SCRIPTS_SYNC_STATUS.md) - Synchronization tracking
- [DEPENDENCIES.md](./DEPENDENCIES.md) - Dependency documentation
- [markdown/README.md](./markdown/README.md) - Markdown script guide
- [../AGENTS.md](../AGENTS.md) - Agent integration
- [../README.md](../README.md) - Main project README

---

## Statistics

| Metric | Value |
| --- | --- |
| Total scripts | 100+ |
| Categories | 16+ |
| Languages | bash, python |
| Configuration files | 2+ |
| Documentation files | 3+ |

---

## Quick Reference

```bash
# Get help on any script
bash scripts/script-name.sh --help
python scripts/script-name.py --help

# Format markdown (use anytime)
bash scripts/markdown/lint-and-format.sh --fix --all

# Check dependencies
python scripts/verify-dependencies.py

# List all scripts
find scripts -type f | sort

# Search for script
find scripts -name "*keyword*"

# See detailed inventory
cat SCRIPTS_INVENTORY.md
```

---

**Status:** Production Ready  
**Last Updated:** December 11, 2025  
**Maintainer:** Script Management System
