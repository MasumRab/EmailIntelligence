# Subtask Expansion Template

Use this template to create a main task file that can expand into subtask files.

## Usage Pattern

1. Fill out this template with subtask definitions
2. Copy to `task-XX.md` (main task file)
3. Use the expansion script to generate `task-XX-1.md`, `task-XX-2.md`, etc.

---

## MAIN TASK CONFIGURATION

# Task XX: [TASK TITLE]

**Status:** pending
**Priority:** [high/medium/low]
**Effort:** [X-Y hours]
**Complexity:** [1-10]
**Dependencies:** [None or parent task]

---

## SUBTASK DEFINITIONS

### Subtask 1: [SUBTASK 1 TITLE]

| Field | Value |
|-------|-------|
| **ID** | XX.1 |
| **Title** | [Subtask 1 Title] |
| **Status** | pending |
| **Priority** | high |
| **Effort** | [X-Y hours] |
| **Complexity** | [1-10] |
| **Dependencies** | None |
| **Owner** | [optional] |

**Purpose:**
[Brief description of what this subtask accomplishes]

**Details:**
[Detailed description of scope and requirements]

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Test Strategy:**
[How to verify completion]

---

### Subtask 2: [SUBTASK 2 TITLE]

| Field | Value |
|-------|-------|
| **ID** | XX.2 |
| **Title** | [Subtask 2 Title] |
| **Status** | pending |
| **Priority** | high |
| **Effort** | [X-Y hours] |
| **Complexity** | [1-10] |
| **Dependencies** | XX.1 |
| **Owner** | [optional] |

**Purpose:**
[Brief description of what this subtask accomplishes]

**Details:**
[Detailed description of scope and requirements]

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Test Strategy:**
[How to verify completion]

---

### Subtask 3: [SUBTASK 3 TITLE]

| Field | Value |
|-------|-------|
| **ID** | XX.3 |
| **Title** | [Subtask 3 Title] |
| **Status** | pending |
| **Priority** | [high/medium/low] |
| **Effort** | [X-Y hours] |
| **Complexity** | [1-10] |
| **Dependencies** | XX.1, XX.2 |
| **Owner** | [optional] |

**Purpose:**
[Brief description of what this subtask accomplishes]

**Details:**
[Detailed description of scope and requirements]

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Test Strategy:**
[How to verify completion]

---

## EXPANSION COMMANDS

```bash
# Generate subtask files from this template
python scripts/expand_subtasks.py --task XX --template task-XX.md

# Or manually copy template sections:
cp task-XX.md task-XX-1.md
cp task-XX.md task-XX-2.md
cp task-XX.md task-XX-3.md
# Then edit each file to keep only relevant sections
```

## DEPENDENCY GRAPH

```
                    [Parent Task]
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
    [XX.1]           [XX.2]           [XX.3]
        │               │               │
        └───────────────┴───────────────┘
                        │
                        ▼
                  [XX.4/Next Task]
```

---

## PROGRESS TRACKING

| Subtask | Status | Effort | Completed |
|---------|--------|--------|-----------|
| XX.1 | [pending/in_progress/done] | Xh | YYYY-MM-DD |
| XX.2 | [pending/in_progress/done] | Xh | YYYY-MM-DD |
| XX.3 | [pending/in_progress/done] | Xh | YYYY-MM-DD |

**Total Progress:** 0/3 subtasks (0%)
**Total Effort:** 0/X hours

---

## EXAMPLE: FILES GENERATED

After expansion, create these files:

| File | Subtask | Purpose |
|------|---------|---------|
| `task-XX.md` | Main | Overview and coordination |
| `task-XX-1.md` | Subtask 1 | Implementation details |
| `task-XX-2.md` | Subtask 2 | Implementation details |
| `task-XX-3.md` | Subtask 3 | Implementation details |

---

## NOTES

- Update `task-XX.md` progress table when subtasks complete
- Keep subtask files self-contained (all info needed for implementation)
- Use consistent naming: `task-XX-Y.md` format
- Each subtask file should be independently actionable
