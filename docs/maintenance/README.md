# Maintenance Runbooks

This directory contains specialized runbooks for repairing and maintaining critical infrastructure components of the EmailIntelligence project.

## Available Runbooks

- [Launcher Repair Runbook](launcher_repair_runbook.md) - Handling `setup/launch.py`, infrastructure core, and conflict resolution.
- [Scientific Subtree Repair Runbook](scientific_subtree_repair_runbook.md) - Managing Git subtree integration and synchronization for the `scientific` branch.
- [Taskmaster Repair Runbook](taskmaster_repair_runbook.md) - Troubleshooting the Task Master AI integration, database integrity, and MCP connectivity.

## General Maintenance Principles

1.  **Safety First:** Always create backups or work on a temporary branch before performing invasive repairs.
2.  **Validate Early:** Use the "Shield" or "Validation" sections in each runbook to verify script integrity before execution.
3.  **Local Context:** Respect developer-specific configurations (`*.env`, `launch-user.env`) and ensure they are not committed to the repository.
4.  **Consistency:** Follow the established patterns for imports and path management (the "Infrastructure Core") to prevent bootstrap paradoxes.
