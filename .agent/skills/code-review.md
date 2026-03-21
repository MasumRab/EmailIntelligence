# Code Review Skill

This skill provides the AI agent with instructions for performing rigorous, industrial-grade code reviews.

## Core Principles
1.  **Forensic Parity**: Always check if removed logic was actually migrated or if it was accidentally deleted.
2.  **Incremental Focus**: Default to reviewing the current `HEAD` against `HEAD~1` to maintain high fidelity and avoid tool limits.
3.  **Security Gating**: Ensure every new I/O operation is wrapped in the `SecurityValidator`.

## Workflow
When a user asks for a "Review" or uses the `/code-review` command:
1.  Verify the current branch and recent commit history.
2.  Trigger the CodeRabbit review using `coderabbit review --base-commit HEAD~1 --plain`.
3.  Perform a manual check of any removed imports or logic blocks.
4.  Synthesize the results and provide actionable architectural feedback.

## Tooling
-   **Primary**: CodeRabbit CLI
-   **Verification**: `python3 dev.py logic-compare`
-   **Audit**: `python3 dev.py code-audit`
