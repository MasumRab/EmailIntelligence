# Agent Files & .gitignore Inconsistency Analysis

## Executive Summary
There is significant inconsistency in how agent instruction files (AGENTS.md, CLAUDE.md, QWEN.md, etc.) and other important configuration files are tracked and propagated across branches. The `.gitignore` rules are identical across branches, but the actual tracked files differ dramatically.

---

## Current State: Agent Files by Branch

### ✅ **Scientific Branch** (Most Complete)
```
AGENT_GUIDANCE_PLAN.md
AGENT.md
AGENTS.md (scientific-specific variant)
CLAUDE.md
CONTRIBUTING.md
GEMINI.md
LLXPRT.md
QWEN.md
```

### ⚠️ **Main Branch** (Partial)
```
AGENT.md
AGENTS.md (taskmaster-focused variant)
CONTRIBUTING.md
GEMINI.md
LLXPRT.md
QWEN.md
```
**Missing:** CLAUDE.md, AGENT_GUIDANCE_PLAN.md

### ⚠️ **Orchestration-Tools Branch** (Minimal)
```
AGENTS.md (generic dispatcher variant)
CLAUDE.md
LLXPRT.md
QWEN.md
```
**Missing:** AGENT.md, CONTRIBUTING.md, AGENT_GUIDANCE_PLAN.md, GEMINI.md

### ❌ **Taskmaster Branch** (Empty)
```
(No agent files)
```

---

## .gitignore Status
**Status:** ✅ Identical across all branches
- All 5 branches have identical `.gitignore` content
- Uses wildcard rule `.*` (line 68) to ignore all hidden files
- Exception: `!.git/hooks/` is preserved
- **Important Note:** `.gitignore` does NOT ignore `AGENTS.md` or other agent files by name

---

## Specific Inconsistencies

### 1. **AGENTS.md Content Divergence**
Three different variants exist:

| Branch | Content Type | Purpose |
|--------|--------------|---------|
| **scientific** | Full Amp conventions | Development standards, architecture, code style |
| **main** | TaskMaster guide + branch dispatcher | Task management + branch switching instructions |
| **orchestration-tools** | Generic dispatcher | Directs users to other branch docs |

**Root Cause:** Each branch has been independently modified without synchronization protocol.

### 2. **Agent-Specific Files Distribution**
| File | Main | Orch-Tools | Scientific | Taskmaster |
|------|------|-----------|-----------|-----------|
| AGENT.md | ✅ | ❌ | ✅ | ❌ |
| AGENTS.md | ✅ | ✅ | ✅ | ❌ |
| CLAUDE.md | ❌ | ✅ | ✅ | ❌ |
| GEMINI.md | ✅ | ❌ | ✅ | ❌ |
| QWEN.md | ✅ | ✅ | ✅ | ❌ |
| LLXPRT.md | ✅ | ✅ | ✅ | ❌ |
| AGENT_GUIDANCE_PLAN.md | ❌ | ❌ | ✅ | ❌ |
| CONTRIBUTING.md | ✅ | ❌ | ✅ | ❌ |

**Pattern:** Scientific has everything, orchestration-tools is stripped, main is partial, taskmaster has nothing.

### 3. **No Controlled Propagation**
- AGENTS.md changes on scientific aren't automatically synced to main/orchestration-tools
- Post-push hook for orchestration files doesn't monitor agent instruction files
- No pre-commit hook validates agent file consistency

### 4. **Wildcard .gitignore Rule (Line 68)**
```bash
.*
!docs/.gitkeep
!.semgrep/
!.gitignore
!.git/hooks/
```

**Issue:** The wildcard `.*` catches hidden files like `.claude/`, `.qwen/`, `.cursor/` which may contain agent-specific configurations that should be tracked or ignored consistently.

---

## Problems This Creates

### 🔴 **For Developers**
- Unclear which agent instructions apply to current branch
- Different guidance depending on which branch you're on
- No single source of truth for conventions

### 🔴 **For Orchestration**
- No automated sync of AGENTS.md across branches
- Orchestration-tools changes to AGENTS.md aren't propagated
- Agent changes don't trigger PR creation like other orchestration files

### 🔴 **For New Contributors**
- Scientific has best practices; main/orch-tools have dispatcher instructions
- Taskmaster has no agent files at all (empty branch)
- Risk of following outdated or inconsistent patterns

### 🔴 **For Tool Integration**
- Each AI tool (Claude, Gemini, Qwen, Llxprt) has branch-specific availability
- Tool configs may be ignored by git but not in `.gitignore` explicitly
- Hidden directories (`.claude/`, `.qwen/`, etc.) are caught by wildcard but not explicitly managed

---

## What Needs To Be Done

### Phase 1: Establish Single Source of Truth
**Action:** Designate orchestration-tools as canonical source for all agent files
1. Audit orchestration-tools branch to be complete reference
2. Add missing files: AGENT.md, CONTRIBUTING.md, GEMINI.md, AGENT_GUIDANCE_PLAN.md
3. Ensure AGENTS.md contains all conventions (not branch dispatcher)

### Phase 2: Add to Orchestration Sync
**Action:** Treat agent files like orchestration-managed files
1. Add to `ORCHESTRATION_MANAGED_FILES` array in post-push hook:
   ```bash
   ORCHESTRATION_MANAGED_FILES=(
       # ... existing files ...
       "AGENTS.md"
       "AGENT.md"
       "CONTRIBUTING.md"
       "CLAUDE.md"
       "GEMINI.md"
       "QWEN.md"
       "LLXPRT.md"
       "AGENT_GUIDANCE_PLAN.md"
   )
   ```
2. Trigger draft PR creation when these files change on non-orchestration-tools branches
3. Auto-sync from orchestration-tools to other branches post-merge

### Phase 3: Explicit .gitignore Management
**Action:** Make hidden directory handling explicit
1. Replace wildcard `.*` with specific entries:
   ```bash
   # Hidden directories to ignore
   .aider/
   .claude/
   .qwen/
   .cursor/
   .continue/
   .vscode/
   # ... etc
   
   # But preserve:
   !.git/
   !.github/
   !.gitignore
   !.gitattributes
   !.gitkeep
   ```
2. This prevents accidental commits and makes rules clear

### Phase 4: Add Validation Hook
**Action:** Create pre-commit hook to validate agent file consistency
1. Check that orchestration-tools version exists if modified elsewhere
2. Warn if modifying agent files outside orchestration-tools branch
3. Suggest creating PR to orchestration-tools instead

### Phase 5: Distribution Policy
**Action:** Define how agent files flow to other branches
```yaml
Orchestration-Tools (Canonical)
  ↓ (post-merge sync)
Main & Scientific (Synchronized copies)
  ↓ (pull/merge from main)
Feature Branches (Inherit from parent)

Taskmaster (Special case - May need isolated set)
```

---

## Implementation Priority

| Priority | Item | Effort | Impact |
|----------|------|--------|--------|
| 🔴 P0 | Add AGENTS.md to orchestration sync | Low | High |
| 🔴 P0 | Add missing agent files to orchestration-tools | Medium | High |
| 🟡 P1 | Update post-push hook to track agent files | Medium | High |
| 🟡 P1 | Explicit .gitignore rules for hidden dirs | Low | Medium |
| 🟡 P1 | Create validation hook | Medium | Medium |
| 🟢 P2 | Define distribution policy document | Low | Low |

---

## Recommended Next Steps

1. **Immediate:** Review scientific branch AGENTS.md as source of truth
2. **This Week:** 
   - Audit which agent-specific files are actually needed
   - Consolidate orchestration-tools with complete agent file set
   - Update AGENTS.md section to add agent file tracking
3. **Next Week:**
   - Implement hook changes
   - Test sync across branches
   - Document in AGENTS.md protocol
