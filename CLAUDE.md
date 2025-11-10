
<!-- BACKLOG.MD MCP GUIDELINES START -->

<CRITICAL_INSTRUCTION>

## BACKLOG WORKFLOW INSTRUCTIONS

This project uses Backlog.md MCP for all task and project management activities.

**CRITICAL GUIDANCE**

- If your client supports MCP resources, read `backlog://workflow/overview` to understand when and how to use Backlog for this project.
- If your client only supports tools or the above request fails, call `backlog.get_workflow_overview()` tool to load the tool-oriented overview (it lists the matching guide tools).

- **First time working here?** Read the overview resource IMMEDIATELY to learn the workflow
- **Already familiar?** You should have the overview cached ("## Backlog.md Overview (MCP)")
- **When to read it**: BEFORE creating tasks, or when you're unsure whether to track work

These guides cover:
- Decision framework for when to create tasks
- Search-first workflow to avoid duplicates
- Links to detailed guides for task creation, execution, and completion
- MCP tools reference

You MUST read the overview resource to understand the complete workflow. The information is NOT summarized here.

</CRITICAL_INSTRUCTION>

<!-- BACKLOG.MD MCP GUIDELINES END -->

## Agent Context Control System

This project implements an **Agent Context Control** system that automatically detects branch environments and provides appropriate context isolation for AI agents. This prevents context contamination between different development branches (scientific, main, orchestration-tools).

### Key Features
- **Branch Detection**: Automatically detects current Git branch and detached HEAD states
- **Context Isolation**: Ensures agents receive branch-specific context without cross-contamination
- **Project Configuration**: Supports project-specific agent capabilities and behavior
- **Performance Optimized**: Context access in <500ms, switching in <2s
- **Comprehensive Testing**: TDD implementation with 95%+ coverage

### Usage
```python
from src.context_control import ContextController

controller = ContextController()
context = controller.get_context_for_branch(agent_id="my_agent")
```

### CLI Tool
```bash
# Get context for current branch
python scripts/context-control

# Validate context
python scripts/context-control --validate
```

### Architecture
- `src/context_control/core.py`: Main context management
- `src/context_control/environment.py`: Git branch detection
- `src/context_control/validation.py`: Context validation
- `src/context_control/models.py`: Data models (ContextProfile, AgentContext)

### Testing
Run tests with: `pytest tests/unit/ tests/integration/`

This system ensures AI agents work safely across different branch environments without context leakage.
