# Comprehensive Repository Analysis Report

## Part 1: Architectural Analysis

### Circular Dependencies

No circular dependencies found. Excellent!

### Module Coupling

#### Top 10 Most Depended-Upon Modules (Highest Afferent Coupling)
| Module | Imported By # Files |
|--------|---------------------|
| `src/core/factory.py` | 23 |
| `backend/node_engine/node_base.py` | 21 |
| `src/core/auth.py` | 15 |
| `backend/node_engine/workflow_engine.py` | 14 |
| `src/core/database.py` | 13 |
| `backend/node_engine/workflow_manager.py` | 10 |
| `backend/node_engine/email_nodes.py` | 9 |
| `backend/node_engine/security_manager.py` | 8 |
| `src/core/models.py` | 8 |
| `src/core/ai_engine.py` | 6 |

#### Top 10 Most Dependent Modules (Highest Efferent Coupling)
| Module | Imports # Files |
|--------|-----------------|
| `tests/core/test_factory.py` | 12 |
| `backend/python_backend/node_workflow_routes.py` | 11 |
| `tests/core/test_data_source.py` | 9 |
| `backend/python_backend/advanced_workflow_routes.py` | 8 |
| `backend/python_backend/workflow_routes.py` | 7 |
| `modules/categories/routes.py` | 7 |
| `modules/email/routes.py` | 7 |
| `backend/python_backend/dashboard_routes.py` | 6 |
| `backend/python_backend/tests/conftest.py` | 6 |
| `backend/node_engine/test_security.py` | 6 |

### Orphan Files (Potential Unused Code or Entrypoints)

Found 62 potential orphan files:
- `demo_mfa.py`
- `backend/plugins/email_visualizer_plugin.py`
- `backend/plugins/email_filter_node.py`
- `backend/extensions/example/example.py`
- `backend/python_backend/enhanced_routes.py`
- `backend/python_backend/workflow_editor_ui.py`
- `backend/python_backend/model_routes.py`
- `backend/python_backend/email_routes.py`
- `backend/python_backend/gradio_app.py`
- `backend/python_backend/filter_routes.py`
- `backend/python_backend/dashboard_routes.py`
- `backend/python_backend/advanced_workflow_routes.py`
- `backend/python_backend/category_routes.py`
- `backend/python_backend/workflow_routes.py`
- `backend/python_backend/node_workflow_routes.py`
- `backend/python_backend/routes/v1/email_routes.py`
- `backend/python_backend/routes/v1/category_routes.py`
- `backend/python_backend/services/base_service.py`
- `backend/python_backend/tests/test_training_routes.py`
- `backend/python_backend/tests/test_gmail_routes.py`
- `backend/python_backend/tests/test_filter_routes.py`
- `backend/python_backend/tests/conftest.py`
- `backend/python_backend/tests/test_database_optimizations.py`
- `backend/python_backend/tests/test_advanced_ai_engine.py`
- `backend/python_backend/tests/test_model_manager.py`
- `backend/python_nlp/gmail_integration.py`
- `backend/python_nlp/tests/test_nlp_engine.py`
- `backend/node_engine/test_nodes.py`
- `backend/node_engine/test_security.py`
- `backend/node_engine/test_integration.py`
- `backend/node_engine/test_migration.py`
- `backend/node_engine/test_sanitization.py`
- `tests/test_api_actions.py`
- `tests/test_auth.py`
- `tests/test_security_integration.py`
- `tests/test_workflow_engine.py`
- `tests/test_basic.py`
- `tests/test_database.py`
- `tests/test_mfa.py`
- `tests/test_password_hashing.py`
- `tests/test_prompt_engineer.py`
- `tests/test_launcher.py`
- `tests/test_filter_api.py`
- `tests/test_email_api.py`
- `tests/test_category_api.py`
- `tests/backend/node_engine/test_security_manager.py`
- `tests/core/test_advanced_workflow_engine.py`
- `tests/core/test_security.py`
- `tests/core/test_workflow_engine.py`
- `tests/core/test_factory.py`
- `tests/core/test_email_repository.py`
- `tests/core/test_data_source.py`
- `tests/core/test_caching.py`
- `tests/core/test_notmuch_data_source.py`
- `tests/modules/dashboard/test_dashboard.py`
- `tests/modules/default_ai_engine/test_modular_ai_engine.py`
- `modules/auth/routes.py`
- `modules/workflows/ui.py`
- `modules/categories/routes.py`
- `modules/email/routes.py`
- `modules/email_retrieval/email_retrieval_ui.py`
- `modules/notmuch/ui.py`

---

## Part 2: Detailed File Metrics

### Directory: `./`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .concurrent_reviews.json | 329 | 0 | 0 | 0 | Configuration |
| .flake8 | 4 | 0 | 0 | 0 | Other |
| .gitattributes | 0 | 0 | 0 | 0 | Other |
| .gitignore | 81 | 0 | 0 | 0 | Other |
| .maintenance_scheduler.json | 208 | 0 | 0 | 0 | Configuration |
| .pylintrc | 22 | 0 | 0 | 0 | Other |
| .voidrules | 0 | 0 | 0 | 0 | Other |
| AGENTS.md | 701 | 0 | 0 | 0 | Documentation |
| BRANCH_ANALYSIS_REPORT.md | 217 | 0 | 0 | 0 | Documentation |
| CLAUDE.md | 24 | 0 | 0 | 0 | Documentation |
| CODEREVIEW_REPORT.md | 95 | 0 | 0 | 0 | Documentation |
| CONTRIBUTING.md | 242 | 0 | 0 | 0 | Documentation |
| CPU_ONLY_DEPLOYMENT_POLICY.md | 195 | 0 | 0 | 0 | Documentation |
| CPU_SETUP.md | 131 | 0 | 0 | 0 | Documentation |
| CRUSH.md | 53 | 0 | 0 | 0 | Documentation |
| Dockerfile.prod | 41 | 0 | 0 | 0 | Containerization |
| GEMINI.md | 533 | 0 | 0 | 0 | Documentation |
| IFLOW.md | 331 | 0 | 0 | 0 | Documentation |
| JULES_WIP_ANALYSIS.md | 136 | 0 | 0 | 0 | Documentation |
| LLXPRT.md | 38 | 0 | 0 | 0 | Documentation |
| NVIDIA_DEPENDENCY_ANALYSIS_PLAN.md | 217 | 0 | 0 | 0 | Documentation |
| QWEN.md | 12 | 0 | 0 | 0 | Documentation |
| README.md | 599 | 0 | 0 | 0 | Documentation |
| SCIENTIFIC_BRANCH_ALIGNMENT_PLAN.md | 78 | 0 | 0 | 0 | Documentation |
| SCIENTIFIC_SUBTREE_GUIDE.md | 55 | 0 | 0 | 0 | Documentation |
| SECURITY.md | 70 | 0 | 0 | 0 | Documentation |
| SECURITY_INCIDENT_RESPONSE.md | 104 | 0 | 0 | 0 | Documentation |
| SESSION_LOG.md | 81 | 0 | 0 | 0 | Documentation |
| SETUP.md | 121 | 0 | 0 | 0 | Documentation |
| STATIC_ANALYSIS_REPORT.md | 74 | 0 | 0 | 0 | Documentation |
| SUBTREE_TESTING_GUIDE.md | 89 | 0 | 0 | 0 | Testing |
| SYSTEM_PACKAGES_README.md | 157 | 0 | 0 | 0 | Documentation |
| UNIFIED_ARCHITECTURAL_PLAN.md | 356 | 0 | 0 | 0 | Documentation |
| WORKFLOW_MIGRATION_PLAN.md | 271 | 0 | 0 | 0 | Documentation |
| WORKTREE_SETUP_INTEGRATION_GUIDE.md | 126 | 0 | 0 | 0 | Documentation |
| actionable_insights.md | 232 | 0 | 0 | 0 | Documentation |
| alignment-main-task-template.md | 100 | 0 | 0 | 0 | Documentation |
| alignment-task-template.md | 100 | 0 | 0 | 0 | Documentation |
| analyze_repo.py | 260 | 4 | 9 | 0 | Core Logic |
| architecture_summary.md | 139 | 0 | 0 | 0 | Documentation |
| backlog-merge-driver.sh | 90 | 0 | 0 | 0 | Scripting |
| backup.sh | 338 | 0 | 0 | 0 | Scripting |
| branch_alignment_report.md | 66 | 0 | 0 | 0 | Documentation |
| branch_management_recommendations.md | 71 | 0 | 0 | 0 | Documentation |
| clean_install.sh | 15 | 0 | 0 | 0 | Scripting |
| codebase_analysis.py | 490 | 8 | 14 | 1 | Core Logic |
| codebase_analysis_report.txt | 367 | 0 | 0 | 0 | Other |
| codebase_issues.json | 460 | 0 | 0 | 0 | Configuration |
| codebuff.json | 27 | 0 | 0 | 0 | Configuration |
| component_relationships.md | 190 | 0 | 0 | 0 | Documentation |
| components.json | 20 | 0 | 0 | 0 | Configuration |
| conftest.py | 6 | 2 | 0 | 0 | Testing |
| data_flow.md | 265 | 0 | 0 | 0 | Documentation |
| demo_mfa.py | 70 | 3 | 0 | 0 | Core Logic |
| deploy.sh | 239 | 0 | 0 | 0 | Scripting |
| detailed_analysis_summary.md | 110 | 0 | 0 | 0 | Documentation |
| development_markers_report.md | 104 | 0 | 0 | 0 | Documentation |
| diagnosis_message.txt | 26 | 0 | 0 | 0 | Other |
| docker-compose.prod.yml | 87 | 0 | 0 | 0 | Configuration |
| docker-compose.yml | 29 | 0 | 0 | 0 | Configuration |
| download_hf_models.py | 37 | 2 | 0 | 0 | Core Logic |
| drizzle.config.ts | 14 | 0 | 0 | 0 | Configuration |
| email_cache.db | 426 | 0 | 0 | 0 | Data |
| error_checking_prompt.py | 215 | 7 | 8 | 1 | Core Logic |
| error_detection_report.txt | 14 | 0 | 0 | 0 | Other |
| error_log.jsonl | 0 | 0 | 0 | 0 | Data |
| final_merge_approach.md | 185 | 0 | 0 | 0 | Documentation |
| functional_analysis_report.md | 119 | 0 | 0 | 0 | Documentation |
| generated-icon.png | 8927 | 0 | 0 | 0 | Asset |
| key_modules.md | 338 | 0 | 0 | 0 | Documentation |
| knowledge.md | 44 | 0 | 0 | 0 | Documentation |
| launch.bat | 13 | 0 | 0 | 0 | Scripting |
| launch.bat.new | 133 | 0 | 0 | 0 | Other |
| launch.py | 23 | 3 | 0 | 0 | Core Logic |
| launch.sh | 10 | 0 | 0 | 0 | Scripting |
| merge_direction_plan.md | 56 | 0 | 0 | 0 | Documentation |
| merge_phase_plan.md | 178 | 0 | 0 | 0 | Documentation |
| package-lock.json | 9055 | 0 | 0 | 0 | Configuration |
| package.json | 122 | 0 | 0 | 0 | Configuration |
| pyproject.toml | 77 | 0 | 0 | 0 | Configuration |
| refactoring_plan.md | 69 | 0 | 0 | 0 | Documentation |
| repository_analysis_report.md | 1746 | 0 | 0 | 0 | Documentation |
| requirements-dev.txt | 11 | 0 | 0 | 0 | Other |
| requirements.txt | 49 | 0 | 0 | 0 | Other |
| requirements_versions.txt | 20 | 0 | 0 | 0 | Other |
| rulesync.jsonc | 24 | 0 | 0 | 0 | Other |
| scientific_branch_features.md | 73 | 0 | 0 | 0 | Documentation |
| setup_linting.py | 158 | 3 | 3 | 0 | Core Logic |
| smart_filters.db | 48 | 0 | 0 | 0 | Data |
| sqlite.db | 0 | 0 | 0 | 0 | Data |
| subtree_integration_scientific.sh | 19 | 0 | 0 | 0 | Scripting |
| subtree_integration_scientific_branch.sh | 19 | 0 | 0 | 0 | Scripting |
| system_vs_pip_requirements.txt | 110 | 0 | 0 | 0 | Other |
| tailwind.config.ts | 90 | 0 | 0 | 0 | Configuration |
| task_verification_report.md | 110 | 0 | 0 | 0 | Documentation |
| technology_stack.md | 383 | 0 | 0 | 0 | Documentation |
| test-improvement-plan.md | 233 | 0 | 0 | 0 | Testing |
| test-migration-plan-updated.md | 100 | 0 | 0 | 0 | Testing |
| test-migration-plan.md | 100 | 0 | 0 | 0 | Testing |
| test-path-issues-plan.md | 247 | 0 | 0 | 0 | Testing |
| tools_used.md | 82 | 0 | 0 | 0 | Documentation |
| tsconfig.json | 24 | 0 | 0 | 0 | Configuration |
| uv.lock | 2411 | 0 | 0 | 0 | Other |
| validate_dependencies.py | 55 | 3 | 1 | 0 | Core Logic |
| verify_packages.py | 121 | 5 | 2 | 0 | Core Logic |
| vite.config.ts | 53 | 0 | 0 | 0 | Configuration |

### Directory: `.continue/models`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| new-model.yaml | 11 | 0 | 0 | 0 | Configuration |

### Directory: `.continue/prompts`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| new-prompt.yaml | 8 | 0 | 0 | 0 | Configuration |

### Directory: `.continue/rules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| new-rule.yaml | 5 | 0 | 0 | 0 | Configuration |

### Directory: `.github/workflows`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 61 | 0 | 0 | 0 | Documentation |
| ci.yml | 44 | 0 | 0 | 0 | Configuration |
| dependabot-auto-merge.yml | 54 | 0 | 0 | 0 | Configuration |
| deploy-staging.yml | 19 | 0 | 0 | 0 | Configuration |
| gemini-dispatch.yml | 204 | 0 | 0 | 0 | Configuration |
| gemini-invoke.yml | 238 | 0 | 0 | 0 | Configuration |
| gemini-review.yml | 271 | 0 | 0 | 0 | Configuration |
| gemini-scheduled-triage.yml | 307 | 0 | 0 | 0 | Configuration |
| gemini-triage.yml | 186 | 0 | 0 | 0 | Configuration |

### Directory: `.openhands/microagents`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| repo.md | 128 | 0 | 0 | 0 | Documentation |

### Directory: `.qwen`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| PROJECT_SUMMARY.md | 44 | 0 | 0 | 0 | Documentation |

### Directory: `analysis_reports`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .continue_models.md | 5 | 0 | 0 | 0 | Documentation |
| .continue_prompts.md | 5 | 0 | 0 | 0 | Documentation |
| .continue_rules.md | 5 | 0 | 0 | 0 | Documentation |
| .github_workflows.md | 13 | 0 | 0 | 0 | Documentation |
| .openhands_microagents.md | 5 | 0 | 0 | 0 | Documentation |
| .qwen.md | 5 | 0 | 0 | 0 | Documentation |

### Directory: `backend`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| db.ts | 14 | 0 | 0 | 0 | Frontend |
| email_cache.db | 15 | 0 | 0 | 0 | Data |

### Directory: `backend/data`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| categories.json | 38 | 0 | 0 | 0 | Configuration |
| categories.json.gz | 2 | 0 | 0 | 0 | Data |
| emails.json | 5 | 0 | 0 | 0 | Configuration |
| emails.json.gz | 2 | 0 | 0 | 0 | Data |
| settings.json | 3 | 0 | 0 | 0 | Configuration |
| users.json | 5 | 0 | 0 | 0 | Configuration |
| users.json.gz | 2 | 0 | 0 | 0 | Data |

### Directory: `backend/extensions`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 9 | 0 | 0 | 0 | Documentation |

### Directory: `backend/extensions/example`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 71 | 0 | 0 | 0 | Documentation |
| example.py | 111 | 4 | 5 | 0 | Core Logic |
| metadata.json | 17 | 0 | 0 | 0 | Configuration |
| requirements.txt | 7 | 0 | 0 | 0 | Other |

### Directory: `backend/node_engine`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| email_nodes.py | 678 | 5 | 8 | 9 | Core Logic |
| migration_utils.py | 363 | 8 | 14 | 3 | Core Logic |
| node_base.py | 353 | 6 | 28 | 7 | Core Logic |
| node_library.py | 271 | 3 | 11 | 1 | Core Logic |
| security_manager.py | 421 | 10 | 20 | 6 | Core Logic |
| test_integration.py | 393 | 10 | 0 | 0 | Testing |
| test_migration.py | 101 | 2 | 2 | 0 | Testing |
| test_nodes.py | 182 | 7 | 0 | 0 | Testing |
| test_sanitization.py | 72 | 4 | 1 | 0 | Testing |
| test_security.py | 253 | 8 | 0 | 0 | Testing |
| workflow_engine.py | 429 | 8 | 6 | 3 | Core Logic |
| workflow_manager.py | 324 | 7 | 9 | 1 | Core Logic |

### Directory: `backend/plugins`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 15 | 1 | 0 | 0 | Core Logic |
| base_plugin.py | 128 | 3 | 14 | 3 | Core Logic |
| email_filter_node.py | 103 | 2 | 8 | 1 | Core Logic |
| email_visualizer_plugin.py | 73 | 3 | 9 | 1 | Core Logic |
| plugin_manager.py | 172 | 7 | 11 | 1 | Core Logic |

### Directory: `backend/python_backend`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 56 | 0 | 0 | 0 | Documentation |
| __init__.py | 60 | 6 | 0 | 0 | Core Logic |
| advanced_workflow_routes.py | 310 | 16 | 1 | 5 | Core Logic |
| ai_engine.py | 192 | 6 | 6 | 2 | Core Logic |
| ai_routes.py | 159 | 6 | 0 | 0 | Core Logic |
| auth.py | 84 | 7 | 3 | 1 | Core Logic |
| category_data_manager.py | 116 | 10 | 3 | 1 | Core Logic |
| category_routes.py | 83 | 12 | 0 | 0 | Core Logic |
| config.py | 40 | 2 | 3 | 2 | Configuration |
| constants.py | 46 | 0 | 0 | 0 | Core Logic |
| dashboard_routes.py | 149 | 16 | 3 | 0 | Core Logic |
| database.py | 721 | 11 | 6 | 1 | Core Logic |
| dependencies.py | 234 | 19 | 6 | 0 | Core Logic |
| email_data_manager.py | 251 | 11 | 4 | 1 | Core Logic |
| email_routes.py | 175 | 16 | 0 | 0 | Core Logic |
| enhanced_routes.py | 199 | 10 | 0 | 4 | Core Logic |
| exceptions.py | 134 | 3 | 10 | 11 | Core Logic |
| filter_routes.py | 94 | 9 | 0 | 0 | Core Logic |
| gmail_routes.py | 240 | 12 | 0 | 0 | Core Logic |
| gradio_app.py | 226 | 11 | 5 | 0 | Core Logic |
| json_database.py | 661 | 11 | 6 | 1 | Core Logic |
| main.py | 385 | 38 | 0 | 1 | Core Logic |
| model_manager.py | 21 | 2 | 3 | 1 | Core Logic |
| model_routes.py | 64 | 6 | 0 | 0 | Core Logic |
| models.py | 533 | 4 | 1 | 61 | Core Logic |
| node_workflow_routes.py | 384 | 18 | 0 | 4 | Core Logic |
| performance_monitor.py | 360 | 10 | 19 | 3 | Core Logic |
| performance_routes.py | 37 | 4 | 0 | 0 | Core Logic |
| plugin_manager.py | 65 | 3 | 3 | 1 | Core Logic |
| run_server.py | 62 | 5 | 0 | 0 | Core Logic |
| settings.py | 74 | 5 | 1 | 2 | Core Logic |
| smart_filters.py | 2 | 0 | 0 | 1 | Core Logic |
| training_routes.py | 170 | 16 | 0 | 0 | Core Logic |
| utils.py | 63 | 3 | 1 | 0 | Core Logic |
| workflow_editor_ui.py | 327 | 7 | 6 | 0 | Core Logic |
| workflow_engine.py | 259 | 9 | 12 | 4 | Core Logic |
| workflow_manager.py | 162 | 7 | 11 | 2 | Core Logic |
| workflow_routes.py | 362 | 12 | 1 | 2 | Core Logic |

### Directory: `backend/python_backend/notebooks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| email_analysis.ipynb | 65 | 0 | 0 | 0 | Notebook |

### Directory: `backend/python_backend/routes/v1`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| category_routes.py | 86 | 10 | 0 | 0 | Core Logic |
| email_routes.py | 165 | 9 | 0 | 0 | Core Logic |

### Directory: `backend/python_backend/services`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| base_service.py | 45 | 5 | 1 | 2 | Core Logic |
| category_service.py | 90 | 3 | 1 | 1 | Core Logic |
| email_service.py | 187 | 5 | 1 | 1 | Core Logic |

### Directory: `backend/python_backend/tests`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conftest.py | 139 | 10 | 6 | 0 | Testing |
| test_advanced_ai_engine.py | 152 | 5 | 3 | 0 | Testing |
| test_category_routes.py | 47 | 1 | 4 | 0 | Testing |
| test_database_optimizations.py | 160 | 11 | 0 | 1 | Testing |
| test_email_routes.py | 212 | 3 | 12 | 1 | Testing |
| test_filter_routes.py | 87 | 3 | 4 | 0 | Testing |
| test_gmail_routes.py | 150 | 6 | 6 | 0 | Testing |
| test_model_manager.py | 111 | 5 | 7 | 0 | Testing |
| test_training_routes.py | 106 | 6 | 3 | 0 | Testing |
| test_workflow_routes.py | 85 | 2 | 3 | 0 | Testing |

### Directory: `backend/python_nlp`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| ai_training.py | 145 | 3 | 8 | 2 | Core Logic |
| data_strategy.py | 572 | 8 | 22 | 3 | Core Logic |
| gmail_integration.py | 614 | 23 | 15 | 5 | Core Logic |
| gmail_metadata.py | 514 | 7 | 23 | 2 | Core Logic |
| gmail_service.py | 451 | 14 | 8 | 1 | Core Logic |
| gmail_service.py.backup | 366 | 0 | 0 | 0 | Other |
| gmail_service.py.final | 366 | 0 | 0 | 0 | Other |
| gmail_service_clean.py | 366 | 14 | 8 | 1 | Core Logic |
| intent_model.pkl | 0 | 0 | 0 | 0 | Other |
| nlp_engine.py | 1271 | 21 | 36 | 1 | Core Logic |
| protocols.py | 28 | 4 | 0 | 2 | Core Logic |
| retrieval_monitor.py | 269 | 8 | 14 | 3 | Core Logic |
| sentiment_model.pkl | 0 | 0 | 0 | 0 | Other |
| smart_filters.py | 468 | 11 | 28 | 3 | Core Logic |
| smart_retrieval.py | 249 | 16 | 6 | 3 | Core Logic |
| text_utils.py | 31 | 2 | 1 | 0 | Core Logic |
| topic_model.pkl | 0 | 0 | 0 | 0 | Other |
| urgency_model.pkl | 0 | 0 | 0 | 0 | Other |

### Directory: `backend/python_nlp/analysis_components`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| importance_model.py | 28 | 0 | 2 | 1 | Core Logic |
| intent_model.py | 20 | 2 | 2 | 1 | Core Logic |
| sentiment_model.py | 36 | 2 | 2 | 1 | Core Logic |
| topic_model.py | 35 | 2 | 2 | 1 | Core Logic |
| urgency_model.py | 20 | 2 | 2 | 1 | Core Logic |

### Directory: `backend/python_nlp/tests`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_nlp_engine.py | 309 | 6 | 11 | 0 | Testing |

### Directory: `backend/tests`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| setup.ts | 21 | 0 | 0 | 0 | Testing |

### Directory: `backlog`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.yml | 14 | 0 | 0 | 0 | Configuration |

### Directory: `backlog/deferred`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-18 - Backend-Migration-to-src.md | 28 | 0 | 0 | 0 | Documentation |
| task-18.1 - Sub-task-Move-Backend-Files-to-src.md | 18 | 0 | 0 | 0 | Documentation |
| task-18.2 - Sub-task-Update-Imports-and-References.md | 18 | 0 | 0 | 0 | Documentation |
| task-18.3 - Sub-task-Update-Configuration-Files.md | 18 | 0 | 0 | 0 | Documentation |
| task-18.4 - Sub-task-Run-and-Fix-Tests.md | 18 | 0 | 0 | 0 | Testing |
| task-18.5 - Sub-task-Final-Cleanup.md | 18 | 0 | 0 | 0 | Documentation |
| task-main-1 - Production-Deployment-Setup.md | 27 | 0 | 0 | 0 | Documentation |
| task-main-2 - Security-Audit-and-Hardening.md | 30 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/sessions`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| IFLOW-20251031-001.md | 63 | 0 | 0 | 0 | Documentation |
| IFLOW-20251101-001.md | 73 | 0 | 0 | 0 | Documentation |
| IFLOW-20251104-001.md | 108 | 0 | 0 | 0 | Documentation |
| IFLOW.md | 274 | 0 | 0 | 0 | Documentation |
| LLXPRT.md | 0 | 0 | 0 | 0 | Documentation |
| README.md | 20 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| pr-template-notmuch-alignment.md | 55 | 0 | 0 | 0 | Documentation |
| task-126 - Security-Enhancements-Authentication-and-Authorization.md | 40 | 0 | 0 | 0 | Documentation |
| task-127 - Error-Handling-Standardization.md | 42 | 0 | 0 | 0 | Documentation |
| task-132 - AI-Engine-Modularization.md | 22 | 0 | 0 | 0 | Documentation |
| task-140 - AI-Model-Performance-Optimization.md | 22 | 0 | 0 | 0 | Documentation |
| task-141 - Input-Validation-Enhancements.md | 41 | 0 | 0 | 0 | Documentation |
| task-142 - Data-Protection-Enhancements.md | 41 | 0 | 0 | 0 | Documentation |
| task-epic-security-enhancement - Overall Security Enhancement.md | 14 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-notmuch-tagging-1-completed.md | 77 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/ai-nlp`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| algorithm_analysis.md | 39 | 0 | 0 | 0 | Documentation |
| task-10 - Code-Quality-Refactoring-Split-large-NLP-modules,-reduce-code-duplication,-and-break-down-high-complexity-functions.md | 38 | 0 | 0 | 0 | Documentation |
| task-10 - Global-State-Management-Refactoring.md | 41 | 0 | 0 | 0 | Documentation |
| task-100 - Task-4.3-Set-up-automated-fix-suggestions.md | 24 | 0 | 0 | 0 | Documentation |
| task-101 - Task-4.4-Add-validation-result-caching.md | 24 | 0 | 0 | 0 | Documentation |
| task-102 - Task-4.5-Create-validation-pipeline-with-early-failure-detection.md | 24 | 0 | 0 | 0 | Documentation |
| task-103 - EPIC-Performance-Monitoring-Track-agent-performance-in-real-time-for-optimization.md | 26 | 0 | 0 | 0 | Documentation |
| task-104 - Task-5.1-Implement-real-time-agent-performance-metrics.md | 24 | 0 | 0 | 0 | Documentation |
| task-105 - Task-5.2-Create-task-completion-rate-tracking.md | 24 | 0 | 0 | 0 | Documentation |
| task-106 - Task-5.3-Set-up-automated-bottleneck-detection.md | 24 | 0 | 0 | 0 | Documentation |
| task-107 - Task-5.4-Add-resource-utilization-monitoring.md | 24 | 0 | 0 | 0 | Documentation |
| task-108 - Task-5.5-Develop-completion-prediction-algorithms.md | 24 | 0 | 0 | 0 | Documentation |
| task-109 - EPIC-Agent-Workflow-Templates-Develop-templates-for-agents-to-generate-documentation-in-parallel.md | 26 | 0 | 0 | 0 | Documentation |
| task-132 - AI-Engine-Modularization.md | 39 | 0 | 0 | 0 | Documentation |
| task-14 - Implement-PromptEngineer-class-for-LLM-interaction-or-update-README.md | 55 | 0 | 0 | 0 | Documentation |
| task-140 - AI-Model-Performance-Optimization.md | 39 | 0 | 0 | 0 | Documentation |
| task-15 - AI-Model-Performance-Optimization.md | 41 | 0 | 0 | 0 | Documentation |
| task-15 - Enhance-Extensions-Guide-with-detailed-Extension-API-documentation.md | 39 | 0 | 0 | 0 | Documentation |
| task-16 - Create-AI-Model-Training-Guide.md | 40 | 0 | 0 | 0 | Documentation |
| task-16 - Input-Validation-Enhancements.md | 41 | 0 | 0 | 0 | Documentation |
| task-30 - Implement-AdvancedAIEngine-in-email_nodes.py-or-ensure-proper-removal.md | 20 | 0 | 0 | 0 | Documentation |
| task-40 - Implement-AdvancedAIEngine-functionality.md | 32 | 0 | 0 | 0 | Documentation |
| task-46 - Implement-analyze_email-in-AI-Engine-protocols.md | 32 | 0 | 0 | 0 | Documentation |
| task-high.1 - Implement-Dynamic-AI-Model-Management-System.md | 45 | 0 | 0 | 0 | Documentation |
| task-medium.2 - Implement-AI-Lab-Interface-for-Scientific-Exploration.md | 42 | 0 | 0 | 0 | Documentation |
| update-ai-nlp-architecture.md | 72 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/alignment`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| align-large-branches-strategy.md | 83 | 0 | 0 | 0 | Documentation |
| branch-alignment-summary.md | 61 | 0 | 0 | 0 | Documentation |
| complete-branch-alignment.md | 84 | 0 | 0 | 0 | Documentation |
| create-merge-validation-framework.md | 72 | 0 | 0 | 0 | Documentation |
| task-1 - Resolve-merge-conflicts-in-PR-#133.md | 66 | 0 | 0 | 0 | Documentation |
| task-1000 - Align-feature-branches-with-scientific.md | 67 | 0 | 0 | 0 | Documentation |
| task-121 - Implement-Git-Subtree-Pull-Process-for-Scientific-Branch.md | 46 | 0 | 0 | 0 | Documentation |
| task-123 - Integrate-Setup-Subtree-in-Scientific-Branch.md | 49 | 0 | 0 | 0 | Documentation |
| task-124 - Test-and-Validate-Subtree-Integration-on-Both-Branches.md | 51 | 0 | 0 | 0 | Testing |
| task-73 - Update-Alignment-Strategy-Address-Technical-Debt-in-Scientific-Branch-While-Preserving-Improvements.md | 64 | 0 | 0 | 0 | Documentation |
| task-73 - Update-Alignment-Strategy-Scientific-Branch-Contains-Most-Improvements.md | 52 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-backlog-ac-updates-main.md | 100 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-backlog-ac-updates.md | 100 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-docs-cleanup.md | 100 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-import-error-corrections-main.md | 100 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-import-error-corrections.md | 100 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-merge-clean.md | 100 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-merge-setup-improvements.md | 100 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-notmuch-tagging-1.md | 116 | 0 | 0 | 0 | Documentation |
| task-feature-branch-alignment-search-in-category.md | 100 | 0 | 0 | 0 | Documentation |
| task-implement-subtree-pull-scientific.md | 45 | 0 | 0 | 0 | Documentation |
| task-integrate-setup-subtree-scientific.md | 52 | 0 | 0 | 0 | Documentation |
| task-test-validate-subtree-integration.md | 60 | 0 | 0 | 0 | Testing |
| update-setup-subtree-integration.md | 70 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/architecture-refactoring`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| architecture_review.md | 131 | 0 | 0 | 0 | Documentation |
| create-refactor-pr.md | 72 | 0 | 0 | 0 | Documentation |
| task-10 - Code-Quality-Refactoring-Split-large-NLP-modules,-reduce-code-duplication,-and-break-down-high-complexity-functions.md | 38 | 0 | 0 | 0 | Documentation |
| task-116 - Dependency-Management-Improvements.md | 57 | 0 | 0 | 0 | Documentation |
| task-130 - Repository-Pattern-Enhancement.md | 39 | 0 | 0 | 0 | Documentation |
| task-131 - Module-System-Improvements.md | 39 | 0 | 0 | 0 | Documentation |
| task-135 - Global-State-Management-Refactoring.md | 39 | 0 | 0 | 0 | Documentation |
| task-136 - Legacy-Code-Migration-Plan.md | 39 | 0 | 0 | 0 | Documentation |
| task-143 - Dependency-Management-Improvements.md | 39 | 0 | 0 | 0 | Documentation |
| task-144 - Code-Organization-Improvements.md | 39 | 0 | 0 | 0 | Documentation |
| task-147 - Implement-node-reconstruction-in-advanced_workflow_routes.py-or-ensure-proper-removal.md | 22 | 0 | 0 | 0 | Documentation |
| task-148 - Implement-'name'-property-for-BasePlugin-subclasses.md | 31 | 0 | 0 | 0 | Documentation |
| task-23 - Implement-cleanup-logic-in-dependencies.py-or-ensure-proper-removal.md | 20 | 0 | 0 | 0 | Documentation |
| task-24 - Implement-CategoryCreate-model-fields-in-models.py-or-ensure-proper-removal.md | 20 | 0 | 0 | 0 | Documentation |
| task-25 - Implement-custom-event-registration-in-email_visualizer_plugin.py-or-ensure-proper-removal.md | 22 | 0 | 0 | 0 | Documentation |
| task-26 - Implement-name-property-in-base_plugin.py-or-ensure-proper-removal.md | 20 | 0 | 0 | 0 | Documentation |
| task-27 - Handle-ImportError-in-example.py-explicitly-or-ensure-proper-removal.md | 20 | 0 | 0 | 0 | Documentation |
| task-28 - Implement-get_all_categories-in-protocols.py-subclasses-or-ensure-proper-removal.md | 22 | 0 | 0 | 0 | Documentation |
| task-29 - Define-WorkflowExecutionException-in-workflow_engine.py-or-ensure-proper-removal.md | 22 | 0 | 0 | 0 | Documentation |
| task-31 - Implement-execute-method-in-node_base.py-subclasses-or-ensure-proper-removal.md | 20 | 0 | 0 | 0 | Documentation |
| task-32 - Implement-workflow-node-reconstruction-logic.md | 48 | 0 | 0 | 0 | Documentation |
| task-33 - Implement-cleanup-logic-in-dependencies.py.md | 30 | 0 | 0 | 0 | Documentation |
| task-34 - Implement-CategoryCreate-model-fields.md | 30 | 0 | 0 | 0 | Documentation |
| task-37 - Refine-ImportError-handling-in-example-extension.md | 31 | 0 | 0 | 0 | Documentation |
| task-38 - Implement-get_all_categories-in-NLP-protocols.md | 31 | 0 | 0 | 0 | Documentation |
| task-39 - Implement-WorkflowExecutionException-details.md | 31 | 0 | 0 | 0 | Documentation |
| task-41 - Implement-execute-method-for-NodeBase-subclasses.md | 24 | 0 | 0 | 0 | Documentation |
| task-43 - Implement-'version'-property-for-BasePlugin-subclasses.md | 31 | 0 | 0 | 0 | Documentation |
| task-44 - Implement-'initialize'-method-for-BasePlugin-subclasses.md | 31 | 0 | 0 | 0 | Documentation |
| task-45 - Implement-'process'-method-for-BasePlugin-subclasses.md | 31 | 0 | 0 | 0 | Documentation |
| task-56 - Audit-Phase-3-tasks-and-move-AI-enhancement-tasks-to-scientific-branch.md | 32 | 0 | 0 | 0 | Documentation |
| task-57 - Document-architectural-improvements-in-feature-branch-for-scientific-branch-adoption.md | 32 | 0 | 0 | 0 | Documentation |
| task-6 - Phase-1-Feature-Integration-Integrate-NetworkX-graph-operations,-security-context,-and-performance-monitoring-into-Node-Engine.md | 54 | 0 | 0 | 0 | Documentation |
| task-7 - Phase-2-Import-Consolidation-Update-all-imports-to-use-Node-Engine-as-primary-workflow-system.md | 38 | 0 | 0 | 0 | Documentation |
| task-999 - Implement-ActivityCreate-model-fields.md | 30 | 0 | 0 | 0 | Documentation |
| task-architecture-improvement.md | 53 | 0 | 0 | 0 | Documentation |
| task-database-refactoring.md | 66 | 0 | 0 | 0 | Documentation |
| task-high.2 - Implement-Plugin-Manager-System.md | 45 | 0 | 0 | 0 | Documentation |
| task-high.4 - Refactor-global-state-management-to-use-dependency-injection.md | 18 | 0 | 0 | 0 | Documentation |
| task-high.5 - Refactor-to-eliminate-global-state-and-singleton-pattern.md | 18 | 0 | 0 | 0 | Documentation |
| task-high.6 - Remove-hidden-side-effects-from-initialization.md | 18 | 0 | 0 | 0 | Documentation |
| task-workflow-enhancement.md | 66 | 0 | 0 | 0 | Documentation |
| update-module-system-architecture.md | 70 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/dashboard/phase1`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-26 - Phase-1.1-Analyze-current-DataSource-interface-and-identify-required-aggregation-methods-for-dashboard-statistics.md | 39 | 0 | 0 | 0 | Documentation |
| task-28 - Phase-1.2-Add-get_dashboard_aggregates()-method-to-DataSource-for-efficient-server-side-calculations.md | 34 | 0 | 0 | 0 | Documentation |
| task-29 - Phase-1.3-Add-get_category_breakdown(limit)-method-to-DataSource-for-efficient-category-statistics.md | 35 | 0 | 0 | 0 | Documentation |
| task-30 - Phase-1.4-Merge-DashboardStats-models-from-both-implementations-into-comprehensive-ConsolidatedDashboardStats.md | 35 | 0 | 0 | 0 | Documentation |
| task-31 - Phase-1.5-Update-modules-dashboard-routes.py-to-use-new-DataSource-aggregation-methods.md | 35 | 0 | 0 | 0 | Documentation |
| task-32 - Phase-1.6-Add-authentication-support-to-dashboard-routes-using-get_current_active_user-dependency.md | 36 | 0 | 0 | 0 | Documentation |
| task-33 - Phase-1.7-Implement-time_saved-calculation-logic-(2-minutes-per-auto-labeled-email)-in-dashboard-routes.md | 35 | 0 | 0 | 0 | Documentation |
| task-34 - Phase-1.8-Update-performance-metrics-calculation-to-work-with-new-aggregated-data-approach.md | 36 | 0 | 0 | 0 | Documentation |
| task-35 - Phase-1.9-Update-modules-dashboard-__init__.py-registration-to-handle-authentication-dependencies-properly.md | 35 | 0 | 0 | 0 | Documentation |
| task-37 - Phase-1.11-Add-integration-tests-to-verify-dashboard-works-with-both-modular-and-legacy-data-sources.md | 29 | 0 | 0 | 0 | Testing |
| task-38 - Phase-1.12-Update-API-documentation-to-reflect-new-consolidated-DashboardStats-response-model.md | 29 | 0 | 0 | 0 | Documentation |
| task-39 - Phase-1.13-Add-deprecation-warnings-and-migration-guide-for-legacy-dashboard-routes.md | 29 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/dashboard/phase2`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-40 - Phase-2.1-Implement-Redis-memory-caching-for-dashboard-statistics-to-reduce-database-load-and-improve-response-times.md | 54 | 0 | 0 | 0 | Documentation |
| task-41 - Phase-2.2-Add-background-job-processing-for-heavy-dashboard-calculations-(weekly-growth,-performance-metrics-aggregation).md | 63 | 0 | 0 | 0 | Documentation |
| task-42 - Phase-2.3-Optimize-category-breakdown-queries-with-database-indexing-and-query-optimization-for-large-email-datasets.md | 30 | 0 | 0 | 0 | Documentation |
| task-43 - Phase-2.4-Implement-WebSocket-support-for-real-time-dashboard-updates-and-live-metrics-streaming.md | 30 | 0 | 0 | 0 | Documentation |
| task-44 - Phase-2.5-Add-dashboard-personalization-features-user-preferences,-custom-layouts,-and-saved-views.md | 30 | 0 | 0 | 0 | Documentation |
| task-45 - Phase-2.6-Implement-dashboard-export-functionality-(CSV,-PDF,-JSON)-for-statistics-and-reports.md | 30 | 0 | 0 | 0 | Documentation |
| task-46 - Phase-2.7-Create-modular-dashboard-widgets-system-for-reusable-dashboard-components.md | 30 | 0 | 0 | 0 | Documentation |
| task-47 - Phase-2.8-Add-historical-trend-analysis-with-time-series-data-visualization-and-forecasting.md | 30 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/dashboard/phase3`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-48 - Phase-3.1-Implement-AI-insights-engine-with-ML-based-recommendations-for-email-management-optimization.md | 30 | 0 | 0 | 0 | Documentation |
| task-49 - Phase-3.2-Add-predictive-analytics-for-email-volume-forecasting-and-categorization-trend-prediction.md | 30 | 0 | 0 | 0 | Documentation |
| task-50 - Phase-3.3-Create-advanced-interactive-visualizations-with-charts,-graphs,-and-drill-down-capabilities.md | 30 | 0 | 0 | 0 | Documentation |
| task-51 - Phase-3.4-Implement-automated-alerting-system-for-dashboard-notifications-and-threshold-based-alerts.md | 31 | 0 | 0 | 0 | Documentation |
| task-52 - Phase-3.5-Implement-A-B-testing-framework-for-dashboard-feature-experimentation-and-analytics.md | 31 | 0 | 0 | 0 | Testing |
| task-53 - Phase-3.6-Implement-multi-tenant-dashboard-support-with-isolated-instances-and-data-segregation.md | 32 | 0 | 0 | 0 | Documentation |
| task-54 - Phase-3.7-Create-comprehensive-dashboard-API-for-programmatic-access-and-third-party-integrations.md | 32 | 0 | 0 | 0 | Documentation |
| task-55 - Phase-3.8-Implement-advanced-reporting-system-with-scheduled-reports-and-analytics-exports.md | 32 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/dashboard/phase4`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-58 - Phase-4.1-Implement-dashboard-clustering-and-load-balancing-for-high-traffic-enterprise-deployments.md | 28 | 0 | 0 | 0 | Documentation |
| task-59 - Phase-4.2-Add-enterprise-security-features-including-SSO,-comprehensive-audit-logs,-and-compliance-reporting.md | 28 | 0 | 0 | 0 | Documentation |
| task-60 - Phase-4.3-Create-dashboard-marketplace-for-custom-widget-ecosystem-and-third-party-extensions.md | 28 | 0 | 0 | 0 | Documentation |
| task-61 - Phase-4.4-Add-global-localization-support-with-multi-language-interface-and-timezone-handling.md | 28 | 0 | 0 | 0 | Documentation |
| task-62 - Phase-4.5-Implement-dashboard-governance-with-access-controls,-approval-workflows,-and-policy-management.md | 28 | 0 | 0 | 0 | Documentation |
| task-63 - Phase-4.6-Add-disaster-recovery-capabilities-with-automated-backups-and-failover-for-dashboard-data.md | 28 | 0 | 0 | 0 | Documentation |
| task-64 - Phase-4.7-Create-dashboard-analytics-to-track-usage-metrics,-performance-insights,-and-optimization-opportunities.md | 28 | 0 | 0 | 0 | Documentation |
| task-65 - Phase-4.8-Implement-API-rate-limiting-and-throttling-to-prevent-abuse-and-ensure-fair-usage.md | 28 | 0 | 0 | 0 | Documentation |
| task-66 - Phase-4.9-Add-comprehensive-monitoring-and-observability-with-distributed-tracing-and-performance-metrics.md | 28 | 0 | 0 | 0 | Documentation |
| task-67 - Phase-4.10-Implement-auto-scaling-capabilities-for-dashboard-infrastructure-based-on-usage-patterns.md | 28 | 0 | 0 | 0 | Documentation |
| task-68 - Phase-4.11-Create-enterprise-integration-hub-for-connecting-with-existing-business-systems-and-workflows.md | 28 | 0 | 0 | 0 | Documentation |
| task-69 - Phase-4.12-Add-compliance-automation-for-GDPR,-HIPAA,-and-other-regulatory-requirements.md | 28 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/database-data`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| address-database-technical-debt.md | 71 | 0 | 0 | 0 | Documentation |
| task-139 - Database-Performance-Optimization.md | 39 | 0 | 0 | 0 | Documentation |
| task-145 - Data-Layer-Improvements.md | 39 | 0 | 0 | 0 | Documentation |
| task-146 - Complete-DatabaseManager-Class-Implementation.md | 51 | 0 | 0 | 0 | Documentation |
| task-18 - Implement-EmailRepository-Interface.md | 24 | 0 | 0 | 0 | Documentation |
| task-21 - Implement-EmailRepository-Interface-on-Main.md | 55 | 0 | 0 | 0 | Documentation |
| task-3 - Implement-SOLID-Email-Data-Source-Abstraction.md | 79 | 0 | 0 | 0 | Documentation |
| task-70 - Complete-Repository-Pattern-Integration-with-Dashboard-Statistics.md | 43 | 0 | 0 | 0 | Documentation |
| task-71 - Align-NotmuchDataSource-Implementation-with-Functional-Requirements.md | 54 | 0 | 0 | 0 | Documentation |
| task-72 - Complete-Database-Dependency-Injection-Alignment.md | 55 | 0 | 0 | 0 | Documentation |
| task-database-refactoring.md | 66 | 0 | 0 | 0 | Documentation |
| task-medium.6 - Make-data-directory-configurable-via-environment-variables-or-settings.md | 18 | 0 | 0 | 0 | Documentation |
| task-medium.7 - Implement-proper-dependency-injection-for-database-manager-instance.md | 18 | 0 | 0 | 0 | Documentation |
| task-medium.8 - Implement-lazy-loading-strategy-that-is-more-predictable-and-testable.md | 18 | 0 | 0 | 0 | Testing |

### Directory: `backlog/tasks/deployment-ci-cd`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-115 - Migrate-documentation-system-to-distributed-worktree-framework.md | 24 | 0 | 0 | 0 | Documentation |
| task-115.1 - Phase-1-Foundation-&-Assessment.md | 25 | 0 | 0 | 0 | Documentation |
| task-115.2 - Phase-2-Parallel-Development.md | 26 | 0 | 0 | 0 | Documentation |
| task-115.3 - Phase-3-Gradual-Rollout.md | 26 | 0 | 0 | 0 | Documentation |
| task-115.4 - Phase-4-Transition-&-Optimization.md | 26 | 0 | 0 | 0 | Documentation |
| task-115.5 - Phase-5-Validation-&-Go-Live.md | 26 | 0 | 0 | 0 | Documentation |
| task-12 - Application-Monitoring-and-Observability.md | 48 | 0 | 0 | 0 | Documentation |
| task-12 - Production-Readiness-&-Deployment-Implement-monitoring,-deployment-configs,-performance-testing,-and-security-audit.md | 80 | 0 | 0 | 0 | Testing |
| task-137 - Application-Monitoring-and-Observability.md | 46 | 0 | 0 | 0 | Documentation |
| task-138 - CI-CD-Pipeline-Implementation.md | 44 | 0 | 0 | 0 | Documentation |
| task-28 - Phase-1.2-Add-get_dashboard_aggregates()-method-to-DataSource-for-efficient-server-side-calculations.md | 34 | 0 | 0 | 0 | Documentation |
| task-29 - Phase-1.3-Add-get_category_breakdown(limit)-method-to-DataSource-for-efficient-category-statistics.md | 35 | 0 | 0 | 0 | Documentation |
| task-42 - Rebase-scientific-branch-onto-main-after-core-enhancements-merge.md | 26 | 0 | 0 | 0 | Documentation |
| task-56 - Audit-Phase-3-tasks-and-move-AI-enhancement-tasks-to-scientific-branch.md | 32 | 0 | 0 | 0 | Documentation |
| task-57 - Document-architectural-improvements-in-feature-branch-for-scientific-branch-adoption.md | 32 | 0 | 0 | 0 | Documentation |
| task-58 - Phase-4.1-Implement-dashboard-clustering-and-load-balancing-for-high-traffic-enterprise-deployments.md | 27 | 0 | 0 | 0 | Documentation |
| task-66 - Phase-4.9-Add-comprehensive-monitoring-and-observability-with-distributed-tracing-and-performance-metrics.md | 27 | 0 | 0 | 0 | Documentation |
| task-82 - Task-1.3-Set-up-automated-load-balancing.md | 24 | 0 | 0 | 0 | Documentation |
| task-89 - Task-2.4-Set-up-automated-agent-health-monitoring.md | 24 | 0 | 0 | 0 | Documentation |
| task-91 - EPIC-Synchronization-Pipeline-Create-efficient-sync-system-that-only-transfers-changed-content.md | 26 | 0 | 0 | 0 | Documentation |
| task-medium.1 - Implement-Scientific-UI-System-Status-Dashboard.md | 42 | 0 | 0 | 0 | Documentation |
| task-medium.2 - Implement-AI-Lab-Interface-for-Scientific-Exploration.md | 42 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/dev-environment`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create-launch-script-fixes-pr.md | 71 | 0 | 0 | 0 | Documentation |
| task-133 - Development-Environment-Enhancements.md | 39 | 0 | 0 | 0 | Documentation |
| task-2 - Fix-launch-bat-issues.md | 43 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/documentation`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create-docs-improvements-pr.md | 72 | 0 | 0 | 0 | Documentation |
| task-128 - Documentation-Improvement-for-Onboarding.md | 40 | 0 | 0 | 0 | Documentation |
| task-15 - Enhance-Extensions-Guide-with-detailed-Extension-API-documentation.md | 39 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/other`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| algorithm_analysis.md | 39 | 0 | 0 | 0 | Documentation |
| create-async-fixes-pr.md | 71 | 0 | 0 | 0 | Documentation |
| create-docs-improvements-pr.md | 72 | 0 | 0 | 0 | Documentation |
| create-focused-prs.md | 71 | 0 | 0 | 0 | Documentation |
| create-import-fixes-pr.md | 71 | 0 | 0 | 0 | Documentation |
| create-launch-script-fixes-pr.md | 71 | 0 | 0 | 0 | Documentation |
| filtering-system-outstanding-tasks.md | 99 | 0 | 0 | 0 | Documentation |
| post-merge-validation.md | 64 | 0 | 0 | 0 | Documentation |
| task-11 - Legacy-Code-Migration-Plan.md | 41 | 0 | 0 | 0 | Documentation |
| task-110 - Task-6.1-Create-parallel-documentation-generation-templates.md | 24 | 0 | 0 | 0 | Documentation |
| task-111 - Task-6.2-Implement-concurrent-review-workflows.md | 24 | 0 | 0 | 0 | Documentation |
| task-112 - Task-6.3-Develop-distributed-translation-pipelines.md | 24 | 0 | 0 | 0 | Documentation |
| task-113 - Task-6.4-Set-up-automated-maintenance-task-scheduling.md | 24 | 0 | 0 | 0 | Documentation |
| task-114 - Task-6.5-Create-agent-onboarding-and-training-guides.md | 24 | 0 | 0 | 0 | Documentation |
| task-117 - Test-Branch-Task-Migration.md | 23 | 0 | 0 | 0 | Testing |
| task-118 - Test-Branch-Task-Migration-Copy.md | 23 | 0 | 0 | 0 | Testing |
| task-129 - Performance-Optimization-Caching-Strategy.md | 39 | 0 | 0 | 0 | Documentation |
| task-13 - CI-CD-Pipeline-Implementation.md | 46 | 0 | 0 | 0 | Documentation |
| task-13 - Implement-api-dashboard-stats-endpoint.md | 65 | 0 | 0 | 0 | Documentation |
| task-14 - Database-Performance-Optimization.md | 41 | 0 | 0 | 0 | Documentation |
| task-14 - Implement-PromptEngineer-class-for-LLM-interaction-or-update-README.md | 55 | 0 | 0 | 0 | Documentation |
| task-17 - Data-Protection-Enhancements.md | 41 | 0 | 0 | 0 | Documentation |
| task-18 - Dependency-Management-Improvements.md | 41 | 0 | 0 | 0 | Documentation |
| task-18 - Implement-EmailRepository-Interface.md | 24 | 0 | 0 | 0 | Documentation |
| task-19 - Code-Organization-Improvements.md | 41 | 0 | 0 | 0 | Documentation |
| task-2 - Error-Handling-Standardization.md | 42 | 0 | 0 | 0 | Documentation |
| task-2 - Fix-launch-bat-issues.md | 43 | 0 | 0 | 0 | Documentation |
| task-20 - Data-Layer-Improvements.md | 41 | 0 | 0 | 0 | Documentation |
| task-21 - Complete-DatabaseManager-Class-Implementation.md | 51 | 0 | 0 | 0 | Documentation |
| task-21 - Implement-EmailRepository-Interface-on-Main.md | 55 | 0 | 0 | 0 | Documentation |
| task-22 - Create-Task-Verification-Framework.md | 91 | 0 | 0 | 0 | Documentation |
| task-26 - Documentation-Improvement-Initiative-Phase-1-Planning-&-Prioritization.md | 24 | 0 | 0 | 0 | Documentation |
| task-26 - Phase-1.1-Analyze-current-DataSource-interface-and-identify-required-aggregation-methods-for-dashboard-statistics.md | 39 | 0 | 0 | 0 | Documentation |
| task-27 - System-Status-Module-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-28 - Model-Management-Module-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-29 - Plugin-Management-Module-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-3 - Documentation-Improvement-for-Onboarding.md | 42 | 0 | 0 | 0 | Documentation |
| task-3 - Implement-SOLID-Email-Data-Source-Abstraction.md | 79 | 0 | 0 | 0 | Documentation |
| task-30 - Email-Retrieval-Module-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-30 - Phase-1.4-Merge-DashboardStats-models-from-both-implementations-into-comprehensive-ConsolidatedDashboardStats.md | 35 | 0 | 0 | 0 | Documentation |
| task-31 - Notmuch-Integration-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-31 - Phase-1.5-Update-modules-dashboard-routes.py-to-use-new-DataSource-aggregation-methods.md | 35 | 0 | 0 | 0 | Documentation |
| task-32 - IMAP-Box-Management-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-33 - Documentation-Enhancement-&-Quality-Assurance.md | 25 | 0 | 0 | 0 | Documentation |
| task-33 - Phase-1.7-Implement-time_saved-calculation-logic-(2-minutes-per-auto-labeled-email)-in-dashboard-routes.md | 35 | 0 | 0 | 0 | Documentation |
| task-34 - Documentation-Integration-&-Maintenance-Setup.md | 25 | 0 | 0 | 0 | Documentation |
| task-34 - Phase-1.8-Update-performance-metrics-calculation-to-work-with-new-aggregated-data-approach.md | 36 | 0 | 0 | 0 | Documentation |
| task-38 - Phase-1.12-Update-API-documentation-to-reflect-new-consolidated-DashboardStats-response-model.md | 29 | 0 | 0 | 0 | Documentation |
| task-39 - Phase-1.13-Add-deprecation-warnings-and-migration-guide-for-legacy-dashboard-routes.md | 29 | 0 | 0 | 0 | Documentation |
| task-4 - Performance-Optimization-Caching-Strategy.md | 41 | 0 | 0 | 0 | Documentation |
| task-40 - Phase-2.1-Implement-Redis-memory-caching-for-dashboard-statistics-to-reduce-database-load-and-improve-response-times.md | 30 | 0 | 0 | 0 | Documentation |
| task-41 - Phase-2.2-Add-background-job-processing-for-heavy-dashboard-calculations-(weekly-growth,-performance-metrics-aggregation).md | 30 | 0 | 0 | 0 | Documentation |
| task-42 - Phase-2.3-Optimize-category-breakdown-queries-with-database-indexing-and-query-optimization-for-large-email-datasets.md | 30 | 0 | 0 | 0 | Documentation |
| task-43 - Phase-2.4-Implement-WebSocket-support-for-real-time-dashboard-updates-and-live-metrics-streaming.md | 30 | 0 | 0 | 0 | Documentation |
| task-44 - Phase-2.5-Add-dashboard-personalization-features-user-preferences,-custom-layouts,-and-saved-views.md | 30 | 0 | 0 | 0 | Documentation |
| task-45 - Phase-2.6-Implement-dashboard-export-functionality-(CSV,-PDF,-JSON)-for-statistics-and-reports.md | 30 | 0 | 0 | 0 | Documentation |
| task-46 - Phase-2.7-Create-modular-dashboard-widgets-system-for-reusable-dashboard-components.md | 30 | 0 | 0 | 0 | Documentation |
| task-47 - Phase-2.8-Add-historical-trend-analysis-with-time-series-data-visualization-and-forecasting.md | 30 | 0 | 0 | 0 | Documentation |
| task-48 - Phase-3.1-Implement-AI-insights-engine-with-ML-based-recommendations-for-email-management-optimization.md | 29 | 0 | 0 | 0 | Documentation |
| task-49 - Phase-3.2-Add-predictive-analytics-for-email-volume-forecasting-and-categorization-trend-prediction.md | 29 | 0 | 0 | 0 | Documentation |
| task-5 - Repository-Pattern-Enhancement.md | 41 | 0 | 0 | 0 | Documentation |
| task-5 - Secure-SQLite-database-paths-to-prevent-path-traversal.md | 66 | 0 | 0 | 0 | Documentation |
| task-50 - Phase-3.3-Create-advanced-interactive-visualizations-with-charts,-graphs,-and-drill-down-capabilities.md | 29 | 0 | 0 | 0 | Documentation |
| task-51 - Phase-3.4-Implement-automated-alerting-system-for-dashboard-notifications-and-threshold-based-alerts.md | 30 | 0 | 0 | 0 | Documentation |
| task-53 - Phase-3.6-Implement-multi-tenant-dashboard-support-with-isolated-instances-and-data-segregation.md | 31 | 0 | 0 | 0 | Documentation |
| task-54 - Phase-3.7-Create-comprehensive-dashboard-API-for-programmatic-access-and-third-party-integrations.md | 31 | 0 | 0 | 0 | Documentation |
| task-55 - Phase-3.8-Implement-advanced-reporting-system-with-scheduled-reports-and-analytics-exports.md | 31 | 0 | 0 | 0 | Documentation |
| task-6 - Module-System-Improvements.md | 41 | 0 | 0 | 0 | Documentation |
| task-60 - Phase-4.3-Create-dashboard-marketplace-for-custom-widget-ecosystem-and-third-party-extensions.md | 27 | 0 | 0 | 0 | Documentation |
| task-61 - Phase-4.4-Add-global-localization-support-with-multi-language-interface-and-timezone-handling.md | 27 | 0 | 0 | 0 | Documentation |
| task-62 - Phase-4.5-Implement-dashboard-governance-with-access-controls,-approval-workflows,-and-policy-management.md | 27 | 0 | 0 | 0 | Documentation |
| task-63 - Phase-4.6-Add-disaster-recovery-capabilities-with-automated-backups-and-failover-for-dashboard-data.md | 27 | 0 | 0 | 0 | Documentation |
| task-64 - Phase-4.7-Create-dashboard-analytics-to-track-usage-metrics,-performance-insights,-and-optimization-opportunities.md | 27 | 0 | 0 | 0 | Documentation |
| task-65 - Phase-4.8-Implement-API-rate-limiting-and-throttling-to-prevent-abuse-and-ensure-fair-usage.md | 27 | 0 | 0 | 0 | Documentation |
| task-67 - Phase-4.10-Implement-auto-scaling-capabilities-for-dashboard-infrastructure-based-on-usage-patterns.md | 27 | 0 | 0 | 0 | Documentation |
| task-68 - Phase-4.11-Create-enterprise-integration-hub-for-connecting-with-existing-business-systems-and-workflows.md | 27 | 0 | 0 | 0 | Documentation |
| task-69 - Phase-4.12-Add-compliance-automation-for-GDPR,-HIPAA,-and-other-regulatory-requirements.md | 27 | 0 | 0 | 0 | Documentation |
| task-7 - AI-Engine-Modularization.md | 41 | 0 | 0 | 0 | Documentation |
| task-7 - Phase-2-Import-Consolidation-Update-all-imports-to-use-Node-Engine-as-primary-workflow-system.md | 38 | 0 | 0 | 0 | Documentation |
| task-70 - Complete-Repository-Pattern-Integration-with-Dashboard-Statistics.md | 43 | 0 | 0 | 0 | Documentation |
| task-71 - Align-NotmuchDataSource-Implementation-with-Functional-Requirements.md | 44 | 0 | 0 | 0 | Documentation |
| task-72 - Complete-Database-Dependency-Injection-Alignment.md | 46 | 0 | 0 | 0 | Documentation |
| task-79 - EPIC-Parallel-Task-Infrastructure-Break-large-documentation-tasks-into-micro-tasks-completable-in-15-minutes-for-better-parallel-utilization.md | 26 | 0 | 0 | 0 | Documentation |
| task-8 - Development-Environment-Enhancements.md | 41 | 0 | 0 | 0 | Documentation |
| task-80 - Task-1.1-Implement-micro-task-decomposition-system.md | 24 | 0 | 0 | 0 | Documentation |
| task-81 - Task-1.2-Create-independent-task-queues-with-smart-routing.md | 24 | 0 | 0 | 0 | Documentation |
| task-83 - Task-1.4-Implement-real-time-completion-tracking.md | 24 | 0 | 0 | 0 | Documentation |
| task-84 - Task-1.5-Add-automated-error-recovery.md | 24 | 0 | 0 | 0 | Documentation |
| task-85 - EPIC-Agent-Coordination-Engine-Replace-polling-with-event-driven-system-for-immediate-task-assignment.md | 26 | 0 | 0 | 0 | Documentation |
| task-86 - Task-2.1-Design-event-driven-task-assignment.md | 24 | 0 | 0 | 0 | Documentation |
| task-87 - Task-2.2-Implement-agent-capability-registry.md | 24 | 0 | 0 | 0 | Documentation |
| task-88 - Task-2.3-Create-predictive-completion-time-estimation.md | 24 | 0 | 0 | 0 | Documentation |
| task-9 - UI-Enhancement-Implement-JavaScript-based-visual-workflow-editor-with-drag-and-drop-functionality.md | 32 | 0 | 0 | 0 | Documentation |
| task-90 - Task-2.5-Develop-task-dependency-resolution.md | 24 | 0 | 0 | 0 | Documentation |
| task-92 - Task-3.1-Implement-incremental-sync-with-change-detection.md | 24 | 0 | 0 | 0 | Documentation |
| task-93 - Task-3.2-Create-parallel-sync-workers.md | 24 | 0 | 0 | 0 | Documentation |
| task-94 - Task-3.3-Set-up-conflict-prediction-and-pre-resolution.md | 24 | 0 | 0 | 0 | Documentation |
| task-95 - Task-3.4-Add-atomic-commit-groups.md | 24 | 0 | 0 | 0 | Documentation |
| task-96 - Task-3.5-Implement-sync-prioritization.md | 24 | 0 | 0 | 0 | Documentation |
| task-97 - EPIC-Quality-Assurance-Automation-Implement-multiple-validation-processes-running-simultaneously.md | 26 | 0 | 0 | 0 | Documentation |
| task-98 - Task-4.1-Create-parallel-validation-workers.md | 24 | 0 | 0 | 0 | Documentation |
| task-99 - Task-4.2-Implement-incremental-validation.md | 24 | 0 | 0 | 0 | Documentation |
| task-dashboard - Overall Dashboard Enhancement Initiative.md | 66 | 0 | 0 | 0 | Documentation |
| task-high.1 - Implement-Dynamic-AI-Model-Management-System.md | 45 | 0 | 0 | 0 | Documentation |
| task-high.2 - Implement-Plugin-Manager-System.md | 45 | 0 | 0 | 0 | Documentation |
| task-medium.3 - Implement-Gmail-Performance-Metrics-API.md | 42 | 0 | 0 | 0 | Documentation |
| task-medium.4 - Implement-Gmail-Integration-UI-Tab.md | 42 | 0 | 0 | 0 | Documentation |
| task-medium.5 - Standardize-Dependency-Management-System.md | 44 | 0 | 0 | 0 | Documentation |
| task-workflow-enhancement.md | 66 | 0 | 0 | 0 | Documentation |
| todo_analysis.md | 164 | 0 | 0 | 0 | Documentation |
| todo_consolidation_strategy.md | 162 | 0 | 0 | 0 | Documentation |
| todo_organization_summary.md | 113 | 0 | 0 | 0 | Documentation |
| verify-and-merge-prs.md | 81 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/security`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| address-node-engine-security.md | 72 | 0 | 0 | 0 | Documentation |
| create-security-fixes-pr.md | 70 | 0 | 0 | 0 | Documentation |
| extract-security-fixes.md | 72 | 0 | 0 | 0 | Documentation |
| task-1 - Security-Enhancements-Authentication-and-Authorization.md | 40 | 0 | 0 | 0 | Documentation |
| task-12.1 - Complete-Security-Audit-and-Hardening.md | 34 | 0 | 0 | 0 | Documentation |
| task-126 - Security-Enhancements-Authentication-and-Authorization.md | 38 | 0 | 0 | 0 | Documentation |
| task-141 - Input-Validation-Enhancements.md | 39 | 0 | 0 | 0 | Documentation |
| task-142 - Data-Protection-Enhancements.md | 39 | 0 | 0 | 0 | Documentation |
| task-17 - Implement-proper-API-authentication-for-sensitive-operations.md | 65 | 0 | 0 | 0 | Documentation |
| task-32 - Phase-1.6-Add-authentication-support-to-dashboard-routes-using-get_current_active_user-dependency.md | 36 | 0 | 0 | 0 | Documentation |
| task-35 - Phase-1.9-Update-modules-dashboard-__init__.py-registration-to-handle-authentication-dependencies-properly.md | 35 | 0 | 0 | 0 | Documentation |
| task-5 - Secure-SQLite-database-paths-to-prevent-path-traversal.md | 66 | 0 | 0 | 0 | Documentation |
| task-59 - Phase-4.2-Add-enterprise-security-features-including-SSO,-comprehensive-audit-logs,-and-compliance-reporting.md | 27 | 0 | 0 | 0 | Documentation |
| task-6 - Phase-1-Feature-Integration-Integrate-NetworkX-graph-operations,-security-context,-and-performance-monitoring-into-Node-Engine.md | 54 | 0 | 0 | 0 | Documentation |
| task-8 - Security-&-Performance-Hardening-Enhance-security-validation,-audit-logging,-rate-limiting,-and-performance-monitoring.md | 83 | 0 | 0 | 0 | Documentation |
| task-high.3 - Implement-Advanced-Workflow-Security-Framework.md | 33 | 0 | 0 | 0 | Documentation |
| task-main-15 - Security-Enhancement.md | 56 | 0 | 0 | 0 | Documentation |
| task-security-enhancement.md | 67 | 0 | 0 | 0 | Documentation |
| update-security-architecture.md | 72 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/tasks/testing`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-11 - Testing-&-Documentation-Completion-Achieve-95%+-test-coverage-and-complete-comprehensive-documentation.md | 102 | 0 | 0 | 0 | Testing |
| task-12 - Production-Readiness-&-Deployment-Implement-monitoring,-deployment-configs,-performance-testing,-and-security-audit.md | 80 | 0 | 0 | 0 | Testing |
| task-134 - Advanced-Testing-Infrastructure.md | 39 | 0 | 0 | 0 | Testing |
| task-19 - Create-Abstraction-Layer-Tests.md | 37 | 0 | 0 | 0 | Testing |
| task-20 - Create-Notmuch-Tests-for-Scientific.md | 37 | 0 | 0 | 0 | Testing |
| task-21 - Create-Abstraction-Layer-Tests-on-Main.md | 58 | 0 | 0 | 0 | Testing |
| task-22 - Create-Task-Verification-Framework.md | 91 | 0 | 0 | 0 | Testing |
| task-36 - Phase-1.10-Update-test_dashboard.py-to-test-consolidated-functionality-with-new-response-model-and-authentication.md | 30 | 0 | 0 | 0 | Testing |
| task-37 - Phase-1.11-Add-integration-tests-to-verify-dashboard-works-with-both-modular-and-legacy-data-sources.md | 29 | 0 | 0 | 0 | Testing |
| task-4 - Fix-test-suite-issues.md | 42 | 0 | 0 | 0 | Testing |
| task-52 - Phase-3.5-Implement-A-B-testing-framework-for-dashboard-feature-experimentation-and-analytics.md | 30 | 0 | 0 | 0 | Testing |
| task-9 - Advanced-Testing-Infrastructure.md | 41 | 0 | 0 | 0 | Testing |
| task-testing-improvement.md | 59 | 0 | 0 | 0 | Testing |

### Directory: `backlog/tasks/ui-frontend`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-35 - Implement-custom-Gradio-events-for-EmailVisualizerPlugin.md | 31 | 0 | 0 | 0 | Documentation |
| task-9 - UI-Enhancement-Implement-JavaScript-based-visual-workflow-editor-with-drag-and-drop-functionality.md | 32 | 0 | 0 | 0 | Documentation |
| task-medium.1 - Implement-Scientific-UI-System-Status-Dashboard.md | 42 | 0 | 0 | 0 | Documentation |
| task-medium.4 - Implement-Gmail-Integration-UI-Tab.md | 42 | 0 | 0 | 0 | Documentation |
| update-ui-components-architecture.md | 72 | 0 | 0 | 0 | Documentation |

### Directory: `client`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| 100 | 0 | 0 | 0 | 0 | Other |
| index.html | 13 | 0 | 0 | 0 | Frontend |
| package-lock.json | 6263 | 0 | 0 | 0 | Configuration |
| package.json | 78 | 0 | 0 | 0 | Configuration |
| postcss.config.js | 6 | 0 | 0 | 0 | Configuration |
| tsconfig.json | 32 | 0 | 0 | 0 | Configuration |
| tsconfig.node.json | 12 | 0 | 0 | 0 | Configuration |

### Directory: `client/logs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| client.log | 1 | 0 | 0 | 0 | Other |

### Directory: `client/src`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| App.tsx | 18 | 0 | 0 | 0 | Frontend |
| main.tsx | 10 | 0 | 0 | 0 | Frontend |

### Directory: `client/src/components`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| advanced-filter-panel.tsx | 451 | 0 | 0 | 0 | Frontend |
| ai-analysis-panel.tsx | 452 | 0 | 0 | 0 | Frontend |
| email-list.tsx | 175 | 0 | 0 | 0 | Frontend |
| sidebar.tsx | 157 | 0 | 0 | 0 | Frontend |

### Directory: `client/src/components/auth`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| login-form.tsx | 118 | 0 | 0 | 0 | Frontend |
| mfa-disable.tsx | 34 | 0 | 0 | 0 | Frontend |
| mfa-setup.tsx | 98 | 0 | 0 | 0 | Frontend |
| user-profile.tsx | 59 | 0 | 0 | 0 | Frontend |

### Directory: `client/src/hooks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| use-auth.ts | 161 | 0 | 0 | 0 | Frontend |

### Directory: `client/src/pages`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dashboard.tsx | 234 | 0 | 0 | 0 | Frontend |
| login.tsx | 15 | 0 | 0 | 0 | Frontend |
| profile.tsx | 15 | 0 | 0 | 0 | Frontend |

### Directory: `config`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 24 | 0 | 0 | 0 | Documentation |
| llm_guidelines.json | 9 | 0 | 0 | 0 | Configuration |
| llm_guidelines.local.json.sample | 9 | 0 | 0 | 0 | Configuration |
| llm_guidelines.opencode.json | 16 | 0 | 0 | 0 | Configuration |
| llm_guidelines.qwen.json | 10 | 0 | 0 | 0 | Configuration |
| llm_guidelines.scientific.json | 21 | 0 | 0 | 0 | Configuration |

### Directory: `data`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| categories.json.gz | 2 | 0 | 0 | 0 | Data |
| emails.json.gz | 2 | 0 | 0 | 0 | Data |
| sender_labels.json | 0 | 0 | 0 | 0 | Configuration |
| settings.json | 3 | 0 | 0 | 0 | Configuration |
| users.json.gz | 2 | 0 | 0 | 0 | Data |

### Directory: `data/email_content`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| 1.json.gz | 2 | 0 | 0 | 0 | Data |

### Directory: `data/workflows`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| my_custom_workflow.json | 8 | 0 | 0 | 0 | Configuration |

### Directory: `deployment`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Dockerfile.backend | 36 | 0 | 0 | 0 | Containerization |
| Dockerfile.frontend | 31 | 0 | 0 | 0 | Containerization |
| README.md | 98 | 0 | 0 | 0 | Documentation |
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| data_migration.py | 576 | 10 | 9 | 0 | Core Logic |
| deploy.py | 48 | 4 | 2 | 0 | Core Logic |
| docker-compose.dev.yml | 16 | 0 | 0 | 0 | Configuration |
| docker-compose.prod.yml | 13 | 0 | 0 | 0 | Configuration |
| docker-compose.stag.yml | 67 | 0 | 0 | 0 | Configuration |
| docker-compose.yml | 25 | 0 | 0 | 0 | Configuration |
| migrate.py | 114 | 7 | 6 | 0 | Core Logic |
| setup_env.py | 185 | 7 | 7 | 0 | Core Logic |
| test_stages.py | 101 | 4 | 7 | 1 | Testing |

### Directory: `deployment/nginx`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| nginx.conf | 18 | 0 | 0 | 0 | Other |

### Directory: `docs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .branch-config.json | 18 | 0 | 0 | 0 | Configuration |
| .gitkeep | 0 | 0 | 0 | 0 | Documentation |
| .merge-history.json | 1 | 0 | 0 | 0 | Configuration |
| .review-queue.json | 94 | 0 | 0 | 0 | Configuration |
| API_REFERENCE.md | 32 | 0 | 0 | 0 | Documentation |
| BRANCH_NAMING_STANDARDIZATION.md | 30 | 0 | 0 | 0 | Documentation |
| BRANCH_OWNERSHIP_GUIDE.md | 30 | 0 | 0 | 0 | Documentation |
| DASHBOARD_CONSOLIDATION_REPORT.md | 30 | 0 | 0 | 0 | Documentation |
| DEVELOPER_GUIDE.md | 30 | 0 | 0 | 0 | Documentation |
| DOCUMENTATION_WORKFLOW.md | 30 | 0 | 0 | 0 | Documentation |
| README.md | 81 | 0 | 0 | 0 | Documentation |
| TROUBLESHOOTING.md | 30 | 0 | 0 | 0 | Documentation |
| WORKFLOW_README-main.md | 229 | 0 | 0 | 0 | Documentation |
| WORKFLOW_README-scientific.md | 229 | 0 | 0 | 0 | Documentation |
| WORKFLOW_README.md | 229 | 0 | 0 | 0 | Documentation |
| actionable_insights.md | 111 | 0 | 0 | 0 | Documentation |
| advanced_filtering_system.md | 117 | 0 | 0 | 0 | Documentation |
| advanced_workflow_system.md | 220 | 0 | 0 | 0 | Documentation |
| ai_model_training_guide.md | 32 | 0 | 0 | 0 | Documentation |
| analysis_WORKFLOW_README.json | 58 | 0 | 0 | 0 | Configuration |
| analysis_test_workflow-scientific.json | 3 | 0 | 0 | 0 | Testing |
| analysis_test_workflow.json | 3 | 0 | 0 | 0 | Testing |
| api_authentication.md | 136 | 0 | 0 | 0 | Documentation |
| application_launch_hardening_strategy.md | 0 | 0 | 0 | 0 | Documentation |
| architecture_overview.md | 0 | 0 | 0 | 0 | Documentation |
| backend_migration_guide.md | 30 | 0 | 0 | 0 | Documentation |
| branch_alignment_executive_summary.md | 30 | 0 | 0 | 0 | Documentation |
| branch_alignment_strategies_analysis.md | 30 | 0 | 0 | 0 | Documentation |
| branch_switching_guide.md | 0 | 0 | 0 | 0 | Documentation |
| changes_report.md | 0 | 0 | 0 | 0 | Documentation |
| client_development.md | 118 | 0 | 0 | 0 | Documentation |
| command_pattern.md | 138 | 0 | 0 | 0 | Documentation |
| database_configuration.md | 30 | 0 | 0 | 0 | Documentation |
| deployment_guide.md | 0 | 0 | 0 | 0 | Documentation |
| detailed_progress_report.md | 30 | 0 | 0 | 0 | Documentation |
| documenting_development_sessions.md | 30 | 0 | 0 | 0 | Documentation |
| documenting_development_sessions_summary.md | 30 | 0 | 0 | 0 | Documentation |
| env_management.md | 264 | 0 | 0 | 0 | Documentation |
| extensions_guide.md | 0 | 0 | 0 | 0 | Documentation |
| getting_started.md | 30 | 0 | 0 | 0 | Documentation |
| git_workflow_plan.md | 182 | 0 | 0 | 0 | Documentation |
| iflow_development_workflow.md | 30 | 0 | 0 | 0 | Documentation |
| key_accomplishments.md | 30 | 0 | 0 | 0 | Documentation |
| launcher_guide.md | 0 | 0 | 0 | 0 | Documentation |
| markdown_style_guide.md | 130 | 0 | 0 | 0 | Documentation |
| mfa_implementation.md | 30 | 0 | 0 | 0 | Documentation |
| multi_agent_code_review.md | 30 | 0 | 0 | 0 | Documentation |
| node_architecture.md | 0 | 0 | 0 | 0 | Documentation |
| notmuch-implementation-comparison.md | 116 | 0 | 0 | 0 | Documentation |
| notmuch-implementation-deviations.md | 118 | 0 | 0 | 0 | Documentation |
| notmuch-implementation-update.md | 69 | 0 | 0 | 0 | Documentation |
| notmuch_datasource_implementation.md | 30 | 0 | 0 | 0 | Documentation |
| orchestration-workflow.md | 210 | 0 | 0 | 0 | Documentation |
| project_documentation_guide.md | 72 | 0 | 0 | 0 | Documentation |
| project_structure_comparison.md | 0 | 0 | 0 | 0 | Documentation |
| python_style_guide.md | 127 | 0 | 0 | 0 | Documentation |
| server_development.md | 88 | 0 | 0 | 0 | Documentation |
| tagging-functionality-analysis.md | 92 | 0 | 0 | 0 | Documentation |
| test_workflow-scientific.md | 29 | 0 | 0 | 0 | Testing |
| test_workflow.md | 29 | 0 | 0 | 0 | Testing |
| unimplemented_code_analysis.md | 30 | 0 | 0 | 0 | Documentation |
| workflow_implementation_plan.md | 225 | 0 | 0 | 0 | Documentation |
| workflow_system_analysis.md | 165 | 0 | 0 | 0 | Documentation |
| worktree-documentation-system.md | 251 | 0 | 0 | 0 | Documentation |

### Directory: `docs/adr`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| 001-node-based-workflow-system.md | 58 | 0 | 0 | 0 | Documentation |
| 002-caching-strategy.md | 72 | 0 | 0 | 0 | Documentation |
| 003-security-framework.md | 69 | 0 | 0 | 0 | Documentation |

### Directory: `docs/api`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| API_REFERENCE.md | 327 | 0 | 0 | 0 | Documentation |

### Directory: `docs/architecture`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| UNIFIED_ARCHITECTURAL_PLAN.md | 356 | 0 | 0 | 0 | Documentation |
| advanced_workflow_system.md | 220 | 0 | 0 | 0 | Documentation |
| architecture_overview.md | 220 | 0 | 0 | 0 | Documentation |
| architecture_summary.md | 139 | 0 | 0 | 0 | Documentation |
| node_architecture.md | 194 | 0 | 0 | 0 | Documentation |
| technology_stack.md | 383 | 0 | 0 | 0 | Documentation |
| workflow_system_analysis.md | 165 | 0 | 0 | 0 | Documentation |

### Directory: `docs/archive`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| comparison-report.txt | 21 | 0 | 0 | 0 | Documentation |
| completion-report.md | 42 | 0 | 0 | 0 | Documentation |
| launch-setup-fixes-history.txt | 20 | 0 | 0 | 0 | Documentation |
| launch-setup-fixes-summary.md | 32 | 0 | 0 | 0 | Documentation |
| targeted-launch-fixes-history.txt | 20 | 0 | 0 | 0 | Documentation |
| targeted-launch-fixes-summary.md | 34 | 0 | 0 | 0 | Documentation |

### Directory: `docs/deployment`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CPU_ONLY_DEPLOYMENT_POLICY.md | 195 | 0 | 0 | 0 | Documentation |
| CPU_SETUP.md | 131 | 0 | 0 | 0 | Documentation |
| application_launch_hardening_strategy.md | 189 | 0 | 0 | 0 | Documentation |
| deployment_guide.md | 186 | 0 | 0 | 0 | Documentation |
| launcher_guide.md | 229 | 0 | 0 | 0 | Documentation |

### Directory: `docs/development`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CONTRIBUTING.md | 242 | 0 | 0 | 0 | Documentation |
| DEVELOPER_GUIDE.md | 389 | 0 | 0 | 0 | Documentation |
| NVIDIA_DEPENDENCY_ANALYSIS_PLAN.md | 217 | 0 | 0 | 0 | Documentation |
| STATIC_ANALYSIS_REPORT.md | 74 | 0 | 0 | 0 | Documentation |
| backend_migration_guide.md | 123 | 0 | 0 | 0 | Documentation |
| branch_cleanup_analysis.py | 219 | 4 | 4 | 0 | Core Logic |
| client_development.md | 118 | 0 | 0 | 0 | Documentation |
| env_management.md | 264 | 0 | 0 | 0 | Documentation |
| extensions_guide.md | 528 | 0 | 0 | 0 | Documentation |
| git_workflow_plan.md | 182 | 0 | 0 | 0 | Documentation |
| markdown_style_guide.md | 130 | 0 | 0 | 0 | Documentation |
| python_style_guide.md | 127 | 0 | 0 | 0 | Documentation |
| quality_standards.md | 276 | 0 | 0 | 0 | Documentation |
| server_development.md | 90 | 0 | 0 | 0 | Documentation |
| tools_used.md | 82 | 0 | 0 | 0 | Documentation |

### Directory: `docs/guides`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CLAUDE.md | 24 | 0 | 0 | 0 | Documentation |
| SCIENTIFIC_SUBTREE_GUIDE.md | 55 | 0 | 0 | 0 | Documentation |
| WORKFLOW_MIGRATION_PLAN.md | 271 | 0 | 0 | 0 | Documentation |
| actionable_insights.md | 111 | 0 | 0 | 0 | Documentation |
| advanced_filtering_system.md | 117 | 0 | 0 | 0 | Documentation |
| ai_model_training_guide.md | 658 | 0 | 0 | 0 | Documentation |
| api_authentication.md | 136 | 0 | 0 | 0 | Documentation |
| branch_switching_guide.md | 255 | 0 | 0 | 0 | Documentation |
| changes_report.md | 190 | 0 | 0 | 0 | Documentation |
| email_retrieval_module.md | 982 | 0 | 0 | 0 | Documentation |
| getting_started.md | 239 | 0 | 0 | 0 | Documentation |
| imbox_module.md | 982 | 0 | 0 | 0 | Documentation |
| mfa_implementation.md | 108 | 0 | 0 | 0 | Documentation |
| model_management_module.md | 1008 | 0 | 0 | 0 | Documentation |
| module_analysis_prioritization.md | 159 | 0 | 0 | 0 | Documentation |
| notmuch_integration.md | 835 | 0 | 0 | 0 | Documentation |
| plugin_management_module.md | 1125 | 0 | 0 | 0 | Documentation |
| project_documentation_guide.md | 72 | 0 | 0 | 0 | Documentation |
| project_structure_comparison.md | 101 | 0 | 0 | 0 | Documentation |
| system_status_module.md | 529 | 0 | 0 | 0 | Documentation |
| unimplemented_code_analysis.md | 123 | 0 | 0 | 0 | Documentation |
| workflow_and_review_process.md | 328 | 0 | 0 | 0 | Documentation |
| workflow_implementation_plan.md | 225 | 0 | 0 | 0 | Documentation |

### Directory: `docs/project-management`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| BRANCH_CLEANUP_SUMMARY.md | 124 | 0 | 0 | 0 | Documentation |
| BRANCH_DELETION_RECOMMENDATIONS.md | 249 | 0 | 0 | 0 | Documentation |
| BRANCH_OWNERSHIP_GUIDE.md | 209 | 0 | 0 | 0 | Documentation |
| DASHBOARD_CONSOLIDATION_REPORT.md | 331 | 0 | 0 | 0 | Documentation |
| DOCUMENTATION_WORKFLOW.md | 196 | 0 | 0 | 0 | Documentation |
| TROUBLESHOOTING.md | 418 | 0 | 0 | 0 | Documentation |
| complete-summary-20251102.md | 64 | 0 | 0 | 0 | Documentation |
| comprehensive-summary-20251102.md | 77 | 0 | 0 | 0 | Documentation |
| daily-summary-20251102.md | 59 | 0 | 0 | 0 | Documentation |
| feature-notmuch-20251102-summary.md | 59 | 0 | 0 | 0 | Documentation |
| feature-notmuch-complete-phased-approach.md | 110 | 0 | 0 | 0 | Documentation |
| feature-notmuch-integration-comprehensive-plan.md | 132 | 0 | 0 | 0 | Documentation |
| feature-notmuch-phase-2-selective-integration.md | 58 | 0 | 0 | 0 | Documentation |
| feature-notmuch-phase-3-testing-verification.md | 59 | 0 | 0 | 0 | Testing |
| feature-notmuch-phase-3-testing.md | 63 | 0 | 0 | 0 | Testing |
| feature-notmuch-phase-4-documentation.md | 64 | 0 | 0 | 0 | Documentation |
| feature-notmuch-phased-approach.md | 85 | 0 | 0 | 0 | Documentation |
| feature-notmuch-scientific-integration-strategy.md | 190 | 0 | 0 | 0 | Documentation |
| feature-notmuch-tagging-1-multitask-plan.md | 207 | 0 | 0 | 0 | Documentation |
| feature-notmuch-testing-verification-procedures.md | 275 | 0 | 0 | 0 | Testing |
| final-enhancement-summary.md | 92 | 0 | 0 | 0 | Documentation |
| modular-enhancement-summary.md | 56 | 0 | 0 | 0 | Documentation |
| phase-1-completion-summary.md | 92 | 0 | 0 | 0 | Documentation |
| phase-1-conflict-identification.md | 173 | 0 | 0 | 0 | Documentation |
| phase-1-current-state-analysis.md | 116 | 0 | 0 | 0 | Documentation |
| phase-1-foundation-preservation-analysis.md | 191 | 0 | 0 | 0 | Documentation |
| phase-1-risk-assessment.md | 145 | 0 | 0 | 0 | Documentation |
| phase-1-scientific-branch-analysis.md | 206 | 0 | 0 | 0 | Documentation |
| phase-2-integration-plan.md | 181 | 0 | 0 | 0 | Documentation |
| phase-2-progress-tracking.md | 159 | 0 | 0 | 0 | Documentation |

### Directory: `docs/project-management/backlog`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.yml | 14 | 0 | 0 | 0 | Configuration |

### Directory: `docs/project-management/backlog/deferred`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-18 - Backend-Migration-to-src.md | 28 | 0 | 0 | 0 | Documentation |
| task-18.1 - Sub-task-Move-Backend-Files-to-src.md | 18 | 0 | 0 | 0 | Documentation |
| task-18.2 - Sub-task-Update-Imports-and-References.md | 18 | 0 | 0 | 0 | Documentation |
| task-18.3 - Sub-task-Update-Configuration-Files.md | 18 | 0 | 0 | 0 | Documentation |
| task-18.4 - Sub-task-Run-and-Fix-Tests.md | 18 | 0 | 0 | 0 | Testing |
| task-18.5 - Sub-task-Final-Cleanup.md | 18 | 0 | 0 | 0 | Documentation |
| task-main-1 - Production-Deployment-Setup.md | 27 | 0 | 0 | 0 | Documentation |
| task-main-2 - Security-Audit-and-Hardening.md | 30 | 0 | 0 | 0 | Documentation |

### Directory: `docs/project-management/backlog/sessions`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| IFLOW-20251028-005.md | 57 | 0 | 0 | 0 | Documentation |
| IFLOW-20251028-006.md | 91 | 0 | 0 | 0 | Documentation |
| IFLOW-20251031-001.md | 63 | 0 | 0 | 0 | Documentation |
| IFLOW.md | 274 | 0 | 0 | 0 | Documentation |
| LLXPRT.md | 0 | 0 | 0 | 0 | Documentation |
| README.md | 20 | 0 | 0 | 0 | Documentation |

### Directory: `docs/project-management/backlog/tasks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| algorithm_analysis.md | 39 | 0 | 0 | 0 | Documentation |
| align-large-branches-strategy.md | 83 | 0 | 0 | 0 | Documentation |
| architecture_review.md | 131 | 0 | 0 | 0 | Documentation |
| branch-alignment-summary.md | 61 | 0 | 0 | 0 | Documentation |
| complete-branch-alignment.md | 84 | 0 | 0 | 0 | Documentation |
| create-async-fixes-pr.md | 71 | 0 | 0 | 0 | Documentation |
| create-docs-improvements-pr.md | 72 | 0 | 0 | 0 | Documentation |
| create-focused-prs.md | 71 | 0 | 0 | 0 | Documentation |
| create-import-fixes-pr.md | 71 | 0 | 0 | 0 | Documentation |
| create-launch-script-fixes-pr.md | 71 | 0 | 0 | 0 | Documentation |
| create-refactor-pr.md | 72 | 0 | 0 | 0 | Documentation |
| create-security-fixes-pr.md | 70 | 0 | 0 | 0 | Documentation |
| extract-security-fixes.md | 72 | 0 | 0 | 0 | Documentation |
| filtering-system-outstanding-tasks.md | 99 | 0 | 0 | 0 | Documentation |
| post-merge-validation.md | 64 | 0 | 0 | 0 | Documentation |
| task-1 - Resolve-merge-conflicts-in-PR-#133.md | 66 | 0 | 0 | 0 | Documentation |
| task-1 - Security-Enhancements-Authentication-and-Authorization.md | 40 | 0 | 0 | 0 | Documentation |
| task-10 - Code-Quality-Refactoring-Split-large-NLP-modules,-reduce-code-duplication,-and-break-down-high-complexity-functions.md | 38 | 0 | 0 | 0 | Documentation |
| task-10 - Global-State-Management-Refactoring.md | 41 | 0 | 0 | 0 | Documentation |
| task-100 - Task-4.3-Set-up-automated-fix-suggestions.md | 24 | 0 | 0 | 0 | Documentation |
| task-101 - Task-4.4-Add-validation-result-caching.md | 24 | 0 | 0 | 0 | Documentation |
| task-102 - Task-4.5-Create-validation-pipeline-with-early-failure-detection.md | 24 | 0 | 0 | 0 | Documentation |
| task-103 - EPIC-Performance-Monitoring-Track-agent-performance-in-real-time-for-optimization.md | 26 | 0 | 0 | 0 | Documentation |
| task-104 - Task-5.1-Implement-real-time-agent-performance-metrics.md | 24 | 0 | 0 | 0 | Documentation |
| task-105 - Task-5.2-Create-task-completion-rate-tracking.md | 24 | 0 | 0 | 0 | Documentation |
| task-106 - Task-5.3-Set-up-automated-bottleneck-detection.md | 24 | 0 | 0 | 0 | Documentation |
| task-107 - Task-5.4-Add-resource-utilization-monitoring.md | 24 | 0 | 0 | 0 | Documentation |
| task-108 - Task-5.5-Develop-completion-prediction-algorithms.md | 24 | 0 | 0 | 0 | Documentation |
| task-109 - EPIC-Agent-Workflow-Templates-Develop-templates-for-agents-to-generate-documentation-in-parallel.md | 26 | 0 | 0 | 0 | Documentation |
| task-11 - Legacy-Code-Migration-Plan.md | 41 | 0 | 0 | 0 | Documentation |
| task-11 - Testing-&-Documentation-Completion-Achieve-95%+-test-coverage-and-complete-comprehensive-documentation.md | 102 | 0 | 0 | 0 | Testing |
| task-110 - Task-6.1-Create-parallel-documentation-generation-templates.md | 24 | 0 | 0 | 0 | Documentation |
| task-111 - Task-6.2-Implement-concurrent-review-workflows.md | 24 | 0 | 0 | 0 | Documentation |
| task-112 - Task-6.3-Develop-distributed-translation-pipelines.md | 24 | 0 | 0 | 0 | Documentation |
| task-113 - Task-6.4-Set-up-automated-maintenance-task-scheduling.md | 24 | 0 | 0 | 0 | Documentation |
| task-114 - Task-6.5-Create-agent-onboarding-and-training-guides.md | 24 | 0 | 0 | 0 | Documentation |
| task-12 - Application-Monitoring-and-Observability.md | 48 | 0 | 0 | 0 | Documentation |
| task-12 - Production-Readiness-&-Deployment-Implement-monitoring,-deployment-configs,-performance-testing,-and-security-audit.md | 80 | 0 | 0 | 0 | Testing |
| task-13 - CI-CD-Pipeline-Implementation.md | 46 | 0 | 0 | 0 | Documentation |
| task-13 - Implement-api-dashboard-stats-endpoint.md | 65 | 0 | 0 | 0 | Documentation |
| task-14 - Database-Performance-Optimization.md | 41 | 0 | 0 | 0 | Documentation |
| task-14 - Implement-PromptEngineer-class-for-LLM-interaction-or-update-README.md | 55 | 0 | 0 | 0 | Documentation |
| task-15 - AI-Model-Performance-Optimization.md | 41 | 0 | 0 | 0 | Documentation |
| task-15 - Enhance-Extensions-Guide-with-detailed-Extension-API-documentation.md | 39 | 0 | 0 | 0 | Documentation |
| task-16 - Create-AI-Model-Training-Guide.md | 40 | 0 | 0 | 0 | Documentation |
| task-16 - Input-Validation-Enhancements.md | 41 | 0 | 0 | 0 | Documentation |
| task-17 - Data-Protection-Enhancements.md | 41 | 0 | 0 | 0 | Documentation |
| task-17 - Implement-proper-API-authentication-for-sensitive-operations.md | 65 | 0 | 0 | 0 | Documentation |
| task-18 - Dependency-Management-Improvements.md | 41 | 0 | 0 | 0 | Documentation |
| task-18 - Implement-EmailRepository-Interface.md | 24 | 0 | 0 | 0 | Documentation |
| task-19 - Code-Organization-Improvements.md | 41 | 0 | 0 | 0 | Documentation |
| task-19 - Create-Abstraction-Layer-Tests.md | 37 | 0 | 0 | 0 | Testing |
| task-2 - Error-Handling-Standardization.md | 42 | 0 | 0 | 0 | Documentation |
| task-2 - Fix-launch-bat-issues.md | 43 | 0 | 0 | 0 | Documentation |
| task-20 - Create-Notmuch-Tests-for-Scientific.md | 37 | 0 | 0 | 0 | Testing |
| task-20 - Data-Layer-Improvements.md | 41 | 0 | 0 | 0 | Documentation |
| task-21 - Complete-DatabaseManager-Class-Implementation.md | 51 | 0 | 0 | 0 | Documentation |
| task-21 - Create-Abstraction-Layer-Tests-on-Main.md | 58 | 0 | 0 | 0 | Testing |
| task-21 - Implement-EmailRepository-Interface-on-Main.md | 55 | 0 | 0 | 0 | Documentation |
| task-22 - Create-Task-Verification-Framework.md | 91 | 0 | 0 | 0 | Documentation |
| task-26 - Documentation-Improvement-Initiative-Phase-1-Planning-&-Prioritization.md | 24 | 0 | 0 | 0 | Documentation |
| task-26 - Phase-1.1-Analyze-current-DataSource-interface-and-identify-required-aggregation-methods-for-dashboard-statistics.md | 39 | 0 | 0 | 0 | Documentation |
| task-27 - System-Status-Module-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-28 - Model-Management-Module-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-28 - Phase-1.2-Add-get_dashboard_aggregates()-method-to-DataSource-for-efficient-server-side-calculations.md | 34 | 0 | 0 | 0 | Documentation |
| task-29 - Phase-1.3-Add-get_category_breakdown(limit)-method-to-DataSource-for-efficient-category-statistics.md | 35 | 0 | 0 | 0 | Documentation |
| task-29 - Plugin-Management-Module-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-3 - Documentation-Improvement-for-Onboarding.md | 42 | 0 | 0 | 0 | Documentation |
| task-3 - Implement-SOLID-Email-Data-Source-Abstraction.md | 79 | 0 | 0 | 0 | Documentation |
| task-30 - Email-Retrieval-Module-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-30 - Phase-1.4-Merge-DashboardStats-models-from-both-implementations-into-comprehensive-ConsolidatedDashboardStats.md | 35 | 0 | 0 | 0 | Documentation |
| task-31 - Notmuch-Integration-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-31 - Phase-1.5-Update-modules-dashboard-routes.py-to-use-new-DataSource-aggregation-methods.md | 35 | 0 | 0 | 0 | Documentation |
| task-32 - IMAP-Box-Management-Documentation.md | 26 | 0 | 0 | 0 | Documentation |
| task-32 - Phase-1.6-Add-authentication-support-to-dashboard-routes-using-get_current_active_user-dependency.md | 36 | 0 | 0 | 0 | Documentation |
| task-33 - Documentation-Enhancement-&-Quality-Assurance.md | 25 | 0 | 0 | 0 | Documentation |
| task-33 - Phase-1.7-Implement-time_saved-calculation-logic-(2-minutes-per-auto-labeled-email)-in-dashboard-routes.md | 35 | 0 | 0 | 0 | Documentation |
| task-34 - Documentation-Integration-&-Maintenance-Setup.md | 25 | 0 | 0 | 0 | Documentation |
| task-34 - Phase-1.8-Update-performance-metrics-calculation-to-work-with-new-aggregated-data-approach.md | 36 | 0 | 0 | 0 | Documentation |
| task-35 - Phase-1.9-Update-modules-dashboard-__init__.py-registration-to-handle-authentication-dependencies-properly.md | 35 | 0 | 0 | 0 | Documentation |
| task-36 - Phase-1.10-Update-test_dashboard.py-to-test-consolidated-functionality-with-new-response-model-and-authentication.md | 30 | 0 | 0 | 0 | Testing |
| task-37 - Phase-1.11-Add-integration-tests-to-verify-dashboard-works-with-both-modular-and-legacy-data-sources.md | 29 | 0 | 0 | 0 | Testing |
| task-38 - Phase-1.12-Update-API-documentation-to-reflect-new-consolidated-DashboardStats-response-model.md | 29 | 0 | 0 | 0 | Documentation |
| task-39 - Phase-1.13-Add-deprecation-warnings-and-migration-guide-for-legacy-dashboard-routes.md | 29 | 0 | 0 | 0 | Documentation |
| task-4 - Fix-test-suite-issues.md | 42 | 0 | 0 | 0 | Testing |
| task-4 - Performance-Optimization-Caching-Strategy.md | 41 | 0 | 0 | 0 | Documentation |
| task-40 - Phase-2.1-Implement-Redis-memory-caching-for-dashboard-statistics-to-reduce-database-load-and-improve-response-times.md | 30 | 0 | 0 | 0 | Documentation |
| task-41 - Phase-2.2-Add-background-job-processing-for-heavy-dashboard-calculations-(weekly-growth,-performance-metrics-aggregation).md | 30 | 0 | 0 | 0 | Documentation |
| task-42 - Phase-2.3-Optimize-category-breakdown-queries-with-database-indexing-and-query-optimization-for-large-email-datasets.md | 30 | 0 | 0 | 0 | Documentation |
| task-42 - Rebase-scientific-branch-onto-main-after-core-enhancements-merge.md | 26 | 0 | 0 | 0 | Documentation |
| task-43 - Phase-2.4-Implement-WebSocket-support-for-real-time-dashboard-updates-and-live-metrics-streaming.md | 30 | 0 | 0 | 0 | Documentation |
| task-44 - Phase-2.5-Add-dashboard-personalization-features-user-preferences,-custom-layouts,-and-saved-views.md | 30 | 0 | 0 | 0 | Documentation |
| task-45 - Phase-2.6-Implement-dashboard-export-functionality-(CSV,-PDF,-JSON)-for-statistics-and-reports.md | 30 | 0 | 0 | 0 | Documentation |
| task-46 - Phase-2.7-Create-modular-dashboard-widgets-system-for-reusable-dashboard-components.md | 30 | 0 | 0 | 0 | Documentation |
| task-47 - Phase-2.8-Add-historical-trend-analysis-with-time-series-data-visualization-and-forecasting.md | 30 | 0 | 0 | 0 | Documentation |
| task-48 - Phase-3.1-Implement-AI-insights-engine-with-ML-based-recommendations-for-email-management-optimization.md | 29 | 0 | 0 | 0 | Documentation |
| task-49 - Phase-3.2-Add-predictive-analytics-for-email-volume-forecasting-and-categorization-trend-prediction.md | 29 | 0 | 0 | 0 | Documentation |
| task-5 - Repository-Pattern-Enhancement.md | 41 | 0 | 0 | 0 | Documentation |
| task-5 - Secure-SQLite-database-paths-to-prevent-path-traversal.md | 66 | 0 | 0 | 0 | Documentation |
| task-50 - Phase-3.3-Create-advanced-interactive-visualizations-with-charts,-graphs,-and-drill-down-capabilities.md | 29 | 0 | 0 | 0 | Documentation |
| task-51 - Phase-3.4-Implement-automated-alerting-system-for-dashboard-notifications-and-threshold-based-alerts.md | 30 | 0 | 0 | 0 | Documentation |
| task-52 - Phase-3.5-Implement-A-B-testing-framework-for-dashboard-feature-experimentation-and-analytics.md | 30 | 0 | 0 | 0 | Testing |
| task-53 - Phase-3.6-Implement-multi-tenant-dashboard-support-with-isolated-instances-and-data-segregation.md | 31 | 0 | 0 | 0 | Documentation |
| task-54 - Phase-3.7-Create-comprehensive-dashboard-API-for-programmatic-access-and-third-party-integrations.md | 31 | 0 | 0 | 0 | Documentation |
| task-55 - Phase-3.8-Implement-advanced-reporting-system-with-scheduled-reports-and-analytics-exports.md | 31 | 0 | 0 | 0 | Documentation |
| task-56 - Audit-Phase-3-tasks-and-move-AI-enhancement-tasks-to-scientific-branch.md | 32 | 0 | 0 | 0 | Documentation |
| task-57 - Document-architectural-improvements-in-feature-branch-for-scientific-branch-adoption.md | 32 | 0 | 0 | 0 | Documentation |
| task-58 - Phase-4.1-Implement-dashboard-clustering-and-load-balancing-for-high-traffic-enterprise-deployments.md | 27 | 0 | 0 | 0 | Documentation |
| task-59 - Phase-4.2-Add-enterprise-security-features-including-SSO,-comprehensive-audit-logs,-and-compliance-reporting.md | 27 | 0 | 0 | 0 | Documentation |
| task-6 - Module-System-Improvements.md | 41 | 0 | 0 | 0 | Documentation |
| task-6 - Phase-1-Feature-Integration-Integrate-NetworkX-graph-operations,-security-context,-and-performance-monitoring-into-Node-Engine.md | 54 | 0 | 0 | 0 | Documentation |
| task-60 - Phase-4.3-Create-dashboard-marketplace-for-custom-widget-ecosystem-and-third-party-extensions.md | 27 | 0 | 0 | 0 | Documentation |
| task-61 - Phase-4.4-Add-global-localization-support-with-multi-language-interface-and-timezone-handling.md | 27 | 0 | 0 | 0 | Documentation |
| task-62 - Phase-4.5-Implement-dashboard-governance-with-access-controls,-approval-workflows,-and-policy-management.md | 27 | 0 | 0 | 0 | Documentation |
| task-63 - Phase-4.6-Add-disaster-recovery-capabilities-with-automated-backups-and-failover-for-dashboard-data.md | 27 | 0 | 0 | 0 | Documentation |
| task-64 - Phase-4.7-Create-dashboard-analytics-to-track-usage-metrics,-performance-insights,-and-optimization-opportunities.md | 27 | 0 | 0 | 0 | Documentation |
| task-65 - Phase-4.8-Implement-API-rate-limiting-and-throttling-to-prevent-abuse-and-ensure-fair-usage.md | 27 | 0 | 0 | 0 | Documentation |
| task-66 - Phase-4.9-Add-comprehensive-monitoring-and-observability-with-distributed-tracing-and-performance-metrics.md | 27 | 0 | 0 | 0 | Documentation |
| task-67 - Phase-4.10-Implement-auto-scaling-capabilities-for-dashboard-infrastructure-based-on-usage-patterns.md | 27 | 0 | 0 | 0 | Documentation |
| task-68 - Phase-4.11-Create-enterprise-integration-hub-for-connecting-with-existing-business-systems-and-workflows.md | 27 | 0 | 0 | 0 | Documentation |
| task-69 - Phase-4.12-Add-compliance-automation-for-GDPR,-HIPAA,-and-other-regulatory-requirements.md | 27 | 0 | 0 | 0 | Documentation |
| task-7 - AI-Engine-Modularization.md | 41 | 0 | 0 | 0 | Documentation |
| task-7 - Phase-2-Import-Consolidation-Update-all-imports-to-use-Node-Engine-as-primary-workflow-system.md | 38 | 0 | 0 | 0 | Documentation |
| task-70 - Complete-Repository-Pattern-Integration-with-Dashboard-Statistics.md | 43 | 0 | 0 | 0 | Documentation |
| task-71 - Align-NotmuchDataSource-Implementation-with-Functional-Requirements.md | 44 | 0 | 0 | 0 | Documentation |
| task-72 - Complete-Database-Dependency-Injection-Alignment.md | 46 | 0 | 0 | 0 | Documentation |
| task-73 - Update-Alignment-Strategy-Scientific-Branch-Contains-Most-Improvements.md | 35 | 0 | 0 | 0 | Documentation |
| task-79 - EPIC-Parallel-Task-Infrastructure-Break-large-documentation-tasks-into-micro-tasks-completable-in-15-minutes-for-better-parallel-utilization.md | 26 | 0 | 0 | 0 | Documentation |
| task-8 - Development-Environment-Enhancements.md | 41 | 0 | 0 | 0 | Documentation |
| task-8 - Security-&-Performance-Hardening-Enhance-security-validation,-audit-logging,-rate-limiting,-and-performance-monitoring.md | 83 | 0 | 0 | 0 | Documentation |
| task-80 - Task-1.1-Implement-micro-task-decomposition-system.md | 24 | 0 | 0 | 0 | Documentation |
| task-81 - Task-1.2-Create-independent-task-queues-with-smart-routing.md | 24 | 0 | 0 | 0 | Documentation |
| task-82 - Task-1.3-Set-up-automated-load-balancing.md | 24 | 0 | 0 | 0 | Documentation |
| task-83 - Task-1.4-Implement-real-time-completion-tracking.md | 24 | 0 | 0 | 0 | Documentation |
| task-84 - Task-1.5-Add-automated-error-recovery.md | 24 | 0 | 0 | 0 | Documentation |
| task-85 - EPIC-Agent-Coordination-Engine-Replace-polling-with-event-driven-system-for-immediate-task-assignment.md | 26 | 0 | 0 | 0 | Documentation |
| task-86 - Task-2.1-Design-event-driven-task-assignment.md | 24 | 0 | 0 | 0 | Documentation |
| task-87 - Task-2.2-Implement-agent-capability-registry.md | 24 | 0 | 0 | 0 | Documentation |
| task-88 - Task-2.3-Create-predictive-completion-time-estimation.md | 24 | 0 | 0 | 0 | Documentation |
| task-89 - Task-2.4-Set-up-automated-agent-health-monitoring.md | 24 | 0 | 0 | 0 | Documentation |
| task-9 - Advanced-Testing-Infrastructure.md | 41 | 0 | 0 | 0 | Testing |
| task-9 - UI-Enhancement-Implement-JavaScript-based-visual-workflow-editor-with-drag-and-drop-functionality.md | 32 | 0 | 0 | 0 | Documentation |
| task-90 - Task-2.5-Develop-task-dependency-resolution.md | 24 | 0 | 0 | 0 | Documentation |
| task-91 - EPIC-Synchronization-Pipeline-Create-efficient-sync-system-that-only-transfers-changed-content.md | 26 | 0 | 0 | 0 | Documentation |
| task-92 - Task-3.1-Implement-incremental-sync-with-change-detection.md | 24 | 0 | 0 | 0 | Documentation |
| task-93 - Task-3.2-Create-parallel-sync-workers.md | 24 | 0 | 0 | 0 | Documentation |
| task-94 - Task-3.3-Set-up-conflict-prediction-and-pre-resolution.md | 24 | 0 | 0 | 0 | Documentation |
| task-95 - Task-3.4-Add-atomic-commit-groups.md | 24 | 0 | 0 | 0 | Documentation |
| task-96 - Task-3.5-Implement-sync-prioritization.md | 24 | 0 | 0 | 0 | Documentation |
| task-97 - EPIC-Quality-Assurance-Automation-Implement-multiple-validation-processes-running-simultaneously.md | 26 | 0 | 0 | 0 | Documentation |
| task-98 - Task-4.1-Create-parallel-validation-workers.md | 24 | 0 | 0 | 0 | Documentation |
| task-99 - Task-4.2-Implement-incremental-validation.md | 24 | 0 | 0 | 0 | Documentation |
| task-architecture-improvement.md | 53 | 0 | 0 | 0 | Documentation |
| task-database-refactoring.md | 66 | 0 | 0 | 0 | Documentation |
| task-high.1 - Implement-Dynamic-AI-Model-Management-System.md | 45 | 0 | 0 | 0 | Documentation |
| task-high.2 - Implement-Plugin-Manager-System.md | 45 | 0 | 0 | 0 | Documentation |
| task-high.3 - Implement-Advanced-Workflow-Security-Framework.md | 33 | 0 | 0 | 0 | Documentation |
| task-medium.1 - Implement-Scientific-UI-System-Status-Dashboard.md | 42 | 0 | 0 | 0 | Documentation |
| task-medium.2 - Implement-AI-Lab-Interface-for-Scientific-Exploration.md | 42 | 0 | 0 | 0 | Documentation |
| task-medium.3 - Implement-Gmail-Performance-Metrics-API.md | 42 | 0 | 0 | 0 | Documentation |
| task-medium.4 - Implement-Gmail-Integration-UI-Tab.md | 42 | 0 | 0 | 0 | Documentation |
| task-medium.5 - Standardize-Dependency-Management-System.md | 44 | 0 | 0 | 0 | Documentation |
| task-security-enhancement.md | 67 | 0 | 0 | 0 | Documentation |
| task-testing-improvement.md | 59 | 0 | 0 | 0 | Testing |
| task-workflow-enhancement.md | 66 | 0 | 0 | 0 | Documentation |
| todo_analysis.md | 164 | 0 | 0 | 0 | Documentation |
| todo_consolidation_strategy.md | 162 | 0 | 0 | 0 | Documentation |
| todo_organization_summary.md | 113 | 0 | 0 | 0 | Documentation |
| verify-and-merge-prs.md | 81 | 0 | 0 | 0 | Documentation |

### Directory: `docs/templates`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| module_documentation_template.md | 386 | 0 | 0 | 0 | Documentation |

### Directory: `implement`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| plan.md | 57 | 0 | 0 | 0 | Documentation |
| state.json | 22 | 0 | 0 | 0 | Configuration |

### Directory: `jules-scratch/verification`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| verification.png | 4 | 0 | 0 | 0 | Asset |
| verify_frontend.py | 52 | 1 | 2 | 0 | Core Logic |

### Directory: `logs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| audit.jsonl | 19 | 0 | 0 | 0 | Data |
| audit.log | 19 | 0 | 0 | 0 | Other |
| docs_sync.log | 56 | 0 | 0 | 0 | Documentation |
| docs_sync_metrics.json | 98 | 0 | 0 | 0 | Configuration |
| maintenance_report_20251102_022517.json | 41 | 0 | 0 | 0 | Configuration |
| maintenance_report_20251102_023206.json | 46 | 0 | 0 | 0 | Configuration |
| performance_metrics.jsonl | 102 | 0 | 0 | 0 | Data |
| server.log | 0 | 0 | 0 | 0 | Other |
| workflow_audit.log | 238 | 0 | 0 | 0 | Other |

### Directory: `models`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| sentiment-default.json | 8 | 0 | 0 | 0 | Configuration |
| test_model_5b8753a1-b0ab-4d30-9566-24c2e95d2fa6.pkl | 46 | 0 | 0 | 0 | Testing |
| test_model_63ba9a7c-088f-48d7-8996-97ab99f871a1.pkl | 47 | 0 | 0 | 0 | Testing |
| test_model_9de096f1-b4f2-4d24-a0d4-faa5eaf6d3fc.pkl | 46 | 0 | 0 | 0 | Testing |
| test_model_d245b4c6-7f9b-40ec-b475-07fd3369bb07.pkl | 46 | 0 | 0 | 0 | Testing |
| test_model_d4ef6ccb-59e7-4862-be91-7608b350c863.pkl | 47 | 0 | 0 | 0 | Testing |
| test_model_f4df251d-668f-4982-934f-8d83abab3802.pkl | 46 | 0 | 0 | 0 | Testing |
| topic-default.json | 8 | 0 | 0 | 0 | Configuration |

### Directory: `models/intent`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.json | 25 | 0 | 0 | 0 | Configuration |
| model.safetensors | 3 | 0 | 0 | 0 | Other |
| special_tokens_map.json | 7 | 0 | 0 | 0 | Configuration |
| tokenizer.json | 30672 | 0 | 0 | 0 | Configuration |
| tokenizer_config.json | 58 | 0 | 0 | 0 | Configuration |
| vocab.txt | 30522 | 0 | 0 | 0 | Other |

### Directory: `models/sentiment`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.json | 33 | 0 | 0 | 0 | Configuration |
| model.safetensors | 3 | 0 | 0 | 0 | Other |
| special_tokens_map.json | 7 | 0 | 0 | 0 | Configuration |
| tokenizer.json | 30672 | 0 | 0 | 0 | Configuration |
| tokenizer_config.json | 58 | 0 | 0 | 0 | Configuration |
| vocab.txt | 30522 | 0 | 0 | 0 | Other |

### Directory: `models/topic`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.json | 70 | 0 | 0 | 0 | Configuration |
| merges.txt | 50001 | 0 | 0 | 0 | Other |
| model.safetensors | 3 | 0 | 0 | 0 | Other |
| special_tokens_map.json | 51 | 0 | 0 | 0 | Configuration |
| tokenizer.json | 250357 | 0 | 0 | 0 | Configuration |
| tokenizer_config.json | 58 | 0 | 0 | 0 | Configuration |
| vocab.json | 1 | 0 | 0 | 0 | Configuration |

### Directory: `models/urgency`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.json | 25 | 0 | 0 | 0 | Configuration |
| model.safetensors | 3 | 0 | 0 | 0 | Other |
| special_tokens_map.json | 7 | 0 | 0 | 0 | Configuration |
| tokenizer.json | 30672 | 0 | 0 | 0 | Configuration |
| tokenizer_config.json | 58 | 0 | 0 | 0 | Configuration |
| vocab.txt | 30522 | 0 | 0 | 0 | Other |

### Directory: `modules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |

### Directory: `modules/auth`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 20 | 4 | 1 | 0 | Core Logic |
| routes.py | 283 | 10 | 0 | 6 | Core Logic |

### Directory: `modules/categories`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 27 | 4 | 1 | 0 | Core Logic |
| routes.py | 56 | 11 | 0 | 0 | Core Logic |

### Directory: `modules/dashboard`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 28 | 3 | 1 | 0 | Core Logic |
| models.py | 44 | 2 | 0 | 4 | Core Logic |
| routes.py | 93 | 10 | 0 | 0 | Core Logic |

### Directory: `modules/default_ai_engine`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 32 | 5 | 1 | 0 | Core Logic |
| engine.py | 104 | 9 | 7 | 1 | Core Logic |
| text_utils.py | 31 | 1 | 1 | 0 | Core Logic |

### Directory: `modules/default_ai_engine/analysis_components`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 8 | 0 | 0 | 0 | Core Logic |
| intent_model.py | 125 | 3 | 4 | 1 | Core Logic |
| sentiment_model.py | 178 | 3 | 5 | 1 | Core Logic |
| topic_model.py | 118 | 2 | 4 | 1 | Core Logic |
| urgency_model.py | 108 | 3 | 4 | 1 | Core Logic |

### Directory: `modules/email`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 20 | 4 | 1 | 0 | Core Logic |
| routes.py | 92 | 10 | 0 | 0 | Core Logic |

### Directory: `modules/email_retrieval`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 9 | 2 | 1 | 0 | Core Logic |
| email_retrieval_ui.py | 395 | 8 | 10 | 0 | Core Logic |

### Directory: `modules/imbox`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 9 | 2 | 1 | 0 | Core Logic |
| imbox_ui.py | 69 | 3 | 2 | 0 | Core Logic |

### Directory: `modules/model_management`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 33 | 4 | 1 | 0 | Core Logic |

### Directory: `modules/notmuch`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 11 | 3 | 1 | 0 | Core Logic |
| ui.py | 86 | 5 | 3 | 0 | Core Logic |

### Directory: `modules/plugin_management`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 33 | 4 | 1 | 0 | Core Logic |

### Directory: `modules/system_status`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 265 | 9 | 6 | 0 | Core Logic |
| models.py | 39 | 3 | 0 | 3 | Core Logic |

### Directory: `modules/workflows`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 28 | 4 | 1 | 0 | Core Logic |
| ui.py | 186 | 5 | 3 | 3 | Core Logic |

### Directory: `monitoring`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| prometheus.yml | 62 | 0 | 0 | 0 | Configuration |

### Directory: `monitoring/grafana/dashboards`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| email-intelligence.json | 98 | 0 | 0 | 0 | Configuration |

### Directory: `monitoring/grafana/provisioning/dashboards`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dashboard.yml | 12 | 0 | 0 | 0 | Configuration |

### Directory: `monitoring/grafana/provisioning/datasources`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| prometheus.yml | 11 | 0 | 0 | 0 | Configuration |

### Directory: `nginx`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| nginx.conf | 176 | 0 | 0 | 0 | Other |

### Directory: `plugins/example_ai_enhancer`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 202 | 3 | 7 | 1 | Core Logic |
| plugin.json | 15 | 0 | 0 | 0 | Configuration |

### Directory: `plugins/example_workflow_plugin`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 92 | 7 | 2 | 1 | Core Logic |

### Directory: `python_backend`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| llm_config.py | 59 | 5 | 3 | 0 | Configuration |

### Directory: `scripts`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| auto_sync_docs.py | 273 | 12 | 10 | 1 | Scripting |
| docs_branch_versioning.py | 141 | 7 | 7 | 1 | Scripting |
| docs_content_analyzer.py | 218 | 8 | 11 | 1 | Scripting |
| docs_merge_strategist.py | 332 | 9 | 15 | 1 | Scripting |
| docs_merge_strategist.py.backup | 288 | 0 | 0 | 0 | Scripting |
| docs_review_manager.py | 323 | 8 | 14 | 1 | Scripting |
| docs_workflow_trigger.py | 147 | 5 | 7 | 1 | Scripting |
| install-hooks.sh | 20 | 0 | 0 | 0 | Scripting |
| maintenance_docs.py | 497 | 8 | 13 | 1 | Scripting |
| orchestration_status.sh | 349 | 0 | 0 | 0 | Scripting |
| post-commit-sync | 20 | 0 | 0 | 0 | Scripting |
| pre-commit-docs-check | 64 | 0 | 0 | 0 | Scripting |
| setup_automation.sh | 173 | 0 | 0 | 0 | Scripting |
| sync-common-docs.sh | 202 | 0 | 0 | 0 | Scripting |
| sync_common_docs.py | 276 | 9 | 11 | 1 | Scripting |
| sync_config.json | 31 | 0 | 0 | 0 | Configuration |
| sync_setup_worktrees.sh | 248 | 0 | 0 | 0 | Scripting |
| test_orchestration.sh | 186 | 0 | 0 | 0 | Testing |

### Directory: `scripts/hooks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| post-checkout | 15 | 0 | 0 | 0 | Scripting |
| post-commit | 15 | 0 | 0 | 0 | Scripting |
| post-commit-setup-sync | 46 | 0 | 0 | 0 | Scripting |
| post-merge | 109 | 0 | 0 | 0 | Scripting |
| post-push | 195 | 0 | 0 | 0 | Scripting |
| pre-commit | 65 | 0 | 0 | 0 | Scripting |

### Directory: `server`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.ts | 121 | 0 | 0 | 0 | Frontend |
| package.json | 26 | 0 | 0 | 0 | Configuration |

### Directory: `setup`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .env.example | 18 | 0 | 0 | 0 | Other |
| README.md | 27 | 0 | 0 | 0 | Documentation |
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| launch.bat | 63 | 0 | 0 | 0 | Scripting |
| launch.py | 1011 | 0 | 0 | 0 | Core Logic |
| launch.sh | 5 | 0 | 0 | 0 | Scripting |
| pyproject.toml | 77 | 0 | 0 | 0 | Configuration |
| requirements-dev.txt | 11 | 0 | 0 | 0 | Other |
| requirements.txt | 49 | 0 | 0 | 0 | Other |
| setup_environment_system.sh | 395 | 0 | 0 | 0 | Scripting |
| setup_environment_wsl.sh | 521 | 0 | 0 | 0 | Scripting |
| setup_python.sh | 128 | 0 | 0 | 0 | Scripting |

### Directory: `shared`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| schema.ts | 151 | 0 | 0 | 0 | Frontend |

### Directory: `src`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| main.py | 713 | 17 | 13 | 0 | Core Logic |

### Directory: `src/core`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| advanced_workflow_engine.py | 775 | 15 | 38 | 11 | Core Logic |
| ai_engine.py | 463 | 4 | 21 | 3 | Core Logic |
| audit_logger.py | 305 | 12 | 9 | 4 | Core Logic |
| auth.py | 312 | 13 | 9 | 3 | Core Logic |
| caching.py | 399 | 9 | 7 | 8 | Core Logic |
| constants.py | 13 | 0 | 0 | 0 | Core Logic |
| data_source.py | 113 | 2 | 0 | 1 | Core Logic |
| database.py | 843 | 15 | 7 | 2 | Core Logic |
| dynamic_model_manager.py | 410 | 9 | 6 | 1 | Core Logic |
| enhanced_caching.py | 230 | 5 | 27 | 3 | Core Logic |
| enhanced_error_reporting.py | 263 | 8 | 16 | 4 | Core Logic |
| exceptions.py | 35 | 0 | 4 | 4 | Core Logic |
| factory.py | 99 | 12 | 0 | 0 | Core Logic |
| job_queue.py | 151 | 9 | 8 | 2 | Core Logic |
| mfa.py | 133 | 7 | 7 | 1 | Core Logic |
| middleware.py | 246 | 9 | 6 | 2 | Core Logic |
| model_registry.py | 717 | 13 | 3 | 5 | Core Logic |
| model_routes.py | 402 | 8 | 0 | 5 | Core Logic |
| models.py | 487 | 4 | 2 | 39 | Core Logic |
| module_manager.py | 59 | 4 | 3 | 1 | Core Logic |
| notmuch_data_source.py | 742 | 13 | 1 | 1 | Core Logic |
| performance_monitor.py | 0 | 0 | 0 | 0 | Core Logic |
| plugin_base.py | 553 | 13 | 14 | 8 | Core Logic |
| plugin_manager.py | 486 | 13 | 8 | 3 | Core Logic |
| plugin_routes.py | 351 | 6 | 0 | 5 | Core Logic |
| rate_limiter.py | 150 | 6 | 4 | 4 | Core Logic |
| security.py | 716 | 21 | 25 | 9 | Core Logic |
| security_validator.py | 315 | 6 | 5 | 4 | Core Logic |
| settings.py | 22 | 2 | 1 | 1 | Core Logic |
| smart_filter_manager.py | 864 | 16 | 18 | 3 | Core Logic |
| workflow_engine.py | 685 | 9 | 12 | 4 | Core Logic |

### Directory: `src/core/data`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 4 | 0 | 0 | 0 | Core Logic |
| data_source.py | 121 | 2 | 0 | 1 | Core Logic |
| database_source.py | 108 | 6 | 1 | 1 | Core Logic |
| factory.py | 9 | 1 | 0 | 0 | Core Logic |
| notmuch_data_source.py | 69 | 2 | 0 | 1 | Core Logic |
| repository.py | 316 | 6 | 2 | 3 | Core Logic |

### Directory: `tests`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Testing |
| conftest.py | 162 | 14 | 7 | 0 | Testing |
| test_api_actions.py | 70 | 3 | 5 | 0 | Testing |
| test_auth.py | 34 | 6 | 2 | 0 | Testing |
| test_basic.py | 36 | 3 | 2 | 0 | Testing |
| test_category_api.py | 89 | 3 | 2 | 0 | Testing |
| test_dashboard_api.py | 77 | 2 | 5 | 0 | Testing |
| test_database.py | 175 | 5 | 0 | 0 | Testing |
| test_email_api.py | 134 | 5 | 0 | 0 | Testing |
| test_filter_api.py | 96 | 5 | 6 | 0 | Testing |
| test_gmail_api.py | 105 | 4 | 7 | 0 | Testing |
| test_launcher.py | 192 | 7 | 12 | 4 | Testing |
| test_mfa.py | 106 | 4 | 1 | 0 | Testing |
| test_password_hashing.py | 34 | 2 | 3 | 0 | Testing |
| test_prompt_engineer.py | 28 | 2 | 3 | 1 | Testing |
| test_security_integration.py | 267 | 11 | 13 | 5 | Testing |
| test_workflow_engine.py | 253 | 5 | 15 | 0 | Testing |

### Directory: `tests/backend/node_engine`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_security_manager.py | 139 | 2 | 12 | 4 | Testing |

### Directory: `tests/core`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_advanced_workflow_engine.py | 165 | 4 | 9 | 3 | Testing |
| test_app.py | 20 | 1 | 2 | 0 | Testing |
| test_caching.py | 153 | 3 | 5 | 3 | Testing |
| test_data_source.py | 422 | 13 | 4 | 5 | Testing |
| test_email_repository.py | 69 | 4 | 2 | 0 | Testing |
| test_factory.py | 342 | 20 | 4 | 5 | Testing |
| test_notmuch_data_source.py | 527 | 7 | 9 | 6 | Testing |
| test_security.py | 200 | 12 | 15 | 3 | Testing |
| test_workflow_engine.py | 253 | 3 | 16 | 0 | Testing |

### Directory: `tests/deprecated`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_api_actions.py | 1 | 0 | 0 | 0 | Testing |
| test_dashboard_api.py | 1 | 0 | 0 | 0 | Testing |
| test_database.py | 1 | 0 | 0 | 0 | Testing |
| test_filter_api.py | 1 | 0 | 0 | 0 | Testing |
| test_gmail_api.py | 1 | 0 | 0 | 0 | Testing |

### Directory: `tests/modules/categories`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_categories.py | 31 | 3 | 0 | 0 | Testing |

### Directory: `tests/modules/dashboard`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_dashboard.py | 168 | 15 | 5 | 0 | Testing |
| test_dashboard.py.backup | 166 | 0 | 0 | 0 | Testing |

### Directory: `tests/modules/default_ai_engine`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_modular_ai_engine.py | 11 | 2 | 1 | 0 | Testing |
