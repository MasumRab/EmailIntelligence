# Agent Orchestration Scripts

This directory contains the core agent orchestration and management scripts for the EmailIntelligence system.

## Core Agent Components

### Agent Registry (`agent_registry.py`)
- **Purpose**: Manages agent registrations and discovery
- **Features**:
  - Agent registration and deregistration
  - Agent capability discovery
  - Health status tracking
  - Load balancing coordination

### Agent Health Monitor (`agent_health_monitor.py`)
- **Purpose**: Monitors the health and status of all agents in the system
- **Features**:
  - Real-time health checks
  - Agent heartbeat monitoring
  - Failure detection and alerting
  - Recovery automation

### Agent Performance Monitor (`agent_performance_monitor.py`)
- **Purpose**: Tracks and analyzes agent performance metrics
- **Features**:
  - Performance metric collection
  - Bottleneck identification
  - Resource utilization tracking
  - Performance optimization recommendations

### Agent Workflow Integration (`agent_workflow_integration.py`)
- **Purpose**: Integrates agents into the overall workflow system
- **Features**:
  - Workflow orchestration
  - Agent task assignment
  - Inter-agent communication
  - Workflow state management

## Testing

Each agent component has corresponding test files:
- `test_agent_registry.py`
- `test_agent_health_monitor.py`
- `test_agent_performance_monitor.py`

## Usage

### Starting Agent Services

```bash
# Start the agent registry
python scripts/agents/agent_registry.py

# Start health monitoring
python scripts/agents/agent_health_monitor.py

# Start performance monitoring
python scripts/agents/agent_performance_monitor.py
```

### Running Tests

```bash
# Run all agent tests
python -m pytest scripts/agents/test_*.py

# Run specific agent tests
python scripts/agents/test_agent_registry.py
```

## Architecture

The agent system follows a microservices architecture where each agent is responsible for a specific domain:

- **Registry**: Service discovery and coordination
- **Health Monitor**: System reliability and uptime
- **Performance Monitor**: Optimization and efficiency
- **Workflow Integration**: Task orchestration and execution

## Dependencies

- Python 3.11+
- Required packages listed in `pyproject.toml`
- Access to shared configuration in `config/`

## Configuration

Agent configurations are managed through:
- `config/llm_guidelines.json` - Agent behavior guidelines
- `scripts/sync_config.json` - Synchronization settings
- Environment variables for runtime configuration

## Monitoring and Logging

All agents include comprehensive logging and monitoring:
- Structured logging with JSON output
- Metrics collection for observability
- Alert generation for critical events
- Performance profiling capabilities

## Development

When adding new agents:
1. Follow the existing naming conventions
2. Include comprehensive test coverage
3. Update this README with new agent documentation
4. Ensure proper error handling and logging
5. Add configuration options as needed

## Related Components

- **Task Management**: `../task_*.py` scripts for task orchestration
- **Synchronization**: `../sync_*.py` scripts for data synchronization
- **Validation**: `../*validator.py` scripts for system validation
- **Documentation**: `../doc_*.py` scripts for automated documentation