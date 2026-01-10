# Data Model: Guided Workflows

## Workflow Context

The `WorkflowContextManager` maintains the state of the user's interaction.

### Entity: WorkflowState

| Field | Type | Description |
|---|---|---|
| `current_workflow` | `str` (Enum) | The active workflow: `guide-dev` or `guide-pr`. |
| `current_step` | `str` | The current step within the workflow (e.g., `intent_selection`, `branch_check`). |

### State Transitions

**Workflow: `guide-dev`**
1. `start` -> `intent_selection`
2. `intent_selection` -> `app_code_guidance` (Terminal)
3. `intent_selection` -> `shared_config_guidance` -> `branch_check`
4. `branch_check` -> `success` (Terminal)
5. `branch_check` -> `warning` (Terminal)

**Workflow: `guide-pr`**
1. `start` -> `type_selection`
2. `type_selection` -> `orchestration_guidance` (Terminal)
3. `type_selection` -> `feature_guidance` (Terminal)
