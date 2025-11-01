# Node-Based Architecture Documentation

## Overview

The Email Intelligence Platform now features a modular, extensible node-based workflow system that allows for complex email processing pipelines. This architecture is inspired by modern AI frameworks like ComfyUI and provides a visual, composable approach to email processing workflows.

## Architecture Components

### Core Node System
- **`BaseNode`**: Abstract base class that all nodes inherit from
- **`NodePort`**: Defines typed input/output connections between nodes
- **`Connection`**: Represents data flow between nodes
- **`Workflow`**: Container for nodes and their connections
- **`ExecutionContext`**: Maintains execution state and context

### Node Types

#### `EmailSourceNode`
- Sources emails from various providers (Gmail, etc.)
- Outputs: `emails` (EMAIL_LIST), `status` (JSON)

#### `PreprocessingNode`
- Cleans and normalizes email data
- Outputs: `processed_emails` (EMAIL_LIST), `stats` (JSON)

#### `AIAnalysisNode`
- Performs NLP and AI analysis (sentiment, topic)
- Outputs: `analysis_results` (JSON), `summary` (JSON)

#### `FilterNode`
- Applies filtering rules based on configurable criteria
- Outputs: `filtered_emails` (EMAIL_LIST), `discarded_emails` (EMAIL_LIST), `stats` (JSON)

#### `ActionNode`
- Executes actions on emails (move, label, forward, respond)
- Outputs: `results` (JSON), `status` (JSON)

## Security Features

### SecurityManager
- Validates node execution against security policies
- Manages trusted vs untrusted node types
- Enforces API call limits per workflow

### InputSanitizer
- Sanitizes all inputs to prevent injection attacks
- Supports string, JSON, and dictionary sanitization
- Removes potentially dangerous patterns

### ExecutionSandbox
- Provides timeout protection for node execution
- Enforces resource limits per node
- Ensures nodes don't run indefinitely

### ResourceManager
- Manages concurrent workflow execution
- Controls resource usage (memory, execution time)
- Provides queuing for high-load scenarios

### AuditLogger
- Maintains comprehensive logs of all operations
- Tracks workflow execution start/end and node execution
- Logs security events for compliance

## Creating Custom Nodes

To create a custom node, inherit from `BaseNode` and implement:

1. Define input/output ports in `__init__`
2. Implement the `execute()` method
3. Register the node type with the workflow engine

Example:
```python
from backend.node_engine.node_base import BaseNode, NodePort, DataType

class CustomEmailNode(BaseNode):
    def __init__(self, config=None, node_id=None, name=None):
        super().__init__(node_id, name or "Custom Email Node", "Description")
        self.config = config or {}
        self.input_ports = [
            NodePort("emails", DataType.EMAIL_LIST, required=True)
        ]
        self.output_ports = [
            NodePort("processed_emails", DataType.EMAIL_LIST, required=True),
            NodePort("stats", DataType.JSON, required=True)
        ]
    
    async def execute(self, context):
        # Implement node logic here
        input_emails = self.inputs.get("emails", [])
        
        # Process emails
        processed_emails = []
        for email in input_emails:
            # Custom processing logic
            processed_email = email.copy()
            processed_email["custom_processed"] = True
            processed_emails.append(processed_email)
        
        return {
            "processed_emails": processed_emails,
            "stats": {"processed_count": len(processed_emails)}
        }

# Register the node
from backend.node_engine.workflow_engine import workflow_engine
workflow_engine.register_node_type(CustomEmailNode)
```

## API Integration

The node-based workflow system can be integrated with existing APIs:

- Workflows can be executed via the workflow engine programmatically
- Results can be stored in the existing database system
- Performance metrics integrate with the existing monitoring system

## Workflow Management

### Creating Workflows
```python
from backend.node_engine.node_base import Workflow, Connection

workflow = Workflow(name="My Email Processing Pipeline")

# Add nodes
source = EmailSourceNode()
processor = PreprocessingNode()
analyzer = AIAnalysisNode()

workflow.add_node(source)
workflow.add_node(processor)
workflow.add_node(analyzer)

# Connect nodes
workflow.add_connection(Connection(
    source_node_id=source.node_id,
    source_port="emails",
    target_node_id=processor.node_id,
    target_port="emails"
))

workflow.add_connection(Connection(
    source_node_id=processor.node_id,
    source_port="processed_emails",
    target_node_id=analyzer.node_id,
    target_port="emails"
))
```

### Executing Workflows
```python
from backend.node_engine.workflow_engine import workflow_engine

context = await workflow_engine.execute_workflow(workflow, user_id="example_user")
```

### Saving and Loading Workflows
```python
from backend.node_engine.workflow_manager import workflow_manager

# Save workflow
file_path = workflow_manager.save_workflow(workflow)

# Load workflow
loaded_workflow = workflow_manager.load_workflow(workflow.workflow_id)
```

## Testing

The node-based system includes comprehensive testing:

- `test_nodes.py`: Basic node functionality
- `test_security.py`: Security and scalability features  
- `test_integration.py`: Complete system integration

Run tests with:
```bash
python -m backend.node_engine.test_nodes
python -m backend.node_engine.test_security
python -m backend.node_engine.test_integration
```

## Migration from Legacy System

The node-based architecture complements existing functionality rather than replacing it:

- Existing API endpoints remain functional
- Database schemas remain unchanged
- Existing NLP and AI models can be accessed through AIAnalysisNode
- Performance monitoring continues to work as before

Legacy workflows can be gradually migrated to the new node-based system as needed.