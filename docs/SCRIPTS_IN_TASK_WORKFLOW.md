# Scripts in Task Workflow - Implementation Guide

**Version:** 1.0  
**Created:** January 6, 2026  
**Purpose:** Detailed usage guide for helper scripts alongside task execution

---

## Overview

Each `task_XXX-Y.md` file lists optional helper scripts that accelerate work or provide validation. This document provides detailed usage for each script without cluttering individual task files.

**Key principle:** Scripts are optional conveniences, not requirements. Every task is completable without using any scripts.

---

## Quick Reference by Task Type

### Task Execution Scripts (Use During Implementation)

| Script | Purpose | When to Use | Complexity |
|--------|---------|-----------|-----------|
| `memory_api.py` | Progress logging | After each sub-subtask | Low |
| `compare_task_files.py` | Validate output format | After completing task | Medium |
| `query_findings.py` | Review research findings | Planning phase | Medium |
| `compress_progress.py` | Archive long-term records | End of phase | Medium |

### Task Management Scripts (Use Between Tasks)

| Script | Purpose | When to Use | Complexity |
|--------|---------|-----------|-----------|
| `list_tasks.py` | View all tasks | Daily standup | Low |
| `show_task.py` | View single task details | Getting started | Low |
| `next_task.py` | Find next available task | Task selection | Low |
| `search_tasks.py` | Search tasks by keyword | Planning/discovery | Low |
| `task_summary.py` | Generate progress summary | Weekly reviews | Low |

### Advanced Scripts (Rare Use)

| Script | Purpose | When to Use | Complexity |
|--------|---------|-----------|-----------|
| `generate_clean_tasks.py` | Create new task files | Phase start | High |
| `enhance_tasks_from_archive.py` | Enhance existing tasks | Task migration | High |
| `split_enhanced_plan.py` | Split plan into task files | Major restructuring | High |
| `regenerate_tasks_from_plan.py` | Regenerate tasks.json | Recovery operations | High |
| `find_lost_tasks.py` | Recover lost tasks | Emergency recovery | High |
| `list_invalid_tasks.py` | Find completed/archived tasks | Archival operations | Medium |
| `markdownlint_check.py` | Validate markdown syntax | CI/CD checks | Low |

---

## Task Execution Scripts (During Implementation)

### Memory API - Progress Logging

**Reference task:** All `task_002.X.md` files  
**Required?** No - manual git commits sufficient  
**Best for:** Multi-session work, agent handoffs, decision logging

#### Why Use It?

- Maintains session continuity across development sessions
- Enables agent handoffs without context loss
- Documents decision history and blockers
- Tracks metrics: lines added, files modified, tests written

#### Quick Start

```python
from memory_api import AgentMemory

# Load session
memory = AgentMemory()
memory.load_session()

# Log after completing sub-subtask
memory.add_work_log(
    action="Completed Task 002.1.3",
    details="Implemented commit recency metric with exponential decay"
)

# Mark subtask complete
memory.update_todo("task_002_1_3", "completed")

# Save progress
memory.save_session()
```

#### Common Operations

**Track Work Activity:**
```python
memory.add_work_log(
    action="Analyzed branch clustering algorithm",
    details="Tested Ward linkage on 50 branches, verified quality metrics"
)
```

**Update Task Status:**
```python
memory.update_todo("task_id", "in_progress")
memory.update_todo("task_id", "completed")
```

**Log Decisions:**
```python
memory.add_decision(
    decision_id="dec_1",
    decision="Use scipy.cluster for Ward linkage",
    rationale="Industry standard, proven on large datasets",
    impact="Reduced implementation time by 40%"
)
```

**Check Progress:**
```python
# Get summary
memory.print_summary()

# Get metrics
metrics = memory.get_metrics()
print(f"Lines added: {metrics.get('lines_added', 0)}")
```

**Query Outstanding Work:**
```python
# Get high-priority pending items
todos = memory.get_outstanding_todos(priority="high", status="pending")

# Get ready tasks
ready = memory.get_ready_tasks()

# Get blocked tasks
blocked = memory.get_blocked_tasks()
```

#### Troubleshooting

**Error: "session_log.json not found"**
```python
# Creates new session automatically
memory = AgentMemory()
memory.load_session()  # Returns False, but creates default session
memory.save_session()  # Initializes file
```

**Error: "Cannot parse existing session"**
```bash
# Check JSON syntax
python -m json.tool .agent_memory/session_log.json

# Restore from backup if corrupted
cp .agent_memory/session_log.json.bak .agent_memory/session_log.json
```

**No data appearing after save?**
```python
# Verify save succeeded
success = memory.save_session()
if not success:
    print("Failed to save session")

# Check file permissions
# Must have write access to .agent_memory/session_log.json
```

#### Full API Reference

See `.agent_memory/MEMORY_SYSTEM_GUIDE.md` for complete documentation.

---

### compare_task_files.py - Output Validation

**Reference task:** Any implementation task (optional after completion)  
**Required?** No - manual verification against specification sufficient  
**Best for:** Automated format checking, schema validation, catching errors early

#### Why Use It?

- Validates output JSON matches expected schema
- Catches format errors before downstream tasks fail
- Compares task files for differences (useful after merges)
- Saves debugging time in downstream task integration

#### Usage Scenarios

**Scenario 1: Validate CommitHistoryAnalyzer Output**

After completing task 002.1 implementation:

```bash
python scripts/compare_task_files.py \
  --validate src/analyzers/commit_history.py \
  --schema specification.json
```

**Expected output (success):**
```
✓ Schema validation passed
  - 13 branches processed
  - All metrics in [0,1] range
  - All required fields present
  - Ready for Task 002.4 (BranchClusterer)
```

**Expected output (failure):**
```
✗ Schema validation failed
  - Branch "feature/auth": merge_readiness=1.5 (should be [0,1])
  - Branch "develop": missing field "stability_score"
  - Check: task_002.1.md § Specification § Output Format
```

**Scenario 2: Compare Task Files After Merge**

```bash
python scripts/compare_task_files.py \
  --compare tasks.json tasks_expanded.json
```

**Output:**
```
tasks.json vs tasks_expanded.json:
  Added: 5 tasks
  Removed: 0 tasks
  Modified: 12 tasks
```

**Scenario 3: Find Differences Between Versions**

```bash
python scripts/compare_task_files.py \
  --compare task_002.1.md task_002.1_backup.md \
  --show-diff
```

#### Command Reference

```bash
# Validate JSON schema
python scripts/compare_task_files.py \
  --validate <output_file> \
  --schema <schema_file>

# Compare two task files
python scripts/compare_task_files.py \
  --compare <file1> <file2>

# Show detailed differences
python scripts/compare_task_files.py \
  --compare <file1> <file2> \
  --show-diff

# Generate validation report
python scripts/compare_task_files.py \
  --validate <file> \
  --output report.txt
```

#### Troubleshooting

**Error: "Schema file not found"**
→ Ensure schema.json exists in same directory as output file, or specify path:
```bash
python scripts/compare_task_files.py \
  --validate src/output.json \
  --schema src/schemas/analyzer_schema.json
```

**Error: "Validation failed: metrics outside [0,1]"**
→ See task_002.X.md § Common Gotchas § Metrics Outside Range  
→ Add bounds checking:
```python
# WRONG
recency = math.exp(-days / 30)

# RIGHT
recency = min(1.0, max(0.0, math.exp(-days / 30)))
```

**Error: "Required field missing"**
→ Check Specification § Output Format in your task file  
→ Verify all fields in output JSON:
```python
required_fields = ["branch_name", "metrics", "aggregate_score"]
for field in required_fields:
    assert field in output, f"Missing field: {field}"
```

---

### query_findings.py - Research Discovery

**Reference task:** Planning phases (especially Tasks 001-002)  
**Required?** No - findings also documented in task files  
**Best for:** Researching decisions, finding examples, understanding architecture

#### Why Use It?

- Queries research findings from prior investigation phases
- Finds relevant examples and patterns
- Speeds up decision-making during planning
- References decision rationale from earlier phases

#### Usage Scenarios

**Find research for your task:**
```bash
# Search by task ID
python scripts/query_findings.py --task 002.1

# Output:
# Task 002.1: CommitHistoryAnalyzer findings
# - Commit frequency metric formula
# - Performance baseline: <2s per branch
# - Edge case: single-commit branches
```

**Find all findings from a phase:**
```bash
python scripts/query_findings.py --phase phase2_assessment

# Output:
# Phase 2 Assessment Findings (Date range: 2025-12-15 to 2026-01-06)
# - 5 tasks analyzed
# - 3 critical decisions documented
# - 12 examples provided
```

**Search for specific patterns:**
```bash
# Search for "merge-base" algorithm
python scripts/query_findings.py --pattern "merge-base"

# Output: All findings mentioning merge-base algorithm
```

**Find findings in date range:**
```bash
python scripts/query_findings.py \
  --from 2026-01-01 \
  --to 2026-01-31
```

**Get summary statistics:**
```bash
python scripts/query_findings.py --stats

# Output:
# Summary Statistics:
#   total_findings: 127
#   successful: 119
#   success_rate: 93.7%
#   phases: [phase1, phase2, phase3]
#   date_range: 2025-12-15 to 2026-01-06
```

#### Output Formats

**Table format (default):**
```bash
python scripts/query_findings.py --task 002.1

# Output:
# Task ID     Phase                Success   Duration   Decision
# ──────────────────────────────────────────────────────────────
# 002.1       phase2_assessment    True      2340ms     Use exponential decay for recency
# 002.1       phase2_assessment    True      1850ms     Normalize all metrics to [0,1]
```

**JSON format (for parsing):**
```bash
python scripts/query_findings.py --task 002.1 --format json

# Output: Structured JSON for automated processing
```

#### Troubleshooting

**Error: "Findings directory not found"**
→ Findings are stored in `task_data/findings/phase*/`  
→ Ensure directory structure exists:
```bash
ls -la task_data/findings/
# Should show: phase1/, phase2/, phase3/, etc.
```

**No findings returned for task:**
→ Task findings may not have been documented yet  
→ Check task file comments instead  
→ Or search by keyword:
```bash
python scripts/query_findings.py --pattern "BranchClusterer"
```

---

### compress_progress.py - Archive Progress Records

**Reference task:** End of phase (especially after large tasks)  
**Required?** No - progress files can be kept as-is  
**Best for:** Long-term storage, reducing disk space, backup management

#### Why Use It?

- Compresses progress tracking files to save disk space
- Creates timestamped archives for version control
- Generates checksums for integrity verification
- Enables fast decompression for recovery

#### Usage Scenarios

**Compress progress files after Phase 1 completion:**

```bash
python scripts/compress_progress.py \
  --compress \
  --source ./ \
  --destination backups/ \
  --format xz
```

**Output:**
```
Compression complete: progress_all_20260106_120000.tar.xz
  Files: 247
  Original: 18.45 MB
  Compressed: 3.21 MB
  Ratio: 82.6%
  Manifest: progress_all_20260106_120000.tar.xz.manifest.json
```

**List compressed archives:**

```bash
python scripts/compress_progress.py

# Output:
# Available archives:
#   progress_all_20260106_120000.tar.xz              3.21 MB  [247 files, 82.6% reduction]
#   progress_essential_20260105_150000.tar.xz        1.45 MB  [52 files, 91.2% reduction]
```

**Verify archive integrity:**

```bash
python scripts/compress_progress.py \
  --verify \
  --archive progress_all_20260106_120000.tar.xz

# Output:
# Archive verification PASSED: progress_all_20260106_120000.tar.xz
#   Files: 247
#   Status: All checks passed
```

**Restore from archive:**

```bash
python scripts/compress_progress.py \
  --decompress \
  --archive progress_all_20260106_120000.tar.xz \
  --restore-to recovery/
```

**Compress only essential files:**

```bash
# Smaller backup, faster restore
python scripts/compress_progress.py \
  --compress \
  --essential-only \
  --source ./ \
  --destination backups/
```

#### Compression Formats

| Format | Compression | Speed | Best For |
|--------|-----------|-------|----------|
| `gz` | Good (40-50%) | Fast | Quick backups |
| `bz2` | Better (60-70%) | Medium | Balanced |
| `xz` | Best (75-85%) | Slow | Long-term storage |

```bash
# Use gzip for speed
python scripts/compress_progress.py \
  --compress \
  --format gz

# Use xz for size (default)
python scripts/compress_progress.py \
  --compress \
  --format xz

# Use bz2 for balance
python scripts/compress_progress.py \
  --compress \
  --format bz2
```

#### Troubleshooting

**Error: "No files found to compress"**
→ Ensure source directory contains compressible files  
→ Check file extensions (.md, .json, .txt, etc.)  
→ Use `--essential-only` to compress only critical files

**Error: "Destination directory does not exist"**
→ Script creates destination automatically  
→ Check permissions on parent directory

**Decompression fails with checksum error:**
→ Archive may be corrupted  
→ Restore from another backup  
→ Verify archive first:
```bash
python scripts/compress_progress.py \
  --verify \
  --archive <archive_name>
```

---

## Task Management Scripts (Between Tasks)

### list_tasks.py - View All Tasks

**When to use:** Daily standup, project planning  
**Learning curve:** Very low  
**Output:** Table of all tasks with status

```bash
# List all tasks
python scripts/list_tasks.py

# Output:
# ID    Title                              Status       Priority
# ──────────────────────────────────────────────────────────────
# 001   Framework Setup                    done         high
# 002   Branch Clustering System           in-progress  high
# 003   Integration Validation             pending      medium
```

**Filter by status:**
```bash
python scripts/list_tasks.py --status pending

# Show only high-priority pending tasks
python scripts/list_tasks.py --status pending --priority high
```

**Show subtasks:**
```bash
python scripts/list_tasks.py --show-subtasks

# Output includes:
# 002.1  CommitHistoryAnalyzer             pending      high
# 002.2  CodebaseStructureAnalyzer         pending      high
# 002.3  DiffDistanceCalculator            pending      high
```

---

### show_task.py - View Task Details

**When to use:** Getting started on a task  
**Learning curve:** Very low  
**Output:** Complete task specification

```bash
# Show task 002.1
python scripts/show_task.py 002.1

# Output:
# ════════════════════════════════════════════
# Task 002.1: CommitHistoryAnalyzer
# ════════════════════════════════════════════
# Status: pending
# Priority: high
# Effort: 24-32 hours
# Dependencies: Task 002.0 (setup)
#
# Purpose:
#   Extract commit history metrics for branches...
#
# Success Criteria:
#   - [ ] Accepts repo_path and branch_name
#   - [ ] Extracts commit data using git log
#   - [ ] Computes 5 normalized metrics
#   ... (all criteria listed)
```

---

### next_task.py - Find Next Available Task

**When to use:** Selecting what to work on  
**Learning curve:** Very low  
**Output:** Next ready task with dependencies

```bash
# Get next available task
python scripts/next_task.py

# Output:
# Next available task:
#   Task 002.1 (CommitHistoryAnalyzer)
#   Status: pending
#   No dependencies blocking
#   Ready to start immediately
#   Effort: 24-32 hours
```

---

### search_tasks.py - Search by Keyword

**When to use:** Finding related tasks  
**Learning curve:** Very low  
**Output:** Tasks matching search term

```bash
# Search for clustering tasks
python scripts/search_tasks.py "clustering"

# Search case-sensitive
python scripts/search_tasks.py Backend --case-sensitive

# Show context around match
python scripts/search_tasks.py "migration" --show-context

# Output:
# Task 002: Branch Clustering System
#   → Found in description
#
# Task 002.4: BranchClusterer
#   → Found in title
#
# Context:
#   "...hierarchical clustering with Ward linkage..."
```

---

### task_summary.py - Generate Progress Summary

**When to use:** Weekly reviews, progress reporting  
**Learning curve:** Very low  
**Output:** Statistics and completion status

```bash
python scripts/task_summary.py

# Output:
# ════════════════════════════════════════════
# Task Summary Report
# ════════════════════════════════════════════
#
# Overall Progress: 8/26 tasks complete (31%)
#
# By Status:
#   Done: 8 tasks
#   In Progress: 3 tasks
#   Pending: 15 tasks
#
# By Priority:
#   High: 5 done, 3 in-progress, 8 pending
#   Medium: 3 done, 0 in-progress, 5 pending
#   Low: 0 done, 0 in-progress, 2 pending
#
# Current Bottlenecks:
#   - Task 002.2 blocked by Task 002.1
#   - Task 002.4 blocked by Tasks 002.1-2.3
#
# Upcoming Milestones:
#   - Complete Task 002: Jan 31 (estimated)
#   - Start Task 003: Feb 1 (estimated)
```

---

## Advanced Scripts (Rare Use)

These scripts are only needed for major restructuring or emergency recovery.

### generate_clean_tasks.py

**When to use:** Starting a new task phase  
**Learning curve:** High  
**Purpose:** Generate clean sequential task files

```bash
# Generate sequential tasks 001-020
python scripts/generate_clean_tasks.py

# Creates: task_001.md through task_020.md with empty templates
```

---

### find_lost_tasks.py

**When to use:** Recovering accidentally deleted tasks  
**Learning curve:** High  
**Purpose:** Find tasks in git history not in current files

```bash
# Search last 50 commits
python scripts/find_lost_tasks.py --commits 50

# Save results to file
python scripts/find_lost_tasks.py \
  --commits 100 \
  --output lost_tasks.json \
  --verbose
```

---

## Integration with Task Files

Each `task_XXX-Y.md` file includes a "Helper Tools (Optional)" section that references this guide.

**Example from task_002.1.md:**

```markdown
## Helper Tools (Optional)

### Progress Logging

After completing sub-subtask 002.1.3, optionally log progress:

```python
from memory_api import AgentMemory
memory = AgentMemory()
memory.load_session()
memory.add_work_log("Completed 002.1.3", "Implemented recency metric")
memory.save_session()
```

**See:** SCRIPTS_IN_TASK_WORKFLOW.md § Memory API for full usage
```

---

## Summary

| Tool | Use Case | Complexity | Learning Time |
|------|----------|-----------|----------------|
| **Memory API** | Session logging | Low | 10 min |
| **compare_task_files.py** | Output validation | Medium | 15 min |
| **list_tasks.py** | View all tasks | Low | 5 min |
| **show_task.py** | View task details | Low | 5 min |
| **next_task.py** | Find next task | Low | 5 min |
| **search_tasks.py** | Search tasks | Low | 5 min |
| **task_summary.py** | Progress report | Low | 5 min |
| **compress_progress.py** | Archive files | Medium | 20 min |
| **query_findings.py** | Research discovery | Medium | 15 min |

**Getting Started:**
1. Use `list_tasks.py` and `next_task.py` daily
2. Add Memory API calls after each sub-subtask
3. Use `compare_task_files.py` when completing tasks
4. Use advanced scripts only when needed

---

**Last Updated:** January 6, 2026  
**Status:** Ready for Integration with Task Files
