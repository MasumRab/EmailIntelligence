# Specification: Centralized Orchestration Distribution Script (Enhanced)

## Overview
Replace distributed file distribution logic currently scattered across git hooks with a single, SOLID-designed centralized orchestration distribution script. This script will be the single source of truth for distributing orchestration files across branches, with improved user feedback and alignment with existing documentation.

## Functional Requirements

### 1. Distribution from Latest Remote
The script MUST always distribute from the latest remote version of orchestration-tools* branches:
- Pull latest changes from origin/orchestration-tools before distribution
- Verify the commit hash is the latest before proceeding
- Warn if local version is outdated
- Provide option to update to latest before distribution

### 2. Branch Isolation
- Orchestration-tools* branches: Full distribution from orchestration-tools
- Taskmaster* branches: No distribution (maintain isolation)
- Main/Scientific branches: No orchestration files distributed

### 3. Safety & Validation
- Dry-run mode to preview distribution
- Verification of distribution targets
- Conflict detection and resolution options
- Rollback capability for accidental distributions
- Validation against existing documentation patterns

### 4. User Experience & Feedback
- Clear progress indicators
- Detailed success/failure messages with actionable next steps
- Alignment with documented workflows
- Integration suggestions for common project goals

## Enhanced User Suggestions & Project Goal Alignment

### A. Integration with Existing Documentation
The script should align with and enhance the following documented workflows:

1. **Task Master Integration** (AGENTS.md):
   - Ensure orchestration files don't interfere with Task Master workflows
   - Provide feedback on how orchestration can support Task Master goals
   - Suggest Task Master commands when appropriate during distribution

2. **Branch Orchestration Guidelines** (TASKMASTER_BRANCH_CONVENTIONS.md):
   - Follow worktree isolation principles (git naturally handles .taskmaster/)
   - Maintain documented branch conventions
   - Preserve Task Master branch isolation requirements

3. **Orchestration Process Guide** (ORCHESTRATION_PROCESS_GUIDE.md):
   - Align with existing Strategy 5/7 workflows
   - Support branch aggregation patterns
   - Maintain context contamination prevention

### B. Feedback for Project Goals
The script should provide specific feedback on how to achieve these project goals:
- **Goal**: Maintain consistency across orchestration-tools branches
  - **Suggestion**: "Use --verify flag after distribution to ensure consistency"
- **Goal**: Prevent context contamination
  - **Suggestion**: "Run ./scripts/validate-orchestration-context.sh after distribution"
- **Goal**: Maintain branch safety
  - **Suggestion**: "Verify hooks with scripts/install-hooks.sh --verify"

### C. Project Goal Alignment Features
- Output distribution summary with links to related documentation
- Suggest next steps based on current branch and project state
- Recommend validation commands after successful distribution
- Provide troubleshooting suggestions for common issues

## Technical Requirements

### 1. Distribution Configuration
```json
{
  "sources": {
    "orchestration-tools": {
      "remote": "origin/orchestration-tools",
      "directories": ["setup/", "scripts/hooks/", "scripts/lib/", "config/"],
      "files": [".flake8", ".pylintrc", ".gitignore", "launch.py"],
      "validation_script": "scripts/validate-orchestration-context.sh"
    }
  },
  "targets": {
    "orchestration-tools-*": {
      "allowed": true,
      "sync_method": "git-worktree-safe",
      "validation_after_sync": true
    },
    "taskmaster-*": {
      "allowed": false,
      "reason": "worktree-isolation-required"
    },
    "other": {
      "allowed": false,
      "reason": "orchestration-not-applicable"
    }
  }
}
```

### 2. Operation Modes
- `--sync-from-remote`: Force pull latest from remote before distribution
- `--dry-run`: Show what would be distributed without making changes
- `--verify-integrity`: Verify all distributed files match source
- `--rollback`: Revert to previous distribution state
- `--selective`: Distribute only specific file types
- `--with-validation`: Run validation scripts after distribution
- `--interactive`: Prompt for each major action

### 3. Safety Features
- Remote validation: Verify remote branch exists and is accessible
- Commit validation: Ensure using latest commit from remote
- Branch validation: Verify target branch is safe for distribution
- File validation: Check for conflicts before overwriting

## Script Architecture

### Core Functions
```bash
# Synchronize from remote orchestration-tools branch
sync_from_remote() {
    local source_branch="$1"
    echo "Pulling latest from $source_branch..."
    git fetch origin "$source_branch" || { echo "ERROR: Could not fetch from $source_branch"; return 1; }
    
    # Verify this is the latest commit
    local remote_hash=$(git rev-parse "origin/$source_branch")
    local local_hash=$(git rev-parse HEAD)
    
    if [[ "$remote_hash" != "$local_hash" ]]; then
        echo "INFO: Local branch is not at latest commit"
        echo "Remote: $remote_hash"
        echo "Local:  $local_hash"
        read -p "Update to latest remote commit? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git reset --hard "$remote_hash"
            echo "Updated to latest remote commit"
        else
            echo "WARNING: Using outdated local version for distribution"
        fi
    fi
}

# Distribute orchestration files
distribute_files() {
    local target_branch="$1"
    local distribution_type="$2"  # all, setup-only, hooks-only, config-only
    
    echo "Distributing orchestration files to: $target_branch"
    # Implementation details...
}

# Validate distribution targets
validate_targets() {
    local branch="$1"
    # Check if branch is safe for orchestration distribution
    if [[ "$branch" == taskmaster* ]]; then
        echo "ERROR: Cannot distribute to taskmaster branches (worktree isolation required)"
        return 1
    fi
    return 0
}

# Provide project-aligned feedback
provide_feedback() {
    local distribution_result="$1"
    echo "✅ Distribution completed successfully!"
    echo ""
    echo "📝 Next recommended steps:"
    echo "  1. Verify distribution: scripts/validate-orchestration-context.sh"
    echo "  2. Test hooks: scripts/install-hooks.sh --verify"
    echo "  3. Check branch consistency: scripts/validate-branch-propagation.sh"
    echo ""
    echo "🔗 Related documentation:"
    echo "  - ORCHESTRATION_PROCESS_GUIDE.md (Strategy 5/7 workflows)"
    echo "  - TASKMASTER_BRANCH_CONVENTIONS.md (branch isolation)"
    echo "  - AGENTS.md (Task Master integration)"
}
```

## Usage Examples with Feedback

### Basic Distribution
```bash
# Full distribution with validation
./scripts/distribute-orchestration-files.sh --with-validation

# Preview distribution with detailed feedback
./scripts/distribute-orchestration-files.sh --dry-run

# Align with project goals
./scripts/distribute-orchestration-files.sh --sync-from-remote --with-validation
```

### Selective Distribution
```bash
# Distribute specific file types with goal-oriented feedback
./scripts/distribute-orchestration-files.sh --setup-only --with-validation
# Feedback: "Setup files distributed. To maintain consistency, consider running validation scripts."
```

## User Experience Enhancements

### 1. Goal-Oriented Feedback
After successful distribution, the script should suggest:
- How this distribution helps achieve project goals
- Next steps to maintain consistency
- Links to relevant documentation
- Validation commands to run

### 2. Alignment with Documentation
- Reference AGENTS.md for Task Master integration
- Follow TASKMASTER_BRANCH_CONVENTIONS.md for isolation
- Align with ORCHESTRATION_PROCESS_GUIDE.md workflows
- Support STRATEGY 5/7 implementation

### 3. Common Project Goal Suggestions
- "To maintain branch consistency, schedule regular distributions"
- "After distribution, verify with: scripts/validate-orchestration-context.sh"
- "For Task Master integration, ensure no conflicts with .taskmaster/ worktree"

## Error Handling & Safety
- Comprehensive error messages with suggested resolutions
- Graceful degradation when targets are unavailable
- Detailed logging of all distribution operations
- Automatic safety checks before each distribution
- Clear warnings for potentially problematic operations

## Integration Points
- Called by: user workflow, CI/CD pipelines, maintenance scripts
- Integrates with existing launch.py orchestration
- Compatible with worktree setup
- Maintains all branch isolation requirements per documentation

## Testing Requirements
- Unit tests for all distribution functions
- Integration tests with documented workflows
- Dry-run validation accuracy tests
- Rollback functionality verification
- Cross-branch distribution safety tests
- Remote synchronization verification

## Success Criteria
- [ ] Distribution script successfully distributes from latest remote version
- [ ] All safety validations pass before any file changes
- [ ] Distribution respects branch isolation requirements
- [ ] User receives actionable feedback aligned with project goals
- [ ] Script integrates seamlessly with existing documentation workflows
- [ ] Comprehensive error handling with helpful suggestions
- [ ] All tests passing (unit + integration + safety checks)
- [ ] Users can achieve project goals with clear guidance
- [ ] Alignment with documented orchestration processes
- [ ] No conflicts with existing Task Master workflows