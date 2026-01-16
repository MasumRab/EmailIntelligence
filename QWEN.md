# Taskmaster - AI-Powered Task Management System

## Project Overview

Taskmaster is an AI-powered task management system designed to facilitate agentic development workflows. It provides a structured approach to managing complex software development projects through automated task generation, analysis, and tracking. The system integrates with AI tools like Claude Code and supports MCP (Model Context Protocol) integration for enhanced development capabilities.

The project combines several key components:
- **Task Management**: Automated generation and tracking of development tasks
- **AI Integration**: Support for multiple AI providers (Anthropic, OpenAI, Gemini, etc.)
- **Git Workflows**: Advanced git worktree-based conflict resolution and management
- **Specification-Driven Development**: Constitutional/specification-based analysis and development

## Core Architecture

### Directory Structure
```
.taskmaster/
├── archive/              # Archived tasks and data
├── backups/              # Backup files
├── complexity_reports/   # Task complexity analysis reports
├── docs/                # Documentation including PRD
├── guidance/            # Guidance and instruction files
├── implement/           # Implementation-related files
├── refactor/            # Refactoring tools and scripts
├── reports/             # Analysis reports
├── scripts/             # Automation scripts
├── src/                 # Main source code
│   ├── analysis/        # Conflict and constitutional analysis modules
│   ├── core/            # Core interfaces, models, and exception handling
│   ├── git/             # Git operations and conflict detection
│   ├── resolution/      # Auto-resolution and semantic merging
│   ├── strategy/        # Strategy generation and risk assessment
│   ├── utils/           # Utility functions and logging
│   └── validation/      # Validation components
├── task_data/           # Task-related data files
├── task_scripts/        # Task-specific scripts
├── tasks/               # Task database and individual task files
├── templates/           # Task templates
├── tests/               # Test files
├── .env                 # API keys (not committed)
├── .mcp.json            # MCP configuration
├── AGENT.md             # Agent integration guide
├── CLAUDE.md            # Claude Code integration
├── config.json          # AI model configuration
├── emailintelligence_cli.py # Main CLI application
├── execute_phases_2_4.py # Execution scripts
├── pyproject.toml       # Python project configuration
└── README.md            # Project documentation
```

### Key Components

1. **EmailIntelligence CLI** (`emailintelligence_cli.py`): The main CLI application for git worktree-based conflict resolution using constitutional/specification-driven analysis.

2. **Task Management System**: Automated generation and tracking of development tasks following a standardized 14-section format.

3. **Constitutional Engine**: Framework for specification-driven analysis and compliance checking.

4. **Git Operations**: Advanced conflict detection and resolution using worktrees and semantic merging.

## Building and Running

### Prerequisites
- Python 3.8+
- Git with worktree support
- API keys for selected AI providers (Anthropic, OpenAI, Gemini, etc.)

### Setup
1. Install dependencies:
   ```bash
   pip install poetry
   poetry install
   ```

2. Configure API keys in `.env`:
   ```
   ANTHROPIC_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   GEMINI_API_KEY=${GEMINI_API_KEY}
   # Add other provider keys as needed
   ```

3. Initialize Taskmaster in your project:
   ```bash
   task-master init
   ```

### Core Commands
```bash
# Project Setup
task-master init                                    # Initialize Task Master in current project
task-master parse-prd .taskmaster/docs/prd.md       # Generate tasks from PRD document
task-master models --setup                          # Configure AI models interactively

# Daily Development Workflow
task-master list                                    # Show all tasks with status
task-master next                                    # Get next available task to work on
task-master show <id>                              # View detailed task information
task-master set-status --id=<id> --status=done     # Mark task complete

# Task Management
task-master add-task --prompt="description" --research        # Add new task with AI assistance
task-master expand --id=<id> --research --force              # Break task into subtasks
task-master update-task --id=<id> --prompt="changes"         # Update specific task
task-master update --from=<id> --prompt="changes"            # Update multiple tasks from ID onwards
task-master update-subtask --id=<id> --prompt="notes"        # Add implementation notes to subtask

# Analysis & Planning
task-master analyze-complexity --research          # Analyze task complexity
task-master complexity-report                      # View complexity analysis
task-master expand --all --research               # Expand all eligible tasks
```

### Running the Service
```bash
# Using the FastAPI application
python -m src.main

# Or with uvicorn
uvicorn src.main:create_app --factory --host 0.0.0.0 --port 8000
```

### MCP Integration
Taskmaster provides an MCP server that can be integrated with Claude Code. Configure in `.mcp.json`:

```json
{
  "mcpServers": {
    "task-master-ai": {
      "command": "npx",
      "args": ["-y", "task-master-ai"],
      "env": {
        "TASK_MASTER_TOOLS": "core",
        "ANTHROPIC_API_KEY": "your_key_here",
        "PERPLEXITY_API_KEY": "your_key_here",
        "OPENAI_API_KEY": "OPENAI_API_KEY_HERE",
        "GEMINI_API_KEY": "${GEMINI_API_KEY}",
        "XAI_API_KEY": "XAI_API_KEY_HERE",
        "OPENROUTER_API_KEY": "OPENROUTER_API_KEY_HERE",
        "MISTRAL_API_KEY": "MISTRAL_API_KEY_HERE",
        "AZURE_OPENAI_API_KEY": "AZURE_OPENAI_API_KEY_HERE",
        "OLLAMA_API_KEY": "OLLAMA_API_KEY_HERE"
      }
    }
  }
}
```

## Development Conventions

### Task Structure Standard
All tasks follow a standardized 14-section format:
1. Task Header
2. Overview/Purpose
3. Success Criteria (detailed)
4. Prerequisites & Dependencies
5. Sub-subtasks Breakdown
6. Specification Details
7. Implementation Guide
8. Configuration Parameters
9. Performance Targets
10. Testing Strategy
11. Common Gotchas & Solutions
12. Integration Checkpoint
13. Done Definition
14. Next Steps

### Git Workflows
- Use git worktrees for parallel development
- Leverage the EmailIntelligence CLI for conflict resolution
- Follow the constitutional analysis approach for code reviews
- Use the orchestration protection mechanisms for critical files

### AI Model Configuration
- Configure three tiers of models: main, research, and fallback
- Use appropriate models for different tasks (e.g., research models for analysis)
- Maintain API key security in environment variables

### Code Quality Standards
- Follow PEP 8 for Python code
- Use type hints for all public interfaces
- Include comprehensive docstrings
- Maintain high test coverage (>95%)
- Implement proper error handling and logging

## Key Features

### AI-Powered Task Management
- Automatic task generation from PRD documents
- Intelligent task expansion and subtask creation
- Research-enhanced task updates using AI
- Complexity analysis and estimation

### Constitutional Analysis
- Specification-driven development approach
- Constitutional compliance checking
- Risk assessment for code changes
- Automated validation of implementation

### Git Integration
- Advanced conflict detection and resolution
- Worktree-based isolation for parallel development
- Constitutional analysis of git operations
- Safe branching and merging workflows

### Orchestration Protection
- Monitoring of critical orchestration files
- Protection against destructive operations
- Automated verification of system integrity
- Migration verification processes

## EmailIntelligence CLI Commands

The EmailIntelligence CLI provides advanced git worktree-based conflict resolution:

```bash
# Setup resolution workspace
eai setup-resolution --pr 123 --source-branch feature/auth --target-branch main

# Analyze constitutional compliance
eai analyze-constitutional --pr 123 --constitution ./constitutions/auth.yaml

# Develop resolution strategy
eai develop-spec-kit-strategy --pr 123 --worktrees --interactive

# Execute content alignment
eai align-content --pr 123 --interactive --checkpoint-each-step

# Validate resolution
eai validate-resolution --pr 123 --comprehensive

# Auto-resolve conflicts
eai auto-resolve --pr 123
```

## Best Practices

### Task Management
- Use `--research` flag for complex technical tasks requiring AI assistance
- Regularly update subtasks with implementation notes using `update-subtask`
- Follow the 14-section task structure standard for consistency
- Use dependency tracking to manage task relationships

### Development Workflow
- Start each session with `task-master next` to get the next task
- Use worktrees for parallel development on different tasks
- Apply constitutional analysis to ensure code quality
- Regularly run complexity analysis to identify potential issues

### Integration with AI Tools
- Configure appropriate models for different types of tasks
- Use Claude Code with the provided integration for enhanced development
- Leverage MCP tools for streamlined AI interactions
- Maintain secure handling of API keys and sensitive information

## Troubleshooting

### Common Issues
- **AI Commands Failing**: Check API key configuration and model settings
- **MCP Connection Issues**: Verify `.mcp.json` configuration and Node.js installation
- **Task File Sync Issues**: Run `task-master generate` to regenerate task files

### Performance Optimization
- Use appropriate model tiers for different tasks to balance cost and capability
- Implement caching for repeated operations
- Monitor resource usage during complex analyses
- Use worktrees to isolate resource-intensive operations