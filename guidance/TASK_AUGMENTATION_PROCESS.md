# Task Augmentation Process

**Purpose**: Systematically enrich canonical tasks with content from archive sources
**Last Updated**: 2026-02-03

---

## ⛔ Pre-Augmentation Checklist

Before augmenting any task, verify:

- [ ] Read [PROJECT_IDENTITY.md](../PROJECT_IDENTITY.md) - understand project scope
- [ ] Target task exists in `tasks/` with underscore naming (`task_XXX.md`)
- [ ] Archive source contains alignment-related content (not separate project/email content)
- [ ] Backup exists or will be created before modification

---

## Archive Source Hierarchy

Use sources in this priority order (richest first):

| Priority | Source | Path | Content Type |
|----------|--------|------|--------------|
| 1 | Enhanced Improved | `enhanced_improved_tasks/` | Richest specs, formulas, schemas |
| 2 | Restructured 14-Section | `restructured_tasks_14_section/` | 14-section formatted tasks |
| 3 | Improved Tasks | `improved_tasks/` | Enhanced descriptions |
| 4 | Task 75 Handoffs | `task_data/archived/handoff_archive_task75/` | Technical specs for Task 002.* |
| 5 | Task 75 Backups | `task_data/archived/backups_archive_task75/` | Backup specs for Task 002.* |
| 6 | Migration Backup | `task_data/migration_backup_20260129/` | Pre-migration state |
| 7 | Archive Docs | `archive/` | Project docs, phase planning |

---

## File Naming Mappings

Archive files use hyphen naming; canonical tasks use underscore naming:

| Archive Pattern | Canonical Pattern | Example |
|-----------------|-------------------|---------|
| `task-001.md` | `task_001.md` | Main task |
| `task-001-1.md` | `task_001.1.md` | Subtask |
| `task-002-4.md` | `task_002.4.md` | Subtask |
| `HANDOFF_75.4_*.md` | `task_002.4.md` | Task 75 → Task 002 mapping |

### Task 75 → Task 002 Subtask Mapping

| Archive File | Canonical Target |
|--------------|------------------|
| `HANDOFF_75.1_CommitHistoryAnalyzer.md` | `task_002.1.md` |
| `HANDOFF_75.2_CodebaseStructureAnalyzer.md` | `task_002.2.md` |
| `HANDOFF_75.3_DiffDistanceCalculator.md` | `task_002.3.md` |
| `HANDOFF_75.4_BranchClusterer.md` | `task_002.4.md` |
| `HANDOFF_75.5_IntegrationTargetAssigner.md` | `task_002.5.md` |
| `HANDOFF_75.6_PipelineIntegration.md` | `task_002.6.md` |
| `HANDOFF_75.7_VisualizationReporting.md` | `task_002.7.md` |
| `HANDOFF_75.8_TestingSuite.md` | `task_002.8.md` |
| `HANDOFF_75.9_FrameworkIntegration.md` | `task_002.9.md` |

---

## Augmentation Rules

### Rule 1: Additive Only
- **NEVER** replace existing content
- **ALWAYS** append new content
- **PRESERVE** existing sections intact

### Rule 2: Provenance Markers
Add import markers before any appended content:

```markdown
<!-- IMPORTED_FROM: /path/to/source/file.md -->

[imported content here]
```

### Rule 3: Placement
- Append imported content under `## Implementation Guide` section
- If no Implementation Guide exists, create it before appending
- Keep existing sections in original order

### Rule 4: Deduplication
- Check if content already exists before importing
- Skip content that duplicates existing sections
- Note skipped imports in augmentation log

### Rule 5: Scope Filtering
- **INCLUDE**: Git, branch, merge, clustering, validation content
- **EXCLUDE**: Email, separate project, EmailIntelligence content
- **CHECK**: [PROJECT_IDENTITY.md](../PROJECT_IDENTITY.md) if uncertain

---

## Step-by-Step Augmentation Process

### Phase 1: Preparation

```bash
# 1. Identify target task
TARGET="task_002.4.md"

# 2. Create backup (optional but recommended)
cp tasks/$TARGET backups/task_markdown_backups/$(basename $TARGET .md)/

# 3. Identify source files (in priority order)
SOURCES=(
  "enhanced_improved_tasks/task-002-4.md"
  "restructured_tasks_14_section/task-002-4.md"
  "task_data/archived/handoff_archive_task75/HANDOFF_75.4_BranchClusterer.md"
)
```

### Phase 2: Content Extraction

For each source file (in priority order):

1. **Read source file**
2. **Identify extractable sections**:
   - Metric formulas
   - Input/output schemas
   - Algorithm specifications
   - Test cases
   - Code examples
3. **Check for duplicates** in target
4. **Skip if already present**

### Phase 3: Append Content

```markdown
## Implementation Guide

[existing content...]

<!-- IMPORTED_FROM: /path/to/enhanced_improved_tasks/task-002-4.md -->

### Clustering Algorithm (from enhanced source)
[extracted content]

<!-- IMPORTED_FROM: /path/to/task_data/archived/handoff_archive_task75/HANDOFF_75.4_BranchClusterer.md -->

### Detailed Specifications (from Task 75 handoff)
[extracted content]
```

### Phase 4: Validation

After augmentation:

1. **Verify 14-section structure** (see TASK_STRUCTURE_STANDARD.md)
2. **Check for broken references**
3. **Validate dependencies** point to correct task IDs
4. **Confirm no separate project content** was accidentally imported

---

## Augmentation Workflow Diagram

```
┌─────────────────┐
│ Select Target   │
│ Task (tasks/)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Check Sources   │
│ (priority order)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│ Content Already │─Yes─▶│ Skip Source  │
│ Present?        │      └──────────────┘
└────────┬────────┘
         │ No
         ▼
┌─────────────────┐     ┌──────────────┐
│ Alignment       │─No──▶│ Skip Source  │
│ Scope Content?  │      └──────────────┘
└────────┬────────┘
         │ Yes
         ▼
┌─────────────────┐
│ Add Provenance  │
│ Marker          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Append Under    │
│ Implementation  │
│ Guide Section   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Next Source or  │
│ Complete        │
└─────────────────┘
```

---

## Example: Augmenting task_002.4.md

### Before Augmentation

```markdown
# Task 002.4: BranchClusterer

**Status:** pending
...

## Implementation Guide

Implementation guide to be defined
```

### After Augmentation

```markdown
# Task 002.4: BranchClusterer

**Status:** pending
...

## Implementation Guide

Implementation guide to be defined

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/enhanced_improved_tasks/task-002-4.md -->

### Clustering Algorithm
- Hierarchical agglomerative clustering (Ward's method)
- Weighted formula: 35% commit history + 35% codebase + 30% diff distance
- Threshold: 0.5 (configurable)

<!-- IMPORTED_FROM: /home/masum/github/PR/.taskmaster/task_data/archived/handoff_archive_task75/HANDOFF_75.4_BranchClusterer.md -->

### Quality Metrics
- Silhouette score
- Davies-Bouldin index
- Calinski-Harabasz index

### Input Schema
```json
{
  "branches": [...],
  "analyzer_outputs": {...}
}
```
```

---

## Batch Augmentation Script Template

```python
#!/usr/bin/env python3
"""
Batch augment tasks from archive sources.
Usage: python augment_tasks.py --task 002.4 --dry-run
"""

import argparse
from pathlib import Path

ARCHIVE_SOURCES = [
    "enhanced_improved_tasks",
    "restructured_tasks_14_section",
    "improved_tasks",
    "task_data/archived/handoff_archive_task75",
    "task_data/archived/backups_archive_task75",
]

def find_source_files(task_id: str) -> list[Path]:
    """Find all archive files matching a task ID."""
    # Implementation: search sources in priority order
    pass

def check_duplicate(target: Path, content: str) -> bool:
    """Check if content already exists in target."""
    pass

def append_with_provenance(target: Path, source: Path, content: str):
    """Append content with IMPORTED_FROM marker."""
    pass

def augment_task(task_id: str, dry_run: bool = True):
    """Main augmentation logic."""
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    augment_task(args.task, args.dry_run)
```

---

## Post-Augmentation Checklist

- [ ] All imported content has `<!-- IMPORTED_FROM: ... -->` markers
- [ ] No existing content was replaced or deleted
- [ ] Task follows 14-section structure
- [ ] Dependencies reference correct task IDs (not old 75.* or 005.* refs)
- [ ] No separate project/EmailIntelligence content was imported
- [ ] Changes committed with descriptive message

---

## Marker Cleanup (Future)

After final audit, IMPORTED_FROM markers can be removed:

```bash
# Find all markers
grep -r "IMPORTED_FROM" tasks/

# Remove markers (only after audit approval)
sed -i '/<!-- IMPORTED_FROM:/d' tasks/*.md
```

---

## Related Documents

- [PROJECT_IDENTITY.md](../PROJECT_IDENTITY.md) - Project scope definition
- [TASK_STRUCTURE_STANDARD.md](../TASK_STRUCTURE_STANDARD.md) - 14-section format
- [ORACLE_RECOMMENDATION_TODO.md](../ORACLE_RECOMMENDATION_TODO.md) - Outstanding work items
