# Documentation Guidance Map

This file provides an organized overview of all markdown documentation in the repository, helping you quickly find the right document for your needs.

---

## Quick Category Index

| Category | Description | Key Files |
|----------|-------------|-----------|
| [1. Project Overview](#1-project-overview) | Core project information | README.md, AGENTS.md |
| [2. Orchestration Tools](#2-orchestration-tools) | Git hooks, automation, branch management | ORCHESTRATION_*.md |
| [3. Task Management](#3-task-management) | Taskmaster, task workflows | TASKMASTER*.md, TASK_*.md |
| [4. AI Agent Instructions](#4-ai-agent-instructions) | Rules for AI coding tools | .github/instructions/*.md |
| [5. Git & Branch Management](#5-git--branch-management) | Merge guides, hook documentation | GIT_*.md, HOOK_*.md |
| [6. Session Notes](#6-session-notes) | Development session records | backlog/sessions/*.md |
| [7. Templates](#7-templates) | Reusable templates | .specify/templates/*.md |
| [8. Technical Analysis](#8-technical-analysis) | Architecture & research docs | *analysis*.md, *summary*.md |
| [9. IDE-Specific Rules](#9-ide-specific-rules) | VS Code, Windsurf, Cursor configs | .windsurf/, .cursor/, .amazonq/ |

---

## 1. Project Overview

Core documentation about the project structure, technology stack, and agent integration.

| File | Purpose |
|------|---------|
| `README.md` | Main project documentation, getting started, project structure |
| `AGENTS.md` | Task Master and agent integration guide, CLI commands |
| `technology_stack.md` | Overview of technologies used in the project |
| `key_modules.md` | Documentation for key modules in the codebase |
| `INSTALLATION.md` | Setup and installation instructions |

---

## 2. Orchestration Tools

Comprehensive documentation about the orchestration tools system including Git hooks, branch management, and automation scripts.

### Index & Guides
| File | Purpose |
|------|---------|
| `ORCHESTRATION_TOOLS_INDEX.md` | Master index for all orchestration documentation |
| `ORCHESTRATION_GUIDE.md` | Main orchestration usage guide |
| `ORCHESTRATION_PROCESS_GUIDE.md` | Process documentation for orchestration workflows |
| `ORCHESTRATION_SYNC_GUIDE.md` | Synchronization between branches |

### Implementation & Distribution
| File | Purpose |
|------|---------|
| `ORCHESTRATION_IMPLEMENTATION_SUMMARY.md` | Implementation details |
| `ORCHESTRATION_DISTRIBUTION_SYSTEM.md` | How orchestration tools are distributed |
| `ORCHESTRATION_TOOLS_CLUSTER_SUMMARY.md` | Clustering of orchestration tools |

### IDE Integration
| File | Purpose |
|------|---------|
| `ORCHESTRATION_IDE_QUICK_REFERENCE.md` | Quick reference for IDE integration |
| `ORCHESTRATION_IDE_DISTRIBUTION_PLAN.md` | IDE distribution plan |
| `ORCHESTRATION_IDE_INCLUSION_SUMMARY.md` | IDE inclusion summary |

### Control & Configuration
| File | Purpose |
|------|---------|
| `ORCHESTRATION_CONTROL_MODULE.md` | Control module documentation |
| `ORCHESTRATION_DISABLE_FLAG.md` | Disable flag configuration |
| `ORCHESTRATION_DISABLE_QUICK_REFERENCE.md` | Quick reference for disabling |

### Hooks & Fixes
| File | Purpose |
|------|---------|
| `ORCHESTRATION_HOOK_FIXES_SUMMARY.md` | Summary of hook fixes |
| `COMPLETE_HOOK_AND_BRANCH_FIXES.md` | Complete hook and branch fixes |

### Quick References
| File | Purpose |
|------|---------|
| `ORCHESTRATION_TOOLS_QUICK_REFERENCE.md` | Quick reference guide |

---

## 3. Task Management

Documentation about Taskmaster, task creation, and workflow management.

| File | Purpose |
|------|---------|
| `AGENTS.md` (section 2) | Task Master CLI and MCP tool reference |
| `TASKMASTER_SUBMODULE_INTEGRATION.md` | Taskmaster submodule setup |
| `TASK_CREATION_WORKFLOW.md` | How to create and manage tasks |
| `TASK_CREATION_QUICK_REF.md` | Quick reference for task creation |
| `TASK_VERIFICATION_REPORT.md` | Task verification process |

---

## 4. AI Agent Instructions

Rules and instructions for various AI coding tools. These files define how AI agents should behave when working on the project.

### GitHub Instructions (Primary)
| File | Purpose |
|------|---------|
| `.github/instructions/dev_workflow.instructions.md` | Development workflow for AI agents |
| `.github/instructions/taskmaster.instructions.md` | Taskmaster tool reference |
| `.github/instructions/self_improve.instructions.md` | Self-improvement rules for AI |
| `.github/instructions/vscode_rules.instructions.md` | VS Code specific rules |

### Tool-Specific Instructions
| File | Purpose |
|------|---------|
| `.github/instructions/GEMINI.instructions.md` | Gemini AI instructions |
| `.github/instructions/copilot-instructions.instructions.md` | GitHub Copilot instructions |

### Configuration
| File | Purpose |
|------|---------|
| `.github/copilot-instructions.md` | Copilot configuration |
| `.github/DOCUMENTATION_DISTRIBUTION_REPORT.md` | Documentation distribution |

---

## 5. Git & Branch Management

Documentation about Git workflows, merge strategies, and hook management.

### Merge & Branch Guides
| File | Purpose |
|------|---------|
| `GIT_MERGE_GUIDE.md` | Git merge procedures |
| `FINAL_MERGE_STRATEGY.md` | Final merge strategy documentation |
| `BRANCH_PROPAGATION_IMPLEMENTATION_SUMMARY.md` | Branch propagation details |

### Hooks & Blocking
| File | Purpose |
|------|---------|
| `HOOK_BLOCKING_SCENARIOS.md` | Scenarios where hooks block actions |
| `GIT_HOOKS_BLOCKING_SUMMARY.md` | Summary of hook blocking behavior |

### Stash Management
| File | Purpose |
|------|---------|
| `STASH_FIXES_COMPLETION.md` | Stash fixes completion status |
| `STASH_MANAGEMENT_ISSUES.md` | Stash management issues |

---

## 6. Session Notes

Development session records and achievements.

| File | Purpose |
|------|---------|
| `backlog/sessions/IFLOW.md` | IFLOW session documentation |
| `backlog/sessions/LLXPRT.md` | LLXPRT session documentation |
| `backlog/sessions/IFLOW-20251112-ACHIEVEMENTS.md` | Session achievements |
| `backlog/sessions/README.md` | Session documentation guide |

---

## 7. Templates

Reusable templates for various purposes.

### Specify Templates
| File | Purpose |
|------|---------|
| `.specify/templates/constitution-template.md` | Constitution template |
| `.specify/templates/plan-template.md` | Plan template |
| `.specify/templates/spec-template.md` | Specification template |
| `.specify/templates/checklist-template.md` | Checklist template |
| `.specify/templates/agent-file-template.md` | Agent file template |
| `.specify/templates/tasks-template.md` | Tasks template |

---

## 8. Technical Analysis

Architecture, research, and analysis documentation.

| File | Purpose |
|------|---------|
| `COMPREHENSIVE_ARCHITECTURE_ANALYSIS.md` | Full architecture analysis |
| `architecture_summary.md` | Architecture overview |
| `scientific_branch_analysis.md` | Scientific branch analysis |
| `orchestration_tools_branch_analysis.md` | Orchestration tools branch analysis |
| `actionable_insights.md` | Key insights and recommendations |

---

## 9. IDE-Specific Rules

Configuration files for various AI coding assistants and IDEs.

### Windsurf
| File | Purpose |
|------|---------|
| `.windsurf/rules/self_improve.md` | Self-improvement rules |
| `.windsurf/rules/windsurf_rules.md` | Windsurf specific rules |
| `.windsurf/rules/taskmaster.md` | Taskmaster integration |

### Cursor
| File | Purpose |
|------|---------|
| `.cursor/rules/` | Cursor-specific rules and configurations |

### Amazon Q
| File | Purpose |
|------|---------|
| `.amazonq/rules/memory-bank/tech.md` | Technical memory bank |
| `.amazonq/rules/memory-bank/product.md` | Product memory bank |
| `.amazonq/rules/memory-bank/structure.md` | Structure memory bank |
| `.amazonq/rules/memory-bank/guidelines.md` | Guidelines memory bank |

---

## 10. Development Standards & Guidelines

Code style guides, development standards, and best practices.

| File | Purpose |
|------|---------|
| `CODE_RECOMMENDATIONS.md` | Code recommendations and best practices |
| `docs/development/python_style_guide.md` | Python code style guide |
| `docs/development/backend_migration_guide.md` | Backend migration guide |
| `docs/development/server_development.md` | Server development guide |
| `docs/development/client_development.md` | Client development guide |
| `docs/development/quality_standards.md` | Quality standards |
| `docs/development/STATIC_ANALYSIS_REPORT.md` | Static analysis results |
| `docs/development/extensions_guide.md` | Extensions guide |
| `docs/development/markdown_style_guide.md` | Markdown style guide |
| `docs/development/env_management.md` | Environment management |

---

## 11. Troubleshooting & Known Issues

Problem-solving guides and known issue documentation.

| File | Purpose |
|------|---------|
| `TROUBLESHOOTING.md` | General troubleshooting guide |
| `DEPRECATED_WARNINGS_REFACTOR_CHECKLIST.md` | Deprecated warnings checklist |
| `CONTEXT_CONTAMINATION_PREVENTION.md` | Context contamination prevention |
| `docs/troubleshooting/dependency_management_guide.md` | Dependency troubleshooting |
| `docs/unimplemented_code_analysis.md` | Unimplemented code analysis |

---

## 12. Progress & Tracking

Progress tracking, dashboards, and todo management.

| File | Purpose |
|------|---------|
| `PROGRESS_DASHBOARD.md` | Progress dashboard |
| `OUTSTANDING_TODOS.md` | Outstanding todos |
| `PROGRESS_TRACKING.md` | Progress tracking |
| `PROGRESS_TRACKING_README.md` | Progress tracking guide |
| `IMPLEMENTATION_SUMMARY.md` | Implementation summary |
| `CLEANUP_SUMMARY.md` | Cleanup summary |
| `BLOCKER_ANALYSIS_INDEX.md` | Blocker analysis |
| `BRANCH_ANALYSIS_REPORT.md` | Branch analysis report |

---

## 13. CI/CD & Migration

CI/CD pipelines, migration guides, and implementation documentation.

| File | Purpose |
|------|---------|
| `CI_MIGRATION_ANALYSIS.md` | CI migration analysis |
| `CI_MIGRATION_IMPLEMENTATION.md` | CI migration implementation |
| `SUBTREE_TESTING_GUIDE.md` | Subtree testing guide |
| `HANDLING_INCOMPLETE_MIGRATIONS.md` | Migration issue handling |

---

## 14. Quick References & Cheat Sheets

Fast lookup guides and reference cards.

| File | Purpose |
|------|---------|
| `QWEN.md` | Qwen quick reference |
| `GEMINI.md` | Gemini quick reference |
| `AGENT_GUIDELINES_QUICK_REFERENCE.md` | Agent guidelines quick ref |
| `docs/cli_workflow_map.md` | CLI workflow map |
| `docs/analysis/QUICK_START.md` | Quick start guide |

---

## 15. Source of Truth Documentation

Authoritative documentation for specific domains.

### Orchestration Source
| File | Purpose |
|------|---------|
| `docs/source-of-truth/orchestration/ORCHESTRATION_TOOLS_ANALYSIS_SUMMARY.md` | Orchestration analysis |
| `docs/source-of-truth/orchestration/ORCHESTRATION_SYNC_GUIDE.md` | Sync guide |
| `docs/source-of-truth/orchestration/ORCHESTRATION_PROGRESS_SUMMARY.md` | Progress summary |
| `docs/source-of-truth/orchestration/GIT_HOOKS_BLOCKING_SUMMARY.md` | Hook summary |

### Branch Source
| File | Purpose |
|------|---------|
| `docs/source-of-truth/branch/TASK_CREATION_WORKFLOW.md` | Task workflow |
| `docs/source-of-truth/branch/TASK_CREATION_GUIDE.md` | Task guide |
| `docs/source-of-truth/branch/BRANCH_AGENT_GUIDELINES_SUMMARY.md` | Branch agent guidelines |
| `docs/source-of-truth/branch/BRANCH_PROPAGATION_IMPLEMENTATION_SUMMARY.md` | Branch propagation |

---

## 16. Deployment & Configuration

Deployment guides and configuration documentation.

| File | Purpose |
|------|---------|
| `docs/deployment/deployment_guide.md` | Deployment guide |
| `docs/deployment/launcher_guide.md` | Launcher guide |
| `docs/deployment/application_launch_hardening_strategy.md` | Launch hardening |
| `docs/deployment/CPU_ONLY_DEPLOYMENT_POLICY.md` | CPU-only policy |
| `CONFIG_ANALYSIS.md` | Configuration analysis |
| `CONFIG.md` | Configuration documentation |

---

## 17. Archives & Deprecated

Outdated documentation kept for historical reference.

| File | Purpose |
|------|---------|
| `docs/archive/completion-report.md` | Archived completion report |
| `docs/archive/launch-setup-fixes-summary.md` | Archived setup fixes |
| `docs/old_workflow_docs/*.md` | Old workflow documents |
| `constitution-update-prompt.md` | Old constitution updates |

---

## How to Use This Guide

1. **Find your category**: Use the Quick Category Index to identify which section contains the information you need
2. **Check the table**: Each section has a table of files with their purposes
3. **Read the file**: Navigate to the file to get detailed information

### Common Use Cases

| Need | Where to Look |
|------|---------------|
| "How do I get started?" | `README.md` |
| "How do orchestration tools work?" | Section 2: Orchestration Tools |
| "How do I use Taskmaster?" | `AGENTS.md` or `.github/instructions/taskmaster.instructions.md` |
| "How do I create tasks?" | `TASK_CREATION_WORKFLOW.md` |
| "What are the AI agent rules?" | Section 4: AI Agent Instructions |
| "How do I resolve merge issues?" | `GIT_MERGE_GUIDE.md` |
| "What templates are available?" | Section 7: Templates |
| "How do I deploy?" | Section 16: Deployment & Configuration |
| "What's the architecture?" | Section 8: Technical Analysis |
| "How do I troubleshoot?" | Section 11: Troubleshooting & Known Issues |

---

## Quick File Lookup

### For Setting Up the Project
- `INSTALLATION.md`
- `README.md`
- `docs/getting_started.md`
- `setup/README.md`

### For Working with Tasks
- `AGENTS.md`
- `TASK_CREATION_WORKFLOW.md`
- `TASKMASTER_SUBMODULE_INTEGRATION.md`

### For Git/Branch Issues
- `GIT_MERGE_GUIDE.md`
- `BRANCH_UPDATE_QUICK_START.md`
- `docs/interactive_stash_resolution.md`
- `HOOK_BLOCKING_SCENARIOS.md`

### For Orchestration Questions
- `ORCHESTRATION_TOOLS_INDEX.md`
- `ORCHESTRATION_GUIDE.md`
- `ORCHESTRATION_TOOLS_QUICK_REFERENCE.md`

### For Architecture Questions
- `architecture_summary.md`
- `COMPREHENSIVE_ARCHITECTURE_ANALYSIS.md`
- `technology_stack.md`

### For Development Standards
- `CODE_RECOMMENDATIONS.md`
- `docs/development/python_style_guide.md`

---

*Last updated: April 2026*
*Generated for EmailIntelligence project documentation*
*Total markdown files documented: 100+*
