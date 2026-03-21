# Unified Forensic Code Review Skill

This skill provides a bridge between high-level AI reasoning and the rigorous internal CLI diagnostics of the EmailIntelligence project.

## 1. Parallel Verification (Ancestral DNA)
When performing a review, analyze the following pillars in parallel:
-   **Quality & Style**: Leverages Ruff and isort (Standardized).
-   **Functional Parity**: Leverages `logic-compare` (Forensic).
-   **Architectural Safety**: Leverages `import-audit` and `code-audit` (AST-based).
-   **Contextual Topology**: Leverages `branch-cluster` (Relationship-based).

## 2. Decision Matrix
Issue a verdict based on tool outputs:
-   **CRITICAL**: Failed `logic-compare` (logic loss) or failed `SecurityValidator` (unsafe I/O).
-   **HIGH**: Architectural layer violation (e.g. CLI importing from Core).
-   **MEDIUM**: Bare exceptions or high-complexity functions.
-   **LOW**: Stylistic inconsistencies reported by Ruff/isort.

## 3. Mandatory Workflow
1.  **Scope Determination**: Target `HEAD` vs `HEAD~1` for incremental tasks.
2.  **Tool Execution**: Run the `code-review` recipe.
3.  **DNA Audit**: Explicitly report the Parity Score for all ported functions.
4.  **Security Audit**: Verify that all I/O is gated by the Project Root isolation logic.
