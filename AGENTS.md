# Additional Conventions Beyond the Built-in Functions

As this project's AI coding tool, you must follow the additional conventions below, in addition to the built-in functions.

# Project Overview

## General Guidelines

- Use TypeScript for all new code
- Follow consistent naming conventions
- Write self-documenting code with clear variable and function names
- Prefer composition over inheritance
- Use meaningful comments for complex business logic

## Code Style

- Use 2 spaces for indentation
- Use semicolons
- Use double quotes for strings
- Use trailing commas in multi-line objects and arrays

## Architecture Principles

- Organize code by feature, not by file type
- Keep related files close together
- Use dependency injection for better testability
- Implement proper error handling
- Follow single responsibility principle

## Context Contamination Prevention

### Definition
Context contamination occurs when information from one task/conversation bleeds into another, causing the AI agent to apply incorrect assumptions, patterns, or state to unrelated work. This can lead to:
- Cross-task information pollution
- Incorrect pattern matching
- State leakage between independent operations
- Biased reasoning from previous contexts

### Prevention Guidelines

#### 1. Task Isolation
- Each task should maintain its own isolated context
- Do not carry assumptions from previous tasks into new ones
- Reset mental state when switching between different features or modules
- Explicitly close out one task before starting another

#### 2. Tool State Management
- Keep tool usage stateless where possible
- Do not assume file system state persists between operations
- Re-verify current branch/working directory at task start
- Clear command history mentally between independent operations

#### 3. Documentation Boundaries
- Document task-specific requirements separately
- Avoid mixing concerns from different features
- Use clear section boundaries in documentation
- Reference shared patterns by explicit link, not implicit memory

#### 4. Code Review Protection
- Review code changes in context of current task only
- Do not apply patterns from adjacent features without explicit consideration
- Verify that dependencies are intentional, not accidental carryover
- Question inherited assumptions from previous work

#### 5. Communication Clarity
- State assumptions explicitly when switching contexts
- Confirm task scope with user before proceeding
- Log context switches in session notes
- Use clear delimiters between different work items

#### 6. Testing and Verification
- Test changes in isolation before integration
- Verify no unintended side effects on unrelated modules
- Run relevant test suites for affected areas only
- Document any discovered cross-module impacts
