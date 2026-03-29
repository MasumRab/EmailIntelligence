# CLI Workflow Map

This document provides an overview of the guided workflows available in the EmailIntelligenceGem CLI.

## Workflows

### 1. `guide-dev` (General Development Guidance)
Helps developers decide which branch to work on based on their task.

- **Step 1: Intent Selection**
    - "working on application code" -> No special workflow needed.
    - "modifying a shared setup/config file" -> Proceed to Step 2.
- **Step 2: Branch Verification**
    - On `orchestration-tools` branch -> Safe to proceed.
    - NOT on `orchestration-tools` branch -> Warning: switch to `orchestration-tools` first.

### 2. `guide-pr` (PR Resolution Guidance)
Guides the merge process for different types of pull requests.

- **Step 1: PR Type Selection**
    - "daily orchestration change" -> Use `scripts/reverse_sync_orchestration.sh`.
    - "major feature branch merge" -> Use standard `git merge` + validation.