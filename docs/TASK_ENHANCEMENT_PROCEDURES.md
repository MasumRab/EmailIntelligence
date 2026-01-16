# Task Enhancement Procedures

Guide for enhancing task markdown files using Task Master CLI and manual procedures.

> **See Also:** [COMPLETE_TASK_WORKFLOW.md](COMPLETE_TASK_WORKFLOW.md) for the master workflow reference.

---

## Quick Reference

| Field | Task Master Support | Procedure |
|-------|---------------------|-----------|
| Title | ✅ `update-task` | CLI |
| Description | ✅ `update-task` | CLI |
| Details | ✅ `update-task` / `update-subtask` | CLI |
| Status | ✅ `set-status` | CLI |
| Priority | ✅ `update-task` | CLI |
| Dependencies | ✅ `add-dependency` / `remove-dependency` | CLI |
| Complexity | ✅ `analyze-complexity` | CLI (generates report) |
| Success Criteria | ⚠️ `research` → Manual | Research + Embed |
| Test Strategy | ⚠️ `research` → Manual | Research + Embed |
| Effort | ⚠️ `research` → Manual | Research + Embed |
| Owner | ❌ Not supported | Manual + Embed |
| Implementation Notes | ⚠️ `research --save-to` | CLI or Manual |
| Progress Log | ⚠️ Partial via `update-subtask` | CLI + Manual |

---

## Task Master CLI Procedures

### 1. Update Task Title/Description/Details

```bash
# Update a single task with AI assistance
task-master update-task <id> <prompt>

# Examples:
task-master update-task 1 add more detail about branch identification steps
task-master update-task 2.3 include error handling requirements

# Update multiple tasks from a given ID onwards
task-master update --from=<id> --prompt="<context>"

# Example:
task-master update --from=3 --prompt="add security validation requirements to all tasks"
```

### 2. Update Subtask Details (Append Notes)

```bash
# Append implementation notes to a subtask
task-master update-subtask --id=<parentId.subtaskId> --prompt="<context>"

# Examples:
task-master update-subtask --id=1.1 --prompt="Completed branch discovery, found 12 active branches"
task-master update-subtask --id=2.3 --prompt="Using Jaccard similarity for diff distance calculation"
```

### 3. Change Task Status

```bash
# Set task status
task-master set-status --id=<id> --status=<status>

# Valid statuses: pending, in-progress, done, review, deferred, cancelled, blocked

# Examples:
task-master set-status --id=1.1 --status=in-progress
task-master set-status --id=1.1 --status=done
```

### 4. Manage Dependencies

```bash
# Add a dependency
task-master add-dependency --id=<id> --depends-on=<id>

# Remove a dependency
task-master remove-dependency --id=<id> --depends-on=<id>

# Validate all dependencies
task-master validate-dependencies

# Auto-fix invalid dependencies
task-master fix-dependencies

# Examples:
task-master add-dependency --id=2.4 --depends-on=2.1
task-master add-dependency --id=2.4 --depends-on=2.2
task-master add-dependency --id=2.4 --depends-on=2.3
```

### 5. Expand Tasks into Subtasks

```bash
# Expand a task into subtasks with AI
task-master expand --id=<id> --research --force

# Expand all eligible tasks
task-master expand --all --research

# Analyze complexity first (helps determine subtask count)
task-master analyze-complexity --research
task-master complexity-report
```

### 6. Analyze Task Complexity

```bash
# Analyze all tasks and generate complexity report
task-master analyze-complexity --research

# Analyze specific tasks
task-master analyze-complexity --id=1,2,3

# Analyze a range of tasks
task-master analyze-complexity --from=1 --to=5

# Set minimum threshold for expansion recommendations (1-10)
task-master analyze-complexity --threshold=7

# View the complexity report
task-master complexity-report
```

**Output:** Generates `.taskmaster/reports/task-complexity-report.json` with:
- Complexity score (1-10) for each task
- Expansion recommendations
- Suggested subtask counts

### 7. Research to Generate Success Criteria, Test Strategy, Effort

Use `task-master research` with custom prompts to generate content for unsupported fields, then manually embed.

#### Generate Success Criteria

```bash
# Research success criteria for a specific task
task-master research "Generate measurable success criteria for this task. Include P0 (must have), P1 (should have), and P2 (nice to have) priorities. Each criterion should be specific, measurable, and verifiable." --id=1 --save-file

# With project context
task-master research "What are the acceptance criteria for branch alignment tasks? Include validation methods." --id=1 --tree --save-file
```

#### Generate Test Strategy

```bash
# Research test strategy for a task
task-master research "Generate a comprehensive test strategy for this task. Include unit tests, integration tests, and manual validation steps. Specify test inputs, expected outputs, and coverage targets." --id=1 --save-file

# For implementation tasks
task-master research "What tests should be written for this feature? Include edge cases and error scenarios." --id=2.3 --files=src/branch_analyzer.py --save-file
```

#### Generate Effort Estimates

```bash
# Research effort estimate
task-master research "Estimate the effort required for this task in hours. Consider complexity, dependencies, testing, and documentation. Break down by subtask if applicable." --id=1 --save-file

# Compare with similar tasks
task-master research "Compare this task with similar implementations. What is a realistic effort estimate based on industry standards?" --id=1 --context="Team has 2 senior developers" --save-file
```

#### Save Research Directly to Task

```bash
# Save research output to a specific task's details
task-master research "Generate implementation notes and best practices" --id=1 --save-to=1

# Save to subtask
task-master research "What are the gotchas and common mistakes for this subtask?" --id=1.3 --save-to=1.3
```

#### Research Workflow for Task Enhancement

```bash
# 1. Generate success criteria
task-master research "Generate success criteria with measurable outcomes" --id=1 --save-file

# 2. Generate test strategy  
task-master research "Generate test strategy with unit/integration/validation" --id=1 --save-file

# 3. Generate effort estimate
task-master research "Estimate effort in hours with breakdown" --id=1 --save-file

# 4. View saved research
ls .taskmaster/docs/research/

# 5. Copy relevant content to task markdown file
# 6. Add EXTENDED_METADATA block
# 7. Embed to tasks.json
python scripts/task_metadata_manager.py embed --task 001
```

**Research Output Location:** `.taskmaster/docs/research/` (when using `--save-file`)

---

## Manual Procedures (Fields Not Supported by Task Master)

### Why Manual Procedures Are Needed

Task Master's `TaskEntity.toJSON()` strips custom fields during serialization. The following fields are **lost** when running `expand`, `update-task`, `update`, or `parse-prd`:

- `effort`
- `complexity`
- `owner`
- `successCriteria`
- `testStrategy`
- Custom metadata

### Procedure: Add Success Criteria

**Step 1:** Edit the task markdown file directly:

```markdown
## Success Criteria

- [ ] Complete list of active feature branches created
- [ ] All branches documented with branch names and creation dates
- [ ] Excluded merged branches identified
- [ ] List ready for assessment phase
```

**Step 2:** Embed in `details` field for preservation:

```markdown
## Details

Implementation steps here...

<!-- EXTENDED_METADATA
successCriteria:
  - Complete list of active feature branches created
  - All branches documented with branch names and creation dates
  - Excluded merged branches identified
  - List ready for assessment phase
END_EXTENDED_METADATA -->
```

**Step 3:** Run embed command to sync to tasks.json:

```bash
python scripts/task_metadata_manager.py embed --task 001
```

### Procedure: Add Test Strategy

**Step 1:** Add to task markdown:

```markdown
## Test Strategy

### Unit Tests
- Test branch listing against known repository state
- Test merge detection logic with mock branches
- Test metadata extraction accuracy

### Integration Tests
- Verify output matches `git branch -r` output
- Confirm merged branches correctly excluded
- Validate against GitHub/GitLab API

### Validation
- Cross-check with manual branch inspection
- Verify completeness with repository owner
```

**Step 2:** Embed in details field:

```markdown
<!-- EXTENDED_METADATA
testStrategy: |
  Unit: branch listing, merge detection, metadata extraction
  Integration: git branch -r comparison, GitHub API validation
  Validation: manual inspection, owner verification
END_EXTENDED_METADATA -->
```

### Procedure: Add Effort/Complexity/Owner

**Step 1:** Add to task header:

```markdown
**Effort:** 2-3 hours
**Complexity:** 4/10
**Owner:** @developer-name
```

**Step 2:** Embed for preservation:

```markdown
<!-- EXTENDED_METADATA
effort: 2-3h
complexity: 4/10
owner: developer-name
END_EXTENDED_METADATA -->
```

**Step 3:** Sync to tasks.json:

```bash
python scripts/task_metadata_manager.py embed --task 001
```

---

## Complete Enhancement Workflow

### Before Any Task Master Operation

```bash
# ALWAYS backup first - Task Master strips custom fields!
python scripts/task_metadata_manager.py backup --all

# Or backup specific task
python scripts/task_metadata_manager.py backup --task 001
```

### Enhancing a New Task

```bash
# 1. Backup existing state
python scripts/task_metadata_manager.py backup --task 001

# 2. Use Task Master for supported fields
task-master update-task 1 add detailed implementation steps for branch discovery

# 3. Regenerate markdown files
task-master generate

# 4. Manually edit markdown for unsupported fields
# Edit: .taskmaster/tasks/task-001.md
# Add: Success Criteria, Test Strategy, Effort, Complexity, Owner

# 5. Add EXTENDED_METADATA block to details section
# (See format below)

# 6. Embed metadata back to tasks.json
python scripts/task_metadata_manager.py embed --task 001

# 7. Verify
python scripts/task_metadata_manager.py report
```

### Extended Metadata Block Format

Add this to the **end** of your `Details` section in the markdown file:

```markdown
<!-- EXTENDED_METADATA
effort: 2-3h
complexity: 4/10
owner: developer-name
initiative: 1
blocks: Tasks 016-017
scope: Strategic framework, decision criteria
focus: Framework definition
successCriteria:
  - Criterion 1 with specific measurable outcome
  - Criterion 2 with validation method
  - Criterion 3 with acceptance threshold
testStrategy: |
  Unit: Component-level tests for each function
  Integration: End-to-end workflow validation
  Validation: Manual review and stakeholder sign-off
END_EXTENDED_METADATA -->
```

### After Task Master Operations

```bash
# If Task Master stripped your metadata:

# 1. List available backups
python scripts/task_metadata_manager.py list-backups --task 001

# 2. Restore from most recent backup (index 0)
python scripts/task_metadata_manager.py restore --task 001 --index 0

# 3. Re-embed metadata
python scripts/task_metadata_manager.py embed --task 001
```

---

## Field-by-Field Enhancement Guide

### Success Criteria Best Practices

```markdown
## Success Criteria

### Must Have (P0)
- [ ] [Measurable outcome with specific threshold]
- [ ] [Verifiable artifact produced]
- [ ] [Automated validation passes]

### Should Have (P1)
- [ ] [Quality metric achieved]
- [ ] [Performance target met]

### Nice to Have (P2)
- [ ] [Additional enhancement]
```

**Example:**
```markdown
## Success Criteria

### Must Have (P0)
- [ ] All 15+ active feature branches identified and cataloged
- [ ] Branch metadata includes: name, creation date, last activity, author(s)
- [ ] Merged branches excluded with 100% accuracy
- [ ] Output format: JSON file at `.taskmaster/data/active_branches.json`

### Should Have (P1)
- [ ] Stale branch detection (>90 days inactive)
- [ ] Branch categorization by prefix (feature/*, docs/*, fix/*)

### Nice to Have (P2)
- [ ] GitHub API integration for additional metadata
```

### Test Strategy Best Practices

```markdown
## Test Strategy

### Unit Tests
| Test | Input | Expected Output | Coverage |
|------|-------|-----------------|----------|
| test_list_branches | mock git repo | list of branch names | branch listing |
| test_filter_merged | mixed branches | only unmerged | merge detection |
| test_extract_metadata | branch ref | metadata dict | metadata extraction |

### Integration Tests
- [ ] Full workflow against test repository
- [ ] Comparison with `git branch -r` output
- [ ] Validation against GitHub API

### Manual Validation
- [ ] Review output with repository owner
- [ ] Spot-check 5 random branches manually
- [ ] Verify excluded branches were correctly excluded

### Test Commands
```bash
pytest tests/test_branch_discovery.py -v
pytest tests/integration/test_full_workflow.py -v
```
```

### Implementation Notes Best Practices

```markdown
## Implementation Notes

### Architecture Decisions
- **Decision:** Use subprocess for git commands vs GitPython
- **Rationale:** Subprocess is lighter, no additional dependency
- **Trade-off:** Less error handling, but simpler code

### Known Limitations
- Shallow clones may have incomplete history
- Very large repositories (>10k branches) may be slow

### Performance Considerations
- Cache branch list for repeated queries
- Batch git commands where possible

### Security Considerations
- Validate branch names before shell execution
- Sanitize output before JSON serialization
```

---

## Automation Scripts

### Batch Enhancement

```bash
#!/bin/bash
# enhance_all_tasks.sh

# Backup all tasks first
python scripts/task_metadata_manager.py backup --all

# Generate coverage report
python scripts/task_metadata_manager.py report

# For each task file, check if EXTENDED_METADATA exists
for file in .taskmaster/tasks/task-*.md; do
    if ! grep -q "EXTENDED_METADATA" "$file"; then
        echo "Missing metadata: $file"
    fi
done
```

### Validation Script

```bash
#!/bin/bash
# validate_task_quality.sh

echo "=== Task Quality Validation ==="

for file in .taskmaster/tasks/task-*.md; do
    echo "Checking: $file"
    
    # Check for Success Criteria
    if ! grep -q "## Success Criteria" "$file"; then
        echo "  ❌ Missing: Success Criteria"
    fi
    
    # Check for Test Strategy
    if ! grep -q "## Test Strategy" "$file"; then
        echo "  ❌ Missing: Test Strategy"
    fi
    
    # Check for EXTENDED_METADATA
    if ! grep -q "EXTENDED_METADATA" "$file"; then
        echo "  ❌ Missing: EXTENDED_METADATA block"
    fi
    
    # Check for effort estimate
    if ! grep -q "Effort:" "$file"; then
        echo "  ❌ Missing: Effort estimate"
    fi
done
```

---

## Summary Cheat Sheet

| Task | Command/Procedure |
|------|-------------------|
| Update title/description | `task-master update-task <id> <prompt>` |
| Add implementation notes | `task-master update-subtask --id=<id> --prompt="..."` |
| Change status | `task-master set-status --id=<id> --status=<status>` |
| Add dependency | `task-master add-dependency --id=<id> --depends-on=<id>` |
| Add Success Criteria | Edit markdown + embed metadata |
| Add Test Strategy | Edit markdown + embed metadata |
| Add Effort/Complexity | Edit markdown + embed metadata |
| Backup before changes | `python scripts/task_metadata_manager.py backup --all` |
| Restore after data loss | `python scripts/task_metadata_manager.py restore --task <id> --index 0` |
| Sync metadata to JSON | `python scripts/task_metadata_manager.py embed --task <id>` |
| Check metadata coverage | `python scripts/task_metadata_manager.py report` |

---

## References

- [TASK_METADATA_PRESERVATION_GUIDE.md](TASK_METADATA_PRESERVATION_GUIDE.md) - Detailed preservation guide
- [TASK_WORKFLOW_INTEGRATION.md](TASK_WORKFLOW_INTEGRATION.md) - Workflow integration details
- [scripts/README.md](../scripts/README.md) - Script documentation
- [GitHub Issue #1555](https://github.com/eyaltoledano/claude-task-master/issues/1555) - TaskEntity.toJSON() bug
