# Branch Workflow Analysis Report

## Overview
This document provides analysis of the different workflows implemented in various branches of the EmailIntelligence repository.

## Branch: feature/generate-tasks-md
**Status**: Local feature branch
**Focus**: AI-assisted task and specification generation (Speckit system)

### Key Characteristics:
- Implements a sophisticated AI-assisted development workflow called "Speckit"
- Contains `.specify/` directory with templates and scripts for generating feature specifications
- Has structured specification templates that guide AI agents through the specification process
- Includes AI command files in `.claude/commands/` and `.opencode/command/` for automated task generation
- Advanced context control system in `.context-control/` to manage project context for AI agents
- Sophisticated orchestration system pulling changes from the `orchestration-tools` branch
- Includes advanced Git hooks with recursion prevention and safety checks
- Features worktree vs subtree detection and different sync strategies

### Unique Files:
- `.specify/` directory with templates and memory files
- Speckit command files in `.claude/commands/` and `.opencode/command/`
- AI agent guidelines for Qwen, Claude, Gemini, etc.

## Branch: 003-execution-layer-tasks-pr
**Status**: Local feature branch
**Focus**: Execution layer specifications and planning

### Key Characteristics:
- Focuses on execution layer specs and planning documentation
- Includes task completion tracking, dependency resolution, and task queuing systems
- Has scripts specifically for task management: `task_completion_tracker.py`, `task_decomposer.py`, `task_dependency_resolver.py`, `task_queue.py`
- Contains alignment templates for tasks: `alignment-main-task-template.md`, `alignment-task-template.md`
- Includes planning files like `implement/plan.md`, `merge_phase_plan.md`, `refactoring_plan.md`

### Unique Files:
- Task management scripts in `scripts/`
- Alignment and planning documentation
- Backlog task expansion research summary

## Branch: feat/modular-ai-platform
**Status**: Local feature branch (tracks remote)
**Focus**: Modular AI platform implementation

### Key Characteristics:
- Implements a modular AI platform architecture
- Contains decoupled AI components that can be swapped or extended
- Likely contains abstraction layers for different AI models and services
- Has significant differences from main branch (625 files changed)

## Branch: feature-notmuch-tagging-1
**Status**: Local feature branch (ahead 1, behind 1 from remote)
**Focus**: Notmuch email tagging integration

### Key Characteristics:
- Integrates with notmuch email system for advanced tagging and search capabilities
- Contains specialized modules for notmuch integration
- Has the most file differences from main (1430 files)
- Focuses on email indexing and tagging workflows

## Branch: scientific
**Status**: Local feature branch (ahead 2, behind 12 from remote)
**Focus**: Scientific computing and advanced analytics

### Key Characteristics:
- Focuses on scientific computing approaches to email analysis
- Contains more advanced algorithms and models
- Includes specialized NLP and machine learning components
- May include more sophisticated data analysis tools

## Branch: orchestration-tools-temp
**Status**: Local branch (ahead 2, behind 52 from remote)
**Focus**: Orchestration tools and automation

### Key Characteristics:
- Contains orchestration and automation tools
- Temporarily modified orchestration scripts
- Focus on development workflow automation

## Summary
The repository contains several specialized branches with distinct purposes:

1. `feature/generate-tasks-md` - AI-assisted development with Speckit system
2. `003-execution-layer-tasks-pr` - Task execution and planning layer
3. `feat/modular-ai-platform` - Modular AI architecture
4. `feature-notmuch-tagging-1` - Notmuch email system integration
5. `scientific` - Scientific computing approaches
6. `orchestration-tools-temp` - Development orchestration tools

Each branch represents a different approach or focus area for the Email Intelligence platform, with the feature branches containing specialized functionality that may eventually be integrated into the main codebase.