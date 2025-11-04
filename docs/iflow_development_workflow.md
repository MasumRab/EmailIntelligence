# iFlow CLI Development Workflow Guide

This document outlines the development workflow when using the iFlow CLI for the EmailIntelligence project.

## Session Structure

1. **Session Initialization**
   - Create a new session log in `backlog/sessions/` with the naming convention `IFLOW-YYYYMMDD-XXX.md`
   - Document session goals, context, and initial state
   - Update the main `SESSION_LOG.md` with session tracking information

2. **Task Planning**
   - Use the iFlow CLI todo system to track tasks
   - Break down complex tasks into manageable steps
   - Prioritize tasks based on project needs

3. **Implementation**
   - Follow project conventions as documented in IFLOW.md
   - Use appropriate tools for code reading, writing, and modification
   - Maintain consistent code style with existing project code

4. **Documentation**
   - Document all activities in the session log
   - Update relevant documentation files as needed
   - Record development priorities and next steps

5. **Session Closure**
   - Summarize completed work and outcomes
   - Document any remaining tasks for future sessions
   - Archive session log appropriately

## iFlow CLI Integration

The iFlow CLI is designed to assist with software engineering tasks in the EmailIntelligence project. It specializes in:

- Code understanding and analysis
- Refactoring and implementation
- Testing and verification
- Following project conventions strictly

## Tools Available

- `read_file`: Read file contents
- `write_file`: Write content to a file
- `replace`: Replace text within a file
- `search_file_content`: Search for patterns in files
- `glob`: Find files matching patterns
- `run_shell_command`: Execute shell commands
- `todo_write`/`todo_read`: Task management

## Workflow Process

1. **Understand**: Analyze the user's request and relevant codebase context
2. **Plan**: Build a coherent plan based on understanding
3. **Implement**: Use available tools to act on the plan
4. **Verify (Tests)**: Run project's testing procedures
5. **Verify (Standards)**: Execute project-specific build, linting and type-checking commands

## Session Expectations

- All development activities should be documented in session logs
- Code changes should follow existing project conventions
- Tasks should be tracked using the iFlow CLI todo system
- Regular updates should be made to session logs during development
- Session logs should be moved to the backlog/sessions directory upon completion