# Phase 2: Content Fixes

**Purpose:** Fix incorrect content in tool rules files.
**Steps:** 7
**Dependencies:** Phase 1 complete

---

## Step 2.1 — Fix Windsurf dev_workflow.md bug (line 36)

**File:** `.windsurf/rules/dev_workflow.md`
**Issue:** Duplicate `windsurf,windsurf` on line 36

**Find:**
```
Use `task-master init --rules windsurf,windsurf` to specify
```

**Replace with:**
```
Use `task-master init --rules cline,windsurf` to specify
```

---

## Step 2.2 — Fix Windsurf dev_workflow.md bug (line 303)

**File:** Same file
**Issue:** Same bug on line 303

**Find:**
```
Use `task-master init --rules windsurf,windsurf` to specify
```

**Replace with:**
```
Use `task-master init --rules cline,windsurf` to specify
```

**Verify:**
```bash
grep -c "windsurf,windsurf" .windsurf/rules/dev_workflow.md
```
**Expected:** `0`

---

## Step 2.3-2.4 — Fix Prisma references in *_rules.md files

**Files:** 5 files
| File | Actions |
|------|---------|
| `.clinerules/cline_rules.md` | 2 edits |
| `.windsurf/rules/windsurf_rules.md` | 2 edits |
| `.roo/rules/roo_rules.md` | 2 edits |
| `.trae/rules/trae_rules.md` | 2 edits |
| `.kiro/steering/kiro_rules.md` | 2 edits |

**Edit 1 — Replace prisma.md reference:**

Find: `Example: [prisma.md](PATH/prisma.md) for rule references`
Replace: `Example: [taskmaster.md](PATH/taskmaster.md) for rule references`

**Edit 2 — Replace schema.prisma reference:**

Find: `Example: [schema.prisma](mdc:prisma/schema.prisma) for code references`
Replace: `Example: [launch.py](mdc:launch.py) for code references`

---

## Step 2.5 — Fix Prisma references in self_improve.md files

**Files:** 5 files
| File | Actions |
|------|---------|
| `.clinerules/self_improve.md` | 2 edits |
| `.windsurf/rules/self_improve.md` | 2 edits |
| `.roo/rules/self_improve.md` | 2 edits |
| `.trae/rules/self_improve.md` | 2 edits |
| `.kiro/steering/self_improve.md` | 2 edits |

**Edit 1 — Replace Prisma code block:**

Find:
```
  const data = await prisma.user.findMany({
    select: { id: true, email: true },
    where: { status: 'ACTIVE' }
  });
```

Replace:
```
  results = db.session.query(User).filter(
      User.status == 'active'
  ).all()
```

**Edit 2 — Replace prisma.md reference:**

Find: `// Consider adding to [prisma.md](PATH/prisma.md):`
Replace: `# Consider adding to [dev_workflow.md](PATH/dev_workflow.md):`

---

## Step 2.6 — Verify Prisma references removed

```bash
grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l
```
**Expected:** `0`

---

## Step 2.7 — Update rulesync.jsonc targets

**File:** `rulesync.jsonc`
**Action:** OVERWRITE with updated target list

```json
{
  "targets": [
    "claudecode",
    "cursor",
    "cline",
    "roo",
    "kiro",
    "windsurf",
    "qwencode",
    "opencode",
    "geminicli",
    "agentsmd",
    "codexcli"
  ]
}
```

---

## Gate Check

```bash
echo "=== PHASE 2 GATE CHECK ==="
echo -n "windsurf,windsurf occurrences: "
grep -r "windsurf,windsurf" .windsurf/ 2>/dev/null | wc -l
echo -n "prisma references in tool rules: "
grep -rl "prisma" .clinerules/ .windsurf/rules/ .roo/rules/ .trae/rules/ .kiro/steering/ 2>/dev/null | wc -l
echo -n "rulesync.jsonc valid: "
python3 -c "import json; json.load(open('rulesync.jsonc')); print('VALID')" 2>/dev/null || echo "INVALID"
```

---

## Step 2.7a — Create rulesync.jsonc (if missing)

**File:** `rulesync.jsonc`

**Action:** CREATE if file doesn't exist.

```jsonc
{
  "targets": [
    "claudecode",
    "cursor",
    "cline",
    "roo",
    "kiro",
    "windsurf",
    "qwencode",
    "opencode",
    "geminicli",
    "agentsmd",
    "codexcli"
  ],
  "source": ".ruler/AGENTS.md",
  "drift_detection": {
    "enabled": true,
    "strict": true
  }
}
```

**Verify:**
```bash
test -f rulesync.jsonc && echo "CREATED" || echo "MISSING"
python3 -c "import json; d=json.load(open('rulesync.jsonc')); print(f'{len(d[\"targets\"])} targets')"
```

**Expected:** 11 targets configured.

**NOTE:** This step was added to address gap where Step 2.7 said "Update" but file may not exist.
