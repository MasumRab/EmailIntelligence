# Specification: Centralized Orchestration Distribution Script

## Overview
Replace distributed file distribution logic currently scattered across git hooks with a single, SOLID-designed centralized orchestration distribution script. This script will be the single source of truth for distributing orchestration files across branches.

## Current State Analysis
### Distributed Logic Issues
- File distribution scattered across post-commit, post-merge, post-checkout hooks
- `post-commit-setup-sync` duplicates work
- No single source of truth
- Difficult to maintain and debug
- Risk of inconsistency between hooks

### Current Distribution Targets
- Setup directory (`setup/`) files
- Git hooks (`post-commit`, `post-merge`, etc.)
- Configuration files (`.flake8`, `.pylintrc`, `.gitignore`)
- Root wrapper script (`launch.py`)

## New Script Requirements

### 1. Single Source of Truth
- `scripts/distribute-orchestration-files.sh` - Single entry point for all distribution
- Replace all distribution logic in git hooks
- Clear, testable, maintainable

### 2. Distribution Strategy
- Orchestration-tools* branches: Distribute from central setup/
- Taskmaster* branches: Isolated (no distribution)
- Main/Scientific branches: No orchestration involvement

### 3. Distribution Configuration
```json
{
  "distribution_rules": {
    "orchestration-tools": {
      "allowed_sources": ["setup/", "scripts/hooks/", "config/", "root_wrapper"],
      "target_branches": ["orchestration-tools*"],
      "file_patterns": ["*.sh", "*.py", "*.md", "*.json", ".*ignore", ".*cfg"]
    },
    "taskmaster": {
      "allowed_sources": [],
      "target_branches": [],
      "file_patterns": []
    }
  }
}
```

### 4. Safety Features
- Dry-run mode for previewing distribution
- Branch validation to prevent wrong-target distribution
- Conflict detection and resolution options
- Rollback capability for accidental distributions

### 5. Operation Modes
- `--dry-run`: Show what would be distributed without making changes
- `--verify`: Verify integrity of distributed files
- `--rollback`: Rollback to previous distribution state
- `--selective`: Distribute only specific file types (setup-only, hooks-only, config-only)
- `--force`: Override safety checks (with confirmation)

## Script Architecture

### Core Functions
```bash
# Distribute setup files
distribute_setup_files() {
  # Copy from setup/ directory to target locations
}

# Distribute git hooks
distribute_hooks() {
  # Copy hooks to .git/hooks/ directory
}

# Distribute configuration files
distribute_configs() {
  # Copy config files preserving permissions
}

# Validate distribution targets
validate_targets() {
  # Check if target branches exist and are safe to modify
}
```

### Safety Validation
```bash
# Check if on allowed branch
is_distribution_allowed() {
  # Return true only for orchestration-tools* branches
}

# Check for pending changes
has_pending_changes() {
  # Return true if there are uncommitted changes
}

# Verify target integrity
verify_target_integrity() {
  # Check if target files are safe to overwrite
}
```

## Migration Plan

### Phase 1: Script Creation
1. Create `scripts/distribute-orchestration-files.sh` with basic functionality
2. Define distribution rules configuration
3. Implement safety validation functions

### Phase 2: Hook Simplification
1. Remove all distribution logic from git hooks
2. Keep only validation and safety checks in hooks
3. Update hook documentation

### Phase 3: Integration & Testing
1. Test distribution script with all branch types
2. Verify hooks work with reduced scope
3. Document new orchestration workflow

## Usage Examples

### Basic Distribution
```bash
# Distribute all files to orchestration-tools branches
./scripts/distribute-orchestration-files.sh

# Preview distribution without making changes
./scripts/distribute-orchestration-files.sh --dry-run

# Distribute only setup files
./scripts/distribute-orchestration-files.sh --setup-only

# Verify distribution integrity
./scripts/distribute-orchestration-files.sh --verify
```

### Selective Distribution
```bash
# Distribute specific file types
./scripts/distribute-orchestration-files.sh --hooks-only
./scripts/distribute-orchestration-files.sh --config-only

# Force distribution with warning
./scripts/distribute-orchestration-files.sh --force
```

## Error Handling
- Comprehensive error messages for failed distributions
- Graceful degradation when targets are unavailable
- Detailed logging of distribution operations
- Automatic rollback on critical failures

## Configuration
- JSON-based distribution rules
- Branch-specific distribution patterns
- Exclusion lists for sensitive files
- Custom target mappings

## Integration Points
- Called by: user, CI/CD, git hooks (minimal integration)
- Integrates with existing launch.py workflow
- Compatible with worktree setup
- Maintains branch isolation requirements

## Testing Requirements
- Unit tests for distribution functions
- Integration tests with branch workflows
- Dry-run validation tests
- Rollback functionality tests
- Cross-branch distribution tests

## Success Criteria
- [ ] Distribution script successfully distributes all files
- [ ] All hooks reduced to <60 lines each
- [ ] All tests passing (unit + integration + hook)
- [ ] No regression in branch safety
- [ ] Easier to maintain and debug
- [ ] User can understand workflow in <5 minutes
- [ ] Single source of truth established