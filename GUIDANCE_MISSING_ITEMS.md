# Guidance Directory Gap Analysis

## Purpose
Document what information exists in `/guidance/` about merging scientific branches that is NOT currently incorporated into the task files.

---

## What Exists in `/guidance/`

### Core Lessons (from actual branch merge experience)

| Topic | Key Points |
|-------|------------|
| **Factory Pattern** | `create_app()` function for service compatibility between branches |
| **Import Path Standardization** | `backend.*` → `src.backend.*` pattern |
| **Context Control Integration** | Remote patterns with local functionality |
| **Hybrid Architecture** | Adapter layers bridging different approaches |
| **Direct Rebase Fails** | Don't rebase branches with different architectures |
| **Import-time vs Runtime** | Use lazy initialization to avoid import failures |
| **File Location Differences** | `backend/` vs `src/backend/` causes import errors |
| **Service Startup Dependencies** | Verify configs work with merged code |

### Checklists in Guidance

**Pre-Merge Assessment (8 items):**
- Analyze architectural differences
- Identify core functionality to preserve
- Map import path dependencies
- Plan compatibility layer
- Create backup
- Check for incomplete migrations
- Identify half-implemented changes
- Verify migration status

**Validation (5 checks):**
- Factory pattern works
- All features preserved
- Context control integrated
- Service startup compatible
- Import paths standardized

**Red Flags (10 items):**
- Service configs pointing to non-existent files
- Expected factory functions missing
- Missing architectural components
- Import-time initialization
- Core entry point conflicts
- Mixed import paths
- Partially migrated components
- Components that break when combined

---

## What's Missing from Task Files

### task-002.md (Merge Validation Framework)
| In Guidance | In task-002.md |
|-------------|----------------|
| Factory pattern validation | ❌ NOT MENTIONED |
| Service startup compatibility | ❌ NOT MENTIONED |
| Import path validation | ❌ NOT MENTIONED |
| 5-point validation checklist | ❌ NOT DOCUMENTED |

### task-004.md (Core Alignment Framework)
| In Guidance | In task-004.md |
|-------------|----------------|
| Hybrid architecture approach | ⚠️ VAGUE MENTION |
| Adapter layers for bridging | ❌ NOT EXPLAINED |
| Pre-merge assessment | ❌ NOT INCLUDED |
| Architectural difference analysis | ❌ NOT INCLUDED |

### task-005.md (Error Detection)
| In Guidance | In task-005.md |
|-------------|----------------|
| Import path conflict detection | ❌ NOT MENTIONED |
| File location mismatch detection | ❌ NOT MENTIONED |
| Service startup validation | ❌ NOT MENTIONED |
| Runtime vs import-time issues | ❌ NOT MENTIONED |

### task-006.md (Backup/Restore)
| In Guidance | In task-006.md |
|-------------|----------------|
| 5-step rollback procedure | ❌ NOT DOCUMENTED |
| Immediate revert actions | ❌ NOT INCLUDED |
| Recovery safeguards | ❌ NOT INCLUDED |

### task-016.md (Scientific Branch Recovery)
| In Guidance | In task-016.md |
|-------------|----------------|
| Factory pattern for compatibility | ❌ NOT MENTIONED |
| Import path standardization | ❌ NOT MENTIONED |
| Context control integration | ❌ NOT MENTIONED |
| Hybrid architecture approach | ❌ NOT EXPLAINED |
| Pre-merge assessment checklist | ❌ NOT INCLUDED |

### task-018.md (Pre/Post Merge Validation)
| In Guidance | In task-018.md |
|-------------|----------------|
| Service startup validation | ⚠️ VAGUE |
| Import path validation | ❌ NOT MENTIONED |
| Factory pattern validation | ❌ NOT MENTIONED |
| Validation checklist | ❌ NOT DOCUMENTED |

---

## Summary of Gaps

| Task File | Critical Gaps |
|-----------|---------------|
| task-002.md | Factory pattern, service startup, import paths, validation checklist |
| task-004.md | Hybrid architecture, adapter layers, pre-merge assessment |
| task-005.md | Import conflicts, file location mismatches, service startup issues |
| task-006.md | Rollback procedure, recovery steps |
| task-016.md | All guidance topics (factory, imports, context, hybrid, checklists) |
| task-018.md | Service startup, import paths, factory pattern validation |

---

## Key Information to Transfer

### 1. Factory Pattern Concept
- `src/main.py` with `create_app()` exists in guidance
- Task files don't reference this pattern for branch compatibility

### 2. Import Path Patterns
- `backend.*` → `src.backend.*` standardization
- Detection commands (`git grep`)
- Task files don't show these patterns

### 3. Hybrid Architecture Approach
- Adapter layers bridging different architectures
- Don't use direct rebase for different architectures
- Task files don't explain this approach

### 4. Validation Checklist
- 5 specific checks (factory, features, context, startup, imports)
- Task files don't have this checklist

### 5. Red Flags
- 10 specific warning signs to watch for
- Task files don't document these

### 6. Rollback Procedure
- 5-step recovery process
- Task files don't include this

---

## Source Files Reference

**Guidance Directory:** `/home/masum/github/PR/.taskmaster/guidance/`
- `MERGE_GUIDANCE_DOCUMENTATION.md` - Main guidance
- `ARCHITECTURE_ALIGNMENT_IMPLEMENTATION_GUIDE.md` - Implementation guide
- `IMPLEMENTATION_SUMMARY.md` - Lessons learned
- `src/main.py` - Factory pattern code
- `validate_architecture_alignment.py` - Validation script

**Task Files:** `/home/masum/github/PR/.taskmaster/new_task_plan/task_files/`
