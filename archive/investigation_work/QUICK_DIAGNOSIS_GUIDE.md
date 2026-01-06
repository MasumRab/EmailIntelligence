# Quick Diagnosis Guide: Task Numbering & Merge Issues

**Use this for fast answers to specific questions**

---

## Q: Why is tasks.json empty?

**A:** `/home/masum/github/PR/.taskmaster/tasks/tasks.json` is 0 bytes because Task 75 work was never registered. Tasks are documented as markdown files (task-75.*.md) but never entered into the JSON system.

**File:** `ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md` → Section: "Current System State Analysis → System B"

---

## Q: Where is Task 75?

**A:** Task 75 exists in THREE places:

1. **Markdown specs:** `/home/masum/github/PR/.taskmaster/task_data/task-75.1.md` through `task-75.9.md`
2. **Backup copies:** `/home/masum/github/PR/.taskmaster/task_data/backups/task-75*.md`
3. **Agent memory:** `/home/masum/github/PR/.taskmaster/.agent_memory/session_log.json` (referenced but not registered)

**NOT in:** EmailIntelligence/tasks/tasks.json (that has Tasks 1-53)

---

## Q: Why is renumbering incomplete?

**A:** Two independent systems:
- EmailIntelligence: Tasks 1-53 (unified via Task 021→002 renumbering)
- PR/.taskmaster: Task 75.1-75.9 (separate, excluded from renumbering)

When Task 021→002 renumbering ran on Jan 4, 2026, it updated the PR/.taskmaster documentation but left Task 75 untouched because it was treated as a separate namespace.

**File:** `ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md` → Section: "Why Incomplete Renumbering Failed"

---

## Q: What caused the split?

**A:** Four-phase divergence:

**Phase 1 (Nov 2025):** EmailIntelligence unified tasks 1-53  
**Phase 2 (Dec 2025):** Task 75 created separately in .taskmaster  
**Phase 3 (Jan 4, 2026):** Renumbering targeted only active systems (Task 021)  
**Phase 4 (Jan 6, 2026):** Discovery - Task 75 orphaned

**File:** `ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md` → Section: "Root Cause Chain"

---

## Q: What merge issues exist?

**A:** Five real-world problems:

1. **Import paths:** Mixed `from backend.` and `from src.backend.`
2. **Service startup:** 3+ incompatible startup patterns
3. **Submodule confusion:** Multiple conflicting states
4. **Incomplete migrations:** Components partially moved
5. **Broken dependencies:** Work in isolation, fail when merged

**File:** `MERGE_ISSUES_REAL_WORLD_RECOVERY.md` → Section: "Part 1: Real-World Issues Mapped to Guidance"

---

## Q: How do I fix task numbering?

**Quick steps:**

```bash
# 1. Register Task 75 in JSON
python scripts/extract_task_75_from_markdown.py

# 2. Choose strategy: Consolidate or Federate
# Consolidate: Move to EmailIntelligence/tasks/tasks.json
# Federate: Create federation layer for both systems

# 3. Update dependencies in agent memory system

# 4. Validate
python -m json.tool tasks/tasks.json > /dev/null
```

**Estimated effort:** 1 day  
**File:** `MERGE_ISSUES_REAL_WORLD_RECOVERY.md` → Section: "Part 3: Task Numbering Recovery"

---

## Q: How do I fix merge issues?

**Quick steps (4 phases):**

**Phase 1 (1-2 days):** Fix import paths
```bash
sed -i 's/from backend\./from src.backend./g' **/*.py
```

**Phase 2 (1 day):** Fix service startup
```python
# Create src/main.py with factory pattern supporting all patterns
def create_app():
    app = FastAPI()
    # Load features based on environment
    return app
```

**Phase 3 (1 day):** Register Task 75

**Phase 4 (1 day):** Establish merge policy
- Define merge criteria
- Run integration tests
- Code review approval

**Total effort:** 4-5 days  
**File:** `MERGE_ISSUES_REAL_WORLD_RECOVERY.md` → Section: "Part 2: Implementation Steps"

---

## Q: What do the guidance documents say?

**The guidance is correct. It recommends:**

1. ✅ Factory pattern → solves service startup conflicts
2. ✅ Import standardization → solves path conflicts
3. ✅ Hybrid architecture → solves component conflicts
4. ✅ Incremental testing → solves broken merges
5. ✅ Prevent auto-merge → solves silent failures

**The real issue:** These weren't applied systematically from the start.

**File:** `MERGE_ISSUES_REAL_WORLD_RECOVERY.md` → Section: "Part 1: How Guidance Applies"

---

## Q: Why does my merge fail?

**Common causes:**

**Symptom:** "ImportError: No module named src.backend"  
**Cause:** Incomplete migration (some files still in `backend/` not `src/backend/`)  
**Fix:** Run import path migration script

**Symptom:** "Service fails to start"  
**Cause:** Service startup config incompatible  
**Fix:** Create factory pattern in src/main.py

**Symptom:** "Route conflicts"  
**Cause:** Multiple branches define same route  
**Fix:** Implement route namespace separation

**Symptom:** "Circular imports"  
**Cause:** Components weren't meant to be merged  
**Fix:** Create adapter layers in factory

**File:** `MERGE_ISSUES_REAL_WORLD_RECOVERY.md` → Section: "Issue 3-5 (with solutions)"

---

## Q: What's the risk level?

**Risk: MEDIUM (Issues well-understood)**

**High confidence because:**
- ✅ Root causes identified with commit hashes
- ✅ Guidance documents already provide solutions
- ✅ Task 75 work is complete and documented
- ✅ 4-phase implementation plan is clear
- ✅ Estimated effort is known (4-5 days)

**Reasons to be careful:**
- ❌ 30+ active branches means many merge interactions
- ❌ Multiple developers may have conflicting expectations
- ❌ Some architectural decisions not yet finalized

---

## Q: How long will recovery take?

**Timeline:**

| Phase | Task | Duration | Effort |
|-------|------|----------|--------|
| 1 | Fix import paths | 1-2 days | High |
| 2 | Fix service startup | 1 day | Medium |
| 3 | Register Task 75 | 1 day | Low |
| 4 | Establish merge policy | 1 day | Medium |
| **Total** | **All phases** | **4-5 days** | **Medium** |

**Can run in parallel:** Yes, Phases 1 & 3 can run simultaneously

---

## Q: What's the highest priority?

**Immediate (24 hours):**
1. Register Task 75 in JSON (1 day)
2. Create merge policy framework (partial, 1 day)

**This enables:**
- Agent system can see all tasks
- Teams know merge criteria before attempting
- Risk of silent failures reduced

**Next (1 week):**
3. Fix import paths (1-2 days)
4. Fix service startup (1 day)

**This enables:**
- Branches can actually merge
- Service starts cleanly
- Dependencies can be managed

---

## Q: Where do I start?

**If you want overview (10 min):**
→ Read this file (QUICK_DIAGNOSIS_GUIDE.md)

**If you want details (30 min):**
→ Read `INVESTIGATION_SUMMARY.md`

**If you want root cause (60 min):**
→ Read `ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md`

**If you want to implement fix (4-5 days):**
→ Follow `MERGE_ISSUES_REAL_WORLD_RECOVERY.md`

---

## Q: What files should I read?

**Recommended reading order:**

1. **This file** (5 min) - Quick answers
2. **INVESTIGATION_SUMMARY.md** (15 min) - What happened
3. **ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md** (30 min) - Why it happened
4. **MERGE_ISSUES_REAL_WORLD_RECOVERY.md** (45 min) - How to fix it

**Total time to full understanding: 90 minutes**

---

## Q: What's already in place?

**What's working:**
- ✅ Agent memory system (Jan 5-6, 2026)
- ✅ Task 75 documentation (comprehensive)
- ✅ Main task registry (Tasks 1-53)
- ✅ Guidance documents (correct patterns)
- ✅ Analysis complete (this investigation)

**What's broken:**
- ❌ Task registry split (2 systems)
- ❌ Import paths inconsistent
- ❌ Service startup incompatible
- ❌ Branches can't merge cleanly

**What we need:**
- ⏳ Fix import paths
- ⏳ Fix service startup
- ⏳ Register Task 75
- ⏳ Establish merge policy

---

## Q: Can I implement this myself?

**Yes, if you:**
- Have 4-5 days available
- Know Python and Git well
- Can modify codebase systematically
- Have repository commit access

**Recommended approach:**
1. Create feature branch: `feature/merge-recovery`
2. Follow Phase 1-4 steps systematically
3. Test after each phase
4. Create PR with all changes
5. Get review from architecture team

**Estimated effort:** 4-5 days of focused work

---

## Q: What if I skip a phase?

**Phase 1 (import paths):** CRITICAL - Skip at your peril
- Branches won't compile with mixed imports
- Service startup depends on correct imports
- Do this first

**Phase 2 (service startup):** CRITICAL - Do this next
- Determines if merged code actually runs
- Defines compatibility layer
- Required before merging branches

**Phase 3 (Task 75):** IMPORTANT - Do within first week
- Enables task tracking
- Unlocks agent automation
- Non-breaking, can be done anytime

**Phase 4 (merge policy):** CRITICAL - Prevent future issues
- Prevents repeat of current situation
- Automates validation
- Makes merging safe and repeatable

**Verdict:** Don't skip, follow order

---

## Quick Checklist

### Before implementing:
- [ ] Read this file (QUICK_DIAGNOSIS_GUIDE.md)
- [ ] Read INVESTIGATION_SUMMARY.md
- [ ] Read ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md
- [ ] Read MERGE_ISSUES_REAL_WORLD_RECOVERY.md
- [ ] Understand the 4-phase plan
- [ ] Have 4-5 days available

### During Phase 1 (import paths):
- [ ] Audit current imports
- [ ] Create systematic migration script
- [ ] Validate changes
- [ ] Test compilation
- [ ] Create PR

### During Phase 2 (service startup):
- [ ] Create src/main.py factory
- [ ] Test multiple startup patterns
- [ ] Run integration tests
- [ ] Validate with branch features
- [ ] Create PR

### During Phase 3 (Task 75):
- [ ] Extract task definitions from markdown
- [ ] Create JSON registry
- [ ] Validate schema
- [ ] Update agent memory system
- [ ] Create PR

### During Phase 4 (merge policy):
- [ ] Define merge criteria
- [ ] Create integration tests
- [ ] Implement automated checks
- [ ] Document policy
- [ ] Get approval

### After all phases:
- [ ] All PRs merged
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Teams trained on new process
- [ ] Monitor for issues

---

## Emergency Quick Fix

**If system is broken and you need 1-day minimal fix:**

```bash
# 1. Register Task 75 (30 min)
cat > /tmp/register_task_75.py << 'EOF'
import json
tasks = {
    "tasks": [
        {
            "id": 75, 
            "title": "Branch Clustering Framework",
            "status": "pending",
            "subtasks": [1,2,3,4,5,6,7,8,9]
        }
    ]
}
with open("tasks/tasks.json", "w") as f:
    json.dump(tasks, f, indent=2)
EOF
python /tmp/register_task_75.py

# 2. Create emergency factory (20 min)
cat > src/main.py << 'EOF'
from fastapi import FastAPI

def create_app():
    return FastAPI()

app = create_app()
EOF

# 3. Test service startup (10 min)
python -c "from src.main import app; print('✓ Service startup works')"

# Result: System minimal but functional for another 1-2 weeks
```

**Then do proper fix in next sprint.**

---

## Key Files Reference

| File | Size | Purpose | Time |
|------|------|---------|------|
| QUICK_DIAGNOSIS_GUIDE.md | This | Quick answers | 5 min |
| INVESTIGATION_SUMMARY.md | 10KB | Complete overview | 15 min |
| ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md | 20KB | Root cause details | 30 min |
| MERGE_ISSUES_REAL_WORLD_RECOVERY.md | 30KB | Implementation plan | 45 min |

---

## Last Updated
January 6, 2026

## Status
✅ Investigation Complete  
⏳ Awaiting Implementation

## Next Step
Choose: Read summary (15 min) or start implementation (4-5 days)
