# Data Model: Orchestration Workflow System

**Spec**: `specs/010-orchestration-workflow/spec.md`

## Configuration Models

### OrchestrationConfig

```yaml
version: "1.0"
orchestration_branch: "orchestration-tools"
sync_on_checkout: true
hook_auto_install: true
conflict_resolution: "manual"
```

### HookVersion

```yaml
hook_name: "post-checkout"
version: "1.2.0"
checksum: "sha256:abc123..."
installed_at: "2025-11-20T10:00:00Z"
```

### SyncStatus

```yaml
branch: "main"
last_sync: "2025-11-20T10:00:00Z"
files_synced: 15
conflicts: []
status: "success" | "partial" | "failed"
```

## Node-Based Workflow Models

### NodeConnection

```yaml
source_node_id: "uuid"
source_port: "output_1"
target_node_id: "uuid"
target_port: "input_email"
connection_id: "uuid"
```

### WorkflowExecutionContext

```yaml
workflow_id: "uuid"
execution_id: "uuid"
node_states: Map[NodeId, NodeState]
connection_states: Map[ConnectionId, ConnectionState]
started_at: "timestamp"
timeout_seconds: 300
retry_policy:
  max_retries: 3
  backoff_multiplier: 2.0
```

### WorkflowTestResult

```yaml
workflow_id: "uuid"
test_type: "unit" | "integration" | "e2e"
passed: true
duration_ms: 1250
error: null | string
```

## References

- Full node-based workflow types: `src/core/models.py`
- Workflow engine: `src/core/advanced_workflow_engine.py`
- Security models: `src/core/security.py`
