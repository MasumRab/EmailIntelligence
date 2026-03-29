# CLI Workflow Map

This document provides a static overview of the decision trees implemented in the `dev.py` guided workflows.

## 1. `guide-dev` (Development Guidance)

```mermaid
graph TD
    A[Start] --> B{Intent?}
    B -- "App Code" --> C[Advice: Proceed on feature branch]
    B -- "Shared Config" --> D{Branch?}
    D -- "orchestration-tools" --> E[Advice: Safe to edit]
    D -- "Other" --> F[Warning: Switch to orchestration-tools]
    C --> G[End]
    E --> G
    F --> G
```

## 2. `guide-pr` (PR Resolution)

```mermaid
graph TD
    A[Start] --> B{PR Type?}
    B -- "Orchestration" --> C[Advice: Use manage_orchestration_changes.sh]
    B -- "Major Feature" --> D{eai available?}
    D -- "Yes" --> E[Advice: eai setup-resolution]
    D -- "No" --> F[Advice: Standard git merge + Validation plan]
    C --> G[End]
    E --> G
    F --> G
```

## 3. Analysis & Resolution

- **`analyze`**: Ported from `scientific` `analyze-constitutional`. Scans for architectural violations.
- **`resolve`**: Ported from `scientific` `auto-resolve`. AI-driven conflict resolution.
- **`strategy`**: Ported from `scientific` `develop-spec-kit-strategy`. Generates merge plans.