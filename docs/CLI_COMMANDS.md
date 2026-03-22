# CLI Commands Reference

## Overview

The EmailIntelligence CLI provides two command systems:

1. **Legacy System**: Original command structure (deprecated)
2. **Modular System**: New SOLID-based command architecture (recommended)

All examples use the modular system unless otherwise noted.

---

## Command Usage

### analyze

Analyze repository conflicts between branches.

**Usage:**
```bash
eai modular analyze <repo_path> [options]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `repo_path` | Path to the repository | Required |
| `--pr PR_ID` | Pull Request ID | None |
| `--base-branch BRANCH` | Base branch for comparison | main |
| `--head-branch BRANCH` | Head branch for comparison | current |

**Examples:**
```bash
# Analyze current branch against main
eai modular analyze /path/to/repo

# Analyze specific branches
eai modular analyze /path/to/repo --base-branch develop --head-branch feature/new

# Analyze with PR context
eai modular analyze /path/to/repo --pr 123 --base-branch main --head-branch feature/test
```

**Output:**
```
Analyzing repository at /path/to/repo...
Comparing branches: main <- feature/new
Found 3 conflicts.
Conflict conflict-test-123: Risk=HIGH, Score=0.85
  Strategy: standard_resolution
    - Resolve conflict in test.py
```

**Exit Codes:**
- `0`: Analysis completed successfully
- `1`: Error occurred (invalid path, missing branch, etc.)

---

### resolve

Resolve a specific conflict using a strategy.

**Usage:**
```bash
eai modular resolve <conflict_id> <strategy_id>
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `conflict_id` | ID of the conflict to resolve |
| `strategy_id` | ID of the strategy to apply |

**Examples:**
```bash
eai modular resolve conflict-abc123 strategy-xyz789
```

**Output:**
```
Resolving conflict conflict-abc123 with strategy strategy-xyz789...
Resolution successful: Conflict resolved using strategy
```

**Exit Codes:**
- `0`: Resolution completed successfully
- `1`: Error occurred or resolution failed

---

### validate

Run validation checks on the codebase.

**Usage:**
```bash
eai modular validate
```

**Examples:**
```bash
# Run validation
eai modular validate
```

**Output:**
```
Running validation...
[PASS] files: True

Validation complete: 1 passed, 0 failed
```

**Exit Codes:**
- `0`: All validations passed
- `1`: One or more validations failed

---

### analyze-history

Analyze git commit history and patterns.

**Usage:**
```bash
eai modular analyze-history [options]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--branch BRANCH` | Branch to analyze | HEAD |
| `--output FILE` | Output file for report | None |

**Examples:**
```bash
# Analyze current branch
eai modular analyze-history

# Analyze specific branch with output
eai modular analyze-history --branch main --output history_report.txt
```

**Output:**
```
Analyzing history for branch: main...

Analysis Report for main
Total Commits: 150

By Category:
  - feat: 45
  - fix: 30
  - docs: 15
  - refactor: 10
  - test: 20
  - chore: 20
  - other: 10

By Risk:
  - LOW: 100
  - MEDIUM: 35
  - HIGH: 15
```

**Exit Codes:**
- `0`: Analysis completed successfully
- `1`: Error occurred

---

### plan-rebase

Generate an optimal rebase plan for a branch.

**Usage:**
```bash
eai modular plan-rebase --output <file> [options]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--branch BRANCH` | Branch to plan rebase for | HEAD |
| `--output FILE` | Output file for plan (required) | None |

**Examples:**
```bash
# Generate rebase plan
eai modular plan-rebase --output rebase_plan.txt

# Plan for specific branch
eai modular plan-rebase --branch feature/test --output rebase_plan.txt
```

**Output:**
```
Planning rebase for branch: feature/test...
Rebase plan saved to rebase_plan.txt
Plan contains 25 commits organized into phases
```

**Plan Format** (rebase_plan.txt):
```markdown
# Automated Rebase Plan

## Phase 1: Critical & Infrastructure
pick abc1234 Initial commit
pick def5678 Add security headers

## Phase 2: Features
pick ghi9012 Add user authentication
pick jkl3456 Add user profile

## Phase 3: Fixes
pick mno7890 Fix login bug
...

## Phase 4: Documentation & Cleanup
pick pqr1234 Update README
```

**Exit Codes:**
- `0`: Plan generated successfully
- `1`: Error occurred

---

## Command Mode Selection

### Using Legacy System (Deprecated)
```bash
eai legacy setup-resolution --pr 123 --source-branch feature/auth --target-branch main
```

### Using Modular System (Recommended)
```bash
eai modular analyze /path/to/repo
# or simply (if configured as default)
eai analyze /path/to/repo
```

---

## Error Handling

All commands follow these error handling conventions:

1. **Error Messages**: Printed to stderr with descriptive context
2. **Exit Codes**:
   - `0` = Success
   - `1` = Error occurred
3. **Stack Traces**: Only shown in debug mode (`--verbose`)

**Example Error Output:**
```
Error: Branch 'nonexistent' not found
```

---

## Global Options

| Option | Description |
|--------|-------------|
| `--help` | Show help message |
| `--verbose` | Enable verbose output |
| `--version` | Show version information |

---

## Exit Code Reference

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `2` | Invalid arguments |
| `3` | Repository not found |
| `4` | Branch not found |
| `5` | Conflict detection failed |

---

## Configuration

Commands read configuration from:

1. `~/.emailintelligence/config.yaml` (user-level)
2. `.emailintelligence/config.yaml` (project-level)
3. Environment variables (override)

---

## See Also

- [Command Specification](../COMMAND_SPECIFICATION.md) - Technical details
- [Architecture Documentation](../README.md) - System overview