# Architectural Review TODO

## Issue: Branch Structure Inefficiencies Identified

During PR #208 conflict resolution, architectural issues were identified that require future review.

### Problems Found

1. **Duplicate Code Across Branches**
   - main: 183 src files + 9 security classes  
   - scientific: 162 src files + full security module
   - orchestration-tools: 171 scripts (no src/) - separate codebase
   - 000-integrated-specs: 284 src files (combined but has 5+ files with 57+ conflict markers)

2. **Missing Imports** - FIXED 2025-05-03
   - PathValidator, secure_path_join added from main to security.py
   - Basic tests passing

3. **Maintenance Burden**
   - Each branch requires separate PRs to sync
   - Conflict resolution manual each time

### Recommended Options for Future Review

#### Option A: Single Source (Recommended)
Make main the single source of truth:
- Merge scientific code INTO main
- orchestration-tools becomes sync mechanism (subtree)
- Clean separation via uv workspace packages

#### Option B: Git Submodules
- main imports orchestration-tools as submodule
- main imports scientific as submodule
- Clean dependency management

#### Option C: Monorepo with uv workspace
- Single repo with packages: app/, orchestration/, backend/
- Clear module boundaries
- Single PR for all changes

### Current Fixes Applied (This PR)

- ✅ Added PathValidator class to src/core/security.py
- ✅ Added secure_path_join function to src/core/security.py
- ✅ Resolved .github/dependabot.yml conflict markers
- ✅ Resolved .github/workflows/ci.yml conflict markers  
- ✅ Tests passing

### Action Items for Future

- [ ] Review branch dependency graph
- [ ] Choose architectural approach (A, B, or C)
- [ ] Plan migration strategy
- [ ] Create workspace structure if using uv
- [ ] Document new branch workflow

---
*Created during PR #208 conflict resolution on 2025-05-03*
