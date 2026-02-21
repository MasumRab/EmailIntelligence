# Task 75 Task Breakdown Guide

## Purpose
This document explains how to use the Task Breakdown documents (HANDOFF_75.X_*_TASKS.md) to create tasks and subtasks in your task management system.

**What changed:** These documents focus on DEFINING WORK, not implementing it.

---

## Format Explanation

Each HANDOFF_75.X_*_TASKS.md document contains:

### 1. Purpose Section
**What it means:** High-level summary of what this component does and why it matters

**For task management:** Use as task title context
```
Main Task: "Build CommitHistoryAnalyzer class"
Purpose: "Create a reusable Python class that extracts and scores commit history metrics"
```

### 2. Success Criteria
**What it means:** The checklist of deliverables for this main task

**For task management:** These are the acceptance criteria for the main task (75.1)
```
Task 75.1 acceptance checklist:
- Class accepts repo_path and branch_name
- Extracts commit data using git
- Returns dict with 5 metrics + aggregate score
- Handles edge cases
- Passes unit tests
```

### 3. Subtasks (75.1.1, 75.1.2, etc.)
**What it means:** Atomic pieces of work that can be assigned independently

**For task management:** Create one subtask per section

**Subtask structure:**
```
Subtask ID: 75.1.1
Title: "Design Metric System"
Purpose: "Define how metrics will be calculated and combined"
Deliverable: "Decision document with metric definitions"

Steps (checklist within subtask):
- Review metric specifications
- Define calculation approach
- Document normalization strategy
- Create weighting scheme
- Document edge case handling

Success Criteria (task acceptance):
- All 5 metrics clearly defined
- Calculation formula for each documented
- Normalization approach specified
- Weights documented (sum = 1.0)
- Edge case list created

Effort: 2-3 hours
Complexity: Not specified (inherit from parent task)
Dependencies: None (can start immediately)
Blocks: 75.1.2, 75.1.3, 75.1.4, 75.1.5
```

### 4. Integration Checkpoint
**What it means:** When this task is ready to hand off to the next task

**For task management:** Transition criteria from one task to the next
```
Before starting Task 75.4:
- Task 75.1 must be 100% complete
- All unit tests passing
- Output matches specification
- Ready for integration
```

### 5. Configuration Parameters
**What it means:** Tunable values that shouldn't be hardcoded

**For task management:** Note these for the implementer
```
Document these in code as configurable:
- RECENCY_WINDOW_DAYS = 30
- COMMIT_RECENCY_WEIGHT = 0.25
- (etc.)

Implementation note: These should be in a config file, not hardcoded constants
```

### 6. Dependencies
**What it means:** What blocks this task and what it blocks

**For task management:** Set up dependency relationships
```
Blocked by: None (can start immediately)
Blocks: Task 75.4 (needs output from this task)
```

---

## How to Create Tasks from These Documents

### Step 1: Initialize and Parse Initial Task Structure

```bash
# If not already initialized
task-master init

# Start with the main Task 75
task-master add-task --prompt="Task 75: Branch Clustering System - Complete implementation of commit history, codebase structure, diff distance analyzers, clustering engine, target assignment, pipeline integration, visualization, testing, and framework integration for branch clustering"
```

### Step 2: Create Main Task (e.g., Task 75.1)

Use TaskMaster or your system:
```bash
task-master add-task --prompt="Build CommitHistoryAnalyzer class - implement git analysis module that extracts and scores commit history metrics. Reference: 75.1_CommitHistoryAnalyzer_TASK_CREATION_OUTLINE.md"
```

Properties:
- **ID:** 75.1
- **Title:** "CommitHistoryAnalyzer Implementation"
- **Description:** [Use Purpose section from 75.1_CommitHistoryAnalyzer_TASK_CREATION_OUTLINE.md]
- **Estimated Effort:** 24-32 hours
- **Complexity:** 7/10
- **Status:** pending
- **Details:** [Use Success Criteria section]

### Step 3: Expand with Complexity Analysis & Research

```bash
# Analyze task complexity with research-backed insights
task-master analyze-complexity --research --to=75.1

# Expand main task into subtasks with research guidance
task-master expand --id=75.1 --research --force --num=8

# This will automatically create subtasks 75.1.1 through 75.1.8 with enhanced context
```

### Step 4: Update Subtasks with Implementation Details

For each subtask (75.1.1, 75.1.2, etc.), add research-backed context:

```bash
# Add implementation details from outline document
task-master update-subtask --id=75.1.1 --prompt="Design Metric System:

**Context from outline:**
- commit_recency: exponential decay over 30-day window
- commit_frequency: commits per day normalized
- authorship_diversity: unique authors ratio
- merge_readiness: commits since merge base
- stability_score: inverse of churn rate

**Research insights:**
- Metrics should normalize to [0,1] independently
- Weight aggregation: 0.25 + 0.20 + 0.20 + 0.20 + 0.15 = 1.0
- Edge cases: zero commits, very old branches, single commits

**Success Criteria:**
✓ All 5 metrics clearly defined
✓ Calculation formula for each documented
✓ Normalization approach specified
✓ Weights documented (sum = 1.0)
✓ Edge case list created"
```

### Step 5: Create Subtasks for Each Section

For each subtask (75.1.1, 75.1.2, etc.) from outline:

```bash
task-master add-task --prompt="75.1.1: Design Metric System - From 75.1_CommitHistoryAnalyzer_TASK_CREATION_OUTLINE.md"
task-master add-task --prompt="75.1.2: Set Up Git Data Extraction - From 75.1_CommitHistoryAnalyzer_TASK_CREATION_OUTLINE.md"
# ... continue for all 8 subtasks
```

Properties per subtask:
- **ID:** 75.1.1 (creates automatic hierarchy)
- **Title:** [From subtask heading in outline]
- **Description:** [From Purpose + Steps]
- **Estimated Effort:** [From Effort field]
- **Complexity:** Inherited from parent or specify per subtask
- **Status:** pending
- **Details:** 
  - Steps (checklist)
  - Success Criteria (acceptance tests)
  - Dependencies
  - Link to outline document

### Step 6: Set Up Dependencies with Validation

```bash
# Set up blocking relationships
task-master add-dependency --id=75.1.2 --depends-on=75.1.1
task-master add-dependency --id=75.1.3 --depends-on=75.1.1,75.1.2
task-master add-dependency --id=75.1.4 --depends-on=75.1.1,75.1.2
task-master add-dependency --id=75.1.5 --depends-on=75.1.1,75.1.2
task-master add-dependency --id=75.1.6 --depends-on=75.1.1,75.1.2
task-master add-dependency --id=75.1.7 --depends-on=75.1.3,75.1.4,75.1.5,75.1.6
task-master add-dependency --id=75.1.8 --depends-on=75.1.7

# Block Task 75.4 on completion of 75.1
task-master add-dependency --id=75.4 --depends-on=75.1

# Validate dependency structure
task-master validate-dependencies
```

Dependencies for Task 75.1:
```
75.1.1 (Design) blocks: 75.1.2, 75.1.3, 75.1.4, 75.1.5, 75.1.6
75.1.2 (Git Setup) blocks: 75.1.3, 75.1.4, 75.1.5, 75.1.6
75.1.3-75.1.6 (Metrics) can run in parallel, block: 75.1.7
75.1.7 (Aggregate) blocks: 75.1.8
75.1.8 (Tests) final step, blocks: 75.4
75.1 (main) blocks: 75.4 (BranchClusterer)
```

### Step 7: Document Implementation Notes & Research

For each subtask, add context and research:

```bash
# Add implementation notes with git commands
task-master update-subtask --id=75.1.2 --prompt="Implementation notes:
- Use subprocess for git commands
- Catch InvalidRepo and BranchNotFound errors
- Return structured data (list of dicts with date, author, message)

**Git Commands:**
  git log main..BRANCH_NAME --pretty=format:'%H|%ai|%an|%s'
  git merge-base main BRANCH_NAME
  git log -1 --format=%ai BRANCH_NAME

**Error Handling:**
  - BranchNotFoundError: branch does not exist
  - InvalidRepositoryError: .git folder missing
  - GitCommandError: git command execution failed

**References:**
  - See HANDOFF_75.1_CommitHistoryAnalyzer.md for detailed spec
  - Test cases in HANDOFF_75.1_CommitHistoryAnalyzer.md"
```

### Step 8: Validation Checkpoint

```bash
# Validate all tasks and dependencies are properly configured
task-master validate-dependencies

# Show next task in queue (should be 75.1.1)
task-master next

# Display full task hierarchy
task-master list --status=pending
```

---

## Example: Creating Task 75.1 Subtasks

See **75.1_CommitHistoryAnalyzer_TASK_CREATION_OUTLINE.md** for complete breakdown.

### Subtask 75.1.1
```
Title: Design Metric System
Description: Define how 5 metrics (recency, frequency, diversity, readiness, stability) will be calculated and combined

Deliverables:
- Metric definitions document
- Calculation formulas
- Normalization approach
- Weighting scheme

Success Criteria:
✓ All 5 metrics clearly defined
✓ Calculation formula for each documented
✓ Normalization approach specified
✓ Weights documented (sum = 1.0)
✓ Edge case list created

Effort: 2-3 hours
Status: pending
```

### Subtask 75.1.2
```
Title: Set Up Git Data Extraction
Description: Create functions to extract commit data from git repository

Deliverables:
- Git command execution module
- Branch validation functions
- Commit extraction functions
- Error handling

Success Criteria:
✓ Can execute git commands without errors
✓ Validates branch existence before processing
✓ Extracts commit list with metadata
✓ Handles non-existent branches gracefully
✓ Returns structured data (list of dicts)

Effort: 4-5 hours
Depends on: 75.1.1
Status: pending
Blocks: 75.1.3, 75.1.4, 75.1.5, 75.1.6
```

[Continue for 75.1.3 through 75.1.8 - see task outline document...]

---

## Mapping to TaskMaster

If using TaskMaster CLI:

```bash
# Create main task 75.1
task-master add-task --prompt="CommitHistoryAnalyzer: Extract and score commit history metrics for branches"

# Create subtasks (TaskMaster will auto-number as 75.1.1, 75.1.2, etc.)
task-master add-task --prompt="75.1.1: Design metric system - define 5 metrics, calculation formulas, weights"
task-master add-task --prompt="75.1.2: Set up git data extraction - implement branch validation and commit extraction"
task-master add-task --prompt="75.1.3: Implement commit recency metric - score how recent commits are"
task-master add-task --prompt="75.1.4: Implement commit frequency metric - score velocity of development"
task-master add-task --prompt="75.1.5: Implement authorship and stability metrics"
task-master add-task --prompt="75.1.6: Implement merge readiness metric - score sync with main"
task-master add-task --prompt="75.1.7: Aggregate metrics and format output - combine 5 metrics into score"
task-master add-task --prompt="75.1.8: Write unit tests - create 5+ test cases"

# Set dependencies
task-master add-dependency --id=75.1.2 --depends-on=75.1.1
task-master add-dependency --id=75.1.3 --depends-on=75.1.2
task-master add-dependency --id=75.1.4 --depends-on=75.1.2
task-master add-dependency --id=75.1.5 --depends-on=75.1.2
task-master add-dependency --id=75.1.6 --depends-on=75.1.2
task-master add-dependency --id=75.1.7 --depends-on=75.1.3,75.1.4,75.1.5,75.1.6
task-master add-dependency --id=75.1.8 --depends-on=75.1.7
```

---

## Key Differences from Original Handoffs

### Original Handoffs (HANDOFF_75.X_*.md)
- Implementation-focused
- Code examples and algorithms
- Test case specifics
- 4-9 KB per file

### New Task Breakdown Docs (HANDOFF_75.X_*_TASKS.md)
- Task definition focused
- Subtask breakdown
- Acceptance criteria
- Dependencies and blocking relationships
- Effort estimates
- Suitable for task management systems

**Use the HANDOFF_75.X_*_TASKS.md documents to:**
1. Create tasks in task management system
2. Set dependencies
3. Assign to team members
4. Track progress

**Use the original HANDOFF_75.X_*.md documents as reference for:**
- Implementation details (when implementing the task)
- Code examples and algorithms
- Test cases
- Edge case handling

---

## All Tasks Summary

| Task | Purpose | Subtasks | Effort | Blocking |
|------|---------|----------|--------|----------|
| **75.1** | CommitHistoryAnalyzer | 8 | 24-32h | 75.4 |
| **75.2** | CodebaseStructureAnalyzer | 7 | 28-36h | 75.4 |
| **75.3** | DiffDistanceCalculator | 8 | 32-40h | 75.4 |
| **75.4** | BranchClusterer | 8 | 28-36h | 75.5 |
| **75.5** | IntegrationTargetAssigner | 9 | 24-32h | 75.6 |
| **75.6** | PipelineIntegration | 7 | 20-28h | 75.7, 75.8 |
| **75.7** | VisualizationReporting | 6 | 20-28h | 75.9 |
| **75.8** | TestingSuite | 5 | 24-32h | 75.9 |
| **75.9** | FrameworkIntegration | 6 | 16-24h | Done |

**Total:** ~60 subtasks across 9 main tasks

---

## Files You Need

1. **TASK_BREAKDOWN_GUIDE.md** (this file) - explains how to use the documents
2. **HANDOFF_INDEX.md** - navigation and overview
3. **75.1_CommitHistoryAnalyzer_TASK_CREATION_OUTLINE.md** - Task 75.1 breakdown (example)
4. **[75.2 through 75.9 _TASK_CREATION_OUTLINE.md]** - Similar breakdowns for each task

When you're ready to implement a subtask:
- Read the corresponding HANDOFF_75.X_*.md (implementation guide)
- Mark subtask "in-progress"
- Complete the deliverables
- Mark subtask "done"

---

## Task Master AI Integration Workflow

### For Each Main Task (75.1-75.9)

**Task Definition Phase**
```bash
# Create main task
task-master add-task --prompt="Task 75.X: [Title] - [Description from outline]"

# Analyze complexity with research
task-master analyze-complexity --research --to=75.X

# Expand into subtasks with research guidance
task-master expand --id=75.X --research --force --num=8
```

**Enrichment Phase**
```bash
# For each subtask, add research-backed context
task-master update-subtask --id=75.X.1 --prompt="[Context from outline + research insights]"
task-master update-subtask --id=75.X.2 --prompt="[Context from outline + research insights]"
# ... repeat for all subtasks

# Set up all dependencies
task-master add-dependency --id=75.X.2 --depends-on=75.X.1
# ... (repeat for all dependencies per outline)

# Validate dependency structure
task-master validate-dependencies
```

**Assignment Phase**
```bash
# Generate complexity report
task-master complexity-report

# Verify next task readiness
task-master next  # Should show 75.1.1
```

---

## Validation Checkpoints

### Pre-Implementation Validation
```bash
# Verify dependency structure is valid
task-master validate-dependencies

# Ensure all subtasks have estimates and success criteria
task-master show 75.X

# Check complexity analysis is complete
task-master complexity-report

# Confirm task queue is correct
task-master next
```

### During Implementation Validation
```bash
# When subtask is complete
task-master set-status --id=75.X.Y --status=done

# Verify next task is unblocked
task-master next

# Track progress
task-master list --status=in-progress
task-master list --status=done | grep "75\."
```

### Post-Task Validation
```bash
# When entire main task complete (all subtasks done)
task-master show 75.X

# Verify output files created and match spec
# Use checklist from 75.X_*_TASK_CREATION_OUTLINE.md

# Check integration requirements from outline
```

### Final System Validation
```bash
# All 9 main tasks complete
task-master list --status=done

# No blocking dependencies remaining
task-master validate-dependencies

# All integration checkpoints passed
# (Manual review: outputs match specification)

# Downstream compatibility verified
# (See HANDOFF_75.9_FrameworkIntegration.md)

# Create final report
task-master complexity-report > task_75_final_report.txt
```

---

## Next Steps

1. ✓ Read this TASK_BREAKDOWN_GUIDE.md
2. ✓ Read HANDOFF_INDEX.md for overview
3. **Initialize:** `task-master init` (if needed)
4. **Create:** Main Task 75 with `task-master add-task`
5. **Expand:** Each subtask 75.1-75.9 with `task-master expand --research`
6. **Enrich:** Add context with `task-master update-subtask`
7. **Validate:** Run validation checkpoints above
8. **Assign:** Distribute to team members
9. **Implement:** Reference HANDOFF_75.X_*.md for details
10. **Track:** Use `task-master` commands to monitor progress

