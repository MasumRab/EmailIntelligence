# Implementation Plan: Guided CLI Workflows

**Branch**: `004-guided-workflow` | **Date**: 2026-01-13 | **Spec**: ./spec.md

## 1. Goal
Implement interactive CLI guides (`guide-dev`, `guide-pr`) to help developers navigate the project's complex orchestration rules.

## 2. Core Architecture
- **WorkflowContextManager**: Maintains state (current step, user intent).
- **CLI**: `launch.py` commands.
- **Interaction**: Simple text prompts.

## 3. Implementation Strategy
- **Phase 1 (Core)**: `WorkflowContextManager` in `src/lib/`.
- **Phase 2 (Dev Guide)**: `guide-dev` command.
- **Phase 3 (PR Guide)**: `guide-pr` command.

## 4. Testing Strategy
- **Unit**: Test `WorkflowContextManager` transitions.
- **Integration**: Test CLI output/prompts.
