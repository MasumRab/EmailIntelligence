# Skill: Smart-Persistence (Native Tracking)

This skill provides a methodology for tracking findings and tasks across agent sessions using Native Memory and Beads.

## 1. Finding Persistence (Native Memory)
Use the `save_memory` tool for **Global/High-Level Context**:
-   User preferences (e.g. "User prefers explicit logging over silent returns").
-   Environment facts (e.g. "System uses Python 3.12 via MISE").
-   Security constraints (e.g. "Never modify .env files").

## 2. Task Persistence (Beads / Git-Backed)
Use the `bd` (Beads) tool for **Project-Specific State**:
-   **Discovery Phase**: Use `bd add` to record every "Gap" or "Debt" found during a scan.
-   **Traceability**: Use `bd link [child] [parent]` to map dependencies (e.g. "Refactor imports" depends on "Port logic-compare").
-   **Durable Handoff**: If a session is interrupted, use `bd list` to identify the exact point of failure.

## 3. Persistent Contract (Project Rules)
Enforce findings through the `.agent/rules/` directory:
-   Once a "Style Guide" violation is consistently found, update `.agent/rules/logic_preservation.md` to permanently prevent it.
-   Use `rule-sync` to publish these persistent findings to all agents (Cursor, Cline, Gemini).

## 4. Sub-Agent Synchronization
-   When delegating to a sub-agent, pass the current `bd` task ID as context.
-   Sub-agents must report their findings back to the Beads graph before exiting.
