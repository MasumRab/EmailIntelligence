# Guides Index (scientific)

How-to guides, tutorials, and feature documentation for the `scientific` branch.
The `scientific` branch is the **experimental** product track — see
[`.taskmaster/BRANCH_MANAGEMENT_MODEL.md`](.taskmaster/BRANCH_MANAGEMENT_MODEL.md)
for the branch workflow (never merge `main ↔ scientific`).

## Feature & Module Guides

- [AI Model Training Guide](ai_model_training_guide.md) — data prep and model training workflows
- [API Authentication](api_authentication.md) — auth mechanisms and tokens
- [Advanced Filtering System](advanced_filtering_system.md) — email filtering pipelines
- [Imbox Module](imbox_module.md) — email retrieval via Imbox
- [Email Retrieval Module](email_retrieval_module.md) — retrieval configuration
- [Notmuch Integration](notmuch_integration.md) — notmuch-backed mail indexing
- [Model Management Module](model_management_module.md) — trained model lifecycle
- [System Status Module](system_status_module.md) — status / health reporting
- [MFA Implementation](mfa_implementation.md) — multi-factor auth guidance
- [Plugin Management Module](plugin_management_module.md) — extension/plugin system
- [Actionable Insights](actionable_insights.md) — derived intelligence outputs

## Workflow & Process Guides

- [Getting Started](getting_started.md) — science-branch setup
- [Branch Switching Guide](branch_switching_guide.md) — moving between branches safely
- [Workflow Implementation Plan](workflow_implementation_plan.md) — workflow engine plan
- [Workflow Migration Plan](WORKFLOW_MIGRATION_PLAN.md) — migrating workflows between branches
- [Workflow & Review Process](workflow_and_review_process.md) — PR review gates and CI control
- [Module Analysis Prioritization](module_analysis_prioritization.md) — module backlog triage
- [Project Structure Comparison](project_structure_comparison.md) — `main` vs `scientific` layouts
- [Unimplemented Code Analysis](unimplemented_code_analysis.md) — known gaps
- [Changes Report](changes_report.md) — change log notes

## Planning & Reference

- [Developer Guide](CLAUDE.md) — agent/IDE reference for this subtree
- [Scientific Subtree Guide](SCIENTIFIC_SUBTREE_GUIDE.md) — what lives on `scientific`
- [Project Documentation Guide](project_documentation_guide.md) — how docs are organized
- [WORKFLOW_README](WORKFLOW_README-scientific.md) — scientific-specific runbook

> 📖 **Testing:** this branch's testing procedures are in [`docs/testing_guide.md`](../testing_guide.md).
