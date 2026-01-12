# Legacy Feature Porting Guide

This document provides instructions for porting features from "Legacy" branches (created before the Modern Architecture migration) to the current `scientific` or `main` branches.

## Context: The Modern Architecture
The codebase has undergone a major architectural shift to a Modular, SOLID-compliant structure.
*   **Frontend:** React + Vite + Tailwind (`client/`).
*   **Backend:** Modular Python (`src/`, `modules/`).
*   **Core Services:** `src/core/` (Command Factory, Security, Database).

**WARNING:** Attempting to `git rebase` a legacy branch (2000+ commits behind) onto `scientific` will fail. **Use the Porting Workflow.**

## Recommended Workflow: "Port and Re-implement"

### 1. Archive the Legacy Branch
Do not delete the work! Rename it to preserve the history and code for reference.

```bash
# Rename the local branch
git branch -m feature-old-name archive/legacy-feature-old-name
```

### 2. Create a New Feature Branch
Start fresh from the current `scientific` (development) or `main` (production) branch.

```bash
git checkout scientific
git pull origin scientific
git checkout -b feature-new-name-port
```

### 3. Port Logic to New Architecture

Compare your archived branch against the base to find the logic, then re-implement it using the new patterns.

| Legacy Component | New Architecture Location | Pattern to Use |
| :--- | :--- | :--- |
| **Scripts** (`launch.py` logic) | `src/core/factory.py` | **Command Factory**: Register new commands here. |
| **Backend Logic** (Monolithic) | `modules/<feature>/` | **Modular**: Create `__init__.py`, `service.py`, `models.py`. |
| **Merge/Conflict Logic** | `src/strategy/` or `src/resolution/` | **SOLID**: Implement `ResolutionStrategy` interface. |
| **Database Queries** | `src/core/database.py` | **Repository**: Use the unified DB layer. |
| **Frontend UI** | `client/src/components/<feature>/` | **React**: Use Functional Components + Hooks. |
| **Frontend State** | `client/src/hooks/` | **Hooks**: Use `useQuery` (React Query) or custom hooks. |

### 4. Implementation Checklist

#### A. Command Registration
If your feature adds a CLI command, do **not** add it to `emailintelligence_cli.py` directly.
1.  Define the command class in `src/core/commands/`.
2.  Register it in `src/core/factory.py`.

#### B. Module Structure
Ensure your new module in `modules/<feature>/` follows this structure:
```
modules/my_feature/
├── __init__.py       # Exports
├── service.py        # Business Logic
├── routes.py         # API Endpoints (FastAPI)
├── models.py         # Pydantic Models
└── tests/            # Unit Tests
```

#### C. Frontend Integration
1.  Create components in `client/src/components/`.
2.  If adding a page, register the route in `client/src/App.tsx` (or Router config).
3.  Use `client/src/hooks/use-auth.ts` for authentication context.

### 5. Verify & Merge
1.  **Test:** `pytest modules/my_feature/tests/`
2.  **Lint:** `flake8 modules/my_feature/`
3.  **Commit:** `git commit -m "feat(module): port <feature> to modular architecture"`
4.  **Push:** Create a PR targeting `scientific`.

## Example: Porting `feature-notmuch-tagging`

1.  **Archive:** `git branch -m feature-notmuch-tagging-1 archive/legacy-notmuch-tagging`
2.  **New Branch:** `git checkout -b feat/notmuch-tagging-port`
3.  **Locate Code:** Found tagging logic in `legacy_backend/tagging.py`.
4.  **Implement:**
    *   Created `modules/notmuch/tagging_service.py`.
    *   Used `src.core.database` for DB access.
    *   Registered `tag` command in `src/core/factory.py`.
5.  **Verify:** Ran tests and confirmed CLI command works.