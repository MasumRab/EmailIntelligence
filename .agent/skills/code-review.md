# Internal-First Code Review Skill

This skill instructs the AI to prioritize the project's internal diagnostic suite (`dev.py`) for all code review tasks.

## Core Pillars of Review

### 1. Topological Awareness (`branch-cluster`)
-   **Goal**: Determine if the change introduces a new "island" or if it correctly aligns with existing functional domains.
-   **Check**: Does the branch sit correctly in the `consolidate/` namespace?

### 2. Forensic DNA Parity (`logic-compare`)
-   **Goal**: Prevent accidental logic loss during porting.
-   **Check**: If functions were moved from `scripts/` to `src/cli/`, their AST-normalized bodies must match >95%.

### 3. Structural Risk Audit (`code-audit`)
-   **Goal**: Find deeper maintainability and security issues using AST visitors.
-   **Check**: 
    -   Are there bare `except:` clauses?
    -   Is `open()` gated by the `SecurityValidator`?
    -   Are there high-complexity functions?

### 4. Architectural Layering (`import-audit`)
-   **Goal**: Enforce SOLID independence.
-   **Check**: CLI components should NOT import from `src.backend` or `src.core` directly; they must use service bridges.

## Automated Workflow
When a review is requested:
1.  **Execute** the `code-review` recipe.
2.  **Synthesize** the output of the internal tools first.
3.  **Cross-reference** with CodeRabbit results if available.
4.  **Verdict**: Issue a "Technical Integrity" score based on internal diagnostic passes.
