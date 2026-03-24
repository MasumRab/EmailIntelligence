# Skill: Smart-Persistence (Native Tracking)

This skill provides a rigorous methodology for tracking findings and tasks across agent sessions using repository-native memory and Beads.

## 1. Finding Persistence (Repo-Native)
**NEVER** use global `save_memory` for project-specific findings. Instead, use the Beads memory engine:
-   **Store Finding**: `bd remember "Context: [Finding description]"`
-   **Retrieve Context**: `bd memories` or `bd recall [search_term]`
-   **Forget Obsolescence**: `bd forget [id]`

## 2. Task Persistence (Beads / Git-Backed)
Use the `bd` (Beads) tool for **Project-Specific State**:
-   **Discovery**: Use `bd create "[Title]" --body "[Description]"` to record every Gap or Debt.
-   **Dependency**: Use `bd dep add [blocked_id] [blocker_id]` to map logic requirements.
-   **Execution**: Use `bd ready` to identify unblocked tasks for the current session.
-   **Completion**: Use `bd close [id]` once the task is verified.

## 3. Persistent Contract (Project Rules)
Enforce long-term findings through the `.agent/rules/` directory:
-   Use `rule-sync` to publish findings from the `bd` database into active agent rules (`.clinerules`, `.cursor/rules`).

## 4. Sub-Agent Synchronization
-   Pass the current `bd` task ID to sub-agents.
-   Sub-agents must update the bead state (`bd update` or `bd comments`) before exiting.
