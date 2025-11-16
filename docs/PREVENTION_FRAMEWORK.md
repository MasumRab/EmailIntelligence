# Agentic Tool Prevention Framework

## Objective

Prevent future contamination of TaskMaster branch and misplaced commits by implementing validation frameworks that constrain agentic tool behavior.

---

## 1. Pre-Commit Validation Hook

### Location
`.git/hooks/pre-commit` (in taskmaster worktree)

### Implementation

```bash
#!/bin/bash
# Pre-commit validation for agentic operations

set -e

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔍 Running pre-commit validation..."

# 1. Check if .taskmaster directory is being tracked
if git ls-files | grep -q "^\.taskmaster/"; then
    echo -e "${RED}❌ ERROR: Attempting to track .taskmaster directory${NC}"
    echo "   .taskmaster is a git worktree and must NOT be tracked in parent repo"
    exit 1
fi

# 2. Protect critical files from deletion
CRITICAL_FILES=(
    "tasks/tasks.json"
    "state.json"
    "config.json"
)

for file in "${CRITICAL_FILES[@]}"; do
    if git diff --cached --diff-filter=D --name-only | grep -q "^${file}$"; then
        echo -e "${RED}❌ ERROR: Attempting to delete critical file: $file${NC}"
        echo "   Critical files require explicit user confirmation and backup"
        echo "   Use: git commit --allow-empty -m 'Message' after manual review"
        exit 1
    fi
done

# 3. Warn on large file deletions
DELETED_FILES=$(git diff --cached --diff-filter=D --name-only | wc -l)
if [ "$DELETED_FILES" -gt 3 ]; then
    echo -e "${YELLOW}⚠️  WARNING: Deleting $DELETED_FILES files${NC}"
    echo "   Large bulk deletions should be reviewed carefully"
    read -p "   Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 4. Validate no nested .taskmaster creation
if git diff --cached --name-only | grep -q "\.taskmaster/"; then
    echo -e "${RED}❌ ERROR: Modifications to .taskmaster detected${NC}"
    echo "   .taskmaster is managed independently in worktree"
    echo "   This branch should not track .taskmaster files"
    exit 1
fi

# 5. Validate file ownership (branch-specific)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

case "$BRANCH" in
    "taskmaster")
        # Only allow: tasks/*, docs/prd.txt, state.json, config.json, reports/*
        ALLOWED_PATTERNS=(
            "^tasks/"
            "^docs/prd\.txt"
            "^state\.json"
            "^config\.json"
            "^reports/"
            "^docs/.*\.md$"
        )
        ;;
    "orchestration-tools-changes")
        # Only allow: scripts/*, .gitignore (orchestration entries), docs (orchestration-specific)
        ALLOWED_PATTERNS=(
            "^scripts/"
            "^\.gitignore"
            "^docs/orchestration"
        )
        ;;
    *)
        # Default: prevent taskmaster file modifications
        ALLOWED_PATTERNS=()
        ;;
esac

if [ ${#ALLOWED_PATTERNS[@]} -gt 0 ]; then
    while IFS= read -r file; do
        MATCHED=0
        for pattern in "${ALLOWED_PATTERNS[@]}"; do
            if [[ "$file" =~ $pattern ]]; then
                MATCHED=1
                break
            fi
        done
        
        if [ $MATCHED -eq 0 ]; then
            echo -e "${RED}❌ ERROR: File not allowed on branch '$BRANCH': $file${NC}"
            echo "   This branch is restricted to specific file types"
            exit 1
        fi
    done < <(git diff --cached --name-only)
fi

echo -e "${GREEN}✅ Pre-commit validation passed${NC}"
exit 0
```

---

## 2. Branch Policy Configuration File

### Location
`.taskmaster/.gitattributes.branch-policy`

### Format

```ini
# Branch: taskmaster
# Purpose: Task management, configuration, and task-related documentation
# OWNS: Task definitions, configuration, task reports
# NEVER_TOUCH: orchestration scripts, application code, nested .taskmaster

[taskmaster]
OWNED_FILES=tasks/*, state.json, config.json, reports/*, docs/prd.txt
PROTECTED_FILES=tasks/tasks.json, state.json, config.json
FORBIDDEN_FILES=.taskmaster/*, scripts/hooks/*, src/*, backend/*
ALLOW_RESTRUCTURING=false
ALLOW_NESTED_DIRECTORIES=false
REQUIRES_CONFIRMATION_FOR_DELETE=true
AUDIT_LOGGING=true

# Branch: orchestration-tools-changes  
# Purpose: Infrastructure and orchestration tool modifications
# OWNS: Orchestration scripts, hooks, orchestration-specific configuration
# NEVER_TOUCH: Task files, application code, worktree files

[orchestration-tools-changes]
OWNED_FILES=scripts/*, deployment/*, .gitignore
PROTECTED_FILES=scripts/sync_setup_worktrees.sh, scripts/hooks/*
FORBIDDEN_FILES=.taskmaster/*, tasks/*, config.json, state.json
ALLOW_RESTRUCTURING=false
ALLOW_NESTED_DIRECTORIES=false
REQUIRES_CONFIRMATION_FOR_DELETE=true
AUDIT_LOGGING=true

# Branch: main
# Purpose: Application code and user-facing documentation
# OWNS: Source code, application documentation
# NEVER_TOUCH: Task files, orchestration scripts, worktree files

[main]
OWNED_FILES=src/*, README.md, docs/user_guide*, LICENSE
PROTECTED_FILES=src/core/*, src/backend/*
FORBIDDEN_FILES=.taskmaster/*, tasks/*, orchestration/*, scripts/hooks/*
ALLOW_RESTRUCTURING=false
ALLOW_NESTED_DIRECTORIES=false
REQUIRES_CONFIRMATION_FOR_DELETE=false
AUDIT_LOGGING=true
```

---

## 3. Architecture Documentation for Agentic Tools

### Location
`.taskmaster/docs/ARCHITECTURE_CONSTRAINTS.md` (NEW)

### Content

```markdown
# TaskMaster Architecture Constraints for Agentic Tools

## Critical Constraints

### 1. Worktree Structure (IMMUTABLE)
- `.taskmaster/` is a git worktree, NOT a nested directory
- Worktrees have independent git state and working directories
- NEVER attempt to track .taskmaster files in parent repository
- NEVER create nested .taskmaster structures
- NEVER flatten or move .taskmaster contents

**Validation**: If modifying any `.taskmaster/*` file, stop and ask user

### 2. File Ownership (ENFORCED)

#### TaskMaster Branch OWNS:
- `tasks/*.json` - Task definitions
- `state.json` - Task execution state
- `config.json` - TaskMaster configuration
- `reports/` - Task analysis and reports
- `docs/prd*.txt` - Product requirement documents
- `docs/*.md` - Task-related documentation

#### TaskMaster Branch MUST NOT TOUCH:
- Anything in parent repository
- Orchestration scripts (scripts/hooks/*, scripts/sync_*, etc.)
- Application code (src/*, backend/*)
- Configuration files that don't belong to TaskMaster

#### Orchestration-Tools Branch OWNS:
- `scripts/` - Orchestration and deployment scripts
- `.gitignore` entries for orchestration
- Hook management files
- Orchestration-specific documentation

#### Orchestration-Tools Branch MUST NOT TOUCH:
- Task files (tasks/*, state.json, config.json)
- Application code
- Any .taskmaster worktree files

### 3. Critical Files (PROTECTED)

These files must NEVER be deleted without explicit user confirmation:
- `tasks/tasks.json` - Primary task database
- `state.json` - Execution state
- Any file containing task definitions

**Safeguard**: Require 3-part confirmation for deletion:
1. Explicit --force flag
2. Backup verification
3. Rollback plan in commit message

### 4. Structural Constraints (IMMUTABLE)

PROHIBITED operations:
- ❌ Creating nested .taskmaster/ directories
- ❌ Attempting to track .taskmaster as submodule
- ❌ Flattening or moving .taskmaster contents
- ❌ Renaming .taskmaster to anything else
- ❌ Modifying .taskmaster parent references

ALLOWED operations:
- ✅ Modifying content within taskmaster worktree
- ✅ Creating/deleting tasks and reports
- ✅ Updating configuration
- ✅ Adding documentation

### 5. Branch-Specific Constraints

#### When on taskmaster branch:
- Only commit to tasks/, state.json, config.json, reports/, docs/
- NEVER commit orchestration scripts
- NEVER attempt .taskmaster restructuring
- NEVER delete critical task files without confirmation

#### When on orchestration-tools-changes:
- Only commit to scripts/, orchestration documentation
- NEVER commit task files
- NEVER touch .taskmaster directory
- NEVER delete application code

#### When on main/feature branches:
- NEVER touch task files (tasks/*, state.json, config.json)
- NEVER attempt .taskmaster modifications
- NEVER commit orchestration infrastructure changes
- These belong on orchestration-tools-changes instead

## Decision Tree for Agentic Tools

```
Is this a modification related to task management?
├─ YES → Is it file ownership validation? (tasks/*, state.json, etc.)
│  ├─ YES → Route to taskmaster branch
│  └─ NO → STOP - unclear file ownership, ask user
│
└─ NO → Is this related to orchestration/infrastructure?
   ├─ YES → Route to orchestration-tools-changes branch
   ├─ NO → Check if it's application code → Route to main
   └─ UNCLEAR → STOP - unknown file ownership, ask user
```

## Pre-Commit Validation Requirements

Before committing, agentic tools MUST:

1. Verify branch purpose matches commit content
2. Validate all files belong to branch's owned files list
3. Check that no protected files are being deleted
4. Ensure no .taskmaster directory modifications
5. Confirm no structural changes to architecture
6. Log operation for audit trail

## Agentic Tool Checklist

Before ANY commit:
- [ ] Verified current branch matches commit purpose
- [ ] Checked all modified files against file ownership rules
- [ ] Confirmed no critical files are being deleted
- [ ] Validated no .taskmaster directory modifications
- [ ] Ensured no structural/architectural changes
- [ ] Reviewed commit message for clarity
- [ ] Ran pre-commit validation hook successfully
```

---

## 4. Audit Logging for Agentic Operations

### Location
`.taskmaster/logs/agentic-audit.log`

### Format

```log
[2025-11-16T17:00:00Z] BRANCH: taskmaster
[2025-11-16T17:00:00Z] AGENT: Amp/Claude Code
[2025-11-16T17:00:00Z] OPERATION: commit
[2025-11-16T17:00:00Z] FILES_MODIFIED: tasks/tasks.json, state.json
[2025-11-16T17:00:00Z] FILES_DELETED: 0
[2025-11-16T17:00:00Z] VALIDATION_STATUS: PASSED
[2025-11-16T17:00:00Z] COMMIT_HASH: 72f1e28c
[2025-11-16T17:00:00Z] MESSAGE: docs: Add contamination analysis
[2025-11-16T17:00:00Z] RISK_ASSESSMENT: LOW
[2025-11-16T17:00:00Z] ---
```

### Automated Audit Logging

```bash
#!/bin/bash
# Post-commit audit logging

COMMIT_HASH=$(git rev-parse HEAD)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

LOG_FILE=".taskmaster/logs/agentic-audit.log"

# Check if commit appears to be from agentic tool
if [[ "$(git log -1 --format=%B)" =~ "Amp-Thread-ID:|Co-authored-by: Amp|Task Master|task-master" ]]; then
    echo "[$TIMESTAMP] BRANCH: $BRANCH" >> "$LOG_FILE"
    echo "[$TIMESTAMP] AGENT: Amp/Claude Code" >> "$LOG_FILE"
    echo "[$TIMESTAMP] OPERATION: commit" >> "$LOG_FILE"
    echo "[$TIMESTAMP] FILES_MODIFIED: $(git diff-tree --no-commit-id --name-only -r $COMMIT_HASH | tr '\n' ', ')" >> "$LOG_FILE"
    echo "[$TIMESTAMP] FILES_DELETED: $(git diff-tree --no-commit-id --diff-filter=D --name-only -r $COMMIT_HASH | wc -l)" >> "$LOG_FILE"
    echo "[$TIMESTAMP] VALIDATION_STATUS: PASSED" >> "$LOG_FILE"
    echo "[$TIMESTAMP] COMMIT_HASH: $COMMIT_HASH" >> "$LOG_FILE"
    echo "[$TIMESTAMP] MESSAGE: $(git log -1 --format=%s)" >> "$LOG_FILE"
    echo "[$TIMESTAMP] ---" >> "$LOG_FILE"
fi
```

---

## 5. Implementation Checklist

### Phase 1: Documentation (Week 1)
- [ ] Add ARCHITECTURE_CONSTRAINTS.md to .taskmaster/docs/
- [ ] Update AGENTS.md with explicit worktree warnings
- [ ] Add BRANCH_PROPAGATION_POLICY.md to .github/
- [ ] Document file ownership rules in both locations

### Phase 2: Validation Hooks (Week 2)
- [ ] Implement pre-commit hook with branch policy validation
- [ ] Add critical file protection in hook
- [ ] Test with intentional violations
- [ ] Add audit logging to post-commit hook

### Phase 3: Configuration (Week 2-3)
- [ ] Create .gitattributes.branch-policy file
- [ ] Define file ownership patterns per branch
- [ ] Configure protected files list
- [ ] Set up audit logging infrastructure

### Phase 4: Testing & Deployment (Week 3-4)
- [ ] Test prevention framework with agentic tool operations
- [ ] Simulate contamination scenarios to verify prevention
- [ ] Deploy hooks to all worktrees
- [ ] Create monitoring dashboard for audit logs

### Phase 5: Monitoring (Ongoing)
- [ ] Review audit logs weekly
- [ ] Monitor for validation failures
- [ ] Update documentation based on real-world usage
- [ ] Track agentic tool error patterns

---

## 6. Fallback Procedures

### If Prevention Framework Fails

1. **Detect contamination**:
   - Monitor audit logs for VALIDATION_STATUS: FAILED
   - Review branch pollution through git diff
   - Identify affected commits via git bisect

2. **Isolate damage**:
   ```bash
   git revert <bad-commit>  # Revert contaminating commit
   git reset --hard origin/<branch>  # If severe, reset to known-good
   ```

3. **Recover lost files**:
   - Check git history for file resurrection
   - Use reflog to recover lost objects
   - Restore from last known-good state

4. **Document incident**:
   - Add entry to CONTAMINATION_INCIDENTS_SUMMARY.md
   - Analyze root cause using contamination framework
   - Update prevention measures

---

## 7. Metrics & Monitoring

### Key Metrics to Track

- **Prevention Success Rate**: % of operations that pass validation
- **Contamination Rate**: Incidents per 100 agentic commits
- **Detection Time**: Average time to detect contamination
- **Remediation Time**: Time to fix contamination
- **Rule Violations**: Number of attempted violations caught by hooks

### Monitoring Dashboard (Conceptual)

```
Agentic Tool Contamination Prevention Dashboard
==================================================

Last 7 Days:
- Operations Attempted:  847
- Validation Passed:     841 (99.3%)
- Validation Failed:     6   (0.7%) ← Alert if > 2%
- Contamination Incidents: 0 (Target: 0)

Branch Status:
- taskmaster:        ✅ Clean
- orchestration-tools-changes: ✅ Clean  
- main:             ✅ Clean

Recent Validation Failures:
1. Nov 16, 14:22 - Attempted to track .taskmaster on main
2. Nov 16, 12:15 - Tried to delete tasks.json without confirmation

Action Items:
- Review .taskmaster tracking prevention
- Verify critical file protection
```

---

## Summary

This framework provides **layered prevention**:

1. **Pre-commit validation** - Catches issues before they enter git
2. **Branch policy enforcement** - Routes changes to correct branches
3. **Critical file protection** - Prevents data loss
4. **Audit logging** - Enables forensic analysis
5. **Architecture documentation** - Guides agentic tool decision-making

Combined, these measures eliminate the root causes identified in contamination analysis while maintaining agentic tool productivity.
