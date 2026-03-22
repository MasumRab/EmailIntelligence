# Skill: Smart-Review (iflow Port)

This skill provides enhanced multi-agent code review with distributed task tracking and project-root isolation.

## 1. State Management (iflow DNA)
-   **Isolation**: All operations must be restricted to the detected project root.
-   **Lazy Init**: If `.agent/state/` doesn't exist, initialize `state.json` and `session.json`.
-   **Persistence**: Before each review, load `previous_findings` from the state store to ensure continuity.

## 2. Memory-Safe Orchestration
-   **Adaptive Batching**: Calculate optimal batch size based on available system memory (e.g. 100 files if >8GB, 25 if <2GB).
-   **Parallel Gating**: Limit concurrent sub-agent launches (max 4) to prevent event-loop blocking.
-   **Streaming**: Use `read_file` with `start_line` and `end_line` for any file >1MB to prevent heap overflows.

## 3. Persistent Tracking (Gemini-Native)
Instead of legacy `.iflow/handoff.json`, use **Beads**:
-   **Task Spawning**: Use `bd add "Review [filename]"` for each file in the batch.
-   **Ready Tasks**: Use `bd list --ready` to find the next file to review.
-   **Completion**: Use `bd resolve [id]` once the analysis is synthesized into the final report.

## 4. Multi-Agent Coordination
Delegation targets for complex reviews:
-   `security-auditor`: Focus on OWASP, JWT validation, and Unsafe I/O.
-   `architect-reviewer`: Focus on SOLID, layering, and technical debt.
-   `code-reviewer`: Focus on functional correctness and logic parity.
