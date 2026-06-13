# Task Analysis & Gotchas

**Created:** 2026-06-11
**Author:** Letta Code agent (agent-f45e48fa)
**Purpose:** Single reference for all known issues, gotchas, and analysis findings about the 25-task branch alignment system. **Read this before working on any task.**

---

## Critical Finding: Subtask-Intent Inversion

**Subtasks are ground truth. Parent tasks should be fixed to match subtasks, not the reverse.**

Across all 25 tasks, subtasks are consistently more grounded, concrete, and faithful to the system's actual purpose than the parent tasks that contain them. The parents describe what someone wished the system would be; the subtasks describe what the system actually is.

| Dimension | Parent Tasks | Subtasks |
|-----------|-------------|----------|
| Language | Architectural, aspirational ("comprehensive framework") | Implementation-oriented, concrete |
| Scope | Inflated | Bounded (specific operations) |
| Alignment with purpose | Often mislabeled or misaligned | Often reveal the real architecture |
| Dependency accuracy | Cross-references wrong (off-by-one) | Internal logic correct |
| Origin | Written for this system (template-applied) | Often imported from prior systems (closer to metal) |
| Honesty | Describe what they want to be | Describe what they actually are |

### Exceptions (3 tasks where parent is more accurate than subtasks)

1. **Task 005**: Subtasks are generic boilerplate; parent has the real intent (AST import validation + merge artifact detection). Here, fix subtasks.
2. **Task 015**: Subtasks are from a different task entirely (Task 27 orchestration). Here, decide whether 015 should be validation (per parent title) or orchestration (per subtask content), then align both.
3. **Numbering issues** (008, 009): Fix the parent's cross-references and the subtask numbering prefixes. Content is correct; labels are wrong.

---

## Evidence by Pattern

### Pattern 1: Subtasks Know What the System Is; Parents Know What They Want It to Be

**Task 002** — Parent: "Advanced intelligent branch clustering" (212–288 hours, 9/10 complexity). Subtasks: extract metrics, compute distances, cluster, assign targets, report. The subtasks describe a ~40-hour project. The parent inflates it into a monster.

**Task 005** — Inverse: Parent has a specific, actionable intent (AST import validation + merge artifact detection), but subtasks are generic boilerplate (research, implement, integrate, document). Here the parent knows what it wants; the subtasks don't know what they are.

### Pattern 2: Subtasks Reveal the Real Architecture; Parents Obscure It

**Task 015** — Parent says "Validation and Verification." Subtasks describe:
- 015.1: Design orchestration workflow architecture
- 015.2: Integrate feature branch identification
- 015.3: Develop interactive branch selection UI
- 015.4: Implement branch processing queue
- 015.6: Implement sequential execution control flow
- 015.7: Integrate backup procedure
- 015.8: Integrate branch alignment logic
- 015.12: Pause/resume/cancel mechanisms
- 015.13: State persistence & recovery

These subtasks describe **the orchestration system** — the same thing Task 012 describes. The subtasks are telling you: the real work is building a sequential orchestrator. The parent title "Validation and Verification" is a mask. The subtasks know what the system is.

### Pattern 3: Subtasks Expose the Real Dependency Graph; Parents Lie

**Task 009** — Parent says it coordinates with Tasks 012/013/014/015. Subtasks say:
- 009.2: "Coordinate safety checks with Task 012" → but backup is Task 013
- 009.7: "Coordinate with Task 013" for conflicts → but conflicts are Task 014
- 009.8: "Coordinate with Task 014" for validation → but validation is Task 015
- 009.9: "Coordinate with Task 015" for rollback → but rollback is Task 016

The subtask descriptions are internally consistent with each other — they form a coherent pipeline (safety → backup → rebase → conflict → validation → rollback). The parent's cross-references are off by one. The subtasks tell the truth about the pipeline; the parent's task IDs are a clerical error layered on top.

### Pattern 4: Subtasks Reveal What Tasks Should Be Collapsed; Parents Pretend Independence

**Task 007** — Parent: "Feature Branch Identification and Categorization Tool." Subtasks:
- 007.1: Destructive merge artifact detection
- 007.2: Content mismatch detection in similarly named branches
- 007.3: Backend-to-src migration status analysis

The subtasks describe error detection and migration analysis, not branch identification. They belong to Task 005 (error detection) or a migration task. The subtasks tell you: the real concern is detecting problems in branches, not categorizing them.

**Task 008** — Parent: "Comprehensive Merge Validation Framework." Subtasks numbered "9.1" through "9.017" — clearly from a different task (Task 9 in a prior numbering system). The subtasks describe coherent CI/CD pipeline setup. They're faithful to their original intent but unfaithful to their current parent.

### Pattern 5: Tail Tasks (019–025) — Parents Are Frameworks, Subtasks Would Be Trivial

All follow: "Implement comprehensive [X] framework" (20–48 hours each). Subtasks are generic (design, implement, test, document). If read individually, they reduce to: "write a deploy script," "write a README," "add a health check" — 2–3 hours total, not 200+. The subtasks' triviality reveals the parents' over-specification.

---

## Critical Data Corruption Issues

### Issue 1: Task 015 Content Contamination

- **Parent title:** "Validation and Verification"
- **Subtasks describe:** Orchestration workflow (branch selection UI, queue management, sequential execution)
- **Subtasks reference phantom "27.x" dependencies** that don't exist in the 25-task system
- **Subtask 015.013** uses zero-padded numbering
- **Diagnosis:** Subtasks were pasted from a prior Task 27 orchestration spec. The parent title was never updated to match.
- **Fix:** Rewrite parent to match what subtasks actually describe, OR rewrite subtasks to match what the parent says. Given the inversion principle, the subtasks are closer to truth — but they also need cleanup (remove 27.x references, fix numbering).

### Issue 2: Task 009 Cross-Reference Off-by-One

- **Parent references** Tasks 012/013/014/015 for backup/conflict/validation/rollback
- **Actual mapping:** 013=backup, 014=conflict, 015=validation, 016=rollback
- **Diagnosis:** Parent was written before Tasks 013–016 were renumbered. Subtask descriptions are internally consistent.
- **Fix:** Update parent's cross-references to match actual task IDs. Subtask descriptions are correct.

### Issue 3: Task 008 Subtask Numbering Catastrophe

- **All subtasks use "9.x" prefix** instead of "8.x"
- **Zero-padded variants** (9.013, 9.003) mixed with non-padded (9.1, 9.15)
- **Diagnosis:** Subtasks imported from a prior Task 9 without renumbering.
- **Fix:** Renumber all subtasks to 8.x. Content is coherent (CI/CD validation) — just wrong numbering.

### Issue 4: Validation Quad-Redundancy (Tasks 003, 008, 011, 017)

- **Task 003:** Pre-merge file validation (basic)
- **Task 008:** CI/CD merge validation framework (comprehensive)
- **Task 011:** Validation integration into alignment workflow (workflow-level)
- **Task 017:** Validation integration framework (plugin-level)
- **Diagnosis:** Subtasks reveal this is a progressive layering (basic → comprehensive → integrated → pluggable), not redundancy. But boundaries aren't clearly defined.
- **Fix:** Define clear boundaries between layers. Document the progression.

---

## Task-by-Task Intent Alignment Summary

| Task | Parent Intent | Subtask Intent | Aligned? | Action |
|------|--------------|----------------|----------|--------|
| 001 | Framework definition | Branch identification + target assignment | Partial | Subtasks more concrete; parent too abstract |
| 002 | Intelligent clustering | Extract metrics, cluster, assign | No | Parent inflates; subtasks are ~40hr not 212hr |
| 003 | Pre-merge validation | Define files, write script, test, CI, docs | Yes | Well-aligned |
| 004 | Branch alignment framework | Git hooks, wrappers, orchestration | Yes | Well-aligned |
| 005 | Error detection (AST + artifacts) | Generic: research, implement, integrate, doc | No | Parent has real intent; subtasks are boilerplate |
| 006 | Backup and restore | Feature backup, primary backup, integration | Yes | Well-aligned |
| 007 | Branch identification | Error detection + migration analysis | No | Subtasks belong to different task |
| 008 | CI/CD validation framework | CI/CD pipeline setup (numbered 9.x) | Partial | Content aligned; numbering wrong |
| 009 | Core alignment orchestration | Single-branch pipeline coordination | Yes | Subtasks correct; parent cross-refs off-by-one |
| 010 | Complex branch strategies | 27 subtasks covering complexity, rebase, conflict | Partial | Subtasks over-specified; many are v2 future work |
| 011 | Validation integration | Embed validation into alignment workflow | Yes | Well-aligned |
| 012 | Sequential orchestration | Multi-branch queue orchestration | Yes | Well-aligned |
| 013 | Branch backup and safety | Backup mechanisms | Yes | Well-aligned |
| 014 | Conflict detection/resolution | Conflict framework | Yes | Well-aligned |
| 015 | Validation and verification | ORCHESTRATION WORKFLOW (not validation) | No | Subtasks describe different task entirely |
| 016 | Rollback and recovery | Rollback mechanisms | Yes | Well-aligned |
| 017 | Validation integration framework | Integration layer connecting validation | Partial | Overlaps with 011; subtasks are generic |
| 018 | E2E testing and reporting | Test framework + scenarios | Yes | Well-aligned |
| 019–025 | Infrastructure frameworks | Generic design/implement/test/doc | No | Parents over-specified; subtasks trivial. **Exception: 022 has a real migration step (012.15) that is a core dependency, not a tail framework** |

---

## Additional Gotchas

### Task Numbering
- Old numbering (task-001 to task-020) is DEPRECATED. Current format: `task_XXX.md`
- See `.taskmaster/OLD_TASK_NUMBERING_DEPRECATED.md`
- Task 008 subtasks use "9.x" prefix (from prior system, never renumbered)
- Task 015 subtasks reference phantom "27.x" dependencies (from prior system)

### Source of Truth
- **Markdown files (`task_001-025.md`) are the SOLE source of truth** — tasks.json was deleted 2026-06-08 (commit `c7bc3895`)
- Manage `.taskmaster/config.json` via `task-master models`, not by hand-editing
- **CRITICAL FIDELITY RULE:** Always edit Markdown files first, then run `python taskmaster_cli.py parse-prd --input tasks/` to sync. DO NOT manually edit `tasks.json`.

### Project Identity
- This is a **branch alignment tooling project**
- EmailIntelligence MVP tasks are in `tasks/mvp/` only — **DO NOT MIX** with alignment tasks
- See `.taskmaster/PROJECT_IDENTITY.md`

### Taskmaster Branch
- The `taskmaster` branch is an **orphan** — it shares zero Git history with main/scientific/orchestration-tools
- Cannot `git merge` or `git rebase` against main without `--allow-unrelated-histories`
- Must use cherry-pick or file-level copy to integrate content
- The branch went through contamination → cleanup → restore cycles (9 self-merge commits)

### Validation Layering (Not Redundancy)
Tasks 003, 008, 011, 017 form a progressive layering, not duplication:
- **003** → Basic file-level validation
- **008** → Comprehensive CI/CD validation
- **011** → Integration into alignment workflow
- **017** → Plugin-level extensibility

### Effort Estimates
- Tasks 002, 019–025 have massively inflated effort estimates (200+ hours). Based on subtask analysis, actual effort is 10–20% of stated estimates.
- Task 002: Stated 212–288 hours. Actual ~40 hours based on subtask scope.
- Tasks 019–025: Stated 20–48 hours each. Actual 2–3 hours each based on subtask triviality.

### AI-Assisted Merge Conflict Resolution
- **NEVER trust AI-resolved merge conflicts** without a line-count and function-signature audit
- Observed on scientific branch: 209 conflict markers resolved, but 8 functions lost in `src/main.py`, 3 functions lost in `src/core/auth.py`, 302 lines lost in `src/core/workflow_engine.py`
- Root cause: Agents rewrite entire files from scratch instead of preserving both sides content
- Prevention: Always compare line counts and function signatures before/after. Use `git show HEAD:<file>` to verify no content was lost

### Wrong-Base PR Pattern
- ~13 open PRs target `main` but their branches diverged from `scientific` or from the repo root
- When a PR diff is 10x+ larger than expected, check `git merge-base` to verify branch origin
- Fix: Retarget PRs to correct base branch, or cherry-pick actual fix commits to a fresh branch

### Jules WIP Branch Root Cause
- Multiple open PRs (#208, #325, #205, #688, #689, #640, #638, #493) show massive diffs (4K–620K lines)
- Root cause: Single Jules WIP session branched from repo's INITIAL COMMIT instead of a real branch
- Resolution: Cherry-pick actual fix commits onto proper branches, then close originals

### Gitignore Exception Ordering
- `!` negation patterns placed BEFORE the Ruler section get overridden by the Ruler section's ignore patterns
- In `.gitignore`, the **last matching pattern wins**
- Fix: Place ALL `!` exceptions AFTER the Ruler-generated section (after `# END Ruler Generated Files`)
- Tracked files ignore gitignore rules entirely — use `git rm --cached <file>` first

### Branch Isolation Policy
- **NO MERGES between main, scientific, orchestration-tools**
- Distribution scripts: `scripts/distribute-orchestration-files.sh`
- Branch-specific directories: `docs/handoff/` exists ONLY on `orchestration-tools` branch

---

## Remediation Priority

When fixing task files, follow this order:

1. **Fix Task 008 numbering** — Renumber all subtasks from 9.x to 8.x (mechanical, low risk)
2. **Fix Task 009 cross-references** — Update parent's 012/013/014/015 to 013/014/015/016 (mechanical, low risk)
3. **Decide Task 015 fate** — Is it validation (per parent) or orchestration (per subtasks)? Then align both directions
4. **Reassign Task 007 subtasks** — Move 007.1/007.2/007.3 to Task 005 or a migration task
5. **Deflate Task 002** — Reduce effort estimate from 212hr to ~40hr based on subtask scope
6. **Deflate Tasks 019–025** — Reduce effort estimates from 20–48hr each to 2–3hr each
7. **Define validation boundaries** — Document the 003→008→011→017 progression clearly
8. **Clean Task 005 subtasks** — Replace generic boilerplate with concrete steps matching parent intent
