# Speckit (Agent-Driven Workflow)

## Overview
This directory is reserved for Speckit logic. However, the native Python implementation has been deprecated in favor of an **LLM-Driven Agent Workflow**.

## Why Agent-Driven?
Complex developer context (like checking consistency between `spec.md`, `plan.md`, and `tasks.md`) requires the reasoning capabilities of a Large Language Model (LLM). Rigid Python scripts using keyword matching or naive NLP are insufficient for this purpose.

## Implementation Standard
If you need to use or extend Speckit features, you should use the following agent-anchored commands:
- `.gemini/commands/speckit.specify.toml`
- `.gemini/commands/speckit.plan.toml`
- `.gemini/commands/speckit.tasks.toml`
- `.gemini/commands/speckit.analyze.toml`

Native code in this directory should only be used for lightweight filesystem helpers used by these agent prompts (via `.specify/scripts/bash/`).
