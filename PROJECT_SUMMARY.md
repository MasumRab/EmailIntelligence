# EmailIntelligenceQwen Project Summary

**Date:** Monday, November 10, 2025  
**Project Location:** `/home/masum/github/EmailIntelligenceQwen`

## Overview
EmailIntelligenceQwen is a GitHub repository focused on email intelligence and AI-powered email processing. The project implements a structured planning workflow for managing development tasks and features using Python 3.12 as the primary technology.

## Technologies Used
- **Primary Language:** Python 3.12
- **Version Control:** Git
- **GitHub CLI:** For repository management
- **Standard Python Libraries:** Core functionality
- **Code Quality Tools:** Snyk, SonarQube, Dependabot
- **Testing Framework:** pytest
- **Code Linting:** ruff

## Project Structure
```
src/
tests/
backlog/
├── tasks/
scripts/
├── planning_workflow_helper.py
├── planning_report_generator.py
├── planning_automation.py
└── task_validator.py
```

## Key Features & Functionality
Based on the repository structure and available tools, the project includes:

1. **Planning Workflow System:**
   - Structured task management system (documented in PLANNING_WORKFLOW.md)
   - Backlog management system with task tracking
   - Automated planning tools and validators
   - Report generation capabilities

2. **Email Intelligence Tools:**
   - AI-powered email processing capabilities
   - Multiple AI model integrations (Qwen, Claude, Gemini, etc.)
   - Scientific approach to feature development

3. **Development Automation:**
   - Automated documentation synchronization (`auto_sync_docs.py`)
   - Merge planning tools (`merge_direction_plan.md`, `final_merge_approach.md`)
   - Feature tracking system (`scientific_branch_features.md`)

## Development Commands
- `cd src && pytest` - Run tests
- `ruff check .` - Run code linting
- `python launch.py` - Launch main application

## Current Status
The project follows a structured planning workflow with a focus on proper tracking and execution of development tasks. It includes multiple AI integration approaches and a systematic planning system for feature development.

## Files of Interest
- `PLANNING_WORKFLOW.md` - Complete planning workflow documentation
- `backlog/README.md` - Backlog system documentation
- `launch.py` - Main application entry point
- Various AI integration files (QWEN.md, CLAUDE.md, GEMINI.md, etc.)