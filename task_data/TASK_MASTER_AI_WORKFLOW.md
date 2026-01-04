# Task Master AI Integration Workflow for Task 75

## Overview

This document explains how to use Task Master AI commands throughout the Task 75 lifecycle: complexity analysis, task expansion, research-backed enrichment, and validation.

---

## Phase 1: Complexity Analysis & Research

### Purpose
Use research-backed AI to understand task complexity before expanding into subtasks.

### Commands

```bash
# Analyze complexity for a specific task
task-master analyze-complexity --research --to=75.1

# Analyze multiple tasks
task-master analyze-complexity --research --to=75.1,75.2,75.3

# Analyze all remaining tasks
task-master analyze-complexity --research --from=75.1 --to=75.9

# Generate complexity report
task-master complexity-report
```

### What This Produces

- **Complexity assessment:** 1-10 scale with reasoning
- **Effort estimation:** Hours breakdown by subtask
- **Risk analysis:** Blockers, dependencies, integration points
- **Research insights:** Best practices, pitfalls, algorithm selection
- **Report file:** `.taskmaster/reports/task-complexity-report.json`

### When to Use

- **Before expanding tasks:** Understand the scope
- **During planning:** Size team allocation
- **Risk mitigation:** Identify potential issues early
- **Decision-making:** Choose implementation approach

### Example Output

```json
{
  "task_id": "75.1",
  "complexity": 7,
  "reasoning": "Git command integration requires proper error handling",
  "estimated_hours": 24-32,
  "subtasks": [
    {
      "id": "75.1.1",
      "title": "Design Metric System",
      "complexity": 6,
      "effort_hours": 2-3,
      "risks": ["metric normalization", "weight validation"],
      "research_insights": "Use exponential decay for time-sensitive metrics"
    }
  ],
  "dependencies": ["git command execution", "error handling patterns"],
  "integration_points": ["75.4 BranchClusterer"]
}
```

---

## Phase 2: Task Expansion with Research

### Purpose
Expand main tasks into atomic subtasks with AI-guided research context.

### Commands

```bash
# Expand single task with research
task-master expand --id=75.1 --research --force --num=8

# Expand with custom count
task-master expand --id=75.1 --research --force --num=10

# Expand all unscheduled tasks
task-master expand --all --research --force

# Expand specific range
task-master expand --id=75.1-75.3 --research --force
```

### What This Produces

- **8 subtasks** with auto-numbering (75.1.1 - 75.1.8)
- **Auto-generated titles** based on analysis
- **Effort estimates** for each subtask
- **Dependency relationships** between subtasks
- **Research context** in task descriptions

### When to Use

- After complexity analysis
- When assigning to team members
- At phase transition boundaries
- When refining estimates

### Expansion Examples

**75.1 CommitHistoryAnalyzer expands to:**
```
75.1.1 Design Metric System (2-3h)
75.1.2 Set Up Git Data Extraction (4-5h)
75.1.3 Implement Commit Recency (3-4h)
75.1.4 Implement Commit Frequency (3-4h)
75.1.5 Implement Authorship & Stability (4-5h)
75.1.6 Implement Merge Readiness (3-4h)
75.1.7 Aggregate Metrics & Format Output (2-3h)
75.1.8 Write Unit Tests (3-4h)
```

**75.4 BranchClusterer expands to:**
```
75.4.1 Design Clustering Architecture (3-4h)
75.4.2 Implement Metric Combination System (4-5h)
75.4.3 Implement Distance Matrix Calculation (3-4h)
75.4.4 Implement Hierarchical Clustering Engine (4-5h)
75.4.5 Compute Cluster Quality Metrics (3-4h)
75.4.6 Compute Cluster Characteristics (2-3h)
75.4.7 Format Output & Output Validation (2-3h)
75.4.8 Write Unit Tests (4-5h)
```

---

## Phase 3: Research-Backed Enrichment

### Purpose
Add research context, implementation guidance, and success criteria to subtasks.

### Commands

```bash
# Update single subtask with context
task-master update-subtask --id=75.1.1 --prompt="[Enrichment content]"

# Update multiple subtasks
for i in {1..8}; do
  task-master update-subtask --id=75.1.$i --prompt="[Context for subtask $i]"
done

# Use research flag for AI-backed suggestions
task-master update-subtask --id=75.1.1 --prompt="[Base context]" --research
```

### Enrichment Content Structure

For each subtask, add:

```markdown
## [Subtask Title]

**Purpose:** What this subtask accomplishes

**From Outline:**
- Step 1: [from task outline]
- Step 2: [from task outline]

**Research Insights:**
- Best practice: [AI-researched insight]
- Pitfall to avoid: [common mistake]
- Algorithm recommendation: [specific approach]

**Success Criteria:**
✓ [Criterion 1]
✓ [Criterion 2]
✓ [Criterion 3]

**Implementation Reference:**
- See HANDOFF_75.X_*.md for detailed algorithms
- Test cases: [specific test scenario]
- Edge cases to handle: [list]

**Effort Estimate:** [Hours from outline]
**Complexity:** [1-10 scale]
**Blocks:** [Which subtasks depend on this]
```

### Example Enrichment

```bash
task-master update-subtask --id=75.1.2 --prompt="
## Git Data Extraction Setup

**Purpose:** Create git command execution utilities with error handling

**From Outline:**
- Utility functions for git command execution
- Branch validation (check if branch exists)
- Commit log extraction (get all commits on branch)
- Commit metadata extraction (dates, authors, messages)
- Error handling (invalid branch, repo not found, git errors)

**Research Insights:**
- Use subprocess.run with capture_output for reliable git access
- Implement retry logic for transient git errors (optional but recommended)
- Cache git command results to avoid repeated calls (improves performance 3-5x)
- Use git --format flags for parsing reliability

**Success Criteria:**
✓ Can execute git commands without errors
✓ Validates branch existence before processing
✓ Extracts commit list with metadata
✓ Handles non-existent branches gracefully
✓ Returns structured data (list of dicts)

**Implementation Reference:**
- See HANDOFF_75.1_CommitHistoryAnalyzer.md 'Git Commands Reference'
- Test with: new branch, stale branch, non-existent branch
- Edge cases: binary changes, merge commits, very large commits

**Effort Estimate:** 4-5 hours
**Complexity:** 6/10
"
```

---

## Phase 4: Validation & Progress Tracking

### Purpose
Validate task structure, progress, and completion before moving to next phase.

### Validation Commands

#### Pre-Implementation Validation

```bash
# Validate all dependency relationships
task-master validate-dependencies

# Check specific task and all subtasks
task-master show 75.1

# Verify next task in queue
task-master next

# Generate summary report
task-master list --status=pending
```

#### During Implementation

```bash
# Mark subtask as in-progress
task-master set-status --id=75.1.1 --status=in-progress

# When complete
task-master set-status --id=75.1.1 --status=done

# Check what's next (should unblock dependent tasks)
task-master next

# Show current progress
task-master list --status=in-progress
task-master list --status=done
```

#### Post-Task Validation

```bash
# Verify all subtasks of main task complete
task-master show 75.1

# Validate dependencies resolved
task-master validate-dependencies

# Check next task is ready
task-master next  # Should show 75.2.1 if 75.1 complete

# Generate completion report
task-master complexity-report | grep "75.1"
```

#### Final System Validation

```bash
# All 9 main tasks complete
task-master list --status=done | wc -l  # Should show 9+

# No blocking dependencies
task-master validate-dependencies  # Should show no errors

# Generate final report
task-master complexity-report > final_report.json

# Create summary
echo "=== Task 75 Completion Summary ===" 
task-master list --status=done | grep "75\." | wc -l
echo "tasks completed"
```

---

## Workflow Timeline

### Week 1: Planning & Analysis
```bash
# Day 1: Initialize
task-master init

# Day 2-3: Create main tasks
task-master add-task --prompt="Task 75: Branch Clustering System..."
task-master add-task --prompt="Task 75.1: CommitHistoryAnalyzer..."
task-master add-task --prompt="Task 75.2: CodebaseStructureAnalyzer..."
# ... continue for 75.3-75.9

# Day 3-4: Complexity analysis
task-master analyze-complexity --research --from=75.1 --to=75.9
task-master complexity-report

# Day 5: Review and planning
Review report.json, identify risks, plan resource allocation
```

### Week 2: Expansion & Enrichment
```bash
# Daily: Expand one main task (75.X) with research
task-master expand --id=75.1 --research --force --num=8
# ... repeat for 75.2-75.9

# During expansion: Add enrichment context
for i in {1..8}; do
  task-master update-subtask --id=75.1.$i --prompt="[Context]"
done

# End of week: Validate all
task-master validate-dependencies
task-master list --status=pending | wc -l  # Should show ~60
```

### Weeks 3-8: Implementation & Validation
```bash
# Daily standup
task-master next  # Show next available task
task-master list --status=in-progress  # Show active work

# After each subtask complete
task-master set-status --id=75.X.Y --status=done

# End of each main task
task-master show 75.X | grep "status.*done"  # Verify all subtasks done
task-master validate-dependencies  # Check no blockers

# Weekly progress report
task-master complexity-report | grep "75\."
```

### Week 9: Final Validation
```bash
# Verify completion
task-master list --status=done

# Validate no open dependencies
task-master validate-dependencies

# Generate final metrics
task-master complexity-report > task_75_final_report.json

# Archive results
mkdir -p task_75_artifacts
cp task_75_final_report.json task_75_artifacts/
task-master show 75 > task_75_artifacts/task_summary.txt
```

---

## Common Workflows

### Adding Context During Implementation

```bash
# When agent encounters design decision
task-master update-subtask --id=75.1.3 --prompt="
**Implementation Note (Added during development):**

Decided to use exponential decay for recency scoring:
  recency_score = exp(-days_since_commit / 30_day_window)
  
Reason: Emphasizes recent activity while remaining smooth for old branches
Alternative considered: Linear decay (rejected as too harsh for old branches)
Test result: Verified against known branches (recent: >0.8, stale: <0.3)
"
```

### Handling Blockers

```bash
# If subtask is blocked
task-master set-status --id=75.1.5 --status=blocked

# Document the blocker
task-master update-subtask --id=75.1.5 --prompt="
**Blocker:** Waiting for 75.1.2 (Git Setup) to complete
Expected resolution: Day 3
Workaround: Using mock git commands for development
"

# When blocker resolved
task-master set-status --id=75.1.5 --status=pending
task-master next  # Check if now available
```

### Rescheduling Estimates

```bash
# If effort estimate changes
task-master update-subtask --id=75.1.3 --prompt="
**Revised Estimate:**
Original: 3-4 hours
Updated: 4-5 hours
Reason: Additional edge case handling for very old branches required more testing
Status: Still on track overall
"
```

---

## Reports & Artifacts

### Complexity Report
```bash
task-master complexity-report
```

Generates: `.taskmaster/reports/task-complexity-report.json`

Contains:
- Overall project complexity
- Per-task complexity scores
- Effort distributions
- Dependency analysis
- Risk assessment

### Task Summary
```bash
task-master show 75  # Root task
task-master show 75.1  # Main task
task-master show 75.1.1  # Subtask
```

Shows:
- Current status
- Blockers/dependencies
- Effort estimates
- Completion percentage
- Associated documentation

### Progress Tracking
```bash
task-master list --status=done
task-master list --status=in-progress
task-master list --status=pending
```

Shows:
- Completed tasks
- Current work
- Remaining work
- Completion rate

---

## Validation Checklist

### Pre-Implementation
- [ ] `task-master validate-dependencies` passes
- [ ] `task-master complexity-report` generated
- [ ] All subtasks have effort estimates
- [ ] All subtasks have success criteria
- [ ] `task-master next` shows first task correctly

### Mid-Implementation (Weekly)
- [ ] `task-master list --status=in-progress` shows current work
- [ ] `task-master next` shows unblocked tasks
- [ ] No "blocked" subtasks without documented reason
- [ ] Progress aligns with original complexity report

### Post-Task (After 75.X complete)
- [ ] `task-master show 75.X` shows all subtasks 'done'
- [ ] `task-master validate-dependencies` shows next task unblocked
- [ ] Output files match specification (manual check)
- [ ] Test coverage >90% confirmed

### Final (After Task 75 complete)
- [ ] All 9 main tasks marked 'done'
- [ ] `task-master validate-dependencies` shows no issues
- [ ] Final report generated
- [ ] Downstream task compatibility verified

---

## Troubleshooting

### Task won't unblock
```bash
# Check dependencies
task-master show 75.1.3 | grep depends-on

# Verify blockers are actually done
task-master show 75.1.2 | grep status

# Check for circular dependencies
task-master validate-dependencies
```

### Estimate seems off
```bash
# Review complexity assessment
task-master complexity-report | grep "75.1.X"

# Check actual time logs
task-master show 75.1.X | grep hours_actual

# Update estimate
task-master update-subtask --id=75.1.X --prompt="Revised effort: ..."
```

### Can't find next task
```bash
# Check task queue
task-master next

# If blocked, see what's blocking
task-master show 75.1.3  # Check dependencies

# Override if needed (carefully)
task-master set-status --id=75.1.2 --status=done  # Only if truly done!
task-master next  # Should show 75.1.3 now
```

---

## Best Practices

1. **Run validation before each phase**
   ```bash
   task-master validate-dependencies
   ```

2. **Update context as you learn**
   ```bash
   task-master update-subtask --id=75.X.Y --prompt="[New insight]"
   ```

3. **Track blockers explicitly**
   ```bash
   task-master set-status --id=75.X.Y --status=blocked
   task-master update-subtask --id=75.X.Y --prompt="Blocker: ..."
   ```

4. **Generate reports regularly**
   ```bash
   task-master complexity-report  # Weekly
   task-master show 75  # Daily standup
   ```

5. **Keep implementation reference docs nearby**
   - When coding: Reference HANDOFF_75.X_*.md
   - When managing: Reference 75.X_*_TASK_CREATION_OUTLINE.md
   - When planning: Reference HANDOFF_INDEX.md

---

## Integration with Git

```bash
# Commit after significant milestones
git add .taskmaster/
git commit -m "feat(task-75): complete complexity analysis for all tasks"

git add .taskmaster/
git commit -m "feat(task-75): expand all main tasks into subtasks with research"

git add .taskmaster/
git commit -m "feat(task-75.1): complete CommitHistoryAnalyzer (all subtasks done)"
```

---

## Success Criteria

Task 75 workflow is successful when:
- [ ] All complexity analyses complete with research
- [ ] All tasks expanded with research-backed insights  
- [ ] All subtasks enriched with implementation context
- [ ] All validation checkpoints pass
- [ ] Final report shows 100% completion
- [ ] Zero dependency issues at handoff to each stage

