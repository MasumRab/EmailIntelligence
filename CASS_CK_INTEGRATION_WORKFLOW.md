# Cass + CK Integration Workflow for Safe Task Fixes

**Date:** 2026-02-26  
**Purpose:** Combine `cass search` (Amp session history) with `ck` (semantic/hybrid search) to safely fix task markdown files  
**Target:** 18 parent task files with ~67,000 lines of bloat (91% reduction potential)

---

## Executive Summary

| Tool | Primary Strength | Role in Workflow |
|------|------------------|------------------|
| **`cass`** | Decision provenance (**WHY**) | Preserves rationale for existing content |
| **`ck`** | Content analysis (**WHAT**) | Identifies duplication and structural issues |

**Combined Power:** `cass` tells you **why** content exists, `ck` tells you **what** needs fixing. Together they enable **safe, informed fixes** without losing important context.

---

## Tool Capabilities Mapping

### Cass Search (Amp Session History)

**What it does:**
- Searches AI agent conversation history
- Finds decision rationale and context
- Preserves "why" behind changes

**Key Commands:**
```bash
# Search for specific task discussions
cass search "task 010 deduplication" --agent amp --robot

# Find decision history
cass search "why task 002 has 981 lines" --week --robot

# Export session for reference
cass view ~/.local/share/amp/threads/T-*.json -n 1 --json
```

**Output:** JSON with conversation context, decisions, rationale

---

### CK (Semantic/Hybrid Search)

**What it does:**
- Semantic search finds conceptually similar code
- Hybrid search combines regex + semantic
- Identifies duplication patterns across files

**Key Commands:**
```bash
# Find duplication patterns
ck --hybrid "section duplication" tasks/

# Find specific content patterns
ck --sem "Purpose section" tasks/

# Count section occurrences
ck "## Purpose" tasks/ --files-with-matches
```

**Output:** File locations, line numbers, similarity scores

---

### Tool Comparison

| Aspect | Cass | CK | Combined |
|--------|------|----|----------|
| **Search Target** | Amp sessions (JSONL) | Task files (MD) | Both |
| **Output** | Decision context | Content patterns | Full picture |
| **Best For** | Why decisions made | What needs fixing | Safe fixes |
| **Limitation** | Doesn't analyze files | Doesn't preserve rationale | Neither alone sufficient |

---

## Safe Fix Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAFE TASK FIX WORKFLOW                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐
│   CASS       │         │     CK       │
│   (WHY)      │         │   (WHAT)     │
│              │         │              │
│ • Decision   │         │ • Duplication│
│   history    │         │   detection  │
│ • Rationale  │         │ • Pattern    │
│ • Context    │         │   analysis   │
│ • AI convos  │         │ • Cross-refs │
└──────┬───────┘         └──────┬───────┘
       │                       │
       │                       │
       └───────────┬───────────┘
                   │
                   ▼
         ┌─────────────────┐
         │  CROSS-REFER-   │
         │    ENCE         │
         │                 │
         │ • Compare       │
         │   findings      │
         │ • Identify      │
         │   gaps          │
         │ • Validate      │
         │   safety        │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │   FIX_PLAN.     │
         │      MD         │
         │                 │
         │ • What to keep  │
         │ • What to cut   │
         │ • Why (cass)    │
         │ • Evidence (ck) │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  APPLY FIXES    │
         │                 │
         │ • Edit files    │
         │ • Preserve      │
         │   rationale     │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │   VALIDATE      │
         │                 │
         │ • ck verifies   │
         │   structure     │
         │ • cass records  │
         │   fix decision  │
         └─────────────────┘
```

---

## Risk Assessment

### What Could Go Wrong

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Losing decision context** | High | Medium | `cass` export before changes |
| **Breaking cross-references** | High | Medium | `ck` identifies all references |
| **Removing unique content** | Critical | Low | Cross-validate both tools |
| **Corrupting file structure** | High | Low | Validate with `ck --sem` after |
| **Losing subtask definitions** | Critical | Low | Backup + `cass` session export |

### How Cass + CK Reduce Risk

| Risk | Cass Mitigation | CK Mitigation |
|------|-----------------|---------------|
| Losing context | Exports full session history | N/A |
| Breaking references | Finds why refs exist | Finds all cross-file refs |
| Removing unique | Shows decision rationale | Identifies unique vs duplicate |
| Structure corruption | Records fix rationale | Validates 14-section compliance |

---

## Step-by-Step Workflow

### Phase 1: Pre-Flight Checks

```bash
# 1. Verify cass is working
cass stats --json | jq .conversations

# Expected: Shows conversation count (should be >100)

# 2. Verify ck is working
ck --status .

# Expected: Shows index status (758 files, 15,313 chunks)

# 3. Create backup
mkdir -p backups/task_fix_$(date +%Y%m%d_%H%M%S)
cp tasks/task_0*.md backups/task_fix_$(date +%Y%m%d_%H%M%S)/
```

---

### Phase 2: Discover Duplication (CK)

```bash
# Find all parent task files with excessive sections
for f in tasks/task_0*.md; do
  count=$(grep -c "^## " "$f")
  if [ "$count" -gt 20 ]; then
    echo "$f: $count sections (should be ~13)"
  fi
done

# Find specific duplication patterns
ck --hybrid "section duplication" tasks/ --limit 20

# Find files with IMPORTED_FROM markers
ck "IMPORTED_FROM" tasks/ --files-with-matches

# Count total bloat
total=$(wc -l tasks/task_0*.md | tail -1 | awk '{print $1}')
echo "Total lines in parent tasks: $total"
echo "Expected (18 files × 300 lines): ~5,400"
echo "Potential reduction: $((total - 5400)) lines"
```

**Expected Output:**
```
tasks/task_001.md: 110 sections (should be ~13)
tasks/task_002.md: 128 sections (should be ~13)
...
Total lines in parent tasks: 67327
Expected: ~5,400
Potential reduction: 61,927 lines
```

---

### Phase 3: Capture Decision History (CASS)

```bash
# Search for task-specific discussions
cass search "task 001 deduplication" --agent amp --week --robot \
  > reports/cass_task001_decisions.json

cass search "task 002 section bloat" --agent amp --week --robot \
  > reports/cass_task002_decisions.json

# Search for general dedup decisions
cass search "why keep this section" --agent amp --robot \
  > reports/cass_dedup_rationale.json

# Export relevant sessions
cass view ~/.local/share/amp/threads/T-019c9548-*.json -n 1 --json \
  > reports/cass_latest_session.json
```

**What to look for:**
- Why certain sections were added
- Decisions about what to preserve
- Rationale for current structure

---

### Phase 4: Cross-Reference Analysis

```bash
# Create cross-reference document
cat > reports/FIX_PLAN.md << 'EOF'
# Task Fix Plan

## Files to Fix

| File | Current | Target | Cass Decisions | CK Findings |
|------|---------|--------|----------------|-------------|
| task_001.md | 502 lines | ~300 | [Link to cass report] | 110 sections |
| task_002.md | 981 lines | ~300 | [Link to cass report] | 128 sections |
...

## Content to Preserve (per Cass)

- [ ] Section X: Decision rationale from session T-XXXXX
- [ ] Subtask Y: AI determined this is unique content
...

## Content to Remove (per CK)

- [ ] Duplicate "Purpose" sections (lines 100-150, 300-350)
- [ ] IMPORTED_FROM markers referencing deleted dirs
- [ ] Trailing junk after "Next Steps"
...

## Validation Checkpoints

- [ ] Cass: All decision rationale preserved
- [ ] CK: 14-section compliance verified
- [ ] Both: No unique content lost
EOF
```

---

### Phase 5: Apply Fixes

```bash
# Run the dedup script (dry-run first)
python scripts/dedup_parent_tasks.py --dry-run

# Review changes
git diff tasks/

# Apply fixes
python scripts/dedup_parent_tasks.py

# Verify reduction
wc -l tasks/task_0*.md | tail -1
```

**Expected:**
```
Before: 67,327 lines
After:  ~6,000 lines
Reduction: 61,327 lines (91%)
```

---

### Phase 6: Post-Fix Validation

```bash
# Validate structure with ck
ck --sem "14 section standard" tasks/ --limit 5

# Verify no more duplication
ck --hybrid "duplicate section" tasks/

# Check section compliance
python scripts/check_section_compliance.py

# Record fix decision in cass
# (Start new amp session documenting the fix)
amp "Documenting task fix: removed 61K lines of bloat from 18 parent tasks"
```

---

### Phase 7: Document Fix Decision

```bash
# Create fix summary
cat > reports/TASK_FIX_COMPLETE.md << 'EOF'
# Task Fix Complete

## Summary

- **Files fixed:** 18 parent tasks
- **Lines before:** 67,327
- **Lines after:** 6,000
- **Reduction:** 91% (61,327 lines)

## Decision Rationale (from Cass)

[Link to cass session exports]

## Evidence (from CK)

[Link to ck analysis reports]

## Validation

- [ ] Section compliance: PASS
- [ ] No unique content lost: VERIFIED
- [ ] Cross-references intact: VERIFIED
- [ ] Cass session recorded: DONE
EOF
```

---

## Tool Usage Quick Reference

### When to Use Cass

| Scenario | Command |
|----------|---------|
| Find why content exists | `cass search "why task XXX has Y"` |
| Get decision context | `cass search "task XXX decision" --robot` |
| Export session history | `cass view path/to/session.json --json` |
| Record fix decision | Start new amp session |

### When to Use CK

| Scenario | Command |
|----------|---------|
| Find duplication | `ck --hybrid "duplication" tasks/` |
| Count sections | `ck "## Purpose" tasks/ --files-with-matches` |
| Validate structure | `ck --sem "14 section" tasks/` |
| Find cross-refs | `ck "task_001" tasks/ --files-with-matches` |

### Combined Workflow

```bash
# 1. CK finds the problem
ck --hybrid "section duplication" tasks/

# 2. Cass finds the why
cass search "task 001 structure" --robot

# 3. Cross-reference
# Compare findings, create FIX_PLAN.md

# 4. Apply fix
python scripts/dedup_parent_tasks.py

# 5. Validate with both
ck --sem "14 section" tasks/
cass search "task fix validation" --robot
```

---

## Expected Outcomes

### Before Fix

| Metric | Value |
|--------|-------|
| Total lines | 67,327 |
| Files with >100 sections | 18 |
| Cross-task overlap clusters | 5 |
| IMPORTED_FROM markers | 45 |
| Duplicate content | ~84% |

### After Fix

| Metric | Value | Change |
|--------|-------|--------|
| Total lines | ~6,000 | -91% |
| Files with >100 sections | 0 | -100% |
| Cross-task overlap clusters | 0 | -100% |
| IMPORTED_FROM markers | 0 | -100% |
| Duplicate content | <10% | -88% |

---

## Troubleshooting

### Issue: Cass finds no sessions

```bash
# Check cass index
cass stats --json

# Rebuild if needed
cass index --full
```

### Issue: CK finds no duplication

```bash
# Verify ck index
ck --status .

# Force reindex
ck --index --force .
```

### Issue: Fix script fails

```bash
# Run with verbose output
python scripts/dedup_parent_tasks.py --verbose

# Check specific file
python scripts/dedup_parent_tasks.py --file tasks/task_001.md
```

---

## Resources

- **Cass Documentation:** `cass --help`
- **CK Documentation:** `ck --help`
- **Cass Integration:** `CASS_INTEGRATION.md`
- **CK Analysis:** `CK_SEMANTIC_SEARCH_ANALYSIS.md`
- **Fix Script:** `scripts/dedup_parent_tasks.py`

---

**Last Updated:** 2026-02-26  
**Status:** Ready for execution  
**Risk Level:** Low (with both tools used together)
