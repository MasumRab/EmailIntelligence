# Sibling Worktrees Agent Files Analysis

## Overview

Analysis of agent files in sibling EmailIntelligence worktrees that are not available on the main repo (branch: `004-guided-workflow`).

## Worktree Summary

| Worktree | Branch | Remote | Agent Files Status |
|----------|--------|--------|-------------------|
| `EmailIntelligenceAider` | `orchestration-tools` | origin | Has IFLOW.md (full) |
| `EmailIntelligenceAuto` | `auto-sync-20260405` | origin | Has IFLOW.md (truncated), CRUSH.md (stub), LLXPRT.md (empty) |
| `EmailIntelligenceGem` | `consolidate/cli-unification` | origin | Has IFLOW.md (full), CRUSH.md (full), LLXPRT.md (full) |

---

## Files NOT in Main Repo (004-guided-workflow)

### 1. IFLOW.md — Iflow Cursor Integration Guide

**Status by Worktree:**

| Worktree | Lines | Content Type | Quality |
|----------|-------|--------------|---------|
| EmailIntelligenceAider | 104 | Full Iflow Cursor guide | ✅ Complete |
| EmailIntelligenceAuto | 41 | Truncated | ⚠️ Incomplete |
| EmailIntelligenceGem | 330 | Full iFlow CLI + project overview | ✅ Complete (best) |

**Content Summary (EmailIntelligenceGem version — most complete):**

```markdown
# EmailIntelligence - Unified Development Environment (iFlow Context)

## Project Overview
EmailIntelligence is a full-stack application for intelligent email analysis...
- Backend: Python 3.12+, FastAPI, NLTK, scikit-learn, PyTorch, Transformers
- Frontend: React (Vite), TypeScript
- NLP/AI: Custom NLP engine with sentiment, topic, intent, urgency analysis
- Database: SQLite (default)
- Deployment: Docker support, unified launcher script

## iFlow CLI Overview
iFlow CLI is an interactive command-line interface agent for software engineering tasks...

## Key Technologies
- Backend: Python 3.12+, FastAPI, NLTK, scikit-learn, PyTorch, Transformers
- Frontend: React (Vite), TypeScript
- NLP/AI: Hugging Face transformers
- Database: SQLite
- Workflow Engine: Node-based workflow system

## Project Structure
[Full directory tree with descriptions]

## Building and Running
[Quick start guide, launcher usage]

## AI Models Setup
[Model training and organization]

## Environment Configuration
[Environment variables, .env file]

## Development Conventions
[Code organization, Python/Frontend development, testing]

## iFlow CLI Core Mandates
### Conventions
- Rigorously adhere to existing project conventions
- Analyze surrounding code, tests, and configuration first
- Mimic code style, framework choices, naming conventions

### Libraries/Frameworks
- NEVER assume a library/framework is available without verifying
- Check imports, configuration files, or neighboring files

## iFlow CLI Task Management
[Todo system usage]

## Documented Development Sessions
- Session Tracking Directory: /backlog/sessions/
- Session File Naming: IFLOW-YYYYMMDD-XXX.md

## iFlow CLI Software Engineering Workflow
1. Understand → 2. Plan → 3. Implement → 4. Verify (Tests) → 5. Verify (Standards)

## iFlow CLI Tools Available
- read_file, write_file, replace, search_file_content, glob
- run_shell_command, todo_write/todo_read

## Advanced Features
[Node-based workflow engine, extension system, filtering, module system]

## Development Commands
[Python backend, TypeScript/React frontend]

## Code Style Guidelines
[Python, TypeScript/React]

## Critical Rules
- Avoid circular dependencies
- Never hard-code paths or expose secrets
- Use dependency injection over global state
- Check existing dependencies before adding new libraries
- Follow security best practices
```

**EmailIntelligenceAider version (104 lines):**
- Iflow Cursor-specific integration guide
- MCP Configuration for Task Master
- Iflow-specific features (inline AI, cursor-based workflows, smart context)
- Important differences from other agents
- Recommended model configuration
- Your role with Iflow Cursor
- Best practices

**Recommendation:** The EmailIntelligenceGem version (330 lines) is the most comprehensive, combining project overview with iFlow CLI specifics. Consider restoring this to main if iFlow is used.

---

### 2. CRUSH.md — Crush IDE Instructions

**Status by Worktree:**

| Worktree | Lines | Content Type | Quality |
|----------|-------|--------------|---------|
| EmailIntelligenceAuto | 5 | Stub only | ❌ Minimal |
| EmailIntelligenceGem | 52 | Full agent guidelines | ✅ Complete |

**Content Summary (EmailIntelligenceGem version — 52 lines):**

```markdown
# EmailIntelligence Agent Guidelines

## Build/Lint/Test Commands
### Python Backend
- Test all: pytest
- Test single file: pytest tests/test_file.py
- Test single function: pytest tests/test_file.py::TestClass::test_function
- Format: black .
- Lint: flake8 . && pylint python_backend src modules
- Type check: mypy .
- Dependency Update: python launch.py --update-deps

### TypeScript/React Frontend
- Build: npm run build (from client/)
- Lint: npm run lint (from client/)
- Dev server: npm run dev (from client/)

## Code Style Guidelines
### Python
- Formatting: Black (line length 100), isort (black profile)
- Naming: snake_case (functions/vars), CapWords (classes), UPPER_CASE (constants)
- Types: Type hints required for all parameters/returns
- Docstrings: Google-style for public functions/classes
- Error handling: Specific exceptions, meaningful messages, logging

### TypeScript/React
- Strict mode: Enabled (noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch)
- JSX: react-jsx transform
- Imports: @/ (client src), @shared/ (shared types)
- Components: PascalCase naming, default export functions
- Styling: Tailwind CSS
- API: Use client from lib/api.ts

## ⚠️ Critical Rules to Follow
- Rigorously adhere to existing project conventions
- Analyze surrounding code, tests, and configuration first
- Mimic code style, framework choices, naming conventions, typing, architectural patterns
- NEVER assume a library/framework is available without verifying
- Check imports, configuration files, or neighboring files
- Follow existing code style and structure strictly
- Use existing libraries and utilities
- Follow existing architectural patterns
- Understand local context to ensure changes integrate naturally
- Make changes that are idiomatic to the existing codebase
- Check existing dependencies before adding new libraries
- Follow security best practices

- No circular dependencies
- No hard-coded paths/secrets
- Strict typing (full annotations)
- Consistent naming conventions
- Security: Never expose or log sensitive data
- Global State: Use dependency injection over global state
```

**Recommendation:** The EmailIntelligenceGem version (52 lines) is a proper Tier 2 agent file with build/lint/test commands and code style guidelines. Consider restoring if Crush IDE is used.

---

### 3. LLXPRT.md — Llxprt Project Overview

**Status by Worktree:**

| Worktree | Lines | Content Type | Quality |
|----------|-------|--------------|---------|
| EmailIntelligenceAuto | 0 | Empty | ❌ Empty |
| EmailIntelligenceGem | 37 | Full project overview | ✅ Complete |

**Content Summary (EmailIntelligenceGem version — 37 lines):**

```markdown
# LLXPRT – EmailIntelligenceGem Project Overview

## Table of Contents
- Project Summary
- High‑Level Architecture
- Core Components
  - Python Backend (FastAPI)
  - Frontend (React + Vite)
  - Node‑Based Workflow Engine
  - AI/NLP Engine
  - Security Framework
  - Performance Monitoring
  - Extension System
- Data Storage
- Running the System (Local Development)
- Running the System (Production / Docker)
- Testing
- Coding Conventions & Project Layout
- Glossary & Terminology
- Open Questions & Future Work
- References & Further Reading

## Project Summary
EmailIntelligenceGem is a modular, extensible platform for intelligent email processing,
categorisation, sentiment analysis and workflow automation. It combines:
- FastAPI Python backend
- React/Vite frontend
- Node‑based workflow engine (inspired by ComfyUI/Stable Diffusion)
- AI/NLP models for natural‑language understanding

Key capabilities:
- Gmail API integration for real‑time email ingestion
- Rich, extensible workflow graphs
- Security‑by‑design (permissions, sanitisation, sandboxing, audit logging)
- Performance dashboard (CPU, memory, disk, model latency, error‑rate metrics)
- Extension system for plug‑and‑play functionality
- Gradio UI for scientific exploration and model debugging
```

**Recommendation:** The EmailIntelligenceGem version (37 lines) is a proper Tier 2 agent file with project overview. Consider restoring if Llxprt IDE is used.

---

## Files DIFFERING from Main Repo

### 1. AGENTS.md

| Worktree | Lines | Main Lines | Difference |
|----------|-------|------------|------------|
| EmailIntelligenceAider | 76 | 883 | -807 lines (truncated) |
| EmailIntelligenceAuto | 11 | 883 | -872 lines (severely truncated) |
| EmailIntelligenceGem | 910 | 883 | +27 lines (extended) |

**Observations:**
- EmailIntelligenceAider: Contains only build/lint/test commands and code style
- EmailIntelligenceAuto: Contains only research mode section (appears corrupted)
- EmailIntelligenceGem: Extended version with additional content

### 2. CLAUDE.md

| Worktree | Lines | Main Lines | Difference |
|----------|-------|------------|------------|
| EmailIntelligenceAider | 112 | 143 | -31 lines |
| EmailIntelligenceAuto | 0 | 143 | Empty file |
| EmailIntelligenceGem | — | 143 | Same as main |

**Observations:**
- EmailIntelligenceAider: Has MCP config but missing some sections
- EmailIntelligenceAuto: Empty file — needs restoration

### 3. GEMINI.md

| Worktree | Lines | Main Lines | Difference |
|----------|-------|------------|------------|
| EmailIntelligenceAuto | 329 | 353 | -24 lines |
| EmailIntelligenceGem | 288 | 353 | -65 lines |

**Observations:**
- Both contain Jules template content
- Main version has additional Gemini CLI instructions (lines 186-353)

---

## Summary Table

| File | Main | Aider | Auto | Gem | Best Source |
|------|------|-------|------|-----|-------------|
| IFLOW.md | ❌ Deleted | ✅ 104 lines | ⚠️ 41 lines | ✅ 330 lines | **Gem** |
| CRUSH.md | ❌ Gitignored | ❌ Missing | ⚠️ 5 lines | ✅ 52 lines | **Gem** |
| LLXPRT.md | ❌ Deleted | ❌ Missing | ❌ Empty | ✅ 37 lines | **Gem** |
| AGENTS.md | 883 lines | 76 lines | 11 lines | 910 lines | **Gem** (extended) |
| CLAUDE.md | 143 lines | 112 lines | 0 lines | Same | **Main** |
| GEMINI.md | 353 lines | Same | 329 lines | 288 lines | **Main** |

---

## Restoration Commands

If these files are needed on the main branch:

```bash
# From EmailIntelligenceGem (most complete versions)
cd ~/github/EmailIntelligence

# Restore IFLOW.md (full 330-line version)
cp ~/github/EmailIntelligenceGem/IFLOW.md ./IFLOW.md

# Restore CRUSH.md (full 52-line version)
cp ~/github/EmailIntelligenceGem/CRUSH.md ./CRUSH.md

# Restore LLXPRT.md (full 37-line version)
cp ~/github/EmailIntelligenceGem/LLXPRT.md ./LLXPRT.md
```

Or from specific branches:

```bash
# From orchestration-tools branch (for IFLOW.md 104-line version)
git show origin/orchestration-tools:IFLOW.md > IFLOW.md

# From consolidate/cli-unification branch (for all 3 files)
git show origin/consolidate/cli-unification:IFLOW.md > IFLOW.md
git show origin/consolidate/cli-unification:CRUSH.md > CRUSH.md
git show origin/consolidate/cli-unification:LLXPRT.md > LLXPRT.md
```

---

## Gitignore Status

From previous analysis, these files are gitignored on the main branch:

```
# .gitignore lines 230-234
CRUSH.md
LLXPRT.md
GEMINI.md
QWEN.md
```

However, IFLOW.md was **deleted** (commit 2b17d13a) not gitignored.

---

## Verification

```bash
# Check if files exist in sibling worktrees
ls -la ~/github/EmailIntelligence*/IFLOW.md
ls -la ~/github/EmailIntelligence*/CRUSH.md
ls -la ~/github/EmailIntelligence*/LLXPRT.md

# Check branch availability
git branch -r | grep -E "orchestration-tools|auto-sync|consolidate"
```

---

## Agents Archive

All agent files from all worktrees have been archived with versioning and git history:

```
~/github/agents/
├── EmailIntelligence/          # 68 files (branch: 004-guided-workflow)
├── EmailIntelligenceAider/     # 105 files (branch: orchestration-tools)
├── EmailIntelligenceAuto/      # 48 files (branch: auto-sync-20260405)
├── EmailIntelligenceGem/       # 59 files (branch: consolidate-cli-unification)
├── history/                    # 57 git history files with diffs
│   ├── EmailIntelligence/
│   ├── EmailIntelligenceAider/
│   ├── EmailIntelligenceAuto/
│   └── EmailIntelligenceGem/
└── README.md
```

**Naming convention:** `<name>__<branch>.<ext>`

**Usage:**
```bash
# Compare versions
diff ~/github/agents/EmailIntelligence/CLAUDE__004-guided-workflow.md \
     ~/github/agents/EmailIntelligenceAider/CLAUDE__orchestration-tools.md

# Restore from best source
cp ~/github/agents/EmailIntelligenceGem/IFLOW__consolidate-cli-unification.md ./IFLOW.md

# View git history
cat ~/github/agents/history/EmailIntelligenceGem/IFLOW_history.md
```

---

## Related Documentation

- `~/github/agents/README.md` — Agents archive structure and usage
- `~/github/agents/history/README.md` — Git history tracking format
- `docs/AGENT_RULES_GAP_ANALYSIS_AND_CONTENT_MAP.md` — Section 3.6 (Git history findings)
- `docs/AGENT_RULES_IMPLEMENTATION_HANDOFF.md` — Step 5.3a (Document deleted/gitignored agent files)
