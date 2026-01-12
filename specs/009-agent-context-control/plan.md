# Implementation Plan: Agent Context Control

**Branch**: `009-agent-context-control` | **Date**: 2026-01-13 | **Spec**: ./spec.md

## 1. Goal
Implement a robust Context Control System that dynamically adjusts the AI agent's working context (prompts, rules, allowed tools) based on the active git branch.

## 2. Core Architecture
- **ContextDetector**: Analyzes git branch name and structure.
- **ContextProfile**: Data model for a set of rules/prompts.
- **ContextManager**: Orchestrates the loading/unloading of profiles.
- **Storage**: `.context-control/profiles/` (JSON/YAML definitions).

## 3. Implementation Strategy
- **Phase 1 (Core)**: Implement `ContextDetector` and `ContextProfile` models.
- **Phase 2 (Manager)**: Implement `ContextManager` logic to detect changes and swap profiles.
- **Phase 3 (Integration)**: Hook into the Agent's startup/loop to check context.

## 4. Testing Strategy
- **Unit Tests**: Test matching logic (regex branch matching).
- **Integration**: Simulate git branch switches and verify profile loaded.
