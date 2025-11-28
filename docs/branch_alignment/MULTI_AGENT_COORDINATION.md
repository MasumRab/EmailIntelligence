# Qwen Code CLI Multi-Agent Coordination System

## Overview
Qwen Code CLI provides multi-agent capabilities for coordinating complex software development tasks. The system is designed to support multiple specialized agents working together to achieve comprehensive software engineering objectives.

## Available Agent Types
The system provides specialized agents to assist with different aspects of software development:

- **architect-reviewer**: Architecture review and consistency validation
- **backend-architect**: Backend architecture and design decisions
- **code-reviewer**: Code quality, correctness, and production-readiness
- **error-detective**: Bug detection and root cause analysis
- **git-error-detective**: Git merge/rebase conflicts and version control issues
- **python-pro**: Python-specific best practices and idiomatic code
- **ai-engineer**: AI application development and LLM integration
- **context-manager**: Multi-agent context management and isolation
- **data-engineer**: Data pipelines and ETL processes
- **docs-architect**: Documentation architecture and technical writing
- **javascript-pro**: JavaScript/TypeScript expertise
- **ml-engineer**: ML pipeline engineering and model serving
- **prompt-engineer**: Prompt optimization and LLM behavior tuning
- **quant-analyst**: Financial modeling and statistical analysis
- **reference-builder**: Technical reference creation and API documentation
- **risk-manager**: Risk assessment and mitigation strategies
- **search-specialist**: Research and information gathering

## Agent Delegation Mechanism
Agents can be proactively used via the `task` tool when tasks match their specific capabilities:

```python
task(description="Review code structure", 
     prompt="Please perform a comprehensive code review...", 
     subagent_type="code-reviewer")
```

## Coordination Architecture
The multi-agent system uses a centralized coordination pattern:

### 1. Centralized Task Management
- Tasks are managed through a central coordinator (the main Qwen Code interface)
- Individual agent execution is initiated via the `task` command
- Results are aggregated and presented to the user

### 2. Context Isolation
- Each agent operates with appropriate context for their specialization
- Context sharing between agents is managed explicitly via shared state files
- The `context-manager` agent specializes in maintaining proper context boundaries

### 3. Capability-Based Routing
- Tasks are automatically routed to appropriate agents based on capability matching
- Each agent has specific expertise areas where they excel
- Agent selection is based on the nature of the task and required expertise

## Usage Guidelines
- For architecture decisions → use `architect-reviewer`
- For code quality → use `code-reviewer` 
- For error detection → use `error-detective`
- For Git issues → use `git-error-detective`
- For Python expertise → use `python-pro`
- For documentation → use `docs-architect`
- For AI-specific tasks → use `ai-engineer`

## Coordination Workflow
The system supports multi-agent workflows through:
1. **Sequential Agent Invocation**: One agent followed by another for different aspects
2. **Parallel Agent Tasks**: Multiple agents working on different aspects simultaneously
3. **Result Aggregation**: Coordinated presentation of multiple agent outputs
4. **Context Handoff**: Proper transfer of context between different agents

This multi-agent coordination system enables comprehensive software development assistance by leveraging specialized expertise while maintaining coordination and consistency.