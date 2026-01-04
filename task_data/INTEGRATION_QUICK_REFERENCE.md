# HANDOFF Integration Quick Reference Card

**TL;DR:** Extract 5 sections from HANDOFF files and insert into task files at specific locations.

---

## What Gets Integrated

| Extract From HANDOFF | Insert Into Task File | Location | Label |
|---|---|---|---|
| **What to Build** (3-5 sentences) | New section | After Purpose | Developer Quick Reference |
| **Class Signature** (code block) | Same section | Under "What to Build" | Code example |
| **Implementation Checklist** (bullets) | Each subtask | After Success Criteria | Implementation Checklist (From HANDOFF) |
| **Test Cases** (5-8 numbered items) | Testing subtask | After Success Criteria | Test Case Examples (From HANDOFF) |
| **Git Commands** (bash blocks) | New section | End of file | Technical Reference - Git Commands |
| **Dependencies** (prose) | Same section | Under Git Commands | Dependencies & Parallel Tasks |

---

## 5-Minute Integration Process

For each task (75.1-75.9):

### Step 1: Open Both Files
```bash
# Terminal 1: Task file (editing)
nano task-75.1.md

# Terminal 2: HANDOFF file (reference)
cat HANDOFF_75.1_CommitHistoryAnalyzer.md
```

### Step 2: Add Developer Quick Reference
**After:** `## Purpose` section  
**Extract from HANDOFF:** First 3-5 paragraphs after title

**Template:**
```markdown
## Developer Quick Reference

[Copy: What to Build paragraph]

### Class Signature
[Copy: Code block from HANDOFF]

**See:** HANDOFF_75.1_CommitHistoryAnalyzer.md for full implementation guide
```

### Step 3: Add Implementation Checklist to Each Subtask
**After:** Each subtask's `Success Criteria`  
**Extract from HANDOFF:** "Implementation Checklist" section

**Template:**
```markdown
### Implementation Checklist (From HANDOFF)
- [ ] [First implementation step]
- [ ] [Git command or specific action]
- [ ] [Error handling requirement]
- [ ] [Validation check]
```

### Step 4: Add Test Cases to Testing Subtask
**After:** Testing subtask's `Success Criteria`  
**Extract from HANDOFF:** "Test Cases" section

**Template:**
```markdown
### Test Case Examples (From HANDOFF)

1. **test_case_name_1**
   - Input: ...
   - Expected: ...
   - Validates: ...

2. **test_case_name_2**
   - Input: ...
   - Expected: ...
   - Validates: ...

[... continue with 5-8 test cases ...]
```

### Step 5: Add Technical Reference Appendix
**Before:** `## Done Definition` section  
**Extract from HANDOFF:** Git Commands, Dependencies, Code Patterns

**Template:**
```markdown
---

## Technical Reference (From HANDOFF)

### Git Commands Reference

[Copy: All bash code blocks from HANDOFF]

### Dependencies & Parallel Tasks
[Copy: Dependencies section from HANDOFF]
```

---

## Example: Integration in 2 Minutes

**Original (split across files):**

task-75.1.md (280 lines):
```
## Purpose
Create a reusable Python class...

## Success Criteria
...

## Subtasks
### 75.1.1: Design...
...
```

HANDOFF_75.1.md (139 lines):
```
## What to Build
A Python class `CommitHistoryAnalyzer` that:
1. Extracts commit data...
2. Computes 5 normalized metrics...

### Class Signature
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict

## Implementation Checklist
- [ ] Initialize with repo validation
- [ ] Extract commit data...
```

**After (single integrated file):**

task-75.1.md (420 lines):
```
## Purpose
Create a reusable Python class...

## Developer Quick Reference

A Python class `CommitHistoryAnalyzer` that:
1. Extracts commit data...
2. Computes 5 normalized metrics...

### Class Signature
class CommitHistoryAnalyzer:
    def __init__(self, repo_path: str, main_branch: str = "main")
    def analyze(self, branch_name: str) -> dict

See: HANDOFF_75.1_CommitHistoryAnalyzer.md for full guide

## Success Criteria
...

## Subtasks
### 75.1.1: Design...
...

### Implementation Checklist (From HANDOFF)
- [ ] Initialize with repo validation
- [ ] Extract commit data...

[...etc...]
```

---

## Content Mapping Quick Table

```
HANDOFF Section           → Task File Section          → Line Position
─────────────────────────────────────────────────────────────────────
What to Build             → Developer Quick Reference  → After Purpose
Class Signature           → Developer Quick Reference  → In Dev Ref
Metrics Table             → First subtask or Dev Ref   → Relevant spot
Implementation Checklist  → Each subtask              → After each subT
Test Cases                → Testing subtask           → After criteria
Git Commands              → Technical Reference       → New section
Code Patterns             → Technical Reference       → New section
Dependencies              → Technical Reference       → New section
Configuration             → Configuration section     → Reference from HANDOFF
```

---

## File Size Reference

**Before:**
- task-75.X.md: ~270 lines
- HANDOFF_75.X.md: ~140 lines
- Total (split): 410 lines

**After:**
- task-75.X.md: ~400-430 lines (integrated)
- Final line count: **~120 additional lines** of practical guidance

---

## Integration Checklist

For each of 9 tasks, verify:

- [ ] Developer Quick Reference added after Purpose
- [ ] Class/Function signature visible in Dev Ref
- [ ] All subtasks have Implementation Checklist
- [ ] Testing subtask has Test Case Examples
- [ ] Technical Reference section added at end
- [ ] Git commands included in Technical Reference
- [ ] Dependencies listed in Technical Reference
- [ ] [From HANDOFF] labels applied
- [ ] No duplicate content between sections
- [ ] All code blocks properly formatted
- [ ] No missing content from HANDOFF
- [ ] File size 350-450 lines

---

## Common Mistakes to Avoid

❌ **Don't:** Copy entire HANDOFF file into task file  
✓ **Do:** Extract only the 5 key sections listed above

❌ **Don't:** Leave HANDOFF sections unchanged  
✓ **Do:** Add section headers like `### Implementation Checklist (From HANDOFF)`

❌ **Don't:** Integrate without labels  
✓ **Do:** Add `[From HANDOFF]` to show where content came from

❌ **Don't:** Duplicate content already in task file  
✓ **Do:** Remove overlapping content, keep one version

❌ **Don't:** Make files over 500 lines  
✓ **Do:** Keep to 350-450 lines max

---

## Quality Validation

After integrating each task:

```bash
# Check line count (should be 350-450)
wc -l task-75.X.md

# Verify section headers exist
grep "^###" task-75.X.md | grep -E "(Developer Quick Reference|Implementation Checklist|Test Case Examples|Technical Reference)"

# Check for markdown formatting issues
grep -n "^```" task-75.X.md  # All code blocks closed?

# Verify "From HANDOFF" labels
grep -c "From HANDOFF" task-75.X.md  # Should be 4-5

# Compare with original (make sure nothing lost)
diff task-75.X.md.backup task-75.X.md
```

---

## Time Estimate

| Phase | Time | Count |
|-------|------|-------|
| Read HANDOFF | 10 min | 1 task |
| Extract sections | 10 min | 1 task |
| Insert into task file | 15 min | 1 task |
| Quality review | 10 min | 1 task |
| **Per task total** | **45 min** | **1** |
| **All 9 tasks** | **6-7 hours** | **9** |

---

## When to Reference What

### For Understanding the Integration Approach
→ Read: **INTEGRATION_STRATEGY.md**

### For Seeing an Example (Before/After)
→ Read: **INTEGRATION_EXAMPLE.md**

### For Step-by-Step Instructions
→ Use: **HANDOFF_INTEGRATION_PLAN.md**

### For This Quick Card
→ Read: **This file (INTEGRATION_QUICK_REFERENCE.md)**

---

## Success = Developers Work From Task File Alone

✓ Developers can understand task completely from task-75.X.md  
✓ Developers can see code signatures immediately  
✓ Developers know what to implement (from Quick Ref)  
✓ Developers see test examples (from Test Cases)  
✓ Developers find git commands (from Technical Reference)  
✓ Developers don't need to flip to HANDOFF file  
✓ HANDOFF files still available as optional backup

---

## Key Principle: Content at Point of Use

Rather than forcing developers to cross-reference files, place guidance where it's needed:

- **Purpose section** → Add "what to build" (from HANDOFF)
- **Subtask section** → Add "how to implement" (from HANDOFF)
- **Testing section** → Add "what to test" (from HANDOFF)
- **End section** → Add "technical reference" (from HANDOFF)

Result: Single task file is complete and self-contained.

---

**Ready to integrate? Start with task-75.1.md. Estimate: 45 minutes for one complete task.**
