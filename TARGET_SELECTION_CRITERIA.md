# Target Selection Criteria

This checklist defines the decision criteria for aligning feature branches with their optimal integration targets (`main`, `scientific`, or `orchestration-tools`).

## Integration Targets Overview

*   **`main`**: The primary operational branch. Targets here should involve core system logic, user interfaces, or standard operational updates.
*   **`scientific`**: The branch focused on research, modeling, deep analysis, and experimental features.
*   **`orchestration-tools`**: The branch focused on infrastructure, deployment, CI/CD, and tooling that manages system components.

## Selection Checklist

Evaluate each feature branch against the following criteria to determine the appropriate target:

### 1. Codebase Similarity & Scope
- [ ] Does the branch primarily modify core application code, UI components, or standard APIs? -> **Target: `main`**
- [ ] Does the branch primarily introduce new analytical models, machine learning algorithms, or data processing pipelines? -> **Target: `scientific`**
- [ ] Does the branch primarily modify deployment scripts, CI/CD workflows, Dockerfiles, or infrastructure automation? -> **Target: `orchestration-tools`**

### 2. Architectural Preservation
- [ ] Does this branch depend heavily on the existing application architecture found in `main`? -> **Target: `main`**
- [ ] Does this branch require the specialized scientific computing libraries or environment configurations present in `scientific`? -> **Target: `scientific`**
- [ ] Does this branch interact primarily with system-level orchestration or deployment mechanisms? -> **Target: `orchestration-tools`**

### 3. Git History & Merging Strategy
- [ ] Will merging this branch into `main` create significant conflicts or require complex rebasing due to deep scientific changes? (If yes, consider `scientific`)
- [ ] Is this branch a fast-forward or clean merge related to operational tooling? (If yes, consider `orchestration-tools`)
- [ ] Does this branch share significant recent history with a specific target branch?

### 4. Strategic Priorities
- [ ] Is the primary goal of this branch immediate operational stability or feature release for end-users? -> **Target: `main`**
- [ ] Is the primary goal long-term research, performance benchmarking of models, or advanced analytics? -> **Target: `scientific`**
- [ ] Is the primary goal improving developer experience, release reliability, or system scalability? -> **Target: `orchestration-tools`**
