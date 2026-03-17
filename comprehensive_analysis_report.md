# Comprehensive Repository Analysis Report

## Part 1: Architectural Analysis

### Circular Dependencies

No circular dependencies found. Excellent!

### Module Coupling

#### Top 10 Most Depended-Upon Modules (Highest Afferent Coupling)
| Module | Imported By # Files |
|--------|---------------------|
| `src/core/factory.py` | 22 |
| `src/core/auth.py` | 14 |
| `src/core/database.py` | 13 |
| `src/backend/node_engine/node_base.py` | 12 |
| `src/core/git/plumbing.py` | 11 |
| `src/backend/node_engine/workflow_engine.py` | 10 |
| `src/backend/python_backend/gradio_app.py` | 9 |
| `src/core/conflict_models.py` | 8 |
| `src/main.py` | 7 |
| `src/backend/python_nlp/smart_filters.py` | 7 |

#### Top 10 Most Dependent Modules (Highest Efferent Coupling)
| Module | Imports # Files |
|--------|-----------------|
| `validate_architecture_alignment.py` | 13 |
| `.taskmaster/emailintelligence_cli.py` | 13 |
| `.taskmaster/guidance/validate_architecture_alignment.py` | 13 |
| `guidance/validate_architecture_alignment.py` | 13 |
| `emailintelligence_cli.py` | 12 |
| `tests/core/test_factory.py` | 12 |
| `src/backend/python_backend/node_workflow_routes.py` | 11 |
| `tests/core/test_data_source.py` | 9 |
| `src/main.py` | 7 |
| `src/backend/python_backend/dependencies.py` | 7 |

### Orphan Files (Potential Unused Code or Entrypoints)

Found 82 potential orphan files:
- `demo_mfa.py`
- `validate_architecture_alignment.py`
- `src/backend/python_backend/model_routes.py`
- `src/backend/python_backend/dashboard_routes.py`
- `src/backend/python_backend/category_routes.py`
- `src/backend/python_backend/enhanced_routes.py`
- `src/backend/python_backend/advanced_workflow_routes.py`
- `src/backend/python_backend/training_routes.py`
- `src/backend/python_backend/email_routes.py`
- `src/backend/python_backend/workflow_routes.py`
- `src/backend/python_backend/filter_routes.py`
- `src/backend/python_backend/node_workflow_routes.py`
- `src/backend/python_backend/workflow_editor_ui.py`
- `src/backend/python_backend/tests/conftest.py`
- `src/backend/python_backend/routes/v1/category_routes.py`
- `src/backend/python_backend/routes/v1/email_routes.py`
- `src/backend/python_backend/services/base_service.py`
- `src/backend/python_nlp/gmail_integration.py`
- `src/core/execution/session.py`
- `src/core/execution/executor.py`
- `src/cli/main.py`
- `src/cli/main_old_backup.py`
- `src/cli/commands/guide.py`
- `src/cli/commands/resolve.py`
- `src/cli/commands/task.py`
- `src/cli/commands/rebase.py`
- `src/cli/commands/schema.py`
- `src/cli/commands/analyze.py`
- `src/cli/commands/compare.py`
- `src/cli/commands/sync.py`
- `setup/test_config.py`
- `setup/commands/check_command.py`
- `setup/commands/run_command.py`
- `setup/commands/setup_command.py`
- `setup/commands/cleanup_command.py`
- `setup/commands/test_command.py`
- `tests/test_security_integration.py`
- `tests/test_basic.py`
- `tests/test_email_api.py`
- `tests/test_launcher.py`
- `tests/test_password_hashing.py`
- `tests/test_category_api.py`
- `tests/test_workflow_engine.py`
- `tests/test_api_actions.py`
- `tests/test_filter_api.py`
- `tests/test_auth.py`
- `tests/test_mfa.py`
- `tests/test_database.py`
- `tests/integration/test_cli_guides.py`
- `tests/core/test_factory.py`
- `tests/core/test_data_source.py`
- `tests/core/test_notmuch_data_source.py`
- `tests/core/test_advanced_workflow_engine.py`
- `tests/core/test_security.py`
- `tests/core/test_workflow_engine.py`
- `tests/core/test_email_repository.py`
- `tests/core/test_caching.py`
- `tests/unit/test_rebase_detector.py`
- `tests/unit/test_merge_verifier.py`
- `tests/unit/test_workflow_context.py`
- `tests/unit/test_analysis_service.py`
- `tests/unit/test_git_wrapper.py`
- `tests/unit/test_rebase_analyzer.py`
- `tests/modules/dashboard/test_dashboard.py`
- `tests/modules/default_ai_engine/test_modular_ai_engine.py`
- `tests/functional/test_advanced_git.py`
- `tests/functional/test_git_comparison.py`
- `tests/functional/test_git_plumbing.py`
- `.taskmaster/emailintelligence_cli.py`
- `.taskmaster/src/main.py`
- `.taskmaster/src/application/conflict_resolution_app.py`
- `.taskmaster/src/analysis/conflict_analyzer.py`
- `.taskmaster/tests/test_security_fixes.py`
- `.taskmaster/guidance/validate_architecture_alignment.py`
- `.taskmaster/guidance/src/main.py`
- `modules/workflows/ui.py`
- `modules/notmuch/ui.py`
- `modules/auth/routes.py`
- `modules/email/routes.py`
- `scripts/architectural_rule_engine.py`
- `guidance/validate_architecture_alignment.py`
- `guidance/src/main.py`

---

## Part 2: Detailed File Metrics

### Directory: `./`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .RULES_ANALYSIS.md | 193 | 0 | 0 | 0 | Documentation |
| .aider.chat.history.md | 5 | 0 | 0 | 0 | Documentation |
| .aider.conf.yml | 44 | 0 | 0 | 0 | Configuration |
| .bandit | 2 | 0 | 0 | 0 | Other |
| .concurrent_reviews.json | 329 | 0 | 0 | 0 | Configuration |
| .cursorignore | 1 | 0 | 0 | 0 | Other |
| .env.example | 12 | 0 | 0 | 0 | Other |
| .flake8 | 28 | 0 | 0 | 0 | Other |
| .geminiignore | 17 | 0 | 0 | 0 | Other |
| .gitattributes | 10 | 0 | 0 | 0 | Other |
| .gitignore | 192 | 0 | 0 | 0 | Other |
| .maintenance_scheduler.json | 208 | 0 | 0 | 0 | Configuration |
| .mcp.json | 1 | 0 | 0 | 0 | Configuration |
| .orchestration-disabled | 0 | 0 | 0 | 0 | Other |
| .pylintrc | 47 | 0 | 0 | 0 | Other |
| .roomodes | 1 | 0 | 0 | 0 | Other |
| .rules | 417 | 0 | 0 | 0 | Other |
| .rulesyncignore | 1 | 0 | 0 | 0 | Other |
| .validation_cache.json | 47 | 0 | 0 | 0 | Configuration |
| AGENT.md | 5 | 0 | 0 | 0 | Documentation |
| AGENTS.md | 863 | 0 | 0 | 0 | Documentation |
| AGENTS_orchestration-tools.md | 304 | 0 | 0 | 0 | Documentation |
| AGENT_GUIDELINES_QUICK_REFERENCE.md | 257 | 0 | 0 | 0 | Documentation |
| AGENT_GUIDELINES_RESOLUTION_PLAN.md | 605 | 0 | 0 | 0 | Documentation |
| ARCHITECTURE_ALIGNMENT_COMPLETE.md | 55 | 0 | 0 | 0 | Documentation |
| ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md | 109 | 0 | 0 | 0 | Documentation |
| BLOCKER_ANALYSIS_INDEX.md | 365 | 0 | 0 | 0 | Documentation |
| BRANCH_AGENT_GUIDELINES_SUMMARY.md | 386 | 0 | 0 | 0 | Documentation |
| BRANCH_ANALYSIS_REPORT.md | 217 | 0 | 0 | 0 | Documentation |
| BRANCH_CLEANUP_RESULTS.md | 63 | 0 | 0 | 0 | Documentation |
| BRANCH_PROPAGATION_IMPLEMENTATION_SUMMARY.md | 535 | 0 | 0 | 0 | Documentation |
| BRANCH_UPDATE_PROCEDURE.md | 628 | 0 | 0 | 0 | Documentation |
| BRANCH_UPDATE_QUICK_START.md | 303 | 0 | 0 | 0 | Documentation |
| CLAUDE.md | 143 | 0 | 0 | 0 | Documentation |
| COMPLETE_HOOK_AND_BRANCH_FIXES.md | 292 | 0 | 0 | 0 | Documentation |
| COMPREHENSIVE_ARCHITECTURE_ANALYSIS.md | 1106 | 0 | 0 | 0 | Documentation |
| COMPREHENSIVE_TODO_ANALYSIS.md | 311 | 0 | 0 | 0 | Documentation |
| CONFIG.md | 87 | 0 | 0 | 0 | Documentation |
| CONTEXT_CONTAMINATION_PREVENTION.md | 318 | 0 | 0 | 0 | Documentation |
| CONTRIBUTING.md | 242 | 0 | 0 | 0 | Documentation |
| CPU_SETUP.md | 131 | 0 | 0 | 0 | Documentation |
| DEPENDENCY_BLOCKER_ANALYSIS.md | 459 | 0 | 0 | 0 | Documentation |
| DOCUMENTATION_DISTRIBUTION_AUDIT.md | 136 | 0 | 0 | 0 | Documentation |
| Dockerfile.prod | 41 | 0 | 0 | 0 | Containerization |
| FINAL_MERGE_STRATEGY.md | 68 | 0 | 0 | 0 | Documentation |
| FINAL_SETUP_STATUS.md | 167 | 0 | 0 | 0 | Documentation |
| FLAKE8_UNIFICATION_SUMMARY.md | 224 | 0 | 0 | 0 | Documentation |
| GEMINI.md | 353 | 0 | 0 | 0 | Documentation |
| GIT_BRANCH_COMPREHENSIVE_ANALYSIS.md | 1029 | 0 | 0 | 0 | Documentation |
| GIT_HOOKS_BLOCKING_SUMMARY.md | 355 | 0 | 0 | 0 | Documentation |
| GIT_MERGE_GUIDE.md | 122 | 0 | 0 | 0 | Documentation |
| HANDLING_INCOMPLETE_MIGRATIONS.md | 96 | 0 | 0 | 0 | Documentation |
| HOOK_BLOCKING_SCENARIOS.md | 320 | 0 | 0 | 0 | Documentation |
| HOOK_BRANCH_MAINTENANCE_FIX.md | 205 | 0 | 0 | 0 | Documentation |
| HOOK_SAFETY_FIXES.md | 186 | 0 | 0 | 0 | Documentation |
| IMPLEMENTATION_SUMMARY.md | 108 | 0 | 0 | 0 | Documentation |
| IMPROVED_PROMPT_ANSWERS.md | 132 | 0 | 0 | 0 | Documentation |
| INSTALLATION.md | 244 | 0 | 0 | 0 | Documentation |
| INTERACTIVE_RESOLVER_ISSUES.md | 149 | 0 | 0 | 0 | Documentation |
| MERGE_GUIDANCE_DOCUMENTATION.md | 203 | 0 | 0 | 0 | Documentation |
| MERGE_PROGRESS_SUMMARY.md | 51 | 0 | 0 | 0 | Documentation |
| MODEL_CONTEXT_STRATEGY.md | 320 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_CONTROL_MODULE.md | 426 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_DELIVERY_CHECKLIST.md | 382 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_DISABLE_BRANCH_SYNC.md | 449 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_DISABLE_FLAG.md | 445 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_DISABLE_QUICK_REFERENCE.md | 139 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_DOCS_INDEX.md | 313 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_DOCS_SCRIPTS_REVIEW.md | 319 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_HOOK_FIXES_SUMMARY.md | 168 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_IDE_AGENT_INCLUSION.md | 208 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_IDE_DISTRIBUTION_PLAN.md | 340 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_IDE_INCLUSION_SUMMARY.md | 196 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_IDE_QUICK_REFERENCE.md | 157 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_IMPLEMENTATION_SUMMARY.md | 362 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_PROCESS_GUIDE.md | 518 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_PROGRESS_SUMMARY.md | 314 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_QUICK_DISABLE.md | 134 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_SYNC_GUIDE.md | 245 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_TEST_PROMPTS.txt | 76 | 0 | 0 | 0 | Testing |
| ORCHESTRATION_TEST_SUITE.md | 369 | 0 | 0 | 0 | Testing |
| ORCHESTRATION_TOOLS_REDESIGN.md | 396 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_VARIANTS_BRANCH_SUPPORT.md | 244 | 0 | 0 | 0 | Documentation |
| OUTSTANDING_TODOS.md | 229 | 0 | 0 | 0 | Documentation |
| PHASE3_ROLLBACK_OPTIONS.md | 200 | 0 | 0 | 0 | Documentation |
| PROGRESS_DASHBOARD.md | 261 | 0 | 0 | 0 | Documentation |
| PROGRESS_TRACKING.md | 500 | 0 | 0 | 0 | Documentation |
| PROGRESS_TRACKING_README.md | 213 | 0 | 0 | 0 | Documentation |
| QWEN.md | 230 | 0 | 0 | 0 | Documentation |
| README.md | 76 | 0 | 0 | 0 | Documentation |
| REMAINING_STASH_FIXES.md | 170 | 0 | 0 | 0 | Documentation |
| SAFE_ACTION_PLAN.md | 155 | 0 | 0 | 0 | Documentation |
| SCIENTIFIC_BRANCH_ALIGNMENT_PLAN.md | 78 | 0 | 0 | 0 | Documentation |
| SCIENTIFIC_SUBTREE_GUIDE.md | 55 | 0 | 0 | 0 | Documentation |
| SECURITY.md | 70 | 0 | 0 | 0 | Documentation |
| SECURITY_INCIDENT_RESPONSE.md | 104 | 0 | 0 | 0 | Documentation |
| SESSION_LOG.md | 81 | 0 | 0 | 0 | Documentation |
| STASH_FIXES_COMPLETION.md | 117 | 0 | 0 | 0 | Documentation |
| STASH_FIXES_FINAL_STATUS.md | 202 | 0 | 0 | 0 | Documentation |
| STASH_FIXES_SUMMARY.md | 118 | 0 | 0 | 0 | Documentation |
| STASH_MANAGEMENT_ISSUES.md | 129 | 0 | 0 | 0 | Documentation |
| STRATEGIC_REFACTORING_GUIDE.md | 1062 | 0 | 0 | 0 | Documentation |
| SUBMODULE_CONFIGURATION.md | 159 | 0 | 0 | 0 | Documentation |
| SUBMODULE_SETUP_SUMMARY.md | 171 | 0 | 0 | 0 | Documentation |
| SUBTREE_TESTING_GUIDE.md | 89 | 0 | 0 | 0 | Testing |
| SYSTEM_PACKAGES_README.md | 157 | 0 | 0 | 0 | Documentation |
| TASKMASTER_BRANCH_CONVENTIONS.md | 195 | 0 | 0 | 0 | Documentation |
| TASKMASTER_INTEGRATION_README.md | 336 | 0 | 0 | 0 | Documentation |
| TASKMASTER_ISOLATION_FIX.md | 143 | 0 | 0 | 0 | Documentation |
| TASKMASTER_WORKTREE_MIGRATION.md | 49 | 0 | 0 | 0 | Documentation |
| TASK_CREATION_GUIDE.md | 471 | 0 | 0 | 0 | Documentation |
| TASK_CREATION_QUICK_REF.md | 269 | 0 | 0 | 0 | Documentation |
| TASK_CREATION_WORKFLOW.md | 467 | 0 | 0 | 0 | Documentation |
| TASK_INVENTORY_REVIEW.md | 267 | 0 | 0 | 0 | Documentation |
| WORKTREE_SETUP_INTEGRATION_GUIDE.md | 126 | 0 | 0 | 0 | Documentation |
| actionable_insights.md | 232 | 0 | 0 | 0 | Documentation |
| agent-config.json | 38 | 0 | 0 | 0 | Configuration |
| alignment-main-task-template.md | 100 | 0 | 0 | 0 | Documentation |
| alignment-task-template.md | 100 | 0 | 0 | 0 | Documentation |
| analyze_repo.py | 260 | 4 | 9 | 0 | Core Logic |
| architecture_summary.md | 139 | 0 | 0 | 0 | Documentation |
| backlog-merge-driver.sh | 90 | 0 | 0 | 0 | Scripting |
| backup.sh | 338 | 0 | 0 | 0 | Scripting |
| benchmark_conflicts.py | 75 | 4 | 5 | 0 | Core Logic |
| branch_management_recommendations.md | 71 | 0 | 0 | 0 | Documentation |
| clean_install.sh | 15 | 0 | 0 | 0 | Scripting |
| codebase_analysis_report.txt | 367 | 0 | 0 | 0 | Other |
| codebase_issues.json | 460 | 0 | 0 | 0 | Configuration |
| component_relationships.md | 190 | 0 | 0 | 0 | Documentation |
| comprehensive_analysis_report.md | 1852 | 0 | 0 | 0 | Documentation |
| conftest.py | 6 | 2 | 0 | 0 | Testing |
| constitution-update-prompt.md | 56 | 0 | 0 | 0 | Documentation |
| data_flow.md | 265 | 0 | 0 | 0 | Documentation |
| demo_mfa.py | 70 | 3 | 0 | 0 | Core Logic |
| deploy.sh | 239 | 0 | 0 | 0 | Scripting |
| dev.py | 130 | 2 | 10 | 0 | Core Logic |
| docker-compose.prod.yml | 87 | 0 | 0 | 0 | Configuration |
| emailintelligence_cli.py | 1755 | 26 | 41 | 1 | Core Logic |
| error_log.jsonl | 0 | 0 | 0 | 0 | Data |
| final_merge_approach.md | 185 | 0 | 0 | 0 | Documentation |
| fixed_settings.json | 79 | 0 | 0 | 0 | Configuration |
| jules_mcp_schedule.json | 636 | 0 | 0 | 0 | Configuration |
| jules_prompts_formatted.txt | 72 | 0 | 0 | 0 | Other |
| key_modules.md | 338 | 0 | 0 | 0 | Documentation |
| launch.bat | 13 | 0 | 0 | 0 | Scripting |
| launch.bat.new | 133 | 0 | 0 | 0 | Other |
| launch.py | 27 | 3 | 0 | 0 | Core Logic |
| launch.sh | 10 | 0 | 0 | 0 | Scripting |
| merge_direction_plan.md | 56 | 0 | 0 | 0 | Documentation |
| opencode.json | 23 | 0 | 0 | 0 | Configuration |
| orchestration_tools_branch_analysis.md | 58 | 0 | 0 | 0 | Documentation |
| package.json | 24 | 0 | 0 | 0 | Configuration |
| performance-results.json | 230 | 0 | 0 | 0 | Configuration |
| pyproject.toml | 142 | 0 | 0 | 0 | Configuration |
| pytest.ini | 15 | 0 | 0 | 0 | Testing |
| requirements-conditional.txt | 21 | 0 | 0 | 0 | Other |
| requirements-dev.txt | 20 | 0 | 0 | 0 | Other |
| rulesync.jsonc | 24 | 0 | 0 | 0 | Other |
| run_cleanup.py | 112 | 6 | 1 | 0 | Core Logic |
| scientific_branch_analysis.md | 48 | 0 | 0 | 0 | Documentation |
| scientific_branch_features.md | 73 | 0 | 0 | 0 | Documentation |
| setup.cfg | 70 | 0 | 0 | 0 | Other |
| setup_agent_env.sh | 32 | 0 | 0 | 0 | Scripting |
| sgconfig.yml | 10 | 0 | 0 | 0 | Configuration |
| speckit-plan-prompt.md | 47 | 0 | 0 | 0 | Documentation |
| subtree_integration_scientific.sh | 19 | 0 | 0 | 0 | Scripting |
| subtree_integration_scientific_branch.sh | 19 | 0 | 0 | 0 | Scripting |
| system_vs_pip_requirements.txt | 110 | 0 | 0 | 0 | Other |
| task_verification_report.md | 110 | 0 | 0 | 0 | Documentation |
| technology_stack.md | 383 | 0 | 0 | 0 | Documentation |
| test-improvement-plan.md | 233 | 0 | 0 | 0 | Testing |
| test-migration-plan-updated.md | 100 | 0 | 0 | 0 | Testing |
| test-migration-plan.md | 100 | 0 | 0 | 0 | Testing |
| test-path-issues-plan.md | 247 | 0 | 0 | 0 | Testing |
| uv.lock | 4421 | 0 | 0 | 0 | Other |
| validate_architecture_alignment.py | 172 | 16 | 6 | 0 | Core Logic |
| validate_dependencies.py | 55 | 3 | 1 | 0 | Core Logic |
| verify_packages.py | 121 | 5 | 2 | 0 | Core Logic |

### Directory: `.agents/commands`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| speckit.analyze.md | 184 | 0 | 0 | 0 | Documentation |
| speckit.checklist.md | 295 | 0 | 0 | 0 | Documentation |
| speckit.clarify.md | 181 | 0 | 0 | 0 | Documentation |
| speckit.constitution.md | 84 | 0 | 0 | 0 | Documentation |
| speckit.implement.md | 198 | 0 | 0 | 0 | Documentation |
| speckit.plan.md | 90 | 0 | 0 | 0 | Documentation |
| speckit.specify.md | 237 | 0 | 0 | 0 | Documentation |
| speckit.tasks.md | 200 | 0 | 0 | 0 | Documentation |
| speckit.taskstoissues.md | 30 | 0 | 0 | 0 | Documentation |

### Directory: `.claude`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mcp.json | 0 | 0 | 0 | 0 | Configuration |
| settings.json | 15 | 0 | 0 | 0 | Configuration |
| settings.local.json | 7 | 0 | 0 | 0 | Configuration |
| slash_commands.json | 100 | 0 | 0 | 0 | Configuration |

### Directory: `.claude/agents`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| planner.md | 13 | 0 | 0 | 0 | Documentation |

### Directory: `.claude/commands`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| review-pr.md | 15 | 0 | 0 | 0 | Documentation |

### Directory: `.claude/memories`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CLAUDE.md | 3 | 0 | 0 | 0 | Documentation |

### Directory: `.clinerules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cline_rules.md | 53 | 0 | 0 | 0 | Documentation |
| dev_workflow.md | 424 | 0 | 0 | 0 | Documentation |
| self_improve.md | 72 | 0 | 0 | 0 | Documentation |
| taskmaster.md | 558 | 0 | 0 | 0 | Documentation |

### Directory: `.context-control/profiles`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| main.json | 54 | 0 | 0 | 0 | Configuration |
| orchestration-tools.json | 44 | 0 | 0 | 0 | Configuration |
| scientific.json | 58 | 0 | 0 | 0 | Configuration |

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

### Directory: `.crush`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitignore | 1 | 0 | 0 | 0 | Other |
| crush.db | 216 | 0 | 0 | 0 | Data |
| init | 0 | 0 | 0 | 0 | Other |

### Directory: `.cursor`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mcp.json | 0 | 0 | 0 | 0 | Configuration |

### Directory: `.cursor/commands`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| review-pr.md | 12 | 0 | 0 | 0 | Documentation |

### Directory: `.cursor/rules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| overview.mdc | 29 | 0 | 0 | 0 | Other |

### Directory: `.cursor/rules/taskmaster`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dev_workflow.mdc | 424 | 0 | 0 | 0 | Other |
| taskmaster.mdc | 558 | 0 | 0 | 0 | Other |

### Directory: `.gemini`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| settings.json | 7 | 0 | 0 | 0 | Configuration |

### Directory: `.gemini/commands`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| speckit.analyze.toml | 188 | 0 | 0 | 0 | Configuration |
| speckit.checklist.toml | 299 | 0 | 0 | 0 | Configuration |
| speckit.clarify.toml | 185 | 0 | 0 | 0 | Configuration |
| speckit.constitution.toml | 88 | 0 | 0 | 0 | Configuration |
| speckit.implement.toml | 202 | 0 | 0 | 0 | Configuration |
| speckit.plan.toml | 94 | 0 | 0 | 0 | Configuration |
| speckit.specify.toml | 241 | 0 | 0 | 0 | Configuration |
| speckit.tasks.toml | 204 | 0 | 0 | 0 | Configuration |
| speckit.taskstoissues.toml | 34 | 0 | 0 | 0 | Configuration |

### Directory: `.github`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| BRANCH_PROPAGATION_POLICY.md | 409 | 0 | 0 | 0 | Documentation |
| DOCUMENTATION_DISTRIBUTION_REPORT.md | 200 | 0 | 0 | 0 | Documentation |
| PROPAGATION_SETUP_CHECKLIST.md | 375 | 0 | 0 | 0 | Documentation |
| copilot-instructions.md | 28 | 0 | 0 | 0 | Documentation |
| dependabot.yml | 49 | 0 | 0 | 0 | Configuration |

### Directory: `.github/instructions`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| GEMINI.instructions.md | 32 | 0 | 0 | 0 | Documentation |
| copilot-instructions.instructions.md | 32 | 0 | 0 | 0 | Documentation |
| dev_workflow.instructions.md | 423 | 0 | 0 | 0 | Documentation |
| self_improve.instructions.md | 71 | 0 | 0 | 0 | Documentation |
| taskmaster.instructions.md | 557 | 0 | 0 | 0 | Documentation |
| tools-manifest.json | 279 | 0 | 0 | 0 | Configuration |
| vscode_rules.instructions.md | 52 | 0 | 0 | 0 | Documentation |

### Directory: `.github/prompts`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| review-pr.prompt.md | 16 | 0 | 0 | 0 | Documentation |

### Directory: `.github/pull_request_templates`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| orchestration-pr.md | 115 | 0 | 0 | 0 | Documentation |

### Directory: `.github/workflows`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ci.yml | 270 | 0 | 0 | 0 | Configuration |
| extract-orchestration-changes.yml | 195 | 0 | 0 | 0 | Configuration |
| lint.yml | 56 | 0 | 0 | 0 | Configuration |
| test.yml | 57 | 0 | 0 | 0 | Testing |

### Directory: `.iflow`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| files_main.txt | 641 | 0 | 0 | 0 | Other |
| files_main_sorted.txt | 641 | 0 | 0 | 0 | Other |
| files_scientific.txt | 1149 | 0 | 0 | 0 | Other |
| files_scientific_sorted.txt | 1149 | 0 | 0 | 0 | Other |
| frontend_analyze.py | 89 | 4 | 3 | 0 | Core Logic |
| handoff.json | 1 | 0 | 0 | 0 | Configuration |
| quick_analyze.py | 84 | 4 | 1 | 0 | Core Logic |
| session.json | 1 | 0 | 0 | 0 | Configuration |
| src_main.txt | 173 | 0 | 0 | 0 | Other |
| src_orchestration.txt | 45 | 0 | 0 | 0 | Other |
| src_scientific.txt | 190 | 0 | 0 | 0 | Other |
| standard_analyze.py | 106 | 5 | 2 | 0 | Core Logic |
| state.json | 1 | 0 | 0 | 0 | Configuration |
| state.json.backup | 1 | 0 | 0 | 0 | Other |

### Directory: `.iflow/commands`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cleanproject.toml | 11 | 0 | 0 | 0 | Configuration |
| create-todos.toml | 11 | 0 | 0 | 0 | Configuration |
| fix-imports.toml | 11 | 0 | 0 | 0 | Configuration |
| fix-todos.toml | 11 | 0 | 0 | 0 | Configuration |
| format.toml | 11 | 0 | 0 | 0 | Configuration |
| implement.toml | 11 | 0 | 0 | 0 | Configuration |
| predict-issues.toml | 11 | 0 | 0 | 0 | Configuration |
| refactor.toml | 11 | 0 | 0 | 0 | Configuration |
| review.toml | 11 | 0 | 0 | 0 | Configuration |
| scaffold.toml | 11 | 0 | 0 | 0 | Configuration |
| test.toml | 11 | 0 | 0 | 0 | Testing |
| understand.toml | 11 | 0 | 0 | 0 | Configuration |
| undo.toml | 11 | 0 | 0 | 0 | Configuration |

### Directory: `.iflow/tmp_sync/client/src/components`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| advanced-filter-panel.tsx | 451 | 0 | 0 | 0 | Frontend |
| ai-analysis-panel.tsx | 452 | 0 | 0 | 0 | Frontend |
| email-list.tsx | 175 | 0 | 0 | 0 | Frontend |

### Directory: `.iflow/tmp_sync/src`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |

### Directory: `.iflow/tmp_sync/src/core`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |

### Directory: `.iflow/understand`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| frontend_analysis.json | 115 | 0 | 0 | 0 | Configuration |
| quick_analysis.json | 73 | 0 | 0 | 0 | Configuration |
| standard_analysis.json | 171 | 0 | 0 | 0 | Configuration |

### Directory: `.kilo`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mcp.json | 18 | 0 | 0 | 0 | Configuration |

### Directory: `.kilo/rules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .kilocodemodes | 63 | 0 | 0 | 0 | Other |
| dev_workflow.md | 424 | 0 | 0 | 0 | Documentation |
| kilo_rules.md | 53 | 0 | 0 | 0 | Documentation |
| self_improve.md | 72 | 0 | 0 | 0 | Documentation |
| taskmaster.md | 558 | 0 | 0 | 0 | Documentation |

### Directory: `.kilo/rules/.kilo/rules-architect`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| architect-rules | 93 | 0 | 0 | 0 | Other |

### Directory: `.kilo/rules/.kilo/rules-ask`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ask-rules | 89 | 0 | 0 | 0 | Other |

### Directory: `.kilo/rules/.kilo/rules-code`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| code-rules | 61 | 0 | 0 | 0 | Other |

### Directory: `.kilo/rules/.kilo/rules-debug`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| debug-rules | 68 | 0 | 0 | 0 | Other |

### Directory: `.kilo/rules/.kilo/rules-orchestrator`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| orchestrator-rules | 181 | 0 | 0 | 0 | Other |

### Directory: `.kilo/rules/.kilo/rules-test`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test-rules | 61 | 0 | 0 | 0 | Testing |

### Directory: `.kilocode/workflows`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| speckit.analyze.md | 184 | 0 | 0 | 0 | Documentation |
| speckit.checklist.md | 295 | 0 | 0 | 0 | Documentation |
| speckit.clarify.md | 181 | 0 | 0 | 0 | Documentation |
| speckit.constitution.md | 84 | 0 | 0 | 0 | Documentation |
| speckit.implement.md | 198 | 0 | 0 | 0 | Documentation |
| speckit.plan.md | 90 | 0 | 0 | 0 | Documentation |
| speckit.specify.md | 237 | 0 | 0 | 0 | Documentation |
| speckit.tasks.md | 200 | 0 | 0 | 0 | Documentation |
| speckit.taskstoissues.md | 30 | 0 | 0 | 0 | Documentation |

### Directory: `.kiro/settings`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mcp.json | 17 | 0 | 0 | 0 | Configuration |

### Directory: `.kiro/steering`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dev_workflow.md | 422 | 0 | 0 | 0 | Documentation |
| kiro_rules.md | 51 | 0 | 0 | 0 | Documentation |
| self_improve.md | 70 | 0 | 0 | 0 | Documentation |
| taskmaster.md | 556 | 0 | 0 | 0 | Documentation |
| taskmaster_hooks_workflow.md | 59 | 0 | 0 | 0 | Documentation |

### Directory: `.kiro/steering/.kiro/hooks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| tm-code-change-task-tracker.kiro.hook | 23 | 0 | 0 | 0 | Other |
| tm-complexity-analyzer.kiro.hook | 16 | 0 | 0 | 0 | Other |
| tm-daily-standup-assistant.kiro.hook | 13 | 0 | 0 | 0 | Other |
| tm-git-commit-task-linker.kiro.hook | 13 | 0 | 0 | 0 | Other |
| tm-pr-readiness-checker.kiro.hook | 13 | 0 | 0 | 0 | Other |
| tm-task-dependency-auto-progression.kiro.hook | 17 | 0 | 0 | 0 | Other |
| tm-test-success-task-completer.kiro.hook | 23 | 0 | 0 | 0 | Testing |

### Directory: `.opencode/command`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| speckit.analyze.md | 184 | 0 | 0 | 0 | Documentation |
| speckit.checklist.md | 294 | 0 | 0 | 0 | Documentation |
| speckit.clarify.md | 177 | 0 | 0 | 0 | Documentation |
| speckit.constitution.md | 78 | 0 | 0 | 0 | Documentation |
| speckit.implement.md | 134 | 0 | 0 | 0 | Documentation |
| speckit.plan.md | 81 | 0 | 0 | 0 | Documentation |
| speckit.specify.md | 249 | 0 | 0 | 0 | Documentation |
| speckit.tasks.md | 128 | 0 | 0 | 0 | Documentation |

### Directory: `.pytest_cache`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitignore | 2 | 0 | 0 | 0 | Testing |
| CACHEDIR.TAG | 4 | 0 | 0 | 0 | Testing |
| README.md | 8 | 0 | 0 | 0 | Testing |

### Directory: `.pytest_cache/v/cache`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| lastfailed | 4 | 0 | 0 | 0 | Testing |
| nodeids | 78 | 0 | 0 | 0 | Testing |

### Directory: `.qwen`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| PROJECT_SUMMARY.md | 48 | 0 | 0 | 0 | Documentation |

### Directory: `.qwen/commands`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| speckit.analyze.md | 184 | 0 | 0 | 0 | Documentation |
| speckit.analyze.toml | 188 | 0 | 0 | 0 | Configuration |
| speckit.checklist.md | 295 | 0 | 0 | 0 | Documentation |
| speckit.checklist.toml | 298 | 0 | 0 | 0 | Configuration |
| speckit.clarify.md | 181 | 0 | 0 | 0 | Documentation |
| speckit.clarify.toml | 181 | 0 | 0 | 0 | Configuration |
| speckit.constitution.md | 84 | 0 | 0 | 0 | Documentation |
| speckit.constitution.toml | 82 | 0 | 0 | 0 | Configuration |
| speckit.implement.md | 198 | 0 | 0 | 0 | Documentation |
| speckit.implement.toml | 138 | 0 | 0 | 0 | Configuration |
| speckit.plan.md | 90 | 0 | 0 | 0 | Documentation |
| speckit.plan.toml | 85 | 0 | 0 | 0 | Configuration |
| speckit.specify.md | 237 | 0 | 0 | 0 | Documentation |
| speckit.specify.toml | 253 | 0 | 0 | 0 | Configuration |
| speckit.tasks.md | 200 | 0 | 0 | 0 | Documentation |
| speckit.tasks.toml | 132 | 0 | 0 | 0 | Configuration |
| speckit.taskstoissues.md | 30 | 0 | 0 | 0 | Documentation |

### Directory: `.roo`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mcp.json | 0 | 0 | 0 | 0 | Configuration |

### Directory: `.roo/rules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .roomodes | 63 | 0 | 0 | 0 | Other |
| dev_workflow.md | 424 | 0 | 0 | 0 | Documentation |
| roo_rules.md | 53 | 0 | 0 | 0 | Documentation |
| self_improve.md | 72 | 0 | 0 | 0 | Documentation |
| taskmaster.md | 558 | 0 | 0 | 0 | Documentation |

### Directory: `.roo/rules/.roo/rules-architect`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| architect-rules | 93 | 0 | 0 | 0 | Other |

### Directory: `.roo/rules/.roo/rules-ask`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ask-rules | 89 | 0 | 0 | 0 | Other |

### Directory: `.roo/rules/.roo/rules-code`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| code-rules | 61 | 0 | 0 | 0 | Other |

### Directory: `.roo/rules/.roo/rules-debug`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| debug-rules | 68 | 0 | 0 | 0 | Other |

### Directory: `.roo/rules/.roo/rules-orchestrator`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| orchestrator-rules | 181 | 0 | 0 | 0 | Other |

### Directory: `.roo/rules/.roo/rules-test`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test-rules | 61 | 0 | 0 | 0 | Testing |

### Directory: `.ruff_cache`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitignore | 2 | 0 | 0 | 0 | Other |
| CACHEDIR.TAG | 1 | 0 | 0 | 0 | Other |

### Directory: `.ruff_cache/0.14.10`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| 10074526889056373008 | 17 | 0 | 0 | 0 | Other |
| 10090424261998791292 | 2 | 0 | 0 | 0 | Other |
| 10159287570972146148 | 2 | 0 | 0 | 0 | Other |
| 10483303256526947496 | 1 | 0 | 0 | 0 | Other |
| 10585835004753270474 | 2 | 0 | 0 | 0 | Other |
| 10642229569607718911 | 1 | 0 | 0 | 0 | Other |
| 1085432852830205942 | 1 | 0 | 0 | 0 | Other |
| 10973792515139830880 | 1 | 0 | 0 | 0 | Other |
| 11317748963155560173 | 1 | 0 | 0 | 0 | Other |
| 11478764486938281372 | 24 | 0 | 0 | 0 | Other |
| 11961822085229237479 | 1 | 0 | 0 | 0 | Other |
| 12478490092352305358 | 2 | 0 | 0 | 0 | Other |
| 126046084490835140 | 1 | 0 | 0 | 0 | Other |
| 13237261251031157075 | 2 | 0 | 0 | 0 | Other |
| 13482880608335345 | 2 | 0 | 0 | 0 | Other |
| 13938506635447158989 | 5 | 0 | 0 | 0 | Other |
| 14418824314438301506 | 4 | 0 | 0 | 0 | Other |
| 14560431637215228077 | 4 | 0 | 0 | 0 | Other |
| 15520426197058315492 | 1 | 0 | 0 | 0 | Other |
| 15823554755784323995 | 1 | 0 | 0 | 0 | Other |
| 16038369326702721236 | 1 | 0 | 0 | 0 | Other |
| 16581802849071738874 | 2 | 0 | 0 | 0 | Other |
| 16703984187048524148 | 2 | 0 | 0 | 0 | Other |
| 16736629551325607444 | 1 | 0 | 0 | 0 | Other |
| 1709031420654231427 | 2 | 0 | 0 | 0 | Other |
| 17358585691808248675 | 5 | 0 | 0 | 0 | Other |
| 17728491520157068546 | 1 | 0 | 0 | 0 | Other |
| 18325137041709965312 | 2 | 0 | 0 | 0 | Other |
| 2149571910905506680 | 9 | 0 | 0 | 0 | Other |
| 2205636470728397081 | 9 | 0 | 0 | 0 | Other |
| 2332607585877801598 | 1 | 0 | 0 | 0 | Other |
| 3013389352632817965 | 10 | 0 | 0 | 0 | Other |
| 3511618883294768234 | 1 | 0 | 0 | 0 | Other |
| 4225204078100217370 | 5 | 0 | 0 | 0 | Other |
| 438604568576250025 | 2 | 0 | 0 | 0 | Other |
| 4667264393983927068 | 1 | 0 | 0 | 0 | Other |
| 4797500528487062914 | 1 | 0 | 0 | 0 | Other |
| 5498880991644548069 | 2 | 0 | 0 | 0 | Other |
| 6091321548498202061 | 1 | 0 | 0 | 0 | Other |
| 6560548821118210143 | 1 | 0 | 0 | 0 | Other |
| 6583107264964235307 | 4 | 0 | 0 | 0 | Other |
| 660112178920572340 | 1 | 0 | 0 | 0 | Other |
| 7439783599119309513 | 1 | 0 | 0 | 0 | Other |
| 788677320174218921 | 1 | 0 | 0 | 0 | Other |
| 9100876846231072178 | 2 | 0 | 0 | 0 | Other |
| 9196605426266870903 | 1 | 0 | 0 | 0 | Other |
| 9216519139500572304 | 3 | 0 | 0 | 0 | Other |
| 974219892935286407 | 12 | 0 | 0 | 0 | Other |

### Directory: `.ruff_cache/0.15.6`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| 5141750204632370518 | 1 | 0 | 0 | 0 | Other |
| 8436066817982908242 | 2 | 0 | 0 | 0 | Other |

### Directory: `.rulesync`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .mcp.json | 30 | 0 | 0 | 0 | Configuration |

### Directory: `.rulesync/commands`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| review-pr.toml | 17 | 0 | 0 | 0 | Configuration |

### Directory: `.rulesync/rules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CLAUDE.md | 11 | 0 | 0 | 0 | Documentation |
| copilot-instructions.md | 36 | 0 | 0 | 0 | Documentation |

### Directory: `.serena`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitignore | 1 | 0 | 0 | 0 | Other |
| project.yml | 84 | 0 | 0 | 0 | Configuration |

### Directory: `.sisyphus`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| boulder.json | 10 | 0 | 0 | 0 | Configuration |

### Directory: `.sisyphus/backups/20260315`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| GAP_ANALYSIS.md | 536 | 0 | 0 | 0 | Documentation |
| constitution.md | 315 | 0 | 0 | 0 | Documentation |
| spec.md | 362 | 0 | 0 | 0 | Documentation |

### Directory: `.sisyphus/plans`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constitution-update-plan.md | 134 | 0 | 0 | 0 | Documentation |

### Directory: `.specify`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| init-options.json | 9 | 0 | 0 | 0 | Configuration |

### Directory: `.specify/memory`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constitution.md | 315 | 0 | 0 | 0 | Documentation |
| constitution.md.backup | 131 | 0 | 0 | 0 | Other |

### Directory: `.specify/scripts/bash`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| check-prerequisites.sh | 190 | 0 | 0 | 0 | Scripting |
| common.sh | 253 | 0 | 0 | 0 | Scripting |
| create-new-feature.sh | 333 | 0 | 0 | 0 | Scripting |
| setup-plan.sh | 73 | 0 | 0 | 0 | Scripting |
| update-agent-context.sh | 808 | 0 | 0 | 0 | Scripting |

### Directory: `.specify/templates`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| agent-file-template.md | 28 | 0 | 0 | 0 | Documentation |
| checklist-template.md | 40 | 0 | 0 | 0 | Documentation |
| constitution-template.md | 50 | 0 | 0 | 0 | Documentation |
| plan-template.md | 104 | 0 | 0 | 0 | Documentation |
| spec-template.md | 115 | 0 | 0 | 0 | Documentation |
| tasks-template.md | 251 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .ckignore | 65 | 0 | 0 | 0 | Other |
| .flake8 | 4 | 0 | 0 | 0 | Other |
| .git | 1 | 0 | 0 | 0 | Other |
| .gitattributes | 3 | 0 | 0 | 0 | Other |
| .gitignore | 149 | 0 | 0 | 0 | Other |
| .pylintrc | 22 | 0 | 0 | 0 | Other |
| AGENT.md | 579 | 0 | 0 | 0 | Documentation |
| AGENTS.md | 864 | 0 | 0 | 0 | Documentation |
| CLAUDE.md | 629 | 0 | 0 | 0 | Documentation |
| COMBINED_UNFINISHED_WORK.md | 267 | 0 | 0 | 0 | Documentation |
| GEMINI.md | 82 | 0 | 0 | 0 | Documentation |
| IFLOW.md | 731 | 0 | 0 | 0 | Documentation |
| OLD_TASK_NUMBERING_DEPRECATED.md | 243 | 0 | 0 | 0 | Documentation |
| OPTION_C_VISUAL_MAP.md | 577 | 0 | 0 | 0 | Documentation |
| PRD_IMPROVEMENT_INVESTIGATION.md | 468 | 0 | 0 | 0 | Documentation |
| PROJECT_IDENTITY.md | 114 | 0 | 0 | 0 | Documentation |
| QUICK_START.md | 93 | 0 | 0 | 0 | Documentation |
| QWEN.md | 530 | 0 | 0 | 0 | Documentation |
| README.md | 28 | 0 | 0 | 0 | Documentation |
| RISK_MINIMIZATION_PLAN.md | 682 | 0 | 0 | 0 | Documentation |
| ROUNDTRIP_FIDELITY_TEST_RESULTS.md | 374 | 0 | 0 | 0 | Testing |
| TASKMASTER_HANDOFF.md | 296 | 0 | 0 | 0 | Documentation |
| TASK_PRD_DIFF_COMPARISON.md | 586 | 0 | 0 | 0 | Documentation |
| TASK_STRUCTURE_STANDARD.md | 554 | 0 | 0 | 0 | Documentation |
| UNFINISHED_TASKS_CONSOLIDATED.md | 495 | 0 | 0 | 0 | Documentation |
| config.json | 49 | 0 | 0 | 0 | Configuration |
| emailintelligence_cli.py | 1746 | 29 | 43 | 1 | Core Logic |
| generated_prd_all_tasks.md | 9541 | 0 | 0 | 0 | Documentation |
| generated_prd_from_tasks.md | 158 | 0 | 0 | 0 | Documentation |
| opencode.json | 12 | 0 | 0 | 0 | Configuration |
| pyproject.toml | 42 | 0 | 0 | 0 | Configuration |
| requirements.txt | 6 | 0 | 0 | 0 | Other |
| state.json | 6 | 0 | 0 | 0 | Configuration |
| taskmaster_cli.py | 301 | 6 | 3 | 0 | Core Logic |
| test_generated_prd.md | 319 | 0 | 0 | 0 | Testing |
| test_roundtrip_prd.md | 543 | 0 | 0 | 0 | Testing |

### Directory: `.taskmaster/.agent_memory`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ARCHITECTURE.md | 457 | 0 | 0 | 0 | Documentation |
| IMPLEMENTATION_LAYOUT.md | 96 | 0 | 0 | 0 | Documentation |
| MEMORY_SYSTEM_GUIDE.md | 430 | 0 | 0 | 0 | Documentation |
| QUICK_REFERENCE.md | 158 | 0 | 0 | 0 | Documentation |
| README.md | 246 | 0 | 0 | 0 | Documentation |
| REVIEW_SUMMARY.md | 228 | 0 | 0 | 0 | Documentation |
| SCOPE_AND_DESIGN.md | 255 | 0 | 0 | 0 | Documentation |
| STATUS.txt | 167 | 0 | 0 | 0 | Other |
| VALIDATION_REPORT.md | 418 | 0 | 0 | 0 | Documentation |
| example_usage.py | 270 | 2 | 8 | 0 | Core Logic |
| memory_api.py | 406 | 5 | 20 | 1 | Core Logic |

### Directory: `.taskmaster/.beads`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitignore | 48 | 0 | 0 | 0 | Other |
| .jsonl.lock | 0 | 0 | 0 | 0 | Other |
| README.md | 81 | 0 | 0 | 0 | Documentation |
| daemon-error | 23 | 0 | 0 | 0 | Other |
| interactions.jsonl | 0 | 0 | 0 | 0 | Data |
| issues.jsonl | 0 | 0 | 0 | 0 | Data |

### Directory: `.taskmaster/.gemini`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ralph-loop.local.md | 52 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/.iflow`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| TODO_ORGANIZATION_REPORT.md | 433 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/.iflow/predictions`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| report-20250106.md | 928 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/.iflow/understand`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| architecture.md | 908 | 0 | 0 | 0 | Documentation |
| diagrams.mermaid | 642 | 0 | 0 | 0 | Other |
| enhanced_architecture.md | 482 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/.qwen`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| PROJECT_SUMMARY.md | 37 | 0 | 0 | 0 | Documentation |
| README.md | 87 | 0 | 0 | 0 | Documentation |
| review_report.md | 306 | 0 | 0 | 0 | Documentation |
| session_cli.py | 113 | 4 | 5 | 0 | Core Logic |
| session_manager.py | 240 | 5 | 10 | 1 | Core Logic |
| state.json.backup | 20 | 0 | 0 | 0 | Other |
| test_session_manager.py | 147 | 5 | 3 | 0 | Testing |

### Directory: `.taskmaster/.qwen/optimize`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| optimizations.md | 421 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/.qwen/predictions`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| report-2026-02-19.md | 399 | 0 | 0 | 0 | Documentation |
| report-20260116_155100.md | 170 | 0 | 0 | 0 | Documentation |
| summary-20260116_155100.csv | 30 | 0 | 0 | 0 | Data |

### Directory: `.taskmaster/.qwen/understand`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| QUICK_SUMMARY.md | 206 | 0 | 0 | 0 | Documentation |
| architecture_analysis.md | 680 | 0 | 0 | 0 | Documentation |
| diagrams.mermaid | 248 | 0 | 0 | 0 | Other |

### Directory: `.taskmaster/.taskmaster/tasks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-7.md | 1051 | 0 | 0 | 0 | Documentation |
| tasks.json.roundtrip_backup | 1 | 0 | 0 | 0 | Other |

### Directory: `.taskmaster/archive`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ARCHIVE_MANIFEST.md | 248 | 0 | 0 | 0 | Documentation |
| README.md | 277 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/cleanup_work`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CLEANUP_BEFORE_AFTER.md | 266 | 0 | 0 | 0 | Documentation |
| CLEANUP_NON_ALIGNMENT_TASKS.md | 280 | 0 | 0 | 0 | Documentation |
| CLEANUP_SCRIPT.sh | 132 | 0 | 0 | 0 | Scripting |
| CLEANUP_STATUS_FINAL.md | 325 | 0 | 0 | 0 | Documentation |
| CLEANUP_VERIFICATION_FINAL.txt | 385 | 0 | 0 | 0 | Other |
| CLEANUP_VERIFICATION_REPORT.md | 416 | 0 | 0 | 0 | Documentation |
| COMPLETION_STATUS.md | 372 | 0 | 0 | 0 | Documentation |
| COMPLETION_SUMMARY.txt | 233 | 0 | 0 | 0 | Other |
| EXECUTIVE_CLEANUP_SUMMARY.md | 329 | 0 | 0 | 0 | Documentation |
| SESSION_COMPLETION_SUMMARY.md | 427 | 0 | 0 | 0 | Documentation |
| VALIDATION_REPORT.md | 340 | 0 | 0 | 0 | Documentation |
| VERIFY_ORCHESTRATION_TOOLS_CLEAN.md | 386 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/deprecated_numbering`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| INDEX.md | 59 | 0 | 0 | 0 | Documentation |
| NEW_TASK_PLAN_EVALUATION_AND_PROCESSING_PLAN.md | 452 | 0 | 0 | 0 | Documentation |
| ROOT_CAUSE_ANALYSIS_TASK_NUMBERING.md | 470 | 0 | 0 | 0 | Documentation |
| TASK_75_CLEANUP_AND_RENUMBERING_PLAN.md | 409 | 0 | 0 | 0 | Documentation |
| TASK_ID_MIGRATION_QUICK_REFERENCE.md | 136 | 0 | 0 | 0 | Documentation |
| TASK_NUMBERING_IMPLEMENTATION_CHECKLIST.md | 553 | 0 | 0 | 0 | Documentation |
| TASK_NUMBERING_ISSUE_ANALYSIS.md | 256 | 0 | 0 | 0 | Documentation |
| TASK_RETROFIT_PLAN.md | 318 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/integration_work`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| HANDOFF_INTEGRATION_BEFORE_AFTER.md | 586 | 0 | 0 | 0 | Documentation |
| HANDOFF_INTEGRATION_COMPLETE.md | 371 | 0 | 0 | 0 | Documentation |
| INTEGRATION_DOCUMENTATION_INDEX.md | 496 | 0 | 0 | 0 | Documentation |
| INTEGRATION_GUIDE_SUMMARY.md | 407 | 0 | 0 | 0 | Documentation |
| INTEGRATION_PLAN_MANIFEST.md | 403 | 0 | 0 | 0 | Documentation |
| INTEGRATION_TRACKING.md | 450 | 0 | 0 | 0 | Documentation |
| MIGRATION_ANALYSIS_AND_FIX.md | 345 | 0 | 0 | 0 | Documentation |
| MIGRATION_COMPLETION_REPORT.md | 514 | 0 | 0 | 0 | Documentation |
| MIGRATION_VERIFICATION_COMPLETE.md | 314 | 0 | 0 | 0 | Documentation |
| NEW_TASK_FOLDER_SYNC_COMPLETION_REPORT.md | 402 | 0 | 0 | 0 | Documentation |
| README_INTEGRATION_COMPLETE.md | 465 | 0 | 0 | 0 | Documentation |
| RESOLVED_TASK_002_INTEGRATION_PLAN_historical_reference.md | 557 | 0 | 0 | 0 | Documentation |
| RESOLVED_UNIFIED_TASK_MD_STRUCTURE_historical_reference.md | 736 | 0 | 0 | 0 | Documentation |
| START_HERE_INTEGRATION.md | 361 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/investigation_work`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AGENT_GUIDANCE_PLAN.md | 74 | 0 | 0 | 0 | Documentation |
| AGENT_MEMORY_IMPLEMENTATION_SUMMARY.md | 416 | 0 | 0 | 0 | Documentation |
| AGENT_MEMORY_INVESTIGATION_REPORT.md | 605 | 0 | 0 | 0 | Documentation |
| COMPLETE_ANALYSIS_INDEX.md | 527 | 0 | 0 | 0 | Documentation |
| COMPLETE_READING_SUMMARY.md | 272 | 0 | 0 | 0 | Documentation |
| CONSOLIDATED_INVESTIGATION_RESOLUTION.md | 289 | 0 | 0 | 0 | Documentation |
| FINDINGS_GUIDE.md | 264 | 0 | 0 | 0 | Documentation |
| INVESTIGATION_INDEX.md | 360 | 0 | 0 | 0 | Documentation |
| INVESTIGATION_SUMMARY.md | 546 | 0 | 0 | 0 | Documentation |
| QUICK_DIAGNOSIS_GUIDE.md | 421 | 0 | 0 | 0 | Documentation |
| ROOT_CAUSE_AND_FIX_ANALYSIS.md | 362 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/phase_planning`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CURRENT_STATUS_PHASE_1.5_COMPLETE.md | 292 | 0 | 0 | 0 | Documentation |
| PARALLEL_WORK_STATUS.md | 321 | 0 | 0 | 0 | Documentation |
| PHASES_1_5_2_4_COMPLETE.txt | 261 | 0 | 0 | 0 | Other |
| PHASES_1_5_2_4_COMPLETE_EXECUTIVE_SUMMARY.md | 323 | 0 | 0 | 0 | Documentation |
| PHASES_2_4_EXECUTION_COMPLETE.md | 316 | 0 | 0 | 0 | Documentation |
| PHASE_1.5_COMPLETION_SUMMARY.txt | 370 | 0 | 0 | 0 | Other |
| PHASE_1_IMPLEMENTATION_COMPLETE.md | 390 | 0 | 0 | 0 | Documentation |
| PHASE_1_STATUS_SUMMARY.md | 291 | 0 | 0 | 0 | Documentation |
| PHASE_2_4_DECISION_FRAMEWORK.md | 409 | 0 | 0 | 0 | Documentation |
| PHASE_4_DEFERRED.md | 134 | 0 | 0 | 0 | Documentation |
| START_HERE_PHASE_1.5.md | 272 | 0 | 0 | 0 | Documentation |
| TEAM_BRIEFING_PHASE_1.5.md | 273 | 0 | 0 | 0 | Documentation |
| WS2-COMPLETE-PROJECT-SUMMARY.md | 391 | 0 | 0 | 0 | Documentation |
| WS2-FINAL-COMPLETION-REPORT.md | 423 | 0 | 0 | 0 | Documentation |
| WS2-PHASE1-COMPLETION-REPORT.md | 244 | 0 | 0 | 0 | Documentation |
| WS2-PHASE1-EXECUTION-LOG.md | 249 | 0 | 0 | 0 | Documentation |
| WS2-PHASE1-ROBUSTNESS-STRATEGY.md | 280 | 0 | 0 | 0 | Documentation |
| WS2-PHASE2-FILE-RENAMES-PLAN.md | 147 | 0 | 0 | 0 | Documentation |
| WS2-PHASE3-SYSTEM-UPDATES-PLAN.md | 209 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/prd_iterations`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| advanced_generated_prd_iteration_1.md | 4101 | 0 | 0 | 0 | Documentation |
| advanced_generated_prd_iteration_2.md | 4110 | 0 | 0 | 0 | Documentation |
| advanced_generated_prd_iteration_3.md | 4110 | 0 | 0 | 0 | Documentation |
| advanced_generated_prd_iteration_4.md | 4110 | 0 | 0 | 0 | Documentation |
| advanced_generated_prd_iteration_5.md | 4110 | 0 | 0 | 0 | Documentation |
| enhanced_generated_prd_iteration_1.md | 3748 | 0 | 0 | 0 | Documentation |
| enhanced_generated_prd_iteration_2.md | 3757 | 0 | 0 | 0 | Documentation |
| enhanced_generated_prd_iteration_3.md | 3757 | 0 | 0 | 0 | Documentation |
| enhanced_generated_prd_iteration_4.md | 3757 | 0 | 0 | 0 | Documentation |
| enhanced_generated_prd_iteration_5.md | 3757 | 0 | 0 | 0 | Documentation |
| generated_prd.md | 138 | 0 | 0 | 0 | Documentation |
| generated_prd_iteration_1.md | 1782 | 0 | 0 | 0 | Documentation |
| generated_prd_iteration_2.md | 1782 | 0 | 0 | 0 | Documentation |
| generated_prd_iteration_3.md | 1782 | 0 | 0 | 0 | Documentation |
| generated_prd_iteration_4.md | 1782 | 0 | 0 | 0 | Documentation |
| generated_prd_iteration_5.md | 1782 | 0 | 0 | 0 | Documentation |
| generated_prd_multi.md | 160 | 0 | 0 | 0 | Documentation |
| roundtrip_test_prd.md | 222 | 0 | 0 | 0 | Testing |
| roundtrip_test_prd_enhanced.md | 12201 | 0 | 0 | 0 | Testing |
| test_enhanced_prd_output.md | 707 | 0 | 0 | 0 | Testing |
| test_enhanced_prd_output_broad.md | 563 | 0 | 0 | 0 | Testing |

### Directory: `.taskmaster/archive/project_docs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| COMPRESSION_GUIDE.md | 350 | 0 | 0 | 0 | Documentation |
| DOCUMENTATION_ROADMAP.md | 539 | 0 | 0 | 0 | Documentation |
| ENHANCED_VALIDATION_PLAN.md | 327 | 0 | 0 | 0 | Documentation |
| EVALUATION_AND_FOLDER_PLAN_SUMMARY.md | 485 | 0 | 0 | 0 | Documentation |
| FILES_CREATED.md | 148 | 0 | 0 | 0 | Documentation |
| GEMINI.md | 289 | 0 | 0 | 0 | Documentation |
| GEMINI.md.disabled | 289 | 0 | 0 | 0 | Documentation |
| HIERARCHY_QUICK_START.md | 356 | 0 | 0 | 0 | Documentation |
| IMPLEMENTATION_DELIVERY_SUMMARY.md | 587 | 0 | 0 | 0 | Documentation |
| IMPLEMENTATION_INDEX.md | 466 | 0 | 0 | 0 | Documentation |
| IMPLEMENTATION_REFERENCE.md | 309 | 0 | 0 | 0 | Documentation |
| IMPLEMENTATION_STATUS.md | 351 | 0 | 0 | 0 | Documentation |
| IMPROVEMENTS_INDEX.md | 410 | 0 | 0 | 0 | Documentation |
| IMPROVEMENTS_QUICK_REFERENCE.md | 310 | 0 | 0 | 0 | Documentation |
| IMPROVEMENTS_SUMMARY.md | 355 | 0 | 0 | 0 | Documentation |
| IMPROVEMENT_CHECKLIST.md | 316 | 0 | 0 | 0 | Documentation |
| IMPROVEMENT_EXAMPLES.md | 765 | 0 | 0 | 0 | Documentation |
| IMPROVEMENT_TEMPLATE.md | 389 | 0 | 0 | 0 | Documentation |
| ISOLATED_TASK_FOLDER_STRUCTURE_PLAN.md | 832 | 0 | 0 | 0 | Documentation |
| PROCESSING_DECISION_SUMMARY.md | 279 | 0 | 0 | 0 | Documentation |
| PROJECT_REFERENCE.md | 568 | 0 | 0 | 0 | Documentation |
| QUICKSTART_IMPROVEMENTS.md | 387 | 0 | 0 | 0 | Documentation |
| QUICK_START_ALL_PHASES.md | 229 | 0 | 0 | 0 | Documentation |
| QUICK_START_APPROVAL_GUIDE.md | 409 | 0 | 0 | 0 | Documentation |
| README_EVALUATION_COMPLETE.md | 337 | 0 | 0 | 0 | Documentation |
| ROOT_MD_REORGANIZATION_PLAN.md | 303 | 0 | 0 | 0 | Documentation |
| START_DEVELOPMENT.md | 386 | 0 | 0 | 0 | Documentation |
| TASK_002_MIGRATION_COMPLETE.md | 370 | 0 | 0 | 0 | Documentation |
| TASK_002_QUICK_START.md | 391 | 0 | 0 | 0 | Documentation |
| TASK_EXECUTION_WORKSPACE_STRUCTURE.md | 1521 | 0 | 0 | 0 | Documentation |
| TASK_HIERARCHY_DOCUMENTATION_INDEX.md | 666 | 0 | 0 | 0 | Documentation |
| TASK_HIERARCHY_VISUAL_MAP.md | 507 | 0 | 0 | 0 | Documentation |
| TOML_VS_NEWTASK_COMPARISON.md | 253 | 0 | 0 | 0 | Documentation |
| plan.md | 387 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/retrofit_work`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| COMPREHENSIVE_RETROFIT_PLAN.md | 478 | 0 | 0 | 0 | Documentation |
| REFACTORING_COMPLETE_GATE_APPROVED.md | 271 | 0 | 0 | 0 | Documentation |
| REFACTORING_STATUS_VERIFIED.md | 259 | 0 | 0 | 0 | Documentation |
| RETROFIT_AUDIT_REPORT.md | 340 | 0 | 0 | 0 | Documentation |
| RETROFIT_COMPLETION_SUMMARY.md | 348 | 0 | 0 | 0 | Documentation |
| RETROFIT_PROGRAM_COMPLETE.md | 350 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/task_context`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| BRANCHES_TO_NEVER_MERGE.md | 160 | 0 | 0 | 0 | Documentation |
| BRANCH_ALIGNMENT_SYSTEM.md | 266 | 0 | 0 | 0 | Documentation |
| BRANCH_ANALYSIS_AND_CLEANUP_RECOMMENDATIONS.md | 546 | 0 | 0 | 0 | Documentation |
| MERGE_ISSUES_REAL_WORLD_RECOVERY.md | 683 | 0 | 0 | 0 | Documentation |
| TASK_75_DOCUMENTATION_INDEX.md | 319 | 0 | 0 | 0 | Documentation |
| TASK_75_NUMBERING_FIX.md | 170 | 0 | 0 | 0 | Documentation |
| TASK_7_IMPLEMENTATION_GUIDE.md | 337 | 0 | 0 | 0 | Documentation |
| TASK_7_QUICK_REFERENCE.md | 339 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/task_data_historical`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| 00_START_HERE.md | 288 | 0 | 0 | 0 | Documentation |
| 00_TASK_STRUCTURE.md | 123 | 0 | 0 | 0 | Documentation |
| CLUSTERING_SYSTEM_SUMMARY.md | 557 | 0 | 0 | 0 | Documentation |
| DELIVERY_CHECKLIST.md | 593 | 0 | 0 | 0 | Documentation |
| HANDOFF_DELIVERY_SUMMARY.md | 508 | 0 | 0 | 0 | Documentation |
| HANDOFF_INDEX.md | 370 | 0 | 0 | 0 | Documentation |
| HANDOFF_INTEGRATION_PLAN.md | 485 | 0 | 0 | 0 | Documentation |
| INTEGRATION_COMPLETE.md | 335 | 0 | 0 | 0 | Documentation |
| INTEGRATION_COMPLETE.txt | 172 | 0 | 0 | 0 | Data |
| INTEGRATION_EXAMPLE.md | 472 | 0 | 0 | 0 | Documentation |
| INTEGRATION_PHASE_COMPLETE.txt | 32 | 0 | 0 | 0 | Data |
| INTEGRATION_QUICK_REFERENCE.md | 319 | 0 | 0 | 0 | Documentation |
| INTEGRATION_STRATEGY.md | 514 | 0 | 0 | 0 | Documentation |
| INTEGRATION_SUMMARY.txt | 230 | 0 | 0 | 0 | Data |
| QUICK_START.md | 518 | 0 | 0 | 0 | Documentation |
| README.md | 520 | 0 | 0 | 0 | Documentation |
| TASK_BREAKDOWN_GUIDE.md | 527 | 0 | 0 | 0 | Documentation |
| TASK_MASTER_AI_WORKFLOW.md | 598 | 0 | 0 | 0 | Documentation |
| branch_clustering_framework.md | 543 | 0 | 0 | 0 | Documentation |
| branch_clustering_implementation.py | 1459 | 11 | 49 | 15 | Core Logic |
| task-7.md | 1051 | 0 | 0 | 0 | Documentation |
| validate_integration.sh | 219 | 0 | 0 | 0 | Scripting |

### Directory: `.taskmaster/archive/task_data_historical/archived/backups_archive_task002`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-002.1.md | 281 | 0 | 0 | 0 | Documentation |
| task-002.2.md | 279 | 0 | 0 | 0 | Documentation |
| task-002.3.md | 312 | 0 | 0 | 0 | Documentation |
| task-002.4.md | 282 | 0 | 0 | 0 | Documentation |
| task-002.5.md | 262 | 0 | 0 | 0 | Documentation |
| task-002.6.md | 317 | 0 | 0 | 0 | Documentation |
| task-002.7.md | 321 | 0 | 0 | 0 | Documentation |
| task-002.8.md | 399 | 0 | 0 | 0 | Documentation |
| task-002.9.md | 508 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/task_data_historical/archived/handoff_archive_task002`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| HANDOFF_002.1_CommitHistoryAnalyzer.md | 139 | 0 | 0 | 0 | Documentation |
| HANDOFF_002.2_CodebaseStructureAnalyzer.md | 194 | 0 | 0 | 0 | Documentation |
| HANDOFF_002.3_DiffDistanceCalculator.md | 228 | 0 | 0 | 0 | Documentation |
| HANDOFF_002.4_BranchClusterer.md | 256 | 0 | 0 | 0 | Documentation |
| HANDOFF_002.5_IntegrationTargetAssigner.md | 342 | 0 | 0 | 0 | Documentation |
| HANDOFF_002.6_PipelineIntegration.md | 388 | 0 | 0 | 0 | Documentation |
| HANDOFF_002.7_VisualizationReporting.md | 368 | 0 | 0 | 0 | Documentation |
| HANDOFF_002.8_TestingSuite.md | 629 | 0 | 0 | 0 | Testing |
| HANDOFF_002.9_FrameworkIntegration.md | 639 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/task_data_historical/archived/task_002_consolidated_v1`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task_002-clustering.md | 966 | 0 | 0 | 0 | Documentation |
| task_002.md | 559 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/archive/task_data_historical/compressed`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| progress_all_20260104_213539.tar.gz | 24 | 0 | 0 | 0 | Data |

### Directory: `.taskmaster/archive/task_data_historical/findings/phase1_foundational`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitkeep | 1 | 0 | 0 | 0 | Data |

### Directory: `.taskmaster/archive/task_data_historical/findings/phase2_assessment`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitkeep | 1 | 0 | 0 | 0 | Data |

### Directory: `.taskmaster/archive/task_data_historical/findings/phase3_build`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitkeep | 1 | 0 | 0 | 0 | Data |

### Directory: `.taskmaster/archive/task_data_historical/findings/phase4_execution`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitkeep | 1 | 0 | 0 | 0 | Data |

### Directory: `.taskmaster/archive/task_data_historical/findings/phase5_finalization`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitkeep | 1 | 0 | 0 | 0 | Data |

### Directory: `.taskmaster/archive/task_data_historical/findings/phase6_maintenance`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitkeep | 1 | 0 | 0 | 0 | Data |

### Directory: `.taskmaster/archive/task_specs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task_spec_012.md | 508 | 0 | 0 | 0 | Documentation |
| task_spec_013.md | 570 | 0 | 0 | 0 | Documentation |
| task_spec_014.md | 605 | 0 | 0 | 0 | Documentation |
| task_spec_015.md | 583 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/complexity_reports`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-001-linting-errors.txt | 104 | 0 | 0 | 0 | Other |

### Directory: `.taskmaster/docs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AGENTIC_CONTAMINATION_ANALYSIS.md | 320 | 0 | 0 | 0 | Documentation |
| ARCHITECTURE_AND_MD_ADJUSTMENT_GUIDE.md | 167 | 0 | 0 | 0 | Documentation |
| ARCHIVE_INVESTIGATION_FINDINGS.md | 670 | 0 | 0 | 0 | Documentation |
| ARCHIVE_INVESTIGATION_SUMMARY.md | 364 | 0 | 0 | 0 | Documentation |
| BEST_PRACTICES_REVIEW_FRAMEWORK.md | 210 | 0 | 0 | 0 | Documentation |
| BRANCH_ANALYSIS_FORWARD_REORGANIZATION_SUMMARY.md | 131 | 0 | 0 | 0 | Documentation |
| BRANCH_ANALYSIS_REORGANIZATION.md | 26 | 0 | 0 | 0 | Documentation |
| BRANCH_ANALYSIS_SUBTASKS_EXACT.md | 206 | 0 | 0 | 0 | Documentation |
| BRANCH_ANALYSIS_TASK_SPECIFICATIONS_IMPROVEMENTS_SUMMARY.md | 142 | 0 | 0 | 0 | Documentation |
| BRANCH_ISOLATION_GUIDELINES.md | 259 | 0 | 0 | 0 | Documentation |
| CLI_CONSOLIDATION_COMPLETION.md | 197 | 0 | 0 | 0 | Documentation |
| CLI_CONSOLIDATION_SETUP.md | 153 | 0 | 0 | 0 | Documentation |
| CLI_TOOLS_INVENTORY.md | 451 | 0 | 0 | 0 | Documentation |
| CODE_FORMATTING.md | 297 | 0 | 0 | 0 | Documentation |
| COMPLETE_TASK_WORKFLOW.md | 485 | 0 | 0 | 0 | Documentation |
| COMPREHENSIVE_CODE_REVIEW_REPORT.md | 115 | 0 | 0 | 0 | Documentation |
| CONSOLIDATION_NEXT_STEPS.md | 16 | 0 | 0 | 0 | Documentation |
| CONTAMINATION_DOCUMENTATION_INDEX.md | 260 | 0 | 0 | 0 | Documentation |
| CONTAMINATION_INCIDENTS_SUMMARY.md | 115 | 0 | 0 | 0 | Documentation |
| CONTENT_DUPLICATION_PREVENTION_GUIDELINES.md | 274 | 0 | 0 | 0 | Documentation |
| CURRENT_DOCUMENTATION_MAP.md | 250 | 0 | 0 | 0 | Documentation |
| CURRENT_SYSTEM_STATE_DIAGRAM.md | 292 | 0 | 0 | 0 | Documentation |
| DEPENDENCY_CORRUPTION_FIX_PLAN.md | 481 | 0 | 0 | 0 | Documentation |
| DEPENDENCY_OUTPUT_AUDIT.md | 1510 | 0 | 0 | 0 | Documentation |
| DOCUMENTATION_CLEANUP_COMPLETE.md | 348 | 0 | 0 | 0 | Documentation |
| ENHANCED_ACCEPTANCE_CRITERIA_SUMMARY.md | 68 | 0 | 0 | 0 | Documentation |
| ENHANCED_TASK_SLASH_COMMAND_PROMPT.md | 208 | 0 | 0 | 0 | Documentation |
| ENHANCED_TASK_SPECIFICATIONS_ARCHITECTURAL_FOCUS_SUMMARY.md | 135 | 0 | 0 | 0 | Documentation |
| ENHANCED_TASK_SPECIFICATIONS_SUMMARY.md | 133 | 0 | 0 | 0 | Documentation |
| EXTERNAL_DATA_REFERENCES.md | 72 | 0 | 0 | 0 | Documentation |
| FINAL_TASK_SPECIFICATION_IMPROVEMENTS_SUMMARY.md | 110 | 0 | 0 | 0 | Documentation |
| FIRST_ORDER_PRD_IMPROVEMENTS_ANALYSIS.md | 235 | 0 | 0 | 0 | Documentation |
| FORMATTING_STATUS.md | 314 | 0 | 0 | 0 | Documentation |
| HANDOFF_HISTORY_AND_MISTAKES_ANALYSIS.md | 649 | 0 | 0 | 0 | Documentation |
| HANDOFF_VERIFICATION_AND_IMPROVEMENT_PLAN.md | 84 | 0 | 0 | 0 | Documentation |
| IMPROVEMENTS_TO_MAXIMIZE_PRD_ACCURACY.md | 314 | 0 | 0 | 0 | Documentation |
| INITIALIZATION_SUMMARY.md | 161 | 0 | 0 | 0 | Documentation |
| INVESTIGATION_SUMMARY_COMPLETE.md | 471 | 0 | 0 | 0 | Documentation |
| MD_ENHANCEMENT_SUMMARY.md | 57 | 0 | 0 | 0 | Documentation |
| MD_FILE_ADJUSTMENT_ACTION_PLAN.md | 212 | 0 | 0 | 0 | Documentation |
| MD_VALIDATION_REPORT.md | 514 | 0 | 0 | 0 | Documentation |
| MEMORY_API_FOR_TASKS.md | 565 | 0 | 0 | 0 | Documentation |
| MERGE_GUIDANCE_DOCUMENTATION.md | 157 | 0 | 0 | 0 | Documentation |
| MIGRATION_STATUS_ANALYSIS.md | 600 | 0 | 0 | 0 | Documentation |
| ORACLE_RECOMMENDATION_TODO.md | 425 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_TOOLS_UPDATE_ANALYSIS.md | 329 | 0 | 0 | 0 | Documentation |
| PERFECT_FIDELITY_PROCESS_DOCUMENTATION.md | 140 | 0 | 0 | 0 | Documentation |
| PERFORMANCE_PROFILING_FRAMEWORK.md | 443 | 0 | 0 | 0 | Documentation |
| PLACEHOLDER_BACKUP_MAPPING.md | 296 | 0 | 0 | 0 | Documentation |
| PLANNING_TASK_UPDATES.md | 223 | 0 | 0 | 0 | Documentation |
| PRD_GENERATION_IMPROVEMENTS_SUMMARY.md | 244 | 0 | 0 | 0 | Documentation |
| PREVENTION_FRAMEWORK.md | 469 | 0 | 0 | 0 | Documentation |
| PROJECT_STATE_CHECKLIST_RECOVERED.md | 420 | 0 | 0 | 0 | Documentation |
| PROJECT_STATUS_SUMMARY.md | 182 | 0 | 0 | 0 | Documentation |
| PROMPT_IMPROVEMENT_ANALYSIS.md | 120 | 0 | 0 | 0 | Documentation |
| READ_THIS_FIRST_INVESTIGATION_INDEX.md | 391 | 0 | 0 | 0 | Documentation |
| REORGANIZATION_PLAN_BRANCH_ANALYSIS_FORWARD.md | 155 | 0 | 0 | 0 | Documentation |
| ROOT_DOCUMENTATION_CLEANUP_PLAN.md | 520 | 0 | 0 | 0 | Documentation |
| ROUND_TRIP_QUICK_REFERENCE.md | 185 | 0 | 0 | 0 | Documentation |
| ROUND_TRIP_SCRIPTS_SUMMARY.md | 348 | 0 | 0 | 0 | Documentation |
| SCRIPTS_IN_TASK_WORKFLOW.md | 771 | 0 | 0 | 0 | Documentation |
| SESSION_MANAGEMENT_IMPLEMENTATION.md | 78 | 0 | 0 | 0 | Documentation |
| SLASH_COMMAND_PROMPT_IMPROVEMENT.md | 145 | 0 | 0 | 0 | Documentation |
| SLASH_COMMAND_TASK_INTEGRATION_PROMPT_IMPROVEMENT.md | 146 | 0 | 0 | 0 | Documentation |
| SUBTASK_MARKDOWN_TEMPLATE.md | 690 | 0 | 0 | 0 | Documentation |
| SUMMARY_TASK_UPDATES.md | 109 | 0 | 0 | 0 | Documentation |
| TASKMASTER_ANALYSIS_CONSOLIDATION_COMPLETE.md | 62 | 0 | 0 | 0 | Documentation |
| TASKMASTER_CHANGES_REVIEW.md | 87 | 0 | 0 | 0 | Documentation |
| TASKMASTER_COMPREHENSIVE_REVIEW_REPORT.md | 112 | 0 | 0 | 0 | Documentation |
| TASK_007_DEPRECATION_SUMMARY.md | 94 | 0 | 0 | 0 | Documentation |
| TASK_7_PURPOSE_CLARIFICATION.md | 65 | 0 | 0 | 0 | Documentation |
| TASK_CLASSIFICATION_SYSTEM.md | 50 | 0 | 0 | 0 | Documentation |
| TASK_DETAIL_IMPROVEMENTS_MAP.md | 204 | 0 | 0 | 0 | Documentation |
| TASK_DISTANCE_MINIMIZATION_FRAMEWORK.md | 49 | 0 | 0 | 0 | Documentation |
| TASK_ENHANCEMENT_PROCEDURES.md | 560 | 0 | 0 | 0 | Documentation |
| TASK_EXPANSION_PLAN_BY_WEEK.md | 1286 | 0 | 0 | 0 | Documentation |
| TASK_IMPLEMENTATION_ANALYSIS_REPORT.md | 85 | 0 | 0 | 0 | Documentation |
| TASK_INTERPRETATION_FINDING_TASK7.md | 39 | 0 | 0 | 0 | Documentation |
| TASK_METADATA_PRESERVATION_GUIDE.md | 359 | 0 | 0 | 0 | Documentation |
| TASK_REDESIGN_VERIFICATION.md | 151 | 0 | 0 | 0 | Documentation |
| TASK_RESTRUCTURING_ANALYSIS_REPORT.md | 763 | 0 | 0 | 0 | Documentation |
| TASK_SPECIFICATION_IMPROVEMENTS_SUMMARY.md | 124 | 0 | 0 | 0 | Documentation |
| TASK_WORKFLOW_INTEGRATION.md | 430 | 0 | 0 | 0 | Documentation |
| TEMPLATE_MIGRATION_PATTERNS_AND_BLOCKERS.md | 449 | 0 | 0 | 0 | Documentation |
| TEMPLATE_STRUCTURE_ANALYSIS.md | 233 | 0 | 0 | 0 | Documentation |
| TOOLSET_DOCUMENTATION.md | 72 | 0 | 0 | 0 | Documentation |
| UNFINISHED_SESSION_TODOS.md | 89 | 0 | 0 | 0 | Documentation |
| UPDATED_CONSOLIDATION_PLAN.md | 251 | 0 | 0 | 0 | Documentation |
| branch-alignment-aggregated-documentation.md | 177 | 0 | 0 | 0 | Documentation |
| branch-alignment-framework-prd.txt | 382 | 0 | 0 | 0 | Documentation |
| branch_alignment_workflow.md | 158 | 0 | 0 | 0 | Documentation |
| complete_tasks_flow.mmd | 122 | 0 | 0 | 0 | Documentation |
| iterative_tasks_flow.mmd | 51 | 0 | 0 | 0 | Documentation |
| master-prd.txt | 11 | 0 | 0 | 0 | Documentation |
| orchestration_summary.md | 102 | 0 | 0 | 0 | Documentation |
| task_004_tuned_recommendations.md | 205 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/docs/archive/large_docs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AGENT_GUIDELINES_RESOLUTION_PLAN.md | 605 | 0 | 0 | 0 | Documentation |
| BRANCH_PROPAGATION_IMPLEMENTATION_SUMMARY.md | 535 | 0 | 0 | 0 | Documentation |
| BRANCH_UPDATE_PROCEDURE.md | 628 | 0 | 0 | 0 | Documentation |
| DEPENDENCY_BLOCKER_ANALYSIS.md | 459 | 0 | 0 | 0 | Documentation |
| GITHUB_WORKFLOWS_ROADMAP.md | 445 | 0 | 0 | 0 | Documentation |
| LLM_DOCUMENTATION_DISCOVERY.md | 778 | 0 | 0 | 0 | Documentation |
| MULTI_TOOL_DISCOVERY.md | 677 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_PROCESS_GUIDE.md | 518 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_SYSTEM.md | 637 | 0 | 0 | 0 | Documentation |
| branch_switching_guide.md | 255 | 0 | 0 | 0 | Documentation |
| orchestration-push-workflow.md | 507 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/docs/archive/old-prds`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| agent-context-control-prd.txt | 146 | 0 | 0 | 0 | Documentation |
| emailintelligence-migration-prd.txt | 93 | 0 | 0 | 0 | Documentation |
| pr176-fixes-prd.txt | 111 | 0 | 0 | 0 | Documentation |
| validation-refactoring-prd.txt | 283 | 0 | 0 | 0 | Documentation |
| workflow_integration_prd.txt | 198 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/docs/archive/old_workflow_docs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CPU_ONLY_DEPLOYMENT_POLICY.md | 195 | 0 | 0 | 0 | Documentation |
| CPU_SETUP.md | 131 | 0 | 0 | 0 | Documentation |
| DOCUMENTATION_WORKFLOW.md | 196 | 0 | 0 | 0 | Documentation |
| TROUBLESHOOTING.md | 418 | 0 | 0 | 0 | Documentation |
| application_launch_hardening_strategy.md | 189 | 0 | 0 | 0 | Documentation |
| deployment_guide.md | 186 | 0 | 0 | 0 | Documentation |
| launcher_guide.md | 229 | 0 | 0 | 0 | Documentation |
| worktree-documentation-system.md | 251 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/docs/branch_alignment`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| BRANCH_ALIGNMENT_SYSTEM.md | 154 | 0 | 0 | 0 | Documentation |
| COORDINATION_AGENTS_SUMMARY.md | 141 | 0 | 0 | 0 | Documentation |
| COORDINATION_AGENT_SYSTEM.md | 198 | 0 | 0 | 0 | Documentation |
| INDEX.md | 31 | 0 | 0 | 0 | Documentation |
| MULTI_AGENT_COORDINATION.md | 70 | 0 | 0 | 0 | Documentation |
| PRECALCULATION_PATTERNS.md | 137 | 0 | 0 | 0 | Documentation |
| README.md | 76 | 0 | 0 | 0 | Documentation |
| SYSTEM_OVERVIEW.md | 79 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/docs/research`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| 2025-11-13_what-are-effective-strategies-for-creating-compreh.md | 179 | 0 | 0 | 0 | Documentation |
| 2025-11-13_what-are-proven-patterns-for-refactoring-global-st.md | 146 | 0 | 0 | 0 | Documentation |
| 2025-11-13_what-are-the-best-practices-for-handling-backward.md | 126 | 0 | 0 | 0 | Documentation |
| 2025-11-21_confirm-tasks-exist-for-all-branches-that-need-ali.md | 262 | 0 | 0 | 0 | Documentation |
| 2025-11-21_how-to-reduce-complexity.md | 135 | 0 | 0 | 0 | Documentation |
| 2025-11-21_there-should-be-a-task-for-each-branch-there-is-no.md | 47 | 0 | 0 | 0 | Documentation |
| 2025-11-22_find-and-create-new-tags-to-help-with-task-organis.md | 123 | 0 | 0 | 0 | Documentation |
| 2025-11-24_there-are-multiple-branchs-containing-attempts-and.md | 175 | 0 | 0 | 0 | Documentation |
| 2025-11-28_create-a-detailed-summary-of-which-tasks-are-inten.md | 60 | 0 | 0 | 0 | Documentation |
| 2025-11-28_find-the-tasks-that-are-dependent-on-this-task-54.md | 58 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/guidance`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md | 109 | 0 | 0 | 0 | Documentation |
| ARCHITECTURE_ALIGNMENT_IMPLEMENTATION_GUIDE.md | 254 | 0 | 0 | 0 | Documentation |
| COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md | 210 | 0 | 0 | 0 | Documentation |
| COMPREHENSIVE_DEPENDENCY_FRAMEWORK.md | 777 | 0 | 0 | 0 | Documentation |
| FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md | 217 | 0 | 0 | 0 | Documentation |
| FINAL_MERGE_STRATEGY.md | 68 | 0 | 0 | 0 | Documentation |
| HANDLING_INCOMPLETE_MIGRATIONS.md | 96 | 0 | 0 | 0 | Documentation |
| IMPLEMENTATION_SUMMARY.md | 108 | 0 | 0 | 0 | Documentation |
| ISOLATED_ENVIRONMENT_SPECIFICATION.md | 120 | 0 | 0 | 0 | Documentation |
| LOGGING_GUIDE.md | 161 | 0 | 0 | 0 | Documentation |
| LOGGING_SYSTEM_PLAN.md | 516 | 0 | 0 | 0 | Documentation |
| MERGE_GUIDANCE_DOCUMENTATION.md | 232 | 0 | 0 | 0 | Documentation |
| OPERATIONAL_PROCEDURES_GUIDELINES.md | 312 | 0 | 0 | 0 | Documentation |
| QUICK_REFERENCE_GUIDE.md | 144 | 0 | 0 | 0 | Documentation |
| README.md | 84 | 0 | 0 | 0 | Documentation |
| SCIENTIFIC_BRANCH_ENHANCEMENTS_COMPARISON.md | 252 | 0 | 0 | 0 | Documentation |
| SCRIPTS_AND_TOOLS_INTEGRATION.md | 495 | 0 | 0 | 0 | Documentation |
| SECURITY_ERROR_TESTING_GUIDELINES.md | 288 | 0 | 0 | 0 | Testing |
| SUBTASK_EXPANSION_TEMPLATE.md | 176 | 0 | 0 | 0 | Documentation |
| SUMMARY.md | 38 | 0 | 0 | 0 | Documentation |
| TASK_AUGMENTATION_PROCESS.md | 333 | 0 | 0 | 0 | Documentation |
| TASK_DEPENDENCY_VISUAL_MAP.md | 583 | 0 | 0 | 0 | Documentation |
| TASK_NUMBERING_ANALYSIS.md | 168 | 0 | 0 | 0 | Documentation |
| new_task_plan_renumbered.md | 271 | 0 | 0 | 0 | Documentation |
| reorganized_tasks.md | 188 | 0 | 0 | 0 | Documentation |
| task_mapping.md | 159 | 0 | 0 | 0 | Documentation |
| task_master_formatted_tasks.md | 313 | 0 | 0 | 0 | Documentation |
| task_master_formatted_tasks_v2.md | 313 | 0 | 0 | 0 | Documentation |
| validate_architecture_alignment.py | 172 | 16 | 6 | 0 | Core Logic |
| validate_guidance_documentation.sh | 159 | 0 | 0 | 0 | Scripting |

### Directory: `.taskmaster/guidance/implementation_lessons`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| task-002-clustering-guide.md | 966 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/guidance/src`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| main.py | 173 | 17 | 2 | 1 | Core Logic |

### Directory: `.taskmaster/reports`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AMP_FILE_CHANGES_ANALYSIS.md | 406 | 0 | 0 | 0 | Documentation |
| AMP_SESSIONS_LAST_WEEK_DETAILED.md | 372 | 0 | 0 | 0 | Documentation |
| COMPREHENSIVE_DOCUMENTATION_ANALYSIS.md | 577 | 0 | 0 | 0 | Documentation |
| MISSING_DOCUMENTS_RECOVERY_REPORT.md | 229 | 0 | 0 | 0 | Documentation |
| ck_similarity_analysis.md | 126 | 0 | 0 | 0 | Documentation |
| documentation_dashboard.html | 567 | 0 | 0 | 0 | Frontend |
| git_history_analysis.md | 187 | 0 | 0 | 0 | Documentation |
| metadata_coverage_report.json | 279 | 0 | 0 | 0 | Configuration |
| task-complexity-report.json | 221 | 0 | 0 | 0 | Configuration |
| task75_techspec_verification.md | 97 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/scripts`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| GIT_MANAGEMENT_TOOLS.md | 29 | 0 | 0 | 0 | Documentation |
| README.md | 543 | 0 | 0 | 0 | Documentation |
| README_TASK_SCRIPTS.md | 231 | 0 | 0 | 0 | Documentation |
| add_missing_sections.py | 121 | 2 | 2 | 0 | Scripting |
| add_subtasks_to_complex_tasks.py | 166 | 4 | 2 | 0 | Scripting |
| add_subtasks_to_tasks_simple.py | 180 | 4 | 2 | 0 | Scripting |
| advanced_iterative_distance_minimizer.py | 268 | 9 | 5 | 0 | Scripting |
| advanced_iterative_distance_minimizer.py.bak | 318 | 0 | 0 | 0 | Scripting |
| advanced_md_enhancer.py | 212 | 3 | 5 | 1 | Scripting |
| advanced_reverse_engineer_prd.py | 640 | 6 | 9 | 0 | Scripting |
| analyze_git_history.py | 87 | 6 | 1 | 0 | Scripting |
| analyze_task_placeholders.py | 121 | 2 | 2 | 0 | Scripting |
| analyze_task_subtasks.py | 162 | 4 | 2 | 0 | Scripting |
| audit_dependencies.py | 157 | 3 | 4 | 0 | Scripting |
| check_guidance_links.py | 62 | 3 | 1 | 0 | Scripting |
| check_section_compliance.py | 325 | 5 | 5 | 0 | Scripting |
| compare_task_files.py | 105 | 4 | 1 | 0 | Scripting |
| compress_progress.py | 513 | 12 | 12 | 1 | Scripting |
| compress_progress.sh | 378 | 0 | 0 | 0 | Scripting |
| consolidate_task_files_complete.py | 213 | 6 | 6 | 0 | Scripting |
| consolidate_task_files_debug.py | 207 | 6 | 6 | 0 | Scripting |
| consolidate_task_versions.py | 269 | 5 | 7 | 0 | Scripting |
| consolidate_task_versions_final.py | 213 | 6 | 6 | 0 | Scripting |
| consolidate_task_versions_fixed.py | 213 | 6 | 6 | 0 | Scripting |
| consolidation_workflow.py | 250 | 6 | 5 | 0 | Scripting |
| critical_logic_identifier.py | 225 | 5 | 5 | 0 | Scripting |
| dedup_parent_tasks.py | 333 | 5 | 6 | 0 | Scripting |
| dedup_subtask_sections.py | 126 | 5 | 2 | 0 | Scripting |
| deduplicate_parent_tasks.py | 432 | 5 | 6 | 0 | Scripting |
| deprecate_task_007.py | 228 | 6 | 4 | 0 | Scripting |
| disable-hooks.sh | 97 | 0 | 0 | 0 | Scripting |
| documentation_inventory.py | 320 | 9 | 14 | 1 | Scripting |
| enhance_acceptance_criteria.py | 185 | 4 | 6 | 0 | Scripting |
| enhance_branch_analysis_tasks_for_prd_accuracy.py | 2107 | 0 | 0 | 0 | Scripting |
| enhance_task_specifications_for_prd_accuracy.py | 525 | 6 | 20 | 0 | Scripting |
| enhance_tasks_from_archive.py | 167 | 2 | 3 | 0 | Scripting |
| enhanced_improve_task_specs_for_prd_accuracy.py | 375 | 5 | 4 | 0 | Scripting |
| enhanced_iterative_distance_minimizer.py | 268 | 9 | 5 | 0 | Scripting |
| enhanced_iterative_distance_minimizer.py.bak | 318 | 0 | 0 | 0 | Scripting |
| enhanced_reverse_engineer_prd.py | 552 | 6 | 9 | 0 | Scripting |
| expand_subtasks.py | 323 | 6 | 7 | 0 | Scripting |
| find_lost_tasks.py | 292 | 8 | 7 | 0 | Scripting |
| fix_legacy_deps.py | 105 | 2 | 3 | 0 | Scripting |
| fix_task_header_section.py | 70 | 2 | 2 | 0 | Scripting |
| format_code.sh | 112 | 0 | 0 | 0 | Scripting |
| functionality_test_suite.py | 212 | 7 | 4 | 0 | Testing |
| generate_clean_tasks.py | 397 | 2 | 2 | 0 | Scripting |
| generate_subtasks_for_complex_tasks.py | 405 | 4 | 2 | 0 | Scripting |
| generate_subtasks_for_complex_tasks_corrected.py | 405 | 4 | 2 | 0 | Scripting |
| generate_subtasks_for_complex_tasks_fixed.py | 405 | 4 | 2 | 0 | Scripting |
| improve_branch_analysis_task_specs.py | 614 | 6 | 3 | 0 | Scripting |
| improve_task_specs_for_prd_accuracy.py | 303 | 5 | 8 | 0 | Scripting |
| inject_markers.py | 54 | 4 | 1 | 0 | Scripting |
| iterative_distance_minimizer.py | 265 | 9 | 5 | 0 | Scripting |
| iterative_distance_minimizer.py.bak | 315 | 0 | 0 | 0 | Scripting |
| list_invalid_tasks.py | 136 | 5 | 2 | 0 | Scripting |
| list_tasks.py | 100 | 6 | 3 | 0 | Scripting |
| logic_evolution_tracer.py | 219 | 0 | 0 | 0 | Scripting |
| markdownlint_check.py | 222 | 7 | 7 | 1 | Scripting |
| md_enhancer.py | 170 | 3 | 5 | 1 | Scripting |
| md_validator.py | 228 | 4 | 6 | 1 | Scripting |
| next_task.py | 132 | 6 | 4 | 0 | Scripting |
| partial_cherry_pick.py | 94 | 4 | 1 | 0 | Scripting |
| perfect_fidelity_reverse_engineer_prd.py | 675 | 8 | 5 | 0 | Scripting |
| perfect_fidelity_simulated_tasks.json | 3108 | 0 | 0 | 0 | Configuration |
| perfect_fidelity_test_prd.md | 26946 | 0 | 0 | 0 | Testing |
| perfect_fidelity_validator.py | 263 | 12 | 6 | 0 | Scripting |
| perfect_fidelity_validator.py.bak | 336 | 0 | 0 | 0 | Scripting |
| query_findings.py | 192 | 6 | 11 | 1 | Scripting |
| ralph_loop_controller.py | 165 | 7 | 3 | 0 | Scripting |
| regenerate_tasks_from_plan.py | 351 | 7 | 6 | 0 | Scripting |
| reorganize_branch_analysis_forward.py | 333 | 6 | 5 | 0 | Scripting |
| restructure_tasks_to_14_section_format.py | 357 | 4 | 3 | 0 | Scripting |
| reverse_engineer_prd.py | 394 | 6 | 6 | 0 | Scripting |
| reverse_sync_orchestration.sh | 146 | 0 | 0 | 0 | Scripting |
| roundtrip_fidelity_test.py | 352 | 6 | 5 | 0 | Testing |
| roundtrip_simulated_tasks.json | 23 | 0 | 0 | 0 | Configuration |
| roundtrip_test.py | 280 | 6 | 9 | 0 | Testing |
| roundtrip_test_prd.md | 141 | 0 | 0 | 0 | Testing |
| script_feature_matrix.py | 212 | 0 | 0 | 0 | Scripting |
| search_tasks.py | 103 | 5 | 2 | 0 | Scripting |
| setup-ralph-loop.sh | 78 | 0 | 0 | 0 | Scripting |
| show_task.py | 145 | 6 | 4 | 0 | Scripting |
| split_enhanced_plan.py | 340 | 5 | 4 | 0 | Scripting |
| standardize_tasks.py | 304 | 5 | 4 | 0 | Scripting |
| super_enhanced_reverse_engineer_prd.py | 705 | 11 | 12 | 0 | Scripting |
| sync_setup_worktrees.sh | 298 | 0 | 0 | 0 | Scripting |
| targeted_placeholder_replacer.py | 267 | 2 | 2 | 0 | Scripting |
| task_complexity_analyzer.py | 549 | 8 | 13 | 0 | Scripting |
| task_distance_analyzer.py | 492 | 7 | 8 | 0 | Scripting |
| task_metadata_manager.py | 549 | 10 | 14 | 1 | Scripting |
| task_summary.py | 201 | 5 | 5 | 0 | Scripting |
| taskmaster_runner.py | 237 | 8 | 3 | 0 | Scripting |
| test_round_trip.py | 266 | 11 | 6 | 0 | Testing |
| test_round_trip.py.bak | 312 | 0 | 0 | 0 | Testing |
| test_round_trip_enhanced.py | 380 | 12 | 9 | 0 | Testing |
| ultra_enhanced_convert_md_to_task_json.py | 256 | 6 | 3 | 0 | Scripting |
| ultra_enhanced_reverse_engineer_prd.py | 757 | 8 | 11 | 0 | Scripting |
| update_flake8_orchestration.sh | 87 | 0 | 0 | 0 | Scripting |
| update_option_c_visual_map.py | 167 | 5 | 6 | 0 | Scripting |
| validate_markdown_refs.py | 50 | 4 | 2 | 0 | Scripting |
| validate_task_specifications.py | 211 | 6 | 3 | 0 | Scripting |

### Directory: `.taskmaster/src`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 23 | 0 | 0 | 0 | Frontend |
| main.py | 176 | 13 | 2 | 1 | Core Logic |

### Directory: `.taskmaster/src/analysis`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conflict_analyzer.py | 117 | 3 | 8 | 1 | Core Logic |

### Directory: `.taskmaster/src/analysis/constitutional`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| analyzer.py | 95 | 6 | 3 | 2 | Core Logic |
| requirement_checker.py | 180 | 3 | 5 | 5 | Core Logic |

### Directory: `.taskmaster/src/api`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| main.py | 76 | 6 | 0 | 0 | Core Logic |

### Directory: `.taskmaster/src/application`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conflict_resolution_app.py | 157 | 8 | 4 | 1 | Core Logic |

### Directory: `.taskmaster/src/core`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AGENTS.md | 39 | 0 | 0 | 0 | Documentation |
| config.py | 91 | 4 | 7 | 1 | Configuration |
| conflict_models.py | 93 | 3 | 1 | 8 | Core Logic |
| exceptions.py | 50 | 0 | 0 | 9 | Core Logic |
| git_operations.py | 145 | 6 | 9 | 1 | Core Logic |
| interfaces.py | 114 | 3 | 0 | 5 | Core Logic |
| security.py | 69 | 3 | 6 | 1 | Core Logic |

### Directory: `.taskmaster/src/git`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conflict_detector.py | 215 | 11 | 8 | 1 | Core Logic |
| repository.py | 240 | 6 | 3 | 1 | Core Logic |

### Directory: `.taskmaster/src/resolution`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 270 | 6 | 9 | 5 | Core Logic |
| auto_resolver.py | 346 | 8 | 9 | 1 | Core Logic |
| semantic_merger.py | 331 | 4 | 15 | 1 | Core Logic |

### Directory: `.taskmaster/src/strategy`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| generator.py | 202 | 4 | 11 | 1 | Core Logic |
| risk_assessor.py | 249 | 3 | 14 | 1 | Core Logic |

### Directory: `.taskmaster/src/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| logger.py | 87 | 4 | 2 | 0 | Core Logic |

### Directory: `.taskmaster/src/validation`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| validator.py | 158 | 4 | 7 | 2 | Core Logic |

### Directory: `.taskmaster/task_scripts`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 299 | 0 | 0 | 0 | Documentation |
| add_status.py | 148 | 7 | 4 | 0 | Scripting |
| consolidate_completed_tasks.py | 130 | 4 | 2 | 0 | Scripting |
| example_usage.py | 134 | 4 | 2 | 0 | Scripting |
| extract_completed_tasks.py | 71 | 2 | 2 | 0 | Scripting |
| finalize_task_move.py | 108 | 4 | 2 | 0 | Scripting |
| fix_relative_deps.py | 409 | 11 | 8 | 0 | Scripting |
| fix_tasks.py | 415 | 12 | 11 | 1 | Scripting |
| merge_config.yaml | 62 | 0 | 0 | 0 | Configuration |
| merge_task_manager.py | 1495 | 16 | 30 | 1 | Scripting |
| move_completed_tasks.py | 112 | 4 | 2 | 0 | Scripting |
| move_specific_tasks.py | 140 | 4 | 2 | 0 | Scripting |
| move_tasks_64_to_69.py | 135 | 3 | 2 | 0 | Scripting |
| quick_start.py | 146 | 1 | 6 | 0 | Scripting |
| remove_duplicates.py | 46 | 1 | 2 | 0 | Scripting |
| sample_task.yaml | 9 | 0 | 0 | 0 | Configuration |
| secure_merge_task_manager.py | 803 | 19 | 29 | 10 | Scripting |
| task_validator_fixer.py | 896 | 10 | 25 | 1 | Scripting |
| taskmaster_common.py | 393 | 10 | 14 | 6 | Scripting |
| test_merge_manager.py | 168 | 9 | 5 | 0 | Testing |

### Directory: `.taskmaster/tasks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .ckignore | 65 | 0 | 0 | 0 | Other |
| AGENTS.md | 153 | 0 | 0 | 0 | Documentation |
| UNIQUE_DELTAS_REPORT.md | 224 | 0 | 0 | 0 | Documentation |
| task_001.1.md | 233 | 0 | 0 | 0 | Documentation |
| task_001.2.md | 244 | 0 | 0 | 0 | Documentation |
| task_001.3.md | 250 | 0 | 0 | 0 | Documentation |
| task_001.4.md | 238 | 0 | 0 | 0 | Documentation |
| task_001.5.md | 223 | 0 | 0 | 0 | Documentation |
| task_001.6.md | 250 | 0 | 0 | 0 | Documentation |
| task_001.7.md | 253 | 0 | 0 | 0 | Documentation |
| task_001.8.md | 285 | 0 | 0 | 0 | Documentation |
| task_001.md | 181 | 0 | 0 | 0 | Documentation |
| task_002-clustering.md | 966 | 0 | 0 | 0 | Documentation |
| task_002.1.md | 337 | 0 | 0 | 0 | Documentation |
| task_002.2.md | 365 | 0 | 0 | 0 | Documentation |
| task_002.3.md | 427 | 0 | 0 | 0 | Documentation |
| task_002.4.md | 579 | 0 | 0 | 0 | Documentation |
| task_002.5.md | 619 | 0 | 0 | 0 | Documentation |
| task_002.6.md | 688 | 0 | 0 | 0 | Documentation |
| task_002.7.md | 529 | 0 | 0 | 0 | Documentation |
| task_002.8.md | 557 | 0 | 0 | 0 | Documentation |
| task_002.9.md | 711 | 0 | 0 | 0 | Documentation |
| task_002.md | 183 | 0 | 0 | 0 | Documentation |
| task_003.1.md | 200 | 0 | 0 | 0 | Documentation |
| task_003.2.md | 227 | 0 | 0 | 0 | Documentation |
| task_003.3.md | 217 | 0 | 0 | 0 | Documentation |
| task_003.4.md | 199 | 0 | 0 | 0 | Documentation |
| task_003.5.md | 204 | 0 | 0 | 0 | Documentation |
| task_003.md | 176 | 0 | 0 | 0 | Documentation |
| task_004.1.md | 204 | 0 | 0 | 0 | Documentation |
| task_004.2.md | 207 | 0 | 0 | 0 | Documentation |
| task_004.3.md | 241 | 0 | 0 | 0 | Documentation |
| task_004.md | 322 | 0 | 0 | 0 | Documentation |
| task_005.1.md | 241 | 0 | 0 | 0 | Documentation |
| task_005.2.md | 213 | 0 | 0 | 0 | Documentation |
| task_005.3.md | 310 | 0 | 0 | 0 | Documentation |
| task_005.md | 323 | 0 | 0 | 0 | Documentation |
| task_006.1.md | 242 | 0 | 0 | 0 | Documentation |
| task_006.2.md | 248 | 0 | 0 | 0 | Documentation |
| task_006.3.md | 283 | 0 | 0 | 0 | Documentation |
| task_006.md | 262 | 0 | 0 | 0 | Documentation |
| task_007.1.md | 189 | 0 | 0 | 0 | Documentation |
| task_007.2.md | 210 | 0 | 0 | 0 | Documentation |
| task_007.3.md | 226 | 0 | 0 | 0 | Documentation |
| task_007.md | 239 | 0 | 0 | 0 | Documentation |
| task_008.1.md | 215 | 0 | 0 | 0 | Documentation |
| task_008.2.md | 211 | 0 | 0 | 0 | Documentation |
| task_008.3.md | 300 | 0 | 0 | 0 | Documentation |
| task_008.4.md | 165 | 0 | 0 | 0 | Documentation |
| task_008.5.md | 179 | 0 | 0 | 0 | Documentation |
| task_008.6.md | 175 | 0 | 0 | 0 | Documentation |
| task_008.7.md | 165 | 0 | 0 | 0 | Documentation |
| task_008.8.md | 181 | 0 | 0 | 0 | Documentation |
| task_008.9.md | 161 | 0 | 0 | 0 | Documentation |
| task_008.md | 232 | 0 | 0 | 0 | Documentation |
| task_009.1.md | 304 | 0 | 0 | 0 | Documentation |
| task_009.2.md | 237 | 0 | 0 | 0 | Documentation |
| task_009.3.md | 271 | 0 | 0 | 0 | Documentation |
| task_009.4.md | 190 | 0 | 0 | 0 | Documentation |
| task_009.5.md | 190 | 0 | 0 | 0 | Documentation |
| task_009.6.md | 214 | 0 | 0 | 0 | Documentation |
| task_009.7.md | 232 | 0 | 0 | 0 | Documentation |
| task_009.md | 653 | 0 | 0 | 0 | Documentation |
| task_010.1.md | 261 | 0 | 0 | 0 | Documentation |
| task_010.2.md | 199 | 0 | 0 | 0 | Documentation |
| task_010.3.md | 205 | 0 | 0 | 0 | Documentation |
| task_010.md | 360 | 0 | 0 | 0 | Documentation |
| task_011.1.md | 171 | 0 | 0 | 0 | Documentation |
| task_011.2.md | 150 | 0 | 0 | 0 | Documentation |
| task_011.3.md | 164 | 0 | 0 | 0 | Documentation |
| task_011.4.md | 156 | 0 | 0 | 0 | Documentation |
| task_011.5.md | 170 | 0 | 0 | 0 | Documentation |
| task_011.6.md | 166 | 0 | 0 | 0 | Documentation |
| task_011.7.md | 156 | 0 | 0 | 0 | Documentation |
| task_011.8.md | 172 | 0 | 0 | 0 | Documentation |
| task_011.9.md | 143 | 0 | 0 | 0 | Documentation |
| task_011.md | 296 | 0 | 0 | 0 | Documentation |
| task_012.1.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.10.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.11.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.12.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.13.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.15.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.16.md | 120 | 0 | 0 | 0 | Documentation |
| task_012.2.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.3.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.4.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.5.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.6.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.7.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.8.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.9.md | 102 | 0 | 0 | 0 | Documentation |
| task_012.md | 290 | 0 | 0 | 0 | Documentation |
| task_013.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_013.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_013.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_013.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_013.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_013.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_013.7.md | 112 | 0 | 0 | 0 | Documentation |
| task_013.8.md | 150 | 0 | 0 | 0 | Documentation |
| task_013.md | 400 | 0 | 0 | 0 | Documentation |
| task_014.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_014.10.md | 159 | 0 | 0 | 0 | Documentation |
| task_014.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_014.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_014.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_014.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_014.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_014.7.md | 112 | 0 | 0 | 0 | Documentation |
| task_014.8.md | 112 | 0 | 0 | 0 | Documentation |
| task_014.9.md | 112 | 0 | 0 | 0 | Documentation |
| task_014.md | 573 | 0 | 0 | 0 | Documentation |
| task_015.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_015.10.md | 171 | 0 | 0 | 0 | Documentation |
| task_015.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_015.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_015.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_015.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_015.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_015.7.md | 112 | 0 | 0 | 0 | Documentation |
| task_015.8.md | 112 | 0 | 0 | 0 | Documentation |
| task_015.9.md | 112 | 0 | 0 | 0 | Documentation |
| task_015.md | 586 | 0 | 0 | 0 | Documentation |
| task_016.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_016.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_016.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_016.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_016.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_016.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_016.7.md | 112 | 0 | 0 | 0 | Documentation |
| task_016.8.md | 112 | 0 | 0 | 0 | Documentation |
| task_016.9.md | 165 | 0 | 0 | 0 | Documentation |
| task_016.md | 585 | 0 | 0 | 0 | Documentation |
| task_017.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_017.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_017.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_017.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_017.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_017.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_017.7.md | 112 | 0 | 0 | 0 | Documentation |
| task_017.8.md | 112 | 0 | 0 | 0 | Documentation |
| task_017.9.md | 169 | 0 | 0 | 0 | Documentation |
| task_017.md | 573 | 0 | 0 | 0 | Documentation |
| task_018.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_018.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_018.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_018.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_018.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_018.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_018.7.md | 112 | 0 | 0 | 0 | Documentation |
| task_018.8.md | 112 | 0 | 0 | 0 | Documentation |
| task_018.9.md | 189 | 0 | 0 | 0 | Documentation |
| task_018.md | 649 | 0 | 0 | 0 | Documentation |
| task_019.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_019.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_019.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_019.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_019.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_019.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_019.7.md | 112 | 0 | 0 | 0 | Documentation |
| task_019.8.md | 172 | 0 | 0 | 0 | Documentation |
| task_019.md | 611 | 0 | 0 | 0 | Documentation |
| task_020.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_020.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_020.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_020.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_020.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_020.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_020.7.md | 112 | 0 | 0 | 0 | Documentation |
| task_020.8.md | 175 | 0 | 0 | 0 | Documentation |
| task_020.md | 616 | 0 | 0 | 0 | Documentation |
| task_021.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_021.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_021.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_021.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_021.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_021.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_021.7.md | 112 | 0 | 0 | 0 | Documentation |
| task_021.8.md | 189 | 0 | 0 | 0 | Documentation |
| task_021.md | 624 | 0 | 0 | 0 | Documentation |
| task_022.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_022.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_022.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_022.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_022.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_022.6.md | 112 | 0 | 0 | 0 | Documentation |
| task_022.7.md | 187 | 0 | 0 | 0 | Documentation |
| task_022.md | 626 | 0 | 0 | 0 | Documentation |
| task_023.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_023.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_023.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_023.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_023.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_023.6.md | 194 | 0 | 0 | 0 | Documentation |
| task_023.md | 651 | 0 | 0 | 0 | Documentation |
| task_024.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_024.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_024.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_024.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_024.5.md | 198 | 0 | 0 | 0 | Documentation |
| task_024.md | 641 | 0 | 0 | 0 | Documentation |
| task_025.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_025.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_025.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_025.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_025.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_025.6.md | 193 | 0 | 0 | 0 | Documentation |
| task_025.md | 681 | 0 | 0 | 0 | Documentation |
| task_026.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_026.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_026.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_026.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_026.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_026.6.md | 194 | 0 | 0 | 0 | Documentation |
| task_026.md | 602 | 0 | 0 | 0 | Documentation |
| task_027.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_027.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_027.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_027.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_027.5.md | 198 | 0 | 0 | 0 | Documentation |
| task_027.md | 597 | 0 | 0 | 0 | Documentation |
| task_028.1.md | 112 | 0 | 0 | 0 | Documentation |
| task_028.2.md | 112 | 0 | 0 | 0 | Documentation |
| task_028.3.md | 112 | 0 | 0 | 0 | Documentation |
| task_028.4.md | 112 | 0 | 0 | 0 | Documentation |
| task_028.5.md | 112 | 0 | 0 | 0 | Documentation |
| task_028.6.md | 193 | 0 | 0 | 0 | Documentation |
| task_028.md | 632 | 0 | 0 | 0 | Documentation |
| tasks.json | 304 | 0 | 0 | 0 | Configuration |

### Directory: `.taskmaster/tasks/mvp`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| EPIC_DEFINITIONS.md | 105 | 0 | 0 | 0 | Documentation |
| MVP_TODO.md | 29 | 0 | 0 | 0 | Documentation |
| README.md | 86 | 0 | 0 | 0 | Documentation |

### Directory: `.taskmaster/templates`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| enhanced_task_template.md | 370 | 0 | 0 | 0 | Documentation |
| example_prd.txt | 47 | 0 | 0 | 0 | Other |
| example_prd_rpg.txt | 511 | 0 | 0 | 0 | Other |

### Directory: `.taskmaster/tests`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_security_fixes.py | 74 | 3 | 6 | 1 | Testing |
| test_taskmaster_common.py | 37 | 5 | 2 | 1 | Testing |

### Directory: `.taskmaster/thread_files`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| handoff_validation_clustering_emulation.md | 168 | 0 | 0 | 0 | Documentation |
| toolu_vrtx_01G1NtG6yuuF42dxRbo2L45q.18141f49-b6c2-4167-afc8-f91e1d357a19 | 10 | 0 | 0 | 0 | Other |
| toolu_vrtx_01NxQbiP36ivamqnErowbeL7.0aa2362b-ddc5-4070-9745-15da3af3a980 | 10 | 0 | 0 | 0 | Other |
| toolu_vrtx_01NxQbiP36ivamqnErowbeL7.51c1cd96-4e3a-43da-aaf7-2865ac567e57 | 10 | 0 | 0 | 0 | Other |
| toolu_vrtx_01NxQbiP36ivamqnErowbeL7.6c723d9c-f1df-49fe-a202-6883a6118d56 | 10 | 0 | 0 | 0 | Other |
| toolu_vrtx_01NxQbiP36ivamqnErowbeL7.74a44940-d34e-4347-a593-44ed9464bae5 | 10 | 0 | 0 | 0 | Other |
| toolu_vrtx_01NxQbiP36ivamqnErowbeL7.a4cf7519-427d-4635-8aac-ed7ff21c065c | 10 | 0 | 0 | 0 | Other |
| toolu_vrtx_01NxQbiP36ivamqnErowbeL7.a89af882-65a5-4b4e-868d-4f607889a065 | 10 | 0 | 0 | 0 | Other |

### Directory: `.trae/rules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dev_workflow.md | 424 | 0 | 0 | 0 | Documentation |
| self_improve.md | 72 | 0 | 0 | 0 | Documentation |
| taskmaster.md | 558 | 0 | 0 | 0 | Documentation |
| trae_rules.md | 53 | 0 | 0 | 0 | Documentation |

### Directory: `.trunk`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitignore | 9 | 0 | 0 | 0 | Other |
| actions | 0 | 0 | 0 | 0 | Other |
| logs | 0 | 0 | 0 | 0 | Other |
| notifications | 0 | 0 | 0 | 0 | Other |
| out | 0 | 0 | 0 | 0 | Other |
| tools | 0 | 0 | 0 | 0 | Other |
| trunk.yaml | 38 | 0 | 0 | 0 | Configuration |

### Directory: `.trunk/configs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .hadolint.yaml | 4 | 0 | 0 | 0 | Configuration |
| .markdownlint.yaml | 2 | 0 | 0 | 0 | Configuration |
| .shellcheckrc | 7 | 0 | 0 | 0 | Configuration |
| .yamllint.yaml | 7 | 0 | 0 | 0 | Configuration |
| ruff.toml | 5 | 0 | 0 | 0 | Configuration |

### Directory: `.trunk/plugins`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| configs | 0 | 0 | 0 | 0 | Configuration |
| trunk | 0 | 0 | 0 | 0 | Other |

### Directory: `.vscode`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mcp.json | 30 | 0 | 0 | 0 | Configuration |
| settings.json | 43 | 0 | 0 | 0 | Configuration |
| tasks.json | 10 | 0 | 0 | 0 | Configuration |

### Directory: `.windsurf`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mcp.json | 18 | 0 | 0 | 0 | Configuration |

### Directory: `.windsurf/rules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dev_workflow.md | 424 | 0 | 0 | 0 | Documentation |
| self_improve.md | 72 | 0 | 0 | 0 | Documentation |
| taskmaster.md | 558 | 0 | 0 | 0 | Documentation |
| windsurf_rules.md | 53 | 0 | 0 | 0 | Documentation |

### Directory: `__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conftest.cpython-313-pytest-8.4.2.pyc | 11 | 0 | 0 | 0 | Testing |
| conftest.cpython-313-pytest-9.0.2.pyc | 11 | 0 | 0 | 0 | Testing |

### Directory: `backlog`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.yml | 14 | 0 | 0 | 0 | Configuration |
| task-expansion-research-summary.md | 110 | 0 | 0 | 0 | Documentation |

### Directory: `backlog/sessions`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| IFLOW-20251031-001.md | 63 | 0 | 0 | 0 | Documentation |
| IFLOW-20251101-001.md | 73 | 0 | 0 | 0 | Documentation |
| IFLOW-20251102-001.md | 63 | 0 | 0 | 0 | Documentation |
| IFLOW-20251104-001.md | 108 | 0 | 0 | 0 | Documentation |
| IFLOW-20251112-ACHIEVEMENTS.md | 332 | 0 | 0 | 0 | Documentation |
| IFLOW.md | 274 | 0 | 0 | 0 | Documentation |
| LLXPRT.md | 0 | 0 | 0 | 0 | Documentation |
| README.md | 21 | 0 | 0 | 0 | Documentation |

### Directory: `backups/branch_cleanup`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| checkpoint_1765859866.json | 77 | 0 | 0 | 0 | Configuration |
| checkpoint_1765859887.json | 77 | 0 | 0 | 0 | Configuration |
| checkpoint_1765859936.json | 77 | 0 | 0 | 0 | Configuration |
| checkpoint_1765859942.json | 77 | 0 | 0 | 0 | Configuration |
| checkpoint_1765859998.json | 68 | 0 | 0 | 0 | Configuration |

### Directory: `branches/orchestration-tools`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| MERGE_TASK.md | 190 | 0 | 0 | 0 | Documentation |

### Directory: `branches/scientific`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| MERGE_TASK.md | 188 | 0 | 0 | 0 | Documentation |

### Directory: `client`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.html | 13 | 0 | 0 | 0 | Frontend |
| package-lock.json | 6263 | 0 | 0 | 0 | Configuration |
| package.json | 78 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/@babel/code-frame/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 216 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 233 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| parse.js | 47 | 0 | 0 | 0 | Frontend |
| parse.js.map | 1 | 0 | 0 | 0 | Other |
| transform-ast.js | 50 | 0 | 0 | 0 | Frontend |
| transform-ast.js.map | 1 | 0 | 0 | 0 | Other |
| transform-file-browser.js | 23 | 0 | 0 | 0 | Frontend |
| transform-file-browser.js.map | 1 | 0 | 0 | 0 | Other |
| transform-file.js | 40 | 0 | 0 | 0 | Frontend |
| transform-file.js.map | 1 | 0 | 0 | 0 | Other |
| transform.js | 49 | 0 | 0 | 0 | Frontend |
| transform.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib/config`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cache-contexts.js | 5 | 0 | 0 | 0 | Configuration |
| cache-contexts.js.map | 1 | 0 | 0 | 0 | Configuration |
| caching.js | 261 | 0 | 0 | 0 | Configuration |
| caching.js.map | 1 | 0 | 0 | 0 | Configuration |
| config-chain.js | 469 | 0 | 0 | 0 | Configuration |
| config-chain.js.map | 1 | 0 | 0 | 0 | Configuration |
| config-descriptors.js | 190 | 0 | 0 | 0 | Configuration |
| config-descriptors.js.map | 1 | 0 | 0 | 0 | Configuration |
| full.js | 312 | 0 | 0 | 0 | Configuration |
| full.js.map | 1 | 0 | 0 | 0 | Configuration |
| index.js | 93 | 0 | 0 | 0 | Configuration |
| index.js.map | 1 | 0 | 0 | 0 | Configuration |
| item.js | 67 | 0 | 0 | 0 | Configuration |
| item.js.map | 1 | 0 | 0 | 0 | Configuration |
| partial.js | 158 | 0 | 0 | 0 | Configuration |
| partial.js.map | 1 | 0 | 0 | 0 | Configuration |
| pattern-to-regex.js | 38 | 0 | 0 | 0 | Configuration |
| pattern-to-regex.js.map | 1 | 0 | 0 | 0 | Configuration |
| plugin.js | 33 | 0 | 0 | 0 | Configuration |
| plugin.js.map | 1 | 0 | 0 | 0 | Configuration |
| printer.js | 113 | 0 | 0 | 0 | Configuration |
| printer.js.map | 1 | 0 | 0 | 0 | Configuration |
| resolve-targets-browser.js | 41 | 0 | 0 | 0 | Configuration |
| resolve-targets-browser.js.map | 1 | 0 | 0 | 0 | Configuration |
| resolve-targets.js | 61 | 0 | 0 | 0 | Configuration |
| resolve-targets.js.map | 1 | 0 | 0 | 0 | Configuration |
| util.js | 31 | 0 | 0 | 0 | Configuration |
| util.js.map | 1 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/@babel/core/lib/config/files`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| configuration.js | 290 | 0 | 0 | 0 | Configuration |
| configuration.js.map | 1 | 0 | 0 | 0 | Configuration |
| import.cjs | 6 | 0 | 0 | 0 | Configuration |
| import.cjs.map | 1 | 0 | 0 | 0 | Configuration |
| index-browser.js | 58 | 0 | 0 | 0 | Configuration |
| index-browser.js.map | 1 | 0 | 0 | 0 | Configuration |
| index.js | 78 | 0 | 0 | 0 | Configuration |
| index.js.map | 1 | 0 | 0 | 0 | Configuration |
| module-types.js | 211 | 0 | 0 | 0 | Configuration |
| module-types.js.map | 1 | 0 | 0 | 0 | Configuration |
| package.js | 61 | 0 | 0 | 0 | Configuration |
| package.js.map | 1 | 0 | 0 | 0 | Configuration |
| plugins.js | 230 | 0 | 0 | 0 | Configuration |
| plugins.js.map | 1 | 0 | 0 | 0 | Configuration |
| types.js | 5 | 0 | 0 | 0 | Configuration |
| types.js.map | 1 | 0 | 0 | 0 | Configuration |
| utils.js | 36 | 0 | 0 | 0 | Configuration |
| utils.js.map | 1 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/@babel/core/lib/config/helpers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config-api.js | 84 | 0 | 0 | 0 | Configuration |
| config-api.js.map | 1 | 0 | 0 | 0 | Configuration |
| deep-array.js | 23 | 0 | 0 | 0 | Configuration |
| deep-array.js.map | 1 | 0 | 0 | 0 | Configuration |
| environment.js | 12 | 0 | 0 | 0 | Configuration |
| environment.js.map | 1 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/@babel/core/lib/config/validation`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| option-assertions.js | 277 | 0 | 0 | 0 | Configuration |
| option-assertions.js.map | 1 | 0 | 0 | 0 | Configuration |
| options.js | 189 | 0 | 0 | 0 | Configuration |
| options.js.map | 1 | 0 | 0 | 0 | Configuration |
| plugins.js | 67 | 0 | 0 | 0 | Configuration |
| plugins.js.map | 1 | 0 | 0 | 0 | Configuration |
| removed.js | 68 | 0 | 0 | 0 | Configuration |
| removed.js.map | 1 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/@babel/core/lib/errors`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config-error.js | 18 | 0 | 0 | 0 | Configuration |
| config-error.js.map | 1 | 0 | 0 | 0 | Configuration |
| rewrite-stack-trace.js | 98 | 0 | 0 | 0 | Frontend |
| rewrite-stack-trace.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib/gensync-utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| async.js | 90 | 0 | 0 | 0 | Frontend |
| async.js.map | 1 | 0 | 0 | 0 | Other |
| fs.js | 31 | 0 | 0 | 0 | Frontend |
| fs.js.map | 1 | 0 | 0 | 0 | Other |
| functional.js | 58 | 0 | 0 | 0 | Frontend |
| functional.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib/parser`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 79 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib/parser/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| missing-plugin-helper.js | 339 | 0 | 0 | 0 | Frontend |
| missing-plugin-helper.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib/tools`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| build-external-helpers.js | 144 | 0 | 0 | 0 | Frontend |
| build-external-helpers.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib/transformation`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| block-hoist-plugin.js | 84 | 0 | 0 | 0 | Frontend |
| block-hoist-plugin.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 92 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| normalize-file.js | 129 | 0 | 0 | 0 | Frontend |
| normalize-file.js.map | 1 | 0 | 0 | 0 | Other |
| normalize-opts.js | 59 | 0 | 0 | 0 | Frontend |
| normalize-opts.js.map | 1 | 0 | 0 | 0 | Other |
| plugin-pass.js | 50 | 0 | 0 | 0 | Frontend |
| plugin-pass.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib/transformation/file`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| babel-7-helpers.cjs | 6 | 0 | 0 | 0 | Other |
| babel-7-helpers.cjs.map | 1 | 0 | 0 | 0 | Other |
| file.js | 219 | 0 | 0 | 0 | Frontend |
| file.js.map | 1 | 0 | 0 | 0 | Other |
| generate.js | 84 | 0 | 0 | 0 | Frontend |
| generate.js.map | 1 | 0 | 0 | 0 | Other |
| merge-map.js | 37 | 0 | 0 | 0 | Frontend |
| merge-map.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib/transformation/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| clone-deep.js | 56 | 0 | 0 | 0 | Frontend |
| clone-deep.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/core/lib/vendor`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| import-meta-resolve.js | 1042 | 0 | 0 | 0 | Frontend |
| import-meta-resolve.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/generator/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| buffer.js | 317 | 0 | 0 | 0 | Frontend |
| buffer.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 112 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| printer.js | 781 | 0 | 0 | 0 | Frontend |
| printer.js.map | 1 | 0 | 0 | 0 | Other |
| source-map.js | 85 | 0 | 0 | 0 | Frontend |
| source-map.js.map | 1 | 0 | 0 | 0 | Other |
| token-map.js | 191 | 0 | 0 | 0 | Frontend |
| token-map.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/generator/lib/generators`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| base.js | 87 | 0 | 0 | 0 | Frontend |
| base.js.map | 1 | 0 | 0 | 0 | Other |
| classes.js | 212 | 0 | 0 | 0 | Frontend |
| classes.js.map | 1 | 0 | 0 | 0 | Other |
| deprecated.js | 28 | 0 | 0 | 0 | Frontend |
| deprecated.js.map | 1 | 0 | 0 | 0 | Other |
| expressions.js | 300 | 0 | 0 | 0 | Frontend |
| expressions.js.map | 1 | 0 | 0 | 0 | Other |
| flow.js | 660 | 0 | 0 | 0 | Frontend |
| flow.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 128 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| jsx.js | 126 | 0 | 0 | 0 | Frontend |
| jsx.js.map | 1 | 0 | 0 | 0 | Other |
| methods.js | 198 | 0 | 0 | 0 | Frontend |
| methods.js.map | 1 | 0 | 0 | 0 | Other |
| modules.js | 287 | 0 | 0 | 0 | Frontend |
| modules.js.map | 1 | 0 | 0 | 0 | Other |
| statements.js | 279 | 0 | 0 | 0 | Frontend |
| statements.js.map | 1 | 0 | 0 | 0 | Other |
| template-literals.js | 40 | 0 | 0 | 0 | Frontend |
| template-literals.js.map | 1 | 0 | 0 | 0 | Other |
| types.js | 238 | 0 | 0 | 0 | Frontend |
| types.js.map | 1 | 0 | 0 | 0 | Other |
| typescript.js | 724 | 0 | 0 | 0 | Scripting |
| typescript.js.map | 1 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/@babel/generator/lib/node`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 122 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| parentheses.js | 262 | 0 | 0 | 0 | Frontend |
| parentheses.js.map | 1 | 0 | 0 | 0 | Other |
| whitespace.js | 145 | 0 | 0 | 0 | Frontend |
| whitespace.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/helper-compilation-targets/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| debug.js | 28 | 0 | 0 | 0 | Frontend |
| debug.js.map | 1 | 0 | 0 | 0 | Other |
| filter-items.js | 67 | 0 | 0 | 0 | Frontend |
| filter-items.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 232 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| options.js | 24 | 0 | 0 | 0 | Frontend |
| options.js.map | 1 | 0 | 0 | 0 | Other |
| pretty.js | 40 | 0 | 0 | 0 | Frontend |
| pretty.js.map | 1 | 0 | 0 | 0 | Other |
| targets.js | 28 | 0 | 0 | 0 | Frontend |
| targets.js.map | 1 | 0 | 0 | 0 | Other |
| utils.js | 58 | 0 | 0 | 0 | Frontend |
| utils.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/helper-module-imports/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| import-builder.js | 122 | 0 | 0 | 0 | Frontend |
| import-builder.js.map | 1 | 0 | 0 | 0 | Other |
| import-injector.js | 304 | 0 | 0 | 0 | Frontend |
| import-injector.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 37 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| is-module.js | 11 | 0 | 0 | 0 | Frontend |
| is-module.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/helper-module-transforms/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dynamic-import.js | 48 | 0 | 0 | 0 | Frontend |
| dynamic-import.js.map | 1 | 0 | 0 | 0 | Other |
| get-module-name.js | 48 | 0 | 0 | 0 | Frontend |
| get-module-name.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 398 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| lazy-modules.js | 31 | 0 | 0 | 0 | Frontend |
| lazy-modules.js.map | 1 | 0 | 0 | 0 | Other |
| normalize-and-load-metadata.js | 364 | 0 | 0 | 0 | Frontend |
| normalize-and-load-metadata.js.map | 1 | 0 | 0 | 0 | Data |
| rewrite-live-references.js | 360 | 0 | 0 | 0 | Frontend |
| rewrite-live-references.js.map | 1 | 0 | 0 | 0 | Other |
| rewrite-this.js | 22 | 0 | 0 | 0 | Frontend |
| rewrite-this.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/helper-plugin-utils/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 76 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/helper-string-parser/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 295 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/helper-validator-identifier/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| identifier.js | 70 | 0 | 0 | 0 | Frontend |
| identifier.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 57 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| keyword.js | 35 | 0 | 0 | 0 | Frontend |
| keyword.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/helper-validator-option/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| find-suggestion.js | 39 | 0 | 0 | 0 | Frontend |
| find-suggestion.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 21 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| validator.js | 48 | 0 | 0 | 0 | Frontend |
| validator.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/helpers/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| helpers-generated.js | 1442 | 0 | 0 | 0 | Frontend |
| helpers-generated.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 126 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/helpers/lib/helpers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AwaitValue.js | 11 | 0 | 0 | 0 | Frontend |
| AwaitValue.js.map | 1 | 0 | 0 | 0 | Other |
| OverloadYield.js | 12 | 0 | 0 | 0 | Frontend |
| OverloadYield.js.map | 1 | 0 | 0 | 0 | Other |
| applyDecoratedDescriptor.js | 31 | 0 | 0 | 0 | Scripting |
| applyDecoratedDescriptor.js.map | 1 | 0 | 0 | 0 | Scripting |
| applyDecs.js | 459 | 0 | 0 | 0 | Frontend |
| applyDecs.js.map | 1 | 0 | 0 | 0 | Other |
| applyDecs2203.js | 363 | 0 | 0 | 0 | Frontend |
| applyDecs2203.js.map | 1 | 0 | 0 | 0 | Other |
| applyDecs2203R.js | 376 | 0 | 0 | 0 | Frontend |
| applyDecs2203R.js.map | 1 | 0 | 0 | 0 | Other |
| applyDecs2301.js | 421 | 0 | 0 | 0 | Frontend |
| applyDecs2301.js.map | 1 | 0 | 0 | 0 | Other |
| applyDecs2305.js | 235 | 0 | 0 | 0 | Frontend |
| applyDecs2305.js.map | 1 | 0 | 0 | 0 | Other |
| applyDecs2311.js | 236 | 0 | 0 | 0 | Frontend |
| applyDecs2311.js.map | 1 | 0 | 0 | 0 | Other |
| arrayLikeToArray.js | 13 | 0 | 0 | 0 | Frontend |
| arrayLikeToArray.js.map | 1 | 0 | 0 | 0 | Other |
| arrayWithHoles.js | 11 | 0 | 0 | 0 | Frontend |
| arrayWithHoles.js.map | 1 | 0 | 0 | 0 | Other |
| arrayWithoutHoles.js | 12 | 0 | 0 | 0 | Frontend |
| arrayWithoutHoles.js.map | 1 | 0 | 0 | 0 | Other |
| assertClassBrand.js | 14 | 0 | 0 | 0 | Frontend |
| assertClassBrand.js.map | 1 | 0 | 0 | 0 | Other |
| assertThisInitialized.js | 14 | 0 | 0 | 0 | Frontend |
| assertThisInitialized.js.map | 1 | 0 | 0 | 0 | Other |
| asyncGeneratorDelegate.js | 52 | 0 | 0 | 0 | Frontend |
| asyncGeneratorDelegate.js.map | 1 | 0 | 0 | 0 | Other |
| asyncIterator.js | 72 | 0 | 0 | 0 | Frontend |
| asyncIterator.js.map | 1 | 0 | 0 | 0 | Other |
| asyncToGenerator.js | 38 | 0 | 0 | 0 | Frontend |
| asyncToGenerator.js.map | 1 | 0 | 0 | 0 | Other |
| awaitAsyncGenerator.js | 12 | 0 | 0 | 0 | Frontend |
| awaitAsyncGenerator.js.map | 1 | 0 | 0 | 0 | Other |
| callSuper.js | 15 | 0 | 0 | 0 | Frontend |
| callSuper.js.map | 1 | 0 | 0 | 0 | Other |
| checkInRHS.js | 14 | 0 | 0 | 0 | Frontend |
| checkInRHS.js.map | 1 | 0 | 0 | 0 | Other |
| checkPrivateRedeclaration.js | 13 | 0 | 0 | 0 | Frontend |
| checkPrivateRedeclaration.js.map | 1 | 0 | 0 | 0 | Other |
| classApplyDescriptorDestructureSet.js | 25 | 0 | 0 | 0 | Scripting |
| classApplyDescriptorDestructureSet.js.map | 1 | 0 | 0 | 0 | Scripting |
| classApplyDescriptorGet.js | 14 | 0 | 0 | 0 | Scripting |
| classApplyDescriptorGet.js.map | 1 | 0 | 0 | 0 | Scripting |
| classApplyDescriptorSet.js | 18 | 0 | 0 | 0 | Scripting |
| classApplyDescriptorSet.js.map | 1 | 0 | 0 | 0 | Scripting |
| classCallCheck.js | 13 | 0 | 0 | 0 | Frontend |
| classCallCheck.js.map | 1 | 0 | 0 | 0 | Other |
| classCheckPrivateStaticAccess.js | 12 | 0 | 0 | 0 | Testing |
| classCheckPrivateStaticAccess.js.map | 1 | 0 | 0 | 0 | Testing |
| classCheckPrivateStaticFieldDescriptor.js | 13 | 0 | 0 | 0 | Testing |
| classCheckPrivateStaticFieldDescriptor.js.map | 1 | 0 | 0 | 0 | Testing |
| classExtractFieldDescriptor.js | 12 | 0 | 0 | 0 | Scripting |
| classExtractFieldDescriptor.js.map | 1 | 0 | 0 | 0 | Scripting |
| classNameTDZError.js | 11 | 0 | 0 | 0 | Frontend |
| classNameTDZError.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateFieldDestructureSet.js | 14 | 0 | 0 | 0 | Frontend |
| classPrivateFieldDestructureSet.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateFieldGet.js | 14 | 0 | 0 | 0 | Frontend |
| classPrivateFieldGet.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateFieldGet2.js | 12 | 0 | 0 | 0 | Frontend |
| classPrivateFieldGet2.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateFieldInitSpec.js | 13 | 0 | 0 | 0 | Frontend |
| classPrivateFieldInitSpec.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateFieldLooseBase.js | 14 | 0 | 0 | 0 | Frontend |
| classPrivateFieldLooseBase.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateFieldLooseKey.js | 12 | 0 | 0 | 0 | Frontend |
| classPrivateFieldLooseKey.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateFieldSet.js | 15 | 0 | 0 | 0 | Frontend |
| classPrivateFieldSet.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateFieldSet2.js | 13 | 0 | 0 | 0 | Frontend |
| classPrivateFieldSet2.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateGetter.js | 12 | 0 | 0 | 0 | Frontend |
| classPrivateGetter.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateMethodGet.js | 13 | 0 | 0 | 0 | Frontend |
| classPrivateMethodGet.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateMethodInitSpec.js | 13 | 0 | 0 | 0 | Frontend |
| classPrivateMethodInitSpec.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateMethodSet.js | 11 | 0 | 0 | 0 | Frontend |
| classPrivateMethodSet.js.map | 1 | 0 | 0 | 0 | Other |
| classPrivateSetter.js | 13 | 0 | 0 | 0 | Frontend |
| classPrivateSetter.js.map | 1 | 0 | 0 | 0 | Other |
| classStaticPrivateFieldDestructureSet.js | 16 | 0 | 0 | 0 | Frontend |
| classStaticPrivateFieldDestructureSet.js.map | 1 | 0 | 0 | 0 | Other |
| classStaticPrivateFieldSpecGet.js | 16 | 0 | 0 | 0 | Frontend |
| classStaticPrivateFieldSpecGet.js.map | 1 | 0 | 0 | 0 | Other |
| classStaticPrivateFieldSpecSet.js | 17 | 0 | 0 | 0 | Frontend |
| classStaticPrivateFieldSpecSet.js.map | 1 | 0 | 0 | 0 | Other |
| classStaticPrivateMethodGet.js | 13 | 0 | 0 | 0 | Frontend |
| classStaticPrivateMethodGet.js.map | 1 | 0 | 0 | 0 | Other |
| classStaticPrivateMethodSet.js | 11 | 0 | 0 | 0 | Frontend |
| classStaticPrivateMethodSet.js.map | 1 | 0 | 0 | 0 | Other |
| construct.js | 20 | 0 | 0 | 0 | Frontend |
| construct.js.map | 1 | 0 | 0 | 0 | Other |
| createClass.js | 26 | 0 | 0 | 0 | Frontend |
| createClass.js.map | 1 | 0 | 0 | 0 | Other |
| createForOfIteratorHelper.js | 64 | 0 | 0 | 0 | Frontend |
| createForOfIteratorHelper.js.map | 1 | 0 | 0 | 0 | Other |
| createForOfIteratorHelperLoose.js | 29 | 0 | 0 | 0 | Frontend |
| createForOfIteratorHelperLoose.js.map | 1 | 0 | 0 | 0 | Other |
| createSuper.js | 25 | 0 | 0 | 0 | Frontend |
| createSuper.js.map | 1 | 0 | 0 | 0 | Other |
| decorate.js | 350 | 0 | 0 | 0 | Frontend |
| decorate.js.map | 1 | 0 | 0 | 0 | Other |
| defaults.js | 18 | 0 | 0 | 0 | Frontend |
| defaults.js.map | 1 | 0 | 0 | 0 | Other |
| defineAccessor.js | 16 | 0 | 0 | 0 | Frontend |
| defineAccessor.js.map | 1 | 0 | 0 | 0 | Other |
| defineEnumerableProperties.js | 27 | 0 | 0 | 0 | Frontend |
| defineEnumerableProperties.js.map | 1 | 0 | 0 | 0 | Other |
| defineProperty.js | 23 | 0 | 0 | 0 | Frontend |
| defineProperty.js.map | 1 | 0 | 0 | 0 | Other |
| dispose.js | 47 | 0 | 0 | 0 | Frontend |
| dispose.js.map | 1 | 0 | 0 | 0 | Other |
| extends.js | 22 | 0 | 0 | 0 | Frontend |
| extends.js.map | 1 | 0 | 0 | 0 | Other |
| get.js | 25 | 0 | 0 | 0 | Frontend |
| get.js.map | 1 | 0 | 0 | 0 | Other |
| getPrototypeOf.js | 14 | 0 | 0 | 0 | Frontend |
| getPrototypeOf.js.map | 1 | 0 | 0 | 0 | Other |
| identity.js | 11 | 0 | 0 | 0 | Frontend |
| identity.js.map | 1 | 0 | 0 | 0 | Other |
| importDeferProxy.js | 35 | 0 | 0 | 0 | Frontend |
| importDeferProxy.js.map | 1 | 0 | 0 | 0 | Other |
| inherits.js | 25 | 0 | 0 | 0 | Frontend |
| inherits.js.map | 1 | 0 | 0 | 0 | Other |
| inheritsLoose.js | 14 | 0 | 0 | 0 | Frontend |
| inheritsLoose.js.map | 1 | 0 | 0 | 0 | Other |
| initializerDefineProperty.js | 17 | 0 | 0 | 0 | Frontend |
| initializerDefineProperty.js.map | 1 | 0 | 0 | 0 | Other |
| initializerWarningHelper.js | 11 | 0 | 0 | 0 | Frontend |
| initializerWarningHelper.js.map | 1 | 0 | 0 | 0 | Other |
| instanceof.js | 15 | 0 | 0 | 0 | Frontend |
| instanceof.js.map | 1 | 0 | 0 | 0 | Other |
| interopRequireDefault.js | 13 | 0 | 0 | 0 | Frontend |
| interopRequireDefault.js.map | 1 | 0 | 0 | 0 | Other |
| interopRequireWildcard.js | 44 | 0 | 0 | 0 | Frontend |
| interopRequireWildcard.js.map | 1 | 0 | 0 | 0 | Other |
| isNativeFunction.js | 15 | 0 | 0 | 0 | Frontend |
| isNativeFunction.js.map | 1 | 0 | 0 | 0 | Other |
| isNativeReflectConstruct.js | 16 | 0 | 0 | 0 | Frontend |
| isNativeReflectConstruct.js.map | 1 | 0 | 0 | 0 | Other |
| iterableToArray.js | 13 | 0 | 0 | 0 | Frontend |
| iterableToArray.js.map | 1 | 0 | 0 | 0 | Other |
| iterableToArrayLimit.js | 41 | 0 | 0 | 0 | Frontend |
| iterableToArrayLimit.js.map | 1 | 0 | 0 | 0 | Other |
| jsx.js | 47 | 0 | 0 | 0 | Frontend |
| jsx.js.map | 1 | 0 | 0 | 0 | Other |
| maybeArrayLike.js | 16 | 0 | 0 | 0 | Frontend |
| maybeArrayLike.js.map | 1 | 0 | 0 | 0 | Other |
| newArrowCheck.js | 13 | 0 | 0 | 0 | Frontend |
| newArrowCheck.js.map | 1 | 0 | 0 | 0 | Other |
| nonIterableRest.js | 11 | 0 | 0 | 0 | Frontend |
| nonIterableRest.js.map | 1 | 0 | 0 | 0 | Other |
| nonIterableSpread.js | 11 | 0 | 0 | 0 | Frontend |
| nonIterableSpread.js.map | 1 | 0 | 0 | 0 | Other |
| nullishReceiverError.js | 11 | 0 | 0 | 0 | Frontend |
| nullishReceiverError.js.map | 1 | 0 | 0 | 0 | Other |
| objectDestructuringEmpty.js | 11 | 0 | 0 | 0 | Frontend |
| objectDestructuringEmpty.js.map | 1 | 0 | 0 | 0 | Other |
| objectSpread.js | 24 | 0 | 0 | 0 | Frontend |
| objectSpread.js.map | 1 | 0 | 0 | 0 | Other |
| objectSpread2.js | 39 | 0 | 0 | 0 | Frontend |
| objectSpread2.js.map | 1 | 0 | 0 | 0 | Other |
| objectWithoutProperties.js | 24 | 0 | 0 | 0 | Frontend |
| objectWithoutProperties.js.map | 1 | 0 | 0 | 0 | Other |
| objectWithoutPropertiesLoose.js | 19 | 0 | 0 | 0 | Frontend |
| objectWithoutPropertiesLoose.js.map | 1 | 0 | 0 | 0 | Other |
| possibleConstructorReturn.js | 17 | 0 | 0 | 0 | Frontend |
| possibleConstructorReturn.js.map | 1 | 0 | 0 | 0 | Other |
| readOnlyError.js | 11 | 0 | 0 | 0 | Frontend |
| readOnlyError.js.map | 1 | 0 | 0 | 0 | Other |
| regenerator.js | 188 | 0 | 0 | 0 | Frontend |
| regenerator.js.map | 1 | 0 | 0 | 0 | Other |
| regeneratorAsync.js | 15 | 0 | 0 | 0 | Frontend |
| regeneratorAsync.js.map | 1 | 0 | 0 | 0 | Other |
| regeneratorAsyncGen.js | 13 | 0 | 0 | 0 | Frontend |
| regeneratorAsyncGen.js.map | 1 | 0 | 0 | 0 | Other |
| regeneratorAsyncIterator.js | 49 | 0 | 0 | 0 | Frontend |
| regeneratorAsyncIterator.js.map | 1 | 0 | 0 | 0 | Other |
| regeneratorDefine.js | 40 | 0 | 0 | 0 | Frontend |
| regeneratorDefine.js.map | 1 | 0 | 0 | 0 | Other |
| regeneratorKeys.js | 28 | 0 | 0 | 0 | Frontend |
| regeneratorKeys.js.map | 1 | 0 | 0 | 0 | Other |
| regeneratorRuntime.js | 98 | 0 | 0 | 0 | Frontend |
| regeneratorRuntime.js.map | 1 | 0 | 0 | 0 | Other |
| regeneratorValues.js | 32 | 0 | 0 | 0 | Frontend |
| regeneratorValues.js.map | 1 | 0 | 0 | 0 | Other |
| set.js | 48 | 0 | 0 | 0 | Frontend |
| set.js.map | 1 | 0 | 0 | 0 | Other |
| setFunctionName.js | 21 | 0 | 0 | 0 | Frontend |
| setFunctionName.js.map | 1 | 0 | 0 | 0 | Other |
| setPrototypeOf.js | 15 | 0 | 0 | 0 | Frontend |
| setPrototypeOf.js.map | 1 | 0 | 0 | 0 | Other |
| skipFirstGeneratorNext.js | 15 | 0 | 0 | 0 | Frontend |
| skipFirstGeneratorNext.js.map | 1 | 0 | 0 | 0 | Other |
| slicedToArray.js | 15 | 0 | 0 | 0 | Frontend |
| slicedToArray.js.map | 1 | 0 | 0 | 0 | Other |
| superPropBase.js | 16 | 0 | 0 | 0 | Frontend |
| superPropBase.js.map | 1 | 0 | 0 | 0 | Other |
| superPropGet.js | 16 | 0 | 0 | 0 | Frontend |
| superPropGet.js.map | 1 | 0 | 0 | 0 | Other |
| superPropSet.js | 13 | 0 | 0 | 0 | Frontend |
| superPropSet.js.map | 1 | 0 | 0 | 0 | Other |
| taggedTemplateLiteral.js | 18 | 0 | 0 | 0 | Frontend |
| taggedTemplateLiteral.js.map | 1 | 0 | 0 | 0 | Other |
| taggedTemplateLiteralLoose.js | 15 | 0 | 0 | 0 | Frontend |
| taggedTemplateLiteralLoose.js.map | 1 | 0 | 0 | 0 | Other |
| tdz.js | 11 | 0 | 0 | 0 | Frontend |
| tdz.js.map | 1 | 0 | 0 | 0 | Other |
| temporalRef.js | 13 | 0 | 0 | 0 | Frontend |
| temporalRef.js.map | 1 | 0 | 0 | 0 | Other |
| temporalUndefined.js | 9 | 0 | 0 | 0 | Frontend |
| temporalUndefined.js.map | 1 | 0 | 0 | 0 | Other |
| toArray.js | 15 | 0 | 0 | 0 | Frontend |
| toArray.js.map | 1 | 0 | 0 | 0 | Other |
| toConsumableArray.js | 15 | 0 | 0 | 0 | Frontend |
| toConsumableArray.js.map | 1 | 0 | 0 | 0 | Other |
| toPrimitive.js | 18 | 0 | 0 | 0 | Frontend |
| toPrimitive.js.map | 1 | 0 | 0 | 0 | Other |
| toPropertyKey.js | 13 | 0 | 0 | 0 | Frontend |
| toPropertyKey.js.map | 1 | 0 | 0 | 0 | Other |
| toSetter.js | 18 | 0 | 0 | 0 | Frontend |
| toSetter.js.map | 1 | 0 | 0 | 0 | Other |
| tsRewriteRelativeImportExtensions.js | 16 | 0 | 0 | 0 | Frontend |
| tsRewriteRelativeImportExtensions.js.map | 1 | 0 | 0 | 0 | Other |
| typeof.js | 22 | 0 | 0 | 0 | Frontend |
| typeof.js.map | 1 | 0 | 0 | 0 | Other |
| unsupportedIterableToArray.js | 19 | 0 | 0 | 0 | Frontend |
| unsupportedIterableToArray.js.map | 1 | 0 | 0 | 0 | Other |
| using.js | 29 | 0 | 0 | 0 | Frontend |
| using.js.map | 1 | 0 | 0 | 0 | Other |
| usingCtx.js | 103 | 0 | 0 | 0 | Frontend |
| usingCtx.js.map | 1 | 0 | 0 | 0 | Other |
| wrapAsyncGenerator.js | 97 | 0 | 0 | 0 | Frontend |
| wrapAsyncGenerator.js.map | 1 | 0 | 0 | 0 | Other |
| wrapNativeSuper.js | 38 | 0 | 0 | 0 | Frontend |
| wrapNativeSuper.js.map | 1 | 0 | 0 | 0 | Other |
| wrapRegExp.js | 72 | 0 | 0 | 0 | Frontend |
| wrapRegExp.js.map | 1 | 0 | 0 | 0 | Other |
| writeOnlyError.js | 11 | 0 | 0 | 0 | Frontend |
| writeOnlyError.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/parser/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 14595 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/plugin-transform-react-jsx-self/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 61 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/plugin-transform-react-jsx-source/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 51 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/template/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| builder.js | 69 | 0 | 0 | 0 | Frontend |
| builder.js.map | 1 | 0 | 0 | 0 | Other |
| formatters.js | 61 | 0 | 0 | 0 | Frontend |
| formatters.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 23 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| literal.js | 69 | 0 | 0 | 0 | Frontend |
| literal.js.map | 1 | 0 | 0 | 0 | Other |
| options.js | 73 | 0 | 0 | 0 | Frontend |
| options.js.map | 1 | 0 | 0 | 0 | Other |
| parse.js | 163 | 0 | 0 | 0 | Frontend |
| parse.js.map | 1 | 0 | 0 | 0 | Other |
| populate.js | 138 | 0 | 0 | 0 | Frontend |
| populate.js.map | 1 | 0 | 0 | 0 | Other |
| string.js | 20 | 0 | 0 | 0 | Frontend |
| string.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/traverse/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cache.js | 38 | 0 | 0 | 0 | Frontend |
| cache.js.map | 1 | 0 | 0 | 0 | Other |
| context.js | 119 | 0 | 0 | 0 | Frontend |
| context.js.map | 1 | 0 | 0 | 0 | Other |
| hub.js | 19 | 0 | 0 | 0 | Frontend |
| hub.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 87 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| traverse-node.js | 138 | 0 | 0 | 0 | Frontend |
| traverse-node.js.map | 1 | 0 | 0 | 0 | Other |
| types.js | 3 | 0 | 0 | 0 | Frontend |
| types.js.map | 1 | 0 | 0 | 0 | Other |
| visitors.js | 258 | 0 | 0 | 0 | Frontend |
| visitors.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/traverse/lib/path`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ancestry.js | 139 | 0 | 0 | 0 | Frontend |
| ancestry.js.map | 1 | 0 | 0 | 0 | Other |
| comments.js | 52 | 0 | 0 | 0 | Frontend |
| comments.js.map | 1 | 0 | 0 | 0 | Other |
| context.js | 242 | 0 | 0 | 0 | Frontend |
| context.js.map | 1 | 0 | 0 | 0 | Other |
| conversion.js | 612 | 0 | 0 | 0 | Frontend |
| conversion.js.map | 1 | 0 | 0 | 0 | Other |
| evaluation.js | 368 | 0 | 0 | 0 | Frontend |
| evaluation.js.map | 1 | 0 | 0 | 0 | Other |
| family.js | 346 | 0 | 0 | 0 | Frontend |
| family.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 293 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| introspection.js | 398 | 0 | 0 | 0 | Frontend |
| introspection.js.map | 1 | 0 | 0 | 0 | Other |
| modification.js | 231 | 0 | 0 | 0 | Frontend |
| modification.js.map | 1 | 0 | 0 | 0 | Other |
| removal.js | 70 | 0 | 0 | 0 | Frontend |
| removal.js.map | 1 | 0 | 0 | 0 | Other |
| replacement.js | 263 | 0 | 0 | 0 | Frontend |
| replacement.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/traverse/lib/path/inference`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 149 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| inferer-reference.js | 151 | 0 | 0 | 0 | Frontend |
| inferer-reference.js.map | 1 | 0 | 0 | 0 | Other |
| inferers.js | 207 | 0 | 0 | 0 | Frontend |
| inferers.js.map | 1 | 0 | 0 | 0 | Other |
| util.js | 30 | 0 | 0 | 0 | Frontend |
| util.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/traverse/lib/path/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| hoister.js | 171 | 0 | 0 | 0 | Frontend |
| hoister.js.map | 1 | 0 | 0 | 0 | Other |
| removal-hooks.js | 37 | 0 | 0 | 0 | Frontend |
| removal-hooks.js.map | 1 | 0 | 0 | 0 | Other |
| virtual-types-validator.js | 163 | 0 | 0 | 0 | Frontend |
| virtual-types-validator.js.map | 1 | 0 | 0 | 0 | Other |
| virtual-types.js | 26 | 0 | 0 | 0 | Frontend |
| virtual-types.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/traverse/lib/scope`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| binding.js | 84 | 0 | 0 | 0 | Frontend |
| binding.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1039 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/traverse/lib/scope/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| renamer.js | 131 | 0 | 0 | 0 | Frontend |
| renamer.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index-legacy.d.ts | 2797 | 0 | 0 | 0 | Frontend |
| index.d.ts | 3308 | 0 | 0 | 0 | Frontend |
| index.js | 584 | 0 | 0 | 0 | Frontend |
| index.js.flow | 2650 | 0 | 0 | 0 | Other |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/asserts`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| assertNode.js | 16 | 0 | 0 | 0 | Frontend |
| assertNode.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/asserts/generated`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 1251 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/ast-types/generated`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 3 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/builders`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| productions.js | 12 | 0 | 0 | 0 | Frontend |
| productions.js.map | 1 | 0 | 0 | 0 | Other |
| validateNode.js | 21 | 0 | 0 | 0 | Frontend |
| validateNode.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/builders/flow`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| createFlowUnionType.js | 18 | 0 | 0 | 0 | Frontend |
| createFlowUnionType.js.map | 1 | 0 | 0 | 0 | Other |
| createTypeAnnotationBasedOnTypeof.js | 31 | 0 | 0 | 0 | Frontend |
| createTypeAnnotationBasedOnTypeof.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/builders/generated`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 29 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| lowercase.js | 2896 | 0 | 0 | 0 | Frontend |
| lowercase.js.map | 1 | 0 | 0 | 0 | Other |
| uppercase.js | 274 | 0 | 0 | 0 | Frontend |
| uppercase.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/builders/react`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| buildChildren.js | 24 | 0 | 0 | 0 | Frontend |
| buildChildren.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/builders/typescript`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| createTSUnionType.js | 22 | 0 | 0 | 0 | Scripting |
| createTSUnionType.js.map | 1 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/@babel/types/lib/clone`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| clone.js | 12 | 0 | 0 | 0 | Frontend |
| clone.js.map | 1 | 0 | 0 | 0 | Other |
| cloneDeep.js | 12 | 0 | 0 | 0 | Frontend |
| cloneDeep.js.map | 1 | 0 | 0 | 0 | Other |
| cloneDeepWithoutLoc.js | 12 | 0 | 0 | 0 | Frontend |
| cloneDeepWithoutLoc.js.map | 1 | 0 | 0 | 0 | Other |
| cloneNode.js | 107 | 0 | 0 | 0 | Frontend |
| cloneNode.js.map | 1 | 0 | 0 | 0 | Other |
| cloneWithoutLoc.js | 12 | 0 | 0 | 0 | Frontend |
| cloneWithoutLoc.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/comments`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| addComment.js | 15 | 0 | 0 | 0 | Frontend |
| addComment.js.map | 1 | 0 | 0 | 0 | Other |
| addComments.js | 22 | 0 | 0 | 0 | Frontend |
| addComments.js.map | 1 | 0 | 0 | 0 | Other |
| inheritInnerComments.js | 12 | 0 | 0 | 0 | Frontend |
| inheritInnerComments.js.map | 1 | 0 | 0 | 0 | Other |
| inheritLeadingComments.js | 12 | 0 | 0 | 0 | Frontend |
| inheritLeadingComments.js.map | 1 | 0 | 0 | 0 | Other |
| inheritTrailingComments.js | 12 | 0 | 0 | 0 | Frontend |
| inheritTrailingComments.js.map | 1 | 0 | 0 | 0 | Other |
| inheritsComments.js | 17 | 0 | 0 | 0 | Frontend |
| inheritsComments.js.map | 1 | 0 | 0 | 0 | Other |
| removeComments.js | 15 | 0 | 0 | 0 | Frontend |
| removeComments.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/constants`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 33 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/constants/generated`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 60 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/converters`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ensureBlock.js | 14 | 0 | 0 | 0 | Frontend |
| ensureBlock.js.map | 1 | 0 | 0 | 0 | Other |
| gatherSequenceExpressions.js | 66 | 0 | 0 | 0 | Frontend |
| gatherSequenceExpressions.js.map | 1 | 0 | 0 | 0 | Other |
| toBindingIdentifierName.js | 14 | 0 | 0 | 0 | Frontend |
| toBindingIdentifierName.js.map | 1 | 0 | 0 | 0 | Other |
| toBlock.js | 29 | 0 | 0 | 0 | Frontend |
| toBlock.js.map | 1 | 0 | 0 | 0 | Other |
| toComputedKey.js | 14 | 0 | 0 | 0 | Frontend |
| toComputedKey.js.map | 1 | 0 | 0 | 0 | Other |
| toExpression.js | 28 | 0 | 0 | 0 | Frontend |
| toExpression.js.map | 1 | 0 | 0 | 0 | Other |
| toIdentifier.js | 25 | 0 | 0 | 0 | Frontend |
| toIdentifier.js.map | 1 | 0 | 0 | 0 | Other |
| toKeyAlias.js | 38 | 0 | 0 | 0 | Frontend |
| toKeyAlias.js.map | 1 | 0 | 0 | 0 | Other |
| toSequenceExpression.js | 20 | 0 | 0 | 0 | Frontend |
| toSequenceExpression.js.map | 1 | 0 | 0 | 0 | Other |
| toStatement.js | 39 | 0 | 0 | 0 | Frontend |
| toStatement.js.map | 1 | 0 | 0 | 0 | Other |
| valueToNode.js | 89 | 0 | 0 | 0 | Frontend |
| valueToNode.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/definitions`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| core.js | 1659 | 0 | 0 | 0 | Frontend |
| core.js.map | 1 | 0 | 0 | 0 | Other |
| deprecated-aliases.js | 11 | 0 | 0 | 0 | Frontend |
| deprecated-aliases.js.map | 1 | 0 | 0 | 0 | Other |
| experimental.js | 126 | 0 | 0 | 0 | Frontend |
| experimental.js.map | 1 | 0 | 0 | 0 | Other |
| flow.js | 495 | 0 | 0 | 0 | Frontend |
| flow.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 100 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| jsx.js | 157 | 0 | 0 | 0 | Frontend |
| jsx.js.map | 1 | 0 | 0 | 0 | Other |
| misc.js | 33 | 0 | 0 | 0 | Frontend |
| misc.js.map | 1 | 0 | 0 | 0 | Other |
| placeholders.js | 27 | 0 | 0 | 0 | Frontend |
| placeholders.js.map | 1 | 0 | 0 | 0 | Other |
| typescript.js | 528 | 0 | 0 | 0 | Scripting |
| typescript.js.map | 1 | 0 | 0 | 0 | Scripting |
| utils.js | 292 | 0 | 0 | 0 | Frontend |
| utils.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/modifications`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| appendToMemberExpression.js | 15 | 0 | 0 | 0 | Frontend |
| appendToMemberExpression.js.map | 1 | 0 | 0 | 0 | Other |
| inherits.js | 28 | 0 | 0 | 0 | Frontend |
| inherits.js.map | 1 | 0 | 0 | 0 | Other |
| prependToMemberExpression.js | 17 | 0 | 0 | 0 | Frontend |
| prependToMemberExpression.js.map | 1 | 0 | 0 | 0 | Other |
| removeProperties.js | 24 | 0 | 0 | 0 | Frontend |
| removeProperties.js.map | 1 | 0 | 0 | 0 | Other |
| removePropertiesDeep.js | 14 | 0 | 0 | 0 | Frontend |
| removePropertiesDeep.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/modifications/flow`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| removeTypeDuplicates.js | 65 | 0 | 0 | 0 | Frontend |
| removeTypeDuplicates.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/modifications/typescript`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| removeTypeDuplicates.js | 66 | 0 | 0 | 0 | Scripting |
| removeTypeDuplicates.js.map | 1 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/@babel/types/lib/retrievers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| getAssignmentIdentifiers.js | 48 | 0 | 0 | 0 | Frontend |
| getAssignmentIdentifiers.js.map | 1 | 0 | 0 | 0 | Other |
| getBindingIdentifiers.js | 102 | 0 | 0 | 0 | Frontend |
| getBindingIdentifiers.js.map | 1 | 0 | 0 | 0 | Other |
| getFunctionName.js | 63 | 0 | 0 | 0 | Frontend |
| getFunctionName.js.map | 1 | 0 | 0 | 0 | Other |
| getOuterBindingIdentifiers.js | 13 | 0 | 0 | 0 | Frontend |
| getOuterBindingIdentifiers.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/traverse`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| traverse.js | 50 | 0 | 0 | 0 | Frontend |
| traverse.js.map | 1 | 0 | 0 | 0 | Other |
| traverseFast.js | 40 | 0 | 0 | 0 | Frontend |
| traverseFast.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| deprecationWarning.js | 44 | 0 | 0 | 0 | Frontend |
| deprecationWarning.js.map | 1 | 0 | 0 | 0 | Other |
| inherit.js | 13 | 0 | 0 | 0 | Frontend |
| inherit.js.map | 1 | 0 | 0 | 0 | Other |
| shallowEqual.js | 17 | 0 | 0 | 0 | Frontend |
| shallowEqual.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/utils/react`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cleanJSXElementLiteralChild.js | 40 | 0 | 0 | 0 | Frontend |
| cleanJSXElementLiteralChild.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/validators`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| buildMatchMemberExpression.js | 13 | 0 | 0 | 0 | Frontend |
| buildMatchMemberExpression.js.map | 1 | 0 | 0 | 0 | Other |
| is.js | 27 | 0 | 0 | 0 | Frontend |
| is.js.map | 1 | 0 | 0 | 0 | Other |
| isBinding.js | 27 | 0 | 0 | 0 | Frontend |
| isBinding.js.map | 1 | 0 | 0 | 0 | Other |
| isBlockScoped.js | 13 | 0 | 0 | 0 | Frontend |
| isBlockScoped.js.map | 1 | 0 | 0 | 0 | Other |
| isImmutable.js | 21 | 0 | 0 | 0 | Frontend |
| isImmutable.js.map | 1 | 0 | 0 | 0 | Other |
| isLet.js | 17 | 0 | 0 | 0 | Frontend |
| isLet.js.map | 1 | 0 | 0 | 0 | Other |
| isNode.js | 12 | 0 | 0 | 0 | Frontend |
| isNode.js.map | 1 | 0 | 0 | 0 | Other |
| isNodesEquivalent.js | 57 | 0 | 0 | 0 | Frontend |
| isNodesEquivalent.js.map | 1 | 0 | 0 | 0 | Other |
| isPlaceholderType.js | 15 | 0 | 0 | 0 | Frontend |
| isPlaceholderType.js.map | 1 | 0 | 0 | 0 | Other |
| isReferenced.js | 96 | 0 | 0 | 0 | Frontend |
| isReferenced.js.map | 1 | 0 | 0 | 0 | Other |
| isScope.js | 18 | 0 | 0 | 0 | Frontend |
| isScope.js.map | 1 | 0 | 0 | 0 | Other |
| isSpecifierDefault.js | 14 | 0 | 0 | 0 | Frontend |
| isSpecifierDefault.js.map | 1 | 0 | 0 | 0 | Other |
| isType.js | 17 | 0 | 0 | 0 | Frontend |
| isType.js.map | 1 | 0 | 0 | 0 | Other |
| isValidES3Identifier.js | 13 | 0 | 0 | 0 | Frontend |
| isValidES3Identifier.js.map | 1 | 0 | 0 | 0 | Other |
| isValidIdentifier.js | 18 | 0 | 0 | 0 | Frontend |
| isValidIdentifier.js.map | 1 | 0 | 0 | 0 | Other |
| isVar.js | 19 | 0 | 0 | 0 | Frontend |
| isVar.js.map | 1 | 0 | 0 | 0 | Other |
| matchesPattern.js | 44 | 0 | 0 | 0 | Frontend |
| matchesPattern.js.map | 1 | 0 | 0 | 0 | Other |
| validate.js | 42 | 0 | 0 | 0 | Frontend |
| validate.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/validators/generated`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 2797 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@babel/types/lib/validators/react`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| isCompatTag.js | 11 | 0 | 0 | 0 | Frontend |
| isCompatTag.js.map | 1 | 0 | 0 | 0 | Other |
| isReactComponent.js | 11 | 0 | 0 | 0 | Frontend |
| isReactComponent.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@floating-ui/core/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| floating-ui.core.browser.min.mjs | 1 | 0 | 0 | 0 | Other |
| floating-ui.core.browser.mjs | 1178 | 0 | 0 | 0 | Other |
| floating-ui.core.d.mts | 528 | 0 | 0 | 0 | Other |
| floating-ui.core.d.ts | 528 | 0 | 0 | 0 | Frontend |
| floating-ui.core.esm.js | 1049 | 0 | 0 | 0 | Frontend |
| floating-ui.core.mjs | 1049 | 0 | 0 | 0 | Other |
| floating-ui.core.umd.js | 1197 | 0 | 0 | 0 | Frontend |
| floating-ui.core.umd.min.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/@floating-ui/dom/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| floating-ui.dom.browser.min.mjs | 1 | 0 | 0 | 0 | Other |
| floating-ui.dom.browser.mjs | 948 | 0 | 0 | 0 | Other |
| floating-ui.dom.d.mts | 356 | 0 | 0 | 0 | Other |
| floating-ui.dom.d.ts | 356 | 0 | 0 | 0 | Frontend |
| floating-ui.dom.esm.js | 777 | 0 | 0 | 0 | Frontend |
| floating-ui.dom.mjs | 777 | 0 | 0 | 0 | Other |
| floating-ui.dom.umd.js | 967 | 0 | 0 | 0 | Frontend |
| floating-ui.dom.umd.min.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/@floating-ui/react-dom/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| floating-ui.react-dom.d.mts | 307 | 0 | 0 | 0 | Other |
| floating-ui.react-dom.d.ts | 307 | 0 | 0 | 0 | Frontend |
| floating-ui.react-dom.esm.js | 371 | 0 | 0 | 0 | Frontend |
| floating-ui.react-dom.mjs | 371 | 0 | 0 | 0 | Other |
| floating-ui.react-dom.umd.js | 422 | 0 | 0 | 0 | Frontend |
| floating-ui.react-dom.umd.min.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/@floating-ui/utils/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| floating-ui.utils.d.mts | 103 | 0 | 0 | 0 | Other |
| floating-ui.utils.d.ts | 103 | 0 | 0 | 0 | Frontend |
| floating-ui.utils.dom.d.mts | 47 | 0 | 0 | 0 | Other |
| floating-ui.utils.dom.d.ts | 47 | 0 | 0 | 0 | Frontend |
| floating-ui.utils.dom.esm.js | 161 | 0 | 0 | 0 | Frontend |
| floating-ui.utils.dom.mjs | 161 | 0 | 0 | 0 | Other |
| floating-ui.utils.dom.umd.js | 188 | 0 | 0 | 0 | Frontend |
| floating-ui.utils.dom.umd.min.js | 1 | 0 | 0 | 0 | Frontend |
| floating-ui.utils.esm.js | 139 | 0 | 0 | 0 | Frontend |
| floating-ui.utils.mjs | 139 | 0 | 0 | 0 | Other |
| floating-ui.utils.umd.js | 170 | 0 | 0 | 0 | Frontend |
| floating-ui.utils.umd.min.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/@isaacs/cliui/build`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.cjs | 317 | 0 | 0 | 0 | Other |
| index.d.cts | 43 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@isaacs/cliui/build/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 302 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/@isaacs/fs-minipass/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 118 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 430 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/@isaacs/fs-minipass/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 118 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 420 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/@jridgewell/gen-mapping/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| gen-mapping.mjs | 292 | 0 | 0 | 0 | Other |
| gen-mapping.mjs.map | 6 | 0 | 0 | 0 | Other |
| gen-mapping.umd.js | 358 | 0 | 0 | 0 | Frontend |
| gen-mapping.umd.js.map | 6 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@jridgewell/gen-mapping/dist/types`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| gen-mapping.d.ts | 88 | 0 | 0 | 0 | Frontend |
| set-array.d.ts | 32 | 0 | 0 | 0 | Frontend |
| sourcemap-segment.d.ts | 12 | 0 | 0 | 0 | Frontend |
| types.d.ts | 43 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/@jridgewell/remapping/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| remapping.mjs | 144 | 0 | 0 | 0 | Other |
| remapping.mjs.map | 6 | 0 | 0 | 0 | Other |
| remapping.umd.js | 212 | 0 | 0 | 0 | Frontend |
| remapping.umd.js.map | 6 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@jridgewell/resolve-uri/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| resolve-uri.mjs | 232 | 0 | 0 | 0 | Other |
| resolve-uri.mjs.map | 1 | 0 | 0 | 0 | Other |
| resolve-uri.umd.js | 240 | 0 | 0 | 0 | Frontend |
| resolve-uri.umd.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@jridgewell/resolve-uri/dist/types`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| resolve-uri.d.ts | 4 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/@jridgewell/sourcemap-codec/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| sourcemap-codec.mjs | 423 | 0 | 0 | 0 | Other |
| sourcemap-codec.mjs.map | 6 | 0 | 0 | 0 | Other |
| sourcemap-codec.umd.js | 464 | 0 | 0 | 0 | Frontend |
| sourcemap-codec.umd.js.map | 6 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@jridgewell/trace-mapping/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| trace-mapping.mjs | 493 | 0 | 0 | 0 | Other |
| trace-mapping.mjs.map | 6 | 0 | 0 | 0 | Other |
| trace-mapping.umd.js | 559 | 0 | 0 | 0 | Frontend |
| trace-mapping.umd.js.map | 6 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/number/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 3 | 0 | 0 | 0 | Other |
| index.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.js | 31 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 8 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/primitive/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 20 | 0 | 0 | 0 | Other |
| index.d.ts | 20 | 0 | 0 | 0 | Frontend |
| index.js | 76 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 53 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-accordion/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 114 | 0 | 0 | 0 | Other |
| index.d.ts | 114 | 0 | 0 | 0 | Frontend |
| index.js | 352 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 320 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-alert-dialog/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 51 | 0 | 0 | 0 | Other |
| index.d.ts | 51 | 0 | 0 | 0 | Frontend |
| index.js | 202 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 170 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-arrow/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 10 | 0 | 0 | 0 | Other |
| index.d.ts | 10 | 0 | 0 | 0 | Frontend |
| index.js | 60 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 27 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-aspect-ratio/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 11 | 0 | 0 | 0 | Other |
| index.d.ts | 11 | 0 | 0 | 0 | Frontend |
| index.js | 79 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 46 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-avatar/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 24 | 0 | 0 | 0 | Other |
| index.d.ts | 24 | 0 | 0 | 0 | Frontend |
| index.js | 160 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 128 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-checkbox/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 50 | 0 | 0 | 0 | Other |
| index.d.ts | 50 | 0 | 0 | 0 | Frontend |
| index.js | 316 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 284 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-collapsible/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 33 | 0 | 0 | 0 | Other |
| index.d.ts | 33 | 0 | 0 | 0 | Frontend |
| index.js | 187 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 155 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-collection/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 98 | 0 | 0 | 0 | Other |
| index.d.ts | 98 | 0 | 0 | 0 | Frontend |
| index.js | 577 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 545 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-compose-refs/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 15 | 0 | 0 | 0 | Other |
| index.d.ts | 15 | 0 | 0 | 0 | Frontend |
| index.js | 74 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 41 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-context-menu/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 96 | 0 | 0 | 0 | Other |
| index.d.ts | 96 | 0 | 0 | 0 | Frontend |
| index.js | 357 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 325 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-context/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 21 | 0 | 0 | 0 | Other |
| index.d.ts | 21 | 0 | 0 | 0 | Frontend |
| index.js | 114 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 81 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-dialog/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 103 | 0 | 0 | 0 | Other |
| index.d.ts | 103 | 0 | 0 | 0 | Frontend |
| index.js | 374 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 342 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-direction/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 12 | 0 | 0 | 0 | Other |
| index.d.ts | 12 | 0 | 0 | 0 | Frontend |
| index.js | 52 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 19 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-dismissable-layer/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 51 | 0 | 0 | 0 | Other |
| index.d.ts | 51 | 0 | 0 | 0 | Frontend |
| index.js | 253 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 221 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-dropdown-menu/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 97 | 0 | 0 | 0 | Other |
| index.d.ts | 97 | 0 | 0 | 0 | Frontend |
| index.js | 337 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 305 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-focus-guards/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 13 | 0 | 0 | 0 | Other |
| index.d.ts | 13 | 0 | 0 | 0 | Frontend |
| index.js | 71 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 39 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-focus-scope/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 32 | 0 | 0 | 0 | Other |
| index.d.ts | 32 | 0 | 0 | 0 | Frontend |
| index.js | 246 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 214 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-hover-card/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 79 | 0 | 0 | 0 | Other |
| index.d.ts | 79 | 0 | 0 | 0 | Frontend |
| index.js | 294 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 262 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-id/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 3 | 0 | 0 | 0 | Other |
| index.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.js | 49 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 16 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-label/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 10 | 0 | 0 | 0 | Other |
| index.d.ts | 10 | 0 | 0 | 0 | Frontend |
| index.js | 61 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 29 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-menu/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 169 | 0 | 0 | 0 | Other |
| index.d.ts | 169 | 0 | 0 | 0 | Frontend |
| index.js | 904 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 872 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-menubar/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 115 | 0 | 0 | 0 | Other |
| index.d.ts | 115 | 0 | 0 | 0 | Frontend |
| index.js | 502 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 470 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-navigation-menu/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 126 | 0 | 0 | 0 | Other |
| index.d.ts | 126 | 0 | 0 | 0 | Frontend |
| index.js | 838 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 806 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-popover/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 85 | 0 | 0 | 0 | Other |
| index.d.ts | 85 | 0 | 0 | 0 | Frontend |
| index.js | 352 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 320 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-popper/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 46 | 0 | 0 | 0 | Other |
| index.d.ts | 46 | 0 | 0 | 0 | Frontend |
| index.js | 330 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 308 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-portal/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 14 | 0 | 0 | 0 | Other |
| index.d.ts | 14 | 0 | 0 | 0 | Frontend |
| index.js | 55 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 23 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-presence/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 12 | 0 | 0 | 0 | Other |
| index.d.ts | 12 | 0 | 0 | 0 | Frontend |
| index.js | 171 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 139 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-primitive/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 52 | 0 | 0 | 0 | Other |
| index.d.ts | 52 | 0 | 0 | 0 | Frontend |
| index.js | 80 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 47 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-progress/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 19 | 0 | 0 | 0 | Other |
| index.d.ts | 19 | 0 | 0 | 0 | Frontend |
| index.js | 133 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 101 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-radio-group/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 58 | 0 | 0 | 0 | Other |
| index.d.ts | 58 | 0 | 0 | 0 | Frontend |
| index.js | 335 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 303 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-roving-focus/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 49 | 0 | 0 | 0 | Other |
| index.d.ts | 49 | 0 | 0 | 0 | Frontend |
| index.js | 263 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 231 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-scroll-area/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 123 | 0 | 0 | 0 | Other |
| index.d.ts | 123 | 0 | 0 | 0 | Frontend |
| index.js | 771 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 739 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-select/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 137 | 0 | 0 | 0 | Other |
| index.d.ts | 137 | 0 | 0 | 0 | Frontend |
| index.js | 1228 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 1196 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-separator/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 21 | 0 | 0 | 0 | Other |
| index.d.ts | 21 | 0 | 0 | 0 | Frontend |
| index.js | 65 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 32 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-slider/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 75 | 0 | 0 | 0 | Other |
| index.d.ts | 75 | 0 | 0 | 0 | Frontend |
| index.js | 598 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 566 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-slot/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 17 | 0 | 0 | 0 | Other |
| index.d.ts | 17 | 0 | 0 | 0 | Frontend |
| index.js | 138 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 105 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-switch/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 21 | 0 | 0 | 0 | Other |
| index.d.ts | 21 | 0 | 0 | 0 | Frontend |
| index.js | 192 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 160 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-tabs/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 56 | 0 | 0 | 0 | Other |
| index.d.ts | 56 | 0 | 0 | 0 | Frontend |
| index.js | 232 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 200 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-toast/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 120 | 0 | 0 | 0 | Other |
| index.d.ts | 120 | 0 | 0 | 0 | Frontend |
| index.js | 677 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 645 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-toggle-group/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 75 | 0 | 0 | 0 | Other |
| index.d.ts | 75 | 0 | 0 | 0 | Frontend |
| index.js | 209 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 177 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-toggle/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 24 | 0 | 0 | 0 | Other |
| index.d.ts | 24 | 0 | 0 | 0 | Frontend |
| index.js | 73 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 41 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-tooltip/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 101 | 0 | 0 | 0 | Other |
| index.d.ts | 101 | 0 | 0 | 0 | Frontend |
| index.js | 540 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 508 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-use-callback-ref/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 7 | 0 | 0 | 0 | Other |
| index.d.ts | 7 | 0 | 0 | 0 | Frontend |
| index.js | 46 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 13 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-use-controllable-state/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 40 | 0 | 0 | 0 | Other |
| index.d.ts | 40 | 0 | 0 | 0 | Frontend |
| index.js | 169 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 136 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-use-effect-event/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 8 | 0 | 0 | 0 | Other |
| index.d.ts | 8 | 0 | 0 | 0 | Frontend |
| index.js | 60 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 27 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-use-escape-keydown/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 6 | 0 | 0 | 0 | Other |
| index.d.ts | 6 | 0 | 0 | 0 | Frontend |
| index.js | 52 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 19 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-use-is-hydrated/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 6 | 0 | 0 | 0 | Other |
| index.d.ts | 6 | 0 | 0 | 0 | Frontend |
| index.js | 40 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 17 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-use-layout-effect/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 12 | 0 | 0 | 0 | Other |
| index.d.ts | 12 | 0 | 0 | 0 | Frontend |
| index.js | 41 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 8 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-use-previous/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 3 | 0 | 0 | 0 | Other |
| index.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.js | 49 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 16 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-use-rect/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 9 | 0 | 0 | 0 | Other |
| index.d.ts | 9 | 0 | 0 | 0 | Frontend |
| index.js | 54 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 21 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-use-size/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 6 | 0 | 0 | 0 | Other |
| index.d.ts | 6 | 0 | 0 | 0 | Frontend |
| index.js | 74 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 41 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/react-visually-hidden/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 22 | 0 | 0 | 0 | Other |
| index.d.ts | 22 | 0 | 0 | 0 | Frontend |
| index.js | 71 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 38 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@radix-ui/rect/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 16 | 0 | 0 | 0 | Other |
| index.d.ts | 16 | 0 | 0 | 0 | Frontend |
| index.js | 73 | 0 | 0 | 0 | Frontend |
| index.js.map | 7 | 0 | 0 | 0 | Other |
| index.mjs | 50 | 0 | 0 | 0 | Other |
| index.mjs.map | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@rolldown/pluginutils/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.cjs | 271 | 0 | 0 | 0 | Other |
| index.d.cts | 157 | 0 | 0 | 0 | Other |
| index.d.ts | 157 | 0 | 0 | 0 | Frontend |
| index.js | 255 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/@tailwindcss/node/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| esm-cache.loader.d.mts | 5 | 0 | 0 | 0 | Other |
| esm-cache.loader.mjs | 1 | 0 | 0 | 0 | Other |
| index.d.mts | 251 | 0 | 0 | 0 | Other |
| index.d.ts | 251 | 0 | 0 | 0 | Frontend |
| index.js | 16 | 0 | 0 | 0 | Frontend |
| index.mjs | 16 | 0 | 0 | 0 | Other |
| require-cache.d.ts | 3 | 0 | 0 | 0 | Frontend |
| require-cache.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/@tailwindcss/node/node_modules/tailwindcss/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| chunk-G32FJCSR.mjs | 1 | 0 | 0 | 0 | Other |
| chunk-HTB5LLOP.mjs | 1 | 0 | 0 | 0 | Other |
| chunk-U5SIPDGO.mjs | 35 | 0 | 0 | 0 | Other |
| colors-b_6i0Oi7.d.ts | 295 | 0 | 0 | 0 | Frontend |
| colors.d.mts | 295 | 0 | 0 | 0 | Other |
| colors.d.ts | 5 | 0 | 0 | 0 | Frontend |
| colors.js | 1 | 0 | 0 | 0 | Frontend |
| colors.mjs | 1 | 0 | 0 | 0 | Other |
| default-theme.d.mts | 1147 | 0 | 0 | 0 | Other |
| default-theme.d.ts | 1147 | 0 | 0 | 0 | Frontend |
| default-theme.js | 1 | 0 | 0 | 0 | Frontend |
| default-theme.mjs | 1 | 0 | 0 | 0 | Other |
| flatten-color-palette.d.mts | 6 | 0 | 0 | 0 | Other |
| flatten-color-palette.d.ts | 6 | 0 | 0 | 0 | Frontend |
| flatten-color-palette.js | 3 | 0 | 0 | 0 | Frontend |
| flatten-color-palette.mjs | 1 | 0 | 0 | 0 | Other |
| lib.d.mts | 351 | 0 | 0 | 0 | Other |
| lib.d.ts | 3 | 0 | 0 | 0 | Frontend |
| lib.js | 35 | 0 | 0 | 0 | Frontend |
| lib.mjs | 1 | 0 | 0 | 0 | Other |
| plugin.d.mts | 11 | 0 | 0 | 0 | Other |
| plugin.d.ts | 131 | 0 | 0 | 0 | Frontend |
| plugin.js | 1 | 0 | 0 | 0 | Frontend |
| plugin.mjs | 1 | 0 | 0 | 0 | Other |
| resolve-config-BIFUA2FY.d.ts | 29 | 0 | 0 | 0 | Configuration |
| resolve-config-QUZ9b-Gn.d.mts | 190 | 0 | 0 | 0 | Configuration |
| types-WlZgYgM8.d.mts | 125 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tailwindcss/vite/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 5 | 0 | 0 | 0 | Other |
| index.mjs | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tailwindcss/vite/node_modules/tailwindcss/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| chunk-G32FJCSR.mjs | 1 | 0 | 0 | 0 | Other |
| chunk-HTB5LLOP.mjs | 1 | 0 | 0 | 0 | Other |
| chunk-U5SIPDGO.mjs | 35 | 0 | 0 | 0 | Other |
| colors-b_6i0Oi7.d.ts | 295 | 0 | 0 | 0 | Frontend |
| colors.d.mts | 295 | 0 | 0 | 0 | Other |
| colors.d.ts | 5 | 0 | 0 | 0 | Frontend |
| colors.js | 1 | 0 | 0 | 0 | Frontend |
| colors.mjs | 1 | 0 | 0 | 0 | Other |
| default-theme.d.mts | 1147 | 0 | 0 | 0 | Other |
| default-theme.d.ts | 1147 | 0 | 0 | 0 | Frontend |
| default-theme.js | 1 | 0 | 0 | 0 | Frontend |
| default-theme.mjs | 1 | 0 | 0 | 0 | Other |
| flatten-color-palette.d.mts | 6 | 0 | 0 | 0 | Other |
| flatten-color-palette.d.ts | 6 | 0 | 0 | 0 | Frontend |
| flatten-color-palette.js | 3 | 0 | 0 | 0 | Frontend |
| flatten-color-palette.mjs | 1 | 0 | 0 | 0 | Other |
| lib.d.mts | 351 | 0 | 0 | 0 | Other |
| lib.d.ts | 3 | 0 | 0 | 0 | Frontend |
| lib.js | 35 | 0 | 0 | 0 | Frontend |
| lib.mjs | 1 | 0 | 0 | 0 | Other |
| plugin.d.mts | 11 | 0 | 0 | 0 | Other |
| plugin.d.ts | 131 | 0 | 0 | 0 | Frontend |
| plugin.js | 1 | 0 | 0 | 0 | Frontend |
| plugin.mjs | 1 | 0 | 0 | 0 | Other |
| resolve-config-BIFUA2FY.d.ts | 29 | 0 | 0 | 0 | Configuration |
| resolve-config-QUZ9b-Gn.d.mts | 190 | 0 | 0 | 0 | Configuration |
| types-WlZgYgM8.d.mts | 125 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/query-core/build/legacy`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| chunk-PXG64RU4.js | 25 | 0 | 0 | 0 | Frontend |
| chunk-PXG64RU4.js.map | 1 | 0 | 0 | 0 | Other |
| focusManager.cjs | 108 | 0 | 0 | 0 | Other |
| focusManager.cjs.map | 1 | 0 | 0 | 0 | Other |
| focusManager.d.cts | 17 | 0 | 0 | 0 | Other |
| focusManager.d.ts | 17 | 0 | 0 | 0 | Frontend |
| focusManager.js | 81 | 0 | 0 | 0 | Frontend |
| focusManager.js.map | 1 | 0 | 0 | 0 | Other |
| hydration-B0J2Tmyo.d.ts | 1376 | 0 | 0 | 0 | Frontend |
| hydration-CGqN5JZ-.d.cts | 1376 | 0 | 0 | 0 | Other |
| hydration.cjs | 172 | 0 | 0 | 0 | Other |
| hydration.cjs.map | 1 | 0 | 0 | 0 | Other |
| hydration.d.cts | 3 | 0 | 0 | 0 | Other |
| hydration.d.ts | 3 | 0 | 0 | 0 | Frontend |
| hydration.js | 146 | 0 | 0 | 0 | Frontend |
| hydration.js.map | 1 | 0 | 0 | 0 | Other |
| index.cjs | 110 | 0 | 0 | 0 | Other |
| index.cjs.map | 1 | 0 | 0 | 0 | Other |
| index.d.cts | 10 | 0 | 0 | 0 | Other |
| index.d.ts | 10 | 0 | 0 | 0 | Frontend |
| index.js | 73 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryBehavior.cjs | 154 | 0 | 0 | 0 | Other |
| infiniteQueryBehavior.cjs.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryBehavior.d.cts | 15 | 0 | 0 | 0 | Other |
| infiniteQueryBehavior.d.ts | 15 | 0 | 0 | 0 | Frontend |
| infiniteQueryBehavior.js | 129 | 0 | 0 | 0 | Frontend |
| infiniteQueryBehavior.js.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryObserver.cjs | 93 | 0 | 0 | 0 | Other |
| infiniteQueryObserver.cjs.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryObserver.d.cts | 20 | 0 | 0 | 0 | Other |
| infiniteQueryObserver.d.ts | 20 | 0 | 0 | 0 | Frontend |
| infiniteQueryObserver.js | 74 | 0 | 0 | 0 | Frontend |
| infiniteQueryObserver.js.map | 1 | 0 | 0 | 0 | Other |
| mutation.cjs | 319 | 0 | 0 | 0 | Other |
| mutation.cjs.map | 1 | 0 | 0 | 0 | Other |
| mutation.d.cts | 3 | 0 | 0 | 0 | Other |
| mutation.d.ts | 3 | 0 | 0 | 0 | Frontend |
| mutation.js | 292 | 0 | 0 | 0 | Frontend |
| mutation.js.map | 1 | 0 | 0 | 0 | Other |
| mutationCache.cjs | 170 | 0 | 0 | 0 | Other |
| mutationCache.cjs.map | 1 | 0 | 0 | 0 | Other |
| mutationCache.d.cts | 3 | 0 | 0 | 0 | Other |
| mutationCache.d.ts | 3 | 0 | 0 | 0 | Frontend |
| mutationCache.js | 137 | 0 | 0 | 0 | Frontend |
| mutationCache.js.map | 1 | 0 | 0 | 0 | Other |
| mutationObserver.cjs | 174 | 0 | 0 | 0 | Other |
| mutationObserver.cjs.map | 1 | 0 | 0 | 0 | Other |
| mutationObserver.d.cts | 3 | 0 | 0 | 0 | Other |
| mutationObserver.d.ts | 3 | 0 | 0 | 0 | Frontend |
| mutationObserver.js | 148 | 0 | 0 | 0 | Frontend |
| mutationObserver.js.map | 1 | 0 | 0 | 0 | Other |
| notifyManager.cjs | 113 | 0 | 0 | 0 | Other |
| notifyManager.cjs.map | 1 | 0 | 0 | 0 | Other |
| notifyManager.d.cts | 46 | 0 | 0 | 0 | Other |
| notifyManager.d.ts | 46 | 0 | 0 | 0 | Frontend |
| notifyManager.js | 88 | 0 | 0 | 0 | Frontend |
| notifyManager.js.map | 1 | 0 | 0 | 0 | Other |
| onlineManager.cjs | 97 | 0 | 0 | 0 | Other |
| onlineManager.cjs.map | 1 | 0 | 0 | 0 | Other |
| onlineManager.d.cts | 16 | 0 | 0 | 0 | Other |
| onlineManager.d.ts | 16 | 0 | 0 | 0 | Frontend |
| onlineManager.js | 70 | 0 | 0 | 0 | Frontend |
| onlineManager.js.map | 1 | 0 | 0 | 0 | Other |
| queriesObserver.cjs | 247 | 0 | 0 | 0 | Other |
| queriesObserver.cjs.map | 1 | 0 | 0 | 0 | Other |
| queriesObserver.d.cts | 27 | 0 | 0 | 0 | Other |
| queriesObserver.d.ts | 27 | 0 | 0 | 0 | Frontend |
| queriesObserver.js | 221 | 0 | 0 | 0 | Frontend |
| queriesObserver.js.map | 1 | 0 | 0 | 0 | Other |
| query.cjs | 471 | 0 | 0 | 0 | Other |
| query.cjs.map | 1 | 0 | 0 | 0 | Other |
| query.d.cts | 3 | 0 | 0 | 0 | Other |
| query.d.ts | 3 | 0 | 0 | 0 | Frontend |
| query.js | 452 | 0 | 0 | 0 | Frontend |
| query.js.map | 1 | 0 | 0 | 0 | Other |
| queryCache.cjs | 131 | 0 | 0 | 0 | Other |
| queryCache.cjs.map | 1 | 0 | 0 | 0 | Other |
| queryCache.d.cts | 3 | 0 | 0 | 0 | Other |
| queryCache.d.ts | 3 | 0 | 0 | 0 | Frontend |
| queryCache.js | 105 | 0 | 0 | 0 | Frontend |
| queryCache.js.map | 1 | 0 | 0 | 0 | Other |
| queryClient.cjs | 349 | 0 | 0 | 0 | Other |
| queryClient.cjs.map | 1 | 0 | 0 | 0 | Other |
| queryClient.d.cts | 3 | 0 | 0 | 0 | Other |
| queryClient.d.ts | 3 | 0 | 0 | 0 | Frontend |
| queryClient.js | 324 | 0 | 0 | 0 | Frontend |
| queryClient.js.map | 1 | 0 | 0 | 0 | Other |
| queryObserver.cjs | 510 | 0 | 0 | 0 | Other |
| queryObserver.cjs.map | 1 | 0 | 0 | 0 | Other |
| queryObserver.d.cts | 3 | 0 | 0 | 0 | Other |
| queryObserver.d.ts | 3 | 0 | 0 | 0 | Frontend |
| queryObserver.js | 493 | 0 | 0 | 0 | Frontend |
| queryObserver.js.map | 1 | 0 | 0 | 0 | Other |
| removable.cjs | 69 | 0 | 0 | 0 | Other |
| removable.cjs.map | 1 | 0 | 0 | 0 | Other |
| removable.d.cts | 11 | 0 | 0 | 0 | Other |
| removable.d.ts | 11 | 0 | 0 | 0 | Frontend |
| removable.js | 43 | 0 | 0 | 0 | Frontend |
| removable.js.map | 1 | 0 | 0 | 0 | Other |
| retryer.cjs | 165 | 0 | 0 | 0 | Other |
| retryer.cjs.map | 1 | 0 | 0 | 0 | Other |
| retryer.d.cts | 3 | 0 | 0 | 0 | Other |
| retryer.d.ts | 3 | 0 | 0 | 0 | Frontend |
| retryer.js | 139 | 0 | 0 | 0 | Frontend |
| retryer.js.map | 1 | 0 | 0 | 0 | Other |
| streamedQuery.cjs | 68 | 0 | 0 | 0 | Other |
| streamedQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| streamedQuery.d.cts | 34 | 0 | 0 | 0 | Other |
| streamedQuery.d.ts | 34 | 0 | 0 | 0 | Frontend |
| streamedQuery.js | 45 | 0 | 0 | 0 | Frontend |
| streamedQuery.js.map | 1 | 0 | 0 | 0 | Other |
| subscribable.cjs | 51 | 0 | 0 | 0 | Other |
| subscribable.cjs.map | 1 | 0 | 0 | 0 | Other |
| subscribable.d.cts | 10 | 0 | 0 | 0 | Other |
| subscribable.d.ts | 10 | 0 | 0 | 0 | Frontend |
| subscribable.js | 28 | 0 | 0 | 0 | Frontend |
| subscribable.js.map | 1 | 0 | 0 | 0 | Other |
| thenable.cjs | 76 | 0 | 0 | 0 | Other |
| thenable.cjs.map | 1 | 0 | 0 | 0 | Other |
| thenable.d.cts | 47 | 0 | 0 | 0 | Other |
| thenable.d.ts | 47 | 0 | 0 | 0 | Frontend |
| thenable.js | 52 | 0 | 0 | 0 | Frontend |
| thenable.js.map | 1 | 0 | 0 | 0 | Other |
| timeoutManager.cjs | 110 | 0 | 0 | 0 | Other |
| timeoutManager.cjs.map | 1 | 0 | 0 | 0 | Other |
| timeoutManager.d.cts | 58 | 0 | 0 | 0 | Other |
| timeoutManager.d.ts | 58 | 0 | 0 | 0 | Frontend |
| timeoutManager.js | 81 | 0 | 0 | 0 | Frontend |
| timeoutManager.js.map | 1 | 0 | 0 | 0 | Other |
| types.cjs | 37 | 0 | 0 | 0 | Other |
| types.cjs.map | 1 | 0 | 0 | 0 | Other |
| types.d.cts | 3 | 0 | 0 | 0 | Other |
| types.d.ts | 3 | 0 | 0 | 0 | Frontend |
| types.js | 12 | 0 | 0 | 0 | Frontend |
| types.js.map | 1 | 0 | 0 | 0 | Other |
| utils.cjs | 306 | 0 | 0 | 0 | Other |
| utils.cjs.map | 1 | 0 | 0 | 0 | Other |
| utils.d.cts | 3 | 0 | 0 | 0 | Other |
| utils.d.ts | 3 | 0 | 0 | 0 | Frontend |
| utils.js | 260 | 0 | 0 | 0 | Frontend |
| utils.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/query-core/build/modern`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| focusManager.cjs | 94 | 0 | 0 | 0 | Other |
| focusManager.cjs.map | 1 | 0 | 0 | 0 | Other |
| focusManager.d.cts | 17 | 0 | 0 | 0 | Other |
| focusManager.d.ts | 17 | 0 | 0 | 0 | Frontend |
| focusManager.js | 68 | 0 | 0 | 0 | Frontend |
| focusManager.js.map | 1 | 0 | 0 | 0 | Other |
| hydration-B0J2Tmyo.d.ts | 1376 | 0 | 0 | 0 | Frontend |
| hydration-CGqN5JZ-.d.cts | 1376 | 0 | 0 | 0 | Other |
| hydration.cjs | 167 | 0 | 0 | 0 | Other |
| hydration.cjs.map | 1 | 0 | 0 | 0 | Other |
| hydration.d.cts | 3 | 0 | 0 | 0 | Other |
| hydration.d.ts | 3 | 0 | 0 | 0 | Frontend |
| hydration.js | 139 | 0 | 0 | 0 | Frontend |
| hydration.js.map | 1 | 0 | 0 | 0 | Other |
| index.cjs | 110 | 0 | 0 | 0 | Other |
| index.cjs.map | 1 | 0 | 0 | 0 | Other |
| index.d.cts | 10 | 0 | 0 | 0 | Other |
| index.d.ts | 10 | 0 | 0 | 0 | Frontend |
| index.js | 71 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryBehavior.cjs | 150 | 0 | 0 | 0 | Other |
| infiniteQueryBehavior.cjs.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryBehavior.d.cts | 15 | 0 | 0 | 0 | Other |
| infiniteQueryBehavior.d.ts | 15 | 0 | 0 | 0 | Frontend |
| infiniteQueryBehavior.js | 123 | 0 | 0 | 0 | Frontend |
| infiniteQueryBehavior.js.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryObserver.cjs | 92 | 0 | 0 | 0 | Other |
| infiniteQueryObserver.cjs.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryObserver.d.cts | 20 | 0 | 0 | 0 | Other |
| infiniteQueryObserver.d.ts | 20 | 0 | 0 | 0 | Frontend |
| infiniteQueryObserver.js | 71 | 0 | 0 | 0 | Frontend |
| infiniteQueryObserver.js.map | 1 | 0 | 0 | 0 | Other |
| mutation.cjs | 292 | 0 | 0 | 0 | Other |
| mutation.cjs.map | 1 | 0 | 0 | 0 | Other |
| mutation.d.cts | 3 | 0 | 0 | 0 | Other |
| mutation.d.ts | 3 | 0 | 0 | 0 | Frontend |
| mutation.js | 266 | 0 | 0 | 0 | Frontend |
| mutation.js.map | 1 | 0 | 0 | 0 | Other |
| mutationCache.cjs | 149 | 0 | 0 | 0 | Other |
| mutationCache.cjs.map | 1 | 0 | 0 | 0 | Other |
| mutationCache.d.cts | 3 | 0 | 0 | 0 | Other |
| mutationCache.d.ts | 3 | 0 | 0 | 0 | Frontend |
| mutationCache.js | 124 | 0 | 0 | 0 | Frontend |
| mutationCache.js.map | 1 | 0 | 0 | 0 | Other |
| mutationObserver.cjs | 149 | 0 | 0 | 0 | Other |
| mutationObserver.cjs.map | 1 | 0 | 0 | 0 | Other |
| mutationObserver.d.cts | 3 | 0 | 0 | 0 | Other |
| mutationObserver.d.ts | 3 | 0 | 0 | 0 | Frontend |
| mutationObserver.js | 124 | 0 | 0 | 0 | Frontend |
| mutationObserver.js.map | 1 | 0 | 0 | 0 | Other |
| notifyManager.cjs | 113 | 0 | 0 | 0 | Other |
| notifyManager.cjs.map | 1 | 0 | 0 | 0 | Other |
| notifyManager.d.cts | 46 | 0 | 0 | 0 | Other |
| notifyManager.d.ts | 46 | 0 | 0 | 0 | Frontend |
| notifyManager.js | 86 | 0 | 0 | 0 | Frontend |
| notifyManager.js.map | 1 | 0 | 0 | 0 | Other |
| onlineManager.cjs | 84 | 0 | 0 | 0 | Other |
| onlineManager.cjs.map | 1 | 0 | 0 | 0 | Other |
| onlineManager.d.cts | 16 | 0 | 0 | 0 | Other |
| onlineManager.d.ts | 16 | 0 | 0 | 0 | Frontend |
| onlineManager.js | 58 | 0 | 0 | 0 | Frontend |
| onlineManager.js.map | 1 | 0 | 0 | 0 | Other |
| queriesObserver.cjs | 226 | 0 | 0 | 0 | Other |
| queriesObserver.cjs.map | 1 | 0 | 0 | 0 | Other |
| queriesObserver.d.cts | 27 | 0 | 0 | 0 | Other |
| queriesObserver.d.ts | 27 | 0 | 0 | 0 | Frontend |
| queriesObserver.js | 201 | 0 | 0 | 0 | Frontend |
| queriesObserver.js.map | 1 | 0 | 0 | 0 | Other |
| query.cjs | 445 | 0 | 0 | 0 | Other |
| query.cjs.map | 1 | 0 | 0 | 0 | Other |
| query.d.cts | 3 | 0 | 0 | 0 | Other |
| query.d.ts | 3 | 0 | 0 | 0 | Frontend |
| query.js | 427 | 0 | 0 | 0 | Frontend |
| query.js.map | 1 | 0 | 0 | 0 | Other |
| queryCache.cjs | 122 | 0 | 0 | 0 | Other |
| queryCache.cjs.map | 1 | 0 | 0 | 0 | Other |
| queryCache.d.cts | 3 | 0 | 0 | 0 | Other |
| queryCache.d.ts | 3 | 0 | 0 | 0 | Frontend |
| queryCache.js | 97 | 0 | 0 | 0 | Frontend |
| queryCache.js.map | 1 | 0 | 0 | 0 | Other |
| queryClient.cjs | 322 | 0 | 0 | 0 | Other |
| queryClient.cjs.map | 1 | 0 | 0 | 0 | Other |
| queryClient.d.cts | 3 | 0 | 0 | 0 | Other |
| queryClient.d.ts | 3 | 0 | 0 | 0 | Frontend |
| queryClient.js | 305 | 0 | 0 | 0 | Frontend |
| queryClient.js.map | 1 | 0 | 0 | 0 | Other |
| queryObserver.cjs | 483 | 0 | 0 | 0 | Other |
| queryObserver.cjs.map | 1 | 0 | 0 | 0 | Other |
| queryObserver.d.cts | 3 | 0 | 0 | 0 | Other |
| queryObserver.d.ts | 3 | 0 | 0 | 0 | Frontend |
| queryObserver.js | 467 | 0 | 0 | 0 | Frontend |
| queryObserver.js.map | 1 | 0 | 0 | 0 | Other |
| removable.cjs | 58 | 0 | 0 | 0 | Other |
| removable.cjs.map | 1 | 0 | 0 | 0 | Other |
| removable.d.cts | 11 | 0 | 0 | 0 | Other |
| removable.d.ts | 11 | 0 | 0 | 0 | Frontend |
| removable.js | 33 | 0 | 0 | 0 | Frontend |
| removable.js.map | 1 | 0 | 0 | 0 | Other |
| retryer.cjs | 161 | 0 | 0 | 0 | Other |
| retryer.cjs.map | 1 | 0 | 0 | 0 | Other |
| retryer.d.cts | 3 | 0 | 0 | 0 | Other |
| retryer.d.ts | 3 | 0 | 0 | 0 | Frontend |
| retryer.js | 133 | 0 | 0 | 0 | Frontend |
| retryer.js.map | 1 | 0 | 0 | 0 | Other |
| streamedQuery.cjs | 68 | 0 | 0 | 0 | Other |
| streamedQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| streamedQuery.d.cts | 34 | 0 | 0 | 0 | Other |
| streamedQuery.d.ts | 34 | 0 | 0 | 0 | Frontend |
| streamedQuery.js | 43 | 0 | 0 | 0 | Frontend |
| streamedQuery.js.map | 1 | 0 | 0 | 0 | Other |
| subscribable.cjs | 51 | 0 | 0 | 0 | Other |
| subscribable.cjs.map | 1 | 0 | 0 | 0 | Other |
| subscribable.d.cts | 10 | 0 | 0 | 0 | Other |
| subscribable.d.ts | 10 | 0 | 0 | 0 | Frontend |
| subscribable.js | 26 | 0 | 0 | 0 | Frontend |
| subscribable.js.map | 1 | 0 | 0 | 0 | Other |
| thenable.cjs | 75 | 0 | 0 | 0 | Other |
| thenable.cjs.map | 1 | 0 | 0 | 0 | Other |
| thenable.d.cts | 47 | 0 | 0 | 0 | Other |
| thenable.d.ts | 47 | 0 | 0 | 0 | Frontend |
| thenable.js | 49 | 0 | 0 | 0 | Frontend |
| thenable.js.map | 1 | 0 | 0 | 0 | Other |
| timeoutManager.cjs | 98 | 0 | 0 | 0 | Other |
| timeoutManager.cjs.map | 1 | 0 | 0 | 0 | Other |
| timeoutManager.d.cts | 58 | 0 | 0 | 0 | Other |
| timeoutManager.d.ts | 58 | 0 | 0 | 0 | Frontend |
| timeoutManager.js | 70 | 0 | 0 | 0 | Frontend |
| timeoutManager.js.map | 1 | 0 | 0 | 0 | Other |
| types.cjs | 37 | 0 | 0 | 0 | Other |
| types.cjs.map | 1 | 0 | 0 | 0 | Other |
| types.d.cts | 3 | 0 | 0 | 0 | Other |
| types.d.ts | 3 | 0 | 0 | 0 | Frontend |
| types.js | 10 | 0 | 0 | 0 | Frontend |
| types.js.map | 1 | 0 | 0 | 0 | Other |
| utils.cjs | 306 | 0 | 0 | 0 | Other |
| utils.cjs.map | 1 | 0 | 0 | 0 | Other |
| utils.d.cts | 3 | 0 | 0 | 0 | Other |
| utils.d.ts | 3 | 0 | 0 | 0 | Frontend |
| utils.js | 258 | 0 | 0 | 0 | Frontend |
| utils.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.cjs | 208 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/utils/transformers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| query-cache-transformer.cjs | 124 | 0 | 0 | 0 | Other |
| query-client-transformer.cjs | 53 | 0 | 0 | 0 | Other |
| use-query-like-transformer.cjs | 38 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v4`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| key-transformation.cjs | 181 | 0 | 0 | 0 | Other |
| replace-import-specifier.cjs | 25 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v4/utils/replacers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| key-replacer.cjs | 164 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v5/is-loading`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| is-loading.cjs | 244 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v5/keep-previous-data`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 32 | 0 | 0 | 0 | Documentation |
| keep-previous-data.cjs | 271 | 0 | 0 | 0 | Data |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v5/keep-previous-data/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| already-has-placeholder-data-property.cjs | 26 | 0 | 0 | 0 | Data |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v5/remove-overloads`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| remove-overloads.cjs | 58 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v5/remove-overloads/transformers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| filter-aware-usage-transformer.cjs | 271 | 0 | 0 | 0 | Other |
| query-fn-aware-usage-transformer.cjs | 185 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v5/remove-overloads/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.cjs | 123 | 0 | 0 | 0 | Other |
| unknown-usage-error.cjs | 27 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v5/rename-hydrate`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| rename-hydrate.cjs | 55 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/codemods/src/v5/rename-properties`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| rename-properties.cjs | 41 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/legacy`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| HydrationBoundary.cjs | 89 | 0 | 0 | 0 | Other |
| HydrationBoundary.cjs.map | 1 | 0 | 0 | 0 | Other |
| HydrationBoundary.d.cts | 14 | 0 | 0 | 0 | Other |
| HydrationBoundary.d.ts | 14 | 0 | 0 | 0 | Frontend |
| HydrationBoundary.js | 55 | 0 | 0 | 0 | Frontend |
| HydrationBoundary.js.map | 1 | 0 | 0 | 0 | Other |
| IsRestoringProvider.cjs | 47 | 0 | 0 | 0 | Other |
| IsRestoringProvider.cjs.map | 1 | 0 | 0 | 0 | Other |
| IsRestoringProvider.d.cts | 6 | 0 | 0 | 0 | Other |
| IsRestoringProvider.d.ts | 6 | 0 | 0 | 0 | Frontend |
| IsRestoringProvider.js | 12 | 0 | 0 | 0 | Frontend |
| IsRestoringProvider.js.map | 1 | 0 | 0 | 0 | Other |
| QueryClientProvider.cjs | 72 | 0 | 0 | 0 | Other |
| QueryClientProvider.cjs.map | 1 | 0 | 0 | 0 | Other |
| QueryClientProvider.d.cts | 12 | 0 | 0 | 0 | Other |
| QueryClientProvider.d.ts | 12 | 0 | 0 | 0 | Frontend |
| QueryClientProvider.js | 36 | 0 | 0 | 0 | Frontend |
| QueryClientProvider.js.map | 1 | 0 | 0 | 0 | Other |
| QueryErrorResetBoundary.cjs | 67 | 0 | 0 | 0 | Other |
| QueryErrorResetBoundary.cjs.map | 1 | 0 | 0 | 0 | Other |
| QueryErrorResetBoundary.d.cts | 19 | 0 | 0 | 0 | Other |
| QueryErrorResetBoundary.d.ts | 19 | 0 | 0 | 0 | Frontend |
| QueryErrorResetBoundary.js | 32 | 0 | 0 | 0 | Frontend |
| QueryErrorResetBoundary.js.map | 1 | 0 | 0 | 0 | Other |
| errorBoundaryUtils.cjs | 68 | 0 | 0 | 0 | Other |
| errorBoundaryUtils.cjs.map | 1 | 0 | 0 | 0 | Other |
| errorBoundaryUtils.d.cts | 16 | 0 | 0 | 0 | Other |
| errorBoundaryUtils.d.ts | 16 | 0 | 0 | 0 | Frontend |
| errorBoundaryUtils.js | 32 | 0 | 0 | 0 | Frontend |
| errorBoundaryUtils.js.map | 1 | 0 | 0 | 0 | Other |
| index.cjs | 97 | 0 | 0 | 0 | Other |
| index.cjs.map | 1 | 0 | 0 | 0 | Other |
| index.d.cts | 22 | 0 | 0 | 0 | Other |
| index.d.ts | 22 | 0 | 0 | 0 | Frontend |
| index.js | 54 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryOptions.cjs | 33 | 0 | 0 | 0 | Other |
| infiniteQueryOptions.cjs.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryOptions.d.cts | 23 | 0 | 0 | 0 | Other |
| infiniteQueryOptions.d.ts | 23 | 0 | 0 | 0 | Frontend |
| infiniteQueryOptions.js | 8 | 0 | 0 | 0 | Frontend |
| infiniteQueryOptions.js.map | 1 | 0 | 0 | 0 | Other |
| mutationOptions.cjs | 33 | 0 | 0 | 0 | Other |
| mutationOptions.cjs.map | 1 | 0 | 0 | 0 | Other |
| mutationOptions.d.cts | 7 | 0 | 0 | 0 | Other |
| mutationOptions.d.ts | 7 | 0 | 0 | 0 | Frontend |
| mutationOptions.js | 8 | 0 | 0 | 0 | Frontend |
| mutationOptions.js.map | 1 | 0 | 0 | 0 | Other |
| queryOptions.cjs | 33 | 0 | 0 | 0 | Other |
| queryOptions.cjs.map | 1 | 0 | 0 | 0 | Other |
| queryOptions.d.cts | 24 | 0 | 0 | 0 | Other |
| queryOptions.d.ts | 24 | 0 | 0 | 0 | Frontend |
| queryOptions.js | 8 | 0 | 0 | 0 | Frontend |
| queryOptions.js.map | 1 | 0 | 0 | 0 | Other |
| suspense.cjs | 58 | 0 | 0 | 0 | Other |
| suspense.cjs.map | 1 | 0 | 0 | 0 | Other |
| suspense.d.cts | 12 | 0 | 0 | 0 | Other |
| suspense.d.ts | 12 | 0 | 0 | 0 | Frontend |
| suspense.js | 29 | 0 | 0 | 0 | Frontend |
| suspense.js.map | 1 | 0 | 0 | 0 | Other |
| types.cjs | 19 | 0 | 0 | 0 | Other |
| types.cjs.map | 1 | 0 | 0 | 0 | Other |
| types.d.cts | 52 | 0 | 0 | 0 | Other |
| types.d.ts | 52 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |
| types.js.map | 1 | 0 | 0 | 0 | Other |
| useBaseQuery.cjs | 132 | 0 | 0 | 0 | Other |
| useBaseQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useBaseQuery.d.cts | 6 | 0 | 0 | 0 | Other |
| useBaseQuery.d.ts | 6 | 0 | 0 | 0 | Frontend |
| useBaseQuery.js | 107 | 0 | 0 | 0 | Frontend |
| useBaseQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useInfiniteQuery.cjs | 40 | 0 | 0 | 0 | Other |
| useInfiniteQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useInfiniteQuery.d.cts | 9 | 0 | 0 | 0 | Other |
| useInfiniteQuery.d.ts | 9 | 0 | 0 | 0 | Frontend |
| useInfiniteQuery.js | 16 | 0 | 0 | 0 | Frontend |
| useInfiniteQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useIsFetching.cjs | 56 | 0 | 0 | 0 | Other |
| useIsFetching.cjs.map | 1 | 0 | 0 | 0 | Other |
| useIsFetching.d.cts | 5 | 0 | 0 | 0 | Other |
| useIsFetching.d.ts | 5 | 0 | 0 | 0 | Frontend |
| useIsFetching.js | 22 | 0 | 0 | 0 | Frontend |
| useIsFetching.js.map | 1 | 0 | 0 | 0 | Other |
| useMutation.cjs | 74 | 0 | 0 | 0 | Other |
| useMutation.cjs.map | 1 | 0 | 0 | 0 | Other |
| useMutation.d.cts | 6 | 0 | 0 | 0 | Other |
| useMutation.d.ts | 6 | 0 | 0 | 0 | Frontend |
| useMutation.js | 45 | 0 | 0 | 0 | Frontend |
| useMutation.js.map | 1 | 0 | 0 | 0 | Other |
| useMutationState.cjs | 86 | 0 | 0 | 0 | Other |
| useMutationState.cjs.map | 1 | 0 | 0 | 0 | Other |
| useMutationState.d.cts | 10 | 0 | 0 | 0 | Other |
| useMutationState.d.ts | 10 | 0 | 0 | 0 | Frontend |
| useMutationState.js | 51 | 0 | 0 | 0 | Frontend |
| useMutationState.js.map | 1 | 0 | 0 | 0 | Other |
| usePrefetchInfiniteQuery.cjs | 37 | 0 | 0 | 0 | Other |
| usePrefetchInfiniteQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| usePrefetchInfiniteQuery.d.cts | 5 | 0 | 0 | 0 | Other |
| usePrefetchInfiniteQuery.d.ts | 5 | 0 | 0 | 0 | Frontend |
| usePrefetchInfiniteQuery.js | 12 | 0 | 0 | 0 | Frontend |
| usePrefetchInfiniteQuery.js.map | 1 | 0 | 0 | 0 | Other |
| usePrefetchQuery.cjs | 37 | 0 | 0 | 0 | Other |
| usePrefetchQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| usePrefetchQuery.d.cts | 6 | 0 | 0 | 0 | Other |
| usePrefetchQuery.d.ts | 6 | 0 | 0 | 0 | Frontend |
| usePrefetchQuery.js | 12 | 0 | 0 | 0 | Frontend |
| usePrefetchQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useQueries.cjs | 131 | 0 | 0 | 0 | Other |
| useQueries.cjs.map | 1 | 0 | 0 | 0 | Other |
| useQueries.d.cts | 76 | 0 | 0 | 0 | Other |
| useQueries.d.ts | 76 | 0 | 0 | 0 | Frontend |
| useQueries.js | 111 | 0 | 0 | 0 | Frontend |
| useQueries.js.map | 1 | 0 | 0 | 0 | Other |
| useQuery.cjs | 36 | 0 | 0 | 0 | Other |
| useQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useQuery.d.cts | 9 | 0 | 0 | 0 | Other |
| useQuery.d.ts | 9 | 0 | 0 | 0 | Frontend |
| useQuery.js | 12 | 0 | 0 | 0 | Frontend |
| useQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseInfiniteQuery.cjs | 51 | 0 | 0 | 0 | Other |
| useSuspenseInfiniteQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseInfiniteQuery.d.cts | 6 | 0 | 0 | 0 | Other |
| useSuspenseInfiniteQuery.d.ts | 6 | 0 | 0 | 0 | Frontend |
| useSuspenseInfiniteQuery.js | 27 | 0 | 0 | 0 | Frontend |
| useSuspenseInfiniteQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseQueries.cjs | 56 | 0 | 0 | 0 | Other |
| useSuspenseQueries.cjs.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseQueries.d.cts | 79 | 0 | 0 | 0 | Other |
| useSuspenseQueries.d.ts | 79 | 0 | 0 | 0 | Frontend |
| useSuspenseQueries.js | 32 | 0 | 0 | 0 | Frontend |
| useSuspenseQueries.js.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseQuery.cjs | 52 | 0 | 0 | 0 | Other |
| useSuspenseQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseQuery.d.cts | 6 | 0 | 0 | 0 | Other |
| useSuspenseQuery.d.ts | 6 | 0 | 0 | 0 | Frontend |
| useSuspenseQuery.js | 28 | 0 | 0 | 0 | Frontend |
| useSuspenseQuery.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/modern`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| HydrationBoundary.cjs | 89 | 0 | 0 | 0 | Other |
| HydrationBoundary.cjs.map | 1 | 0 | 0 | 0 | Other |
| HydrationBoundary.d.cts | 14 | 0 | 0 | 0 | Other |
| HydrationBoundary.d.ts | 14 | 0 | 0 | 0 | Frontend |
| HydrationBoundary.js | 55 | 0 | 0 | 0 | Frontend |
| HydrationBoundary.js.map | 1 | 0 | 0 | 0 | Other |
| IsRestoringProvider.cjs | 47 | 0 | 0 | 0 | Other |
| IsRestoringProvider.cjs.map | 1 | 0 | 0 | 0 | Other |
| IsRestoringProvider.d.cts | 6 | 0 | 0 | 0 | Other |
| IsRestoringProvider.d.ts | 6 | 0 | 0 | 0 | Frontend |
| IsRestoringProvider.js | 12 | 0 | 0 | 0 | Frontend |
| IsRestoringProvider.js.map | 1 | 0 | 0 | 0 | Other |
| QueryClientProvider.cjs | 72 | 0 | 0 | 0 | Other |
| QueryClientProvider.cjs.map | 1 | 0 | 0 | 0 | Other |
| QueryClientProvider.d.cts | 12 | 0 | 0 | 0 | Other |
| QueryClientProvider.d.ts | 12 | 0 | 0 | 0 | Frontend |
| QueryClientProvider.js | 36 | 0 | 0 | 0 | Frontend |
| QueryClientProvider.js.map | 1 | 0 | 0 | 0 | Other |
| QueryErrorResetBoundary.cjs | 67 | 0 | 0 | 0 | Other |
| QueryErrorResetBoundary.cjs.map | 1 | 0 | 0 | 0 | Other |
| QueryErrorResetBoundary.d.cts | 19 | 0 | 0 | 0 | Other |
| QueryErrorResetBoundary.d.ts | 19 | 0 | 0 | 0 | Frontend |
| QueryErrorResetBoundary.js | 32 | 0 | 0 | 0 | Frontend |
| QueryErrorResetBoundary.js.map | 1 | 0 | 0 | 0 | Other |
| errorBoundaryUtils.cjs | 68 | 0 | 0 | 0 | Other |
| errorBoundaryUtils.cjs.map | 1 | 0 | 0 | 0 | Other |
| errorBoundaryUtils.d.cts | 16 | 0 | 0 | 0 | Other |
| errorBoundaryUtils.d.ts | 16 | 0 | 0 | 0 | Frontend |
| errorBoundaryUtils.js | 32 | 0 | 0 | 0 | Frontend |
| errorBoundaryUtils.js.map | 1 | 0 | 0 | 0 | Other |
| index.cjs | 97 | 0 | 0 | 0 | Other |
| index.cjs.map | 1 | 0 | 0 | 0 | Other |
| index.d.cts | 22 | 0 | 0 | 0 | Other |
| index.d.ts | 22 | 0 | 0 | 0 | Frontend |
| index.js | 54 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryOptions.cjs | 33 | 0 | 0 | 0 | Other |
| infiniteQueryOptions.cjs.map | 1 | 0 | 0 | 0 | Other |
| infiniteQueryOptions.d.cts | 23 | 0 | 0 | 0 | Other |
| infiniteQueryOptions.d.ts | 23 | 0 | 0 | 0 | Frontend |
| infiniteQueryOptions.js | 8 | 0 | 0 | 0 | Frontend |
| infiniteQueryOptions.js.map | 1 | 0 | 0 | 0 | Other |
| mutationOptions.cjs | 33 | 0 | 0 | 0 | Other |
| mutationOptions.cjs.map | 1 | 0 | 0 | 0 | Other |
| mutationOptions.d.cts | 7 | 0 | 0 | 0 | Other |
| mutationOptions.d.ts | 7 | 0 | 0 | 0 | Frontend |
| mutationOptions.js | 8 | 0 | 0 | 0 | Frontend |
| mutationOptions.js.map | 1 | 0 | 0 | 0 | Other |
| queryOptions.cjs | 33 | 0 | 0 | 0 | Other |
| queryOptions.cjs.map | 1 | 0 | 0 | 0 | Other |
| queryOptions.d.cts | 24 | 0 | 0 | 0 | Other |
| queryOptions.d.ts | 24 | 0 | 0 | 0 | Frontend |
| queryOptions.js | 8 | 0 | 0 | 0 | Frontend |
| queryOptions.js.map | 1 | 0 | 0 | 0 | Other |
| suspense.cjs | 58 | 0 | 0 | 0 | Other |
| suspense.cjs.map | 1 | 0 | 0 | 0 | Other |
| suspense.d.cts | 12 | 0 | 0 | 0 | Other |
| suspense.d.ts | 12 | 0 | 0 | 0 | Frontend |
| suspense.js | 29 | 0 | 0 | 0 | Frontend |
| suspense.js.map | 1 | 0 | 0 | 0 | Other |
| types.cjs | 19 | 0 | 0 | 0 | Other |
| types.cjs.map | 1 | 0 | 0 | 0 | Other |
| types.d.cts | 52 | 0 | 0 | 0 | Other |
| types.d.ts | 52 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |
| types.js.map | 1 | 0 | 0 | 0 | Other |
| useBaseQuery.cjs | 129 | 0 | 0 | 0 | Other |
| useBaseQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useBaseQuery.d.cts | 6 | 0 | 0 | 0 | Other |
| useBaseQuery.d.ts | 6 | 0 | 0 | 0 | Frontend |
| useBaseQuery.js | 104 | 0 | 0 | 0 | Frontend |
| useBaseQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useInfiniteQuery.cjs | 40 | 0 | 0 | 0 | Other |
| useInfiniteQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useInfiniteQuery.d.cts | 9 | 0 | 0 | 0 | Other |
| useInfiniteQuery.d.ts | 9 | 0 | 0 | 0 | Frontend |
| useInfiniteQuery.js | 16 | 0 | 0 | 0 | Frontend |
| useInfiniteQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useIsFetching.cjs | 56 | 0 | 0 | 0 | Other |
| useIsFetching.cjs.map | 1 | 0 | 0 | 0 | Other |
| useIsFetching.d.cts | 5 | 0 | 0 | 0 | Other |
| useIsFetching.d.ts | 5 | 0 | 0 | 0 | Frontend |
| useIsFetching.js | 22 | 0 | 0 | 0 | Frontend |
| useIsFetching.js.map | 1 | 0 | 0 | 0 | Other |
| useMutation.cjs | 74 | 0 | 0 | 0 | Other |
| useMutation.cjs.map | 1 | 0 | 0 | 0 | Other |
| useMutation.d.cts | 6 | 0 | 0 | 0 | Other |
| useMutation.d.ts | 6 | 0 | 0 | 0 | Frontend |
| useMutation.js | 45 | 0 | 0 | 0 | Frontend |
| useMutation.js.map | 1 | 0 | 0 | 0 | Other |
| useMutationState.cjs | 86 | 0 | 0 | 0 | Other |
| useMutationState.cjs.map | 1 | 0 | 0 | 0 | Other |
| useMutationState.d.cts | 10 | 0 | 0 | 0 | Other |
| useMutationState.d.ts | 10 | 0 | 0 | 0 | Frontend |
| useMutationState.js | 51 | 0 | 0 | 0 | Frontend |
| useMutationState.js.map | 1 | 0 | 0 | 0 | Other |
| usePrefetchInfiniteQuery.cjs | 37 | 0 | 0 | 0 | Other |
| usePrefetchInfiniteQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| usePrefetchInfiniteQuery.d.cts | 5 | 0 | 0 | 0 | Other |
| usePrefetchInfiniteQuery.d.ts | 5 | 0 | 0 | 0 | Frontend |
| usePrefetchInfiniteQuery.js | 12 | 0 | 0 | 0 | Frontend |
| usePrefetchInfiniteQuery.js.map | 1 | 0 | 0 | 0 | Other |
| usePrefetchQuery.cjs | 37 | 0 | 0 | 0 | Other |
| usePrefetchQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| usePrefetchQuery.d.cts | 6 | 0 | 0 | 0 | Other |
| usePrefetchQuery.d.ts | 6 | 0 | 0 | 0 | Frontend |
| usePrefetchQuery.js | 12 | 0 | 0 | 0 | Frontend |
| usePrefetchQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useQueries.cjs | 131 | 0 | 0 | 0 | Other |
| useQueries.cjs.map | 1 | 0 | 0 | 0 | Other |
| useQueries.d.cts | 76 | 0 | 0 | 0 | Other |
| useQueries.d.ts | 76 | 0 | 0 | 0 | Frontend |
| useQueries.js | 111 | 0 | 0 | 0 | Frontend |
| useQueries.js.map | 1 | 0 | 0 | 0 | Other |
| useQuery.cjs | 36 | 0 | 0 | 0 | Other |
| useQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useQuery.d.cts | 9 | 0 | 0 | 0 | Other |
| useQuery.d.ts | 9 | 0 | 0 | 0 | Frontend |
| useQuery.js | 12 | 0 | 0 | 0 | Frontend |
| useQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseInfiniteQuery.cjs | 51 | 0 | 0 | 0 | Other |
| useSuspenseInfiniteQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseInfiniteQuery.d.cts | 6 | 0 | 0 | 0 | Other |
| useSuspenseInfiniteQuery.d.ts | 6 | 0 | 0 | 0 | Frontend |
| useSuspenseInfiniteQuery.js | 27 | 0 | 0 | 0 | Frontend |
| useSuspenseInfiniteQuery.js.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseQueries.cjs | 56 | 0 | 0 | 0 | Other |
| useSuspenseQueries.cjs.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseQueries.d.cts | 79 | 0 | 0 | 0 | Other |
| useSuspenseQueries.d.ts | 79 | 0 | 0 | 0 | Frontend |
| useSuspenseQueries.js | 32 | 0 | 0 | 0 | Frontend |
| useSuspenseQueries.js.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseQuery.cjs | 52 | 0 | 0 | 0 | Other |
| useSuspenseQuery.cjs.map | 1 | 0 | 0 | 0 | Other |
| useSuspenseQuery.d.cts | 6 | 0 | 0 | 0 | Other |
| useSuspenseQuery.d.ts | 6 | 0 | 0 | 0 | Frontend |
| useSuspenseQuery.js | 28 | 0 | 0 | 0 | Frontend |
| useSuspenseQuery.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/@tanstack/react-query/build/query-codemods`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| eslint.config.js | 18 | 0 | 0 | 0 | Configuration |
| package.json | 38 | 0 | 0 | 0 | Configuration |
| root.eslint.config.js | 55 | 0 | 0 | 0 | Configuration |
| tsconfig.json | 8 | 0 | 0 | 0 | Configuration |
| vite.config.ts | 26 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/@vitejs/plugin-react/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.cjs | 343 | 0 | 0 | 0 | Other |
| index.d.cts | 67 | 0 | 0 | 0 | Other |
| index.d.ts | 67 | 0 | 0 | 0 | Frontend |
| index.js | 320 | 0 | 0 | 0 | Frontend |
| refresh-runtime.js | 670 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/aria-hidden/dist/es2015`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 29 | 0 | 0 | 0 | Frontend |
| index.js | 167 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/aria-hidden/dist/es2019`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 29 | 0 | 0 | 0 | Frontend |
| index.js | 156 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/aria-hidden/dist/es5`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 29 | 0 | 0 | 0 | Frontend |
| index.js | 174 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/autoprefixer/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| at-rule.js | 35 | 0 | 0 | 0 | Frontend |
| autoprefixer.d.ts | 95 | 0 | 0 | 0 | Frontend |
| autoprefixer.js | 164 | 0 | 0 | 0 | Frontend |
| brackets.js | 51 | 0 | 0 | 0 | Frontend |
| browsers.js | 79 | 0 | 0 | 0 | Frontend |
| declaration.js | 187 | 0 | 0 | 0 | Frontend |
| info.js | 123 | 0 | 0 | 0 | Frontend |
| old-selector.js | 67 | 0 | 0 | 0 | Frontend |
| old-value.js | 22 | 0 | 0 | 0 | Frontend |
| prefixer.js | 144 | 0 | 0 | 0 | Frontend |
| prefixes.js | 428 | 0 | 0 | 0 | Frontend |
| processor.js | 709 | 0 | 0 | 0 | Frontend |
| resolution.js | 97 | 0 | 0 | 0 | Frontend |
| selector.js | 150 | 0 | 0 | 0 | Frontend |
| supports.js | 302 | 0 | 0 | 0 | Frontend |
| transition.js | 329 | 0 | 0 | 0 | Frontend |
| utils.js | 93 | 0 | 0 | 0 | Frontend |
| value.js | 125 | 0 | 0 | 0 | Frontend |
| vendor.js | 14 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/autoprefixer/lib/hacks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| align-content.js | 49 | 0 | 0 | 0 | Frontend |
| align-items.js | 46 | 0 | 0 | 0 | Frontend |
| align-self.js | 56 | 0 | 0 | 0 | Frontend |
| animation.js | 17 | 0 | 0 | 0 | Frontend |
| appearance.js | 23 | 0 | 0 | 0 | Frontend |
| autofill.js | 26 | 0 | 0 | 0 | Frontend |
| backdrop-filter.js | 20 | 0 | 0 | 0 | Frontend |
| background-clip.js | 24 | 0 | 0 | 0 | Frontend |
| background-size.js | 23 | 0 | 0 | 0 | Frontend |
| block-logical.js | 40 | 0 | 0 | 0 | Frontend |
| border-image.js | 15 | 0 | 0 | 0 | Frontend |
| border-radius.js | 40 | 0 | 0 | 0 | Frontend |
| break-props.js | 63 | 0 | 0 | 0 | Frontend |
| cross-fade.js | 35 | 0 | 0 | 0 | Frontend |
| display-flex.js | 65 | 0 | 0 | 0 | Frontend |
| display-grid.js | 21 | 0 | 0 | 0 | Frontend |
| file-selector-button.js | 26 | 0 | 0 | 0 | Frontend |
| filter-value.js | 14 | 0 | 0 | 0 | Frontend |
| filter.js | 19 | 0 | 0 | 0 | Frontend |
| flex-basis.js | 39 | 0 | 0 | 0 | Frontend |
| flex-direction.js | 72 | 0 | 0 | 0 | Frontend |
| flex-flow.js | 53 | 0 | 0 | 0 | Frontend |
| flex-grow.js | 30 | 0 | 0 | 0 | Frontend |
| flex-shrink.js | 39 | 0 | 0 | 0 | Frontend |
| flex-spec.js | 19 | 0 | 0 | 0 | Frontend |
| flex-wrap.js | 19 | 0 | 0 | 0 | Frontend |
| flex.js | 54 | 0 | 0 | 0 | Frontend |
| fullscreen.js | 20 | 0 | 0 | 0 | Frontend |
| gradient.js | 448 | 0 | 0 | 0 | Frontend |
| grid-area.js | 34 | 0 | 0 | 0 | Frontend |
| grid-column-align.js | 28 | 0 | 0 | 0 | Frontend |
| grid-end.js | 52 | 0 | 0 | 0 | Frontend |
| grid-row-align.js | 28 | 0 | 0 | 0 | Frontend |
| grid-row-column.js | 33 | 0 | 0 | 0 | Frontend |
| grid-rows-columns.js | 125 | 0 | 0 | 0 | Frontend |
| grid-start.js | 33 | 0 | 0 | 0 | Frontend |
| grid-template-areas.js | 84 | 0 | 0 | 0 | Frontend |
| grid-template.js | 69 | 0 | 0 | 0 | Frontend |
| grid-utils.js | 1113 | 0 | 0 | 0 | Frontend |
| image-rendering.js | 48 | 0 | 0 | 0 | Frontend |
| image-set.js | 18 | 0 | 0 | 0 | Frontend |
| inline-logical.js | 34 | 0 | 0 | 0 | Frontend |
| intrinsic.js | 61 | 0 | 0 | 0 | Frontend |
| justify-content.js | 54 | 0 | 0 | 0 | Frontend |
| mask-border.js | 38 | 0 | 0 | 0 | Frontend |
| mask-composite.js | 88 | 0 | 0 | 0 | Frontend |
| order.js | 42 | 0 | 0 | 0 | Frontend |
| overscroll-behavior.js | 33 | 0 | 0 | 0 | Frontend |
| pixelated.js | 34 | 0 | 0 | 0 | Frontend |
| place-self.js | 32 | 0 | 0 | 0 | Frontend |
| placeholder-shown.js | 19 | 0 | 0 | 0 | Frontend |
| placeholder.js | 33 | 0 | 0 | 0 | Frontend |
| print-color-adjust.js | 25 | 0 | 0 | 0 | Frontend |
| text-decoration-skip-ink.js | 23 | 0 | 0 | 0 | Frontend |
| text-decoration.js | 25 | 0 | 0 | 0 | Frontend |
| text-emphasis-position.js | 14 | 0 | 0 | 0 | Frontend |
| transform-decl.js | 79 | 0 | 0 | 0 | Frontend |
| user-select.js | 33 | 0 | 0 | 0 | Frontend |
| writing-mode.js | 42 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/baseline-browser-mapping/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cli.js | 2 | 0 | 0 | 0 | Frontend |
| index.cjs | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 90 | 0 | 0 | 0 | Frontend |
| index.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/braces/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| compile.js | 60 | 0 | 0 | 0 | Frontend |
| constants.js | 57 | 0 | 0 | 0 | Frontend |
| expand.js | 113 | 0 | 0 | 0 | Frontend |
| parse.js | 331 | 0 | 0 | 0 | Frontend |
| stringify.js | 32 | 0 | 0 | 0 | Frontend |
| utils.js | 122 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/caniuse-lite/dist/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| statuses.js | 9 | 0 | 0 | 0 | Frontend |
| supported.js | 9 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/caniuse-lite/dist/unpacker`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| agents.js | 47 | 0 | 0 | 0 | Frontend |
| browserVersions.js | 1 | 0 | 0 | 0 | Frontend |
| browsers.js | 1 | 0 | 0 | 0 | Frontend |
| feature.js | 52 | 0 | 0 | 0 | Frontend |
| features.js | 6 | 0 | 0 | 0 | Frontend |
| index.js | 4 | 0 | 0 | 0 | Frontend |
| region.js | 22 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/chokidar/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constants.js | 66 | 0 | 0 | 0 | Frontend |
| fsevents-handler.js | 526 | 0 | 0 | 0 | Frontend |
| nodefs-handler.js | 654 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/chownr/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 93 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/chownr/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 85 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/class-variance-authority/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 36 | 0 | 0 | 0 | Frontend |
| index.js | 74 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| index.mjs | 56 | 0 | 0 | 0 | Other |
| index.mjs.map | 1 | 0 | 0 | 0 | Other |
| types.d.ts | 30 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/clsx/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| clsx.js | 1 | 0 | 0 | 0 | Frontend |
| clsx.min.js | 1 | 0 | 0 | 0 | Frontend |
| clsx.mjs | 1 | 0 | 0 | 0 | Other |
| lite.js | 1 | 0 | 0 | 0 | Frontend |
| lite.mjs | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/cmdk/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| chunk-NZJY6EH4.mjs | 1 | 0 | 0 | 0 | Other |
| chunk-XJATAMEX.mjs | 1 | 0 | 0 | 0 | Other |
| command-score.d.mts | 3 | 0 | 0 | 0 | Other |
| command-score.d.ts | 3 | 0 | 0 | 0 | Frontend |
| command-score.js | 1 | 0 | 0 | 0 | Frontend |
| command-score.mjs | 1 | 0 | 0 | 0 | Other |
| index.d.mts | 412 | 0 | 0 | 0 | Other |
| index.d.ts | 412 | 0 | 0 | 0 | Frontend |
| index.js | 1 | 0 | 0 | 0 | Frontend |
| index.mjs | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/cross-spawn/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| enoent.js | 59 | 0 | 0 | 0 | Frontend |
| parse.js | 91 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/cross-spawn/lib/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| escape.js | 47 | 0 | 0 | 0 | Frontend |
| readShebang.js | 23 | 0 | 0 | 0 | Frontend |
| resolveCommand.js | 52 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-array/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-array.js | 1455 | 0 | 0 | 0 | Frontend |
| d3-array.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-color/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-color.js | 606 | 0 | 0 | 0 | Frontend |
| d3-color.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-ease/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-ease.js | 262 | 0 | 0 | 0 | Frontend |
| d3-ease.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-format/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-format.js | 345 | 0 | 0 | 0 | Frontend |
| d3-format.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-interpolate/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-interpolate.js | 590 | 0 | 0 | 0 | Frontend |
| d3-interpolate.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-path/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-path.js | 169 | 0 | 0 | 0 | Frontend |
| d3-path.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-scale/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-scale.js | 1196 | 0 | 0 | 0 | Frontend |
| d3-scale.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-shape/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-shape.js | 2141 | 0 | 0 | 0 | Frontend |
| d3-shape.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-time-format/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-time-format.js | 745 | 0 | 0 | 0 | Frontend |
| d3-time-format.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-time/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-time.js | 445 | 0 | 0 | 0 | Frontend |
| d3-time.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/d3-timer/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-timer.js | 153 | 0 | 0 | 0 | Frontend |
| d3-timer.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/detect-libc/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| detect-libc.js | 313 | 0 | 0 | 0 | Frontend |
| elf.js | 39 | 0 | 0 | 0 | Frontend |
| filesystem.js | 51 | 0 | 0 | 0 | Frontend |
| process.js | 24 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/dlv/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dlv.es.js | 2 | 0 | 0 | 0 | Frontend |
| dlv.es.js.map | 1 | 0 | 0 | 0 | Other |
| dlv.js | 2 | 0 | 0 | 0 | Frontend |
| dlv.js.map | 1 | 0 | 0 | 0 | Other |
| dlv.umd.js | 2 | 0 | 0 | 0 | Frontend |
| dlv.umd.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/enhanced-resolve/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AliasFieldPlugin.js | 103 | 0 | 0 | 0 | Frontend |
| AliasPlugin.js | 176 | 0 | 0 | 0 | Frontend |
| AppendPlugin.js | 49 | 0 | 0 | 0 | Frontend |
| CachedInputFileSystem.js | 677 | 0 | 0 | 0 | Frontend |
| CloneBasenamePlugin.js | 53 | 0 | 0 | 0 | Frontend |
| ConditionalPlugin.js | 59 | 0 | 0 | 0 | Frontend |
| DescriptionFilePlugin.js | 98 | 0 | 0 | 0 | Scripting |
| DescriptionFileUtils.js | 200 | 0 | 0 | 0 | Scripting |
| DirectoryExistsPlugin.js | 68 | 0 | 0 | 0 | Frontend |
| ExportsFieldPlugin.js | 201 | 0 | 0 | 0 | Frontend |
| ExtensionAliasPlugin.js | 100 | 0 | 0 | 0 | Frontend |
| FileExistsPlugin.js | 61 | 0 | 0 | 0 | Frontend |
| ImportsFieldPlugin.js | 223 | 0 | 0 | 0 | Frontend |
| JoinRequestPartPlugin.js | 75 | 0 | 0 | 0 | Frontend |
| JoinRequestPlugin.js | 45 | 0 | 0 | 0 | Frontend |
| LogInfoPlugin.js | 58 | 0 | 0 | 0 | Frontend |
| MainFieldPlugin.js | 87 | 0 | 0 | 0 | Frontend |
| ModulesInHierachicDirectoriesPlugin.js | 9 | 0 | 0 | 0 | Frontend |
| ModulesInHierarchicalDirectoriesPlugin.js | 91 | 0 | 0 | 0 | Frontend |
| ModulesInRootPlugin.js | 49 | 0 | 0 | 0 | Frontend |
| NextPlugin.js | 33 | 0 | 0 | 0 | Frontend |
| ParsePlugin.js | 77 | 0 | 0 | 0 | Frontend |
| PnpPlugin.js | 134 | 0 | 0 | 0 | Frontend |
| Resolver.js | 799 | 0 | 0 | 0 | Frontend |
| ResolverFactory.js | 731 | 0 | 0 | 0 | Frontend |
| RestrictionsPlugin.js | 70 | 0 | 0 | 0 | Frontend |
| ResultPlugin.js | 43 | 0 | 0 | 0 | Frontend |
| RootsPlugin.js | 69 | 0 | 0 | 0 | Frontend |
| SelfReferencePlugin.js | 82 | 0 | 0 | 0 | Frontend |
| SymlinkPlugin.js | 101 | 0 | 0 | 0 | Frontend |
| SyncAsyncFileSystemDecorator.js | 258 | 0 | 0 | 0 | Frontend |
| TryNextPlugin.js | 41 | 0 | 0 | 0 | Frontend |
| UnsafeCachePlugin.js | 114 | 0 | 0 | 0 | Frontend |
| UseFilePlugin.js | 55 | 0 | 0 | 0 | Frontend |
| createInnerContext.js | 46 | 0 | 0 | 0 | Frontend |
| forEachBail.js | 50 | 0 | 0 | 0 | Frontend |
| getInnerRequest.js | 39 | 0 | 0 | 0 | Frontend |
| getPaths.js | 45 | 0 | 0 | 0 | Frontend |
| index.js | 225 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/enhanced-resolve/lib/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| entrypoints.js | 574 | 0 | 0 | 0 | Frontend |
| identifier.js | 69 | 0 | 0 | 0 | Frontend |
| memoize.js | 37 | 0 | 0 | 0 | Frontend |
| module-browser.js | 8 | 0 | 0 | 0 | Frontend |
| path.js | 203 | 0 | 0 | 0 | Frontend |
| process-browser.js | 25 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/esbuild/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| main.d.ts | 716 | 0 | 0 | 0 | Frontend |
| main.js | 2242 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/escalade/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 22 | 0 | 0 | 0 | Frontend |
| index.mjs | 22 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/fast-equals/dist/cjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.cjs | 638 | 0 | 0 | 0 | Other |
| index.cjs.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/fast-equals/dist/cjs/types`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| comparator.d.ts | 26 | 0 | 0 | 0 | Frontend |
| equals.d.ts | 54 | 0 | 0 | 0 | Frontend |
| index.d.ts | 47 | 0 | 0 | 0 | Frontend |
| internalTypes.d.ts | 157 | 0 | 0 | 0 | Frontend |
| utils.d.ts | 28 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/fast-equals/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 627 | 0 | 0 | 0 | Other |
| index.mjs.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/fast-equals/dist/esm/types`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| comparator.d.ts | 26 | 0 | 0 | 0 | Frontend |
| equals.d.ts | 54 | 0 | 0 | 0 | Frontend |
| index.d.ts | 47 | 0 | 0 | 0 | Frontend |
| internalTypes.d.ts | 157 | 0 | 0 | 0 | Frontend |
| utils.d.ts | 28 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/fast-equals/dist/min`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/fast-equals/dist/min/types`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| comparator.d.ts | 26 | 0 | 0 | 0 | Frontend |
| equals.d.ts | 54 | 0 | 0 | 0 | Frontend |
| index.d.ts | 47 | 0 | 0 | 0 | Frontend |
| internalTypes.d.ts | 157 | 0 | 0 | 0 | Frontend |
| utils.d.ts | 28 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/fast-equals/dist/umd`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 644 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/fast-equals/dist/umd/types`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| comparator.d.ts | 26 | 0 | 0 | 0 | Frontend |
| equals.d.ts | 54 | 0 | 0 | 0 | Frontend |
| index.d.ts | 47 | 0 | 0 | 0 | Frontend |
| internalTypes.d.ts | 157 | 0 | 0 | 0 | Frontend |
| utils.d.ts | 28 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/foreground-child/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| all-signals.d.ts | 2 | 0 | 0 | 0 | Frontend |
| all-signals.d.ts.map | 1 | 0 | 0 | 0 | Other |
| all-signals.js | 58 | 0 | 0 | 0 | Frontend |
| all-signals.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 58 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 123 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| proxy-signals.d.ts | 6 | 0 | 0 | 0 | Frontend |
| proxy-signals.d.ts.map | 1 | 0 | 0 | 0 | Other |
| proxy-signals.js | 38 | 0 | 0 | 0 | Frontend |
| proxy-signals.js.map | 1 | 0 | 0 | 0 | Other |
| watchdog.d.ts | 10 | 0 | 0 | 0 | Frontend |
| watchdog.d.ts.map | 1 | 0 | 0 | 0 | Other |
| watchdog.js | 50 | 0 | 0 | 0 | Frontend |
| watchdog.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/foreground-child/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| all-signals.d.ts | 2 | 0 | 0 | 0 | Frontend |
| all-signals.d.ts.map | 1 | 0 | 0 | 0 | Other |
| all-signals.js | 52 | 0 | 0 | 0 | Frontend |
| all-signals.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 58 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 115 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| proxy-signals.d.ts | 6 | 0 | 0 | 0 | Frontend |
| proxy-signals.d.ts.map | 1 | 0 | 0 | 0 | Other |
| proxy-signals.js | 34 | 0 | 0 | 0 | Frontend |
| proxy-signals.js.map | 1 | 0 | 0 | 0 | Other |
| watchdog.d.ts | 10 | 0 | 0 | 0 | Frontend |
| watchdog.d.ts.map | 1 | 0 | 0 | 0 | Other |
| watchdog.js | 46 | 0 | 0 | 0 | Frontend |
| watchdog.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| client.d.ts | 2554 | 0 | 0 | 0 | Frontend |
| dom-mini.d.ts | 230 | 0 | 0 | 0 | Frontend |
| dom-mini.js | 1 | 0 | 0 | 0 | Frontend |
| dom.d.ts | 579 | 0 | 0 | 0 | Frontend |
| dom.js | 1 | 0 | 0 | 0 | Frontend |
| framer-motion.dev.js | 13255 | 0 | 0 | 0 | Frontend |
| framer-motion.js | 1 | 0 | 0 | 0 | Frontend |
| index.d.ts | 4691 | 0 | 0 | 0 | Frontend |
| m.d.ts | 2554 | 0 | 0 | 0 | Frontend |
| mini.d.ts | 6 | 0 | 0 | 0 | Frontend |
| mini.js | 1 | 0 | 0 | 0 | Frontend |
| three.d.ts | 2828 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/framer-motion/dist/cjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| client.js | 9700 | 0 | 0 | 0 | Frontend |
| dom-mini.js | 644 | 0 | 0 | 0 | Frontend |
| dom.js | 5926 | 0 | 0 | 0 | Frontend |
| index.js | 12631 | 0 | 0 | 0 | Frontend |
| m.js | 1881 | 0 | 0 | 0 | Frontend |
| mini.js | 273 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/framer-motion/dist/es`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| client.mjs | 3 | 0 | 0 | 0 | Other |
| dom-mini.mjs | 2 | 0 | 0 | 0 | Other |
| dom.mjs | 31 | 0 | 0 | 0 | Other |
| index.mjs | 110 | 0 | 0 | 0 | Other |
| m.mjs | 3 | 0 | 0 | 0 | Other |
| mini.mjs | 1 | 0 | 0 | 0 | Other |
| projection.mjs | 11 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/animate`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 34 | 0 | 0 | 0 | Other |
| resolve-subjects.mjs | 19 | 0 | 0 | 0 | Other |
| sequence.mjs | 14 | 0 | 0 | 0 | Other |
| single-value.mjs | 11 | 0 | 0 | 0 | Other |
| subject.mjs | 52 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/animators`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AcceleratedAnimation.mjs | 317 | 0 | 0 | 0 | Other |
| BaseAnimation.mjs | 118 | 0 | 0 | 0 | Other |
| MainThreadAnimation.mjs | 389 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/animators/drivers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| driver-frameloop.mjs | 17 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/animators/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| accelerated-values.mjs | 14 | 0 | 0 | 0 | Other |
| can-animate.mjs | 42 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/animators/waapi`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| NativeAnimation.mjs | 112 | 0 | 0 | 0 | Other |
| animate-elements.mjs | 34 | 0 | 0 | 0 | Other |
| animate-sequence.mjs | 13 | 0 | 0 | 0 | Other |
| animate-style.mjs | 12 | 0 | 0 | 0 | Other |
| index.mjs | 23 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/animators/waapi/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| get-final-keyframe.mjs | 12 | 0 | 0 | 0 | Other |
| style.mjs | 8 | 0 | 0 | 0 | Other |
| supports-partial-keyframes.mjs | 13 | 0 | 0 | 0 | Other |
| supports-waapi.mjs | 5 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/generators`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| inertia.mjs | 87 | 0 | 0 | 0 | Other |
| keyframes.mjs | 51 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/generators/spring`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| defaults.mjs | 27 | 0 | 0 | 0 | Other |
| find.mjs | 85 | 0 | 0 | 0 | Other |
| index.mjs | 166 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/generators/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| velocity.mjs | 9 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/hooks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| animation-controls.mjs | 80 | 0 | 0 | 0 | Other |
| use-animate-style.mjs | 17 | 0 | 0 | 0 | Other |
| use-animate.mjs | 17 | 0 | 0 | 0 | Other |
| use-animated-state.mjs | 64 | 0 | 0 | 0 | Other |
| use-animation.mjs | 41 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/interfaces`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| motion-value.mjs | 112 | 0 | 0 | 0 | Other |
| visual-element-target.mjs | 75 | 0 | 0 | 0 | Other |
| visual-element-variant.mjs | 66 | 0 | 0 | 0 | Other |
| visual-element.mjs | 26 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/optimized-appear`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| data-id.mjs | 6 | 0 | 0 | 0 | Data |
| get-appear-id.mjs | 7 | 0 | 0 | 0 | Other |
| handoff.mjs | 40 | 0 | 0 | 0 | Other |
| start.mjs | 173 | 0 | 0 | 0 | Other |
| store-id.mjs | 8 | 0 | 0 | 0 | Other |
| store.mjs | 4 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/sequence`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create.mjs | 253 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/sequence/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| calc-repeat-duration.mjs | 5 | 0 | 0 | 0 | Other |
| calc-time.mjs | 21 | 0 | 0 | 0 | Other |
| edit.mjs | 31 | 0 | 0 | 0 | Other |
| normalize-times.mjs | 13 | 0 | 0 | 0 | Other |
| sort.mjs | 14 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/animation/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create-visual-element.mjs | 44 | 0 | 0 | 0 | Other |
| default-transitions.mjs | 40 | 0 | 0 | 0 | Other |
| is-animatable.mjs | 30 | 0 | 0 | 0 | Other |
| is-animation-controls.mjs | 7 | 0 | 0 | 0 | Other |
| is-dom-keyframes.mjs | 5 | 0 | 0 | 0 | Other |
| is-keyframes-target.mjs | 5 | 0 | 0 | 0 | Other |
| is-none.mjs | 15 | 0 | 0 | 0 | Other |
| is-transition-defined.mjs | 10 | 0 | 0 | 0 | Other |
| stagger.mjs | 26 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/components`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AnimateSharedLayout.mjs | 15 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/components/AnimatePresence`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| PopChild.mjs | 77 | 0 | 0 | 0 | Other |
| PresenceChild.mjs | 61 | 0 | 0 | 0 | Other |
| index.mjs | 166 | 0 | 0 | 0 | Other |
| use-presence.mjs | 69 | 0 | 0 | 0 | Other |
| utils.mjs | 14 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/components/LayoutGroup`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 32 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/components/LazyMotion`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 68 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/components/MotionConfig`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 48 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/framer-motion/dist/es/components/Reorder`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Group.mjs | 53 | 0 | 0 | 0 | Other |
| Item.mjs | 34 | 0 | 0 | 0 | Other |
| namespace.mjs | 2 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/components/Reorder/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| check-reorder.mjs | 24 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/context`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| DeprecatedLayoutGroupContext.mjs | 10 | 0 | 0 | 0 | Other |
| LayoutGroupContext.mjs | 6 | 0 | 0 | 0 | Other |
| LazyContext.mjs | 6 | 0 | 0 | 0 | Other |
| MotionConfigContext.mjs | 13 | 0 | 0 | 0 | Configuration |
| PresenceContext.mjs | 9 | 0 | 0 | 0 | Other |
| ReorderContext.mjs | 6 | 0 | 0 | 0 | Other |
| SwitchLayoutGroupContext.mjs | 9 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/context/MotionContext`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create.mjs | 13 | 0 | 0 | 0 | Other |
| index.mjs | 6 | 0 | 0 | 0 | Other |
| utils.mjs | 17 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/easing`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| anticipate.mjs | 5 | 0 | 0 | 0 | Other |
| back.mjs | 9 | 0 | 0 | 0 | Other |
| circ.mjs | 8 | 0 | 0 | 0 | Other |
| cubic-bezier.mjs | 51 | 0 | 0 | 0 | Other |
| ease.mjs | 7 | 0 | 0 | 0 | Other |
| steps.mjs | 15 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/easing/modifiers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mirror.mjs | 5 | 0 | 0 | 0 | Other |
| reverse.mjs | 5 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/easing/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| get-easing-for-segment.mjs | 8 | 0 | 0 | 0 | Other |
| is-easing-array.mjs | 5 | 0 | 0 | 0 | Other |
| map.mjs | 37 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/events`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| add-dom-event.mjs | 6 | 0 | 0 | 0 | Other |
| add-pointer-event.mjs | 8 | 0 | 0 | 0 | Other |
| event-info.mjs | 15 | 0 | 0 | 0 | Other |
| use-dom-event.mjs | 34 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/frameloop`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| batcher.mjs | 74 | 0 | 0 | 0 | Other |
| frame.mjs | 6 | 0 | 0 | 0 | Other |
| index-legacy.mjs | 20 | 0 | 0 | 0 | Other |
| microtask.mjs | 5 | 0 | 0 | 0 | Other |
| render-step.mjs | 81 | 0 | 0 | 0 | Other |
| sync-time.mjs | 31 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/gestures`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| focus.mjs | 41 | 0 | 0 | 0 | Other |
| hover.mjs | 30 | 0 | 0 | 0 | Other |
| press.mjs | 30 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/gestures/drag`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| VisualElementDragControls.mjs | 484 | 0 | 0 | 0 | Other |
| index.mjs | 27 | 0 | 0 | 0 | Other |
| use-drag-controls.mjs | 88 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/gestures/drag/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constraints.mjs | 129 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/gestures/pan`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| PanSession.mjs | 156 | 0 | 0 | 0 | Other |
| index.mjs | 50 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/motion`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 102 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/motion/features`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Feature.mjs | 9 | 0 | 0 | 0 | Other |
| animations.mjs | 13 | 0 | 0 | 0 | Other |
| definitions.mjs | 28 | 0 | 0 | 0 | Other |
| drag.mjs | 17 | 0 | 0 | 0 | Other |
| gestures.mjs | 21 | 0 | 0 | 0 | Other |
| layout.mjs | 11 | 0 | 0 | 0 | Other |
| load-features.mjs | 12 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/motion/features/animation`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| exit.mjs | 31 | 0 | 0 | 0 | Other |
| index.mjs | 41 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/motion/features/layout`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| MeasureLayout.mjs | 134 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/motion/features/viewport`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 72 | 0 | 0 | 0 | Other |
| observers.mjs | 49 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/motion/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| is-forced-motion-value.mjs | 11 | 0 | 0 | 0 | Other |
| is-motion-component.mjs | 12 | 0 | 0 | 0 | Other |
| symbol.mjs | 3 | 0 | 0 | 0 | Other |
| unwrap-motion-component.mjs | 17 | 0 | 0 | 0 | Other |
| use-motion-ref.mjs | 38 | 0 | 0 | 0 | Other |
| use-visual-element.mjs | 134 | 0 | 0 | 0 | Other |
| use-visual-state.mjs | 88 | 0 | 0 | 0 | Other |
| valid-prop.mjs | 57 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/projection`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| use-instant-layout-transition.mjs | 14 | 0 | 0 | 0 | Other |
| use-reset-projection.mjs | 14 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/projection/animation`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mix-values.mjs | 92 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/projection/geometry`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conversion.mjs | 33 | 0 | 0 | 0 | Other |
| copy.mjs | 31 | 0 | 0 | 0 | Other |
| delta-apply.mjs | 119 | 0 | 0 | 0 | Other |
| delta-calc.mjs | 52 | 0 | 0 | 0 | Other |
| delta-remove.mjs | 54 | 0 | 0 | 0 | Other |
| models.mjs | 17 | 0 | 0 | 0 | Other |
| utils.mjs | 31 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/projection/node`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| DocumentProjectionNode.mjs | 13 | 0 | 0 | 0 | Other |
| HTMLProjectionNode.mjs | 27 | 0 | 0 | 0 | Other |
| create-projection-node.mjs | 1583 | 0 | 0 | 0 | Other |
| group.mjs | 24 | 0 | 0 | 0 | Other |
| state.mjs | 19 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/projection/shared`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| stack.mjs | 112 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/projection/styles`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| scale-border-radius.mjs | 41 | 0 | 0 | 0 | Other |
| scale-box-shadow.mjs | 35 | 0 | 0 | 0 | Other |
| scale-correction.mjs | 6 | 0 | 0 | 0 | Other |
| transform.mjs | 49 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/projection/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| each-axis.mjs | 5 | 0 | 0 | 0 | Other |
| has-transform.mjs | 26 | 0 | 0 | 0 | Other |
| measure.mjs | 17 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| VisualElement.mjs | 479 | 0 | 0 | 0 | Other |
| store.mjs | 3 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/components`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create-factory.mjs | 23 | 0 | 0 | 0 | Other |
| create-proxy.mjs | 38 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/components/m`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create.mjs | 6 | 0 | 0 | 0 | Other |
| elements.mjs | 227 | 0 | 0 | 0 | Other |
| proxy.mjs | 6 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/components/motion`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create.mjs | 15 | 0 | 0 | 0 | Other |
| elements.mjs | 194 | 0 | 0 | 0 | Other |
| proxy.mjs | 6 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/dom`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| DOMKeyframesResolver.mjs | 131 | 0 | 0 | 0 | Other |
| DOMVisualElement.mjs | 43 | 0 | 0 | 0 | Other |
| create-visual-element.mjs | 14 | 0 | 0 | 0 | Other |
| features-animation.mjs | 14 | 0 | 0 | 0 | Other |
| features-max.mjs | 14 | 0 | 0 | 0 | Other |
| features-min.mjs | 12 | 0 | 0 | 0 | Other |
| use-render.mjs | 33 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/dom/resize`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| handle-element.mjs | 64 | 0 | 0 | 0 | Other |
| handle-window.mjs | 30 | 0 | 0 | 0 | Other |
| index.mjs | 8 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/dom/scroll`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 87 | 0 | 0 | 0 | Other |
| info.mjs | 56 | 0 | 0 | 0 | Other |
| observe.mjs | 18 | 0 | 0 | 0 | Other |
| on-scroll-handler.mjs | 48 | 0 | 0 | 0 | Other |
| track.mjs | 84 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/dom/scroll/offsets`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| edge.mjs | 45 | 0 | 0 | 0 | Other |
| index.mjs | 60 | 0 | 0 | 0 | Other |
| inset.mjs | 45 | 0 | 0 | 0 | Other |
| offset.mjs | 35 | 0 | 0 | 0 | Other |
| presets.mjs | 20 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/dom/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| camel-to-dash.mjs | 6 | 0 | 0 | 0 | Other |
| css-variables-conversion.mjs | 42 | 0 | 0 | 0 | Other |
| filter-props.mjs | 59 | 0 | 0 | 0 | Other |
| is-css-variable.mjs | 15 | 0 | 0 | 0 | Other |
| is-svg-component.mjs | 30 | 0 | 0 | 0 | Other |
| is-svg-element.mjs | 5 | 0 | 0 | 0 | Other |
| unit-conversion.mjs | 53 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/dom/value-types`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| animatable-none.mjs | 15 | 0 | 0 | 0 | Other |
| defaults.mjs | 30 | 0 | 0 | 0 | Other |
| dimensions.mjs | 15 | 0 | 0 | 0 | Other |
| find.mjs | 15 | 0 | 0 | 0 | Other |
| get-as-type.mjs | 10 | 0 | 0 | 0 | Other |
| number-browser.mjs | 41 | 0 | 0 | 0 | Other |
| number.mjs | 18 | 0 | 0 | 0 | Other |
| test.mjs | 6 | 0 | 0 | 0 | Testing |
| transform.mjs | 31 | 0 | 0 | 0 | Other |
| type-auto.mjs | 9 | 0 | 0 | 0 | Other |
| type-int.mjs | 8 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/dom/viewport`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 43 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/html`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| HTMLVisualElement.mjs | 43 | 0 | 0 | 0 | Other |
| config-motion.mjs | 12 | 0 | 0 | 0 | Configuration |
| use-props.mjs | 57 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/html/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| build-styles.mjs | 65 | 0 | 0 | 0 | Other |
| build-transform.mjs | 62 | 0 | 0 | 0 | Other |
| create-render-state.mjs | 8 | 0 | 0 | 0 | Other |
| keys-position.mjs | 13 | 0 | 0 | 0 | Other |
| keys-transform.mjs | 28 | 0 | 0 | 0 | Other |
| make-none-animatable.mjs | 30 | 0 | 0 | 0 | Other |
| render.mjs | 9 | 0 | 0 | 0 | Other |
| scrape-motion-values.mjs | 20 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/object`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ObjectVisualElement.mjs | 41 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/svg`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| SVGVisualElement.mjs | 45 | 0 | 0 | 0 | Other |
| config-motion.mjs | 73 | 0 | 0 | 0 | Configuration |
| lowercase-elements.mjs | 33 | 0 | 0 | 0 | Other |
| use-props.mjs | 24 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/svg/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| build-attrs.mjs | 52 | 0 | 0 | 0 | Other |
| camel-case-attrs.mjs | 30 | 0 | 0 | 0 | Other |
| create-render-state.mjs | 8 | 0 | 0 | 0 | Other |
| is-svg-tag.mjs | 3 | 0 | 0 | 0 | Other |
| path.mjs | 32 | 0 | 0 | 0 | Other |
| render.mjs | 12 | 0 | 0 | 0 | Other |
| scrape-motion-values.mjs | 19 | 0 | 0 | 0 | Other |
| transform-origin.mjs | 18 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/render/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| KeyframesResolver.mjs | 164 | 0 | 0 | 0 | Other |
| animation-state.mjs | 332 | 0 | 0 | 0 | Other |
| compare-by-depth.mjs | 3 | 0 | 0 | 0 | Other |
| flat-tree.mjs | 24 | 0 | 0 | 0 | Other |
| get-variant-context.mjs | 28 | 0 | 0 | 0 | Other |
| is-controlling-variants.mjs | 13 | 0 | 0 | 0 | Other |
| is-variant-label.mjs | 8 | 0 | 0 | 0 | Other |
| motion-values.mjs | 59 | 0 | 0 | 0 | Other |
| resolve-dynamic-variants.mjs | 8 | 0 | 0 | 0 | Other |
| resolve-variants.mjs | 36 | 0 | 0 | 0 | Other |
| setters.mjs | 27 | 0 | 0 | 0 | Other |
| variant-props.mjs | 12 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| GlobalConfig.mjs | 6 | 0 | 0 | 0 | Configuration |
| array.mjs | 21 | 0 | 0 | 0 | Other |
| clamp.mjs | 9 | 0 | 0 | 0 | Other |
| delay.mjs | 24 | 0 | 0 | 0 | Other |
| distance.mjs | 9 | 0 | 0 | 0 | Other |
| get-context-window.mjs | 6 | 0 | 0 | 0 | Other |
| hsla-to-rgba.mjs | 42 | 0 | 0 | 0 | Other |
| interpolate.mjs | 76 | 0 | 0 | 0 | Other |
| is-browser.mjs | 3 | 0 | 0 | 0 | Other |
| is-numerical-string.mjs | 6 | 0 | 0 | 0 | Other |
| is-ref-object.mjs | 7 | 0 | 0 | 0 | Other |
| is-zero-value-string.mjs | 6 | 0 | 0 | 0 | Other |
| pipe.mjs | 11 | 0 | 0 | 0 | Other |
| resolve-value.mjs | 11 | 0 | 0 | 0 | Other |
| shallow-compare.mjs | 14 | 0 | 0 | 0 | Other |
| subscription-manager.mjs | 40 | 0 | 0 | 0 | Scripting |
| transform.mjs | 21 | 0 | 0 | 0 | Other |
| use-animation-frame.mjs | 21 | 0 | 0 | 0 | Other |
| use-constant.mjs | 18 | 0 | 0 | 0 | Other |
| use-cycle.mjs | 47 | 0 | 0 | 0 | Other |
| use-force-update.mjs | 19 | 0 | 0 | 0 | Other |
| use-in-view.mjs | 23 | 0 | 0 | 0 | Other |
| use-instant-transition-state.mjs | 5 | 0 | 0 | 0 | Other |
| use-instant-transition.mjs | 41 | 0 | 0 | 0 | Other |
| use-is-mounted.mjs | 15 | 0 | 0 | 0 | Other |
| use-isomorphic-effect.mjs | 6 | 0 | 0 | 0 | Other |
| use-motion-value-event.mjs | 13 | 0 | 0 | 0 | Other |
| use-unmount-effect.mjs | 7 | 0 | 0 | 0 | Other |
| velocity-per-second.mjs | 11 | 0 | 0 | 0 | Other |
| warn-once.mjs | 11 | 0 | 0 | 0 | Other |
| wrap.mjs | 6 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/utils/mix`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| color.mjs | 47 | 0 | 0 | 0 | Other |
| complex.mjs | 94 | 0 | 0 | 0 | Other |
| immediate.mjs | 5 | 0 | 0 | 0 | Other |
| index.mjs | 14 | 0 | 0 | 0 | Other |
| number.mjs | 26 | 0 | 0 | 0 | Other |
| visibility.mjs | 16 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/utils/offsets`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| default.mjs | 9 | 0 | 0 | 0 | Other |
| fill.mjs | 12 | 0 | 0 | 0 | Other |
| time.mjs | 5 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/utils/reduced-motion`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 19 | 0 | 0 | 0 | Other |
| state.mjs | 5 | 0 | 0 | 0 | Other |
| use-reduced-motion-config.mjs | 19 | 0 | 0 | 0 | Configuration |
| use-reduced-motion.mjs | 47 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/value`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 319 | 0 | 0 | 0 | Other |
| use-combine-values.mjs | 37 | 0 | 0 | 0 | Other |
| use-computed.mjs | 19 | 0 | 0 | 0 | Other |
| use-inverted-scale.mjs | 52 | 0 | 0 | 0 | Other |
| use-motion-template.mjs | 45 | 0 | 0 | 0 | Other |
| use-motion-value.mjs | 38 | 0 | 0 | 0 | Other |
| use-scroll.mjs | 39 | 0 | 0 | 0 | Other |
| use-spring.mjs | 85 | 0 | 0 | 0 | Other |
| use-time.mjs | 10 | 0 | 0 | 0 | Other |
| use-transform.mjs | 29 | 0 | 0 | 0 | Other |
| use-velocity.mjs | 35 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/value/scroll`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| use-element-scroll.mjs | 14 | 0 | 0 | 0 | Other |
| use-viewport-scroll.mjs | 14 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/value/types/color`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| hex.mjs | 40 | 0 | 0 | 0 | Other |
| hsla.mjs | 22 | 0 | 0 | 0 | Other |
| index.mjs | 27 | 0 | 0 | 0 | Other |
| rgba.mjs | 25 | 0 | 0 | 0 | Other |
| utils.mjs | 29 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/value/types/complex`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| filter.mjs | 30 | 0 | 0 | 0 | Other |
| index.mjs | 92 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/value/types/numbers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 17 | 0 | 0 | 0 | Other |
| units.mjs | 17 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/value/types/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| color-regex.mjs | 3 | 0 | 0 | 0 | Other |
| float-regex.mjs | 3 | 0 | 0 | 0 | Other |
| is-nullish.mjs | 5 | 0 | 0 | 0 | Other |
| sanitize.mjs | 5 | 0 | 0 | 0 | Other |
| single-color-regex.mjs | 3 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/value/use-will-change`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| WillChangeMotionValue.mjs | 22 | 0 | 0 | 0 | Other |
| add-will-change.mjs | 14 | 0 | 0 | 0 | Other |
| get-will-change-name.mjs | 14 | 0 | 0 | 0 | Other |
| index.mjs | 8 | 0 | 0 | 0 | Other |
| is.mjs | 7 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/framer-motion/dist/es/value/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| is-motion-value.mjs | 3 | 0 | 0 | 0 | Other |
| resolve-motion-value.mjs | 16 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/get-nonce/dist/es2015`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 2 | 0 | 0 | 0 | Frontend |
| index.js | 13 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/get-nonce/dist/es5`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 2 | 0 | 0 | 0 | Frontend |
| index.js | 15 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/glob/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| glob.d.ts | 388 | 0 | 0 | 0 | Frontend |
| glob.d.ts.map | 1 | 0 | 0 | 0 | Other |
| glob.js | 247 | 0 | 0 | 0 | Frontend |
| glob.js.map | 1 | 0 | 0 | 0 | Other |
| has-magic.d.ts | 14 | 0 | 0 | 0 | Frontend |
| has-magic.d.ts.map | 1 | 0 | 0 | 0 | Other |
| has-magic.js | 27 | 0 | 0 | 0 | Frontend |
| has-magic.js.map | 1 | 0 | 0 | 0 | Other |
| ignore.d.ts | 24 | 0 | 0 | 0 | Frontend |
| ignore.d.ts.map | 1 | 0 | 0 | 0 | Other |
| ignore.js | 119 | 0 | 0 | 0 | Frontend |
| ignore.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 97 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 68 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| pattern.d.ts | 76 | 0 | 0 | 0 | Frontend |
| pattern.d.ts.map | 1 | 0 | 0 | 0 | Other |
| pattern.js | 219 | 0 | 0 | 0 | Frontend |
| pattern.js.map | 1 | 0 | 0 | 0 | Other |
| processor.d.ts | 59 | 0 | 0 | 0 | Frontend |
| processor.d.ts.map | 1 | 0 | 0 | 0 | Other |
| processor.js | 301 | 0 | 0 | 0 | Frontend |
| processor.js.map | 1 | 0 | 0 | 0 | Other |
| walker.d.ts | 97 | 0 | 0 | 0 | Frontend |
| walker.d.ts.map | 1 | 0 | 0 | 0 | Other |
| walker.js | 387 | 0 | 0 | 0 | Frontend |
| walker.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/glob/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| bin.d.mts | 3 | 0 | 0 | 0 | Other |
| bin.d.mts.map | 1 | 0 | 0 | 0 | Other |
| bin.mjs | 270 | 0 | 0 | 0 | Other |
| bin.mjs.map | 1 | 0 | 0 | 0 | Other |
| glob.d.ts | 388 | 0 | 0 | 0 | Frontend |
| glob.d.ts.map | 1 | 0 | 0 | 0 | Other |
| glob.js | 243 | 0 | 0 | 0 | Frontend |
| glob.js.map | 1 | 0 | 0 | 0 | Other |
| has-magic.d.ts | 14 | 0 | 0 | 0 | Frontend |
| has-magic.d.ts.map | 1 | 0 | 0 | 0 | Other |
| has-magic.js | 23 | 0 | 0 | 0 | Frontend |
| has-magic.js.map | 1 | 0 | 0 | 0 | Other |
| ignore.d.ts | 24 | 0 | 0 | 0 | Frontend |
| ignore.d.ts.map | 1 | 0 | 0 | 0 | Other |
| ignore.js | 115 | 0 | 0 | 0 | Frontend |
| ignore.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 97 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 55 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| pattern.d.ts | 76 | 0 | 0 | 0 | Frontend |
| pattern.d.ts.map | 1 | 0 | 0 | 0 | Other |
| pattern.js | 215 | 0 | 0 | 0 | Frontend |
| pattern.js.map | 1 | 0 | 0 | 0 | Other |
| processor.d.ts | 59 | 0 | 0 | 0 | Frontend |
| processor.d.ts.map | 1 | 0 | 0 | 0 | Other |
| processor.js | 294 | 0 | 0 | 0 | Frontend |
| processor.js.map | 1 | 0 | 0 | 0 | Other |
| walker.d.ts | 97 | 0 | 0 | 0 | Frontend |
| walker.d.ts.map | 1 | 0 | 0 | 0 | Other |
| walker.js | 381 | 0 | 0 | 0 | Frontend |
| walker.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/input-otp/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 42 | 0 | 0 | 0 | Other |
| index.d.ts | 42 | 0 | 0 | 0 | Frontend |
| index.js | 21 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| index.mjs | 21 | 0 | 0 | 0 | Other |
| index.mjs.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/internmap/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| internmap.js | 75 | 0 | 0 | 0 | Frontend |
| internmap.min.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/jackspeak/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 315 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1010 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| parse-args-cjs.cjs.map | 1 | 0 | 0 | 0 | Other |
| parse-args-cjs.d.cts.map | 1 | 0 | 0 | 0 | Other |
| parse-args.d.ts | 4 | 0 | 0 | 0 | Frontend |
| parse-args.js | 50 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/jackspeak/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 315 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1000 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| parse-args.d.ts | 4 | 0 | 0 | 0 | Frontend |
| parse-args.d.ts.map | 1 | 0 | 0 | 0 | Other |
| parse-args.js | 26 | 0 | 0 | 0 | Frontend |
| parse-args.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/jiti/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| babel.cjs | 426 | 0 | 0 | 0 | Other |
| jiti.cjs | 6 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/jiti/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| jiti-cli.mjs | 34 | 0 | 0 | 0 | Other |
| jiti-hooks.mjs | 124 | 0 | 0 | 0 | Other |
| jiti-native.mjs | 121 | 0 | 0 | 0 | Other |
| jiti-register.d.mts | 1 | 0 | 0 | 0 | Other |
| jiti-register.mjs | 4 | 0 | 0 | 0 | Other |
| jiti.cjs | 30 | 0 | 0 | 0 | Other |
| jiti.d.cts | 8 | 0 | 0 | 0 | Other |
| jiti.d.mts | 8 | 0 | 0 | 0 | Other |
| jiti.mjs | 29 | 0 | 0 | 0 | Other |
| types.d.ts | 363 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/json5/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 1737 | 0 | 0 | 0 | Frontend |
| index.min.js | 1 | 0 | 0 | 0 | Frontend |
| index.min.mjs | 1 | 0 | 0 | 0 | Other |
| index.mjs | 1426 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/json5/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cli.js | 152 | 0 | 0 | 0 | Frontend |
| index.d.ts | 4 | 0 | 0 | 0 | Frontend |
| index.js | 9 | 0 | 0 | 0 | Frontend |
| parse.d.ts | 15 | 0 | 0 | 0 | Frontend |
| parse.js | 1114 | 0 | 0 | 0 | Frontend |
| register.js | 13 | 0 | 0 | 0 | Frontend |
| require.js | 4 | 0 | 0 | 0 | Frontend |
| stringify.d.ts | 89 | 0 | 0 | 0 | Frontend |
| stringify.js | 261 | 0 | 0 | 0 | Frontend |
| unicode.d.ts | 3 | 0 | 0 | 0 | Frontend |
| unicode.js | 4 | 0 | 0 | 0 | Frontend |
| util.d.ts | 5 | 0 | 0 | 0 | Frontend |
| util.js | 35 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/lines-and-columns/build`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 13 | 0 | 0 | 0 | Frontend |
| index.js | 62 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/lucide-react/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| lucide-react.d.ts | 21661 | 0 | 0 | 0 | Frontend |
| lucide-react.prefixed.d.ts | 21661 | 0 | 0 | 0 | Frontend |
| lucide-react.suffixed.d.ts | 21661 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/lucide-react/dist/cjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| lucide-react.js | 21138 | 0 | 0 | 0 | Frontend |
| lucide-react.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/lucide-react/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Icon.js | 44 | 0 | 0 | 0 | Frontend |
| Icon.js.map | 1 | 0 | 0 | 0 | Other |
| createLucideIcon.js | 26 | 0 | 0 | 0 | Frontend |
| createLucideIcon.js.map | 1 | 0 | 0 | 0 | Other |
| defaultAttributes.js | 21 | 0 | 0 | 0 | Frontend |
| defaultAttributes.js.map | 1 | 0 | 0 | 0 | Other |
| lucide-react.js | 1556 | 0 | 0 | 0 | Frontend |
| lucide-react.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/lucide-react/dist/esm/icons`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| a-arrow-down.js | 18 | 0 | 0 | 0 | Frontend |
| a-arrow-down.js.map | 1 | 0 | 0 | 0 | Other |
| a-arrow-up.js | 18 | 0 | 0 | 0 | Frontend |
| a-arrow-up.js.map | 1 | 0 | 0 | 0 | Other |
| a-large-small.js | 18 | 0 | 0 | 0 | Frontend |
| a-large-small.js.map | 1 | 0 | 0 | 0 | Other |
| accessibility.js | 19 | 0 | 0 | 0 | Frontend |
| accessibility.js.map | 1 | 0 | 0 | 0 | Other |
| activity-square.js | 9 | 0 | 0 | 0 | Frontend |
| activity-square.js.map | 1 | 0 | 0 | 0 | Other |
| activity.js | 21 | 0 | 0 | 0 | Frontend |
| activity.js.map | 1 | 0 | 0 | 0 | Other |
| air-vent.js | 24 | 0 | 0 | 0 | Frontend |
| air-vent.js.map | 1 | 0 | 0 | 0 | Other |
| airplay.js | 22 | 0 | 0 | 0 | Frontend |
| airplay.js.map | 1 | 0 | 0 | 0 | Other |
| alarm-check.js | 9 | 0 | 0 | 0 | Frontend |
| alarm-check.js.map | 1 | 0 | 0 | 0 | Other |
| alarm-clock-check.js | 20 | 0 | 0 | 0 | Frontend |
| alarm-clock-check.js.map | 1 | 0 | 0 | 0 | Other |
| alarm-clock-minus.js | 20 | 0 | 0 | 0 | Frontend |
| alarm-clock-minus.js.map | 1 | 0 | 0 | 0 | Other |
| alarm-clock-off.js | 20 | 0 | 0 | 0 | Frontend |
| alarm-clock-off.js.map | 1 | 0 | 0 | 0 | Other |
| alarm-clock-plus.js | 21 | 0 | 0 | 0 | Frontend |
| alarm-clock-plus.js.map | 1 | 0 | 0 | 0 | Other |
| alarm-clock.js | 20 | 0 | 0 | 0 | Frontend |
| alarm-clock.js.map | 1 | 0 | 0 | 0 | Other |
| alarm-minus.js | 9 | 0 | 0 | 0 | Frontend |
| alarm-minus.js.map | 1 | 0 | 0 | 0 | Other |
| alarm-plus.js | 9 | 0 | 0 | 0 | Frontend |
| alarm-plus.js.map | 1 | 0 | 0 | 0 | Other |
| alarm-smoke.js | 22 | 0 | 0 | 0 | Frontend |
| alarm-smoke.js.map | 1 | 0 | 0 | 0 | Other |
| album.js | 16 | 0 | 0 | 0 | Frontend |
| album.js.map | 1 | 0 | 0 | 0 | Other |
| alert-circle.js | 9 | 0 | 0 | 0 | Frontend |
| alert-circle.js.map | 1 | 0 | 0 | 0 | Other |
| alert-octagon.js | 9 | 0 | 0 | 0 | Frontend |
| alert-octagon.js.map | 1 | 0 | 0 | 0 | Other |
| alert-triangle.js | 9 | 0 | 0 | 0 | Frontend |
| alert-triangle.js.map | 1 | 0 | 0 | 0 | Other |
| align-center-horizontal.js | 19 | 0 | 0 | 0 | Frontend |
| align-center-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| align-center-vertical.js | 19 | 0 | 0 | 0 | Frontend |
| align-center-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| align-center.js | 17 | 0 | 0 | 0 | Frontend |
| align-center.js.map | 1 | 0 | 0 | 0 | Other |
| align-end-horizontal.js | 17 | 0 | 0 | 0 | Frontend |
| align-end-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| align-end-vertical.js | 17 | 0 | 0 | 0 | Frontend |
| align-end-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| align-horizontal-distribute-center.js | 20 | 0 | 0 | 0 | Frontend |
| align-horizontal-distribute-center.js.map | 1 | 0 | 0 | 0 | Other |
| align-horizontal-distribute-end.js | 18 | 0 | 0 | 0 | Frontend |
| align-horizontal-distribute-end.js.map | 1 | 0 | 0 | 0 | Other |
| align-horizontal-distribute-start.js | 18 | 0 | 0 | 0 | Frontend |
| align-horizontal-distribute-start.js.map | 1 | 0 | 0 | 0 | Other |
| align-horizontal-justify-center.js | 17 | 0 | 0 | 0 | Frontend |
| align-horizontal-justify-center.js.map | 1 | 0 | 0 | 0 | Other |
| align-horizontal-justify-end.js | 17 | 0 | 0 | 0 | Frontend |
| align-horizontal-justify-end.js.map | 1 | 0 | 0 | 0 | Other |
| align-horizontal-justify-start.js | 17 | 0 | 0 | 0 | Frontend |
| align-horizontal-justify-start.js.map | 1 | 0 | 0 | 0 | Other |
| align-horizontal-space-around.js | 17 | 0 | 0 | 0 | Frontend |
| align-horizontal-space-around.js.map | 1 | 0 | 0 | 0 | Other |
| align-horizontal-space-between.js | 18 | 0 | 0 | 0 | Frontend |
| align-horizontal-space-between.js.map | 1 | 0 | 0 | 0 | Other |
| align-justify.js | 17 | 0 | 0 | 0 | Frontend |
| align-justify.js.map | 1 | 0 | 0 | 0 | Other |
| align-left.js | 17 | 0 | 0 | 0 | Frontend |
| align-left.js.map | 1 | 0 | 0 | 0 | Other |
| align-right.js | 17 | 0 | 0 | 0 | Frontend |
| align-right.js.map | 1 | 0 | 0 | 0 | Other |
| align-start-horizontal.js | 17 | 0 | 0 | 0 | Frontend |
| align-start-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| align-start-vertical.js | 17 | 0 | 0 | 0 | Frontend |
| align-start-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| align-vertical-distribute-center.js | 20 | 0 | 0 | 0 | Frontend |
| align-vertical-distribute-center.js.map | 1 | 0 | 0 | 0 | Other |
| align-vertical-distribute-end.js | 18 | 0 | 0 | 0 | Frontend |
| align-vertical-distribute-end.js.map | 1 | 0 | 0 | 0 | Other |
| align-vertical-distribute-start.js | 18 | 0 | 0 | 0 | Frontend |
| align-vertical-distribute-start.js.map | 1 | 0 | 0 | 0 | Other |
| align-vertical-justify-center.js | 17 | 0 | 0 | 0 | Frontend |
| align-vertical-justify-center.js.map | 1 | 0 | 0 | 0 | Other |
| align-vertical-justify-end.js | 17 | 0 | 0 | 0 | Frontend |
| align-vertical-justify-end.js.map | 1 | 0 | 0 | 0 | Other |
| align-vertical-justify-start.js | 17 | 0 | 0 | 0 | Frontend |
| align-vertical-justify-start.js.map | 1 | 0 | 0 | 0 | Other |
| align-vertical-space-around.js | 17 | 0 | 0 | 0 | Frontend |
| align-vertical-space-around.js.map | 1 | 0 | 0 | 0 | Other |
| align-vertical-space-between.js | 18 | 0 | 0 | 0 | Frontend |
| align-vertical-space-between.js.map | 1 | 0 | 0 | 0 | Other |
| ambulance.js | 27 | 0 | 0 | 0 | Frontend |
| ambulance.js.map | 1 | 0 | 0 | 0 | Other |
| ampersand.js | 22 | 0 | 0 | 0 | Frontend |
| ampersand.js.map | 1 | 0 | 0 | 0 | Other |
| ampersands.js | 28 | 0 | 0 | 0 | Frontend |
| ampersands.js.map | 1 | 0 | 0 | 0 | Other |
| amphora.js | 23 | 0 | 0 | 0 | Frontend |
| amphora.js.map | 1 | 0 | 0 | 0 | Other |
| anchor.js | 17 | 0 | 0 | 0 | Frontend |
| anchor.js.map | 1 | 0 | 0 | 0 | Other |
| angry.js | 20 | 0 | 0 | 0 | Frontend |
| angry.js.map | 1 | 0 | 0 | 0 | Other |
| annoyed.js | 18 | 0 | 0 | 0 | Frontend |
| annoyed.js.map | 1 | 0 | 0 | 0 | Other |
| antenna.js | 20 | 0 | 0 | 0 | Frontend |
| antenna.js.map | 1 | 0 | 0 | 0 | Other |
| anvil.js | 25 | 0 | 0 | 0 | Frontend |
| anvil.js.map | 1 | 0 | 0 | 0 | Other |
| aperture.js | 21 | 0 | 0 | 0 | Frontend |
| aperture.js.map | 1 | 0 | 0 | 0 | Other |
| app-window-mac.js | 18 | 0 | 0 | 0 | Frontend |
| app-window-mac.js.map | 1 | 0 | 0 | 0 | Other |
| app-window.js | 18 | 0 | 0 | 0 | Frontend |
| app-window.js.map | 1 | 0 | 0 | 0 | Other |
| apple.js | 22 | 0 | 0 | 0 | Frontend |
| apple.js.map | 1 | 0 | 0 | 0 | Other |
| archive-restore.js | 19 | 0 | 0 | 0 | Frontend |
| archive-restore.js.map | 1 | 0 | 0 | 0 | Other |
| archive-x.js | 18 | 0 | 0 | 0 | Frontend |
| archive-x.js.map | 1 | 0 | 0 | 0 | Other |
| archive.js | 17 | 0 | 0 | 0 | Frontend |
| archive.js.map | 1 | 0 | 0 | 0 | Other |
| area-chart.js | 9 | 0 | 0 | 0 | Frontend |
| area-chart.js.map | 1 | 0 | 0 | 0 | Other |
| armchair.js | 24 | 0 | 0 | 0 | Frontend |
| armchair.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-big-down-dash.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-big-down-dash.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-big-down.js | 15 | 0 | 0 | 0 | Frontend |
| arrow-big-down.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-big-left-dash.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-big-left-dash.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-big-left.js | 15 | 0 | 0 | 0 | Frontend |
| arrow-big-left.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-big-right-dash.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-big-right-dash.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-big-right.js | 15 | 0 | 0 | 0 | Frontend |
| arrow-big-right.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-big-up-dash.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-big-up-dash.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-big-up.js | 15 | 0 | 0 | 0 | Frontend |
| arrow-big-up.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-0-1.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-down-0-1.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-01.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-01.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-1-0.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-down-1-0.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-10.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-10.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-a-z.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-down-a-z.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-az.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-az.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-circle.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-circle.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-from-line.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-down-from-line.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-left-from-circle.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-left-from-circle.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-left-from-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-left-from-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-left-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-left-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-left.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-down-left.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-narrow-wide.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-down-narrow-wide.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-right-from-circle.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-right-from-circle.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-right-from-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-right-from-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-right-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-right-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-right.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-down-right.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-to-dot.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-down-to-dot.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-to-line.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-down-to-line.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-up.js | 18 | 0 | 0 | 0 | Frontend |
| arrow-down-up.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-wide-narrow.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-down-wide-narrow.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-z-a.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-down-z-a.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down-za.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-down-za.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-down.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-down.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-left-circle.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-left-circle.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-left-from-line.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-left-from-line.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-left-right.js | 18 | 0 | 0 | 0 | Frontend |
| arrow-left-right.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-left-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-left-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-left-to-line.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-left-to-line.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-left.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-left.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-right-circle.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-right-circle.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-right-from-line.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-right-from-line.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-right-left.js | 18 | 0 | 0 | 0 | Frontend |
| arrow-right-left.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-right-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-right-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-right-to-line.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-right-to-line.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-right.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-right.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-0-1.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-up-0-1.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-01.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-01.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-1-0.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-up-1-0.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-10.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-10.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-a-z.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-up-a-z.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-az.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-az.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-circle.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-circle.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-down.js | 18 | 0 | 0 | 0 | Frontend |
| arrow-up-down.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-from-dot.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-up-from-dot.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-from-line.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-up-from-line.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-left-from-circle.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-left-from-circle.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-left-from-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-left-from-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-left-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-left-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-left.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-up-left.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-narrow-wide.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-up-narrow-wide.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-right-from-circle.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-right-from-circle.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-right-from-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-right-from-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-right-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-right-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-right.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-up-right.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-square.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-square.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-to-line.js | 17 | 0 | 0 | 0 | Frontend |
| arrow-up-to-line.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-wide-narrow.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-up-wide-narrow.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-z-a.js | 19 | 0 | 0 | 0 | Frontend |
| arrow-up-z-a.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up-za.js | 9 | 0 | 0 | 0 | Frontend |
| arrow-up-za.js.map | 1 | 0 | 0 | 0 | Other |
| arrow-up.js | 16 | 0 | 0 | 0 | Frontend |
| arrow-up.js.map | 1 | 0 | 0 | 0 | Other |
| arrows-up-from-line.js | 19 | 0 | 0 | 0 | Frontend |
| arrows-up-from-line.js.map | 1 | 0 | 0 | 0 | Other |
| asterisk-square.js | 9 | 0 | 0 | 0 | Frontend |
| asterisk-square.js.map | 1 | 0 | 0 | 0 | Other |
| asterisk.js | 17 | 0 | 0 | 0 | Frontend |
| asterisk.js.map | 1 | 0 | 0 | 0 | Other |
| at-sign.js | 16 | 0 | 0 | 0 | Frontend |
| at-sign.js.map | 1 | 0 | 0 | 0 | Other |
| atom.js | 29 | 0 | 0 | 0 | Frontend |
| atom.js.map | 1 | 0 | 0 | 0 | Other |
| audio-lines.js | 20 | 0 | 0 | 0 | Frontend |
| audio-lines.js.map | 1 | 0 | 0 | 0 | Other |
| audio-waveform.js | 21 | 0 | 0 | 0 | Frontend |
| audio-waveform.js.map | 1 | 0 | 0 | 0 | Other |
| award.js | 22 | 0 | 0 | 0 | Frontend |
| award.js.map | 1 | 0 | 0 | 0 | Other |
| axe.js | 16 | 0 | 0 | 0 | Frontend |
| axe.js.map | 1 | 0 | 0 | 0 | Other |
| axis-3-d.js | 9 | 0 | 0 | 0 | Frontend |
| axis-3-d.js.map | 1 | 0 | 0 | 0 | Other |
| axis-3d.js | 16 | 0 | 0 | 0 | Frontend |
| axis-3d.js.map | 1 | 0 | 0 | 0 | Other |
| baby.js | 24 | 0 | 0 | 0 | Frontend |
| baby.js.map | 1 | 0 | 0 | 0 | Other |
| backpack.js | 22 | 0 | 0 | 0 | Frontend |
| backpack.js.map | 1 | 0 | 0 | 0 | Other |
| badge-alert.js | 23 | 0 | 0 | 0 | Frontend |
| badge-alert.js.map | 1 | 0 | 0 | 0 | Other |
| badge-cent.js | 23 | 0 | 0 | 0 | Frontend |
| badge-cent.js.map | 1 | 0 | 0 | 0 | Other |
| badge-check.js | 22 | 0 | 0 | 0 | Frontend |
| badge-check.js.map | 1 | 0 | 0 | 0 | Other |
| badge-dollar-sign.js | 23 | 0 | 0 | 0 | Frontend |
| badge-dollar-sign.js.map | 1 | 0 | 0 | 0 | Other |
| badge-euro.js | 23 | 0 | 0 | 0 | Frontend |
| badge-euro.js.map | 1 | 0 | 0 | 0 | Other |
| badge-help.js | 23 | 0 | 0 | 0 | Frontend |
| badge-help.js.map | 1 | 0 | 0 | 0 | Other |
| badge-indian-rupee.js | 24 | 0 | 0 | 0 | Frontend |
| badge-indian-rupee.js.map | 1 | 0 | 0 | 0 | Other |
| badge-info.js | 23 | 0 | 0 | 0 | Frontend |
| badge-info.js.map | 1 | 0 | 0 | 0 | Other |
| badge-japanese-yen.js | 25 | 0 | 0 | 0 | Frontend |
| badge-japanese-yen.js.map | 1 | 0 | 0 | 0 | Other |
| badge-minus.js | 22 | 0 | 0 | 0 | Frontend |
| badge-minus.js.map | 1 | 0 | 0 | 0 | Other |
| badge-percent.js | 24 | 0 | 0 | 0 | Frontend |
| badge-percent.js.map | 1 | 0 | 0 | 0 | Other |
| badge-plus.js | 23 | 0 | 0 | 0 | Frontend |
| badge-plus.js.map | 1 | 0 | 0 | 0 | Other |
| badge-pound-sterling.js | 24 | 0 | 0 | 0 | Frontend |
| badge-pound-sterling.js.map | 1 | 0 | 0 | 0 | Other |
| badge-russian-ruble.js | 23 | 0 | 0 | 0 | Frontend |
| badge-russian-ruble.js.map | 1 | 0 | 0 | 0 | Other |
| badge-swiss-franc.js | 24 | 0 | 0 | 0 | Frontend |
| badge-swiss-franc.js.map | 1 | 0 | 0 | 0 | Other |
| badge-x.js | 23 | 0 | 0 | 0 | Frontend |
| badge-x.js.map | 1 | 0 | 0 | 0 | Other |
| badge.js | 21 | 0 | 0 | 0 | Frontend |
| badge.js.map | 1 | 0 | 0 | 0 | Other |
| baggage-claim.js | 19 | 0 | 0 | 0 | Frontend |
| baggage-claim.js.map | 1 | 0 | 0 | 0 | Other |
| ban.js | 16 | 0 | 0 | 0 | Frontend |
| ban.js.map | 1 | 0 | 0 | 0 | Other |
| banana.js | 22 | 0 | 0 | 0 | Frontend |
| banana.js.map | 1 | 0 | 0 | 0 | Other |
| bandage.js | 21 | 0 | 0 | 0 | Frontend |
| bandage.js.map | 1 | 0 | 0 | 0 | Other |
| banknote.js | 17 | 0 | 0 | 0 | Frontend |
| banknote.js.map | 1 | 0 | 0 | 0 | Other |
| bar-chart-2.js | 9 | 0 | 0 | 0 | Frontend |
| bar-chart-2.js.map | 1 | 0 | 0 | 0 | Other |
| bar-chart-3.js | 9 | 0 | 0 | 0 | Frontend |
| bar-chart-3.js.map | 1 | 0 | 0 | 0 | Other |
| bar-chart-4.js | 9 | 0 | 0 | 0 | Frontend |
| bar-chart-4.js.map | 1 | 0 | 0 | 0 | Other |
| bar-chart-big.js | 9 | 0 | 0 | 0 | Frontend |
| bar-chart-big.js.map | 1 | 0 | 0 | 0 | Other |
| bar-chart-horizontal-big.js | 9 | 0 | 0 | 0 | Frontend |
| bar-chart-horizontal-big.js.map | 1 | 0 | 0 | 0 | Other |
| bar-chart-horizontal.js | 9 | 0 | 0 | 0 | Frontend |
| bar-chart-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| bar-chart.js | 9 | 0 | 0 | 0 | Frontend |
| bar-chart.js.map | 1 | 0 | 0 | 0 | Other |
| barcode.js | 19 | 0 | 0 | 0 | Frontend |
| barcode.js.map | 1 | 0 | 0 | 0 | Other |
| baseline.js | 17 | 0 | 0 | 0 | Frontend |
| baseline.js.map | 1 | 0 | 0 | 0 | Other |
| bath.js | 25 | 0 | 0 | 0 | Frontend |
| bath.js.map | 1 | 0 | 0 | 0 | Other |
| battery-charging.js | 18 | 0 | 0 | 0 | Frontend |
| battery-charging.js.map | 1 | 0 | 0 | 0 | Other |
| battery-full.js | 19 | 0 | 0 | 0 | Frontend |
| battery-full.js.map | 1 | 0 | 0 | 0 | Other |
| battery-low.js | 17 | 0 | 0 | 0 | Frontend |
| battery-low.js.map | 1 | 0 | 0 | 0 | Other |
| battery-medium.js | 18 | 0 | 0 | 0 | Frontend |
| battery-medium.js.map | 1 | 0 | 0 | 0 | Other |
| battery-warning.js | 19 | 0 | 0 | 0 | Frontend |
| battery-warning.js.map | 1 | 0 | 0 | 0 | Other |
| battery.js | 16 | 0 | 0 | 0 | Frontend |
| battery.js.map | 1 | 0 | 0 | 0 | Other |
| beaker.js | 17 | 0 | 0 | 0 | Frontend |
| beaker.js.map | 1 | 0 | 0 | 0 | Other |
| bean-off.js | 30 | 0 | 0 | 0 | Frontend |
| bean-off.js.map | 1 | 0 | 0 | 0 | Other |
| bean.js | 22 | 0 | 0 | 0 | Frontend |
| bean.js.map | 1 | 0 | 0 | 0 | Other |
| bed-double.js | 18 | 0 | 0 | 0 | Frontend |
| bed-double.js.map | 1 | 0 | 0 | 0 | Other |
| bed-single.js | 17 | 0 | 0 | 0 | Frontend |
| bed-single.js.map | 1 | 0 | 0 | 0 | Other |
| bed.js | 18 | 0 | 0 | 0 | Frontend |
| bed.js.map | 1 | 0 | 0 | 0 | Other |
| beef.js | 29 | 0 | 0 | 0 | Frontend |
| beef.js.map | 1 | 0 | 0 | 0 | Other |
| beer-off.js | 31 | 0 | 0 | 0 | Frontend |
| beer-off.js.map | 1 | 0 | 0 | 0 | Other |
| beer.js | 25 | 0 | 0 | 0 | Frontend |
| beer.js.map | 1 | 0 | 0 | 0 | Other |
| bell-dot.js | 23 | 0 | 0 | 0 | Frontend |
| bell-dot.js.map | 1 | 0 | 0 | 0 | Other |
| bell-electric.js | 20 | 0 | 0 | 0 | Frontend |
| bell-electric.js.map | 1 | 0 | 0 | 0 | Other |
| bell-minus.js | 23 | 0 | 0 | 0 | Frontend |
| bell-minus.js.map | 1 | 0 | 0 | 0 | Other |
| bell-off.js | 24 | 0 | 0 | 0 | Frontend |
| bell-off.js.map | 1 | 0 | 0 | 0 | Other |
| bell-plus.js | 24 | 0 | 0 | 0 | Frontend |
| bell-plus.js.map | 1 | 0 | 0 | 0 | Other |
| bell-ring.js | 24 | 0 | 0 | 0 | Frontend |
| bell-ring.js.map | 1 | 0 | 0 | 0 | Other |
| bell.js | 22 | 0 | 0 | 0 | Frontend |
| bell.js.map | 1 | 0 | 0 | 0 | Other |
| between-horizonal-end.js | 9 | 0 | 0 | 0 | Frontend |
| between-horizonal-end.js.map | 1 | 0 | 0 | 0 | Other |
| between-horizonal-start.js | 9 | 0 | 0 | 0 | Frontend |
| between-horizonal-start.js.map | 1 | 0 | 0 | 0 | Other |
| between-horizontal-end.js | 17 | 0 | 0 | 0 | Frontend |
| between-horizontal-end.js.map | 1 | 0 | 0 | 0 | Other |
| between-horizontal-start.js | 17 | 0 | 0 | 0 | Frontend |
| between-horizontal-start.js.map | 1 | 0 | 0 | 0 | Other |
| between-vertical-end.js | 17 | 0 | 0 | 0 | Frontend |
| between-vertical-end.js.map | 1 | 0 | 0 | 0 | Other |
| between-vertical-start.js | 17 | 0 | 0 | 0 | Frontend |
| between-vertical-start.js.map | 1 | 0 | 0 | 0 | Other |
| biceps-flexed.js | 23 | 0 | 0 | 0 | Frontend |
| biceps-flexed.js.map | 1 | 0 | 0 | 0 | Other |
| bike.js | 18 | 0 | 0 | 0 | Frontend |
| bike.js.map | 1 | 0 | 0 | 0 | Other |
| binary.js | 20 | 0 | 0 | 0 | Frontend |
| binary.js.map | 1 | 0 | 0 | 0 | Other |
| binoculars.js | 32 | 0 | 0 | 0 | Frontend |
| binoculars.js.map | 1 | 0 | 0 | 0 | Other |
| biohazard.js | 24 | 0 | 0 | 0 | Frontend |
| biohazard.js.map | 1 | 0 | 0 | 0 | Other |
| bird.js | 20 | 0 | 0 | 0 | Frontend |
| bird.js.map | 1 | 0 | 0 | 0 | Other |
| bitcoin.js | 21 | 0 | 0 | 0 | Frontend |
| bitcoin.js.map | 1 | 0 | 0 | 0 | Other |
| blend.js | 16 | 0 | 0 | 0 | Frontend |
| blend.js.map | 1 | 0 | 0 | 0 | Other |
| blinds.js | 21 | 0 | 0 | 0 | Frontend |
| blinds.js.map | 1 | 0 | 0 | 0 | Other |
| blocks.js | 22 | 0 | 0 | 0 | Frontend |
| blocks.js.map | 1 | 0 | 0 | 0 | Other |
| bluetooth-connected.js | 17 | 0 | 0 | 0 | Frontend |
| bluetooth-connected.js.map | 1 | 0 | 0 | 0 | Other |
| bluetooth-off.js | 17 | 0 | 0 | 0 | Frontend |
| bluetooth-off.js.map | 1 | 0 | 0 | 0 | Other |
| bluetooth-searching.js | 17 | 0 | 0 | 0 | Frontend |
| bluetooth-searching.js.map | 1 | 0 | 0 | 0 | Other |
| bluetooth.js | 15 | 0 | 0 | 0 | Frontend |
| bluetooth.js.map | 1 | 0 | 0 | 0 | Other |
| bold.js | 18 | 0 | 0 | 0 | Frontend |
| bold.js.map | 1 | 0 | 0 | 0 | Other |
| bolt.js | 22 | 0 | 0 | 0 | Frontend |
| bolt.js.map | 1 | 0 | 0 | 0 | Other |
| bomb.js | 23 | 0 | 0 | 0 | Frontend |
| bomb.js.map | 1 | 0 | 0 | 0 | Other |
| bone.js | 21 | 0 | 0 | 0 | Frontend |
| bone.js.map | 1 | 0 | 0 | 0 | Other |
| book-a.js | 23 | 0 | 0 | 0 | Frontend |
| book-a.js.map | 1 | 0 | 0 | 0 | Other |
| book-audio.js | 24 | 0 | 0 | 0 | Frontend |
| book-audio.js.map | 1 | 0 | 0 | 0 | Other |
| book-check.js | 22 | 0 | 0 | 0 | Frontend |
| book-check.js.map | 1 | 0 | 0 | 0 | Other |
| book-copy.js | 23 | 0 | 0 | 0 | Frontend |
| book-copy.js.map | 1 | 0 | 0 | 0 | Other |
| book-dashed.js | 25 | 0 | 0 | 0 | Frontend |
| book-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| book-down.js | 23 | 0 | 0 | 0 | Frontend |
| book-down.js.map | 1 | 0 | 0 | 0 | Other |
| book-headphones.js | 24 | 0 | 0 | 0 | Frontend |
| book-headphones.js.map | 1 | 0 | 0 | 0 | Other |
| book-heart.js | 28 | 0 | 0 | 0 | Frontend |
| book-heart.js.map | 1 | 0 | 0 | 0 | Other |
| book-image.js | 23 | 0 | 0 | 0 | Frontend |
| book-image.js.map | 1 | 0 | 0 | 0 | Other |
| book-key.js | 19 | 0 | 0 | 0 | Frontend |
| book-key.js.map | 1 | 0 | 0 | 0 | Other |
| book-lock.js | 18 | 0 | 0 | 0 | Frontend |
| book-lock.js.map | 1 | 0 | 0 | 0 | Other |
| book-marked.js | 22 | 0 | 0 | 0 | Frontend |
| book-marked.js.map | 1 | 0 | 0 | 0 | Other |
| book-minus.js | 22 | 0 | 0 | 0 | Frontend |
| book-minus.js.map | 1 | 0 | 0 | 0 | Other |
| book-open-check.js | 23 | 0 | 0 | 0 | Frontend |
| book-open-check.js.map | 1 | 0 | 0 | 0 | Other |
| book-open-text.js | 26 | 0 | 0 | 0 | Frontend |
| book-open-text.js.map | 1 | 0 | 0 | 0 | Other |
| book-open.js | 22 | 0 | 0 | 0 | Frontend |
| book-open.js.map | 1 | 0 | 0 | 0 | Other |
| book-plus.js | 23 | 0 | 0 | 0 | Frontend |
| book-plus.js.map | 1 | 0 | 0 | 0 | Other |
| book-template.js | 9 | 0 | 0 | 0 | Frontend |
| book-template.js.map | 1 | 0 | 0 | 0 | Other |
| book-text.js | 23 | 0 | 0 | 0 | Frontend |
| book-text.js.map | 1 | 0 | 0 | 0 | Other |
| book-type.js | 24 | 0 | 0 | 0 | Frontend |
| book-type.js.map | 1 | 0 | 0 | 0 | Other |
| book-up-2.js | 19 | 0 | 0 | 0 | Frontend |
| book-up-2.js.map | 1 | 0 | 0 | 0 | Other |
| book-up.js | 23 | 0 | 0 | 0 | Frontend |
| book-up.js.map | 1 | 0 | 0 | 0 | Other |
| book-user.js | 23 | 0 | 0 | 0 | Frontend |
| book-user.js.map | 1 | 0 | 0 | 0 | Other |
| book-x.js | 23 | 0 | 0 | 0 | Frontend |
| book-x.js.map | 1 | 0 | 0 | 0 | Other |
| book.js | 21 | 0 | 0 | 0 | Frontend |
| book.js.map | 1 | 0 | 0 | 0 | Other |
| bookmark-check.js | 16 | 0 | 0 | 0 | Frontend |
| bookmark-check.js.map | 1 | 0 | 0 | 0 | Other |
| bookmark-minus.js | 16 | 0 | 0 | 0 | Frontend |
| bookmark-minus.js.map | 1 | 0 | 0 | 0 | Other |
| bookmark-plus.js | 17 | 0 | 0 | 0 | Frontend |
| bookmark-plus.js.map | 1 | 0 | 0 | 0 | Other |
| bookmark-x.js | 17 | 0 | 0 | 0 | Frontend |
| bookmark-x.js.map | 1 | 0 | 0 | 0 | Other |
| bookmark.js | 15 | 0 | 0 | 0 | Frontend |
| bookmark.js.map | 1 | 0 | 0 | 0 | Other |
| boom-box.js | 21 | 0 | 0 | 0 | Frontend |
| boom-box.js.map | 1 | 0 | 0 | 0 | Other |
| bot-message-square.js | 20 | 0 | 0 | 0 | Frontend |
| bot-message-square.js.map | 1 | 0 | 0 | 0 | Other |
| bot-off.js | 21 | 0 | 0 | 0 | Frontend |
| bot-off.js.map | 1 | 0 | 0 | 0 | Other |
| bot.js | 20 | 0 | 0 | 0 | Frontend |
| bot.js.map | 1 | 0 | 0 | 0 | Other |
| box-select.js | 9 | 0 | 0 | 0 | Frontend |
| box-select.js.map | 1 | 0 | 0 | 0 | Other |
| box.js | 23 | 0 | 0 | 0 | Frontend |
| box.js.map | 1 | 0 | 0 | 0 | Other |
| boxes.js | 44 | 0 | 0 | 0 | Frontend |
| boxes.js.map | 1 | 0 | 0 | 0 | Other |
| braces.js | 25 | 0 | 0 | 0 | Frontend |
| braces.js.map | 1 | 0 | 0 | 0 | Other |
| brackets.js | 16 | 0 | 0 | 0 | Frontend |
| brackets.js.map | 1 | 0 | 0 | 0 | Other |
| brain-circuit.js | 33 | 0 | 0 | 0 | Frontend |
| brain-circuit.js.map | 1 | 0 | 0 | 0 | Other |
| brain-cog.js | 36 | 0 | 0 | 0 | Frontend |
| brain-cog.js.map | 1 | 0 | 0 | 0 | Other |
| brain.js | 35 | 0 | 0 | 0 | Frontend |
| brain.js.map | 1 | 0 | 0 | 0 | Other |
| brick-wall.js | 22 | 0 | 0 | 0 | Frontend |
| brick-wall.js.map | 1 | 0 | 0 | 0 | Other |
| briefcase-business.js | 18 | 0 | 0 | 0 | Frontend |
| briefcase-business.js.map | 1 | 0 | 0 | 0 | Other |
| briefcase-conveyor-belt.js | 21 | 0 | 0 | 0 | Frontend |
| briefcase-conveyor-belt.js.map | 1 | 0 | 0 | 0 | Other |
| briefcase-medical.js | 20 | 0 | 0 | 0 | Frontend |
| briefcase-medical.js.map | 1 | 0 | 0 | 0 | Other |
| briefcase.js | 16 | 0 | 0 | 0 | Frontend |
| briefcase.js.map | 1 | 0 | 0 | 0 | Other |
| bring-to-front.js | 17 | 0 | 0 | 0 | Frontend |
| bring-to-front.js.map | 1 | 0 | 0 | 0 | Other |
| brush.js | 22 | 0 | 0 | 0 | Frontend |
| brush.js.map | 1 | 0 | 0 | 0 | Other |
| bug-off.js | 23 | 0 | 0 | 0 | Frontend |
| bug-off.js.map | 1 | 0 | 0 | 0 | Other |
| bug-play.js | 29 | 0 | 0 | 0 | Frontend |
| bug-play.js.map | 1 | 0 | 0 | 0 | Other |
| bug.js | 31 | 0 | 0 | 0 | Frontend |
| bug.js.map | 1 | 0 | 0 | 0 | Other |
| building-2.js | 21 | 0 | 0 | 0 | Frontend |
| building-2.js.map | 1 | 0 | 0 | 0 | Other |
| building.js | 25 | 0 | 0 | 0 | Frontend |
| building.js.map | 1 | 0 | 0 | 0 | Other |
| bus-front.js | 23 | 0 | 0 | 0 | Frontend |
| bus-front.js.map | 1 | 0 | 0 | 0 | Other |
| bus.js | 27 | 0 | 0 | 0 | Frontend |
| bus.js.map | 1 | 0 | 0 | 0 | Other |
| cable-car.js | 22 | 0 | 0 | 0 | Frontend |
| cable-car.js.map | 1 | 0 | 0 | 0 | Other |
| cable.js | 28 | 0 | 0 | 0 | Frontend |
| cable.js.map | 1 | 0 | 0 | 0 | Other |
| cake-slice.js | 21 | 0 | 0 | 0 | Frontend |
| cake-slice.js.map | 1 | 0 | 0 | 0 | Other |
| cake.js | 23 | 0 | 0 | 0 | Frontend |
| cake.js.map | 1 | 0 | 0 | 0 | Other |
| calculator.js | 24 | 0 | 0 | 0 | Frontend |
| calculator.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-1.js | 19 | 0 | 0 | 0 | Frontend |
| calendar-1.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-arrow-down.js | 23 | 0 | 0 | 0 | Frontend |
| calendar-arrow-down.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-arrow-up.js | 20 | 0 | 0 | 0 | Frontend |
| calendar-arrow-up.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-check-2.js | 19 | 0 | 0 | 0 | Frontend |
| calendar-check-2.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-check.js | 19 | 0 | 0 | 0 | Frontend |
| calendar-check.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-clock.js | 20 | 0 | 0 | 0 | Frontend |
| calendar-clock.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-cog.js | 27 | 0 | 0 | 0 | Frontend |
| calendar-cog.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-days.js | 24 | 0 | 0 | 0 | Frontend |
| calendar-days.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-fold.js | 19 | 0 | 0 | 0 | Frontend |
| calendar-fold.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-heart.js | 24 | 0 | 0 | 0 | Frontend |
| calendar-heart.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-minus-2.js | 19 | 0 | 0 | 0 | Frontend |
| calendar-minus-2.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-minus.js | 19 | 0 | 0 | 0 | Frontend |
| calendar-minus.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-off.js | 20 | 0 | 0 | 0 | Frontend |
| calendar-off.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-plus-2.js | 20 | 0 | 0 | 0 | Frontend |
| calendar-plus-2.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-plus.js | 20 | 0 | 0 | 0 | Frontend |
| calendar-plus.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-range.js | 22 | 0 | 0 | 0 | Frontend |
| calendar-range.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-search.js | 20 | 0 | 0 | 0 | Frontend |
| calendar-search.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-sync.js | 22 | 0 | 0 | 0 | Frontend |
| calendar-sync.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-x-2.js | 20 | 0 | 0 | 0 | Frontend |
| calendar-x-2.js.map | 1 | 0 | 0 | 0 | Other |
| calendar-x.js | 20 | 0 | 0 | 0 | Frontend |
| calendar-x.js.map | 1 | 0 | 0 | 0 | Other |
| calendar.js | 18 | 0 | 0 | 0 | Frontend |
| calendar.js.map | 1 | 0 | 0 | 0 | Other |
| camera-off.js | 18 | 0 | 0 | 0 | Frontend |
| camera-off.js.map | 1 | 0 | 0 | 0 | Other |
| camera.js | 22 | 0 | 0 | 0 | Frontend |
| camera.js.map | 1 | 0 | 0 | 0 | Other |
| candlestick-chart.js | 9 | 0 | 0 | 0 | Frontend |
| candlestick-chart.js.map | 1 | 0 | 0 | 0 | Other |
| candy-cane.js | 25 | 0 | 0 | 0 | Frontend |
| candy-cane.js.map | 1 | 0 | 0 | 0 | Other |
| candy-off.js | 37 | 0 | 0 | 0 | Frontend |
| candy-off.js.map | 1 | 0 | 0 | 0 | Other |
| candy.js | 25 | 0 | 0 | 0 | Frontend |
| candy.js.map | 1 | 0 | 0 | 0 | Other |
| cannabis.js | 22 | 0 | 0 | 0 | Frontend |
| cannabis.js.map | 1 | 0 | 0 | 0 | Other |
| captions-off.js | 20 | 0 | 0 | 0 | Frontend |
| captions-off.js.map | 1 | 0 | 0 | 0 | Other |
| captions.js | 16 | 0 | 0 | 0 | Frontend |
| captions.js.map | 1 | 0 | 0 | 0 | Other |
| car-front.js | 23 | 0 | 0 | 0 | Frontend |
| car-front.js.map | 1 | 0 | 0 | 0 | Other |
| car-taxi-front.js | 24 | 0 | 0 | 0 | Frontend |
| car-taxi-front.js.map | 1 | 0 | 0 | 0 | Other |
| car.js | 24 | 0 | 0 | 0 | Frontend |
| car.js.map | 1 | 0 | 0 | 0 | Other |
| caravan.js | 18 | 0 | 0 | 0 | Frontend |
| caravan.js.map | 1 | 0 | 0 | 0 | Other |
| carrot.js | 23 | 0 | 0 | 0 | Frontend |
| carrot.js.map | 1 | 0 | 0 | 0 | Other |
| case-lower.js | 18 | 0 | 0 | 0 | Frontend |
| case-lower.js.map | 1 | 0 | 0 | 0 | Other |
| case-sensitive.js | 18 | 0 | 0 | 0 | Frontend |
| case-sensitive.js.map | 1 | 0 | 0 | 0 | Other |
| case-upper.js | 17 | 0 | 0 | 0 | Frontend |
| case-upper.js.map | 1 | 0 | 0 | 0 | Other |
| cassette-tape.js | 19 | 0 | 0 | 0 | Frontend |
| cassette-tape.js.map | 1 | 0 | 0 | 0 | Other |
| cast.js | 18 | 0 | 0 | 0 | Frontend |
| cast.js.map | 1 | 0 | 0 | 0 | Other |
| castle.js | 23 | 0 | 0 | 0 | Frontend |
| castle.js.map | 1 | 0 | 0 | 0 | Other |
| cat.js | 24 | 0 | 0 | 0 | Frontend |
| cat.js.map | 1 | 0 | 0 | 0 | Other |
| cctv.js | 31 | 0 | 0 | 0 | Frontend |
| cctv.js.map | 1 | 0 | 0 | 0 | Other |
| chart-area.js | 22 | 0 | 0 | 0 | Frontend |
| chart-area.js.map | 1 | 0 | 0 | 0 | Other |
| chart-bar-big.js | 17 | 0 | 0 | 0 | Frontend |
| chart-bar-big.js.map | 1 | 0 | 0 | 0 | Other |
| chart-bar-decreasing.js | 18 | 0 | 0 | 0 | Frontend |
| chart-bar-decreasing.js.map | 1 | 0 | 0 | 0 | Other |
| chart-bar-increasing.js | 18 | 0 | 0 | 0 | Frontend |
| chart-bar-increasing.js.map | 1 | 0 | 0 | 0 | Other |
| chart-bar-stacked.js | 19 | 0 | 0 | 0 | Frontend |
| chart-bar-stacked.js.map | 1 | 0 | 0 | 0 | Other |
| chart-bar.js | 18 | 0 | 0 | 0 | Frontend |
| chart-bar.js.map | 1 | 0 | 0 | 0 | Other |
| chart-candlestick.js | 21 | 0 | 0 | 0 | Frontend |
| chart-candlestick.js.map | 1 | 0 | 0 | 0 | Other |
| chart-column-big.js | 17 | 0 | 0 | 0 | Frontend |
| chart-column-big.js.map | 1 | 0 | 0 | 0 | Other |
| chart-column-decreasing.js | 18 | 0 | 0 | 0 | Frontend |
| chart-column-decreasing.js.map | 1 | 0 | 0 | 0 | Other |
| chart-column-increasing.js | 18 | 0 | 0 | 0 | Frontend |
| chart-column-increasing.js.map | 1 | 0 | 0 | 0 | Other |
| chart-column-stacked.js | 19 | 0 | 0 | 0 | Frontend |
| chart-column-stacked.js.map | 1 | 0 | 0 | 0 | Other |
| chart-column.js | 18 | 0 | 0 | 0 | Frontend |
| chart-column.js.map | 1 | 0 | 0 | 0 | Other |
| chart-gantt.js | 18 | 0 | 0 | 0 | Frontend |
| chart-gantt.js.map | 1 | 0 | 0 | 0 | Other |
| chart-line.js | 16 | 0 | 0 | 0 | Frontend |
| chart-line.js.map | 1 | 0 | 0 | 0 | Other |
| chart-network.js | 21 | 0 | 0 | 0 | Frontend |
| chart-network.js.map | 1 | 0 | 0 | 0 | Other |
| chart-no-axes-column-decreasing.js | 17 | 0 | 0 | 0 | Frontend |
| chart-no-axes-column-decreasing.js.map | 1 | 0 | 0 | 0 | Other |
| chart-no-axes-column-increasing.js | 17 | 0 | 0 | 0 | Frontend |
| chart-no-axes-column-increasing.js.map | 1 | 0 | 0 | 0 | Other |
| chart-no-axes-column.js | 17 | 0 | 0 | 0 | Frontend |
| chart-no-axes-column.js.map | 1 | 0 | 0 | 0 | Other |
| chart-no-axes-combined.js | 23 | 0 | 0 | 0 | Frontend |
| chart-no-axes-combined.js.map | 1 | 0 | 0 | 0 | Other |
| chart-no-axes-gantt.js | 17 | 0 | 0 | 0 | Frontend |
| chart-no-axes-gantt.js.map | 1 | 0 | 0 | 0 | Other |
| chart-pie.js | 22 | 0 | 0 | 0 | Frontend |
| chart-pie.js.map | 1 | 0 | 0 | 0 | Other |
| chart-scatter.js | 20 | 0 | 0 | 0 | Frontend |
| chart-scatter.js.map | 1 | 0 | 0 | 0 | Other |
| chart-spline.js | 16 | 0 | 0 | 0 | Frontend |
| chart-spline.js.map | 1 | 0 | 0 | 0 | Other |
| check-check.js | 16 | 0 | 0 | 0 | Frontend |
| check-check.js.map | 1 | 0 | 0 | 0 | Other |
| check-circle-2.js | 9 | 0 | 0 | 0 | Frontend |
| check-circle-2.js.map | 1 | 0 | 0 | 0 | Other |
| check-circle.js | 9 | 0 | 0 | 0 | Frontend |
| check-circle.js.map | 1 | 0 | 0 | 0 | Other |
| check-square-2.js | 9 | 0 | 0 | 0 | Frontend |
| check-square-2.js.map | 1 | 0 | 0 | 0 | Other |
| check-square.js | 9 | 0 | 0 | 0 | Frontend |
| check-square.js.map | 1 | 0 | 0 | 0 | Other |
| check.js | 13 | 0 | 0 | 0 | Frontend |
| check.js.map | 1 | 0 | 0 | 0 | Other |
| chef-hat.js | 22 | 0 | 0 | 0 | Frontend |
| chef-hat.js.map | 1 | 0 | 0 | 0 | Other |
| cherry.js | 18 | 0 | 0 | 0 | Frontend |
| cherry.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-down-circle.js | 9 | 0 | 0 | 0 | Frontend |
| chevron-down-circle.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-down-square.js | 9 | 0 | 0 | 0 | Frontend |
| chevron-down-square.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-down.js | 15 | 0 | 0 | 0 | Frontend |
| chevron-down.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-first.js | 16 | 0 | 0 | 0 | Frontend |
| chevron-first.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-last.js | 16 | 0 | 0 | 0 | Frontend |
| chevron-last.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-left-circle.js | 9 | 0 | 0 | 0 | Frontend |
| chevron-left-circle.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-left-square.js | 9 | 0 | 0 | 0 | Frontend |
| chevron-left-square.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-left.js | 15 | 0 | 0 | 0 | Frontend |
| chevron-left.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-right-circle.js | 9 | 0 | 0 | 0 | Frontend |
| chevron-right-circle.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-right-square.js | 9 | 0 | 0 | 0 | Frontend |
| chevron-right-square.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-right.js | 15 | 0 | 0 | 0 | Frontend |
| chevron-right.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-up-circle.js | 9 | 0 | 0 | 0 | Frontend |
| chevron-up-circle.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-up-square.js | 9 | 0 | 0 | 0 | Frontend |
| chevron-up-square.js.map | 1 | 0 | 0 | 0 | Other |
| chevron-up.js | 13 | 0 | 0 | 0 | Frontend |
| chevron-up.js.map | 1 | 0 | 0 | 0 | Other |
| chevrons-down-up.js | 16 | 0 | 0 | 0 | Frontend |
| chevrons-down-up.js.map | 1 | 0 | 0 | 0 | Other |
| chevrons-down.js | 16 | 0 | 0 | 0 | Frontend |
| chevrons-down.js.map | 1 | 0 | 0 | 0 | Other |
| chevrons-left-right-ellipsis.js | 19 | 0 | 0 | 0 | Frontend |
| chevrons-left-right-ellipsis.js.map | 1 | 0 | 0 | 0 | Other |
| chevrons-left-right.js | 16 | 0 | 0 | 0 | Frontend |
| chevrons-left-right.js.map | 1 | 0 | 0 | 0 | Other |
| chevrons-left.js | 16 | 0 | 0 | 0 | Frontend |
| chevrons-left.js.map | 1 | 0 | 0 | 0 | Other |
| chevrons-right-left.js | 16 | 0 | 0 | 0 | Frontend |
| chevrons-right-left.js.map | 1 | 0 | 0 | 0 | Other |
| chevrons-right.js | 16 | 0 | 0 | 0 | Frontend |
| chevrons-right.js.map | 1 | 0 | 0 | 0 | Other |
| chevrons-up-down.js | 16 | 0 | 0 | 0 | Frontend |
| chevrons-up-down.js.map | 1 | 0 | 0 | 0 | Other |
| chevrons-up.js | 16 | 0 | 0 | 0 | Frontend |
| chevrons-up.js.map | 1 | 0 | 0 | 0 | Other |
| chrome.js | 19 | 0 | 0 | 0 | Frontend |
| chrome.js.map | 1 | 0 | 0 | 0 | Other |
| church.js | 31 | 0 | 0 | 0 | Frontend |
| church.js.map | 1 | 0 | 0 | 0 | Other |
| cigarette-off.js | 20 | 0 | 0 | 0 | Frontend |
| cigarette-off.js.map | 1 | 0 | 0 | 0 | Other |
| cigarette.js | 19 | 0 | 0 | 0 | Frontend |
| cigarette.js.map | 1 | 0 | 0 | 0 | Other |
| circle-alert.js | 17 | 0 | 0 | 0 | Frontend |
| circle-alert.js.map | 1 | 0 | 0 | 0 | Other |
| circle-arrow-down.js | 17 | 0 | 0 | 0 | Frontend |
| circle-arrow-down.js.map | 1 | 0 | 0 | 0 | Other |
| circle-arrow-left.js | 17 | 0 | 0 | 0 | Frontend |
| circle-arrow-left.js.map | 1 | 0 | 0 | 0 | Other |
| circle-arrow-out-down-left.js | 17 | 0 | 0 | 0 | Frontend |
| circle-arrow-out-down-left.js.map | 1 | 0 | 0 | 0 | Other |
| circle-arrow-out-down-right.js | 17 | 0 | 0 | 0 | Frontend |
| circle-arrow-out-down-right.js.map | 1 | 0 | 0 | 0 | Other |
| circle-arrow-out-up-left.js | 17 | 0 | 0 | 0 | Frontend |
| circle-arrow-out-up-left.js.map | 1 | 0 | 0 | 0 | Other |
| circle-arrow-out-up-right.js | 17 | 0 | 0 | 0 | Frontend |
| circle-arrow-out-up-right.js.map | 1 | 0 | 0 | 0 | Other |
| circle-arrow-right.js | 17 | 0 | 0 | 0 | Frontend |
| circle-arrow-right.js.map | 1 | 0 | 0 | 0 | Other |
| circle-arrow-up.js | 17 | 0 | 0 | 0 | Frontend |
| circle-arrow-up.js.map | 1 | 0 | 0 | 0 | Other |
| circle-check-big.js | 16 | 0 | 0 | 0 | Frontend |
| circle-check-big.js.map | 1 | 0 | 0 | 0 | Other |
| circle-check.js | 16 | 0 | 0 | 0 | Frontend |
| circle-check.js.map | 1 | 0 | 0 | 0 | Other |
| circle-chevron-down.js | 16 | 0 | 0 | 0 | Frontend |
| circle-chevron-down.js.map | 1 | 0 | 0 | 0 | Other |
| circle-chevron-left.js | 16 | 0 | 0 | 0 | Frontend |
| circle-chevron-left.js.map | 1 | 0 | 0 | 0 | Other |
| circle-chevron-right.js | 16 | 0 | 0 | 0 | Frontend |
| circle-chevron-right.js.map | 1 | 0 | 0 | 0 | Other |
| circle-chevron-up.js | 16 | 0 | 0 | 0 | Frontend |
| circle-chevron-up.js.map | 1 | 0 | 0 | 0 | Other |
| circle-dashed.js | 22 | 0 | 0 | 0 | Frontend |
| circle-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| circle-divide.js | 18 | 0 | 0 | 0 | Frontend |
| circle-divide.js.map | 1 | 0 | 0 | 0 | Other |
| circle-dollar-sign.js | 17 | 0 | 0 | 0 | Frontend |
| circle-dollar-sign.js.map | 1 | 0 | 0 | 0 | Other |
| circle-dot-dashed.js | 23 | 0 | 0 | 0 | Frontend |
| circle-dot-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| circle-dot.js | 16 | 0 | 0 | 0 | Frontend |
| circle-dot.js.map | 1 | 0 | 0 | 0 | Other |
| circle-ellipsis.js | 18 | 0 | 0 | 0 | Frontend |
| circle-ellipsis.js.map | 1 | 0 | 0 | 0 | Other |
| circle-equal.js | 17 | 0 | 0 | 0 | Frontend |
| circle-equal.js.map | 1 | 0 | 0 | 0 | Other |
| circle-fading-arrow-up.js | 21 | 0 | 0 | 0 | Frontend |
| circle-fading-arrow-up.js.map | 1 | 0 | 0 | 0 | Other |
| circle-fading-plus.js | 21 | 0 | 0 | 0 | Frontend |
| circle-fading-plus.js.map | 1 | 0 | 0 | 0 | Other |
| circle-gauge.js | 17 | 0 | 0 | 0 | Frontend |
| circle-gauge.js.map | 1 | 0 | 0 | 0 | Other |
| circle-help.js | 17 | 0 | 0 | 0 | Frontend |
| circle-help.js.map | 1 | 0 | 0 | 0 | Other |
| circle-minus.js | 16 | 0 | 0 | 0 | Frontend |
| circle-minus.js.map | 1 | 0 | 0 | 0 | Other |
| circle-off.js | 17 | 0 | 0 | 0 | Frontend |
| circle-off.js.map | 1 | 0 | 0 | 0 | Other |
| circle-parking-off.js | 18 | 0 | 0 | 0 | Frontend |
| circle-parking-off.js.map | 1 | 0 | 0 | 0 | Other |
| circle-parking.js | 16 | 0 | 0 | 0 | Frontend |
| circle-parking.js.map | 1 | 0 | 0 | 0 | Other |
| circle-pause.js | 17 | 0 | 0 | 0 | Frontend |
| circle-pause.js.map | 1 | 0 | 0 | 0 | Other |
| circle-percent.js | 18 | 0 | 0 | 0 | Frontend |
| circle-percent.js.map | 1 | 0 | 0 | 0 | Other |
| circle-play.js | 16 | 0 | 0 | 0 | Frontend |
| circle-play.js.map | 1 | 0 | 0 | 0 | Other |
| circle-plus.js | 17 | 0 | 0 | 0 | Frontend |
| circle-plus.js.map | 1 | 0 | 0 | 0 | Other |
| circle-power.js | 17 | 0 | 0 | 0 | Frontend |
| circle-power.js.map | 1 | 0 | 0 | 0 | Other |
| circle-slash-2.js | 16 | 0 | 0 | 0 | Frontend |
| circle-slash-2.js.map | 1 | 0 | 0 | 0 | Other |
| circle-slash.js | 16 | 0 | 0 | 0 | Frontend |
| circle-slash.js.map | 1 | 0 | 0 | 0 | Other |
| circle-slashed.js | 9 | 0 | 0 | 0 | Frontend |
| circle-slashed.js.map | 1 | 0 | 0 | 0 | Other |
| circle-stop.js | 16 | 0 | 0 | 0 | Frontend |
| circle-stop.js.map | 1 | 0 | 0 | 0 | Other |
| circle-user-round.js | 17 | 0 | 0 | 0 | Frontend |
| circle-user-round.js.map | 1 | 0 | 0 | 0 | Other |
| circle-user.js | 17 | 0 | 0 | 0 | Frontend |
| circle-user.js.map | 1 | 0 | 0 | 0 | Other |
| circle-x.js | 17 | 0 | 0 | 0 | Frontend |
| circle-x.js.map | 1 | 0 | 0 | 0 | Other |
| circle.js | 15 | 0 | 0 | 0 | Frontend |
| circle.js.map | 1 | 0 | 0 | 0 | Other |
| circuit-board.js | 19 | 0 | 0 | 0 | Frontend |
| circuit-board.js.map | 1 | 0 | 0 | 0 | Other |
| citrus.js | 24 | 0 | 0 | 0 | Frontend |
| citrus.js.map | 1 | 0 | 0 | 0 | Other |
| clapperboard.js | 21 | 0 | 0 | 0 | Frontend |
| clapperboard.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-check.js | 23 | 0 | 0 | 0 | Frontend |
| clipboard-check.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-copy.js | 19 | 0 | 0 | 0 | Frontend |
| clipboard-copy.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-edit.js | 9 | 0 | 0 | 0 | Frontend |
| clipboard-edit.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-list.js | 26 | 0 | 0 | 0 | Frontend |
| clipboard-list.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-minus.js | 23 | 0 | 0 | 0 | Frontend |
| clipboard-minus.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-paste.js | 26 | 0 | 0 | 0 | Frontend |
| clipboard-paste.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-pen-line.js | 25 | 0 | 0 | 0 | Frontend |
| clipboard-pen-line.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-pen.js | 24 | 0 | 0 | 0 | Frontend |
| clipboard-pen.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-plus.js | 24 | 0 | 0 | 0 | Frontend |
| clipboard-plus.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-signature.js | 9 | 0 | 0 | 0 | Frontend |
| clipboard-signature.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-type.js | 25 | 0 | 0 | 0 | Frontend |
| clipboard-type.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard-x.js | 24 | 0 | 0 | 0 | Frontend |
| clipboard-x.js.map | 1 | 0 | 0 | 0 | Other |
| clipboard.js | 22 | 0 | 0 | 0 | Frontend |
| clipboard.js.map | 1 | 0 | 0 | 0 | Other |
| clock-1.js | 16 | 0 | 0 | 0 | Frontend |
| clock-1.js.map | 1 | 0 | 0 | 0 | Other |
| clock-10.js | 16 | 0 | 0 | 0 | Frontend |
| clock-10.js.map | 1 | 0 | 0 | 0 | Other |
| clock-11.js | 16 | 0 | 0 | 0 | Frontend |
| clock-11.js.map | 1 | 0 | 0 | 0 | Other |
| clock-12.js | 16 | 0 | 0 | 0 | Frontend |
| clock-12.js.map | 1 | 0 | 0 | 0 | Other |
| clock-2.js | 16 | 0 | 0 | 0 | Frontend |
| clock-2.js.map | 1 | 0 | 0 | 0 | Other |
| clock-3.js | 16 | 0 | 0 | 0 | Frontend |
| clock-3.js.map | 1 | 0 | 0 | 0 | Other |
| clock-4.js | 16 | 0 | 0 | 0 | Frontend |
| clock-4.js.map | 1 | 0 | 0 | 0 | Other |
| clock-5.js | 16 | 0 | 0 | 0 | Frontend |
| clock-5.js.map | 1 | 0 | 0 | 0 | Other |
| clock-6.js | 16 | 0 | 0 | 0 | Frontend |
| clock-6.js.map | 1 | 0 | 0 | 0 | Other |
| clock-7.js | 16 | 0 | 0 | 0 | Frontend |
| clock-7.js.map | 1 | 0 | 0 | 0 | Other |
| clock-8.js | 16 | 0 | 0 | 0 | Frontend |
| clock-8.js.map | 1 | 0 | 0 | 0 | Other |
| clock-9.js | 16 | 0 | 0 | 0 | Frontend |
| clock-9.js.map | 1 | 0 | 0 | 0 | Other |
| clock-alert.js | 18 | 0 | 0 | 0 | Frontend |
| clock-alert.js.map | 1 | 0 | 0 | 0 | Other |
| clock-arrow-down.js | 18 | 0 | 0 | 0 | Frontend |
| clock-arrow-down.js.map | 1 | 0 | 0 | 0 | Other |
| clock-arrow-up.js | 18 | 0 | 0 | 0 | Frontend |
| clock-arrow-up.js.map | 1 | 0 | 0 | 0 | Other |
| clock.js | 16 | 0 | 0 | 0 | Frontend |
| clock.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-alert.js | 17 | 0 | 0 | 0 | Frontend |
| cloud-alert.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-cog.js | 24 | 0 | 0 | 0 | Frontend |
| cloud-cog.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-download.js | 17 | 0 | 0 | 0 | Frontend |
| cloud-download.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-drizzle.js | 21 | 0 | 0 | 0 | Frontend |
| cloud-drizzle.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-fog.js | 17 | 0 | 0 | 0 | Frontend |
| cloud-fog.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-hail.js | 21 | 0 | 0 | 0 | Frontend |
| cloud-hail.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-lightning.js | 16 | 0 | 0 | 0 | Frontend |
| cloud-lightning.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-moon-rain.js | 18 | 0 | 0 | 0 | Frontend |
| cloud-moon-rain.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-moon.js | 16 | 0 | 0 | 0 | Frontend |
| cloud-moon.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-off.js | 20 | 0 | 0 | 0 | Frontend |
| cloud-off.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-rain-wind.js | 18 | 0 | 0 | 0 | Frontend |
| cloud-rain-wind.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-rain.js | 18 | 0 | 0 | 0 | Frontend |
| cloud-rain.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-snow.js | 21 | 0 | 0 | 0 | Frontend |
| cloud-snow.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-sun-rain.js | 22 | 0 | 0 | 0 | Frontend |
| cloud-sun-rain.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-sun.js | 20 | 0 | 0 | 0 | Frontend |
| cloud-sun.js.map | 1 | 0 | 0 | 0 | Other |
| cloud-upload.js | 17 | 0 | 0 | 0 | Frontend |
| cloud-upload.js.map | 1 | 0 | 0 | 0 | Other |
| cloud.js | 15 | 0 | 0 | 0 | Frontend |
| cloud.js.map | 1 | 0 | 0 | 0 | Other |
| cloudy.js | 16 | 0 | 0 | 0 | Frontend |
| cloudy.js.map | 1 | 0 | 0 | 0 | Other |
| clover.js | 23 | 0 | 0 | 0 | Frontend |
| clover.js.map | 1 | 0 | 0 | 0 | Other |
| club.js | 22 | 0 | 0 | 0 | Frontend |
| club.js.map | 1 | 0 | 0 | 0 | Other |
| code-2.js | 9 | 0 | 0 | 0 | Frontend |
| code-2.js.map | 1 | 0 | 0 | 0 | Other |
| code-square.js | 9 | 0 | 0 | 0 | Frontend |
| code-square.js.map | 1 | 0 | 0 | 0 | Other |
| code-xml.js | 17 | 0 | 0 | 0 | Frontend |
| code-xml.js.map | 1 | 0 | 0 | 0 | Other |
| code.js | 16 | 0 | 0 | 0 | Frontend |
| code.js.map | 1 | 0 | 0 | 0 | Other |
| codepen.js | 19 | 0 | 0 | 0 | Frontend |
| codepen.js.map | 1 | 0 | 0 | 0 | Other |
| codesandbox.js | 26 | 0 | 0 | 0 | Frontend |
| codesandbox.js.map | 1 | 0 | 0 | 0 | Other |
| coffee.js | 24 | 0 | 0 | 0 | Frontend |
| coffee.js.map | 1 | 0 | 0 | 0 | Other |
| cog.js | 28 | 0 | 0 | 0 | Frontend |
| cog.js.map | 1 | 0 | 0 | 0 | Other |
| coins.js | 18 | 0 | 0 | 0 | Frontend |
| coins.js.map | 1 | 0 | 0 | 0 | Other |
| columns-2.js | 16 | 0 | 0 | 0 | Frontend |
| columns-2.js.map | 1 | 0 | 0 | 0 | Other |
| columns-3.js | 17 | 0 | 0 | 0 | Frontend |
| columns-3.js.map | 1 | 0 | 0 | 0 | Other |
| columns-4.js | 18 | 0 | 0 | 0 | Frontend |
| columns-4.js.map | 1 | 0 | 0 | 0 | Other |
| columns.js | 9 | 0 | 0 | 0 | Frontend |
| columns.js.map | 1 | 0 | 0 | 0 | Other |
| combine.js | 20 | 0 | 0 | 0 | Frontend |
| combine.js.map | 1 | 0 | 0 | 0 | Other |
| command.js | 18 | 0 | 0 | 0 | Frontend |
| command.js.map | 1 | 0 | 0 | 0 | Other |
| compass.js | 22 | 0 | 0 | 0 | Frontend |
| compass.js.map | 1 | 0 | 0 | 0 | Other |
| component.js | 42 | 0 | 0 | 0 | Frontend |
| component.js.map | 1 | 0 | 0 | 0 | Other |
| computer.js | 18 | 0 | 0 | 0 | Frontend |
| computer.js.map | 1 | 0 | 0 | 0 | Other |
| concierge-bell.js | 21 | 0 | 0 | 0 | Frontend |
| concierge-bell.js.map | 1 | 0 | 0 | 0 | Other |
| cone.js | 16 | 0 | 0 | 0 | Frontend |
| cone.js.map | 1 | 0 | 0 | 0 | Other |
| construction.js | 22 | 0 | 0 | 0 | Frontend |
| construction.js.map | 1 | 0 | 0 | 0 | Other |
| contact-2.js | 9 | 0 | 0 | 0 | Frontend |
| contact-2.js.map | 1 | 0 | 0 | 0 | Other |
| contact-round.js | 19 | 0 | 0 | 0 | Frontend |
| contact-round.js.map | 1 | 0 | 0 | 0 | Other |
| contact.js | 19 | 0 | 0 | 0 | Frontend |
| contact.js.map | 1 | 0 | 0 | 0 | Other |
| container.js | 25 | 0 | 0 | 0 | Frontend |
| container.js.map | 1 | 0 | 0 | 0 | Other |
| contrast.js | 16 | 0 | 0 | 0 | Frontend |
| contrast.js.map | 1 | 0 | 0 | 0 | Other |
| cookie.js | 20 | 0 | 0 | 0 | Frontend |
| cookie.js.map | 1 | 0 | 0 | 0 | Other |
| cooking-pot.js | 24 | 0 | 0 | 0 | Frontend |
| cooking-pot.js.map | 1 | 0 | 0 | 0 | Other |
| copy-check.js | 17 | 0 | 0 | 0 | Frontend |
| copy-check.js.map | 1 | 0 | 0 | 0 | Other |
| copy-minus.js | 17 | 0 | 0 | 0 | Frontend |
| copy-minus.js.map | 1 | 0 | 0 | 0 | Other |
| copy-plus.js | 18 | 0 | 0 | 0 | Frontend |
| copy-plus.js.map | 1 | 0 | 0 | 0 | Other |
| copy-slash.js | 17 | 0 | 0 | 0 | Frontend |
| copy-slash.js.map | 1 | 0 | 0 | 0 | Other |
| copy-x.js | 18 | 0 | 0 | 0 | Frontend |
| copy-x.js.map | 1 | 0 | 0 | 0 | Other |
| copy.js | 16 | 0 | 0 | 0 | Frontend |
| copy.js.map | 1 | 0 | 0 | 0 | Other |
| copyleft.js | 16 | 0 | 0 | 0 | Frontend |
| copyleft.js.map | 1 | 0 | 0 | 0 | Other |
| copyright.js | 16 | 0 | 0 | 0 | Frontend |
| copyright.js.map | 1 | 0 | 0 | 0 | Other |
| corner-down-left.js | 16 | 0 | 0 | 0 | Frontend |
| corner-down-left.js.map | 1 | 0 | 0 | 0 | Other |
| corner-down-right.js | 16 | 0 | 0 | 0 | Frontend |
| corner-down-right.js.map | 1 | 0 | 0 | 0 | Other |
| corner-left-down.js | 16 | 0 | 0 | 0 | Frontend |
| corner-left-down.js.map | 1 | 0 | 0 | 0 | Other |
| corner-left-up.js | 16 | 0 | 0 | 0 | Frontend |
| corner-left-up.js.map | 1 | 0 | 0 | 0 | Other |
| corner-right-down.js | 16 | 0 | 0 | 0 | Frontend |
| corner-right-down.js.map | 1 | 0 | 0 | 0 | Other |
| corner-right-up.js | 16 | 0 | 0 | 0 | Frontend |
| corner-right-up.js.map | 1 | 0 | 0 | 0 | Other |
| corner-up-left.js | 16 | 0 | 0 | 0 | Frontend |
| corner-up-left.js.map | 1 | 0 | 0 | 0 | Other |
| corner-up-right.js | 16 | 0 | 0 | 0 | Frontend |
| corner-up-right.js.map | 1 | 0 | 0 | 0 | Other |
| cpu.js | 24 | 0 | 0 | 0 | Frontend |
| cpu.js.map | 1 | 0 | 0 | 0 | Other |
| creative-commons.js | 23 | 0 | 0 | 0 | Frontend |
| creative-commons.js.map | 1 | 0 | 0 | 0 | Other |
| credit-card.js | 16 | 0 | 0 | 0 | Frontend |
| credit-card.js.map | 1 | 0 | 0 | 0 | Other |
| croissant.js | 37 | 0 | 0 | 0 | Frontend |
| croissant.js.map | 1 | 0 | 0 | 0 | Other |
| crop.js | 16 | 0 | 0 | 0 | Frontend |
| crop.js.map | 1 | 0 | 0 | 0 | Other |
| cross.js | 21 | 0 | 0 | 0 | Frontend |
| cross.js.map | 1 | 0 | 0 | 0 | Other |
| crosshair.js | 19 | 0 | 0 | 0 | Frontend |
| crosshair.js.map | 1 | 0 | 0 | 0 | Other |
| crown.js | 22 | 0 | 0 | 0 | Frontend |
| crown.js.map | 1 | 0 | 0 | 0 | Other |
| cuboid.js | 23 | 0 | 0 | 0 | Frontend |
| cuboid.js.map | 1 | 0 | 0 | 0 | Other |
| cup-soda.js | 18 | 0 | 0 | 0 | Frontend |
| cup-soda.js.map | 1 | 0 | 0 | 0 | Other |
| curly-braces.js | 9 | 0 | 0 | 0 | Frontend |
| curly-braces.js.map | 1 | 0 | 0 | 0 | Other |
| currency.js | 19 | 0 | 0 | 0 | Frontend |
| currency.js.map | 1 | 0 | 0 | 0 | Other |
| cylinder.js | 16 | 0 | 0 | 0 | Frontend |
| cylinder.js.map | 1 | 0 | 0 | 0 | Other |
| dam.js | 27 | 0 | 0 | 0 | Frontend |
| dam.js.map | 1 | 0 | 0 | 0 | Other |
| database-backup.js | 26 | 0 | 0 | 0 | Frontend |
| database-backup.js.map | 1 | 0 | 0 | 0 | Data |
| database-zap.js | 19 | 0 | 0 | 0 | Frontend |
| database-zap.js.map | 1 | 0 | 0 | 0 | Data |
| database.js | 17 | 0 | 0 | 0 | Frontend |
| database.js.map | 1 | 0 | 0 | 0 | Data |
| delete.js | 23 | 0 | 0 | 0 | Frontend |
| delete.js.map | 1 | 0 | 0 | 0 | Other |
| dessert.js | 23 | 0 | 0 | 0 | Frontend |
| dessert.js.map | 1 | 0 | 0 | 0 | Other |
| diameter.js | 19 | 0 | 0 | 0 | Frontend |
| diameter.js.map | 1 | 0 | 0 | 0 | Other |
| diamond-minus.js | 22 | 0 | 0 | 0 | Frontend |
| diamond-minus.js.map | 1 | 0 | 0 | 0 | Other |
| diamond-percent.js | 24 | 0 | 0 | 0 | Frontend |
| diamond-percent.js.map | 1 | 0 | 0 | 0 | Other |
| diamond-plus.js | 23 | 0 | 0 | 0 | Frontend |
| diamond-plus.js.map | 1 | 0 | 0 | 0 | Other |
| diamond.js | 21 | 0 | 0 | 0 | Frontend |
| diamond.js.map | 1 | 0 | 0 | 0 | Other |
| dice-1.js | 16 | 0 | 0 | 0 | Frontend |
| dice-1.js.map | 1 | 0 | 0 | 0 | Other |
| dice-2.js | 17 | 0 | 0 | 0 | Frontend |
| dice-2.js.map | 1 | 0 | 0 | 0 | Other |
| dice-3.js | 18 | 0 | 0 | 0 | Frontend |
| dice-3.js.map | 1 | 0 | 0 | 0 | Other |
| dice-4.js | 19 | 0 | 0 | 0 | Frontend |
| dice-4.js.map | 1 | 0 | 0 | 0 | Other |
| dice-5.js | 20 | 0 | 0 | 0 | Frontend |
| dice-5.js.map | 1 | 0 | 0 | 0 | Other |
| dice-6.js | 21 | 0 | 0 | 0 | Frontend |
| dice-6.js.map | 1 | 0 | 0 | 0 | Other |
| dices.js | 23 | 0 | 0 | 0 | Frontend |
| dices.js.map | 1 | 0 | 0 | 0 | Other |
| diff.js | 17 | 0 | 0 | 0 | Frontend |
| diff.js.map | 1 | 0 | 0 | 0 | Other |
| disc-2.js | 17 | 0 | 0 | 0 | Frontend |
| disc-2.js.map | 1 | 0 | 0 | 0 | Other |
| disc-3.js | 18 | 0 | 0 | 0 | Frontend |
| disc-3.js.map | 1 | 0 | 0 | 0 | Other |
| disc-album.js | 17 | 0 | 0 | 0 | Frontend |
| disc-album.js.map | 1 | 0 | 0 | 0 | Other |
| disc.js | 16 | 0 | 0 | 0 | Frontend |
| disc.js.map | 1 | 0 | 0 | 0 | Other |
| divide-circle.js | 9 | 0 | 0 | 0 | Frontend |
| divide-circle.js.map | 1 | 0 | 0 | 0 | Other |
| divide-square.js | 9 | 0 | 0 | 0 | Frontend |
| divide-square.js.map | 1 | 0 | 0 | 0 | Other |
| divide.js | 17 | 0 | 0 | 0 | Frontend |
| divide.js.map | 1 | 0 | 0 | 0 | Other |
| dna-off.js | 24 | 0 | 0 | 0 | Frontend |
| dna-off.js.map | 1 | 0 | 0 | 0 | Other |
| dna.js | 25 | 0 | 0 | 0 | Frontend |
| dna.js.map | 1 | 0 | 0 | 0 | Other |
| dock.js | 17 | 0 | 0 | 0 | Frontend |
| dock.js.map | 1 | 0 | 0 | 0 | Other |
| dog.js | 31 | 0 | 0 | 0 | Frontend |
| dog.js.map | 1 | 0 | 0 | 0 | Other |
| dollar-sign.js | 16 | 0 | 0 | 0 | Frontend |
| dollar-sign.js.map | 1 | 0 | 0 | 0 | Other |
| donut.js | 22 | 0 | 0 | 0 | Frontend |
| donut.js.map | 1 | 0 | 0 | 0 | Other |
| door-closed.js | 17 | 0 | 0 | 0 | Frontend |
| door-closed.js.map | 1 | 0 | 0 | 0 | Other |
| door-open.js | 25 | 0 | 0 | 0 | Frontend |
| door-open.js.map | 1 | 0 | 0 | 0 | Other |
| dot-square.js | 9 | 0 | 0 | 0 | Frontend |
| dot-square.js.map | 1 | 0 | 0 | 0 | Other |
| dot.js | 15 | 0 | 0 | 0 | Frontend |
| dot.js.map | 1 | 0 | 0 | 0 | Other |
| download-cloud.js | 9 | 0 | 0 | 0 | Frontend |
| download-cloud.js.map | 1 | 0 | 0 | 0 | Other |
| download.js | 17 | 0 | 0 | 0 | Frontend |
| download.js.map | 1 | 0 | 0 | 0 | Other |
| drafting-compass.js | 19 | 0 | 0 | 0 | Frontend |
| drafting-compass.js.map | 1 | 0 | 0 | 0 | Other |
| drama.js | 28 | 0 | 0 | 0 | Frontend |
| drama.js.map | 1 | 0 | 0 | 0 | Other |
| dribbble.js | 18 | 0 | 0 | 0 | Frontend |
| dribbble.js.map | 1 | 0 | 0 | 0 | Other |
| drill.js | 29 | 0 | 0 | 0 | Frontend |
| drill.js.map | 1 | 0 | 0 | 0 | Other |
| droplet-off.js | 26 | 0 | 0 | 0 | Frontend |
| droplet-off.js.map | 1 | 0 | 0 | 0 | Other |
| droplet.js | 21 | 0 | 0 | 0 | Frontend |
| droplet.js.map | 1 | 0 | 0 | 0 | Other |
| droplets.js | 28 | 0 | 0 | 0 | Frontend |
| droplets.js.map | 1 | 0 | 0 | 0 | Other |
| drum.js | 21 | 0 | 0 | 0 | Frontend |
| drum.js.map | 1 | 0 | 0 | 0 | Other |
| drumstick.js | 25 | 0 | 0 | 0 | Frontend |
| drumstick.js.map | 1 | 0 | 0 | 0 | Other |
| dumbbell.js | 31 | 0 | 0 | 0 | Frontend |
| dumbbell.js.map | 1 | 0 | 0 | 0 | Other |
| ear-off.js | 19 | 0 | 0 | 0 | Frontend |
| ear-off.js.map | 1 | 0 | 0 | 0 | Other |
| ear.js | 16 | 0 | 0 | 0 | Frontend |
| ear.js.map | 1 | 0 | 0 | 0 | Other |
| earth-lock.js | 20 | 0 | 0 | 0 | Frontend |
| earth-lock.js.map | 1 | 0 | 0 | 0 | Other |
| earth.js | 24 | 0 | 0 | 0 | Frontend |
| earth.js.map | 1 | 0 | 0 | 0 | Other |
| eclipse.js | 16 | 0 | 0 | 0 | Frontend |
| eclipse.js.map | 1 | 0 | 0 | 0 | Other |
| edit-2.js | 9 | 0 | 0 | 0 | Frontend |
| edit-2.js.map | 1 | 0 | 0 | 0 | Other |
| edit-3.js | 9 | 0 | 0 | 0 | Frontend |
| edit-3.js.map | 1 | 0 | 0 | 0 | Other |
| edit.js | 9 | 0 | 0 | 0 | Frontend |
| edit.js.map | 1 | 0 | 0 | 0 | Other |
| egg-fried.js | 22 | 0 | 0 | 0 | Frontend |
| egg-fried.js.map | 1 | 0 | 0 | 0 | Other |
| egg-off.js | 29 | 0 | 0 | 0 | Frontend |
| egg-off.js.map | 1 | 0 | 0 | 0 | Other |
| egg.js | 21 | 0 | 0 | 0 | Frontend |
| egg.js.map | 1 | 0 | 0 | 0 | Other |
| ellipsis-vertical.js | 17 | 0 | 0 | 0 | Frontend |
| ellipsis-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| ellipsis.js | 17 | 0 | 0 | 0 | Frontend |
| ellipsis.js.map | 1 | 0 | 0 | 0 | Other |
| equal-approximately.js | 16 | 0 | 0 | 0 | Frontend |
| equal-approximately.js.map | 1 | 0 | 0 | 0 | Other |
| equal-not.js | 17 | 0 | 0 | 0 | Frontend |
| equal-not.js.map | 1 | 0 | 0 | 0 | Other |
| equal-square.js | 9 | 0 | 0 | 0 | Frontend |
| equal-square.js.map | 1 | 0 | 0 | 0 | Other |
| equal.js | 16 | 0 | 0 | 0 | Frontend |
| equal.js.map | 1 | 0 | 0 | 0 | Other |
| eraser.js | 23 | 0 | 0 | 0 | Frontend |
| eraser.js.map | 1 | 0 | 0 | 0 | Other |
| ethernet-port.js | 25 | 0 | 0 | 0 | Frontend |
| ethernet-port.js.map | 1 | 0 | 0 | 0 | Other |
| euro.js | 23 | 0 | 0 | 0 | Frontend |
| euro.js.map | 1 | 0 | 0 | 0 | Other |
| expand.js | 18 | 0 | 0 | 0 | Frontend |
| expand.js.map | 1 | 0 | 0 | 0 | Other |
| external-link.js | 17 | 0 | 0 | 0 | Frontend |
| external-link.js.map | 1 | 0 | 0 | 0 | Other |
| eye-closed.js | 19 | 0 | 0 | 0 | Frontend |
| eye-closed.js.map | 1 | 0 | 0 | 0 | Other |
| eye-off.js | 30 | 0 | 0 | 0 | Frontend |
| eye-off.js.map | 1 | 0 | 0 | 0 | Other |
| eye.js | 22 | 0 | 0 | 0 | Frontend |
| eye.js.map | 1 | 0 | 0 | 0 | Other |
| facebook.js | 18 | 0 | 0 | 0 | Frontend |
| facebook.js.map | 1 | 0 | 0 | 0 | Other |
| factory.js | 24 | 0 | 0 | 0 | Frontend |
| factory.js.map | 1 | 0 | 0 | 0 | Other |
| fan.js | 22 | 0 | 0 | 0 | Frontend |
| fan.js.map | 1 | 0 | 0 | 0 | Other |
| fast-forward.js | 16 | 0 | 0 | 0 | Frontend |
| fast-forward.js.map | 1 | 0 | 0 | 0 | Other |
| feather.js | 23 | 0 | 0 | 0 | Frontend |
| feather.js.map | 1 | 0 | 0 | 0 | Other |
| fence.js | 21 | 0 | 0 | 0 | Frontend |
| fence.js.map | 1 | 0 | 0 | 0 | Other |
| ferris-wheel.js | 23 | 0 | 0 | 0 | Frontend |
| ferris-wheel.js.map | 1 | 0 | 0 | 0 | Other |
| figma.js | 19 | 0 | 0 | 0 | Frontend |
| figma.js.map | 1 | 0 | 0 | 0 | Other |
| file-archive.js | 23 | 0 | 0 | 0 | Frontend |
| file-archive.js.map | 1 | 0 | 0 | 0 | Other |
| file-audio-2.js | 19 | 0 | 0 | 0 | Frontend |
| file-audio-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-audio.js | 23 | 0 | 0 | 0 | Frontend |
| file-audio.js.map | 1 | 0 | 0 | 0 | Other |
| file-axis-3-d.js | 9 | 0 | 0 | 0 | Frontend |
| file-axis-3-d.js.map | 1 | 0 | 0 | 0 | Other |
| file-axis-3d.js | 18 | 0 | 0 | 0 | Frontend |
| file-axis-3d.js.map | 1 | 0 | 0 | 0 | Other |
| file-badge-2.js | 18 | 0 | 0 | 0 | Frontend |
| file-badge-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-badge.js | 18 | 0 | 0 | 0 | Frontend |
| file-badge.js.map | 1 | 0 | 0 | 0 | Other |
| file-bar-chart-2.js | 9 | 0 | 0 | 0 | Frontend |
| file-bar-chart-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-bar-chart.js | 9 | 0 | 0 | 0 | Frontend |
| file-bar-chart.js.map | 1 | 0 | 0 | 0 | Other |
| file-box.js | 25 | 0 | 0 | 0 | Frontend |
| file-box.js.map | 1 | 0 | 0 | 0 | Other |
| file-chart-column-increasing.js | 19 | 0 | 0 | 0 | Frontend |
| file-chart-column-increasing.js.map | 1 | 0 | 0 | 0 | Other |
| file-chart-column.js | 19 | 0 | 0 | 0 | Frontend |
| file-chart-column.js.map | 1 | 0 | 0 | 0 | Other |
| file-chart-line.js | 17 | 0 | 0 | 0 | Frontend |
| file-chart-line.js.map | 1 | 0 | 0 | 0 | Other |
| file-chart-pie.js | 24 | 0 | 0 | 0 | Frontend |
| file-chart-pie.js.map | 1 | 0 | 0 | 0 | Other |
| file-check-2.js | 17 | 0 | 0 | 0 | Frontend |
| file-check-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-check.js | 17 | 0 | 0 | 0 | Frontend |
| file-check.js.map | 1 | 0 | 0 | 0 | Other |
| file-clock.js | 18 | 0 | 0 | 0 | Frontend |
| file-clock.js.map | 1 | 0 | 0 | 0 | Other |
| file-code-2.js | 18 | 0 | 0 | 0 | Frontend |
| file-code-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-code.js | 18 | 0 | 0 | 0 | Frontend |
| file-code.js.map | 1 | 0 | 0 | 0 | Other |
| file-cog-2.js | 9 | 0 | 0 | 0 | Frontend |
| file-cog-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-cog.js | 31 | 0 | 0 | 0 | Frontend |
| file-cog.js.map | 1 | 0 | 0 | 0 | Other |
| file-diff.js | 18 | 0 | 0 | 0 | Frontend |
| file-diff.js.map | 1 | 0 | 0 | 0 | Other |
| file-digit.js | 19 | 0 | 0 | 0 | Frontend |
| file-digit.js.map | 1 | 0 | 0 | 0 | Other |
| file-down.js | 18 | 0 | 0 | 0 | Frontend |
| file-down.js.map | 1 | 0 | 0 | 0 | Other |
| file-edit.js | 9 | 0 | 0 | 0 | Frontend |
| file-edit.js.map | 1 | 0 | 0 | 0 | Other |
| file-heart.js | 23 | 0 | 0 | 0 | Frontend |
| file-heart.js.map | 1 | 0 | 0 | 0 | Other |
| file-image.js | 18 | 0 | 0 | 0 | Frontend |
| file-image.js.map | 1 | 0 | 0 | 0 | Other |
| file-input.js | 18 | 0 | 0 | 0 | Frontend |
| file-input.js.map | 1 | 0 | 0 | 0 | Other |
| file-json-2.js | 24 | 0 | 0 | 0 | Frontend |
| file-json-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-json.js | 24 | 0 | 0 | 0 | Frontend |
| file-json.js.map | 1 | 0 | 0 | 0 | Other |
| file-key-2.js | 19 | 0 | 0 | 0 | Frontend |
| file-key-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-key.js | 18 | 0 | 0 | 0 | Frontend |
| file-key.js.map | 1 | 0 | 0 | 0 | Other |
| file-line-chart.js | 9 | 0 | 0 | 0 | Frontend |
| file-line-chart.js.map | 1 | 0 | 0 | 0 | Other |
| file-lock-2.js | 18 | 0 | 0 | 0 | Frontend |
| file-lock-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-lock.js | 17 | 0 | 0 | 0 | Frontend |
| file-lock.js.map | 1 | 0 | 0 | 0 | Other |
| file-minus-2.js | 17 | 0 | 0 | 0 | Frontend |
| file-minus-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-minus.js | 17 | 0 | 0 | 0 | Frontend |
| file-minus.js.map | 1 | 0 | 0 | 0 | Other |
| file-music.js | 18 | 0 | 0 | 0 | Frontend |
| file-music.js.map | 1 | 0 | 0 | 0 | Other |
| file-output.js | 19 | 0 | 0 | 0 | Frontend |
| file-output.js.map | 1 | 0 | 0 | 0 | Other |
| file-pen-line.js | 29 | 0 | 0 | 0 | Frontend |
| file-pen-line.js.map | 1 | 0 | 0 | 0 | Other |
| file-pen.js | 23 | 0 | 0 | 0 | Frontend |
| file-pen.js.map | 1 | 0 | 0 | 0 | Other |
| file-pie-chart.js | 9 | 0 | 0 | 0 | Frontend |
| file-pie-chart.js.map | 1 | 0 | 0 | 0 | Other |
| file-plus-2.js | 18 | 0 | 0 | 0 | Frontend |
| file-plus-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-plus.js | 18 | 0 | 0 | 0 | Frontend |
| file-plus.js.map | 1 | 0 | 0 | 0 | Other |
| file-question.js | 17 | 0 | 0 | 0 | Frontend |
| file-question.js.map | 1 | 0 | 0 | 0 | Other |
| file-scan.js | 20 | 0 | 0 | 0 | Frontend |
| file-scan.js.map | 1 | 0 | 0 | 0 | Other |
| file-search-2.js | 18 | 0 | 0 | 0 | Frontend |
| file-search-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-search.js | 21 | 0 | 0 | 0 | Frontend |
| file-search.js.map | 1 | 0 | 0 | 0 | Other |
| file-signature.js | 9 | 0 | 0 | 0 | Frontend |
| file-signature.js.map | 1 | 0 | 0 | 0 | Other |
| file-sliders.js | 20 | 0 | 0 | 0 | Frontend |
| file-sliders.js.map | 1 | 0 | 0 | 0 | Other |
| file-spreadsheet.js | 20 | 0 | 0 | 0 | Frontend |
| file-spreadsheet.js.map | 1 | 0 | 0 | 0 | Other |
| file-stack.js | 24 | 0 | 0 | 0 | Frontend |
| file-stack.js.map | 1 | 0 | 0 | 0 | Other |
| file-symlink.js | 23 | 0 | 0 | 0 | Frontend |
| file-symlink.js.map | 1 | 0 | 0 | 0 | Other |
| file-terminal.js | 18 | 0 | 0 | 0 | Frontend |
| file-terminal.js.map | 1 | 0 | 0 | 0 | Other |
| file-text.js | 19 | 0 | 0 | 0 | Frontend |
| file-text.js.map | 1 | 0 | 0 | 0 | Other |
| file-type-2.js | 19 | 0 | 0 | 0 | Frontend |
| file-type-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-type.js | 19 | 0 | 0 | 0 | Frontend |
| file-type.js.map | 1 | 0 | 0 | 0 | Other |
| file-up.js | 18 | 0 | 0 | 0 | Frontend |
| file-up.js.map | 1 | 0 | 0 | 0 | Other |
| file-user.js | 18 | 0 | 0 | 0 | Frontend |
| file-user.js.map | 1 | 0 | 0 | 0 | Other |
| file-video-2.js | 18 | 0 | 0 | 0 | Frontend |
| file-video-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-video.js | 17 | 0 | 0 | 0 | Frontend |
| file-video.js.map | 1 | 0 | 0 | 0 | Other |
| file-volume-2.js | 19 | 0 | 0 | 0 | Frontend |
| file-volume-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-volume.js | 27 | 0 | 0 | 0 | Frontend |
| file-volume.js.map | 1 | 0 | 0 | 0 | Other |
| file-warning.js | 17 | 0 | 0 | 0 | Frontend |
| file-warning.js.map | 1 | 0 | 0 | 0 | Other |
| file-x-2.js | 18 | 0 | 0 | 0 | Frontend |
| file-x-2.js.map | 1 | 0 | 0 | 0 | Other |
| file-x.js | 18 | 0 | 0 | 0 | Frontend |
| file-x.js.map | 1 | 0 | 0 | 0 | Other |
| file.js | 16 | 0 | 0 | 0 | Frontend |
| file.js.map | 1 | 0 | 0 | 0 | Other |
| files.js | 17 | 0 | 0 | 0 | Frontend |
| files.js.map | 1 | 0 | 0 | 0 | Other |
| film.js | 22 | 0 | 0 | 0 | Frontend |
| film.js.map | 1 | 0 | 0 | 0 | Other |
| filter-x.js | 17 | 0 | 0 | 0 | Frontend |
| filter-x.js.map | 1 | 0 | 0 | 0 | Other |
| filter.js | 15 | 0 | 0 | 0 | Frontend |
| filter.js.map | 1 | 0 | 0 | 0 | Other |
| fingerprint.js | 23 | 0 | 0 | 0 | Frontend |
| fingerprint.js.map | 1 | 0 | 0 | 0 | Other |
| fire-extinguisher.js | 20 | 0 | 0 | 0 | Frontend |
| fire-extinguisher.js.map | 1 | 0 | 0 | 0 | Other |
| fish-off.js | 35 | 0 | 0 | 0 | Frontend |
| fish-off.js.map | 1 | 0 | 0 | 0 | Other |
| fish-symbol.js | 15 | 0 | 0 | 0 | Frontend |
| fish-symbol.js.map | 1 | 0 | 0 | 0 | Other |
| fish.js | 38 | 0 | 0 | 0 | Frontend |
| fish.js.map | 1 | 0 | 0 | 0 | Other |
| flag-off.js | 18 | 0 | 0 | 0 | Frontend |
| flag-off.js.map | 1 | 0 | 0 | 0 | Other |
| flag-triangle-left.js | 15 | 0 | 0 | 0 | Frontend |
| flag-triangle-left.js.map | 1 | 0 | 0 | 0 | Other |
| flag-triangle-right.js | 15 | 0 | 0 | 0 | Frontend |
| flag-triangle-right.js.map | 1 | 0 | 0 | 0 | Other |
| flag.js | 16 | 0 | 0 | 0 | Frontend |
| flag.js.map | 1 | 0 | 0 | 0 | Other |
| flame-kindling.js | 23 | 0 | 0 | 0 | Frontend |
| flame-kindling.js.map | 1 | 0 | 0 | 0 | Other |
| flame.js | 21 | 0 | 0 | 0 | Frontend |
| flame.js.map | 1 | 0 | 0 | 0 | Other |
| flashlight-off.js | 18 | 0 | 0 | 0 | Frontend |
| flashlight-off.js.map | 1 | 0 | 0 | 0 | Other |
| flashlight.js | 23 | 0 | 0 | 0 | Frontend |
| flashlight.js.map | 1 | 0 | 0 | 0 | Other |
| flask-conical-off.js | 20 | 0 | 0 | 0 | Frontend |
| flask-conical-off.js.map | 1 | 0 | 0 | 0 | Other |
| flask-conical.js | 23 | 0 | 0 | 0 | Frontend |
| flask-conical.js.map | 1 | 0 | 0 | 0 | Other |
| flask-round.js | 17 | 0 | 0 | 0 | Frontend |
| flask-round.js.map | 1 | 0 | 0 | 0 | Other |
| flip-horizontal-2.js | 20 | 0 | 0 | 0 | Frontend |
| flip-horizontal-2.js.map | 1 | 0 | 0 | 0 | Other |
| flip-horizontal.js | 20 | 0 | 0 | 0 | Frontend |
| flip-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| flip-vertical-2.js | 20 | 0 | 0 | 0 | Frontend |
| flip-vertical-2.js.map | 1 | 0 | 0 | 0 | Other |
| flip-vertical.js | 20 | 0 | 0 | 0 | Frontend |
| flip-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| flower-2.js | 25 | 0 | 0 | 0 | Frontend |
| flower-2.js.map | 1 | 0 | 0 | 0 | Other |
| flower.js | 30 | 0 | 0 | 0 | Frontend |
| flower.js.map | 1 | 0 | 0 | 0 | Other |
| focus.js | 19 | 0 | 0 | 0 | Frontend |
| focus.js.map | 1 | 0 | 0 | 0 | Other |
| fold-horizontal.js | 22 | 0 | 0 | 0 | Frontend |
| fold-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| fold-vertical.js | 22 | 0 | 0 | 0 | Frontend |
| fold-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| folder-archive.js | 24 | 0 | 0 | 0 | Frontend |
| folder-archive.js.map | 1 | 0 | 0 | 0 | Other |
| folder-check.js | 22 | 0 | 0 | 0 | Frontend |
| folder-check.js.map | 1 | 0 | 0 | 0 | Other |
| folder-clock.js | 23 | 0 | 0 | 0 | Frontend |
| folder-clock.js.map | 1 | 0 | 0 | 0 | Other |
| folder-closed.js | 22 | 0 | 0 | 0 | Frontend |
| folder-closed.js.map | 1 | 0 | 0 | 0 | Other |
| folder-code.js | 23 | 0 | 0 | 0 | Frontend |
| folder-code.js.map | 1 | 0 | 0 | 0 | Other |
| folder-cog-2.js | 9 | 0 | 0 | 0 | Frontend |
| folder-cog-2.js.map | 1 | 0 | 0 | 0 | Other |
| folder-cog.js | 30 | 0 | 0 | 0 | Frontend |
| folder-cog.js.map | 1 | 0 | 0 | 0 | Other |
| folder-dot.js | 22 | 0 | 0 | 0 | Frontend |
| folder-dot.js.map | 1 | 0 | 0 | 0 | Other |
| folder-down.js | 23 | 0 | 0 | 0 | Frontend |
| folder-down.js.map | 1 | 0 | 0 | 0 | Other |
| folder-edit.js | 9 | 0 | 0 | 0 | Frontend |
| folder-edit.js.map | 1 | 0 | 0 | 0 | Other |
| folder-git-2.js | 24 | 0 | 0 | 0 | Frontend |
| folder-git-2.js.map | 1 | 0 | 0 | 0 | Other |
| folder-git.js | 24 | 0 | 0 | 0 | Frontend |
| folder-git.js.map | 1 | 0 | 0 | 0 | Other |
| folder-heart.js | 28 | 0 | 0 | 0 | Frontend |
| folder-heart.js.map | 1 | 0 | 0 | 0 | Other |
| folder-input.js | 23 | 0 | 0 | 0 | Frontend |
| folder-input.js.map | 1 | 0 | 0 | 0 | Other |
| folder-kanban.js | 24 | 0 | 0 | 0 | Frontend |
| folder-kanban.js.map | 1 | 0 | 0 | 0 | Other |
| folder-key.js | 24 | 0 | 0 | 0 | Frontend |
| folder-key.js.map | 1 | 0 | 0 | 0 | Other |
| folder-lock.js | 23 | 0 | 0 | 0 | Frontend |
| folder-lock.js.map | 1 | 0 | 0 | 0 | Other |
| folder-minus.js | 22 | 0 | 0 | 0 | Frontend |
| folder-minus.js.map | 1 | 0 | 0 | 0 | Other |
| folder-open-dot.js | 22 | 0 | 0 | 0 | Frontend |
| folder-open-dot.js.map | 1 | 0 | 0 | 0 | Other |
| folder-open.js | 21 | 0 | 0 | 0 | Frontend |
| folder-open.js.map | 1 | 0 | 0 | 0 | Other |
| folder-output.js | 23 | 0 | 0 | 0 | Frontend |
| folder-output.js.map | 1 | 0 | 0 | 0 | Other |
| folder-pen.js | 28 | 0 | 0 | 0 | Frontend |
| folder-pen.js.map | 1 | 0 | 0 | 0 | Other |
| folder-plus.js | 23 | 0 | 0 | 0 | Frontend |
| folder-plus.js.map | 1 | 0 | 0 | 0 | Other |
| folder-root.js | 23 | 0 | 0 | 0 | Frontend |
| folder-root.js.map | 1 | 0 | 0 | 0 | Other |
| folder-search-2.js | 23 | 0 | 0 | 0 | Frontend |
| folder-search-2.js.map | 1 | 0 | 0 | 0 | Other |
| folder-search.js | 23 | 0 | 0 | 0 | Frontend |
| folder-search.js.map | 1 | 0 | 0 | 0 | Other |
| folder-symlink.js | 22 | 0 | 0 | 0 | Frontend |
| folder-symlink.js.map | 1 | 0 | 0 | 0 | Other |
| folder-sync.js | 25 | 0 | 0 | 0 | Frontend |
| folder-sync.js.map | 1 | 0 | 0 | 0 | Other |
| folder-tree.js | 30 | 0 | 0 | 0 | Frontend |
| folder-tree.js.map | 1 | 0 | 0 | 0 | Other |
| folder-up.js | 23 | 0 | 0 | 0 | Frontend |
| folder-up.js.map | 1 | 0 | 0 | 0 | Other |
| folder-x.js | 23 | 0 | 0 | 0 | Frontend |
| folder-x.js.map | 1 | 0 | 0 | 0 | Other |
| folder.js | 21 | 0 | 0 | 0 | Frontend |
| folder.js.map | 1 | 0 | 0 | 0 | Other |
| folders.js | 22 | 0 | 0 | 0 | Frontend |
| folders.js.map | 1 | 0 | 0 | 0 | Other |
| footprints.js | 30 | 0 | 0 | 0 | Frontend |
| footprints.js.map | 1 | 0 | 0 | 0 | Other |
| fork-knife-crossed.js | 9 | 0 | 0 | 0 | Frontend |
| fork-knife-crossed.js.map | 1 | 0 | 0 | 0 | Other |
| fork-knife.js | 9 | 0 | 0 | 0 | Frontend |
| fork-knife.js.map | 1 | 0 | 0 | 0 | Other |
| forklift.js | 18 | 0 | 0 | 0 | Frontend |
| forklift.js.map | 1 | 0 | 0 | 0 | Other |
| form-input.js | 9 | 0 | 0 | 0 | Frontend |
| form-input.js.map | 1 | 0 | 0 | 0 | Other |
| forward.js | 16 | 0 | 0 | 0 | Frontend |
| forward.js.map | 1 | 0 | 0 | 0 | Other |
| frame.js | 18 | 0 | 0 | 0 | Frontend |
| frame.js.map | 1 | 0 | 0 | 0 | Other |
| framer.js | 15 | 0 | 0 | 0 | Frontend |
| framer.js.map | 1 | 0 | 0 | 0 | Other |
| frown.js | 18 | 0 | 0 | 0 | Frontend |
| frown.js.map | 1 | 0 | 0 | 0 | Other |
| fuel.js | 24 | 0 | 0 | 0 | Frontend |
| fuel.js.map | 1 | 0 | 0 | 0 | Other |
| fullscreen.js | 19 | 0 | 0 | 0 | Frontend |
| fullscreen.js.map | 1 | 0 | 0 | 0 | Other |
| function-square.js | 9 | 0 | 0 | 0 | Frontend |
| function-square.js.map | 1 | 0 | 0 | 0 | Other |
| gallery-horizontal-end.js | 17 | 0 | 0 | 0 | Frontend |
| gallery-horizontal-end.js.map | 1 | 0 | 0 | 0 | Other |
| gallery-horizontal.js | 17 | 0 | 0 | 0 | Frontend |
| gallery-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| gallery-thumbnails.js | 19 | 0 | 0 | 0 | Frontend |
| gallery-thumbnails.js.map | 1 | 0 | 0 | 0 | Other |
| gallery-vertical-end.js | 17 | 0 | 0 | 0 | Frontend |
| gallery-vertical-end.js.map | 1 | 0 | 0 | 0 | Other |
| gallery-vertical.js | 17 | 0 | 0 | 0 | Frontend |
| gallery-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| gamepad-2.js | 25 | 0 | 0 | 0 | Frontend |
| gamepad-2.js.map | 1 | 0 | 0 | 0 | Other |
| gamepad.js | 19 | 0 | 0 | 0 | Frontend |
| gamepad.js.map | 1 | 0 | 0 | 0 | Other |
| gantt-chart-square.js | 9 | 0 | 0 | 0 | Frontend |
| gantt-chart-square.js.map | 1 | 0 | 0 | 0 | Other |
| gantt-chart.js | 9 | 0 | 0 | 0 | Frontend |
| gantt-chart.js.map | 1 | 0 | 0 | 0 | Other |
| gauge-circle.js | 9 | 0 | 0 | 0 | Frontend |
| gauge-circle.js.map | 1 | 0 | 0 | 0 | Other |
| gauge.js | 16 | 0 | 0 | 0 | Frontend |
| gauge.js.map | 1 | 0 | 0 | 0 | Other |
| gavel.js | 19 | 0 | 0 | 0 | Frontend |
| gavel.js.map | 1 | 0 | 0 | 0 | Other |
| gem.js | 17 | 0 | 0 | 0 | Frontend |
| gem.js.map | 1 | 0 | 0 | 0 | Other |
| ghost.js | 23 | 0 | 0 | 0 | Frontend |
| ghost.js.map | 1 | 0 | 0 | 0 | Other |
| gift.js | 24 | 0 | 0 | 0 | Frontend |
| gift.js.map | 1 | 0 | 0 | 0 | Other |
| git-branch-plus.js | 20 | 0 | 0 | 0 | Frontend |
| git-branch-plus.js.map | 1 | 0 | 0 | 0 | Other |
| git-branch.js | 18 | 0 | 0 | 0 | Frontend |
| git-branch.js.map | 1 | 0 | 0 | 0 | Other |
| git-commit-horizontal.js | 17 | 0 | 0 | 0 | Frontend |
| git-commit-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| git-commit-vertical.js | 17 | 0 | 0 | 0 | Frontend |
| git-commit-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| git-commit.js | 9 | 0 | 0 | 0 | Frontend |
| git-commit.js.map | 1 | 0 | 0 | 0 | Other |
| git-compare-arrows.js | 20 | 0 | 0 | 0 | Frontend |
| git-compare-arrows.js.map | 1 | 0 | 0 | 0 | Other |
| git-compare.js | 18 | 0 | 0 | 0 | Frontend |
| git-compare.js.map | 1 | 0 | 0 | 0 | Other |
| git-fork.js | 19 | 0 | 0 | 0 | Frontend |
| git-fork.js.map | 1 | 0 | 0 | 0 | Other |
| git-graph.js | 20 | 0 | 0 | 0 | Frontend |
| git-graph.js.map | 1 | 0 | 0 | 0 | Other |
| git-merge.js | 17 | 0 | 0 | 0 | Frontend |
| git-merge.js.map | 1 | 0 | 0 | 0 | Other |
| git-pull-request-arrow.js | 19 | 0 | 0 | 0 | Frontend |
| git-pull-request-arrow.js.map | 1 | 0 | 0 | 0 | Other |
| git-pull-request-closed.js | 20 | 0 | 0 | 0 | Frontend |
| git-pull-request-closed.js.map | 1 | 0 | 0 | 0 | Other |
| git-pull-request-create-arrow.js | 20 | 0 | 0 | 0 | Frontend |
| git-pull-request-create-arrow.js.map | 1 | 0 | 0 | 0 | Other |
| git-pull-request-create.js | 19 | 0 | 0 | 0 | Frontend |
| git-pull-request-create.js.map | 1 | 0 | 0 | 0 | Other |
| git-pull-request-draft.js | 19 | 0 | 0 | 0 | Frontend |
| git-pull-request-draft.js.map | 1 | 0 | 0 | 0 | Other |
| git-pull-request.js | 18 | 0 | 0 | 0 | Frontend |
| git-pull-request.js.map | 1 | 0 | 0 | 0 | Other |
| github.js | 22 | 0 | 0 | 0 | Frontend |
| github.js.map | 1 | 0 | 0 | 0 | CI/CD |
| gitlab.js | 21 | 0 | 0 | 0 | Frontend |
| gitlab.js.map | 1 | 0 | 0 | 0 | CI/CD |
| glass-water.js | 22 | 0 | 0 | 0 | Frontend |
| glass-water.js.map | 1 | 0 | 0 | 0 | Other |
| glasses.js | 19 | 0 | 0 | 0 | Frontend |
| glasses.js.map | 1 | 0 | 0 | 0 | Other |
| globe-2.js | 9 | 0 | 0 | 0 | Frontend |
| globe-2.js.map | 1 | 0 | 0 | 0 | Other |
| globe-lock.js | 24 | 0 | 0 | 0 | Frontend |
| globe-lock.js.map | 1 | 0 | 0 | 0 | Other |
| globe.js | 17 | 0 | 0 | 0 | Frontend |
| globe.js.map | 1 | 0 | 0 | 0 | Other |
| goal.js | 17 | 0 | 0 | 0 | Frontend |
| goal.js.map | 1 | 0 | 0 | 0 | Other |
| grab.js | 22 | 0 | 0 | 0 | Frontend |
| grab.js.map | 1 | 0 | 0 | 0 | Other |
| graduation-cap.js | 23 | 0 | 0 | 0 | Frontend |
| graduation-cap.js.map | 1 | 0 | 0 | 0 | Other |
| grape.js | 23 | 0 | 0 | 0 | Frontend |
| grape.js.map | 1 | 0 | 0 | 0 | Other |
| grid-2-x-2-plus.js | 9 | 0 | 0 | 0 | Frontend |
| grid-2-x-2-plus.js.map | 1 | 0 | 0 | 0 | Other |
| grid-2-x-2.js | 9 | 0 | 0 | 0 | Frontend |
| grid-2-x-2.js.map | 1 | 0 | 0 | 0 | Other |
| grid-2x2-check.js | 22 | 0 | 0 | 0 | Frontend |
| grid-2x2-check.js.map | 1 | 0 | 0 | 0 | Other |
| grid-2x2-plus.js | 23 | 0 | 0 | 0 | Frontend |
| grid-2x2-plus.js.map | 1 | 0 | 0 | 0 | Other |
| grid-2x2-x.js | 23 | 0 | 0 | 0 | Frontend |
| grid-2x2-x.js.map | 1 | 0 | 0 | 0 | Other |
| grid-2x2.js | 17 | 0 | 0 | 0 | Frontend |
| grid-2x2.js.map | 1 | 0 | 0 | 0 | Other |
| grid-3-x-3.js | 9 | 0 | 0 | 0 | Frontend |
| grid-3-x-3.js.map | 1 | 0 | 0 | 0 | Other |
| grid-3x3.js | 19 | 0 | 0 | 0 | Frontend |
| grid-3x3.js.map | 1 | 0 | 0 | 0 | Other |
| grid.js | 9 | 0 | 0 | 0 | Frontend |
| grid.js.map | 1 | 0 | 0 | 0 | Other |
| grip-horizontal.js | 20 | 0 | 0 | 0 | Frontend |
| grip-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| grip-vertical.js | 20 | 0 | 0 | 0 | Frontend |
| grip-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| grip.js | 23 | 0 | 0 | 0 | Frontend |
| grip.js.map | 1 | 0 | 0 | 0 | Other |
| group.js | 20 | 0 | 0 | 0 | Frontend |
| group.js.map | 1 | 0 | 0 | 0 | Other |
| guitar.js | 31 | 0 | 0 | 0 | Frontend |
| guitar.js.map | 1 | 0 | 0 | 0 | Other |
| ham.js | 30 | 0 | 0 | 0 | Frontend |
| ham.js.map | 1 | 0 | 0 | 0 | Other |
| hammer.js | 23 | 0 | 0 | 0 | Frontend |
| hammer.js.map | 1 | 0 | 0 | 0 | Other |
| hand-coins.js | 25 | 0 | 0 | 0 | Frontend |
| hand-coins.js.map | 1 | 0 | 0 | 0 | Other |
| hand-heart.js | 30 | 0 | 0 | 0 | Frontend |
| hand-heart.js.map | 1 | 0 | 0 | 0 | Other |
| hand-helping.js | 23 | 0 | 0 | 0 | Frontend |
| hand-helping.js.map | 1 | 0 | 0 | 0 | Other |
| hand-metal.js | 24 | 0 | 0 | 0 | Frontend |
| hand-metal.js.map | 1 | 0 | 0 | 0 | Other |
| hand-platter.js | 26 | 0 | 0 | 0 | Frontend |
| hand-platter.js.map | 1 | 0 | 0 | 0 | Other |
| hand.js | 24 | 0 | 0 | 0 | Frontend |
| hand.js.map | 1 | 0 | 0 | 0 | Other |
| handshake.js | 25 | 0 | 0 | 0 | Frontend |
| handshake.js.map | 1 | 0 | 0 | 0 | Other |
| hard-drive-download.js | 19 | 0 | 0 | 0 | Frontend |
| hard-drive-download.js.map | 1 | 0 | 0 | 0 | Other |
| hard-drive-upload.js | 19 | 0 | 0 | 0 | Frontend |
| hard-drive-upload.js.map | 1 | 0 | 0 | 0 | Other |
| hard-drive.js | 24 | 0 | 0 | 0 | Frontend |
| hard-drive.js.map | 1 | 0 | 0 | 0 | Other |
| hard-hat.js | 18 | 0 | 0 | 0 | Frontend |
| hard-hat.js.map | 1 | 0 | 0 | 0 | Other |
| hash.js | 18 | 0 | 0 | 0 | Frontend |
| hash.js.map | 1 | 0 | 0 | 0 | Other |
| haze.js | 22 | 0 | 0 | 0 | Frontend |
| haze.js.map | 1 | 0 | 0 | 0 | Other |
| hdmi-port.js | 22 | 0 | 0 | 0 | Frontend |
| hdmi-port.js.map | 1 | 0 | 0 | 0 | Other |
| heading-1.js | 18 | 0 | 0 | 0 | Frontend |
| heading-1.js.map | 1 | 0 | 0 | 0 | Other |
| heading-2.js | 18 | 0 | 0 | 0 | Frontend |
| heading-2.js.map | 1 | 0 | 0 | 0 | Other |
| heading-3.js | 19 | 0 | 0 | 0 | Frontend |
| heading-3.js.map | 1 | 0 | 0 | 0 | Other |
| heading-4.js | 19 | 0 | 0 | 0 | Frontend |
| heading-4.js.map | 1 | 0 | 0 | 0 | Other |
| heading-5.js | 22 | 0 | 0 | 0 | Frontend |
| heading-5.js.map | 1 | 0 | 0 | 0 | Other |
| heading-6.js | 19 | 0 | 0 | 0 | Frontend |
| heading-6.js.map | 1 | 0 | 0 | 0 | Other |
| heading.js | 17 | 0 | 0 | 0 | Frontend |
| heading.js.map | 1 | 0 | 0 | 0 | Other |
| headphone-off.js | 25 | 0 | 0 | 0 | Frontend |
| headphone-off.js.map | 1 | 0 | 0 | 0 | Other |
| headphones.js | 21 | 0 | 0 | 0 | Frontend |
| headphones.js.map | 1 | 0 | 0 | 0 | Other |
| headset.js | 22 | 0 | 0 | 0 | Frontend |
| headset.js.map | 1 | 0 | 0 | 0 | Other |
| heart-crack.js | 22 | 0 | 0 | 0 | Frontend |
| heart-crack.js.map | 1 | 0 | 0 | 0 | Other |
| heart-handshake.js | 30 | 0 | 0 | 0 | Frontend |
| heart-handshake.js.map | 1 | 0 | 0 | 0 | Other |
| heart-off.js | 26 | 0 | 0 | 0 | Frontend |
| heart-off.js.map | 1 | 0 | 0 | 0 | Other |
| heart-pulse.js | 22 | 0 | 0 | 0 | Frontend |
| heart-pulse.js.map | 1 | 0 | 0 | 0 | Other |
| heart.js | 21 | 0 | 0 | 0 | Frontend |
| heart.js.map | 1 | 0 | 0 | 0 | Other |
| heater.js | 27 | 0 | 0 | 0 | Frontend |
| heater.js.map | 1 | 0 | 0 | 0 | Other |
| help-circle.js | 9 | 0 | 0 | 0 | Frontend |
| help-circle.js.map | 1 | 0 | 0 | 0 | Other |
| helping-hand.js | 9 | 0 | 0 | 0 | Frontend |
| helping-hand.js.map | 1 | 0 | 0 | 0 | Other |
| hexagon.js | 21 | 0 | 0 | 0 | Frontend |
| hexagon.js.map | 1 | 0 | 0 | 0 | Other |
| highlighter.js | 16 | 0 | 0 | 0 | Frontend |
| highlighter.js.map | 1 | 0 | 0 | 0 | Other |
| history.js | 17 | 0 | 0 | 0 | Frontend |
| history.js.map | 1 | 0 | 0 | 0 | Other |
| home.js | 9 | 0 | 0 | 0 | Frontend |
| home.js.map | 1 | 0 | 0 | 0 | Other |
| hop-off.js | 53 | 0 | 0 | 0 | Frontend |
| hop-off.js.map | 1 | 0 | 0 | 0 | Other |
| hop.js | 64 | 0 | 0 | 0 | Frontend |
| hop.js.map | 1 | 0 | 0 | 0 | Other |
| hospital.js | 26 | 0 | 0 | 0 | Frontend |
| hospital.js.map | 1 | 0 | 0 | 0 | Other |
| hotel.js | 24 | 0 | 0 | 0 | Frontend |
| hotel.js.map | 1 | 0 | 0 | 0 | Other |
| hourglass.js | 27 | 0 | 0 | 0 | Frontend |
| hourglass.js.map | 1 | 0 | 0 | 0 | Other |
| house-plug.js | 27 | 0 | 0 | 0 | Frontend |
| house-plug.js.map | 1 | 0 | 0 | 0 | Other |
| house-plus.js | 24 | 0 | 0 | 0 | Frontend |
| house-plus.js.map | 1 | 0 | 0 | 0 | Other |
| house.js | 22 | 0 | 0 | 0 | Frontend |
| house.js.map | 1 | 0 | 0 | 0 | Other |
| ice-cream-2.js | 9 | 0 | 0 | 0 | Frontend |
| ice-cream-2.js.map | 1 | 0 | 0 | 0 | Other |
| ice-cream-bowl.js | 23 | 0 | 0 | 0 | Frontend |
| ice-cream-bowl.js.map | 1 | 0 | 0 | 0 | Other |
| ice-cream-cone.js | 17 | 0 | 0 | 0 | Frontend |
| ice-cream-cone.js.map | 1 | 0 | 0 | 0 | Other |
| ice-cream.js | 9 | 0 | 0 | 0 | Frontend |
| ice-cream.js.map | 1 | 0 | 0 | 0 | Other |
| id-card.js | 19 | 0 | 0 | 0 | Frontend |
| id-card.js.map | 1 | 0 | 0 | 0 | Other |
| image-down.js | 24 | 0 | 0 | 0 | Frontend |
| image-down.js.map | 1 | 0 | 0 | 0 | Other |
| image-minus.js | 18 | 0 | 0 | 0 | Frontend |
| image-minus.js.map | 1 | 0 | 0 | 0 | Other |
| image-off.js | 26 | 0 | 0 | 0 | Frontend |
| image-off.js.map | 1 | 0 | 0 | 0 | Other |
| image-play.js | 24 | 0 | 0 | 0 | Frontend |
| image-play.js.map | 1 | 0 | 0 | 0 | Other |
| image-plus.js | 19 | 0 | 0 | 0 | Frontend |
| image-plus.js.map | 1 | 0 | 0 | 0 | Other |
| image-up.js | 24 | 0 | 0 | 0 | Frontend |
| image-up.js.map | 1 | 0 | 0 | 0 | Other |
| image-upscale.js | 22 | 0 | 0 | 0 | Frontend |
| image-upscale.js.map | 1 | 0 | 0 | 0 | Other |
| image.js | 17 | 0 | 0 | 0 | Frontend |
| image.js.map | 1 | 0 | 0 | 0 | Other |
| images.js | 18 | 0 | 0 | 0 | Frontend |
| images.js.map | 1 | 0 | 0 | 0 | Other |
| import.js | 23 | 0 | 0 | 0 | Frontend |
| import.js.map | 1 | 0 | 0 | 0 | Other |
| inbox.js | 22 | 0 | 0 | 0 | Frontend |
| inbox.js.map | 1 | 0 | 0 | 0 | Other |
| indent-decrease.js | 18 | 0 | 0 | 0 | Frontend |
| indent-decrease.js.map | 1 | 0 | 0 | 0 | Other |
| indent-increase.js | 18 | 0 | 0 | 0 | Frontend |
| indent-increase.js.map | 1 | 0 | 0 | 0 | Other |
| indent.js | 9 | 0 | 0 | 0 | Frontend |
| indent.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1552 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| indian-rupee.js | 19 | 0 | 0 | 0 | Frontend |
| indian-rupee.js.map | 1 | 0 | 0 | 0 | Other |
| infinity.js | 21 | 0 | 0 | 0 | Frontend |
| infinity.js.map | 1 | 0 | 0 | 0 | Other |
| info.js | 17 | 0 | 0 | 0 | Frontend |
| info.js.map | 1 | 0 | 0 | 0 | Other |
| inspect.js | 9 | 0 | 0 | 0 | Frontend |
| inspect.js.map | 1 | 0 | 0 | 0 | Other |
| inspection-panel.js | 19 | 0 | 0 | 0 | Frontend |
| inspection-panel.js.map | 1 | 0 | 0 | 0 | Other |
| instagram.js | 17 | 0 | 0 | 0 | Frontend |
| instagram.js.map | 1 | 0 | 0 | 0 | Other |
| italic.js | 17 | 0 | 0 | 0 | Frontend |
| italic.js.map | 1 | 0 | 0 | 0 | Other |
| iteration-ccw.js | 16 | 0 | 0 | 0 | Frontend |
| iteration-ccw.js.map | 1 | 0 | 0 | 0 | Other |
| iteration-cw.js | 16 | 0 | 0 | 0 | Frontend |
| iteration-cw.js.map | 1 | 0 | 0 | 0 | Other |
| japanese-yen.js | 17 | 0 | 0 | 0 | Frontend |
| japanese-yen.js.map | 1 | 0 | 0 | 0 | Other |
| joystick.js | 24 | 0 | 0 | 0 | Frontend |
| joystick.js.map | 1 | 0 | 0 | 0 | Other |
| kanban-square-dashed.js | 9 | 0 | 0 | 0 | Frontend |
| kanban-square-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| kanban-square.js | 9 | 0 | 0 | 0 | Frontend |
| kanban-square.js.map | 1 | 0 | 0 | 0 | Other |
| kanban.js | 17 | 0 | 0 | 0 | Frontend |
| kanban.js.map | 1 | 0 | 0 | 0 | Other |
| key-round.js | 22 | 0 | 0 | 0 | Frontend |
| key-round.js.map | 1 | 0 | 0 | 0 | Other |
| key-square.js | 29 | 0 | 0 | 0 | Frontend |
| key-square.js.map | 1 | 0 | 0 | 0 | Other |
| key.js | 17 | 0 | 0 | 0 | Frontend |
| key.js.map | 1 | 0 | 0 | 0 | Other |
| keyboard-music.js | 23 | 0 | 0 | 0 | Frontend |
| keyboard-music.js.map | 1 | 0 | 0 | 0 | Other |
| keyboard-off.js | 24 | 0 | 0 | 0 | Frontend |
| keyboard-off.js.map | 1 | 0 | 0 | 0 | Other |
| keyboard.js | 23 | 0 | 0 | 0 | Frontend |
| keyboard.js.map | 1 | 0 | 0 | 0 | Other |
| lamp-ceiling.js | 17 | 0 | 0 | 0 | Frontend |
| lamp-ceiling.js.map | 1 | 0 | 0 | 0 | Other |
| lamp-desk.js | 18 | 0 | 0 | 0 | Frontend |
| lamp-desk.js.map | 1 | 0 | 0 | 0 | Other |
| lamp-floor.js | 17 | 0 | 0 | 0 | Frontend |
| lamp-floor.js.map | 1 | 0 | 0 | 0 | Other |
| lamp-wall-down.js | 17 | 0 | 0 | 0 | Frontend |
| lamp-wall-down.js.map | 1 | 0 | 0 | 0 | Other |
| lamp-wall-up.js | 17 | 0 | 0 | 0 | Frontend |
| lamp-wall-up.js.map | 1 | 0 | 0 | 0 | Other |
| lamp.js | 17 | 0 | 0 | 0 | Frontend |
| lamp.js.map | 1 | 0 | 0 | 0 | Other |
| land-plot.js | 24 | 0 | 0 | 0 | Frontend |
| land-plot.js.map | 1 | 0 | 0 | 0 | Other |
| landmark.js | 20 | 0 | 0 | 0 | Frontend |
| landmark.js.map | 1 | 0 | 0 | 0 | Other |
| languages.js | 20 | 0 | 0 | 0 | Frontend |
| languages.js.map | 1 | 0 | 0 | 0 | Other |
| laptop-2.js | 9 | 0 | 0 | 0 | Frontend |
| laptop-2.js.map | 1 | 0 | 0 | 0 | Other |
| laptop-minimal-check.js | 17 | 0 | 0 | 0 | Frontend |
| laptop-minimal-check.js.map | 1 | 0 | 0 | 0 | Other |
| laptop-minimal.js | 16 | 0 | 0 | 0 | Frontend |
| laptop-minimal.js.map | 1 | 0 | 0 | 0 | Other |
| laptop.js | 21 | 0 | 0 | 0 | Frontend |
| laptop.js.map | 1 | 0 | 0 | 0 | Other |
| lasso-select.js | 31 | 0 | 0 | 0 | Frontend |
| lasso-select.js.map | 1 | 0 | 0 | 0 | Other |
| lasso.js | 23 | 0 | 0 | 0 | Frontend |
| lasso.js.map | 1 | 0 | 0 | 0 | Other |
| laugh.js | 18 | 0 | 0 | 0 | Frontend |
| laugh.js.map | 1 | 0 | 0 | 0 | Other |
| layers-2.js | 28 | 0 | 0 | 0 | Frontend |
| layers-2.js.map | 1 | 0 | 0 | 0 | Other |
| layers-3.js | 9 | 0 | 0 | 0 | Frontend |
| layers-3.js.map | 1 | 0 | 0 | 0 | Other |
| layers.js | 35 | 0 | 0 | 0 | Frontend |
| layers.js.map | 1 | 0 | 0 | 0 | Other |
| layout-dashboard.js | 18 | 0 | 0 | 0 | Frontend |
| layout-dashboard.js.map | 1 | 0 | 0 | 0 | Other |
| layout-grid.js | 18 | 0 | 0 | 0 | Frontend |
| layout-grid.js.map | 1 | 0 | 0 | 0 | Other |
| layout-list.js | 20 | 0 | 0 | 0 | Frontend |
| layout-list.js.map | 1 | 0 | 0 | 0 | Other |
| layout-panel-left.js | 17 | 0 | 0 | 0 | Frontend |
| layout-panel-left.js.map | 1 | 0 | 0 | 0 | Other |
| layout-panel-top.js | 17 | 0 | 0 | 0 | Frontend |
| layout-panel-top.js.map | 1 | 0 | 0 | 0 | Other |
| layout-template.js | 17 | 0 | 0 | 0 | Frontend |
| layout-template.js.map | 1 | 0 | 0 | 0 | Other |
| layout.js | 9 | 0 | 0 | 0 | Frontend |
| layout.js.map | 1 | 0 | 0 | 0 | Other |
| leaf.js | 22 | 0 | 0 | 0 | Frontend |
| leaf.js.map | 1 | 0 | 0 | 0 | Other |
| leafy-green.js | 22 | 0 | 0 | 0 | Frontend |
| leafy-green.js.map | 1 | 0 | 0 | 0 | Other |
| lectern.js | 23 | 0 | 0 | 0 | Frontend |
| lectern.js.map | 1 | 0 | 0 | 0 | Other |
| letter-text.js | 19 | 0 | 0 | 0 | Frontend |
| letter-text.js.map | 1 | 0 | 0 | 0 | Other |
| library-big.js | 23 | 0 | 0 | 0 | Frontend |
| library-big.js.map | 1 | 0 | 0 | 0 | Other |
| library-square.js | 9 | 0 | 0 | 0 | Frontend |
| library-square.js.map | 1 | 0 | 0 | 0 | Other |
| library.js | 18 | 0 | 0 | 0 | Frontend |
| library.js.map | 1 | 0 | 0 | 0 | Other |
| life-buoy.js | 20 | 0 | 0 | 0 | Frontend |
| life-buoy.js.map | 1 | 0 | 0 | 0 | Other |
| ligature.js | 19 | 0 | 0 | 0 | Frontend |
| ligature.js.map | 1 | 0 | 0 | 0 | Other |
| lightbulb-off.js | 19 | 0 | 0 | 0 | Frontend |
| lightbulb-off.js.map | 1 | 0 | 0 | 0 | Other |
| lightbulb.js | 23 | 0 | 0 | 0 | Frontend |
| lightbulb.js.map | 1 | 0 | 0 | 0 | Other |
| line-chart.js | 9 | 0 | 0 | 0 | Frontend |
| line-chart.js.map | 1 | 0 | 0 | 0 | Other |
| link-2-off.js | 18 | 0 | 0 | 0 | Frontend |
| link-2-off.js.map | 1 | 0 | 0 | 0 | Other |
| link-2.js | 17 | 0 | 0 | 0 | Frontend |
| link-2.js.map | 1 | 0 | 0 | 0 | Other |
| link.js | 16 | 0 | 0 | 0 | Frontend |
| link.js.map | 1 | 0 | 0 | 0 | Other |
| linkedin.js | 23 | 0 | 0 | 0 | Frontend |
| linkedin.js.map | 1 | 0 | 0 | 0 | Other |
| list-check.js | 18 | 0 | 0 | 0 | Frontend |
| list-check.js.map | 1 | 0 | 0 | 0 | Other |
| list-checks.js | 19 | 0 | 0 | 0 | Frontend |
| list-checks.js.map | 1 | 0 | 0 | 0 | Other |
| list-collapse.js | 19 | 0 | 0 | 0 | Frontend |
| list-collapse.js.map | 1 | 0 | 0 | 0 | Other |
| list-end.js | 19 | 0 | 0 | 0 | Frontend |
| list-end.js.map | 1 | 0 | 0 | 0 | Other |
| list-filter-plus.js | 19 | 0 | 0 | 0 | Frontend |
| list-filter-plus.js.map | 1 | 0 | 0 | 0 | Other |
| list-filter.js | 17 | 0 | 0 | 0 | Frontend |
| list-filter.js.map | 1 | 0 | 0 | 0 | Other |
| list-minus.js | 18 | 0 | 0 | 0 | Frontend |
| list-minus.js.map | 1 | 0 | 0 | 0 | Other |
| list-music.js | 19 | 0 | 0 | 0 | Frontend |
| list-music.js.map | 1 | 0 | 0 | 0 | Other |
| list-ordered.js | 20 | 0 | 0 | 0 | Frontend |
| list-ordered.js.map | 1 | 0 | 0 | 0 | Other |
| list-plus.js | 19 | 0 | 0 | 0 | Frontend |
| list-plus.js.map | 1 | 0 | 0 | 0 | Other |
| list-restart.js | 25 | 0 | 0 | 0 | Frontend |
| list-restart.js.map | 1 | 0 | 0 | 0 | Other |
| list-start.js | 19 | 0 | 0 | 0 | Frontend |
| list-start.js.map | 1 | 0 | 0 | 0 | Other |
| list-todo.js | 19 | 0 | 0 | 0 | Frontend |
| list-todo.js.map | 1 | 0 | 0 | 0 | Other |
| list-tree.js | 19 | 0 | 0 | 0 | Frontend |
| list-tree.js.map | 1 | 0 | 0 | 0 | Other |
| list-video.js | 18 | 0 | 0 | 0 | Frontend |
| list-video.js.map | 1 | 0 | 0 | 0 | Other |
| list-x.js | 19 | 0 | 0 | 0 | Frontend |
| list-x.js.map | 1 | 0 | 0 | 0 | Other |
| list.js | 20 | 0 | 0 | 0 | Frontend |
| list.js.map | 1 | 0 | 0 | 0 | Other |
| loader-2.js | 9 | 0 | 0 | 0 | Frontend |
| loader-2.js.map | 1 | 0 | 0 | 0 | Other |
| loader-circle.js | 15 | 0 | 0 | 0 | Frontend |
| loader-circle.js.map | 1 | 0 | 0 | 0 | Other |
| loader-pinwheel.js | 18 | 0 | 0 | 0 | Frontend |
| loader-pinwheel.js.map | 1 | 0 | 0 | 0 | Other |
| loader.js | 22 | 0 | 0 | 0 | Frontend |
| loader.js.map | 1 | 0 | 0 | 0 | Other |
| locate-fixed.js | 20 | 0 | 0 | 0 | Frontend |
| locate-fixed.js.map | 1 | 0 | 0 | 0 | Other |
| locate-off.js | 33 | 0 | 0 | 0 | Frontend |
| locate-off.js.map | 1 | 0 | 0 | 0 | Other |
| locate.js | 19 | 0 | 0 | 0 | Frontend |
| locate.js.map | 1 | 0 | 0 | 0 | Other |
| lock-keyhole-open.js | 17 | 0 | 0 | 0 | Frontend |
| lock-keyhole-open.js.map | 1 | 0 | 0 | 0 | Other |
| lock-keyhole.js | 17 | 0 | 0 | 0 | Frontend |
| lock-keyhole.js.map | 1 | 0 | 0 | 0 | Other |
| lock-open.js | 16 | 0 | 0 | 0 | Frontend |
| lock-open.js.map | 1 | 0 | 0 | 0 | Other |
| lock.js | 16 | 0 | 0 | 0 | Frontend |
| lock.js.map | 1 | 0 | 0 | 0 | Other |
| log-in.js | 17 | 0 | 0 | 0 | Frontend |
| log-in.js.map | 1 | 0 | 0 | 0 | Other |
| log-out.js | 17 | 0 | 0 | 0 | Frontend |
| log-out.js.map | 1 | 0 | 0 | 0 | Other |
| logs.js | 23 | 0 | 0 | 0 | Frontend |
| logs.js.map | 1 | 0 | 0 | 0 | Other |
| lollipop.js | 17 | 0 | 0 | 0 | Frontend |
| lollipop.js.map | 1 | 0 | 0 | 0 | Other |
| luggage.js | 22 | 0 | 0 | 0 | Frontend |
| luggage.js.map | 1 | 0 | 0 | 0 | Other |
| m-square.js | 9 | 0 | 0 | 0 | Frontend |
| m-square.js.map | 1 | 0 | 0 | 0 | Other |
| magnet.js | 23 | 0 | 0 | 0 | Frontend |
| magnet.js.map | 1 | 0 | 0 | 0 | Other |
| mail-check.js | 17 | 0 | 0 | 0 | Frontend |
| mail-check.js.map | 1 | 0 | 0 | 0 | Other |
| mail-minus.js | 17 | 0 | 0 | 0 | Frontend |
| mail-minus.js.map | 1 | 0 | 0 | 0 | Other |
| mail-open.js | 22 | 0 | 0 | 0 | Frontend |
| mail-open.js.map | 1 | 0 | 0 | 0 | Other |
| mail-plus.js | 18 | 0 | 0 | 0 | Frontend |
| mail-plus.js.map | 1 | 0 | 0 | 0 | Other |
| mail-question.js | 24 | 0 | 0 | 0 | Frontend |
| mail-question.js.map | 1 | 0 | 0 | 0 | Other |
| mail-search.js | 19 | 0 | 0 | 0 | Frontend |
| mail-search.js.map | 1 | 0 | 0 | 0 | Other |
| mail-warning.js | 18 | 0 | 0 | 0 | Frontend |
| mail-warning.js.map | 1 | 0 | 0 | 0 | Other |
| mail-x.js | 18 | 0 | 0 | 0 | Frontend |
| mail-x.js.map | 1 | 0 | 0 | 0 | Other |
| mail.js | 16 | 0 | 0 | 0 | Frontend |
| mail.js.map | 1 | 0 | 0 | 0 | Other |
| mailbox.js | 24 | 0 | 0 | 0 | Frontend |
| mailbox.js.map | 1 | 0 | 0 | 0 | Other |
| mails.js | 17 | 0 | 0 | 0 | Frontend |
| mails.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-check-inside.js | 22 | 0 | 0 | 0 | Frontend |
| map-pin-check-inside.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-check.js | 23 | 0 | 0 | 0 | Frontend |
| map-pin-check.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-house.js | 30 | 0 | 0 | 0 | Frontend |
| map-pin-house.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-minus-inside.js | 22 | 0 | 0 | 0 | Frontend |
| map-pin-minus-inside.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-minus.js | 23 | 0 | 0 | 0 | Frontend |
| map-pin-minus.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-off.js | 25 | 0 | 0 | 0 | Frontend |
| map-pin-off.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-plus-inside.js | 23 | 0 | 0 | 0 | Frontend |
| map-pin-plus-inside.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-plus.js | 24 | 0 | 0 | 0 | Frontend |
| map-pin-plus.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-x-inside.js | 23 | 0 | 0 | 0 | Frontend |
| map-pin-x-inside.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin-x.js | 24 | 0 | 0 | 0 | Frontend |
| map-pin-x.js.map | 1 | 0 | 0 | 0 | Other |
| map-pin.js | 22 | 0 | 0 | 0 | Frontend |
| map-pin.js.map | 1 | 0 | 0 | 0 | Other |
| map-pinned.js | 29 | 0 | 0 | 0 | Frontend |
| map-pinned.js.map | 1 | 0 | 0 | 0 | Other |
| map.js | 23 | 0 | 0 | 0 | Frontend |
| map.js.map | 1 | 0 | 0 | 0 | Other |
| martini.js | 17 | 0 | 0 | 0 | Frontend |
| martini.js.map | 1 | 0 | 0 | 0 | Other |
| maximize-2.js | 18 | 0 | 0 | 0 | Frontend |
| maximize-2.js.map | 1 | 0 | 0 | 0 | Other |
| maximize.js | 18 | 0 | 0 | 0 | Frontend |
| maximize.js.map | 1 | 0 | 0 | 0 | Other |
| medal.js | 26 | 0 | 0 | 0 | Frontend |
| medal.js.map | 1 | 0 | 0 | 0 | Other |
| megaphone-off.js | 18 | 0 | 0 | 0 | Frontend |
| megaphone-off.js.map | 1 | 0 | 0 | 0 | Other |
| megaphone.js | 16 | 0 | 0 | 0 | Frontend |
| megaphone.js.map | 1 | 0 | 0 | 0 | Other |
| meh.js | 18 | 0 | 0 | 0 | Frontend |
| meh.js.map | 1 | 0 | 0 | 0 | Other |
| memory-stick.js | 29 | 0 | 0 | 0 | Frontend |
| memory-stick.js.map | 1 | 0 | 0 | 0 | Other |
| menu-square.js | 9 | 0 | 0 | 0 | Frontend |
| menu-square.js.map | 1 | 0 | 0 | 0 | Other |
| menu.js | 17 | 0 | 0 | 0 | Frontend |
| menu.js.map | 1 | 0 | 0 | 0 | Other |
| merge.js | 17 | 0 | 0 | 0 | Frontend |
| merge.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-code.js | 17 | 0 | 0 | 0 | Frontend |
| message-circle-code.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-dashed.js | 22 | 0 | 0 | 0 | Frontend |
| message-circle-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-heart.js | 22 | 0 | 0 | 0 | Frontend |
| message-circle-heart.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-more.js | 18 | 0 | 0 | 0 | Frontend |
| message-circle-more.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-off.js | 17 | 0 | 0 | 0 | Frontend |
| message-circle-off.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-plus.js | 17 | 0 | 0 | 0 | Frontend |
| message-circle-plus.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-question.js | 17 | 0 | 0 | 0 | Frontend |
| message-circle-question.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-reply.js | 17 | 0 | 0 | 0 | Frontend |
| message-circle-reply.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-warning.js | 17 | 0 | 0 | 0 | Frontend |
| message-circle-warning.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle-x.js | 17 | 0 | 0 | 0 | Frontend |
| message-circle-x.js.map | 1 | 0 | 0 | 0 | Other |
| message-circle.js | 15 | 0 | 0 | 0 | Frontend |
| message-circle.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-code.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-code.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-dashed.js | 23 | 0 | 0 | 0 | Frontend |
| message-square-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-diff.js | 18 | 0 | 0 | 0 | Frontend |
| message-square-diff.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-dot.js | 16 | 0 | 0 | 0 | Frontend |
| message-square-dot.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-heart.js | 22 | 0 | 0 | 0 | Frontend |
| message-square-heart.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-lock.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-lock.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-more.js | 18 | 0 | 0 | 0 | Frontend |
| message-square-more.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-off.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-off.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-plus.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-plus.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-quote.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-quote.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-reply.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-reply.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-share.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-share.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-text.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-text.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-warning.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-warning.js.map | 1 | 0 | 0 | 0 | Other |
| message-square-x.js | 17 | 0 | 0 | 0 | Frontend |
| message-square-x.js.map | 1 | 0 | 0 | 0 | Other |
| message-square.js | 15 | 0 | 0 | 0 | Frontend |
| message-square.js.map | 1 | 0 | 0 | 0 | Other |
| messages-square.js | 16 | 0 | 0 | 0 | Frontend |
| messages-square.js.map | 1 | 0 | 0 | 0 | Other |
| mic-2.js | 9 | 0 | 0 | 0 | Frontend |
| mic-2.js.map | 1 | 0 | 0 | 0 | Other |
| mic-off.js | 20 | 0 | 0 | 0 | Frontend |
| mic-off.js.map | 1 | 0 | 0 | 0 | Other |
| mic-vocal.js | 29 | 0 | 0 | 0 | Frontend |
| mic-vocal.js.map | 1 | 0 | 0 | 0 | Other |
| mic.js | 17 | 0 | 0 | 0 | Frontend |
| mic.js.map | 1 | 0 | 0 | 0 | Other |
| microchip.js | 31 | 0 | 0 | 0 | Frontend |
| microchip.js.map | 1 | 0 | 0 | 0 | Other |
| microscope.js | 20 | 0 | 0 | 0 | Frontend |
| microscope.js.map | 1 | 0 | 0 | 0 | Other |
| microwave.js | 19 | 0 | 0 | 0 | Frontend |
| microwave.js.map | 1 | 0 | 0 | 0 | Other |
| milestone.js | 23 | 0 | 0 | 0 | Frontend |
| milestone.js.map | 1 | 0 | 0 | 0 | Other |
| milk-off.js | 24 | 0 | 0 | 0 | Frontend |
| milk-off.js.map | 1 | 0 | 0 | 0 | Other |
| milk.js | 23 | 0 | 0 | 0 | Frontend |
| milk.js.map | 1 | 0 | 0 | 0 | Other |
| minimize-2.js | 18 | 0 | 0 | 0 | Frontend |
| minimize-2.js.map | 1 | 0 | 0 | 0 | Other |
| minimize.js | 18 | 0 | 0 | 0 | Frontend |
| minimize.js.map | 1 | 0 | 0 | 0 | Other |
| minus-circle.js | 9 | 0 | 0 | 0 | Frontend |
| minus-circle.js.map | 1 | 0 | 0 | 0 | Other |
| minus-square.js | 9 | 0 | 0 | 0 | Frontend |
| minus-square.js.map | 1 | 0 | 0 | 0 | Other |
| minus.js | 13 | 0 | 0 | 0 | Frontend |
| minus.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-check.js | 18 | 0 | 0 | 0 | Frontend |
| monitor-check.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-cog.js | 26 | 0 | 0 | 0 | Frontend |
| monitor-cog.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-dot.js | 18 | 0 | 0 | 0 | Frontend |
| monitor-dot.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-down.js | 19 | 0 | 0 | 0 | Frontend |
| monitor-down.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-off.js | 19 | 0 | 0 | 0 | Frontend |
| monitor-off.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-pause.js | 19 | 0 | 0 | 0 | Frontend |
| monitor-pause.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-play.js | 24 | 0 | 0 | 0 | Frontend |
| monitor-play.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-smartphone.js | 18 | 0 | 0 | 0 | Frontend |
| monitor-smartphone.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-speaker.js | 19 | 0 | 0 | 0 | Frontend |
| monitor-speaker.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-stop.js | 18 | 0 | 0 | 0 | Frontend |
| monitor-stop.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-up.js | 19 | 0 | 0 | 0 | Frontend |
| monitor-up.js.map | 1 | 0 | 0 | 0 | Other |
| monitor-x.js | 19 | 0 | 0 | 0 | Frontend |
| monitor-x.js.map | 1 | 0 | 0 | 0 | Other |
| monitor.js | 17 | 0 | 0 | 0 | Frontend |
| monitor.js.map | 1 | 0 | 0 | 0 | Other |
| moon-star.js | 17 | 0 | 0 | 0 | Frontend |
| moon-star.js.map | 1 | 0 | 0 | 0 | Other |
| moon.js | 15 | 0 | 0 | 0 | Frontend |
| moon.js.map | 1 | 0 | 0 | 0 | Other |
| more-horizontal.js | 9 | 0 | 0 | 0 | Frontend |
| more-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| more-vertical.js | 9 | 0 | 0 | 0 | Frontend |
| more-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| mountain-snow.js | 19 | 0 | 0 | 0 | Frontend |
| mountain-snow.js.map | 1 | 0 | 0 | 0 | Other |
| mountain.js | 15 | 0 | 0 | 0 | Frontend |
| mountain.js.map | 1 | 0 | 0 | 0 | Other |
| mouse-off.js | 18 | 0 | 0 | 0 | Frontend |
| mouse-off.js.map | 1 | 0 | 0 | 0 | Other |
| mouse-pointer-2.js | 21 | 0 | 0 | 0 | Frontend |
| mouse-pointer-2.js.map | 1 | 0 | 0 | 0 | Other |
| mouse-pointer-ban.js | 23 | 0 | 0 | 0 | Frontend |
| mouse-pointer-ban.js.map | 1 | 0 | 0 | 0 | Other |
| mouse-pointer-click.js | 25 | 0 | 0 | 0 | Frontend |
| mouse-pointer-click.js.map | 1 | 0 | 0 | 0 | Other |
| mouse-pointer-square-dashed.js | 9 | 0 | 0 | 0 | Frontend |
| mouse-pointer-square-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| mouse-pointer.js | 22 | 0 | 0 | 0 | Frontend |
| mouse-pointer.js.map | 1 | 0 | 0 | 0 | Other |
| mouse.js | 16 | 0 | 0 | 0 | Frontend |
| mouse.js.map | 1 | 0 | 0 | 0 | Other |
| move-3-d.js | 9 | 0 | 0 | 0 | Frontend |
| move-3-d.js.map | 1 | 0 | 0 | 0 | Other |
| move-3d.js | 18 | 0 | 0 | 0 | Frontend |
| move-3d.js.map | 1 | 0 | 0 | 0 | Other |
| move-diagonal-2.js | 17 | 0 | 0 | 0 | Frontend |
| move-diagonal-2.js.map | 1 | 0 | 0 | 0 | Other |
| move-diagonal.js | 17 | 0 | 0 | 0 | Frontend |
| move-diagonal.js.map | 1 | 0 | 0 | 0 | Other |
| move-down-left.js | 16 | 0 | 0 | 0 | Frontend |
| move-down-left.js.map | 1 | 0 | 0 | 0 | Other |
| move-down-right.js | 16 | 0 | 0 | 0 | Frontend |
| move-down-right.js.map | 1 | 0 | 0 | 0 | Other |
| move-down.js | 16 | 0 | 0 | 0 | Frontend |
| move-down.js.map | 1 | 0 | 0 | 0 | Other |
| move-horizontal.js | 17 | 0 | 0 | 0 | Frontend |
| move-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| move-left.js | 16 | 0 | 0 | 0 | Frontend |
| move-left.js.map | 1 | 0 | 0 | 0 | Other |
| move-right.js | 16 | 0 | 0 | 0 | Frontend |
| move-right.js.map | 1 | 0 | 0 | 0 | Other |
| move-up-left.js | 16 | 0 | 0 | 0 | Frontend |
| move-up-left.js.map | 1 | 0 | 0 | 0 | Other |
| move-up-right.js | 16 | 0 | 0 | 0 | Frontend |
| move-up-right.js.map | 1 | 0 | 0 | 0 | Other |
| move-up.js | 16 | 0 | 0 | 0 | Frontend |
| move-up.js.map | 1 | 0 | 0 | 0 | Other |
| move-vertical.js | 17 | 0 | 0 | 0 | Frontend |
| move-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| move.js | 20 | 0 | 0 | 0 | Frontend |
| move.js.map | 1 | 0 | 0 | 0 | Other |
| music-2.js | 16 | 0 | 0 | 0 | Frontend |
| music-2.js.map | 1 | 0 | 0 | 0 | Other |
| music-3.js | 16 | 0 | 0 | 0 | Frontend |
| music-3.js.map | 1 | 0 | 0 | 0 | Other |
| music-4.js | 18 | 0 | 0 | 0 | Frontend |
| music-4.js.map | 1 | 0 | 0 | 0 | Other |
| music.js | 17 | 0 | 0 | 0 | Frontend |
| music.js.map | 1 | 0 | 0 | 0 | Other |
| navigation-2-off.js | 17 | 0 | 0 | 0 | Frontend |
| navigation-2-off.js.map | 1 | 0 | 0 | 0 | Other |
| navigation-2.js | 15 | 0 | 0 | 0 | Frontend |
| navigation-2.js.map | 1 | 0 | 0 | 0 | Other |
| navigation-off.js | 17 | 0 | 0 | 0 | Frontend |
| navigation-off.js.map | 1 | 0 | 0 | 0 | Other |
| navigation.js | 15 | 0 | 0 | 0 | Frontend |
| navigation.js.map | 1 | 0 | 0 | 0 | Other |
| network.js | 19 | 0 | 0 | 0 | Frontend |
| network.js.map | 1 | 0 | 0 | 0 | Other |
| newspaper.js | 24 | 0 | 0 | 0 | Frontend |
| newspaper.js.map | 1 | 0 | 0 | 0 | Other |
| nfc.js | 18 | 0 | 0 | 0 | Frontend |
| nfc.js.map | 1 | 0 | 0 | 0 | Other |
| notebook-pen.js | 26 | 0 | 0 | 0 | Frontend |
| notebook-pen.js.map | 1 | 0 | 0 | 0 | Notebook |
| notebook-tabs.js | 23 | 0 | 0 | 0 | Frontend |
| notebook-tabs.js.map | 1 | 0 | 0 | 0 | Notebook |
| notebook-text.js | 22 | 0 | 0 | 0 | Frontend |
| notebook-text.js.map | 1 | 0 | 0 | 0 | Notebook |
| notebook.js | 20 | 0 | 0 | 0 | Frontend |
| notebook.js.map | 1 | 0 | 0 | 0 | Notebook |
| notepad-text-dashed.js | 27 | 0 | 0 | 0 | Frontend |
| notepad-text-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| notepad-text.js | 21 | 0 | 0 | 0 | Frontend |
| notepad-text.js.map | 1 | 0 | 0 | 0 | Other |
| nut-off.js | 31 | 0 | 0 | 0 | Frontend |
| nut-off.js.map | 1 | 0 | 0 | 0 | Other |
| nut.js | 29 | 0 | 0 | 0 | Frontend |
| nut.js.map | 1 | 0 | 0 | 0 | Other |
| octagon-alert.js | 23 | 0 | 0 | 0 | Frontend |
| octagon-alert.js.map | 1 | 0 | 0 | 0 | Other |
| octagon-minus.js | 22 | 0 | 0 | 0 | Frontend |
| octagon-minus.js.map | 1 | 0 | 0 | 0 | Other |
| octagon-pause.js | 23 | 0 | 0 | 0 | Frontend |
| octagon-pause.js.map | 1 | 0 | 0 | 0 | Other |
| octagon-x.js | 23 | 0 | 0 | 0 | Frontend |
| octagon-x.js.map | 1 | 0 | 0 | 0 | Other |
| octagon.js | 21 | 0 | 0 | 0 | Frontend |
| octagon.js.map | 1 | 0 | 0 | 0 | Other |
| omega.js | 21 | 0 | 0 | 0 | Frontend |
| omega.js.map | 1 | 0 | 0 | 0 | Other |
| option.js | 16 | 0 | 0 | 0 | Frontend |
| option.js.map | 1 | 0 | 0 | 0 | Other |
| orbit.js | 19 | 0 | 0 | 0 | Frontend |
| orbit.js.map | 1 | 0 | 0 | 0 | Other |
| origami.js | 29 | 0 | 0 | 0 | Frontend |
| origami.js.map | 1 | 0 | 0 | 0 | Other |
| outdent.js | 9 | 0 | 0 | 0 | Frontend |
| outdent.js.map | 1 | 0 | 0 | 0 | Other |
| package-2.js | 17 | 0 | 0 | 0 | Frontend |
| package-2.js.map | 1 | 0 | 0 | 0 | Other |
| package-check.js | 25 | 0 | 0 | 0 | Frontend |
| package-check.js.map | 1 | 0 | 0 | 0 | Other |
| package-minus.js | 25 | 0 | 0 | 0 | Frontend |
| package-minus.js.map | 1 | 0 | 0 | 0 | Other |
| package-open.js | 36 | 0 | 0 | 0 | Frontend |
| package-open.js.map | 1 | 0 | 0 | 0 | Other |
| package-plus.js | 26 | 0 | 0 | 0 | Frontend |
| package-plus.js.map | 1 | 0 | 0 | 0 | Other |
| package-search.js | 26 | 0 | 0 | 0 | Frontend |
| package-search.js.map | 1 | 0 | 0 | 0 | Other |
| package-x.js | 25 | 0 | 0 | 0 | Frontend |
| package-x.js.map | 1 | 0 | 0 | 0 | Other |
| package.js | 24 | 0 | 0 | 0 | Frontend |
| package.js.map | 1 | 0 | 0 | 0 | Other |
| paint-bucket.js | 21 | 0 | 0 | 0 | Frontend |
| paint-bucket.js.map | 1 | 0 | 0 | 0 | Other |
| paint-roller.js | 17 | 0 | 0 | 0 | Frontend |
| paint-roller.js.map | 1 | 0 | 0 | 0 | Other |
| paintbrush-2.js | 9 | 0 | 0 | 0 | Frontend |
| paintbrush-2.js.map | 1 | 0 | 0 | 0 | Other |
| paintbrush-vertical.js | 24 | 0 | 0 | 0 | Frontend |
| paintbrush-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| paintbrush.js | 29 | 0 | 0 | 0 | Frontend |
| paintbrush.js.map | 1 | 0 | 0 | 0 | Other |
| palette.js | 25 | 0 | 0 | 0 | Frontend |
| palette.js.map | 1 | 0 | 0 | 0 | Other |
| palmtree.js | 9 | 0 | 0 | 0 | Frontend |
| palmtree.js.map | 1 | 0 | 0 | 0 | Other |
| panel-bottom-close.js | 17 | 0 | 0 | 0 | Frontend |
| panel-bottom-close.js.map | 1 | 0 | 0 | 0 | Other |
| panel-bottom-dashed.js | 19 | 0 | 0 | 0 | Frontend |
| panel-bottom-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| panel-bottom-inactive.js | 9 | 0 | 0 | 0 | Frontend |
| panel-bottom-inactive.js.map | 1 | 0 | 0 | 0 | Other |
| panel-bottom-open.js | 17 | 0 | 0 | 0 | Frontend |
| panel-bottom-open.js.map | 1 | 0 | 0 | 0 | Other |
| panel-bottom.js | 16 | 0 | 0 | 0 | Frontend |
| panel-bottom.js.map | 1 | 0 | 0 | 0 | Other |
| panel-left-close.js | 17 | 0 | 0 | 0 | Frontend |
| panel-left-close.js.map | 1 | 0 | 0 | 0 | Other |
| panel-left-dashed.js | 19 | 0 | 0 | 0 | Frontend |
| panel-left-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| panel-left-inactive.js | 9 | 0 | 0 | 0 | Frontend |
| panel-left-inactive.js.map | 1 | 0 | 0 | 0 | Other |
| panel-left-open.js | 17 | 0 | 0 | 0 | Frontend |
| panel-left-open.js.map | 1 | 0 | 0 | 0 | Other |
| panel-left.js | 16 | 0 | 0 | 0 | Frontend |
| panel-left.js.map | 1 | 0 | 0 | 0 | Other |
| panel-right-close.js | 17 | 0 | 0 | 0 | Frontend |
| panel-right-close.js.map | 1 | 0 | 0 | 0 | Other |
| panel-right-dashed.js | 19 | 0 | 0 | 0 | Frontend |
| panel-right-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| panel-right-inactive.js | 9 | 0 | 0 | 0 | Frontend |
| panel-right-inactive.js.map | 1 | 0 | 0 | 0 | Other |
| panel-right-open.js | 17 | 0 | 0 | 0 | Frontend |
| panel-right-open.js.map | 1 | 0 | 0 | 0 | Other |
| panel-right.js | 16 | 0 | 0 | 0 | Frontend |
| panel-right.js.map | 1 | 0 | 0 | 0 | Other |
| panel-top-close.js | 17 | 0 | 0 | 0 | Frontend |
| panel-top-close.js.map | 1 | 0 | 0 | 0 | Other |
| panel-top-dashed.js | 19 | 0 | 0 | 0 | Frontend |
| panel-top-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| panel-top-inactive.js | 9 | 0 | 0 | 0 | Frontend |
| panel-top-inactive.js.map | 1 | 0 | 0 | 0 | Other |
| panel-top-open.js | 17 | 0 | 0 | 0 | Frontend |
| panel-top-open.js.map | 1 | 0 | 0 | 0 | Other |
| panel-top.js | 16 | 0 | 0 | 0 | Frontend |
| panel-top.js.map | 1 | 0 | 0 | 0 | Other |
| panels-left-bottom.js | 17 | 0 | 0 | 0 | Frontend |
| panels-left-bottom.js.map | 1 | 0 | 0 | 0 | Other |
| panels-left-right.js | 9 | 0 | 0 | 0 | Frontend |
| panels-left-right.js.map | 1 | 0 | 0 | 0 | Other |
| panels-right-bottom.js | 17 | 0 | 0 | 0 | Frontend |
| panels-right-bottom.js.map | 1 | 0 | 0 | 0 | Other |
| panels-top-bottom.js | 9 | 0 | 0 | 0 | Frontend |
| panels-top-bottom.js.map | 1 | 0 | 0 | 0 | Other |
| panels-top-left.js | 17 | 0 | 0 | 0 | Frontend |
| panels-top-left.js.map | 1 | 0 | 0 | 0 | Other |
| paperclip.js | 22 | 0 | 0 | 0 | Frontend |
| paperclip.js.map | 1 | 0 | 0 | 0 | Other |
| parentheses.js | 16 | 0 | 0 | 0 | Frontend |
| parentheses.js.map | 1 | 0 | 0 | 0 | Other |
| parking-circle-off.js | 9 | 0 | 0 | 0 | Frontend |
| parking-circle-off.js.map | 1 | 0 | 0 | 0 | Other |
| parking-circle.js | 9 | 0 | 0 | 0 | Frontend |
| parking-circle.js.map | 1 | 0 | 0 | 0 | Other |
| parking-meter.js | 25 | 0 | 0 | 0 | Frontend |
| parking-meter.js.map | 1 | 0 | 0 | 0 | Other |
| parking-square-off.js | 9 | 0 | 0 | 0 | Frontend |
| parking-square-off.js.map | 1 | 0 | 0 | 0 | Other |
| parking-square.js | 9 | 0 | 0 | 0 | Frontend |
| parking-square.js.map | 1 | 0 | 0 | 0 | Other |
| party-popper.js | 38 | 0 | 0 | 0 | Frontend |
| party-popper.js.map | 1 | 0 | 0 | 0 | Other |
| pause-circle.js | 9 | 0 | 0 | 0 | Frontend |
| pause-circle.js.map | 1 | 0 | 0 | 0 | Other |
| pause-octagon.js | 9 | 0 | 0 | 0 | Frontend |
| pause-octagon.js.map | 1 | 0 | 0 | 0 | Other |
| pause.js | 16 | 0 | 0 | 0 | Frontend |
| pause.js.map | 1 | 0 | 0 | 0 | Other |
| paw-print.js | 24 | 0 | 0 | 0 | Frontend |
| paw-print.js.map | 1 | 0 | 0 | 0 | Other |
| pc-case.js | 18 | 0 | 0 | 0 | Frontend |
| pc-case.js.map | 1 | 0 | 0 | 0 | Other |
| pen-box.js | 9 | 0 | 0 | 0 | Frontend |
| pen-box.js.map | 1 | 0 | 0 | 0 | Other |
| pen-line.js | 22 | 0 | 0 | 0 | Frontend |
| pen-line.js.map | 1 | 0 | 0 | 0 | Other |
| pen-off.js | 23 | 0 | 0 | 0 | Frontend |
| pen-off.js.map | 1 | 0 | 0 | 0 | Other |
| pen-square.js | 9 | 0 | 0 | 0 | Frontend |
| pen-square.js.map | 1 | 0 | 0 | 0 | Other |
| pen-tool.js | 30 | 0 | 0 | 0 | Frontend |
| pen-tool.js.map | 1 | 0 | 0 | 0 | Other |
| pen.js | 21 | 0 | 0 | 0 | Frontend |
| pen.js.map | 1 | 0 | 0 | 0 | Other |
| pencil-line.js | 23 | 0 | 0 | 0 | Frontend |
| pencil-line.js.map | 1 | 0 | 0 | 0 | Other |
| pencil-off.js | 24 | 0 | 0 | 0 | Frontend |
| pencil-off.js.map | 1 | 0 | 0 | 0 | Other |
| pencil-ruler.js | 35 | 0 | 0 | 0 | Frontend |
| pencil-ruler.js.map | 1 | 0 | 0 | 0 | Other |
| pencil.js | 22 | 0 | 0 | 0 | Frontend |
| pencil.js.map | 1 | 0 | 0 | 0 | Other |
| pentagon.js | 21 | 0 | 0 | 0 | Frontend |
| pentagon.js.map | 1 | 0 | 0 | 0 | Other |
| percent-circle.js | 9 | 0 | 0 | 0 | Frontend |
| percent-circle.js.map | 1 | 0 | 0 | 0 | Other |
| percent-diamond.js | 9 | 0 | 0 | 0 | Frontend |
| percent-diamond.js.map | 1 | 0 | 0 | 0 | Other |
| percent-square.js | 9 | 0 | 0 | 0 | Frontend |
| percent-square.js.map | 1 | 0 | 0 | 0 | Other |
| percent.js | 17 | 0 | 0 | 0 | Frontend |
| percent.js.map | 1 | 0 | 0 | 0 | Other |
| person-standing.js | 18 | 0 | 0 | 0 | Frontend |
| person-standing.js.map | 1 | 0 | 0 | 0 | Other |
| philippine-peso.js | 17 | 0 | 0 | 0 | Frontend |
| philippine-peso.js.map | 1 | 0 | 0 | 0 | Other |
| phone-call.js | 23 | 0 | 0 | 0 | Frontend |
| phone-call.js.map | 1 | 0 | 0 | 0 | Other |
| phone-forwarded.js | 23 | 0 | 0 | 0 | Frontend |
| phone-forwarded.js.map | 1 | 0 | 0 | 0 | Other |
| phone-incoming.js | 23 | 0 | 0 | 0 | Frontend |
| phone-incoming.js.map | 1 | 0 | 0 | 0 | Other |
| phone-missed.js | 23 | 0 | 0 | 0 | Frontend |
| phone-missed.js.map | 1 | 0 | 0 | 0 | Other |
| phone-off.js | 22 | 0 | 0 | 0 | Frontend |
| phone-off.js.map | 1 | 0 | 0 | 0 | Other |
| phone-outgoing.js | 23 | 0 | 0 | 0 | Frontend |
| phone-outgoing.js.map | 1 | 0 | 0 | 0 | Other |
| phone.js | 21 | 0 | 0 | 0 | Frontend |
| phone.js.map | 1 | 0 | 0 | 0 | Other |
| pi-square.js | 9 | 0 | 0 | 0 | Frontend |
| pi-square.js.map | 1 | 0 | 0 | 0 | Other |
| pi.js | 17 | 0 | 0 | 0 | Frontend |
| pi.js.map | 1 | 0 | 0 | 0 | Other |
| piano.js | 26 | 0 | 0 | 0 | Frontend |
| piano.js.map | 1 | 0 | 0 | 0 | Other |
| pickaxe.js | 36 | 0 | 0 | 0 | Frontend |
| pickaxe.js.map | 1 | 0 | 0 | 0 | Other |
| picture-in-picture-2.js | 16 | 0 | 0 | 0 | Frontend |
| picture-in-picture-2.js.map | 1 | 0 | 0 | 0 | Other |
| picture-in-picture.js | 19 | 0 | 0 | 0 | Frontend |
| picture-in-picture.js.map | 1 | 0 | 0 | 0 | Other |
| pie-chart.js | 9 | 0 | 0 | 0 | Frontend |
| pie-chart.js.map | 1 | 0 | 0 | 0 | Other |
| piggy-bank.js | 23 | 0 | 0 | 0 | Frontend |
| piggy-bank.js.map | 1 | 0 | 0 | 0 | Other |
| pilcrow-left.js | 19 | 0 | 0 | 0 | Frontend |
| pilcrow-left.js.map | 1 | 0 | 0 | 0 | Other |
| pilcrow-right.js | 19 | 0 | 0 | 0 | Frontend |
| pilcrow-right.js.map | 1 | 0 | 0 | 0 | Other |
| pilcrow-square.js | 9 | 0 | 0 | 0 | Frontend |
| pilcrow-square.js.map | 1 | 0 | 0 | 0 | Other |
| pilcrow.js | 17 | 0 | 0 | 0 | Frontend |
| pilcrow.js.map | 1 | 0 | 0 | 0 | Other |
| pill-bottle.js | 17 | 0 | 0 | 0 | Frontend |
| pill-bottle.js.map | 1 | 0 | 0 | 0 | Other |
| pill.js | 19 | 0 | 0 | 0 | Frontend |
| pill.js.map | 1 | 0 | 0 | 0 | Other |
| pin-off.js | 24 | 0 | 0 | 0 | Frontend |
| pin-off.js.map | 1 | 0 | 0 | 0 | Other |
| pin.js | 22 | 0 | 0 | 0 | Frontend |
| pin.js.map | 1 | 0 | 0 | 0 | Other |
| pipette.js | 23 | 0 | 0 | 0 | Frontend |
| pipette.js.map | 1 | 0 | 0 | 0 | Other |
| pizza.js | 25 | 0 | 0 | 0 | Frontend |
| pizza.js.map | 1 | 0 | 0 | 0 | Other |
| plane-landing.js | 22 | 0 | 0 | 0 | Frontend |
| plane-landing.js.map | 1 | 0 | 0 | 0 | Other |
| plane-takeoff.js | 22 | 0 | 0 | 0 | Frontend |
| plane-takeoff.js.map | 1 | 0 | 0 | 0 | Other |
| plane.js | 21 | 0 | 0 | 0 | Frontend |
| plane.js.map | 1 | 0 | 0 | 0 | Other |
| play-circle.js | 9 | 0 | 0 | 0 | Frontend |
| play-circle.js.map | 1 | 0 | 0 | 0 | Other |
| play-square.js | 9 | 0 | 0 | 0 | Frontend |
| play-square.js.map | 1 | 0 | 0 | 0 | Other |
| play.js | 15 | 0 | 0 | 0 | Frontend |
| play.js.map | 1 | 0 | 0 | 0 | Other |
| plug-2.js | 19 | 0 | 0 | 0 | Frontend |
| plug-2.js.map | 1 | 0 | 0 | 0 | Other |
| plug-zap-2.js | 9 | 0 | 0 | 0 | Frontend |
| plug-zap-2.js.map | 1 | 0 | 0 | 0 | Other |
| plug-zap.js | 22 | 0 | 0 | 0 | Frontend |
| plug-zap.js.map | 1 | 0 | 0 | 0 | Other |
| plug.js | 18 | 0 | 0 | 0 | Frontend |
| plug.js.map | 1 | 0 | 0 | 0 | Other |
| plus-circle.js | 9 | 0 | 0 | 0 | Frontend |
| plus-circle.js.map | 1 | 0 | 0 | 0 | Other |
| plus-square.js | 9 | 0 | 0 | 0 | Frontend |
| plus-square.js.map | 1 | 0 | 0 | 0 | Other |
| plus.js | 16 | 0 | 0 | 0 | Frontend |
| plus.js.map | 1 | 0 | 0 | 0 | Other |
| pocket-knife.js | 19 | 0 | 0 | 0 | Frontend |
| pocket-knife.js.map | 1 | 0 | 0 | 0 | Other |
| pocket.js | 22 | 0 | 0 | 0 | Frontend |
| pocket.js.map | 1 | 0 | 0 | 0 | Other |
| podcast.js | 18 | 0 | 0 | 0 | Frontend |
| podcast.js.map | 1 | 0 | 0 | 0 | Other |
| pointer-off.js | 29 | 0 | 0 | 0 | Frontend |
| pointer-off.js.map | 1 | 0 | 0 | 0 | Other |
| pointer.js | 25 | 0 | 0 | 0 | Frontend |
| pointer.js.map | 1 | 0 | 0 | 0 | Other |
| popcorn.js | 30 | 0 | 0 | 0 | Frontend |
| popcorn.js.map | 1 | 0 | 0 | 0 | Other |
| popsicle.js | 22 | 0 | 0 | 0 | Frontend |
| popsicle.js.map | 1 | 0 | 0 | 0 | Other |
| pound-sterling.js | 18 | 0 | 0 | 0 | Frontend |
| pound-sterling.js.map | 1 | 0 | 0 | 0 | Other |
| power-circle.js | 9 | 0 | 0 | 0 | Frontend |
| power-circle.js.map | 1 | 0 | 0 | 0 | Other |
| power-off.js | 18 | 0 | 0 | 0 | Frontend |
| power-off.js.map | 1 | 0 | 0 | 0 | Other |
| power-square.js | 9 | 0 | 0 | 0 | Frontend |
| power-square.js.map | 1 | 0 | 0 | 0 | Other |
| power.js | 16 | 0 | 0 | 0 | Frontend |
| power.js.map | 1 | 0 | 0 | 0 | Other |
| presentation.js | 17 | 0 | 0 | 0 | Frontend |
| presentation.js.map | 1 | 0 | 0 | 0 | Other |
| printer-check.js | 18 | 0 | 0 | 0 | Frontend |
| printer-check.js.map | 1 | 0 | 0 | 0 | Other |
| printer.js | 23 | 0 | 0 | 0 | Frontend |
| printer.js.map | 1 | 0 | 0 | 0 | Other |
| projector.js | 26 | 0 | 0 | 0 | Frontend |
| projector.js.map | 1 | 0 | 0 | 0 | Other |
| proportions.js | 17 | 0 | 0 | 0 | Frontend |
| proportions.js.map | 1 | 0 | 0 | 0 | Other |
| puzzle.js | 21 | 0 | 0 | 0 | Frontend |
| puzzle.js.map | 1 | 0 | 0 | 0 | Other |
| pyramid.js | 22 | 0 | 0 | 0 | Frontend |
| pyramid.js.map | 1 | 0 | 0 | 0 | Other |
| qr-code.js | 26 | 0 | 0 | 0 | Frontend |
| qr-code.js.map | 1 | 0 | 0 | 0 | Other |
| quote.js | 28 | 0 | 0 | 0 | Frontend |
| quote.js.map | 1 | 0 | 0 | 0 | Other |
| rabbit.js | 25 | 0 | 0 | 0 | Frontend |
| rabbit.js.map | 1 | 0 | 0 | 0 | Other |
| radar.js | 22 | 0 | 0 | 0 | Frontend |
| radar.js.map | 1 | 0 | 0 | 0 | Other |
| radiation.js | 36 | 0 | 0 | 0 | Frontend |
| radiation.js.map | 1 | 0 | 0 | 0 | Other |
| radical.js | 21 | 0 | 0 | 0 | Frontend |
| radical.js.map | 1 | 0 | 0 | 0 | Other |
| radio-receiver.js | 18 | 0 | 0 | 0 | Frontend |
| radio-receiver.js.map | 1 | 0 | 0 | 0 | Other |
| radio-tower.js | 21 | 0 | 0 | 0 | Frontend |
| radio-tower.js.map | 1 | 0 | 0 | 0 | Other |
| radio.js | 19 | 0 | 0 | 0 | Frontend |
| radio.js.map | 1 | 0 | 0 | 0 | Other |
| radius.js | 18 | 0 | 0 | 0 | Frontend |
| radius.js.map | 1 | 0 | 0 | 0 | Other |
| rail-symbol.js | 17 | 0 | 0 | 0 | Frontend |
| rail-symbol.js.map | 1 | 0 | 0 | 0 | Other |
| rainbow.js | 17 | 0 | 0 | 0 | Frontend |
| rainbow.js.map | 1 | 0 | 0 | 0 | Other |
| rat.js | 31 | 0 | 0 | 0 | Frontend |
| rat.js.map | 1 | 0 | 0 | 0 | Other |
| ratio.js | 16 | 0 | 0 | 0 | Frontend |
| ratio.js.map | 1 | 0 | 0 | 0 | Other |
| receipt-cent.js | 20 | 0 | 0 | 0 | Frontend |
| receipt-cent.js.map | 1 | 0 | 0 | 0 | Other |
| receipt-euro.js | 20 | 0 | 0 | 0 | Frontend |
| receipt-euro.js.map | 1 | 0 | 0 | 0 | Other |
| receipt-indian-rupee.js | 21 | 0 | 0 | 0 | Frontend |
| receipt-indian-rupee.js.map | 1 | 0 | 0 | 0 | Other |
| receipt-japanese-yen.js | 22 | 0 | 0 | 0 | Frontend |
| receipt-japanese-yen.js.map | 1 | 0 | 0 | 0 | Other |
| receipt-pound-sterling.js | 21 | 0 | 0 | 0 | Frontend |
| receipt-pound-sterling.js.map | 1 | 0 | 0 | 0 | Other |
| receipt-russian-ruble.js | 20 | 0 | 0 | 0 | Frontend |
| receipt-russian-ruble.js.map | 1 | 0 | 0 | 0 | Other |
| receipt-swiss-franc.js | 21 | 0 | 0 | 0 | Frontend |
| receipt-swiss-franc.js.map | 1 | 0 | 0 | 0 | Other |
| receipt-text.js | 21 | 0 | 0 | 0 | Frontend |
| receipt-text.js.map | 1 | 0 | 0 | 0 | Other |
| receipt.js | 20 | 0 | 0 | 0 | Frontend |
| receipt.js.map | 1 | 0 | 0 | 0 | Other |
| rectangle-ellipsis.js | 18 | 0 | 0 | 0 | Frontend |
| rectangle-ellipsis.js.map | 1 | 0 | 0 | 0 | Other |
| rectangle-horizontal.js | 15 | 0 | 0 | 0 | Frontend |
| rectangle-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| rectangle-vertical.js | 15 | 0 | 0 | 0 | Frontend |
| rectangle-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| recycle.js | 38 | 0 | 0 | 0 | Frontend |
| recycle.js.map | 1 | 0 | 0 | 0 | Other |
| redo-2.js | 16 | 0 | 0 | 0 | Frontend |
| redo-2.js.map | 1 | 0 | 0 | 0 | Other |
| redo-dot.js | 17 | 0 | 0 | 0 | Frontend |
| redo-dot.js.map | 1 | 0 | 0 | 0 | Other |
| redo.js | 16 | 0 | 0 | 0 | Frontend |
| redo.js.map | 1 | 0 | 0 | 0 | Other |
| refresh-ccw-dot.js | 19 | 0 | 0 | 0 | Frontend |
| refresh-ccw-dot.js.map | 1 | 0 | 0 | 0 | Other |
| refresh-ccw.js | 18 | 0 | 0 | 0 | Frontend |
| refresh-ccw.js.map | 1 | 0 | 0 | 0 | Other |
| refresh-cw-off.js | 21 | 0 | 0 | 0 | Frontend |
| refresh-cw-off.js.map | 1 | 0 | 0 | 0 | Other |
| refresh-cw.js | 18 | 0 | 0 | 0 | Frontend |
| refresh-cw.js.map | 1 | 0 | 0 | 0 | Other |
| refrigerator.js | 20 | 0 | 0 | 0 | Frontend |
| refrigerator.js.map | 1 | 0 | 0 | 0 | Other |
| regex.js | 21 | 0 | 0 | 0 | Frontend |
| regex.js.map | 1 | 0 | 0 | 0 | Other |
| remove-formatting.js | 19 | 0 | 0 | 0 | Frontend |
| remove-formatting.js.map | 1 | 0 | 0 | 0 | Other |
| repeat-1.js | 19 | 0 | 0 | 0 | Frontend |
| repeat-1.js.map | 1 | 0 | 0 | 0 | Other |
| repeat-2.js | 18 | 0 | 0 | 0 | Frontend |
| repeat-2.js.map | 1 | 0 | 0 | 0 | Other |
| repeat.js | 18 | 0 | 0 | 0 | Frontend |
| repeat.js.map | 1 | 0 | 0 | 0 | Other |
| replace-all.js | 23 | 0 | 0 | 0 | Frontend |
| replace-all.js.map | 1 | 0 | 0 | 0 | Other |
| replace.js | 21 | 0 | 0 | 0 | Frontend |
| replace.js.map | 1 | 0 | 0 | 0 | Other |
| reply-all.js | 17 | 0 | 0 | 0 | Frontend |
| reply-all.js.map | 1 | 0 | 0 | 0 | Other |
| reply.js | 16 | 0 | 0 | 0 | Frontend |
| reply.js.map | 1 | 0 | 0 | 0 | Other |
| rewind.js | 16 | 0 | 0 | 0 | Frontend |
| rewind.js.map | 1 | 0 | 0 | 0 | Other |
| ribbon.js | 28 | 0 | 0 | 0 | Frontend |
| ribbon.js.map | 1 | 0 | 0 | 0 | Other |
| rocket.js | 30 | 0 | 0 | 0 | Frontend |
| rocket.js.map | 1 | 0 | 0 | 0 | Other |
| rocking-chair.js | 18 | 0 | 0 | 0 | Frontend |
| rocking-chair.js.map | 1 | 0 | 0 | 0 | Other |
| roller-coaster.js | 21 | 0 | 0 | 0 | Frontend |
| roller-coaster.js.map | 1 | 0 | 0 | 0 | Other |
| rotate-3-d.js | 9 | 0 | 0 | 0 | Frontend |
| rotate-3-d.js.map | 1 | 0 | 0 | 0 | Other |
| rotate-3d.js | 29 | 0 | 0 | 0 | Frontend |
| rotate-3d.js.map | 1 | 0 | 0 | 0 | Other |
| rotate-ccw-square.js | 17 | 0 | 0 | 0 | Frontend |
| rotate-ccw-square.js.map | 1 | 0 | 0 | 0 | Other |
| rotate-ccw.js | 16 | 0 | 0 | 0 | Frontend |
| rotate-ccw.js.map | 1 | 0 | 0 | 0 | Other |
| rotate-cw-square.js | 17 | 0 | 0 | 0 | Frontend |
| rotate-cw-square.js.map | 1 | 0 | 0 | 0 | Other |
| rotate-cw.js | 16 | 0 | 0 | 0 | Frontend |
| rotate-cw.js.map | 1 | 0 | 0 | 0 | Other |
| route-off.js | 21 | 0 | 0 | 0 | Frontend |
| route-off.js.map | 1 | 0 | 0 | 0 | Other |
| route.js | 17 | 0 | 0 | 0 | Frontend |
| route.js.map | 1 | 0 | 0 | 0 | Other |
| router.js | 20 | 0 | 0 | 0 | Frontend |
| router.js.map | 1 | 0 | 0 | 0 | Other |
| rows-2.js | 16 | 0 | 0 | 0 | Frontend |
| rows-2.js.map | 1 | 0 | 0 | 0 | Other |
| rows-3.js | 17 | 0 | 0 | 0 | Frontend |
| rows-3.js.map | 1 | 0 | 0 | 0 | Other |
| rows-4.js | 18 | 0 | 0 | 0 | Frontend |
| rows-4.js.map | 1 | 0 | 0 | 0 | Other |
| rows.js | 9 | 0 | 0 | 0 | Frontend |
| rows.js.map | 1 | 0 | 0 | 0 | Other |
| rss.js | 17 | 0 | 0 | 0 | Frontend |
| rss.js.map | 1 | 0 | 0 | 0 | Other |
| ruler.js | 25 | 0 | 0 | 0 | Frontend |
| ruler.js.map | 1 | 0 | 0 | 0 | Other |
| russian-ruble.js | 16 | 0 | 0 | 0 | Frontend |
| russian-ruble.js.map | 1 | 0 | 0 | 0 | Other |
| sailboat.js | 17 | 0 | 0 | 0 | Frontend |
| sailboat.js.map | 1 | 0 | 0 | 0 | Other |
| salad.js | 25 | 0 | 0 | 0 | Frontend |
| salad.js.map | 1 | 0 | 0 | 0 | Other |
| sandwich.js | 19 | 0 | 0 | 0 | Frontend |
| sandwich.js.map | 1 | 0 | 0 | 0 | Other |
| satellite-dish.js | 18 | 0 | 0 | 0 | Frontend |
| satellite-dish.js.map | 1 | 0 | 0 | 0 | Other |
| satellite.js | 19 | 0 | 0 | 0 | Frontend |
| satellite.js.map | 1 | 0 | 0 | 0 | Other |
| save-all.js | 24 | 0 | 0 | 0 | Frontend |
| save-all.js.map | 1 | 0 | 0 | 0 | Other |
| save-off.js | 24 | 0 | 0 | 0 | Frontend |
| save-off.js.map | 1 | 0 | 0 | 0 | Other |
| save.js | 23 | 0 | 0 | 0 | Frontend |
| save.js.map | 1 | 0 | 0 | 0 | Other |
| scale-3-d.js | 9 | 0 | 0 | 0 | Frontend |
| scale-3-d.js.map | 1 | 0 | 0 | 0 | Other |
| scale-3d.js | 18 | 0 | 0 | 0 | Frontend |
| scale-3d.js.map | 1 | 0 | 0 | 0 | Other |
| scale.js | 19 | 0 | 0 | 0 | Frontend |
| scale.js.map | 1 | 0 | 0 | 0 | Other |
| scaling.js | 18 | 0 | 0 | 0 | Frontend |
| scaling.js.map | 1 | 0 | 0 | 0 | Other |
| scan-barcode.js | 21 | 0 | 0 | 0 | Frontend |
| scan-barcode.js.map | 1 | 0 | 0 | 0 | Other |
| scan-eye.js | 26 | 0 | 0 | 0 | Frontend |
| scan-eye.js.map | 1 | 0 | 0 | 0 | Other |
| scan-face.js | 21 | 0 | 0 | 0 | Frontend |
| scan-face.js.map | 1 | 0 | 0 | 0 | Other |
| scan-heart.js | 25 | 0 | 0 | 0 | Frontend |
| scan-heart.js.map | 1 | 0 | 0 | 0 | Other |
| scan-line.js | 19 | 0 | 0 | 0 | Frontend |
| scan-line.js.map | 1 | 0 | 0 | 0 | Other |
| scan-qr-code.js | 22 | 0 | 0 | 0 | Frontend |
| scan-qr-code.js.map | 1 | 0 | 0 | 0 | Other |
| scan-search.js | 20 | 0 | 0 | 0 | Frontend |
| scan-search.js.map | 1 | 0 | 0 | 0 | Other |
| scan-text.js | 21 | 0 | 0 | 0 | Frontend |
| scan-text.js.map | 1 | 0 | 0 | 0 | Other |
| scan.js | 18 | 0 | 0 | 0 | Frontend |
| scan.js.map | 1 | 0 | 0 | 0 | Other |
| scatter-chart.js | 9 | 0 | 0 | 0 | Frontend |
| scatter-chart.js.map | 1 | 0 | 0 | 0 | Other |
| school-2.js | 9 | 0 | 0 | 0 | Frontend |
| school-2.js.map | 1 | 0 | 0 | 0 | Other |
| school.js | 26 | 0 | 0 | 0 | Frontend |
| school.js.map | 1 | 0 | 0 | 0 | Other |
| scissors-line-dashed.js | 21 | 0 | 0 | 0 | Frontend |
| scissors-line-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| scissors-square-dashed-bottom.js | 9 | 0 | 0 | 0 | Frontend |
| scissors-square-dashed-bottom.js.map | 1 | 0 | 0 | 0 | Other |
| scissors-square.js | 9 | 0 | 0 | 0 | Frontend |
| scissors-square.js.map | 1 | 0 | 0 | 0 | Other |
| scissors.js | 19 | 0 | 0 | 0 | Frontend |
| scissors.js.map | 1 | 0 | 0 | 0 | Other |
| screen-share-off.js | 19 | 0 | 0 | 0 | Frontend |
| screen-share-off.js.map | 1 | 0 | 0 | 0 | Other |
| screen-share.js | 19 | 0 | 0 | 0 | Frontend |
| screen-share.js.map | 1 | 0 | 0 | 0 | Other |
| scroll-text.js | 24 | 0 | 0 | 0 | Frontend |
| scroll-text.js.map | 1 | 0 | 0 | 0 | Other |
| scroll.js | 22 | 0 | 0 | 0 | Frontend |
| scroll.js.map | 1 | 0 | 0 | 0 | Other |
| search-check.js | 17 | 0 | 0 | 0 | Frontend |
| search-check.js.map | 1 | 0 | 0 | 0 | Other |
| search-code.js | 18 | 0 | 0 | 0 | Frontend |
| search-code.js.map | 1 | 0 | 0 | 0 | Other |
| search-slash.js | 17 | 0 | 0 | 0 | Frontend |
| search-slash.js.map | 1 | 0 | 0 | 0 | Other |
| search-x.js | 18 | 0 | 0 | 0 | Frontend |
| search-x.js.map | 1 | 0 | 0 | 0 | Other |
| search.js | 16 | 0 | 0 | 0 | Frontend |
| search.js.map | 1 | 0 | 0 | 0 | Other |
| section.js | 16 | 0 | 0 | 0 | Frontend |
| section.js.map | 1 | 0 | 0 | 0 | Other |
| send-horizonal.js | 9 | 0 | 0 | 0 | Frontend |
| send-horizonal.js.map | 1 | 0 | 0 | 0 | Other |
| send-horizontal.js | 22 | 0 | 0 | 0 | Frontend |
| send-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| send-to-back.js | 18 | 0 | 0 | 0 | Frontend |
| send-to-back.js.map | 1 | 0 | 0 | 0 | Other |
| send.js | 22 | 0 | 0 | 0 | Frontend |
| send.js.map | 1 | 0 | 0 | 0 | Other |
| separator-horizontal.js | 17 | 0 | 0 | 0 | Frontend |
| separator-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| separator-vertical.js | 17 | 0 | 0 | 0 | Frontend |
| separator-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| server-cog.js | 39 | 0 | 0 | 0 | Frontend |
| server-cog.js.map | 1 | 0 | 0 | 0 | Other |
| server-crash.js | 31 | 0 | 0 | 0 | Frontend |
| server-crash.js.map | 1 | 0 | 0 | 0 | Other |
| server-off.js | 20 | 0 | 0 | 0 | Frontend |
| server-off.js.map | 1 | 0 | 0 | 0 | Other |
| server.js | 18 | 0 | 0 | 0 | Frontend |
| server.js.map | 1 | 0 | 0 | 0 | Other |
| settings-2.js | 18 | 0 | 0 | 0 | Frontend |
| settings-2.js.map | 1 | 0 | 0 | 0 | Other |
| settings.js | 22 | 0 | 0 | 0 | Frontend |
| settings.js.map | 1 | 0 | 0 | 0 | Other |
| shapes.js | 23 | 0 | 0 | 0 | Frontend |
| shapes.js.map | 1 | 0 | 0 | 0 | Other |
| share-2.js | 19 | 0 | 0 | 0 | Frontend |
| share-2.js.map | 1 | 0 | 0 | 0 | Other |
| share.js | 17 | 0 | 0 | 0 | Frontend |
| share.js.map | 1 | 0 | 0 | 0 | Other |
| sheet.js | 19 | 0 | 0 | 0 | Frontend |
| sheet.js.map | 1 | 0 | 0 | 0 | Other |
| shell.js | 21 | 0 | 0 | 0 | Frontend |
| shell.js.map | 1 | 0 | 0 | 0 | Other |
| shield-alert.js | 23 | 0 | 0 | 0 | Frontend |
| shield-alert.js.map | 1 | 0 | 0 | 0 | Other |
| shield-ban.js | 22 | 0 | 0 | 0 | Frontend |
| shield-ban.js.map | 1 | 0 | 0 | 0 | Other |
| shield-check.js | 22 | 0 | 0 | 0 | Frontend |
| shield-check.js.map | 1 | 0 | 0 | 0 | Other |
| shield-close.js | 9 | 0 | 0 | 0 | Frontend |
| shield-close.js.map | 1 | 0 | 0 | 0 | Other |
| shield-ellipsis.js | 24 | 0 | 0 | 0 | Frontend |
| shield-ellipsis.js.map | 1 | 0 | 0 | 0 | Other |
| shield-half.js | 22 | 0 | 0 | 0 | Frontend |
| shield-half.js.map | 1 | 0 | 0 | 0 | Other |
| shield-minus.js | 22 | 0 | 0 | 0 | Frontend |
| shield-minus.js.map | 1 | 0 | 0 | 0 | Other |
| shield-off.js | 29 | 0 | 0 | 0 | Frontend |
| shield-off.js.map | 1 | 0 | 0 | 0 | Other |
| shield-plus.js | 23 | 0 | 0 | 0 | Frontend |
| shield-plus.js.map | 1 | 0 | 0 | 0 | Other |
| shield-question.js | 23 | 0 | 0 | 0 | Frontend |
| shield-question.js.map | 1 | 0 | 0 | 0 | Other |
| shield-x.js | 23 | 0 | 0 | 0 | Frontend |
| shield-x.js.map | 1 | 0 | 0 | 0 | Other |
| shield.js | 21 | 0 | 0 | 0 | Frontend |
| shield.js.map | 1 | 0 | 0 | 0 | Other |
| ship-wheel.js | 24 | 0 | 0 | 0 | Frontend |
| ship-wheel.js.map | 1 | 0 | 0 | 0 | Other |
| ship.js | 31 | 0 | 0 | 0 | Frontend |
| ship.js.map | 1 | 0 | 0 | 0 | Other |
| shirt.js | 21 | 0 | 0 | 0 | Frontend |
| shirt.js.map | 1 | 0 | 0 | 0 | Other |
| shopping-bag.js | 17 | 0 | 0 | 0 | Frontend |
| shopping-bag.js.map | 1 | 0 | 0 | 0 | Other |
| shopping-basket.js | 21 | 0 | 0 | 0 | Frontend |
| shopping-basket.js.map | 1 | 0 | 0 | 0 | Other |
| shopping-cart.js | 23 | 0 | 0 | 0 | Frontend |
| shopping-cart.js.map | 1 | 0 | 0 | 0 | Other |
| shovel.js | 20 | 0 | 0 | 0 | Frontend |
| shovel.js.map | 1 | 0 | 0 | 0 | Other |
| shower-head.js | 24 | 0 | 0 | 0 | Frontend |
| shower-head.js.map | 1 | 0 | 0 | 0 | Other |
| shrink.js | 18 | 0 | 0 | 0 | Frontend |
| shrink.js.map | 1 | 0 | 0 | 0 | Other |
| shrub.js | 17 | 0 | 0 | 0 | Frontend |
| shrub.js.map | 1 | 0 | 0 | 0 | Other |
| shuffle.js | 19 | 0 | 0 | 0 | Frontend |
| shuffle.js.map | 1 | 0 | 0 | 0 | Other |
| sidebar-close.js | 9 | 0 | 0 | 0 | Frontend |
| sidebar-close.js.map | 1 | 0 | 0 | 0 | Other |
| sidebar-open.js | 9 | 0 | 0 | 0 | Frontend |
| sidebar-open.js.map | 1 | 0 | 0 | 0 | Other |
| sidebar.js | 9 | 0 | 0 | 0 | Frontend |
| sidebar.js.map | 1 | 0 | 0 | 0 | Other |
| sigma-square.js | 9 | 0 | 0 | 0 | Frontend |
| sigma-square.js.map | 1 | 0 | 0 | 0 | Other |
| sigma.js | 21 | 0 | 0 | 0 | Frontend |
| sigma.js.map | 1 | 0 | 0 | 0 | Other |
| signal-high.js | 18 | 0 | 0 | 0 | Frontend |
| signal-high.js.map | 1 | 0 | 0 | 0 | Other |
| signal-low.js | 16 | 0 | 0 | 0 | Frontend |
| signal-low.js.map | 1 | 0 | 0 | 0 | Other |
| signal-medium.js | 17 | 0 | 0 | 0 | Frontend |
| signal-medium.js.map | 1 | 0 | 0 | 0 | Other |
| signal-zero.js | 13 | 0 | 0 | 0 | Frontend |
| signal-zero.js.map | 1 | 0 | 0 | 0 | Other |
| signal.js | 19 | 0 | 0 | 0 | Frontend |
| signal.js.map | 1 | 0 | 0 | 0 | Other |
| signature.js | 22 | 0 | 0 | 0 | Frontend |
| signature.js.map | 1 | 0 | 0 | 0 | Other |
| signpost-big.js | 18 | 0 | 0 | 0 | Frontend |
| signpost-big.js.map | 1 | 0 | 0 | 0 | Other |
| signpost.js | 23 | 0 | 0 | 0 | Frontend |
| signpost.js.map | 1 | 0 | 0 | 0 | Other |
| siren.js | 25 | 0 | 0 | 0 | Frontend |
| siren.js.map | 1 | 0 | 0 | 0 | Other |
| skip-back.js | 16 | 0 | 0 | 0 | Frontend |
| skip-back.js.map | 1 | 0 | 0 | 0 | Other |
| skip-forward.js | 16 | 0 | 0 | 0 | Frontend |
| skip-forward.js.map | 1 | 0 | 0 | 0 | Other |
| skull.js | 24 | 0 | 0 | 0 | Frontend |
| skull.js.map | 1 | 0 | 0 | 0 | Other |
| slack.js | 22 | 0 | 0 | 0 | Frontend |
| slack.js.map | 1 | 0 | 0 | 0 | Other |
| slash-square.js | 9 | 0 | 0 | 0 | Frontend |
| slash-square.js.map | 1 | 0 | 0 | 0 | Other |
| slash.js | 13 | 0 | 0 | 0 | Frontend |
| slash.js.map | 1 | 0 | 0 | 0 | Other |
| slice.js | 21 | 0 | 0 | 0 | Frontend |
| slice.js.map | 1 | 0 | 0 | 0 | Other |
| sliders-horizontal.js | 23 | 0 | 0 | 0 | Frontend |
| sliders-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| sliders-vertical.js | 23 | 0 | 0 | 0 | Frontend |
| sliders-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| sliders.js | 9 | 0 | 0 | 0 | Frontend |
| sliders.js.map | 1 | 0 | 0 | 0 | Other |
| smartphone-charging.js | 16 | 0 | 0 | 0 | Frontend |
| smartphone-charging.js.map | 1 | 0 | 0 | 0 | Other |
| smartphone-nfc.js | 18 | 0 | 0 | 0 | Frontend |
| smartphone-nfc.js.map | 1 | 0 | 0 | 0 | Other |
| smartphone.js | 16 | 0 | 0 | 0 | Frontend |
| smartphone.js.map | 1 | 0 | 0 | 0 | Other |
| smile-plus.js | 20 | 0 | 0 | 0 | Frontend |
| smile-plus.js.map | 1 | 0 | 0 | 0 | Other |
| smile.js | 18 | 0 | 0 | 0 | Frontend |
| smile.js.map | 1 | 0 | 0 | 0 | Other |
| snail.js | 19 | 0 | 0 | 0 | Frontend |
| snail.js.map | 1 | 0 | 0 | 0 | Other |
| snowflake.js | 20 | 0 | 0 | 0 | Frontend |
| snowflake.js.map | 1 | 0 | 0 | 0 | Other |
| sofa.js | 25 | 0 | 0 | 0 | Frontend |
| sofa.js.map | 1 | 0 | 0 | 0 | Other |
| sort-asc.js | 9 | 0 | 0 | 0 | Frontend |
| sort-asc.js.map | 1 | 0 | 0 | 0 | Other |
| sort-desc.js | 9 | 0 | 0 | 0 | Frontend |
| sort-desc.js.map | 1 | 0 | 0 | 0 | Other |
| soup.js | 35 | 0 | 0 | 0 | Frontend |
| soup.js.map | 1 | 0 | 0 | 0 | Other |
| space.js | 15 | 0 | 0 | 0 | Frontend |
| space.js.map | 1 | 0 | 0 | 0 | Other |
| spade.js | 22 | 0 | 0 | 0 | Frontend |
| spade.js.map | 1 | 0 | 0 | 0 | Other |
| sparkle.js | 21 | 0 | 0 | 0 | Frontend |
| sparkle.js.map | 1 | 0 | 0 | 0 | Other |
| sparkles.js | 25 | 0 | 0 | 0 | Frontend |
| sparkles.js.map | 1 | 0 | 0 | 0 | Other |
| speaker.js | 18 | 0 | 0 | 0 | Frontend |
| speaker.js.map | 1 | 0 | 0 | 0 | Other |
| speech.js | 23 | 0 | 0 | 0 | Frontend |
| speech.js.map | 1 | 0 | 0 | 0 | Other |
| spell-check-2.js | 23 | 0 | 0 | 0 | Frontend |
| spell-check-2.js.map | 1 | 0 | 0 | 0 | Other |
| spell-check.js | 17 | 0 | 0 | 0 | Frontend |
| spell-check.js.map | 1 | 0 | 0 | 0 | Other |
| spline.js | 17 | 0 | 0 | 0 | Frontend |
| spline.js.map | 1 | 0 | 0 | 0 | Other |
| split-square-horizontal.js | 9 | 0 | 0 | 0 | Frontend |
| split-square-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| split-square-vertical.js | 9 | 0 | 0 | 0 | Frontend |
| split-square-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| split.js | 18 | 0 | 0 | 0 | Frontend |
| split.js.map | 1 | 0 | 0 | 0 | Other |
| spray-can.js | 24 | 0 | 0 | 0 | Frontend |
| spray-can.js.map | 1 | 0 | 0 | 0 | Other |
| sprout.js | 30 | 0 | 0 | 0 | Frontend |
| sprout.js.map | 1 | 0 | 0 | 0 | Other |
| square-activity.js | 16 | 0 | 0 | 0 | Frontend |
| square-activity.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-down-left.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-down-left.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-down-right.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-down-right.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-down.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-down.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-left.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-left.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-out-down-left.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-out-down-left.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-out-down-right.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-out-down-right.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-out-up-left.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-out-up-left.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-out-up-right.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-out-up-right.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-right.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-right.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-up-left.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-up-left.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-up-right.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-up-right.js.map | 1 | 0 | 0 | 0 | Other |
| square-arrow-up.js | 17 | 0 | 0 | 0 | Frontend |
| square-arrow-up.js.map | 1 | 0 | 0 | 0 | Other |
| square-asterisk.js | 18 | 0 | 0 | 0 | Frontend |
| square-asterisk.js.map | 1 | 0 | 0 | 0 | Other |
| square-bottom-dashed-scissors.js | 25 | 0 | 0 | 0 | Frontend |
| square-bottom-dashed-scissors.js.map | 1 | 0 | 0 | 0 | Other |
| square-chart-gantt.js | 18 | 0 | 0 | 0 | Frontend |
| square-chart-gantt.js.map | 1 | 0 | 0 | 0 | Other |
| square-check-big.js | 16 | 0 | 0 | 0 | Frontend |
| square-check-big.js.map | 1 | 0 | 0 | 0 | Other |
| square-check.js | 16 | 0 | 0 | 0 | Frontend |
| square-check.js.map | 1 | 0 | 0 | 0 | Other |
| square-chevron-down.js | 16 | 0 | 0 | 0 | Frontend |
| square-chevron-down.js.map | 1 | 0 | 0 | 0 | Other |
| square-chevron-left.js | 16 | 0 | 0 | 0 | Frontend |
| square-chevron-left.js.map | 1 | 0 | 0 | 0 | Other |
| square-chevron-right.js | 16 | 0 | 0 | 0 | Frontend |
| square-chevron-right.js.map | 1 | 0 | 0 | 0 | Other |
| square-chevron-up.js | 16 | 0 | 0 | 0 | Frontend |
| square-chevron-up.js.map | 1 | 0 | 0 | 0 | Other |
| square-code.js | 17 | 0 | 0 | 0 | Frontend |
| square-code.js.map | 1 | 0 | 0 | 0 | Other |
| square-dashed-bottom-code.js | 22 | 0 | 0 | 0 | Frontend |
| square-dashed-bottom-code.js.map | 1 | 0 | 0 | 0 | Other |
| square-dashed-bottom.js | 20 | 0 | 0 | 0 | Frontend |
| square-dashed-bottom.js.map | 1 | 0 | 0 | 0 | Other |
| square-dashed-kanban.js | 29 | 0 | 0 | 0 | Frontend |
| square-dashed-kanban.js.map | 1 | 0 | 0 | 0 | Other |
| square-dashed-mouse-pointer.js | 30 | 0 | 0 | 0 | Frontend |
| square-dashed-mouse-pointer.js.map | 1 | 0 | 0 | 0 | Other |
| square-dashed.js | 26 | 0 | 0 | 0 | Frontend |
| square-dashed.js.map | 1 | 0 | 0 | 0 | Other |
| square-divide.js | 18 | 0 | 0 | 0 | Frontend |
| square-divide.js.map | 1 | 0 | 0 | 0 | Other |
| square-dot.js | 16 | 0 | 0 | 0 | Frontend |
| square-dot.js.map | 1 | 0 | 0 | 0 | Other |
| square-equal.js | 17 | 0 | 0 | 0 | Frontend |
| square-equal.js.map | 1 | 0 | 0 | 0 | Other |
| square-function.js | 17 | 0 | 0 | 0 | Frontend |
| square-function.js.map | 1 | 0 | 0 | 0 | Other |
| square-gantt-chart.js | 9 | 0 | 0 | 0 | Frontend |
| square-gantt-chart.js.map | 1 | 0 | 0 | 0 | Other |
| square-kanban.js | 18 | 0 | 0 | 0 | Frontend |
| square-kanban.js.map | 1 | 0 | 0 | 0 | Other |
| square-library.js | 18 | 0 | 0 | 0 | Frontend |
| square-library.js.map | 1 | 0 | 0 | 0 | Other |
| square-m.js | 16 | 0 | 0 | 0 | Frontend |
| square-m.js.map | 1 | 0 | 0 | 0 | Other |
| square-menu.js | 18 | 0 | 0 | 0 | Frontend |
| square-menu.js.map | 1 | 0 | 0 | 0 | Other |
| square-minus.js | 16 | 0 | 0 | 0 | Frontend |
| square-minus.js.map | 1 | 0 | 0 | 0 | Other |
| square-mouse-pointer.js | 22 | 0 | 0 | 0 | Frontend |
| square-mouse-pointer.js.map | 1 | 0 | 0 | 0 | Other |
| square-parking-off.js | 19 | 0 | 0 | 0 | Frontend |
| square-parking-off.js.map | 1 | 0 | 0 | 0 | Other |
| square-parking.js | 16 | 0 | 0 | 0 | Frontend |
| square-parking.js.map | 1 | 0 | 0 | 0 | Other |
| square-pen.js | 22 | 0 | 0 | 0 | Frontend |
| square-pen.js.map | 1 | 0 | 0 | 0 | Other |
| square-percent.js | 18 | 0 | 0 | 0 | Frontend |
| square-percent.js.map | 1 | 0 | 0 | 0 | Other |
| square-pi.js | 18 | 0 | 0 | 0 | Frontend |
| square-pi.js.map | 1 | 0 | 0 | 0 | Other |
| square-pilcrow.js | 18 | 0 | 0 | 0 | Frontend |
| square-pilcrow.js.map | 1 | 0 | 0 | 0 | Other |
| square-play.js | 16 | 0 | 0 | 0 | Frontend |
| square-play.js.map | 1 | 0 | 0 | 0 | Other |
| square-plus.js | 17 | 0 | 0 | 0 | Frontend |
| square-plus.js.map | 1 | 0 | 0 | 0 | Other |
| square-power.js | 17 | 0 | 0 | 0 | Frontend |
| square-power.js.map | 1 | 0 | 0 | 0 | Other |
| square-radical.js | 16 | 0 | 0 | 0 | Frontend |
| square-radical.js.map | 1 | 0 | 0 | 0 | Other |
| square-scissors.js | 20 | 0 | 0 | 0 | Frontend |
| square-scissors.js.map | 1 | 0 | 0 | 0 | Other |
| square-sigma.js | 16 | 0 | 0 | 0 | Frontend |
| square-sigma.js.map | 1 | 0 | 0 | 0 | Other |
| square-slash.js | 16 | 0 | 0 | 0 | Frontend |
| square-slash.js.map | 1 | 0 | 0 | 0 | Other |
| square-split-horizontal.js | 17 | 0 | 0 | 0 | Frontend |
| square-split-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| square-split-vertical.js | 17 | 0 | 0 | 0 | Frontend |
| square-split-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| square-square.js | 16 | 0 | 0 | 0 | Frontend |
| square-square.js.map | 1 | 0 | 0 | 0 | Other |
| square-stack.js | 17 | 0 | 0 | 0 | Frontend |
| square-stack.js.map | 1 | 0 | 0 | 0 | Other |
| square-terminal.js | 17 | 0 | 0 | 0 | Frontend |
| square-terminal.js.map | 1 | 0 | 0 | 0 | Other |
| square-user-round.js | 17 | 0 | 0 | 0 | Frontend |
| square-user-round.js.map | 1 | 0 | 0 | 0 | Other |
| square-user.js | 17 | 0 | 0 | 0 | Frontend |
| square-user.js.map | 1 | 0 | 0 | 0 | Other |
| square-x.js | 17 | 0 | 0 | 0 | Frontend |
| square-x.js.map | 1 | 0 | 0 | 0 | Other |
| square.js | 15 | 0 | 0 | 0 | Frontend |
| square.js.map | 1 | 0 | 0 | 0 | Other |
| squircle.js | 15 | 0 | 0 | 0 | Frontend |
| squircle.js.map | 1 | 0 | 0 | 0 | Other |
| squirrel.js | 24 | 0 | 0 | 0 | Frontend |
| squirrel.js.map | 1 | 0 | 0 | 0 | Other |
| stamp.js | 26 | 0 | 0 | 0 | Frontend |
| stamp.js.map | 1 | 0 | 0 | 0 | Other |
| star-half.js | 21 | 0 | 0 | 0 | Frontend |
| star-half.js.map | 1 | 0 | 0 | 0 | Other |
| star-off.js | 17 | 0 | 0 | 0 | Frontend |
| star-off.js.map | 1 | 0 | 0 | 0 | Other |
| star.js | 21 | 0 | 0 | 0 | Frontend |
| star.js.map | 1 | 0 | 0 | 0 | Other |
| stars.js | 9 | 0 | 0 | 0 | Frontend |
| stars.js.map | 1 | 0 | 0 | 0 | Other |
| step-back.js | 16 | 0 | 0 | 0 | Frontend |
| step-back.js.map | 1 | 0 | 0 | 0 | Other |
| step-forward.js | 16 | 0 | 0 | 0 | Frontend |
| step-forward.js.map | 1 | 0 | 0 | 0 | Other |
| stethoscope.js | 19 | 0 | 0 | 0 | Frontend |
| stethoscope.js.map | 1 | 0 | 0 | 0 | Other |
| sticker.js | 22 | 0 | 0 | 0 | Frontend |
| sticker.js.map | 1 | 0 | 0 | 0 | Other |
| sticky-note.js | 16 | 0 | 0 | 0 | Frontend |
| sticky-note.js.map | 1 | 0 | 0 | 0 | Other |
| stop-circle.js | 9 | 0 | 0 | 0 | Frontend |
| stop-circle.js.map | 1 | 0 | 0 | 0 | Other |
| store.js | 25 | 0 | 0 | 0 | Frontend |
| store.js.map | 1 | 0 | 0 | 0 | Other |
| stretch-horizontal.js | 16 | 0 | 0 | 0 | Frontend |
| stretch-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| stretch-vertical.js | 16 | 0 | 0 | 0 | Frontend |
| stretch-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| strikethrough.js | 17 | 0 | 0 | 0 | Frontend |
| strikethrough.js.map | 1 | 0 | 0 | 0 | Other |
| subscript.js | 23 | 0 | 0 | 0 | Scripting |
| subscript.js.map | 1 | 0 | 0 | 0 | Scripting |
| subtitles.js | 9 | 0 | 0 | 0 | Frontend |
| subtitles.js.map | 1 | 0 | 0 | 0 | Other |
| sun-dim.js | 23 | 0 | 0 | 0 | Frontend |
| sun-dim.js.map | 1 | 0 | 0 | 0 | Other |
| sun-medium.js | 23 | 0 | 0 | 0 | Frontend |
| sun-medium.js.map | 1 | 0 | 0 | 0 | Other |
| sun-moon.js | 23 | 0 | 0 | 0 | Frontend |
| sun-moon.js.map | 1 | 0 | 0 | 0 | Other |
| sun-snow.js | 25 | 0 | 0 | 0 | Frontend |
| sun-snow.js.map | 1 | 0 | 0 | 0 | Other |
| sun.js | 23 | 0 | 0 | 0 | Frontend |
| sun.js.map | 1 | 0 | 0 | 0 | Other |
| sunrise.js | 22 | 0 | 0 | 0 | Frontend |
| sunrise.js.map | 1 | 0 | 0 | 0 | Other |
| sunset.js | 22 | 0 | 0 | 0 | Frontend |
| sunset.js.map | 1 | 0 | 0 | 0 | Other |
| superscript.js | 23 | 0 | 0 | 0 | Scripting |
| superscript.js.map | 1 | 0 | 0 | 0 | Scripting |
| swatch-book.js | 24 | 0 | 0 | 0 | Frontend |
| swatch-book.js.map | 1 | 0 | 0 | 0 | Other |
| swiss-franc.js | 17 | 0 | 0 | 0 | Frontend |
| swiss-franc.js.map | 1 | 0 | 0 | 0 | Other |
| switch-camera.js | 19 | 0 | 0 | 0 | Frontend |
| switch-camera.js.map | 1 | 0 | 0 | 0 | Other |
| sword.js | 18 | 0 | 0 | 0 | Frontend |
| sword.js.map | 1 | 0 | 0 | 0 | Other |
| swords.js | 22 | 0 | 0 | 0 | Frontend |
| swords.js.map | 1 | 0 | 0 | 0 | Other |
| syringe.js | 20 | 0 | 0 | 0 | Frontend |
| syringe.js.map | 1 | 0 | 0 | 0 | Other |
| table-2.js | 21 | 0 | 0 | 0 | Frontend |
| table-2.js.map | 1 | 0 | 0 | 0 | Other |
| table-cells-merge.js | 19 | 0 | 0 | 0 | Frontend |
| table-cells-merge.js.map | 1 | 0 | 0 | 0 | Other |
| table-cells-split.js | 18 | 0 | 0 | 0 | Frontend |
| table-cells-split.js.map | 1 | 0 | 0 | 0 | Other |
| table-columns-split.js | 25 | 0 | 0 | 0 | Frontend |
| table-columns-split.js.map | 1 | 0 | 0 | 0 | Other |
| table-of-contents.js | 20 | 0 | 0 | 0 | Frontend |
| table-of-contents.js.map | 1 | 0 | 0 | 0 | Other |
| table-properties.js | 18 | 0 | 0 | 0 | Frontend |
| table-properties.js.map | 1 | 0 | 0 | 0 | Other |
| table-rows-split.js | 25 | 0 | 0 | 0 | Frontend |
| table-rows-split.js.map | 1 | 0 | 0 | 0 | Other |
| table.js | 18 | 0 | 0 | 0 | Frontend |
| table.js.map | 1 | 0 | 0 | 0 | Other |
| tablet-smartphone.js | 17 | 0 | 0 | 0 | Frontend |
| tablet-smartphone.js.map | 1 | 0 | 0 | 0 | Other |
| tablet.js | 16 | 0 | 0 | 0 | Frontend |
| tablet.js.map | 1 | 0 | 0 | 0 | Other |
| tablets.js | 18 | 0 | 0 | 0 | Frontend |
| tablets.js.map | 1 | 0 | 0 | 0 | Other |
| tag.js | 22 | 0 | 0 | 0 | Frontend |
| tag.js.map | 1 | 0 | 0 | 0 | Other |
| tags.js | 23 | 0 | 0 | 0 | Frontend |
| tags.js.map | 1 | 0 | 0 | 0 | Other |
| tally-1.js | 13 | 0 | 0 | 0 | Frontend |
| tally-1.js.map | 1 | 0 | 0 | 0 | Other |
| tally-2.js | 16 | 0 | 0 | 0 | Frontend |
| tally-2.js.map | 1 | 0 | 0 | 0 | Other |
| tally-3.js | 17 | 0 | 0 | 0 | Frontend |
| tally-3.js.map | 1 | 0 | 0 | 0 | Other |
| tally-4.js | 18 | 0 | 0 | 0 | Frontend |
| tally-4.js.map | 1 | 0 | 0 | 0 | Other |
| tally-5.js | 19 | 0 | 0 | 0 | Frontend |
| tally-5.js.map | 1 | 0 | 0 | 0 | Other |
| tangent.js | 18 | 0 | 0 | 0 | Frontend |
| tangent.js.map | 1 | 0 | 0 | 0 | Other |
| target.js | 17 | 0 | 0 | 0 | Frontend |
| target.js.map | 1 | 0 | 0 | 0 | Other |
| telescope.js | 33 | 0 | 0 | 0 | Frontend |
| telescope.js.map | 1 | 0 | 0 | 0 | Other |
| tent-tree.js | 21 | 0 | 0 | 0 | Frontend |
| tent-tree.js.map | 1 | 0 | 0 | 0 | Other |
| tent.js | 18 | 0 | 0 | 0 | Frontend |
| tent.js.map | 1 | 0 | 0 | 0 | Other |
| terminal-square.js | 9 | 0 | 0 | 0 | Frontend |
| terminal-square.js.map | 1 | 0 | 0 | 0 | Other |
| terminal.js | 16 | 0 | 0 | 0 | Frontend |
| terminal.js.map | 1 | 0 | 0 | 0 | Other |
| test-tube-2.js | 9 | 0 | 0 | 0 | Testing |
| test-tube-2.js.map | 1 | 0 | 0 | 0 | Testing |
| test-tube-diagonal.js | 20 | 0 | 0 | 0 | Testing |
| test-tube-diagonal.js.map | 1 | 0 | 0 | 0 | Testing |
| test-tube.js | 17 | 0 | 0 | 0 | Testing |
| test-tube.js.map | 1 | 0 | 0 | 0 | Testing |
| test-tubes.js | 20 | 0 | 0 | 0 | Testing |
| test-tubes.js.map | 1 | 0 | 0 | 0 | Testing |
| text-cursor-input.js | 19 | 0 | 0 | 0 | Frontend |
| text-cursor-input.js.map | 1 | 0 | 0 | 0 | Other |
| text-cursor.js | 17 | 0 | 0 | 0 | Frontend |
| text-cursor.js.map | 1 | 0 | 0 | 0 | Other |
| text-quote.js | 18 | 0 | 0 | 0 | Frontend |
| text-quote.js.map | 1 | 0 | 0 | 0 | Other |
| text-search.js | 19 | 0 | 0 | 0 | Frontend |
| text-search.js.map | 1 | 0 | 0 | 0 | Other |
| text-select.js | 29 | 0 | 0 | 0 | Frontend |
| text-select.js.map | 1 | 0 | 0 | 0 | Other |
| text-selection.js | 9 | 0 | 0 | 0 | Frontend |
| text-selection.js.map | 1 | 0 | 0 | 0 | Other |
| text.js | 17 | 0 | 0 | 0 | Frontend |
| text.js.map | 1 | 0 | 0 | 0 | Other |
| theater.js | 23 | 0 | 0 | 0 | Frontend |
| theater.js.map | 1 | 0 | 0 | 0 | Other |
| thermometer-snowflake.js | 20 | 0 | 0 | 0 | Frontend |
| thermometer-snowflake.js.map | 1 | 0 | 0 | 0 | Other |
| thermometer-sun.js | 20 | 0 | 0 | 0 | Frontend |
| thermometer-sun.js.map | 1 | 0 | 0 | 0 | Other |
| thermometer.js | 15 | 0 | 0 | 0 | Frontend |
| thermometer.js.map | 1 | 0 | 0 | 0 | Other |
| thumbs-down.js | 22 | 0 | 0 | 0 | Frontend |
| thumbs-down.js.map | 1 | 0 | 0 | 0 | Other |
| thumbs-up.js | 22 | 0 | 0 | 0 | Frontend |
| thumbs-up.js.map | 1 | 0 | 0 | 0 | Other |
| ticket-check.js | 22 | 0 | 0 | 0 | Frontend |
| ticket-check.js.map | 1 | 0 | 0 | 0 | Other |
| ticket-minus.js | 22 | 0 | 0 | 0 | Frontend |
| ticket-minus.js.map | 1 | 0 | 0 | 0 | Other |
| ticket-percent.js | 24 | 0 | 0 | 0 | Frontend |
| ticket-percent.js.map | 1 | 0 | 0 | 0 | Other |
| ticket-plus.js | 23 | 0 | 0 | 0 | Frontend |
| ticket-plus.js.map | 1 | 0 | 0 | 0 | Other |
| ticket-slash.js | 22 | 0 | 0 | 0 | Frontend |
| ticket-slash.js.map | 1 | 0 | 0 | 0 | Other |
| ticket-x.js | 23 | 0 | 0 | 0 | Frontend |
| ticket-x.js.map | 1 | 0 | 0 | 0 | Other |
| ticket.js | 24 | 0 | 0 | 0 | Frontend |
| ticket.js.map | 1 | 0 | 0 | 0 | Other |
| tickets-plane.js | 21 | 0 | 0 | 0 | Frontend |
| tickets-plane.js.map | 1 | 0 | 0 | 0 | Other |
| tickets.js | 19 | 0 | 0 | 0 | Frontend |
| tickets.js.map | 1 | 0 | 0 | 0 | Other |
| timer-off.js | 19 | 0 | 0 | 0 | Frontend |
| timer-off.js.map | 1 | 0 | 0 | 0 | Other |
| timer-reset.js | 18 | 0 | 0 | 0 | Frontend |
| timer-reset.js.map | 1 | 0 | 0 | 0 | Other |
| timer.js | 17 | 0 | 0 | 0 | Frontend |
| timer.js.map | 1 | 0 | 0 | 0 | Other |
| toggle-left.js | 16 | 0 | 0 | 0 | Frontend |
| toggle-left.js.map | 1 | 0 | 0 | 0 | Other |
| toggle-right.js | 16 | 0 | 0 | 0 | Frontend |
| toggle-right.js.map | 1 | 0 | 0 | 0 | Other |
| toilet.js | 22 | 0 | 0 | 0 | Frontend |
| toilet.js.map | 1 | 0 | 0 | 0 | Other |
| tornado.js | 19 | 0 | 0 | 0 | Frontend |
| tornado.js.map | 1 | 0 | 0 | 0 | Other |
| torus.js | 16 | 0 | 0 | 0 | Frontend |
| torus.js.map | 1 | 0 | 0 | 0 | Other |
| touchpad-off.js | 20 | 0 | 0 | 0 | Frontend |
| touchpad-off.js.map | 1 | 0 | 0 | 0 | Other |
| touchpad.js | 17 | 0 | 0 | 0 | Frontend |
| touchpad.js.map | 1 | 0 | 0 | 0 | Other |
| tower-control.js | 24 | 0 | 0 | 0 | Frontend |
| tower-control.js.map | 1 | 0 | 0 | 0 | Other |
| toy-brick.js | 17 | 0 | 0 | 0 | Frontend |
| toy-brick.js.map | 1 | 0 | 0 | 0 | Other |
| tractor.js | 23 | 0 | 0 | 0 | Frontend |
| tractor.js.map | 1 | 0 | 0 | 0 | Other |
| traffic-cone.js | 30 | 0 | 0 | 0 | Frontend |
| traffic-cone.js.map | 1 | 0 | 0 | 0 | Other |
| train-front-tunnel.js | 21 | 0 | 0 | 0 | Frontend |
| train-front-tunnel.js.map | 1 | 0 | 0 | 0 | Other |
| train-front.js | 20 | 0 | 0 | 0 | Frontend |
| train-front.js.map | 1 | 0 | 0 | 0 | Other |
| train-track.js | 21 | 0 | 0 | 0 | Frontend |
| train-track.js.map | 1 | 0 | 0 | 0 | Other |
| train.js | 9 | 0 | 0 | 0 | Frontend |
| train.js.map | 1 | 0 | 0 | 0 | Other |
| tram-front.js | 21 | 0 | 0 | 0 | Frontend |
| tram-front.js.map | 1 | 0 | 0 | 0 | Other |
| trash-2.js | 19 | 0 | 0 | 0 | Frontend |
| trash-2.js.map | 1 | 0 | 0 | 0 | Other |
| trash.js | 17 | 0 | 0 | 0 | Frontend |
| trash.js.map | 1 | 0 | 0 | 0 | Other |
| tree-deciduous.js | 22 | 0 | 0 | 0 | Frontend |
| tree-deciduous.js.map | 1 | 0 | 0 | 0 | Other |
| tree-palm.js | 27 | 0 | 0 | 0 | Frontend |
| tree-palm.js.map | 1 | 0 | 0 | 0 | Other |
| tree-pine.js | 22 | 0 | 0 | 0 | Frontend |
| tree-pine.js.map | 1 | 0 | 0 | 0 | Other |
| trees.js | 24 | 0 | 0 | 0 | Frontend |
| trees.js.map | 1 | 0 | 0 | 0 | Other |
| trello.js | 17 | 0 | 0 | 0 | Frontend |
| trello.js.map | 1 | 0 | 0 | 0 | Other |
| trending-down.js | 16 | 0 | 0 | 0 | Frontend |
| trending-down.js.map | 1 | 0 | 0 | 0 | Other |
| trending-up-down.js | 18 | 0 | 0 | 0 | Frontend |
| trending-up-down.js.map | 1 | 0 | 0 | 0 | Other |
| trending-up.js | 16 | 0 | 0 | 0 | Frontend |
| trending-up.js.map | 1 | 0 | 0 | 0 | Other |
| triangle-alert.js | 23 | 0 | 0 | 0 | Frontend |
| triangle-alert.js.map | 1 | 0 | 0 | 0 | Other |
| triangle-right.js | 21 | 0 | 0 | 0 | Frontend |
| triangle-right.js.map | 1 | 0 | 0 | 0 | Other |
| triangle.js | 18 | 0 | 0 | 0 | Frontend |
| triangle.js.map | 1 | 0 | 0 | 0 | Other |
| trophy.js | 20 | 0 | 0 | 0 | Frontend |
| trophy.js.map | 1 | 0 | 0 | 0 | Other |
| truck.js | 25 | 0 | 0 | 0 | Frontend |
| truck.js.map | 1 | 0 | 0 | 0 | Other |
| turtle.js | 24 | 0 | 0 | 0 | Frontend |
| turtle.js.map | 1 | 0 | 0 | 0 | Other |
| tv-2.js | 9 | 0 | 0 | 0 | Frontend |
| tv-2.js.map | 1 | 0 | 0 | 0 | Other |
| tv-minimal-play.js | 23 | 0 | 0 | 0 | Frontend |
| tv-minimal-play.js.map | 1 | 0 | 0 | 0 | Other |
| tv-minimal.js | 16 | 0 | 0 | 0 | Frontend |
| tv-minimal.js.map | 1 | 0 | 0 | 0 | Other |
| tv.js | 16 | 0 | 0 | 0 | Frontend |
| tv.js.map | 1 | 0 | 0 | 0 | Other |
| twitch.js | 15 | 0 | 0 | 0 | Frontend |
| twitch.js.map | 1 | 0 | 0 | 0 | Other |
| twitter.js | 21 | 0 | 0 | 0 | Frontend |
| twitter.js.map | 1 | 0 | 0 | 0 | Other |
| type-outline.js | 21 | 0 | 0 | 0 | Frontend |
| type-outline.js.map | 1 | 0 | 0 | 0 | Other |
| type.js | 17 | 0 | 0 | 0 | Frontend |
| type.js.map | 1 | 0 | 0 | 0 | Other |
| umbrella-off.js | 18 | 0 | 0 | 0 | Frontend |
| umbrella-off.js.map | 1 | 0 | 0 | 0 | Other |
| umbrella.js | 17 | 0 | 0 | 0 | Frontend |
| umbrella.js.map | 1 | 0 | 0 | 0 | Other |
| underline.js | 16 | 0 | 0 | 0 | Frontend |
| underline.js.map | 1 | 0 | 0 | 0 | Other |
| undo-2.js | 16 | 0 | 0 | 0 | Frontend |
| undo-2.js.map | 1 | 0 | 0 | 0 | Other |
| undo-dot.js | 17 | 0 | 0 | 0 | Frontend |
| undo-dot.js.map | 1 | 0 | 0 | 0 | Other |
| undo.js | 16 | 0 | 0 | 0 | Frontend |
| undo.js.map | 1 | 0 | 0 | 0 | Other |
| unfold-horizontal.js | 22 | 0 | 0 | 0 | Frontend |
| unfold-horizontal.js.map | 1 | 0 | 0 | 0 | Other |
| unfold-vertical.js | 22 | 0 | 0 | 0 | Frontend |
| unfold-vertical.js.map | 1 | 0 | 0 | 0 | Other |
| ungroup.js | 16 | 0 | 0 | 0 | Frontend |
| ungroup.js.map | 1 | 0 | 0 | 0 | Other |
| university.js | 21 | 0 | 0 | 0 | Frontend |
| university.js.map | 1 | 0 | 0 | 0 | Other |
| unlink-2.js | 15 | 0 | 0 | 0 | Frontend |
| unlink-2.js.map | 1 | 0 | 0 | 0 | Other |
| unlink.js | 32 | 0 | 0 | 0 | Frontend |
| unlink.js.map | 1 | 0 | 0 | 0 | Other |
| unlock-keyhole.js | 9 | 0 | 0 | 0 | Frontend |
| unlock-keyhole.js.map | 1 | 0 | 0 | 0 | Other |
| unlock.js | 9 | 0 | 0 | 0 | Frontend |
| unlock.js.map | 1 | 0 | 0 | 0 | Other |
| unplug.js | 26 | 0 | 0 | 0 | Frontend |
| unplug.js.map | 1 | 0 | 0 | 0 | Other |
| upload-cloud.js | 9 | 0 | 0 | 0 | Frontend |
| upload-cloud.js.map | 1 | 0 | 0 | 0 | Other |
| upload.js | 17 | 0 | 0 | 0 | Frontend |
| upload.js.map | 1 | 0 | 0 | 0 | Other |
| usb.js | 21 | 0 | 0 | 0 | Frontend |
| usb.js.map | 1 | 0 | 0 | 0 | Other |
| user-2.js | 9 | 0 | 0 | 0 | Frontend |
| user-2.js.map | 1 | 0 | 0 | 0 | Other |
| user-check-2.js | 9 | 0 | 0 | 0 | Frontend |
| user-check-2.js.map | 1 | 0 | 0 | 0 | Other |
| user-check.js | 17 | 0 | 0 | 0 | Frontend |
| user-check.js.map | 1 | 0 | 0 | 0 | Other |
| user-circle-2.js | 9 | 0 | 0 | 0 | Frontend |
| user-circle-2.js.map | 1 | 0 | 0 | 0 | Other |
| user-circle.js | 9 | 0 | 0 | 0 | Frontend |
| user-circle.js.map | 1 | 0 | 0 | 0 | Other |
| user-cog-2.js | 9 | 0 | 0 | 0 | Frontend |
| user-cog-2.js.map | 1 | 0 | 0 | 0 | Other |
| user-cog.js | 25 | 0 | 0 | 0 | Frontend |
| user-cog.js.map | 1 | 0 | 0 | 0 | Other |
| user-minus-2.js | 9 | 0 | 0 | 0 | Frontend |
| user-minus-2.js.map | 1 | 0 | 0 | 0 | Other |
| user-minus.js | 17 | 0 | 0 | 0 | Frontend |
| user-minus.js.map | 1 | 0 | 0 | 0 | Other |
| user-pen.js | 23 | 0 | 0 | 0 | Frontend |
| user-pen.js.map | 1 | 0 | 0 | 0 | Other |
| user-plus-2.js | 9 | 0 | 0 | 0 | Frontend |
| user-plus-2.js.map | 1 | 0 | 0 | 0 | Other |
| user-plus.js | 18 | 0 | 0 | 0 | Frontend |
| user-plus.js.map | 1 | 0 | 0 | 0 | Other |
| user-round-check.js | 17 | 0 | 0 | 0 | Frontend |
| user-round-check.js.map | 1 | 0 | 0 | 0 | Other |
| user-round-cog.js | 25 | 0 | 0 | 0 | Frontend |
| user-round-cog.js.map | 1 | 0 | 0 | 0 | Other |
| user-round-minus.js | 17 | 0 | 0 | 0 | Frontend |
| user-round-minus.js.map | 1 | 0 | 0 | 0 | Other |
| user-round-pen.js | 23 | 0 | 0 | 0 | Frontend |
| user-round-pen.js.map | 1 | 0 | 0 | 0 | Other |
| user-round-plus.js | 18 | 0 | 0 | 0 | Frontend |
| user-round-plus.js.map | 1 | 0 | 0 | 0 | Other |
| user-round-search.js | 18 | 0 | 0 | 0 | Frontend |
| user-round-search.js.map | 1 | 0 | 0 | 0 | Other |
| user-round-x.js | 18 | 0 | 0 | 0 | Frontend |
| user-round-x.js.map | 1 | 0 | 0 | 0 | Other |
| user-round.js | 16 | 0 | 0 | 0 | Frontend |
| user-round.js.map | 1 | 0 | 0 | 0 | Other |
| user-search.js | 18 | 0 | 0 | 0 | Frontend |
| user-search.js.map | 1 | 0 | 0 | 0 | Other |
| user-square-2.js | 9 | 0 | 0 | 0 | Frontend |
| user-square-2.js.map | 1 | 0 | 0 | 0 | Other |
| user-square.js | 9 | 0 | 0 | 0 | Frontend |
| user-square.js.map | 1 | 0 | 0 | 0 | Other |
| user-x-2.js | 9 | 0 | 0 | 0 | Frontend |
| user-x-2.js.map | 1 | 0 | 0 | 0 | Other |
| user-x.js | 18 | 0 | 0 | 0 | Frontend |
| user-x.js.map | 1 | 0 | 0 | 0 | Other |
| user.js | 16 | 0 | 0 | 0 | Frontend |
| user.js.map | 1 | 0 | 0 | 0 | Other |
| users-2.js | 9 | 0 | 0 | 0 | Frontend |
| users-2.js.map | 1 | 0 | 0 | 0 | Other |
| users-round.js | 17 | 0 | 0 | 0 | Frontend |
| users-round.js.map | 1 | 0 | 0 | 0 | Other |
| users.js | 18 | 0 | 0 | 0 | Frontend |
| users.js.map | 1 | 0 | 0 | 0 | Other |
| utensils-crossed.js | 21 | 0 | 0 | 0 | Frontend |
| utensils-crossed.js.map | 1 | 0 | 0 | 0 | Other |
| utensils.js | 17 | 0 | 0 | 0 | Frontend |
| utensils.js.map | 1 | 0 | 0 | 0 | Other |
| utility-pole.js | 21 | 0 | 0 | 0 | Frontend |
| utility-pole.js.map | 1 | 0 | 0 | 0 | Other |
| variable.js | 18 | 0 | 0 | 0 | Frontend |
| variable.js.map | 1 | 0 | 0 | 0 | Other |
| vault.js | 24 | 0 | 0 | 0 | Frontend |
| vault.js.map | 1 | 0 | 0 | 0 | Other |
| vegan.js | 17 | 0 | 0 | 0 | Frontend |
| vegan.js.map | 1 | 0 | 0 | 0 | Other |
| venetian-mask.js | 23 | 0 | 0 | 0 | Frontend |
| venetian-mask.js.map | 1 | 0 | 0 | 0 | Other |
| verified.js | 9 | 0 | 0 | 0 | Frontend |
| verified.js.map | 1 | 0 | 0 | 0 | Other |
| vibrate-off.js | 19 | 0 | 0 | 0 | Frontend |
| vibrate-off.js.map | 1 | 0 | 0 | 0 | Other |
| vibrate.js | 17 | 0 | 0 | 0 | Frontend |
| vibrate.js.map | 1 | 0 | 0 | 0 | Other |
| video-off.js | 20 | 0 | 0 | 0 | Frontend |
| video-off.js.map | 1 | 0 | 0 | 0 | Other |
| video.js | 22 | 0 | 0 | 0 | Frontend |
| video.js.map | 1 | 0 | 0 | 0 | Other |
| videotape.js | 19 | 0 | 0 | 0 | Frontend |
| videotape.js.map | 1 | 0 | 0 | 0 | Other |
| view.js | 24 | 0 | 0 | 0 | Frontend |
| view.js.map | 1 | 0 | 0 | 0 | Other |
| voicemail.js | 17 | 0 | 0 | 0 | Frontend |
| voicemail.js.map | 1 | 0 | 0 | 0 | Other |
| volleyball.js | 20 | 0 | 0 | 0 | Frontend |
| volleyball.js.map | 1 | 0 | 0 | 0 | Other |
| volume-1.js | 22 | 0 | 0 | 0 | Frontend |
| volume-1.js.map | 1 | 0 | 0 | 0 | Other |
| volume-2.js | 23 | 0 | 0 | 0 | Frontend |
| volume-2.js.map | 1 | 0 | 0 | 0 | Other |
| volume-off.js | 25 | 0 | 0 | 0 | Frontend |
| volume-off.js.map | 1 | 0 | 0 | 0 | Other |
| volume-x.js | 23 | 0 | 0 | 0 | Frontend |
| volume-x.js.map | 1 | 0 | 0 | 0 | Other |
| volume.js | 21 | 0 | 0 | 0 | Frontend |
| volume.js.map | 1 | 0 | 0 | 0 | Other |
| vote.js | 17 | 0 | 0 | 0 | Frontend |
| vote.js.map | 1 | 0 | 0 | 0 | Other |
| wallet-2.js | 9 | 0 | 0 | 0 | Frontend |
| wallet-2.js.map | 1 | 0 | 0 | 0 | Other |
| wallet-cards.js | 23 | 0 | 0 | 0 | Frontend |
| wallet-cards.js.map | 1 | 0 | 0 | 0 | Other |
| wallet-minimal.js | 22 | 0 | 0 | 0 | Frontend |
| wallet-minimal.js.map | 1 | 0 | 0 | 0 | Other |
| wallet.js | 22 | 0 | 0 | 0 | Frontend |
| wallet.js.map | 1 | 0 | 0 | 0 | Other |
| wallpaper.js | 24 | 0 | 0 | 0 | Frontend |
| wallpaper.js.map | 1 | 0 | 0 | 0 | Other |
| wand-2.js | 9 | 0 | 0 | 0 | Frontend |
| wand-2.js.map | 1 | 0 | 0 | 0 | Other |
| wand-sparkles.js | 28 | 0 | 0 | 0 | Frontend |
| wand-sparkles.js.map | 1 | 0 | 0 | 0 | Other |
| wand.js | 23 | 0 | 0 | 0 | Frontend |
| wand.js.map | 1 | 0 | 0 | 0 | Other |
| warehouse.js | 24 | 0 | 0 | 0 | Frontend |
| warehouse.js.map | 1 | 0 | 0 | 0 | Other |
| washing-machine.js | 19 | 0 | 0 | 0 | Frontend |
| washing-machine.js.map | 1 | 0 | 0 | 0 | Other |
| watch.js | 21 | 0 | 0 | 0 | Frontend |
| watch.js.map | 1 | 0 | 0 | 0 | Other |
| waves-ladder.js | 25 | 0 | 0 | 0 | Frontend |
| waves-ladder.js.map | 1 | 0 | 0 | 0 | Other |
| waves.js | 35 | 0 | 0 | 0 | Frontend |
| waves.js.map | 1 | 0 | 0 | 0 | Other |
| waypoints.js | 21 | 0 | 0 | 0 | Frontend |
| waypoints.js.map | 1 | 0 | 0 | 0 | Other |
| webcam.js | 18 | 0 | 0 | 0 | Frontend |
| webcam.js.map | 1 | 0 | 0 | 0 | Other |
| webhook-off.js | 21 | 0 | 0 | 0 | Frontend |
| webhook-off.js.map | 1 | 0 | 0 | 0 | Other |
| webhook.js | 23 | 0 | 0 | 0 | Frontend |
| webhook.js.map | 1 | 0 | 0 | 0 | Other |
| weight.js | 22 | 0 | 0 | 0 | Frontend |
| weight.js.map | 1 | 0 | 0 | 0 | Other |
| wheat-off.js | 54 | 0 | 0 | 0 | Frontend |
| wheat-off.js.map | 1 | 0 | 0 | 0 | Other |
| wheat.js | 58 | 0 | 0 | 0 | Frontend |
| wheat.js.map | 1 | 0 | 0 | 0 | Other |
| whole-word.js | 19 | 0 | 0 | 0 | Frontend |
| whole-word.js.map | 1 | 0 | 0 | 0 | Other |
| wifi-high.js | 17 | 0 | 0 | 0 | Frontend |
| wifi-high.js.map | 1 | 0 | 0 | 0 | Other |
| wifi-low.js | 16 | 0 | 0 | 0 | Frontend |
| wifi-low.js.map | 1 | 0 | 0 | 0 | Other |
| wifi-off.js | 21 | 0 | 0 | 0 | Frontend |
| wifi-off.js.map | 1 | 0 | 0 | 0 | Other |
| wifi-zero.js | 13 | 0 | 0 | 0 | Frontend |
| wifi-zero.js.map | 1 | 0 | 0 | 0 | Other |
| wifi.js | 18 | 0 | 0 | 0 | Frontend |
| wifi.js.map | 1 | 0 | 0 | 0 | Other |
| wind-arrow-down.js | 18 | 0 | 0 | 0 | Frontend |
| wind-arrow-down.js.map | 1 | 0 | 0 | 0 | Other |
| wind.js | 17 | 0 | 0 | 0 | Frontend |
| wind.js.map | 1 | 0 | 0 | 0 | Other |
| wine-off.js | 25 | 0 | 0 | 0 | Frontend |
| wine-off.js.map | 1 | 0 | 0 | 0 | Other |
| wine.js | 21 | 0 | 0 | 0 | Frontend |
| wine.js.map | 1 | 0 | 0 | 0 | Other |
| workflow.js | 17 | 0 | 0 | 0 | Frontend |
| workflow.js.map | 1 | 0 | 0 | 0 | Other |
| worm.js | 23 | 0 | 0 | 0 | Frontend |
| worm.js.map | 1 | 0 | 0 | 0 | Other |
| wrap-text.js | 18 | 0 | 0 | 0 | Frontend |
| wrap-text.js.map | 1 | 0 | 0 | 0 | Other |
| wrench.js | 21 | 0 | 0 | 0 | Frontend |
| wrench.js.map | 1 | 0 | 0 | 0 | Other |
| x-circle.js | 9 | 0 | 0 | 0 | Frontend |
| x-circle.js.map | 1 | 0 | 0 | 0 | Other |
| x-octagon.js | 9 | 0 | 0 | 0 | Frontend |
| x-octagon.js.map | 1 | 0 | 0 | 0 | Other |
| x-square.js | 9 | 0 | 0 | 0 | Frontend |
| x-square.js.map | 1 | 0 | 0 | 0 | Other |
| x.js | 16 | 0 | 0 | 0 | Frontend |
| x.js.map | 1 | 0 | 0 | 0 | Other |
| youtube.js | 22 | 0 | 0 | 0 | Frontend |
| youtube.js.map | 1 | 0 | 0 | 0 | Other |
| zap-off.js | 24 | 0 | 0 | 0 | Frontend |
| zap-off.js.map | 1 | 0 | 0 | 0 | Other |
| zap.js | 21 | 0 | 0 | 0 | Frontend |
| zap.js.map | 1 | 0 | 0 | 0 | Other |
| zoom-in.js | 18 | 0 | 0 | 0 | Frontend |
| zoom-in.js.map | 1 | 0 | 0 | 0 | Other |
| zoom-out.js | 17 | 0 | 0 | 0 | Frontend |
| zoom-out.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/lucide-react/dist/esm/shared/src`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| utils.js | 14 | 0 | 0 | 0 | Frontend |
| utils.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/lucide-react/dist/umd`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| lucide-react.js | 21142 | 0 | 0 | 0 | Frontend |
| lucide-react.js.map | 1 | 0 | 0 | 0 | Other |
| lucide-react.min.js | 9 | 0 | 0 | 0 | Frontend |
| lucide-react.min.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/magic-string/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| magic-string.cjs.d.ts | 289 | 0 | 0 | 0 | Frontend |
| magic-string.cjs.js | 1594 | 0 | 0 | 0 | Frontend |
| magic-string.cjs.js.map | 1 | 0 | 0 | 0 | Other |
| magic-string.es.d.mts | 289 | 0 | 0 | 0 | Other |
| magic-string.es.mjs | 1588 | 0 | 0 | 0 | Other |
| magic-string.es.mjs.map | 1 | 0 | 0 | 0 | Other |
| magic-string.umd.js | 1682 | 0 | 0 | 0 | Frontend |
| magic-string.umd.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/minimatch/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| assert-valid-pattern.d.ts | 2 | 0 | 0 | 0 | Frontend |
| assert-valid-pattern.d.ts.map | 1 | 0 | 0 | 0 | Other |
| assert-valid-pattern.js | 14 | 0 | 0 | 0 | Frontend |
| assert-valid-pattern.js.map | 1 | 0 | 0 | 0 | Other |
| ast.d.ts | 20 | 0 | 0 | 0 | Frontend |
| ast.d.ts.map | 1 | 0 | 0 | 0 | Other |
| ast.js | 592 | 0 | 0 | 0 | Frontend |
| ast.js.map | 1 | 0 | 0 | 0 | Other |
| brace-expressions.d.ts | 8 | 0 | 0 | 0 | Frontend |
| brace-expressions.d.ts.map | 1 | 0 | 0 | 0 | Other |
| brace-expressions.js | 152 | 0 | 0 | 0 | Frontend |
| brace-expressions.js.map | 1 | 0 | 0 | 0 | Other |
| escape.d.ts | 12 | 0 | 0 | 0 | Frontend |
| escape.d.ts.map | 1 | 0 | 0 | 0 | Other |
| escape.js | 22 | 0 | 0 | 0 | Frontend |
| escape.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 94 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1017 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| unescape.d.ts | 17 | 0 | 0 | 0 | Frontend |
| unescape.d.ts.map | 1 | 0 | 0 | 0 | Other |
| unescape.js | 24 | 0 | 0 | 0 | Frontend |
| unescape.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/minimatch/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| assert-valid-pattern.d.ts | 2 | 0 | 0 | 0 | Frontend |
| assert-valid-pattern.d.ts.map | 1 | 0 | 0 | 0 | Other |
| assert-valid-pattern.js | 10 | 0 | 0 | 0 | Frontend |
| assert-valid-pattern.js.map | 1 | 0 | 0 | 0 | Other |
| ast.d.ts | 20 | 0 | 0 | 0 | Frontend |
| ast.d.ts.map | 1 | 0 | 0 | 0 | Other |
| ast.js | 588 | 0 | 0 | 0 | Frontend |
| ast.js.map | 1 | 0 | 0 | 0 | Other |
| brace-expressions.d.ts | 8 | 0 | 0 | 0 | Frontend |
| brace-expressions.d.ts.map | 1 | 0 | 0 | 0 | Other |
| brace-expressions.js | 148 | 0 | 0 | 0 | Frontend |
| brace-expressions.js.map | 1 | 0 | 0 | 0 | Other |
| escape.d.ts | 12 | 0 | 0 | 0 | Frontend |
| escape.d.ts.map | 1 | 0 | 0 | 0 | Other |
| escape.js | 18 | 0 | 0 | 0 | Frontend |
| escape.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 94 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1001 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| unescape.d.ts | 17 | 0 | 0 | 0 | Frontend |
| unescape.d.ts.map | 1 | 0 | 0 | 0 | Other |
| unescape.js | 20 | 0 | 0 | 0 | Frontend |
| unescape.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/minipass/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 549 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1028 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/minipass/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 549 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1018 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/minizlib/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constants.d.ts | 2 | 0 | 0 | 0 | Frontend |
| constants.d.ts.map | 1 | 0 | 0 | 0 | Other |
| constants.js | 123 | 0 | 0 | 0 | Frontend |
| constants.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 99 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 416 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/minizlib/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constants.d.ts | 2 | 0 | 0 | 0 | Frontend |
| constants.d.ts.map | 1 | 0 | 0 | 0 | Other |
| constants.js | 117 | 0 | 0 | 0 | Frontend |
| constants.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 99 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 363 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/mitt/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| mitt.js | 2 | 0 | 0 | 0 | Frontend |
| mitt.js.map | 1 | 0 | 0 | 0 | Other |
| mitt.mjs | 2 | 0 | 0 | 0 | Other |
| mitt.mjs.map | 1 | 0 | 0 | 0 | Other |
| mitt.umd.js | 2 | 0 | 0 | 0 | Frontend |
| mitt.umd.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 753 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/motion-dom/dist/cjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 901 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/motion-dom/dist/es`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 21 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/animation/controls`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| BaseGroup.mjs | 82 | 0 | 0 | 0 | Other |
| Group.mjs | 13 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/animation/generators/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| calc-duration.mjs | 17 | 0 | 0 | 0 | Other |
| create-generator-easing.mjs | 19 | 0 | 0 | 0 | Other |
| is-generator.mjs | 5 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/animation/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| get-value-transition.mjs | 9 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/animation/waapi`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| NativeAnimationControls.mjs | 83 | 0 | 0 | 0 | Other |
| PseudoAnimation.mjs | 15 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/animation/waapi/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| attach-timeline.mjs | 6 | 0 | 0 | 0 | Other |
| convert-options.mjs | 55 | 0 | 0 | 0 | Other |
| easing.mjs | 44 | 0 | 0 | 0 | Other |
| linear.mjs | 14 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/gestures`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| hover.mjs | 41 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/gestures/drag/state`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| is-active.mjs | 9 | 0 | 0 | 0 | Other |
| set-active.mjs | 28 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/gestures/press`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 76 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/gestures/press/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| is-keyboard-accessible.mjs | 13 | 0 | 0 | 0 | Other |
| keyboard.mjs | 38 | 0 | 0 | 0 | Other |
| state.mjs | 3 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/gestures/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| is-node-or-child.mjs | 20 | 0 | 0 | 0 | Other |
| is-primary-pointer.mjs | 18 | 0 | 0 | 0 | Other |
| setup.mjs | 15 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| is-bezier-definition.mjs | 3 | 0 | 0 | 0 | Other |
| resolve-elements.mjs | 22 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/utils/supports`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| flags.mjs | 9 | 0 | 0 | 0 | Other |
| linear-easing.mjs | 15 | 0 | 0 | 0 | Other |
| memo.mjs | 9 | 0 | 0 | 0 | Other |
| scroll-timeline.mjs | 5 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/view`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.mjs | 67 | 0 | 0 | 0 | Other |
| start.mjs | 146 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-dom/dist/es/view/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| choose-layer-type.mjs | 11 | 0 | 0 | 0 | Other |
| css.mjs | 32 | 0 | 0 | 0 | Other |
| get-layer-name.mjs | 8 | 0 | 0 | 0 | Other |
| get-view-animations.mjs | 13 | 0 | 0 | 0 | Other |
| has-target.mjs | 5 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/motion-utils/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 20 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/motion-utils/dist/cjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 66 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/motion-utils/dist/es`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| errors.mjs | 18 | 0 | 0 | 0 | Other |
| index.mjs | 5 | 0 | 0 | 0 | Other |
| memo.mjs | 11 | 0 | 0 | 0 | Other |
| noop.mjs | 4 | 0 | 0 | 0 | Other |
| progress.mjs | 19 | 0 | 0 | 0 | Other |
| time-conversion.mjs | 12 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/next-themes/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 53 | 0 | 0 | 0 | Other |
| index.d.ts | 53 | 0 | 0 | 0 | Frontend |
| index.js | 1 | 0 | 0 | 0 | Frontend |
| index.mjs | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/object-hash/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| object_hash.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/package-json-from-dist/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 89 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 134 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/package-json-from-dist/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 89 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 129 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/path-scurry/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 1116 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 2014 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/path-scurry/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 1116 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1979 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/path-scurry/node_modules/lru-cache/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 1277 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1546 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| index.min.js | 2 | 0 | 0 | 0 | Frontend |
| index.min.js.map | 7 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/path-scurry/node_modules/lru-cache/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 1277 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 1542 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| index.min.js | 2 | 0 | 0 | 0 | Frontend |
| index.min.js.map | 7 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/picomatch/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constants.js | 179 | 0 | 0 | 0 | Frontend |
| parse.js | 1091 | 0 | 0 | 0 | Frontend |
| picomatch.js | 342 | 0 | 0 | 0 | Frontend |
| scan.js | 391 | 0 | 0 | 0 | Frontend |
| utils.js | 64 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/pirates/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 155 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/postcss-import/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| assign-layer-names.js | 17 | 0 | 0 | 0 | Frontend |
| data-url.js | 17 | 0 | 0 | 0 | Frontend |
| join-layer.js | 9 | 0 | 0 | 0 | Frontend |
| join-media.js | 28 | 0 | 0 | 0 | Frontend |
| load-content.js | 12 | 0 | 0 | 0 | Frontend |
| parse-statements.js | 172 | 0 | 0 | 0 | Frontend |
| process-content.js | 59 | 0 | 0 | 0 | Frontend |
| resolve-id.js | 42 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/postcss-nested/node_modules/postcss-selector-parser/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 17 | 0 | 0 | 0 | Frontend |
| parser.js | 1015 | 0 | 0 | 0 | Frontend |
| processor.js | 170 | 0 | 0 | 0 | Frontend |
| sortAscending.js | 11 | 0 | 0 | 0 | Frontend |
| tokenTypes.js | 70 | 0 | 0 | 0 | Frontend |
| tokenize.js | 239 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/postcss-nested/node_modules/postcss-selector-parser/dist/selectors`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| attribute.js | 448 | 0 | 0 | 0 | Frontend |
| className.js | 50 | 0 | 0 | 0 | Frontend |
| combinator.js | 21 | 0 | 0 | 0 | Frontend |
| comment.js | 21 | 0 | 0 | 0 | Frontend |
| constructors.js | 65 | 0 | 0 | 0 | Frontend |
| container.js | 308 | 0 | 0 | 0 | Frontend |
| guards.js | 58 | 0 | 0 | 0 | Frontend |
| id.js | 25 | 0 | 0 | 0 | Frontend |
| index.js | 21 | 0 | 0 | 0 | Frontend |
| namespace.js | 80 | 0 | 0 | 0 | Frontend |
| nesting.js | 22 | 0 | 0 | 0 | Frontend |
| node.js | 192 | 0 | 0 | 0 | Frontend |
| pseudo.js | 26 | 0 | 0 | 0 | Frontend |
| root.js | 44 | 0 | 0 | 0 | Frontend |
| selector.js | 21 | 0 | 0 | 0 | Frontend |
| string.js | 21 | 0 | 0 | 0 | Frontend |
| tag.js | 21 | 0 | 0 | 0 | Frontend |
| types.js | 28 | 0 | 0 | 0 | Frontend |
| universal.js | 22 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/postcss-nested/node_modules/postcss-selector-parser/dist/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ensureObject.js | 17 | 0 | 0 | 0 | Frontend |
| getProp.js | 18 | 0 | 0 | 0 | Frontend |
| index.js | 13 | 0 | 0 | 0 | Frontend |
| stripComments.js | 21 | 0 | 0 | 0 | Frontend |
| unesc.js | 76 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/postcss-selector-parser/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 24 | 0 | 0 | 0 | Frontend |
| parser.js | 1243 | 0 | 0 | 0 | Frontend |
| processor.js | 206 | 0 | 0 | 0 | Frontend |
| sortAscending.js | 13 | 0 | 0 | 0 | Frontend |
| tokenTypes.js | 95 | 0 | 0 | 0 | Frontend |
| tokenize.js | 271 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/postcss-selector-parser/dist/selectors`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| attribute.js | 515 | 0 | 0 | 0 | Frontend |
| className.js | 69 | 0 | 0 | 0 | Frontend |
| combinator.js | 31 | 0 | 0 | 0 | Frontend |
| comment.js | 31 | 0 | 0 | 0 | Frontend |
| constructors.js | 102 | 0 | 0 | 0 | Frontend |
| container.js | 395 | 0 | 0 | 0 | Frontend |
| guards.js | 64 | 0 | 0 | 0 | Frontend |
| id.js | 37 | 0 | 0 | 0 | Frontend |
| index.js | 27 | 0 | 0 | 0 | Frontend |
| namespace.js | 101 | 0 | 0 | 0 | Frontend |
| nesting.js | 32 | 0 | 0 | 0 | Frontend |
| node.js | 239 | 0 | 0 | 0 | Frontend |
| pseudo.js | 38 | 0 | 0 | 0 | Frontend |
| root.js | 60 | 0 | 0 | 0 | Frontend |
| selector.js | 31 | 0 | 0 | 0 | Frontend |
| string.js | 31 | 0 | 0 | 0 | Frontend |
| tag.js | 31 | 0 | 0 | 0 | Frontend |
| types.js | 28 | 0 | 0 | 0 | Frontend |
| universal.js | 32 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/postcss-selector-parser/dist/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ensureObject.js | 22 | 0 | 0 | 0 | Frontend |
| getProp.js | 24 | 0 | 0 | 0 | Frontend |
| index.js | 22 | 0 | 0 | 0 | Frontend |
| stripComments.js | 27 | 0 | 0 | 0 | Frontend |
| unesc.js | 93 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/postcss-value-parser/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 177 | 0 | 0 | 0 | Frontend |
| index.js | 28 | 0 | 0 | 0 | Frontend |
| parse.js | 321 | 0 | 0 | 0 | Frontend |
| stringify.js | 48 | 0 | 0 | 0 | Frontend |
| unit.js | 120 | 0 | 0 | 0 | Frontend |
| walk.js | 22 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/postcss/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| at-rule.d.ts | 140 | 0 | 0 | 0 | Frontend |
| at-rule.js | 25 | 0 | 0 | 0 | Frontend |
| comment.d.ts | 68 | 0 | 0 | 0 | Frontend |
| comment.js | 13 | 0 | 0 | 0 | Frontend |
| container.d.ts | 483 | 0 | 0 | 0 | Frontend |
| container.js | 447 | 0 | 0 | 0 | Frontend |
| css-syntax-error.d.ts | 248 | 0 | 0 | 0 | Frontend |
| css-syntax-error.js | 133 | 0 | 0 | 0 | Frontend |
| declaration.d.ts | 151 | 0 | 0 | 0 | Frontend |
| declaration.js | 24 | 0 | 0 | 0 | Frontend |
| document.d.ts | 69 | 0 | 0 | 0 | Frontend |
| document.js | 33 | 0 | 0 | 0 | Frontend |
| fromJSON.d.ts | 9 | 0 | 0 | 0 | Frontend |
| fromJSON.js | 54 | 0 | 0 | 0 | Frontend |
| input.d.ts | 227 | 0 | 0 | 0 | Frontend |
| input.js | 265 | 0 | 0 | 0 | Frontend |
| lazy-result.d.ts | 190 | 0 | 0 | 0 | Frontend |
| lazy-result.js | 550 | 0 | 0 | 0 | Frontend |
| list.d.ts | 60 | 0 | 0 | 0 | Frontend |
| list.js | 58 | 0 | 0 | 0 | Frontend |
| map-generator.js | 368 | 0 | 0 | 0 | Frontend |
| no-work-result.d.ts | 46 | 0 | 0 | 0 | Frontend |
| no-work-result.js | 138 | 0 | 0 | 0 | Frontend |
| node.d.ts | 556 | 0 | 0 | 0 | Frontend |
| node.js | 449 | 0 | 0 | 0 | Frontend |
| parse.d.ts | 9 | 0 | 0 | 0 | Frontend |
| parse.js | 42 | 0 | 0 | 0 | Frontend |
| parser.js | 611 | 0 | 0 | 0 | Frontend |
| postcss.d.mts | 69 | 0 | 0 | 0 | Other |
| postcss.d.ts | 458 | 0 | 0 | 0 | Frontend |
| postcss.js | 101 | 0 | 0 | 0 | Frontend |
| postcss.mjs | 30 | 0 | 0 | 0 | Other |
| previous-map.d.ts | 81 | 0 | 0 | 0 | Frontend |
| previous-map.js | 144 | 0 | 0 | 0 | Frontend |
| processor.d.ts | 115 | 0 | 0 | 0 | Frontend |
| processor.js | 67 | 0 | 0 | 0 | Frontend |
| result.d.ts | 205 | 0 | 0 | 0 | Frontend |
| result.js | 42 | 0 | 0 | 0 | Frontend |
| root.d.ts | 87 | 0 | 0 | 0 | Frontend |
| root.js | 61 | 0 | 0 | 0 | Frontend |
| rule.d.ts | 126 | 0 | 0 | 0 | Frontend |
| rule.js | 27 | 0 | 0 | 0 | Frontend |
| stringifier.d.ts | 46 | 0 | 0 | 0 | Frontend |
| stringifier.js | 353 | 0 | 0 | 0 | Frontend |
| stringify.d.ts | 9 | 0 | 0 | 0 | Frontend |
| stringify.js | 11 | 0 | 0 | 0 | Frontend |
| symbols.js | 5 | 0 | 0 | 0 | Frontend |
| terminal-highlight.js | 70 | 0 | 0 | 0 | Frontend |
| tokenize.js | 266 | 0 | 0 | 0 | Frontend |
| warn-once.js | 13 | 0 | 0 | 0 | Frontend |
| warning.d.ts | 147 | 0 | 0 | 0 | Frontend |
| warning.js | 37 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/prop-types/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ReactPropTypesSecret.js | 12 | 0 | 0 | 0 | Frontend |
| has.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-day-picker/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 1363 | 0 | 0 | 0 | Frontend |
| index.esm.js | 2277 | 0 | 0 | 0 | Frontend |
| index.esm.js.map | 1 | 0 | 0 | 0 | Other |
| index.js | 2332 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| index.min.js | 2 | 0 | 0 | 0 | Frontend |
| index.min.js.map | 1 | 0 | 0 | 0 | Other |
| style.css | 318 | 0 | 0 | 0 | Frontend |
| style.css.d.ts | 39 | 0 | 0 | 0 | Frontend |
| style.css.map | 1 | 0 | 0 | 0 | Other |
| style.module.css | 316 | 0 | 0 | 0 | Frontend |
| style.module.css.d.ts | 39 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-hook-form/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constants.d.ts | 22 | 0 | 0 | 0 | Frontend |
| constants.d.ts.map | 1 | 0 | 0 | 0 | Other |
| controller.d.ts | 46 | 0 | 0 | 0 | Frontend |
| controller.d.ts.map | 1 | 0 | 0 | 0 | Other |
| form.d.ts | 27 | 0 | 0 | 0 | Frontend |
| form.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.cjs.js | 2 | 0 | 0 | 0 | Frontend |
| index.cjs.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 12 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.esm.mjs | 2803 | 0 | 0 | 0 | Other |
| index.esm.mjs.map | 1 | 0 | 0 | 0 | Other |
| index.react-server.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.react-server.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.umd.js | 2 | 0 | 0 | 0 | Frontend |
| index.umd.js.map | 1 | 0 | 0 | 0 | Other |
| react-server.esm.mjs | 1832 | 0 | 0 | 0 | Other |
| react-server.esm.mjs.map | 1 | 0 | 0 | 0 | Other |
| useController.d.ts | 27 | 0 | 0 | 0 | Frontend |
| useController.d.ts.map | 1 | 0 | 0 | 0 | Other |
| useFieldArray.d.ts | 40 | 0 | 0 | 0 | Frontend |
| useFieldArray.d.ts.map | 1 | 0 | 0 | 0 | Other |
| useForm.d.ts | 32 | 0 | 0 | 0 | Frontend |
| useForm.d.ts.map | 1 | 0 | 0 | 0 | Other |
| useFormContext.d.ts | 65 | 0 | 0 | 0 | Frontend |
| useFormContext.d.ts.map | 1 | 0 | 0 | 0 | Other |
| useFormState.d.ts | 33 | 0 | 0 | 0 | Frontend |
| useFormState.d.ts.map | 1 | 0 | 0 | 0 | Other |
| useIsomorphicLayoutEffect.d.ts | 3 | 0 | 0 | 0 | Frontend |
| useIsomorphicLayoutEffect.d.ts.map | 1 | 0 | 0 | 0 | Other |
| useWatch.d.ts | 191 | 0 | 0 | 0 | Frontend |
| useWatch.d.ts.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/react-hook-form/dist/logic`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| appendErrors.d.ts | 4 | 0 | 0 | 0 | Frontend |
| appendErrors.d.ts.map | 1 | 0 | 0 | 0 | Other |
| createFormControl.d.ts | 5 | 0 | 0 | 0 | Frontend |
| createFormControl.d.ts.map | 1 | 0 | 0 | 0 | Other |
| generateId.d.ts | 3 | 0 | 0 | 0 | Frontend |
| generateId.d.ts.map | 1 | 0 | 0 | 0 | Other |
| generateWatchOutput.d.ts | 4 | 0 | 0 | 0 | Frontend |
| generateWatchOutput.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getCheckboxValue.d.ts | 7 | 0 | 0 | 0 | Frontend |
| getCheckboxValue.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getDirtyFields.d.ts | 4 | 0 | 0 | 0 | Frontend |
| getDirtyFields.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getEventValue.d.ts | 3 | 0 | 0 | 0 | Frontend |
| getEventValue.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getFieldValue.d.ts | 3 | 0 | 0 | 0 | Frontend |
| getFieldValue.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getFieldValueAs.d.ts | 4 | 0 | 0 | 0 | Frontend |
| getFieldValueAs.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getFocusFieldName.d.ts | 4 | 0 | 0 | 0 | Frontend |
| getFocusFieldName.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getNodeParentName.d.ts | 3 | 0 | 0 | 0 | Frontend |
| getNodeParentName.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getProxyFormState.d.ts | 4 | 0 | 0 | 0 | Frontend |
| getProxyFormState.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getRadioValue.d.ts | 7 | 0 | 0 | 0 | Frontend |
| getRadioValue.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getResolverOptions.d.ts | 14 | 0 | 0 | 0 | Frontend |
| getResolverOptions.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getRuleValue.d.ts | 4 | 0 | 0 | 0 | Frontend |
| getRuleValue.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getValidateError.d.ts | 3 | 0 | 0 | 0 | Frontend |
| getValidateError.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getValidationModes.d.ts | 4 | 0 | 0 | 0 | Frontend |
| getValidationModes.d.ts.map | 1 | 0 | 0 | 0 | Other |
| getValueAndMessage.d.ts | 7 | 0 | 0 | 0 | Frontend |
| getValueAndMessage.d.ts.map | 1 | 0 | 0 | 0 | Other |
| hasPromiseValidation.d.ts | 4 | 0 | 0 | 0 | Frontend |
| hasPromiseValidation.d.ts.map | 1 | 0 | 0 | 0 | Other |
| hasValidation.d.ts | 4 | 0 | 0 | 0 | Frontend |
| hasValidation.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 4 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isNameInFieldArray.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isNameInFieldArray.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isWatched.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isWatched.d.ts.map | 1 | 0 | 0 | 0 | Other |
| iterateFieldsByAction.d.ts | 4 | 0 | 0 | 0 | Frontend |
| iterateFieldsByAction.d.ts.map | 1 | 0 | 0 | 0 | Other |
| schemaErrorLookup.d.ts | 6 | 0 | 0 | 0 | Frontend |
| schemaErrorLookup.d.ts.map | 1 | 0 | 0 | 0 | Other |
| shouldRenderFormState.d.ts | 7 | 0 | 0 | 0 | Frontend |
| shouldRenderFormState.d.ts.map | 1 | 0 | 0 | 0 | Other |
| shouldSubscribeByName.d.ts | 3 | 0 | 0 | 0 | Frontend |
| shouldSubscribeByName.d.ts.map | 1 | 0 | 0 | 0 | Other |
| skipValidation.d.ts | 7 | 0 | 0 | 0 | Frontend |
| skipValidation.d.ts.map | 1 | 0 | 0 | 0 | Other |
| unsetEmptyArray.d.ts | 3 | 0 | 0 | 0 | Frontend |
| unsetEmptyArray.d.ts.map | 1 | 0 | 0 | 0 | Other |
| updateFieldArrayRootError.d.ts | 4 | 0 | 0 | 0 | Frontend |
| updateFieldArrayRootError.d.ts.map | 1 | 0 | 0 | 0 | Other |
| validateField.d.ts | 4 | 0 | 0 | 0 | Frontend |
| validateField.d.ts.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/react-hook-form/dist/types`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| controller.d.ts | 60 | 0 | 0 | 0 | Frontend |
| controller.d.ts.map | 1 | 0 | 0 | 0 | Other |
| errors.d.ts | 36 | 0 | 0 | 0 | Frontend |
| errors.d.ts.map | 1 | 0 | 0 | 0 | Other |
| events.d.ts | 2 | 0 | 0 | 0 | Frontend |
| events.d.ts.map | 1 | 0 | 0 | 0 | Other |
| fieldArray.d.ts | 195 | 0 | 0 | 0 | Frontend |
| fieldArray.d.ts.map | 1 | 0 | 0 | 0 | Other |
| fields.d.ts | 31 | 0 | 0 | 0 | Frontend |
| fields.d.ts.map | 1 | 0 | 0 | 0 | Other |
| form.d.ts | 730 | 0 | 0 | 0 | Frontend |
| form.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 11 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| resolvers.d.ts | 20 | 0 | 0 | 0 | Frontend |
| resolvers.d.ts.map | 1 | 0 | 0 | 0 | Other |
| utils.d.ts | 72 | 0 | 0 | 0 | Frontend |
| utils.d.ts.map | 1 | 0 | 0 | 0 | Other |
| validator.d.ts | 43 | 0 | 0 | 0 | Frontend |
| validator.d.ts.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/react-hook-form/dist/types/path`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| common.d.ts | 316 | 0 | 0 | 0 | Frontend |
| common.d.ts.map | 1 | 0 | 0 | 0 | Other |
| eager.d.ts | 135 | 0 | 0 | 0 | Frontend |
| eager.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 4 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/react-hook-form/dist/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| append.d.ts | 3 | 0 | 0 | 0 | Frontend |
| append.d.ts.map | 1 | 0 | 0 | 0 | Other |
| cloneObject.d.ts | 2 | 0 | 0 | 0 | Frontend |
| cloneObject.d.ts.map | 1 | 0 | 0 | 0 | Other |
| compact.d.ts | 3 | 0 | 0 | 0 | Frontend |
| compact.d.ts.map | 1 | 0 | 0 | 0 | Other |
| convertToArrayPayload.d.ts | 3 | 0 | 0 | 0 | Frontend |
| convertToArrayPayload.d.ts.map | 1 | 0 | 0 | 0 | Other |
| createSubject.d.ts | 15 | 0 | 0 | 0 | Frontend |
| createSubject.d.ts.map | 1 | 0 | 0 | 0 | Other |
| deepEqual.d.ts | 2 | 0 | 0 | 0 | Frontend |
| deepEqual.d.ts.map | 1 | 0 | 0 | 0 | Other |
| deepMerge.d.ts | 2 | 0 | 0 | 0 | Frontend |
| deepMerge.d.ts.map | 1 | 0 | 0 | 0 | Other |
| extractFormValues.d.ts | 2 | 0 | 0 | 0 | Frontend |
| extractFormValues.d.ts.map | 1 | 0 | 0 | 0 | Other |
| fillEmptyArray.d.ts | 3 | 0 | 0 | 0 | Frontend |
| fillEmptyArray.d.ts.map | 1 | 0 | 0 | 0 | Other |
| flatten.d.ts | 3 | 0 | 0 | 0 | Frontend |
| flatten.d.ts.map | 1 | 0 | 0 | 0 | Other |
| get.d.ts | 3 | 0 | 0 | 0 | Frontend |
| get.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 4 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| insert.d.ts | 3 | 0 | 0 | 0 | Frontend |
| insert.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isBoolean.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isBoolean.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isCheckBoxInput.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isCheckBoxInput.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isDateObject.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isDateObject.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isEmptyObject.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isEmptyObject.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isFileInput.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isFileInput.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isFunction.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isFunction.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isHTMLElement.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isHTMLElement.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isKey.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isKey.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isMultipleSelect.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isMultipleSelect.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isNullOrUndefined.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isNullOrUndefined.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isObject.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isObject.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isPlainObject.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isPlainObject.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isPrimitive.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isPrimitive.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isRadioInput.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isRadioInput.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isRadioOrCheckbox.d.ts | 4 | 0 | 0 | 0 | Frontend |
| isRadioOrCheckbox.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isRegex.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isRegex.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isString.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isString.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isUndefined.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isUndefined.d.ts.map | 1 | 0 | 0 | 0 | Other |
| isWeb.d.ts | 3 | 0 | 0 | 0 | Frontend |
| isWeb.d.ts.map | 1 | 0 | 0 | 0 | Other |
| live.d.ts | 4 | 0 | 0 | 0 | Frontend |
| live.d.ts.map | 1 | 0 | 0 | 0 | Other |
| move.d.ts | 3 | 0 | 0 | 0 | Frontend |
| move.d.ts.map | 1 | 0 | 0 | 0 | Other |
| noop.d.ts | 2 | 0 | 0 | 0 | Frontend |
| noop.d.ts.map | 1 | 0 | 0 | 0 | Other |
| objectHasFunction.d.ts | 3 | 0 | 0 | 0 | Frontend |
| objectHasFunction.d.ts.map | 1 | 0 | 0 | 0 | Other |
| prepend.d.ts | 3 | 0 | 0 | 0 | Frontend |
| prepend.d.ts.map | 1 | 0 | 0 | 0 | Other |
| remove.d.ts | 3 | 0 | 0 | 0 | Frontend |
| remove.d.ts.map | 1 | 0 | 0 | 0 | Other |
| set.d.ts | 4 | 0 | 0 | 0 | Frontend |
| set.d.ts.map | 1 | 0 | 0 | 0 | Other |
| sleep.d.ts | 3 | 0 | 0 | 0 | Frontend |
| sleep.d.ts.map | 1 | 0 | 0 | 0 | Other |
| stringToPath.d.ts | 3 | 0 | 0 | 0 | Frontend |
| stringToPath.d.ts.map | 1 | 0 | 0 | 0 | Other |
| swap.d.ts | 3 | 0 | 0 | 0 | Frontend |
| swap.d.ts.map | 1 | 0 | 0 | 0 | Other |
| unset.d.ts | 2 | 0 | 0 | 0 | Frontend |
| unset.d.ts.map | 1 | 0 | 0 | 0 | Other |
| update.d.ts | 3 | 0 | 0 | 0 | Frontend |
| update.d.ts.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/react-icons/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| iconBase.d.ts | 19 | 0 | 0 | 0 | Frontend |
| iconBase.js | 57 | 0 | 0 | 0 | Frontend |
| iconBase.mjs | 49 | 0 | 0 | 0 | Other |
| iconContext.d.ts | 10 | 0 | 0 | 0 | Frontend |
| iconContext.js | 16 | 0 | 0 | 0 | Frontend |
| iconContext.mjs | 9 | 0 | 0 | 0 | Other |
| iconsManifest.d.ts | 8 | 0 | 0 | 0 | Frontend |
| iconsManifest.js | 219 | 0 | 0 | 0 | Frontend |
| iconsManifest.mjs | 219 | 0 | 0 | 0 | Other |
| index.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.js | 38 | 0 | 0 | 0 | Frontend |
| index.mjs | 3 | 0 | 0 | 0 | Other |
| package.json | 4 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/react-remove-scroll-bar/dist/es2015`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| component.d.ts | 13 | 0 | 0 | 0 | Frontend |
| component.js | 53 | 0 | 0 | 0 | Frontend |
| constants.d.ts | 8 | 0 | 0 | 0 | Frontend |
| constants.js | 8 | 0 | 0 | 0 | Frontend |
| index.d.ts | 4 | 0 | 0 | 0 | Frontend |
| index.js | 4 | 0 | 0 | 0 | Frontend |
| utils.d.ts | 14 | 0 | 0 | 0 | Frontend |
| utils.js | 29 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-remove-scroll-bar/dist/es2019`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| component.d.ts | 13 | 0 | 0 | 0 | Frontend |
| component.js | 85 | 0 | 0 | 0 | Frontend |
| constants.d.ts | 8 | 0 | 0 | 0 | Frontend |
| constants.js | 8 | 0 | 0 | 0 | Frontend |
| index.d.ts | 4 | 0 | 0 | 0 | Frontend |
| index.js | 4 | 0 | 0 | 0 | Frontend |
| utils.d.ts | 14 | 0 | 0 | 0 | Frontend |
| utils.js | 28 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-remove-scroll-bar/dist/es5`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| component.d.ts | 13 | 0 | 0 | 0 | Frontend |
| component.js | 59 | 0 | 0 | 0 | Frontend |
| constants.d.ts | 8 | 0 | 0 | 0 | Frontend |
| constants.js | 11 | 0 | 0 | 0 | Frontend |
| index.d.ts | 4 | 0 | 0 | 0 | Frontend |
| index.js | 12 | 0 | 0 | 0 | Frontend |
| utils.d.ts | 14 | 0 | 0 | 0 | Frontend |
| utils.js | 33 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-remove-scroll/dist/es2015`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Combination.d.ts | 3 | 0 | 0 | 0 | Frontend |
| Combination.js | 7 | 0 | 0 | 0 | Frontend |
| SideEffect.d.ts | 5 | 0 | 0 | 0 | Frontend |
| SideEffect.js | 157 | 0 | 0 | 0 | Frontend |
| UI.d.ts | 7 | 0 | 0 | 0 | Frontend |
| UI.js | 36 | 0 | 0 | 0 | Frontend |
| aggresiveCapture.d.ts | 3 | 0 | 0 | 0 | Frontend |
| aggresiveCapture.js | 19 | 0 | 0 | 0 | Frontend |
| handleScroll.d.ts | 3 | 0 | 0 | 0 | Frontend |
| handleScroll.js | 108 | 0 | 0 | 0 | Frontend |
| index.d.ts | 2 | 0 | 0 | 0 | Frontend |
| index.js | 2 | 0 | 0 | 0 | Frontend |
| medium.d.ts | 2 | 0 | 0 | 0 | Frontend |
| medium.js | 2 | 0 | 0 | 0 | Frontend |
| pinchAndZoom.d.ts | 8 | 0 | 0 | 0 | Frontend |
| pinchAndZoom.js | 33 | 0 | 0 | 0 | Frontend |
| sidecar.d.ts | 2 | 0 | 0 | 0 | Frontend |
| sidecar.js | 4 | 0 | 0 | 0 | Frontend |
| types.d.ts | 104 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-remove-scroll/dist/es2019`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Combination.d.ts | 3 | 0 | 0 | 0 | Frontend |
| Combination.js | 6 | 0 | 0 | 0 | Frontend |
| SideEffect.d.ts | 5 | 0 | 0 | 0 | Frontend |
| SideEffect.js | 155 | 0 | 0 | 0 | Frontend |
| UI.d.ts | 7 | 0 | 0 | 0 | Frontend |
| UI.js | 41 | 0 | 0 | 0 | Frontend |
| aggresiveCapture.d.ts | 3 | 0 | 0 | 0 | Frontend |
| aggresiveCapture.js | 19 | 0 | 0 | 0 | Frontend |
| handleScroll.d.ts | 3 | 0 | 0 | 0 | Frontend |
| handleScroll.js | 96 | 0 | 0 | 0 | Frontend |
| index.d.ts | 2 | 0 | 0 | 0 | Frontend |
| index.js | 2 | 0 | 0 | 0 | Frontend |
| medium.d.ts | 2 | 0 | 0 | 0 | Frontend |
| medium.js | 2 | 0 | 0 | 0 | Frontend |
| pinchAndZoom.d.ts | 8 | 0 | 0 | 0 | Frontend |
| pinchAndZoom.js | 33 | 0 | 0 | 0 | Frontend |
| sidecar.d.ts | 2 | 0 | 0 | 0 | Frontend |
| sidecar.js | 4 | 0 | 0 | 0 | Frontend |
| types.d.ts | 104 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-remove-scroll/dist/es5`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Combination.d.ts | 3 | 0 | 0 | 0 | Frontend |
| Combination.js | 9 | 0 | 0 | 0 | Frontend |
| SideEffect.d.ts | 5 | 0 | 0 | 0 | Frontend |
| SideEffect.js | 163 | 0 | 0 | 0 | Frontend |
| UI.d.ts | 7 | 0 | 0 | 0 | Frontend |
| UI.js | 39 | 0 | 0 | 0 | Frontend |
| aggresiveCapture.d.ts | 3 | 0 | 0 | 0 | Frontend |
| aggresiveCapture.js | 22 | 0 | 0 | 0 | Frontend |
| handleScroll.d.ts | 3 | 0 | 0 | 0 | Frontend |
| handleScroll.js | 113 | 0 | 0 | 0 | Frontend |
| index.d.ts | 2 | 0 | 0 | 0 | Frontend |
| index.js | 6 | 0 | 0 | 0 | Frontend |
| medium.d.ts | 2 | 0 | 0 | 0 | Frontend |
| medium.js | 5 | 0 | 0 | 0 | Frontend |
| pinchAndZoom.d.ts | 8 | 0 | 0 | 0 | Frontend |
| pinchAndZoom.js | 37 | 0 | 0 | 0 | Frontend |
| sidecar.d.ts | 2 | 0 | 0 | 0 | Frontend |
| sidecar.js | 6 | 0 | 0 | 0 | Frontend |
| types.d.ts | 104 | 0 | 0 | 0 | Frontend |
| types.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-resizable-panels/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| react-resizable-panels.browser.cjs.js | 2483 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.browser.cjs.mjs | 19 | 0 | 0 | 0 | Other |
| react-resizable-panels.browser.development.cjs.js | 2589 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.browser.development.cjs.mjs | 19 | 0 | 0 | 0 | Other |
| react-resizable-panels.browser.development.esm.js | 2550 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.browser.esm.js | 2444 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.cjs.d.mts | 2 | 0 | 0 | 0 | Other |
| react-resizable-panels.cjs.d.mts.map | 1 | 0 | 0 | 0 | Other |
| react-resizable-panels.cjs.d.ts | 2 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.cjs.d.ts.map | 1 | 0 | 0 | 0 | Other |
| react-resizable-panels.cjs.js | 2485 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.cjs.mjs | 19 | 0 | 0 | 0 | Other |
| react-resizable-panels.development.cjs.js | 2596 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.development.cjs.mjs | 19 | 0 | 0 | 0 | Other |
| react-resizable-panels.development.esm.js | 2557 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.development.node.cjs.js | 2362 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.development.node.cjs.mjs | 19 | 0 | 0 | 0 | Other |
| react-resizable-panels.development.node.esm.js | 2323 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.esm.js | 2446 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.node.cjs.js | 2261 | 0 | 0 | 0 | Frontend |
| react-resizable-panels.node.cjs.mjs | 19 | 0 | 0 | 0 | Other |
| react-resizable-panels.node.esm.js | 2222 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-resizable-panels/dist/declarations/src`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Panel.d.ts | 70 | 0 | 0 | 0 | Frontend |
| PanelGroup.d.ts | 38 | 0 | 0 | 0 | Frontend |
| PanelResizeHandle.d.ts | 23 | 0 | 0 | 0 | Frontend |
| PanelResizeHandleRegistry.d.ts | 19 | 0 | 0 | 0 | Frontend |
| constants.d.ts | 15 | 0 | 0 | 0 | Frontend |
| index.d.ts | 21 | 0 | 0 | 0 | Frontend |
| types.d.ts | 3 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-resizable-panels/dist/declarations/src/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| assert.d.ts | 1 | 0 | 0 | 0 | Frontend |
| csp.d.ts | 2 | 0 | 0 | 0 | Frontend |
| cursor.d.ts | 7 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-resizable-panels/dist/declarations/src/utils/dom`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| getPanelElement.d.ts | 1 | 0 | 0 | 0 | Frontend |
| getPanelElementsForGroup.d.ts | 1 | 0 | 0 | 0 | Frontend |
| getPanelGroupElement.d.ts | 1 | 0 | 0 | 0 | Frontend |
| getResizeHandleElement.d.ts | 1 | 0 | 0 | 0 | Frontend |
| getResizeHandleElementIndex.d.ts | 1 | 0 | 0 | 0 | Frontend |
| getResizeHandleElementsForGroup.d.ts | 1 | 0 | 0 | 0 | Frontend |
| getResizeHandlePanelIds.d.ts | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-resizable-panels/dist/declarations/src/utils/rects`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| getIntersectingRectangle.d.ts | 2 | 0 | 0 | 0 | Frontend |
| intersects.d.ts | 2 | 0 | 0 | 0 | Frontend |
| types.d.ts | 6 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-smooth/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Animate.js | 363 | 0 | 0 | 0 | Frontend |
| AnimateGroup.js | 42 | 0 | 0 | 0 | Frontend |
| AnimateGroupChild.js | 119 | 0 | 0 | 0 | Frontend |
| AnimateManager.js | 67 | 0 | 0 | 0 | Frontend |
| configUpdate.js | 141 | 0 | 0 | 0 | Configuration |
| easing.js | 184 | 0 | 0 | 0 | Frontend |
| index.js | 29 | 0 | 0 | 0 | Frontend |
| setRafTimeout.js | 25 | 0 | 0 | 0 | Frontend |
| util.js | 100 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-style-singleton/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-style-singleton/dist/es2015`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| component.d.ts | 21 | 0 | 0 | 0 | Frontend |
| component.js | 16 | 0 | 0 | 0 | Frontend |
| hook.d.ts | 23 | 0 | 0 | 0 | Frontend |
| hook.js | 22 | 0 | 0 | 0 | Frontend |
| index.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.js | 3 | 0 | 0 | 0 | Frontend |
| singleton.d.ts | 4 | 0 | 0 | 0 | Frontend |
| singleton.js | 48 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-style-singleton/dist/es2019`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| component.d.ts | 21 | 0 | 0 | 0 | Frontend |
| component.js | 15 | 0 | 0 | 0 | Frontend |
| hook.d.ts | 23 | 0 | 0 | 0 | Frontend |
| hook.js | 22 | 0 | 0 | 0 | Frontend |
| index.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.js | 3 | 0 | 0 | 0 | Frontend |
| singleton.d.ts | 4 | 0 | 0 | 0 | Frontend |
| singleton.js | 48 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-style-singleton/dist/es5`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| component.d.ts | 21 | 0 | 0 | 0 | Frontend |
| component.js | 20 | 0 | 0 | 0 | Frontend |
| hook.d.ts | 23 | 0 | 0 | 0 | Frontend |
| hook.js | 27 | 0 | 0 | 0 | Frontend |
| index.d.ts | 3 | 0 | 0 | 0 | Frontend |
| index.js | 9 | 0 | 0 | 0 | Frontend |
| singleton.d.ts | 4 | 0 | 0 | 0 | Frontend |
| singleton.js | 52 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/react-transition-group/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| react-transition-group.js | 2840 | 0 | 0 | 0 | Frontend |
| react-transition-group.min.js | 9 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts-scale/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| getNiceTickValues.js | 317 | 0 | 0 | 0 | Frontend |
| index.js | 25 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts-scale/lib/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| arithmetic.js | 115 | 0 | 0 | 0 | Frontend |
| utils.js | 155 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 383 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/cartesian`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Area.js | 551 | 0 | 0 | 0 | Frontend |
| Bar.js | 458 | 0 | 0 | 0 | Frontend |
| Brush.js | 629 | 0 | 0 | 0 | Frontend |
| CartesianAxis.js | 362 | 0 | 0 | 0 | Frontend |
| CartesianGrid.js | 375 | 0 | 0 | 0 | Frontend |
| ErrorBar.js | 163 | 0 | 0 | 0 | Frontend |
| Line.js | 519 | 0 | 0 | 0 | Frontend |
| ReferenceArea.js | 136 | 0 | 0 | 0 | Frontend |
| ReferenceDot.js | 134 | 0 | 0 | 0 | Frontend |
| ReferenceLine.js | 200 | 0 | 0 | 0 | Frontend |
| Scatter.js | 428 | 0 | 0 | 0 | Frontend |
| XAxis.js | 93 | 0 | 0 | 0 | Frontend |
| YAxis.js | 91 | 0 | 0 | 0 | Frontend |
| ZAxis.js | 46 | 0 | 0 | 0 | Frontend |
| getEquidistantTicks.js | 61 | 0 | 0 | 0 | Frontend |
| getTicks.js | 162 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/chart`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AccessibilityManager.js | 116 | 0 | 0 | 0 | Frontend |
| AreaChart.js | 27 | 0 | 0 | 0 | Frontend |
| BarChart.js | 29 | 0 | 0 | 0 | Frontend |
| ComposedChart.js | 34 | 0 | 0 | 0 | Frontend |
| FunnelChart.js | 22 | 0 | 0 | 0 | Frontend |
| LineChart.js | 27 | 0 | 0 | 0 | Frontend |
| PieChart.js | 39 | 0 | 0 | 0 | Frontend |
| RadarChart.js | 36 | 0 | 0 | 0 | Frontend |
| RadialBarChart.js | 39 | 0 | 0 | 0 | Frontend |
| Sankey.js | 676 | 0 | 0 | 0 | Frontend |
| ScatterChart.js | 33 | 0 | 0 | 0 | Frontend |
| SunburstChart.js | 212 | 0 | 0 | 0 | Frontend |
| Treemap.js | 682 | 0 | 0 | 0 | Frontend |
| generateCategoricalChart.js | 2106 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/component`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Cell.js | 14 | 0 | 0 | 0 | Frontend |
| Cursor.js | 87 | 0 | 0 | 0 | Frontend |
| Customized.js | 40 | 0 | 0 | 0 | Frontend |
| DefaultLegendContent.js | 193 | 0 | 0 | 0 | Frontend |
| DefaultTooltipContent.js | 133 | 0 | 0 | 0 | Frontend |
| Label.js | 478 | 0 | 0 | 0 | Frontend |
| LabelList.js | 118 | 0 | 0 | 0 | Frontend |
| Legend.js | 210 | 0 | 0 | 0 | Frontend |
| ResponsiveContainer.js | 167 | 0 | 0 | 0 | Frontend |
| Text.js | 260 | 0 | 0 | 0 | Frontend |
| Tooltip.js | 133 | 0 | 0 | 0 | Frontend |
| TooltipBoundingBox.js | 164 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/container`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Layer.js | 25 | 0 | 0 | 0 | Frontend |
| Surface.js | 42 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/context`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| chartLayoutContext.js | 171 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/numberAxis`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Funnel.js | 389 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/polar`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Pie.js | 561 | 0 | 0 | 0 | Frontend |
| PolarAngleAxis.js | 212 | 0 | 0 | 0 | Frontend |
| PolarGrid.js | 164 | 0 | 0 | 0 | Frontend |
| PolarRadiusAxis.js | 217 | 0 | 0 | 0 | Frontend |
| Radar.js | 327 | 0 | 0 | 0 | Frontend |
| RadialBar.js | 365 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/shape`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Cross.js | 58 | 0 | 0 | 0 | Frontend |
| Curve.js | 124 | 0 | 0 | 0 | Frontend |
| Dot.js | 33 | 0 | 0 | 0 | Frontend |
| Polygon.js | 96 | 0 | 0 | 0 | Frontend |
| Rectangle.js | 176 | 0 | 0 | 0 | Frontend |
| Sector.js | 219 | 0 | 0 | 0 | Frontend |
| Symbols.js | 103 | 0 | 0 | 0 | Frontend |
| Trapezoid.js | 128 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ActiveShapeUtils.js | 215 | 0 | 0 | 0 | Frontend |
| BarUtils.js | 75 | 0 | 0 | 0 | Frontend |
| CartesianUtils.js | 290 | 0 | 0 | 0 | Frontend |
| ChartUtils.js | 1079 | 0 | 0 | 0 | Frontend |
| Constants.js | 7 | 0 | 0 | 0 | Frontend |
| CssPrefixUtils.js | 26 | 0 | 0 | 0 | Frontend |
| DOMUtils.js | 118 | 0 | 0 | 0 | Frontend |
| DataUtils.js | 179 | 0 | 0 | 0 | Frontend |
| DetectReferenceElementsDomain.js | 57 | 0 | 0 | 0 | Frontend |
| Events.js | 10 | 0 | 0 | 0 | Frontend |
| FunnelUtils.js | 40 | 0 | 0 | 0 | Frontend |
| Global.js | 27 | 0 | 0 | 0 | Frontend |
| IfOverflowMatches.js | 14 | 0 | 0 | 0 | Frontend |
| LogUtils.js | 28 | 0 | 0 | 0 | Frontend |
| PolarUtils.js | 215 | 0 | 0 | 0 | Frontend |
| RadialBarUtils.js | 45 | 0 | 0 | 0 | Frontend |
| ReactUtils.js | 311 | 0 | 0 | 0 | Frontend |
| ReduceCSSCalc.js | 180 | 0 | 0 | 0 | Frontend |
| ScatterUtils.js | 35 | 0 | 0 | 0 | Frontend |
| ShallowEqual.js | 20 | 0 | 0 | 0 | Frontend |
| TickUtils.js | 47 | 0 | 0 | 0 | Frontend |
| calculateViewBox.js | 25 | 0 | 0 | 0 | Frontend |
| getEveryNthWithCondition.js | 32 | 0 | 0 | 0 | Frontend |
| getLegendProps.js | 68 | 0 | 0 | 0 | Frontend |
| isDomainSpecifiedByUser.js | 29 | 0 | 0 | 0 | Frontend |
| types.js | 132 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/util/cursor`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| getCursorPoints.js | 45 | 0 | 0 | 0 | Frontend |
| getCursorRectangle.js | 17 | 0 | 0 | 0 | Frontend |
| getRadialCursorPoints.js | 29 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/util/payload`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| getUniqPayload.js | 26 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/recharts/lib/util/tooltip`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| translate.js | 117 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/regexparam/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 43 | 0 | 0 | 0 | Frontend |
| index.min.js | 1 | 0 | 0 | 0 | Frontend |
| index.mjs | 40 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/resolve/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| async.js | 329 | 0 | 0 | 0 | Frontend |
| caller.js | 8 | 0 | 0 | 0 | Frontend |
| core.js | 12 | 0 | 0 | 0 | Frontend |
| core.json | 162 | 0 | 0 | 0 | Configuration |
| homedir.js | 24 | 0 | 0 | 0 | Frontend |
| is-core.js | 5 | 0 | 0 | 0 | Frontend |
| node-modules-paths.js | 42 | 0 | 0 | 0 | Frontend |
| normalize-options.js | 10 | 0 | 0 | 0 | Frontend |
| sync.js | 208 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/resolve/test/resolver/other_path/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| other-lib.js | 0 | 0 | 0 | 0 | Testing |

### Directory: `client/node_modules/rollup/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| getLogFilter.d.ts | 5 | 0 | 0 | 0 | Frontend |
| getLogFilter.js | 69 | 0 | 0 | 0 | Frontend |
| loadConfigFile.d.ts | 20 | 0 | 0 | 0 | Configuration |
| loadConfigFile.js | 29 | 0 | 0 | 0 | Configuration |
| native.js | 129 | 0 | 0 | 0 | Frontend |
| parseAst.d.ts | 4 | 0 | 0 | 0 | Frontend |
| parseAst.js | 22 | 0 | 0 | 0 | Frontend |
| rollup.d.ts | 1185 | 0 | 0 | 0 | Frontend |
| rollup.js | 127 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/rollup/dist/bin`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| rollup | 1912 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/rollup/dist/es`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| getLogFilter.js | 64 | 0 | 0 | 0 | Frontend |
| package.json | 1 | 0 | 0 | 0 | Configuration |
| parseAst.js | 12 | 0 | 0 | 0 | Frontend |
| rollup.js | 17 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/rollup/dist/es/shared`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| node-entry.js | 23919 | 0 | 0 | 0 | Frontend |
| parseAst.js | 2086 | 0 | 0 | 0 | Frontend |
| watch.js | 9297 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/rollup/dist/shared`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| fsevents-importer.js | 37 | 0 | 0 | 0 | Frontend |
| index.js | 9003 | 0 | 0 | 0 | Frontend |
| loadConfigFile.js | 572 | 0 | 0 | 0 | Configuration |
| parseAst.js | 2318 | 0 | 0 | 0 | Frontend |
| rollup.js | 23841 | 0 | 0 | 0 | Frontend |
| watch-cli.js | 542 | 0 | 0 | 0 | Frontend |
| watch.js | 324 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/signal-exit/dist/cjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| browser.d.ts | 12 | 0 | 0 | 0 | Frontend |
| browser.d.ts.map | 1 | 0 | 0 | 0 | Other |
| browser.js | 10 | 0 | 0 | 0 | Frontend |
| browser.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 48 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 279 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| signals.d.ts | 29 | 0 | 0 | 0 | Frontend |
| signals.d.ts.map | 1 | 0 | 0 | 0 | Other |
| signals.js | 42 | 0 | 0 | 0 | Frontend |
| signals.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/signal-exit/dist/mjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| browser.d.ts | 12 | 0 | 0 | 0 | Frontend |
| browser.d.ts.map | 1 | 0 | 0 | 0 | Other |
| browser.js | 4 | 0 | 0 | 0 | Frontend |
| browser.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 48 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 275 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| signals.d.ts | 29 | 0 | 0 | 0 | Frontend |
| signals.d.ts.map | 1 | 0 | 0 | 0 | Other |
| signals.js | 39 | 0 | 0 | 0 | Frontend |
| signals.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/source-map-js/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| array-set.js | 121 | 0 | 0 | 0 | Frontend |
| base64-vlq.js | 140 | 0 | 0 | 0 | Frontend |
| base64.js | 67 | 0 | 0 | 0 | Frontend |
| binary-search.js | 111 | 0 | 0 | 0 | Frontend |
| mapping-list.js | 79 | 0 | 0 | 0 | Frontend |
| quick-sort.js | 132 | 0 | 0 | 0 | Frontend |
| source-map-consumer.d.ts | 1 | 0 | 0 | 0 | Frontend |
| source-map-consumer.js | 1188 | 0 | 0 | 0 | Frontend |
| source-map-generator.d.ts | 1 | 0 | 0 | 0 | Frontend |
| source-map-generator.js | 444 | 0 | 0 | 0 | Frontend |
| source-node.d.ts | 1 | 0 | 0 | 0 | Frontend |
| source-node.js | 413 | 0 | 0 | 0 | Frontend |
| util.js | 594 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CJSImportProcessor.js | 456 | 0 | 0 | 0 | Frontend |
| HelperManager.js | 176 | 0 | 0 | 0 | Frontend |
| NameManager.js | 27 | 0 | 0 | 0 | Frontend |
| Options-gen-types.js | 42 | 0 | 0 | 0 | Frontend |
| Options.js | 101 | 0 | 0 | 0 | Frontend |
| TokenProcessor.js | 357 | 0 | 0 | 0 | Frontend |
| cli.js | 317 | 0 | 0 | 0 | Frontend |
| computeSourceMap.js | 89 | 0 | 0 | 0 | Frontend |
| identifyShadowedGlobals.js | 98 | 0 | 0 | 0 | Frontend |
| index.js | 133 | 0 | 0 | 0 | Frontend |
| register.js | 88 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CJSImportProcessor.js | 456 | 0 | 0 | 0 | Frontend |
| HelperManager.js | 176 | 0 | 0 | 0 | Frontend |
| NameManager.js | 27 | 0 | 0 | 0 | Frontend |
| Options-gen-types.js | 42 | 0 | 0 | 0 | Frontend |
| Options.js | 101 | 0 | 0 | 0 | Frontend |
| TokenProcessor.js | 357 | 0 | 0 | 0 | Frontend |
| cli.js | 317 | 0 | 0 | 0 | Frontend |
| computeSourceMap.js | 89 | 0 | 0 | 0 | Frontend |
| identifyShadowedGlobals.js | 98 | 0 | 0 | 0 | Frontend |
| index.js | 133 | 0 | 0 | 0 | Frontend |
| register.js | 88 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/esm/parser`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 31 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/esm/parser/plugins`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| flow.js | 1105 | 0 | 0 | 0 | Frontend |
| types.js | 37 | 0 | 0 | 0 | Frontend |
| typescript.js | 1632 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/sucrase/dist/esm/parser/plugins/jsx`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 367 | 0 | 0 | 0 | Frontend |
| xhtml.js | 256 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/esm/parser/tokenizer`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 1004 | 0 | 0 | 0 | Frontend |
| keywords.js | 43 | 0 | 0 | 0 | Frontend |
| readWord.js | 64 | 0 | 0 | 0 | Frontend |
| readWordTree.js | 671 | 0 | 0 | 0 | Frontend |
| state.js | 106 | 0 | 0 | 0 | Frontend |
| types.js | 361 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/esm/parser/traverser`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| base.js | 60 | 0 | 0 | 0 | Frontend |
| expression.js | 1022 | 0 | 0 | 0 | Frontend |
| index.js | 18 | 0 | 0 | 0 | Frontend |
| lval.js | 159 | 0 | 0 | 0 | Frontend |
| statement.js | 1332 | 0 | 0 | 0 | Frontend |
| util.js | 104 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/esm/parser/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| charcodes.js | 115 | 0 | 0 | 0 | Frontend |
| identifier.js | 34 | 0 | 0 | 0 | Frontend |
| whitespace.js | 33 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/esm/transformers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CJSImportTransformer.js | 916 | 0 | 0 | 0 | Frontend |
| ESMImportTransformer.js | 415 | 0 | 0 | 0 | Frontend |
| FlowTransformer.js | 182 | 0 | 0 | 0 | Frontend |
| JSXTransformer.js | 733 | 0 | 0 | 0 | Frontend |
| JestHoistTransformer.js | 111 | 0 | 0 | 0 | Frontend |
| NumericSeparatorTransformer.js | 20 | 0 | 0 | 0 | Frontend |
| OptionalCatchBindingTransformer.js | 19 | 0 | 0 | 0 | Frontend |
| OptionalChainingNullishTransformer.js | 155 | 0 | 0 | 0 | Frontend |
| ReactDisplayNameTransformer.js | 160 | 0 | 0 | 0 | Frontend |
| ReactHotLoaderTransformer.js | 69 | 0 | 0 | 0 | Frontend |
| RootTransformer.js | 462 | 0 | 0 | 0 | Frontend |
| Transformer.js | 16 | 0 | 0 | 0 | Frontend |
| TypeScriptTransformer.js | 279 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/sucrase/dist/esm/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| elideImportEquals.js | 29 | 0 | 0 | 0 | Frontend |
| formatTokens.js | 74 | 0 | 0 | 0 | Frontend |
| getClassInfo.js | 352 | 0 | 0 | 0 | Frontend |
| getDeclarationInfo.js | 40 | 0 | 0 | 0 | Frontend |
| getIdentifierNames.js | 15 | 0 | 0 | 0 | Frontend |
| getImportExportSpecifierInfo.js | 92 | 0 | 0 | 0 | Frontend |
| getJSXPragmaInfo.js | 22 | 0 | 0 | 0 | Frontend |
| getNonTypeIdentifiers.js | 43 | 0 | 0 | 0 | Frontend |
| getTSImportedNames.js | 84 | 0 | 0 | 0 | Frontend |
| isAsyncOperation.js | 38 | 0 | 0 | 0 | Frontend |
| isExportFrom.js | 18 | 0 | 0 | 0 | Frontend |
| isIdentifier.js | 81 | 0 | 0 | 0 | Frontend |
| removeMaybeImportAttributes.js | 22 | 0 | 0 | 0 | Frontend |
| shouldElideDefaultExport.js | 38 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/parser`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 31 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/parser/plugins`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| flow.js | 1105 | 0 | 0 | 0 | Frontend |
| types.js | 37 | 0 | 0 | 0 | Frontend |
| typescript.js | 1632 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/sucrase/dist/parser/plugins/jsx`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 367 | 0 | 0 | 0 | Frontend |
| xhtml.js | 256 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/parser/tokenizer`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 1004 | 0 | 0 | 0 | Frontend |
| keywords.js | 43 | 0 | 0 | 0 | Frontend |
| readWord.js | 64 | 0 | 0 | 0 | Frontend |
| readWordTree.js | 671 | 0 | 0 | 0 | Frontend |
| state.js | 106 | 0 | 0 | 0 | Frontend |
| types.js | 361 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/parser/traverser`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| base.js | 60 | 0 | 0 | 0 | Frontend |
| expression.js | 1022 | 0 | 0 | 0 | Frontend |
| index.js | 18 | 0 | 0 | 0 | Frontend |
| lval.js | 159 | 0 | 0 | 0 | Frontend |
| statement.js | 1332 | 0 | 0 | 0 | Frontend |
| util.js | 104 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/parser/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| charcodes.js | 115 | 0 | 0 | 0 | Frontend |
| identifier.js | 34 | 0 | 0 | 0 | Frontend |
| whitespace.js | 33 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/transformers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CJSImportTransformer.js | 916 | 0 | 0 | 0 | Frontend |
| ESMImportTransformer.js | 415 | 0 | 0 | 0 | Frontend |
| FlowTransformer.js | 182 | 0 | 0 | 0 | Frontend |
| JSXTransformer.js | 733 | 0 | 0 | 0 | Frontend |
| JestHoistTransformer.js | 111 | 0 | 0 | 0 | Frontend |
| NumericSeparatorTransformer.js | 20 | 0 | 0 | 0 | Frontend |
| OptionalCatchBindingTransformer.js | 19 | 0 | 0 | 0 | Frontend |
| OptionalChainingNullishTransformer.js | 155 | 0 | 0 | 0 | Frontend |
| ReactDisplayNameTransformer.js | 160 | 0 | 0 | 0 | Frontend |
| ReactHotLoaderTransformer.js | 69 | 0 | 0 | 0 | Frontend |
| RootTransformer.js | 462 | 0 | 0 | 0 | Frontend |
| Transformer.js | 16 | 0 | 0 | 0 | Frontend |
| TypeScriptTransformer.js | 279 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/sucrase/dist/types`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CJSImportProcessor.d.ts | 67 | 0 | 0 | 0 | Frontend |
| HelperManager.d.ts | 15 | 0 | 0 | 0 | Frontend |
| NameManager.d.ts | 7 | 0 | 0 | 0 | Frontend |
| Options-gen-types.d.ts | 9 | 0 | 0 | 0 | Frontend |
| Options.d.ts | 90 | 0 | 0 | 0 | Frontend |
| TokenProcessor.d.ts | 87 | 0 | 0 | 0 | Frontend |
| cli.d.ts | 1 | 0 | 0 | 0 | Frontend |
| computeSourceMap.d.ts | 17 | 0 | 0 | 0 | Frontend |
| identifyShadowedGlobals.d.ts | 12 | 0 | 0 | 0 | Frontend |
| index.d.ts | 26 | 0 | 0 | 0 | Frontend |
| register.d.ts | 14 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/types/parser`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 8 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/types/parser/plugins`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| flow.d.ts | 27 | 0 | 0 | 0 | Frontend |
| types.d.ts | 5 | 0 | 0 | 0 | Frontend |
| typescript.d.ts | 49 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/sucrase/dist/types/parser/plugins/jsx`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 2 | 0 | 0 | 0 | Frontend |
| xhtml.d.ts | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/types/parser/tokenizer`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 93 | 0 | 0 | 0 | Frontend |
| keywords.d.ts | 43 | 0 | 0 | 0 | Frontend |
| readWord.d.ts | 7 | 0 | 0 | 0 | Frontend |
| readWordTree.d.ts | 1 | 0 | 0 | 0 | Frontend |
| state.d.ts | 50 | 0 | 0 | 0 | Frontend |
| types.d.ts | 126 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/types/parser/traverser`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| base.d.ts | 16 | 0 | 0 | 0 | Frontend |
| expression.d.ts | 34 | 0 | 0 | 0 | Frontend |
| index.d.ts | 2 | 0 | 0 | 0 | Frontend |
| lval.d.ts | 9 | 0 | 0 | 0 | Frontend |
| statement.d.ts | 20 | 0 | 0 | 0 | Frontend |
| util.d.ts | 17 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/types/parser/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| charcodes.d.ts | 107 | 0 | 0 | 0 | Frontend |
| identifier.d.ts | 2 | 0 | 0 | 0 | Frontend |
| whitespace.d.ts | 3 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/types/transformers`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CJSImportTransformer.d.ts | 149 | 0 | 0 | 0 | Frontend |
| ESMImportTransformer.d.ts | 52 | 0 | 0 | 0 | Frontend |
| FlowTransformer.d.ts | 79 | 0 | 0 | 0 | Frontend |
| JSXTransformer.d.ts | 144 | 0 | 0 | 0 | Frontend |
| JestHoistTransformer.d.ts | 32 | 0 | 0 | 0 | Frontend |
| NumericSeparatorTransformer.d.ts | 7 | 0 | 0 | 0 | Frontend |
| OptionalCatchBindingTransformer.d.ts | 9 | 0 | 0 | 0 | Frontend |
| OptionalChainingNullishTransformer.d.ts | 36 | 0 | 0 | 0 | Frontend |
| ReactDisplayNameTransformer.d.ts | 29 | 0 | 0 | 0 | Frontend |
| ReactHotLoaderTransformer.d.ts | 12 | 0 | 0 | 0 | Frontend |
| RootTransformer.d.ts | 52 | 0 | 0 | 0 | Frontend |
| Transformer.d.ts | 6 | 0 | 0 | 0 | Frontend |
| TypeScriptTransformer.d.ts | 104 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/sucrase/dist/types/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| elideImportEquals.d.ts | 2 | 0 | 0 | 0 | Frontend |
| formatTokens.d.ts | 2 | 0 | 0 | 0 | Frontend |
| getClassInfo.d.ts | 34 | 0 | 0 | 0 | Frontend |
| getDeclarationInfo.d.ts | 18 | 0 | 0 | 0 | Frontend |
| getIdentifierNames.d.ts | 5 | 0 | 0 | 0 | Frontend |
| getImportExportSpecifierInfo.d.ts | 36 | 0 | 0 | 0 | Frontend |
| getJSXPragmaInfo.d.ts | 8 | 0 | 0 | 0 | Frontend |
| getNonTypeIdentifiers.d.ts | 3 | 0 | 0 | 0 | Frontend |
| getTSImportedNames.d.ts | 9 | 0 | 0 | 0 | Frontend |
| isAsyncOperation.d.ts | 11 | 0 | 0 | 0 | Frontend |
| isExportFrom.d.ts | 6 | 0 | 0 | 0 | Frontend |
| isIdentifier.d.ts | 8 | 0 | 0 | 0 | Frontend |
| removeMaybeImportAttributes.d.ts | 6 | 0 | 0 | 0 | Frontend |
| shouldElideDefaultExport.d.ts | 6 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/sucrase/dist/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| elideImportEquals.js | 29 | 0 | 0 | 0 | Frontend |
| formatTokens.js | 74 | 0 | 0 | 0 | Frontend |
| getClassInfo.js | 352 | 0 | 0 | 0 | Frontend |
| getDeclarationInfo.js | 40 | 0 | 0 | 0 | Frontend |
| getIdentifierNames.js | 15 | 0 | 0 | 0 | Frontend |
| getImportExportSpecifierInfo.js | 92 | 0 | 0 | 0 | Frontend |
| getJSXPragmaInfo.js | 22 | 0 | 0 | 0 | Frontend |
| getNonTypeIdentifiers.js | 43 | 0 | 0 | 0 | Frontend |
| getTSImportedNames.js | 84 | 0 | 0 | 0 | Frontend |
| isAsyncOperation.js | 38 | 0 | 0 | 0 | Frontend |
| isExportFrom.js | 18 | 0 | 0 | 0 | Frontend |
| isIdentifier.js | 81 | 0 | 0 | 0 | Frontend |
| removeMaybeImportAttributes.js | 22 | 0 | 0 | 0 | Frontend |
| shouldElideDefaultExport.js | 38 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwind-merge/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| bundle-cjs.js | 2571 | 0 | 0 | 0 | Frontend |
| bundle-cjs.js.map | 1 | 0 | 0 | 0 | Other |
| bundle-mjs.mjs | 2559 | 0 | 0 | 0 | Other |
| bundle-mjs.mjs.map | 1 | 0 | 0 | 0 | Other |
| types.d.ts | 2234 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwind-merge/dist/es5`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| bundle-cjs.js | 2658 | 0 | 0 | 0 | Frontend |
| bundle-cjs.js.map | 1 | 0 | 0 | 0 | Other |
| bundle-mjs.mjs | 2646 | 0 | 0 | 0 | Other |
| bundle-mjs.mjs.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/tailwind-merge/src/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| class-group-utils.ts | 214 | 0 | 0 | 0 | Frontend |
| config-utils.ts | 12 | 0 | 0 | 0 | Configuration |
| create-tailwind-merge.ts | 50 | 0 | 0 | 0 | Frontend |
| default-config.ts | 1876 | 0 | 0 | 0 | Configuration |
| extend-tailwind-merge.ts | 25 | 0 | 0 | 0 | Frontend |
| from-theme.ts | 13 | 0 | 0 | 0 | Frontend |
| lru-cache.ts | 52 | 0 | 0 | 0 | Frontend |
| merge-classlist.ts | 78 | 0 | 0 | 0 | Frontend |
| merge-configs.ts | 74 | 0 | 0 | 0 | Configuration |
| parse-class-name.ts | 101 | 0 | 0 | 0 | Frontend |
| tw-join.ts | 50 | 0 | 0 | 0 | Frontend |
| tw-merge.ts | 4 | 0 | 0 | 0 | Frontend |
| types.ts | 488 | 0 | 0 | 0 | Frontend |
| validators.ts | 74 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cli-peer-dependencies.js | 36 | 0 | 0 | 0 | Frontend |
| cli.js | 3 | 0 | 0 | 0 | Frontend |
| corePluginList.js | 191 | 0 | 0 | 0 | Frontend |
| corePlugins.js | 4339 | 0 | 0 | 0 | Frontend |
| featureFlags.js | 79 | 0 | 0 | 0 | Frontend |
| index.js | 2 | 0 | 0 | 0 | Frontend |
| plugin.js | 48 | 0 | 0 | 0 | Frontend |
| processTailwindFeatures.js | 62 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib/cli`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 230 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib/cli/build`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| deps.js | 62 | 0 | 0 | 0 | Frontend |
| index.js | 54 | 0 | 0 | 0 | Frontend |
| plugin.js | 373 | 0 | 0 | 0 | Frontend |
| utils.js | 88 | 0 | 0 | 0 | Frontend |
| watching.js | 182 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib/cli/help`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 73 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib/cli/init`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 63 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib/css`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| LICENSE | 25 | 0 | 0 | 0 | Other |
| preflight.css | 386 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cacheInvalidation.js | 92 | 0 | 0 | 0 | Frontend |
| collapseAdjacentRules.js | 61 | 0 | 0 | 0 | Frontend |
| collapseDuplicateDeclarations.js | 85 | 0 | 0 | 0 | Frontend |
| content.js | 247 | 0 | 0 | 0 | Frontend |
| defaultExtractor.js | 273 | 0 | 0 | 0 | Frontend |
| evaluateTailwindFunctions.js | 238 | 0 | 0 | 0 | Frontend |
| expandApplyAtRules.js | 553 | 0 | 0 | 0 | Frontend |
| expandTailwindAtRules.js | 279 | 0 | 0 | 0 | Frontend |
| findAtConfigPath.js | 46 | 0 | 0 | 0 | Configuration |
| generateRules.js | 907 | 0 | 0 | 0 | Frontend |
| getModuleDependencies.js | 99 | 0 | 0 | 0 | Frontend |
| load-config.js | 65 | 0 | 0 | 0 | Configuration |
| normalizeTailwindDirectives.js | 89 | 0 | 0 | 0 | Frontend |
| offsets.js | 355 | 0 | 0 | 0 | Frontend |
| partitionApplyAtRules.js | 58 | 0 | 0 | 0 | Frontend |
| regex.js | 74 | 0 | 0 | 0 | Frontend |
| remap-bitfield.js | 89 | 0 | 0 | 0 | Frontend |
| resolveDefaultsAtRules.js | 165 | 0 | 0 | 0 | Frontend |
| setupContextUtils.js | 1298 | 0 | 0 | 0 | Frontend |
| setupTrackingContext.js | 166 | 0 | 0 | 0 | Frontend |
| sharedState.js | 79 | 0 | 0 | 0 | Frontend |
| substituteScreenAtRules.js | 31 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib/postcss-plugins/nesting`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 42 | 0 | 0 | 0 | Documentation |
| index.js | 21 | 0 | 0 | 0 | Frontend |
| plugin.js | 89 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib/public`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| colors.js | 355 | 0 | 0 | 0 | Frontend |
| create-plugin.js | 17 | 0 | 0 | 0 | Frontend |
| default-config.js | 18 | 0 | 0 | 0 | Configuration |
| default-theme.js | 18 | 0 | 0 | 0 | Frontend |
| load-config.js | 12 | 0 | 0 | 0 | Configuration |
| resolve-config.js | 24 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/tailwindcss/lib/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| applyImportantSelector.js | 38 | 0 | 0 | 0 | Frontend |
| bigSign.js | 13 | 0 | 0 | 0 | Frontend |
| buildMediaQuery.js | 27 | 0 | 0 | 0 | Frontend |
| cloneDeep.js | 22 | 0 | 0 | 0 | Frontend |
| cloneNodes.js | 54 | 0 | 0 | 0 | Frontend |
| color.js | 116 | 0 | 0 | 0 | Frontend |
| colorNames.js | 752 | 0 | 0 | 0 | Frontend |
| configurePlugins.js | 23 | 0 | 0 | 0 | Configuration |
| createPlugin.js | 32 | 0 | 0 | 0 | Frontend |
| createUtilityPlugin.js | 53 | 0 | 0 | 0 | Frontend |
| dataTypes.js | 444 | 0 | 0 | 0 | Frontend |
| defaults.js | 27 | 0 | 0 | 0 | Frontend |
| escapeClassName.js | 24 | 0 | 0 | 0 | Frontend |
| escapeCommas.js | 13 | 0 | 0 | 0 | Frontend |
| flattenColorPalette.js | 18 | 0 | 0 | 0 | Frontend |
| formatVariantSelector.js | 270 | 0 | 0 | 0 | Frontend |
| getAllConfigs.js | 50 | 0 | 0 | 0 | Configuration |
| hashConfig.js | 21 | 0 | 0 | 0 | Configuration |
| isKeyframeRule.js | 13 | 0 | 0 | 0 | Frontend |
| isPlainObject.js | 17 | 0 | 0 | 0 | Frontend |
| isSyntacticallyValidPropertyValue.js | 74 | 0 | 0 | 0 | Frontend |
| log.js | 61 | 0 | 0 | 0 | Frontend |
| nameClass.js | 49 | 0 | 0 | 0 | Frontend |
| negateValue.js | 36 | 0 | 0 | 0 | Frontend |
| normalizeConfig.js | 281 | 0 | 0 | 0 | Configuration |
| normalizeScreens.js | 178 | 0 | 0 | 0 | Frontend |
| parseAnimationValue.js | 93 | 0 | 0 | 0 | Frontend |
| parseBoxShadowValue.js | 88 | 0 | 0 | 0 | Frontend |
| parseDependency.js | 47 | 0 | 0 | 0 | Frontend |
| parseGlob.js | 35 | 0 | 0 | 0 | Frontend |
| parseObjectStyles.js | 36 | 0 | 0 | 0 | Frontend |
| pluginUtils.js | 289 | 0 | 0 | 0 | Frontend |
| prefixSelector.js | 39 | 0 | 0 | 0 | Frontend |
| pseudoElements.js | 212 | 0 | 0 | 0 | Frontend |
| removeAlphaVariables.js | 33 | 0 | 0 | 0 | Frontend |
| resolveConfig.js | 256 | 0 | 0 | 0 | Configuration |
| resolveConfigPath.js | 72 | 0 | 0 | 0 | Configuration |
| responsive.js | 24 | 0 | 0 | 0 | Frontend |
| splitAtTopLevelOnly.js | 47 | 0 | 0 | 0 | Frontend |
| tap.js | 14 | 0 | 0 | 0 | Frontend |
| toColorValue.js | 13 | 0 | 0 | 0 | Frontend |
| toPath.js | 32 | 0 | 0 | 0 | Frontend |
| transformThemeValue.js | 73 | 0 | 0 | 0 | Frontend |
| validateConfig.js | 37 | 0 | 0 | 0 | Configuration |
| validateFormalSyntax.js | 26 | 0 | 0 | 0 | Frontend |
| withAlphaVariable.js | 79 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/lib/value-parser`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| LICENSE | 22 | 0 | 0 | 0 | Other |
| README.md | 3 | 0 | 0 | 0 | Documentation |
| index.d.js | 2 | 0 | 0 | 0 | Frontend |
| index.js | 22 | 0 | 0 | 0 | Frontend |
| parse.js | 259 | 0 | 0 | 0 | Frontend |
| stringify.js | 38 | 0 | 0 | 0 | Frontend |
| unit.js | 86 | 0 | 0 | 0 | Frontend |
| walk.js | 16 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/node_modules/jiti/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| babel.d.ts | 2 | 0 | 0 | 0 | Frontend |
| babel.js | 227 | 0 | 0 | 0 | Frontend |
| jiti.d.ts | 20 | 0 | 0 | 0 | Frontend |
| jiti.js | 1 | 0 | 0 | 0 | Frontend |
| types.d.ts | 35 | 0 | 0 | 0 | Frontend |
| utils.d.ts | 8 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/node_modules/jiti/dist/plugins`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| babel-plugin-transform-import-meta.d.ts | 4 | 0 | 0 | 0 | Frontend |
| import-meta-env.d.ts | 5 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/node_modules/jiti/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 15 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/node_modules/postcss-selector-parser/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.js | 17 | 0 | 0 | 0 | Frontend |
| parser.js | 1015 | 0 | 0 | 0 | Frontend |
| processor.js | 170 | 0 | 0 | 0 | Frontend |
| sortAscending.js | 11 | 0 | 0 | 0 | Frontend |
| tokenTypes.js | 70 | 0 | 0 | 0 | Frontend |
| tokenize.js | 239 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/node_modules/postcss-selector-parser/dist/selectors`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| attribute.js | 448 | 0 | 0 | 0 | Frontend |
| className.js | 50 | 0 | 0 | 0 | Frontend |
| combinator.js | 21 | 0 | 0 | 0 | Frontend |
| comment.js | 21 | 0 | 0 | 0 | Frontend |
| constructors.js | 65 | 0 | 0 | 0 | Frontend |
| container.js | 308 | 0 | 0 | 0 | Frontend |
| guards.js | 58 | 0 | 0 | 0 | Frontend |
| id.js | 25 | 0 | 0 | 0 | Frontend |
| index.js | 21 | 0 | 0 | 0 | Frontend |
| namespace.js | 80 | 0 | 0 | 0 | Frontend |
| nesting.js | 22 | 0 | 0 | 0 | Frontend |
| node.js | 192 | 0 | 0 | 0 | Frontend |
| pseudo.js | 26 | 0 | 0 | 0 | Frontend |
| root.js | 44 | 0 | 0 | 0 | Frontend |
| selector.js | 21 | 0 | 0 | 0 | Frontend |
| string.js | 21 | 0 | 0 | 0 | Frontend |
| tag.js | 21 | 0 | 0 | 0 | Frontend |
| types.js | 28 | 0 | 0 | 0 | Frontend |
| universal.js | 22 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/node_modules/postcss-selector-parser/dist/util`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ensureObject.js | 17 | 0 | 0 | 0 | Frontend |
| getProp.js | 18 | 0 | 0 | 0 | Frontend |
| index.js | 13 | 0 | 0 | 0 | Frontend |
| stripComments.js | 21 | 0 | 0 | 0 | Frontend |
| unesc.js | 76 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/src/cli/build`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| deps.js | 56 | 0 | 0 | 0 | Frontend |
| index.js | 49 | 0 | 0 | 0 | Frontend |
| plugin.js | 441 | 0 | 0 | 0 | Frontend |
| utils.js | 76 | 0 | 0 | 0 | Frontend |
| watching.js | 229 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tailwindcss/src/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cacheInvalidation.js | 52 | 0 | 0 | 0 | Frontend |
| collapseAdjacentRules.js | 58 | 0 | 0 | 0 | Frontend |
| collapseDuplicateDeclarations.js | 93 | 0 | 0 | 0 | Frontend |
| content.js | 295 | 0 | 0 | 0 | Frontend |
| defaultExtractor.js | 255 | 0 | 0 | 0 | Frontend |
| evaluateTailwindFunctions.js | 272 | 0 | 0 | 0 | Frontend |
| expandApplyAtRules.js | 637 | 0 | 0 | 0 | Frontend |
| expandTailwindAtRules.js | 282 | 0 | 0 | 0 | Frontend |
| findAtConfigPath.js | 48 | 0 | 0 | 0 | Configuration |
| generateRules.js | 951 | 0 | 0 | 0 | Frontend |
| getModuleDependencies.js | 79 | 0 | 0 | 0 | Frontend |
| load-config.ts | 61 | 0 | 0 | 0 | Configuration |
| normalizeTailwindDirectives.js | 84 | 0 | 0 | 0 | Frontend |
| offsets.js | 432 | 0 | 0 | 0 | Frontend |
| partitionApplyAtRules.js | 52 | 0 | 0 | 0 | Frontend |
| regex.js | 74 | 0 | 0 | 0 | Frontend |
| remap-bitfield.js | 82 | 0 | 0 | 0 | Frontend |
| resolveDefaultsAtRules.js | 165 | 0 | 0 | 0 | Frontend |
| setupContextUtils.js | 1371 | 0 | 0 | 0 | Frontend |
| setupTrackingContext.js | 169 | 0 | 0 | 0 | Frontend |
| sharedState.js | 57 | 0 | 0 | 0 | Frontend |
| substituteScreenAtRules.js | 19 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tapable/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| AsyncParallelBailHook.js | 87 | 0 | 0 | 0 | Frontend |
| AsyncParallelHook.js | 37 | 0 | 0 | 0 | Frontend |
| AsyncSeriesBailHook.js | 42 | 0 | 0 | 0 | Frontend |
| AsyncSeriesHook.js | 37 | 0 | 0 | 0 | Frontend |
| AsyncSeriesLoopHook.js | 37 | 0 | 0 | 0 | Frontend |
| AsyncSeriesWaterfallHook.js | 48 | 0 | 0 | 0 | Frontend |
| Hook.js | 183 | 0 | 0 | 0 | Frontend |
| HookCodeFactory.js | 454 | 0 | 0 | 0 | Frontend |
| HookMap.js | 69 | 0 | 0 | 0 | Frontend |
| MultiHook.js | 52 | 0 | 0 | 0 | Frontend |
| SyncBailHook.js | 51 | 0 | 0 | 0 | Frontend |
| SyncHook.js | 46 | 0 | 0 | 0 | Frontend |
| SyncLoopHook.js | 46 | 0 | 0 | 0 | Frontend |
| SyncWaterfallHook.js | 58 | 0 | 0 | 0 | Frontend |
| index.js | 19 | 0 | 0 | 0 | Frontend |
| util-browser.js | 18 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tar/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create.d.ts | 3 | 0 | 0 | 0 | Frontend |
| create.d.ts.map | 1 | 0 | 0 | 0 | Other |
| create.js | 83 | 0 | 0 | 0 | Frontend |
| create.js.map | 1 | 0 | 0 | 0 | Other |
| cwd-error.d.ts | 8 | 0 | 0 | 0 | Frontend |
| cwd-error.d.ts.map | 1 | 0 | 0 | 0 | Other |
| cwd-error.js | 18 | 0 | 0 | 0 | Frontend |
| cwd-error.js.map | 1 | 0 | 0 | 0 | Other |
| extract.d.ts | 3 | 0 | 0 | 0 | Frontend |
| extract.d.ts.map | 1 | 0 | 0 | 0 | Other |
| extract.js | 78 | 0 | 0 | 0 | Frontend |
| extract.js.map | 1 | 0 | 0 | 0 | Other |
| get-write-flag.d.ts | 2 | 0 | 0 | 0 | Frontend |
| get-write-flag.d.ts.map | 1 | 0 | 0 | 0 | Other |
| get-write-flag.js | 29 | 0 | 0 | 0 | Frontend |
| get-write-flag.js.map | 1 | 0 | 0 | 0 | Other |
| header.d.ts | 55 | 0 | 0 | 0 | Frontend |
| header.d.ts.map | 1 | 0 | 0 | 0 | Other |
| header.js | 315 | 0 | 0 | 0 | Frontend |
| header.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 20 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 54 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| large-numbers.d.ts | 5 | 0 | 0 | 0 | Frontend |
| large-numbers.d.ts.map | 1 | 0 | 0 | 0 | Other |
| large-numbers.js | 99 | 0 | 0 | 0 | Frontend |
| large-numbers.js.map | 1 | 0 | 0 | 0 | Other |
| list.d.ts | 7 | 0 | 0 | 0 | Frontend |
| list.d.ts.map | 1 | 0 | 0 | 0 | Other |
| list.js | 140 | 0 | 0 | 0 | Frontend |
| list.js.map | 1 | 0 | 0 | 0 | Other |
| make-command.d.ts | 49 | 0 | 0 | 0 | Frontend |
| make-command.d.ts.map | 1 | 0 | 0 | 0 | Other |
| make-command.js | 61 | 0 | 0 | 0 | Frontend |
| make-command.js.map | 1 | 0 | 0 | 0 | Other |
| mkdir.d.ts | 26 | 0 | 0 | 0 | Frontend |
| mkdir.d.ts.map | 1 | 0 | 0 | 0 | Other |
| mkdir.js | 188 | 0 | 0 | 0 | Frontend |
| mkdir.js.map | 1 | 0 | 0 | 0 | Other |
| mode-fix.d.ts | 2 | 0 | 0 | 0 | Frontend |
| mode-fix.d.ts.map | 1 | 0 | 0 | 0 | Other |
| mode-fix.js | 29 | 0 | 0 | 0 | Frontend |
| mode-fix.js.map | 1 | 0 | 0 | 0 | Other |
| normalize-unicode.d.ts | 2 | 0 | 0 | 0 | Frontend |
| normalize-unicode.d.ts.map | 1 | 0 | 0 | 0 | Other |
| normalize-unicode.js | 34 | 0 | 0 | 0 | Frontend |
| normalize-unicode.js.map | 1 | 0 | 0 | 0 | Other |
| normalize-windows-path.d.ts | 2 | 0 | 0 | 0 | Frontend |
| normalize-windows-path.d.ts.map | 1 | 0 | 0 | 0 | Other |
| normalize-windows-path.js | 12 | 0 | 0 | 0 | Frontend |
| normalize-windows-path.js.map | 1 | 0 | 0 | 0 | Other |
| options.d.ts | 621 | 0 | 0 | 0 | Frontend |
| options.d.ts.map | 1 | 0 | 0 | 0 | Other |
| options.js | 66 | 0 | 0 | 0 | Frontend |
| options.js.map | 1 | 0 | 0 | 0 | Other |
| pack.d.ts | 103 | 0 | 0 | 0 | Frontend |
| pack.d.ts.map | 1 | 0 | 0 | 0 | Other |
| pack.js | 494 | 0 | 0 | 0 | Frontend |
| pack.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| parse.d.ts | 88 | 0 | 0 | 0 | Frontend |
| parse.d.ts.map | 1 | 0 | 0 | 0 | Other |
| parse.js | 620 | 0 | 0 | 0 | Frontend |
| parse.js.map | 1 | 0 | 0 | 0 | Other |
| path-reservations.d.ts | 11 | 0 | 0 | 0 | Frontend |
| path-reservations.d.ts.map | 1 | 0 | 0 | 0 | Other |
| path-reservations.js | 170 | 0 | 0 | 0 | Frontend |
| path-reservations.js.map | 1 | 0 | 0 | 0 | Other |
| pax.d.ts | 28 | 0 | 0 | 0 | Frontend |
| pax.d.ts.map | 1 | 0 | 0 | 0 | Other |
| pax.js | 158 | 0 | 0 | 0 | Frontend |
| pax.js.map | 1 | 0 | 0 | 0 | Other |
| read-entry.d.ts | 38 | 0 | 0 | 0 | Frontend |
| read-entry.d.ts.map | 1 | 0 | 0 | 0 | Other |
| read-entry.js | 140 | 0 | 0 | 0 | Frontend |
| read-entry.js.map | 1 | 0 | 0 | 0 | Other |
| replace.d.ts | 2 | 0 | 0 | 0 | Frontend |
| replace.d.ts.map | 1 | 0 | 0 | 0 | Other |
| replace.js | 232 | 0 | 0 | 0 | Frontend |
| replace.js.map | 1 | 0 | 0 | 0 | Other |
| strip-absolute-path.d.ts | 2 | 0 | 0 | 0 | Frontend |
| strip-absolute-path.d.ts.map | 1 | 0 | 0 | 0 | Other |
| strip-absolute-path.js | 29 | 0 | 0 | 0 | Frontend |
| strip-absolute-path.js.map | 1 | 0 | 0 | 0 | Other |
| strip-trailing-slashes.d.ts | 2 | 0 | 0 | 0 | Frontend |
| strip-trailing-slashes.d.ts.map | 1 | 0 | 0 | 0 | Other |
| strip-trailing-slashes.js | 18 | 0 | 0 | 0 | Frontend |
| strip-trailing-slashes.js.map | 1 | 0 | 0 | 0 | Other |
| symlink-error.d.ts | 9 | 0 | 0 | 0 | Frontend |
| symlink-error.d.ts.map | 1 | 0 | 0 | 0 | Other |
| symlink-error.js | 19 | 0 | 0 | 0 | Frontend |
| symlink-error.js.map | 1 | 0 | 0 | 0 | Other |
| types.d.ts | 7 | 0 | 0 | 0 | Frontend |
| types.d.ts.map | 1 | 0 | 0 | 0 | Other |
| types.js | 50 | 0 | 0 | 0 | Frontend |
| types.js.map | 1 | 0 | 0 | 0 | Other |
| unpack.d.ts | 96 | 0 | 0 | 0 | Frontend |
| unpack.d.ts.map | 1 | 0 | 0 | 0 | Other |
| unpack.js | 871 | 0 | 0 | 0 | Frontend |
| unpack.js.map | 1 | 0 | 0 | 0 | Other |
| update.d.ts | 2 | 0 | 0 | 0 | Frontend |
| update.d.ts.map | 1 | 0 | 0 | 0 | Other |
| update.js | 33 | 0 | 0 | 0 | Frontend |
| update.js.map | 1 | 0 | 0 | 0 | Other |
| warn-method.d.ts | 26 | 0 | 0 | 0 | Frontend |
| warn-method.d.ts.map | 1 | 0 | 0 | 0 | Other |
| warn-method.js | 31 | 0 | 0 | 0 | Frontend |
| warn-method.js.map | 1 | 0 | 0 | 0 | Other |
| winchars.d.ts | 3 | 0 | 0 | 0 | Frontend |
| winchars.d.ts.map | 1 | 0 | 0 | 0 | Other |
| winchars.js | 14 | 0 | 0 | 0 | Frontend |
| winchars.js.map | 1 | 0 | 0 | 0 | Other |
| write-entry.d.ts | 133 | 0 | 0 | 0 | Frontend |
| write-entry.d.ts.map | 1 | 0 | 0 | 0 | Other |
| write-entry.js | 689 | 0 | 0 | 0 | Frontend |
| write-entry.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/tar/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create.d.ts | 3 | 0 | 0 | 0 | Frontend |
| create.d.ts.map | 1 | 0 | 0 | 0 | Other |
| create.js | 77 | 0 | 0 | 0 | Frontend |
| create.js.map | 1 | 0 | 0 | 0 | Other |
| cwd-error.d.ts | 8 | 0 | 0 | 0 | Frontend |
| cwd-error.d.ts.map | 1 | 0 | 0 | 0 | Other |
| cwd-error.js | 14 | 0 | 0 | 0 | Frontend |
| cwd-error.js.map | 1 | 0 | 0 | 0 | Other |
| extract.d.ts | 3 | 0 | 0 | 0 | Frontend |
| extract.d.ts.map | 1 | 0 | 0 | 0 | Other |
| extract.js | 49 | 0 | 0 | 0 | Frontend |
| extract.js.map | 1 | 0 | 0 | 0 | Other |
| get-write-flag.d.ts | 2 | 0 | 0 | 0 | Frontend |
| get-write-flag.d.ts.map | 1 | 0 | 0 | 0 | Other |
| get-write-flag.js | 23 | 0 | 0 | 0 | Frontend |
| get-write-flag.js.map | 1 | 0 | 0 | 0 | Other |
| header.d.ts | 55 | 0 | 0 | 0 | Frontend |
| header.d.ts.map | 1 | 0 | 0 | 0 | Other |
| header.js | 288 | 0 | 0 | 0 | Frontend |
| header.js.map | 1 | 0 | 0 | 0 | Other |
| index.d.ts | 20 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 20 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| large-numbers.d.ts | 5 | 0 | 0 | 0 | Frontend |
| large-numbers.d.ts.map | 1 | 0 | 0 | 0 | Other |
| large-numbers.js | 94 | 0 | 0 | 0 | Frontend |
| large-numbers.js.map | 1 | 0 | 0 | 0 | Other |
| list.d.ts | 7 | 0 | 0 | 0 | Frontend |
| list.d.ts.map | 1 | 0 | 0 | 0 | Other |
| list.js | 110 | 0 | 0 | 0 | Frontend |
| list.js.map | 1 | 0 | 0 | 0 | Other |
| make-command.d.ts | 49 | 0 | 0 | 0 | Frontend |
| make-command.d.ts.map | 1 | 0 | 0 | 0 | Other |
| make-command.js | 57 | 0 | 0 | 0 | Frontend |
| make-command.js.map | 1 | 0 | 0 | 0 | Other |
| mkdir.d.ts | 26 | 0 | 0 | 0 | Frontend |
| mkdir.d.ts.map | 1 | 0 | 0 | 0 | Other |
| mkdir.js | 180 | 0 | 0 | 0 | Frontend |
| mkdir.js.map | 1 | 0 | 0 | 0 | Other |
| mode-fix.d.ts | 2 | 0 | 0 | 0 | Frontend |
| mode-fix.d.ts.map | 1 | 0 | 0 | 0 | Other |
| mode-fix.js | 25 | 0 | 0 | 0 | Frontend |
| mode-fix.js.map | 1 | 0 | 0 | 0 | Other |
| normalize-unicode.d.ts | 2 | 0 | 0 | 0 | Frontend |
| normalize-unicode.d.ts.map | 1 | 0 | 0 | 0 | Other |
| normalize-unicode.js | 30 | 0 | 0 | 0 | Frontend |
| normalize-unicode.js.map | 1 | 0 | 0 | 0 | Other |
| normalize-windows-path.d.ts | 2 | 0 | 0 | 0 | Frontend |
| normalize-windows-path.d.ts.map | 1 | 0 | 0 | 0 | Other |
| normalize-windows-path.js | 9 | 0 | 0 | 0 | Frontend |
| normalize-windows-path.js.map | 1 | 0 | 0 | 0 | Other |
| options.d.ts | 621 | 0 | 0 | 0 | Frontend |
| options.d.ts.map | 1 | 0 | 0 | 0 | Other |
| options.js | 54 | 0 | 0 | 0 | Frontend |
| options.js.map | 1 | 0 | 0 | 0 | Other |
| pack.d.ts | 103 | 0 | 0 | 0 | Frontend |
| pack.d.ts.map | 1 | 0 | 0 | 0 | Other |
| pack.js | 462 | 0 | 0 | 0 | Frontend |
| pack.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |
| parse.d.ts | 88 | 0 | 0 | 0 | Frontend |
| parse.d.ts.map | 1 | 0 | 0 | 0 | Other |
| parse.js | 616 | 0 | 0 | 0 | Frontend |
| parse.js.map | 1 | 0 | 0 | 0 | Other |
| path-reservations.d.ts | 11 | 0 | 0 | 0 | Frontend |
| path-reservations.d.ts.map | 1 | 0 | 0 | 0 | Other |
| path-reservations.js | 166 | 0 | 0 | 0 | Frontend |
| path-reservations.js.map | 1 | 0 | 0 | 0 | Other |
| pax.d.ts | 28 | 0 | 0 | 0 | Frontend |
| pax.d.ts.map | 1 | 0 | 0 | 0 | Other |
| pax.js | 154 | 0 | 0 | 0 | Frontend |
| pax.js.map | 1 | 0 | 0 | 0 | Other |
| read-entry.d.ts | 38 | 0 | 0 | 0 | Frontend |
| read-entry.d.ts.map | 1 | 0 | 0 | 0 | Other |
| read-entry.js | 136 | 0 | 0 | 0 | Frontend |
| read-entry.js.map | 1 | 0 | 0 | 0 | Other |
| replace.d.ts | 2 | 0 | 0 | 0 | Frontend |
| replace.d.ts.map | 1 | 0 | 0 | 0 | Other |
| replace.js | 226 | 0 | 0 | 0 | Frontend |
| replace.js.map | 1 | 0 | 0 | 0 | Other |
| strip-absolute-path.d.ts | 2 | 0 | 0 | 0 | Frontend |
| strip-absolute-path.d.ts.map | 1 | 0 | 0 | 0 | Other |
| strip-absolute-path.js | 25 | 0 | 0 | 0 | Frontend |
| strip-absolute-path.js.map | 1 | 0 | 0 | 0 | Other |
| strip-trailing-slashes.d.ts | 2 | 0 | 0 | 0 | Frontend |
| strip-trailing-slashes.d.ts.map | 1 | 0 | 0 | 0 | Other |
| strip-trailing-slashes.js | 14 | 0 | 0 | 0 | Frontend |
| strip-trailing-slashes.js.map | 1 | 0 | 0 | 0 | Other |
| symlink-error.d.ts | 9 | 0 | 0 | 0 | Frontend |
| symlink-error.d.ts.map | 1 | 0 | 0 | 0 | Other |
| symlink-error.js | 15 | 0 | 0 | 0 | Frontend |
| symlink-error.js.map | 1 | 0 | 0 | 0 | Other |
| types.d.ts | 7 | 0 | 0 | 0 | Frontend |
| types.d.ts.map | 1 | 0 | 0 | 0 | Other |
| types.js | 45 | 0 | 0 | 0 | Frontend |
| types.js.map | 1 | 0 | 0 | 0 | Other |
| unpack.d.ts | 96 | 0 | 0 | 0 | Frontend |
| unpack.d.ts.map | 1 | 0 | 0 | 0 | Other |
| unpack.js | 840 | 0 | 0 | 0 | Frontend |
| unpack.js.map | 1 | 0 | 0 | 0 | Other |
| update.d.ts | 2 | 0 | 0 | 0 | Frontend |
| update.d.ts.map | 1 | 0 | 0 | 0 | Other |
| update.js | 30 | 0 | 0 | 0 | Frontend |
| update.js.map | 1 | 0 | 0 | 0 | Other |
| warn-method.d.ts | 26 | 0 | 0 | 0 | Frontend |
| warn-method.d.ts.map | 1 | 0 | 0 | 0 | Other |
| warn-method.js | 27 | 0 | 0 | 0 | Frontend |
| warn-method.js.map | 1 | 0 | 0 | 0 | Other |
| winchars.d.ts | 3 | 0 | 0 | 0 | Frontend |
| winchars.d.ts.map | 1 | 0 | 0 | 0 | Other |
| winchars.js | 9 | 0 | 0 | 0 | Frontend |
| winchars.js.map | 1 | 0 | 0 | 0 | Other |
| write-entry.d.ts | 133 | 0 | 0 | 0 | Frontend |
| write-entry.d.ts.map | 1 | 0 | 0 | 0 | Other |
| write-entry.js | 657 | 0 | 0 | 0 | Frontend |
| write-entry.js.map | 1 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/tar/node_modules/yallist/dist/commonjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 39 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 384 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/tar/node_modules/yallist/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 39 | 0 | 0 | 0 | Frontend |
| index.d.ts.map | 1 | 0 | 0 | 0 | Other |
| index.js | 379 | 0 | 0 | 0 | Frontend |
| index.js.map | 1 | 0 | 0 | 0 | Other |
| package.json | 3 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/tiny-invariant/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| tiny-invariant.cjs.js | 17 | 0 | 0 | 0 | Frontend |
| tiny-invariant.d.ts | 21 | 0 | 0 | 0 | Frontend |
| tiny-invariant.esm.js | 15 | 0 | 0 | 0 | Frontend |
| tiny-invariant.js | 23 | 0 | 0 | 0 | Frontend |
| tiny-invariant.min.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tiny-invariant/dist/esm`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| package.json | 1 | 0 | 0 | 0 | Configuration |
| tiny-invariant.d.ts | 21 | 0 | 0 | 0 | Frontend |
| tiny-invariant.js | 15 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tinyglobby/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.cjs | 350 | 0 | 0 | 0 | Other |
| index.d.cts | 147 | 0 | 0 | 0 | Other |
| index.d.mts | 147 | 0 | 0 | 0 | Other |
| index.mjs | 318 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/tinyglobby/node_modules/fdir/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.cjs | 588 | 0 | 0 | 0 | Other |
| index.d.cts | 155 | 0 | 0 | 0 | Other |
| index.d.mts | 155 | 0 | 0 | 0 | Other |
| index.mjs | 570 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/tinyglobby/node_modules/picomatch/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constants.js | 180 | 0 | 0 | 0 | Frontend |
| parse.js | 1085 | 0 | 0 | 0 | Frontend |
| picomatch.js | 341 | 0 | 0 | 0 | Frontend |
| scan.js | 391 | 0 | 0 | 0 | Frontend |
| utils.js | 72 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/ts-interface-checker/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.ts | 124 | 0 | 0 | 0 | Frontend |
| index.js | 224 | 0 | 0 | 0 | Frontend |
| types.d.ts | 181 | 0 | 0 | 0 | Frontend |
| types.js | 566 | 0 | 0 | 0 | Frontend |
| util.d.ts | 55 | 0 | 0 | 0 | Frontend |
| util.js | 130 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/tw-animate-css/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| tw-animate-prefix.css | 1 | 0 | 0 | 0 | Frontend |
| tw-animate.css | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/typescript/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| _tsc.js | 133792 | 0 | 0 | 0 | Scripting |
| _tsserver.js | 659 | 0 | 0 | 0 | Scripting |
| _typingsInstaller.js | 222 | 0 | 0 | 0 | Scripting |
| lib.d.ts | 22 | 0 | 0 | 0 | Scripting |
| lib.decorators.d.ts | 384 | 0 | 0 | 0 | Scripting |
| lib.decorators.legacy.d.ts | 22 | 0 | 0 | 0 | Scripting |
| lib.dom.asynciterable.d.ts | 41 | 0 | 0 | 0 | Scripting |
| lib.dom.d.ts | 39429 | 0 | 0 | 0 | Scripting |
| lib.dom.iterable.d.ts | 571 | 0 | 0 | 0 | Scripting |
| lib.es2015.collection.d.ts | 147 | 0 | 0 | 0 | Scripting |
| lib.es2015.core.d.ts | 597 | 0 | 0 | 0 | Scripting |
| lib.es2015.d.ts | 28 | 0 | 0 | 0 | Scripting |
| lib.es2015.generator.d.ts | 77 | 0 | 0 | 0 | Scripting |
| lib.es2015.iterable.d.ts | 605 | 0 | 0 | 0 | Scripting |
| lib.es2015.promise.d.ts | 81 | 0 | 0 | 0 | Scripting |
| lib.es2015.proxy.d.ts | 128 | 0 | 0 | 0 | Scripting |
| lib.es2015.reflect.d.ts | 144 | 0 | 0 | 0 | Scripting |
| lib.es2015.symbol.d.ts | 46 | 0 | 0 | 0 | Scripting |
| lib.es2015.symbol.wellknown.d.ts | 326 | 0 | 0 | 0 | Scripting |
| lib.es2016.array.include.d.ts | 116 | 0 | 0 | 0 | Scripting |
| lib.es2016.d.ts | 21 | 0 | 0 | 0 | Scripting |
| lib.es2016.full.d.ts | 23 | 0 | 0 | 0 | Scripting |
| lib.es2016.intl.d.ts | 31 | 0 | 0 | 0 | Scripting |
| lib.es2017.arraybuffer.d.ts | 21 | 0 | 0 | 0 | Scripting |
| lib.es2017.d.ts | 26 | 0 | 0 | 0 | Scripting |
| lib.es2017.date.d.ts | 31 | 0 | 0 | 0 | Scripting |
| lib.es2017.full.d.ts | 23 | 0 | 0 | 0 | Scripting |
| lib.es2017.intl.d.ts | 44 | 0 | 0 | 0 | Scripting |
| lib.es2017.object.d.ts | 49 | 0 | 0 | 0 | Scripting |
| lib.es2017.sharedmemory.d.ts | 135 | 0 | 0 | 0 | Scripting |
| lib.es2017.string.d.ts | 45 | 0 | 0 | 0 | Scripting |
| lib.es2017.typedarrays.d.ts | 53 | 0 | 0 | 0 | Scripting |
| lib.es2018.asyncgenerator.d.ts | 77 | 0 | 0 | 0 | Scripting |
| lib.es2018.asynciterable.d.ts | 53 | 0 | 0 | 0 | Scripting |
| lib.es2018.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2018.full.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2018.intl.d.ts | 83 | 0 | 0 | 0 | Scripting |
| lib.es2018.promise.d.ts | 30 | 0 | 0 | 0 | Scripting |
| lib.es2018.regexp.d.ts | 37 | 0 | 0 | 0 | Scripting |
| lib.es2019.array.d.ts | 79 | 0 | 0 | 0 | Scripting |
| lib.es2019.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2019.full.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2019.intl.d.ts | 23 | 0 | 0 | 0 | Scripting |
| lib.es2019.object.d.ts | 33 | 0 | 0 | 0 | Scripting |
| lib.es2019.string.d.ts | 37 | 0 | 0 | 0 | Scripting |
| lib.es2019.symbol.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2020.bigint.d.ts | 765 | 0 | 0 | 0 | Scripting |
| lib.es2020.d.ts | 27 | 0 | 0 | 0 | Scripting |
| lib.es2020.date.d.ts | 42 | 0 | 0 | 0 | Scripting |
| lib.es2020.full.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2020.intl.d.ts | 474 | 0 | 0 | 0 | Scripting |
| lib.es2020.number.d.ts | 28 | 0 | 0 | 0 | Scripting |
| lib.es2020.promise.d.ts | 47 | 0 | 0 | 0 | Scripting |
| lib.es2020.sharedmemory.d.ts | 99 | 0 | 0 | 0 | Scripting |
| lib.es2020.string.d.ts | 44 | 0 | 0 | 0 | Scripting |
| lib.es2020.symbol.wellknown.d.ts | 41 | 0 | 0 | 0 | Scripting |
| lib.es2021.d.ts | 23 | 0 | 0 | 0 | Scripting |
| lib.es2021.full.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2021.intl.d.ts | 166 | 0 | 0 | 0 | Scripting |
| lib.es2021.promise.d.ts | 48 | 0 | 0 | 0 | Scripting |
| lib.es2021.string.d.ts | 33 | 0 | 0 | 0 | Scripting |
| lib.es2021.weakref.d.ts | 78 | 0 | 0 | 0 | Scripting |
| lib.es2022.array.d.ts | 121 | 0 | 0 | 0 | Scripting |
| lib.es2022.d.ts | 25 | 0 | 0 | 0 | Scripting |
| lib.es2022.error.d.ts | 75 | 0 | 0 | 0 | Scripting |
| lib.es2022.full.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2022.intl.d.ts | 145 | 0 | 0 | 0 | Scripting |
| lib.es2022.object.d.ts | 26 | 0 | 0 | 0 | Scripting |
| lib.es2022.regexp.d.ts | 39 | 0 | 0 | 0 | Scripting |
| lib.es2022.string.d.ts | 25 | 0 | 0 | 0 | Scripting |
| lib.es2023.array.d.ts | 924 | 0 | 0 | 0 | Scripting |
| lib.es2023.collection.d.ts | 21 | 0 | 0 | 0 | Scripting |
| lib.es2023.d.ts | 22 | 0 | 0 | 0 | Scripting |
| lib.es2023.full.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2023.intl.d.ts | 56 | 0 | 0 | 0 | Scripting |
| lib.es2024.arraybuffer.d.ts | 65 | 0 | 0 | 0 | Scripting |
| lib.es2024.collection.d.ts | 29 | 0 | 0 | 0 | Scripting |
| lib.es2024.d.ts | 26 | 0 | 0 | 0 | Scripting |
| lib.es2024.full.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.es2024.object.d.ts | 29 | 0 | 0 | 0 | Scripting |
| lib.es2024.promise.d.ts | 35 | 0 | 0 | 0 | Scripting |
| lib.es2024.regexp.d.ts | 25 | 0 | 0 | 0 | Scripting |
| lib.es2024.sharedmemory.d.ts | 68 | 0 | 0 | 0 | Scripting |
| lib.es2024.string.d.ts | 29 | 0 | 0 | 0 | Scripting |
| lib.es5.d.ts | 4601 | 0 | 0 | 0 | Scripting |
| lib.es6.d.ts | 23 | 0 | 0 | 0 | Scripting |
| lib.esnext.array.d.ts | 35 | 0 | 0 | 0 | Scripting |
| lib.esnext.collection.d.ts | 96 | 0 | 0 | 0 | Scripting |
| lib.esnext.d.ts | 29 | 0 | 0 | 0 | Scripting |
| lib.esnext.decorators.d.ts | 28 | 0 | 0 | 0 | Scripting |
| lib.esnext.disposable.d.ts | 193 | 0 | 0 | 0 | Scripting |
| lib.esnext.error.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.esnext.float16.d.ts | 443 | 0 | 0 | 0 | Scripting |
| lib.esnext.full.d.ts | 24 | 0 | 0 | 0 | Scripting |
| lib.esnext.intl.d.ts | 21 | 0 | 0 | 0 | Scripting |
| lib.esnext.iterator.d.ts | 148 | 0 | 0 | 0 | Scripting |
| lib.esnext.promise.d.ts | 34 | 0 | 0 | 0 | Scripting |
| lib.esnext.sharedmemory.d.ts | 25 | 0 | 0 | 0 | Scripting |
| lib.scripthost.d.ts | 322 | 0 | 0 | 0 | Scripting |
| lib.webworker.asynciterable.d.ts | 41 | 0 | 0 | 0 | Scripting |
| lib.webworker.d.ts | 13150 | 0 | 0 | 0 | Scripting |
| lib.webworker.importscripts.d.ts | 23 | 0 | 0 | 0 | Scripting |
| lib.webworker.iterable.d.ts | 340 | 0 | 0 | 0 | Scripting |
| tsc.js | 8 | 0 | 0 | 0 | Scripting |
| tsserver.js | 8 | 0 | 0 | 0 | Scripting |
| tsserverlibrary.d.ts | 17 | 0 | 0 | 0 | Scripting |
| tsserverlibrary.js | 21 | 0 | 0 | 0 | Scripting |
| typesMap.json | 497 | 0 | 0 | 0 | Configuration |
| typescript.d.ts | 11438 | 0 | 0 | 0 | Scripting |
| typescript.js | 200253 | 0 | 0 | 0 | Scripting |
| typingsInstaller.js | 8 | 0 | 0 | 0 | Scripting |
| watchGuard.js | 53 | 0 | 0 | 0 | Scripting |

### Directory: `client/node_modules/typescript/lib/cs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/de`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/es`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/fr`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/it`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/ja`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/ko`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/pl`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/pt-br`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/ru`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/tr`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/zh-cn`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/typescript/lib/zh-tw`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| diagnosticMessages.generated.json | 2122 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/use-callback-ref/dist/es2015`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| assignRef.d.ts | 15 | 0 | 0 | 0 | Frontend |
| assignRef.js | 22 | 0 | 0 | 0 | Frontend |
| createRef.d.ts | 10 | 0 | 0 | 0 | Frontend |
| createRef.js | 23 | 0 | 0 | 0 | Frontend |
| index.d.ts | 8 | 0 | 0 | 0 | Frontend |
| index.js | 12 | 0 | 0 | 0 | Frontend |
| mergeRef.d.ts | 16 | 0 | 0 | 0 | Frontend |
| mergeRef.js | 18 | 0 | 0 | 0 | Frontend |
| refToCallback.d.ts | 24 | 0 | 0 | 0 | Frontend |
| refToCallback.js | 48 | 0 | 0 | 0 | Frontend |
| transformRef.d.ts | 11 | 0 | 0 | 0 | Frontend |
| transformRef.js | 14 | 0 | 0 | 0 | Frontend |
| types.d.ts | 5 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |
| useMergeRef.d.ts | 17 | 0 | 0 | 0 | Frontend |
| useMergeRef.js | 45 | 0 | 0 | 0 | Frontend |
| useRef.d.ts | 16 | 0 | 0 | 0 | Frontend |
| useRef.js | 39 | 0 | 0 | 0 | Frontend |
| useTransformRef.d.ts | 15 | 0 | 0 | 0 | Frontend |
| useTransformRef.js | 18 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/use-callback-ref/dist/es2019`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| assignRef.d.ts | 15 | 0 | 0 | 0 | Frontend |
| assignRef.js | 22 | 0 | 0 | 0 | Frontend |
| createRef.d.ts | 10 | 0 | 0 | 0 | Frontend |
| createRef.js | 23 | 0 | 0 | 0 | Frontend |
| index.d.ts | 8 | 0 | 0 | 0 | Frontend |
| index.js | 12 | 0 | 0 | 0 | Frontend |
| mergeRef.d.ts | 16 | 0 | 0 | 0 | Frontend |
| mergeRef.js | 18 | 0 | 0 | 0 | Frontend |
| refToCallback.d.ts | 24 | 0 | 0 | 0 | Frontend |
| refToCallback.js | 48 | 0 | 0 | 0 | Frontend |
| transformRef.d.ts | 11 | 0 | 0 | 0 | Frontend |
| transformRef.js | 14 | 0 | 0 | 0 | Frontend |
| types.d.ts | 5 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |
| useMergeRef.d.ts | 17 | 0 | 0 | 0 | Frontend |
| useMergeRef.js | 43 | 0 | 0 | 0 | Frontend |
| useRef.d.ts | 16 | 0 | 0 | 0 | Frontend |
| useRef.js | 39 | 0 | 0 | 0 | Frontend |
| useTransformRef.d.ts | 15 | 0 | 0 | 0 | Frontend |
| useTransformRef.js | 18 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/use-callback-ref/dist/es5`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| assignRef.d.ts | 15 | 0 | 0 | 0 | Frontend |
| assignRef.js | 26 | 0 | 0 | 0 | Frontend |
| createRef.d.ts | 10 | 0 | 0 | 0 | Frontend |
| createRef.js | 27 | 0 | 0 | 0 | Frontend |
| index.d.ts | 8 | 0 | 0 | 0 | Frontend |
| index.js | 24 | 0 | 0 | 0 | Frontend |
| mergeRef.d.ts | 16 | 0 | 0 | 0 | Frontend |
| mergeRef.js | 22 | 0 | 0 | 0 | Frontend |
| refToCallback.d.ts | 24 | 0 | 0 | 0 | Frontend |
| refToCallback.js | 53 | 0 | 0 | 0 | Frontend |
| transformRef.d.ts | 11 | 0 | 0 | 0 | Frontend |
| transformRef.js | 18 | 0 | 0 | 0 | Frontend |
| types.d.ts | 5 | 0 | 0 | 0 | Frontend |
| types.js | 2 | 0 | 0 | 0 | Frontend |
| useMergeRef.d.ts | 17 | 0 | 0 | 0 | Frontend |
| useMergeRef.js | 50 | 0 | 0 | 0 | Frontend |
| useRef.d.ts | 16 | 0 | 0 | 0 | Frontend |
| useRef.js | 43 | 0 | 0 | 0 | Frontend |
| useTransformRef.d.ts | 15 | 0 | 0 | 0 | Frontend |
| useTransformRef.js | 22 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/use-sidecar/dist/es2015`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.d.ts | 5 | 0 | 0 | 0 | Configuration |
| config.js | 6 | 0 | 0 | 0 | Configuration |
| env.d.ts | 4 | 0 | 0 | 0 | Frontend |
| env.js | 5 | 0 | 0 | 0 | Frontend |
| exports.d.ts | 3 | 0 | 0 | 0 | Frontend |
| exports.js | 18 | 0 | 0 | 0 | Frontend |
| hoc.d.ts | 3 | 0 | 0 | 0 | Frontend |
| hoc.js | 15 | 0 | 0 | 0 | Frontend |
| hook.d.ts | 2 | 0 | 0 | 0 | Frontend |
| hook.js | 41 | 0 | 0 | 0 | Frontend |
| index.d.ts | 7 | 0 | 0 | 0 | Frontend |
| index.js | 6 | 0 | 0 | 0 | Frontend |
| medium.d.ts | 3 | 0 | 0 | 0 | Frontend |
| medium.js | 78 | 0 | 0 | 0 | Frontend |
| renderProp.d.ts | 9 | 0 | 0 | 0 | Frontend |
| renderProp.js | 35 | 0 | 0 | 0 | Frontend |
| types.d.ts | 47 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/use-sidecar/dist/es2019`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.d.ts | 5 | 0 | 0 | 0 | Configuration |
| config.js | 6 | 0 | 0 | 0 | Configuration |
| env.d.ts | 4 | 0 | 0 | 0 | Frontend |
| env.js | 5 | 0 | 0 | 0 | Frontend |
| exports.d.ts | 3 | 0 | 0 | 0 | Frontend |
| exports.js | 16 | 0 | 0 | 0 | Frontend |
| hoc.d.ts | 3 | 0 | 0 | 0 | Frontend |
| hoc.js | 14 | 0 | 0 | 0 | Frontend |
| hook.d.ts | 2 | 0 | 0 | 0 | Frontend |
| hook.js | 41 | 0 | 0 | 0 | Frontend |
| index.d.ts | 7 | 0 | 0 | 0 | Frontend |
| index.js | 6 | 0 | 0 | 0 | Frontend |
| medium.d.ts | 3 | 0 | 0 | 0 | Frontend |
| medium.js | 78 | 0 | 0 | 0 | Frontend |
| renderProp.d.ts | 9 | 0 | 0 | 0 | Frontend |
| renderProp.js | 28 | 0 | 0 | 0 | Frontend |
| types.d.ts | 47 | 0 | 0 | 0 | Frontend |
| types.js | 1 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/use-sidecar/dist/es5`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| config.d.ts | 5 | 0 | 0 | 0 | Configuration |
| config.js | 10 | 0 | 0 | 0 | Configuration |
| env.d.ts | 4 | 0 | 0 | 0 | Frontend |
| env.js | 8 | 0 | 0 | 0 | Frontend |
| exports.d.ts | 3 | 0 | 0 | 0 | Frontend |
| exports.js | 22 | 0 | 0 | 0 | Frontend |
| hoc.d.ts | 3 | 0 | 0 | 0 | Frontend |
| hoc.js | 19 | 0 | 0 | 0 | Frontend |
| hook.d.ts | 2 | 0 | 0 | 0 | Frontend |
| hook.js | 45 | 0 | 0 | 0 | Frontend |
| index.d.ts | 7 | 0 | 0 | 0 | Frontend |
| index.js | 16 | 0 | 0 | 0 | Frontend |
| medium.d.ts | 3 | 0 | 0 | 0 | Frontend |
| medium.js | 83 | 0 | 0 | 0 | Frontend |
| renderProp.d.ts | 9 | 0 | 0 | 0 | Frontend |
| renderProp.js | 39 | 0 | 0 | 0 | Frontend |
| types.d.ts | 47 | 0 | 0 | 0 | Frontend |
| types.js | 2 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/vaul/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 141 | 0 | 0 | 0 | Other |
| index.d.ts | 141 | 0 | 0 | 0 | Frontend |
| index.js | 1683 | 0 | 0 | 0 | Frontend |
| index.mjs | 1655 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/victory-vendor/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| d3-array.js | 6 | 0 | 0 | 0 | Frontend |
| d3-color.js | 6 | 0 | 0 | 0 | Frontend |
| d3-ease.js | 6 | 0 | 0 | 0 | Frontend |
| d3-format.js | 6 | 0 | 0 | 0 | Frontend |
| d3-interpolate.js | 6 | 0 | 0 | 0 | Frontend |
| d3-path.js | 6 | 0 | 0 | 0 | Frontend |
| d3-scale.js | 6 | 0 | 0 | 0 | Frontend |
| d3-shape.js | 6 | 0 | 0 | 0 | Frontend |
| d3-time-format.js | 6 | 0 | 0 | 0 | Frontend |
| d3-time.js | 6 | 0 | 0 | 0 | Frontend |
| d3-timer.js | 6 | 0 | 0 | 0 | Frontend |
| d3-voronoi.js | 6 | 0 | 0 | 0 | Frontend |
| internmap.js | 6 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/vite-tsconfig-paths/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.d.mts | 6 | 0 | 0 | 0 | Configuration |
| index.d.ts | 62 | 0 | 0 | 0 | Configuration |
| index.js | 387 | 0 | 0 | 0 | Configuration |
| index.js.map | 1 | 0 | 0 | 0 | Configuration |

### Directory: `client/node_modules/vite/dist/client`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| client.mjs | 1134 | 0 | 0 | 0 | Other |
| env.mjs | 24 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/vite/dist/node`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cli.js | 949 | 0 | 0 | 0 | Frontend |
| constants.js | 149 | 0 | 0 | 0 | Frontend |
| index.d.ts | 4222 | 0 | 0 | 0 | Frontend |
| index.js | 194 | 0 | 0 | 0 | Frontend |
| module-runner.d.ts | 290 | 0 | 0 | 0 | Frontend |
| module-runner.js | 1311 | 0 | 0 | 0 | Frontend |
| moduleRunnerTransport.d-DJ_mE5sf.d.ts | 87 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/vite/dist/node-cjs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| publicUtils.cjs | 3987 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/vite/dist/node/chunks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dep-3RmXg9uo.js | 553 | 0 | 0 | 0 | Frontend |
| dep-C9BXG1mU.js | 822 | 0 | 0 | 0 | Frontend |
| dep-CvfTChi5.js | 8218 | 0 | 0 | 0 | Frontend |
| dep-D4NMHUTW.js | 49531 | 0 | 0 | 0 | Frontend |
| dep-DWMUTS1A.js | 7113 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/vite/node_modules/fdir/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| index.cjs | 588 | 0 | 0 | 0 | Other |
| index.d.cts | 155 | 0 | 0 | 0 | Other |
| index.d.mts | 155 | 0 | 0 | 0 | Other |
| index.mjs | 570 | 0 | 0 | 0 | Other |

### Directory: `client/node_modules/vite/node_modules/picomatch/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| constants.js | 180 | 0 | 0 | 0 | Frontend |
| parse.js | 1085 | 0 | 0 | 0 | Frontend |
| picomatch.js | 341 | 0 | 0 | 0 | Frontend |
| scan.js | 391 | 0 | 0 | 0 | Frontend |
| utils.js | 72 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| errors.js | 57 | 0 | 0 | 0 | Frontend |
| index.js | 17 | 0 | 0 | 0 | Frontend |
| log.js | 11 | 0 | 0 | 0 | Frontend |
| public-api.js | 102 | 0 | 0 | 0 | Frontend |
| util.js | 11 | 0 | 0 | 0 | Frontend |
| visit.js | 233 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/compose`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| compose-collection.js | 88 | 0 | 0 | 0 | Frontend |
| compose-doc.js | 43 | 0 | 0 | 0 | Frontend |
| compose-node.js | 102 | 0 | 0 | 0 | Frontend |
| compose-scalar.js | 86 | 0 | 0 | 0 | Frontend |
| composer.js | 217 | 0 | 0 | 0 | Frontend |
| resolve-block-map.js | 115 | 0 | 0 | 0 | Frontend |
| resolve-block-scalar.js | 198 | 0 | 0 | 0 | Frontend |
| resolve-block-seq.js | 49 | 0 | 0 | 0 | Frontend |
| resolve-end.js | 37 | 0 | 0 | 0 | Frontend |
| resolve-flow-collection.js | 207 | 0 | 0 | 0 | Frontend |
| resolve-flow-scalar.js | 223 | 0 | 0 | 0 | Frontend |
| resolve-props.js | 146 | 0 | 0 | 0 | Frontend |
| util-contains-newline.js | 34 | 0 | 0 | 0 | Frontend |
| util-empty-scalar-position.js | 26 | 0 | 0 | 0 | Frontend |
| util-flow-indent-check.js | 15 | 0 | 0 | 0 | Frontend |
| util-map-includes.js | 13 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/doc`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Document.js | 335 | 0 | 0 | 0 | Frontend |
| anchors.js | 71 | 0 | 0 | 0 | Frontend |
| applyReviver.js | 55 | 0 | 0 | 0 | Frontend |
| createNode.js | 88 | 0 | 0 | 0 | Frontend |
| directives.js | 176 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/nodes`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Alias.js | 114 | 0 | 0 | 0 | Frontend |
| Collection.js | 147 | 0 | 0 | 0 | Frontend |
| Node.js | 38 | 0 | 0 | 0 | Frontend |
| Pair.js | 36 | 0 | 0 | 0 | Frontend |
| Scalar.js | 24 | 0 | 0 | 0 | Frontend |
| YAMLMap.js | 144 | 0 | 0 | 0 | Frontend |
| YAMLSeq.js | 113 | 0 | 0 | 0 | Frontend |
| addPairToJSMap.js | 63 | 0 | 0 | 0 | Frontend |
| identity.js | 36 | 0 | 0 | 0 | Frontend |
| toJS.js | 37 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/parse`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cst-scalar.js | 214 | 0 | 0 | 0 | Frontend |
| cst-stringify.js | 61 | 0 | 0 | 0 | Frontend |
| cst-visit.js | 97 | 0 | 0 | 0 | Frontend |
| cst.js | 98 | 0 | 0 | 0 | Frontend |
| lexer.js | 717 | 0 | 0 | 0 | Frontend |
| line-counter.js | 39 | 0 | 0 | 0 | Frontend |
| parser.js | 967 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/schema`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Schema.js | 37 | 0 | 0 | 0 | Frontend |
| tags.js | 96 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/schema/common`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| map.js | 17 | 0 | 0 | 0 | Frontend |
| null.js | 15 | 0 | 0 | 0 | Frontend |
| seq.js | 17 | 0 | 0 | 0 | Frontend |
| string.js | 14 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/schema/core`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| bool.js | 19 | 0 | 0 | 0 | Frontend |
| float.js | 43 | 0 | 0 | 0 | Frontend |
| int.js | 38 | 0 | 0 | 0 | Frontend |
| schema.js | 23 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/schema/json`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| schema.js | 62 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/schema/yaml-1.1`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| binary.js | 58 | 0 | 0 | 0 | Frontend |
| bool.js | 26 | 0 | 0 | 0 | Frontend |
| float.js | 46 | 0 | 0 | 0 | Frontend |
| int.js | 71 | 0 | 0 | 0 | Frontend |
| merge.js | 64 | 0 | 0 | 0 | Frontend |
| omap.js | 74 | 0 | 0 | 0 | Frontend |
| pairs.js | 78 | 0 | 0 | 0 | Frontend |
| schema.js | 39 | 0 | 0 | 0 | Frontend |
| set.js | 93 | 0 | 0 | 0 | Frontend |
| timestamp.js | 101 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/browser/dist/stringify`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| foldFlowLines.js | 146 | 0 | 0 | 0 | Frontend |
| stringify.js | 128 | 0 | 0 | 0 | Frontend |
| stringifyCollection.js | 143 | 0 | 0 | 0 | Frontend |
| stringifyComment.js | 20 | 0 | 0 | 0 | Frontend |
| stringifyDocument.js | 85 | 0 | 0 | 0 | Frontend |
| stringifyNumber.js | 24 | 0 | 0 | 0 | Frontend |
| stringifyPair.js | 150 | 0 | 0 | 0 | Frontend |
| stringifyString.js | 336 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cli.d.ts | 8 | 0 | 0 | 0 | Frontend |
| cli.mjs | 201 | 0 | 0 | 0 | Other |
| errors.d.ts | 21 | 0 | 0 | 0 | Frontend |
| errors.js | 62 | 0 | 0 | 0 | Frontend |
| index.d.ts | 25 | 0 | 0 | 0 | Frontend |
| index.js | 50 | 0 | 0 | 0 | Frontend |
| log.d.ts | 3 | 0 | 0 | 0 | Frontend |
| log.js | 19 | 0 | 0 | 0 | Frontend |
| options.d.ts | 344 | 0 | 0 | 0 | Frontend |
| public-api.d.ts | 44 | 0 | 0 | 0 | Frontend |
| public-api.js | 107 | 0 | 0 | 0 | Frontend |
| test-events.d.ts | 4 | 0 | 0 | 0 | Testing |
| test-events.js | 134 | 0 | 0 | 0 | Testing |
| util.d.ts | 16 | 0 | 0 | 0 | Frontend |
| util.js | 28 | 0 | 0 | 0 | Frontend |
| visit.d.ts | 102 | 0 | 0 | 0 | Frontend |
| visit.js | 236 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/compose`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| compose-collection.d.ts | 11 | 0 | 0 | 0 | Frontend |
| compose-collection.js | 90 | 0 | 0 | 0 | Frontend |
| compose-doc.d.ts | 7 | 0 | 0 | 0 | Frontend |
| compose-doc.js | 45 | 0 | 0 | 0 | Frontend |
| compose-node.d.ts | 29 | 0 | 0 | 0 | Frontend |
| compose-node.js | 105 | 0 | 0 | 0 | Frontend |
| compose-scalar.d.ts | 5 | 0 | 0 | 0 | Frontend |
| compose-scalar.js | 88 | 0 | 0 | 0 | Frontend |
| composer.d.ts | 63 | 0 | 0 | 0 | Frontend |
| composer.js | 222 | 0 | 0 | 0 | Frontend |
| resolve-block-map.d.ts | 6 | 0 | 0 | 0 | Frontend |
| resolve-block-map.js | 117 | 0 | 0 | 0 | Frontend |
| resolve-block-scalar.d.ts | 11 | 0 | 0 | 0 | Frontend |
| resolve-block-scalar.js | 200 | 0 | 0 | 0 | Frontend |
| resolve-block-seq.d.ts | 6 | 0 | 0 | 0 | Frontend |
| resolve-block-seq.js | 51 | 0 | 0 | 0 | Frontend |
| resolve-end.d.ts | 6 | 0 | 0 | 0 | Frontend |
| resolve-end.js | 39 | 0 | 0 | 0 | Frontend |
| resolve-flow-collection.d.ts | 7 | 0 | 0 | 0 | Frontend |
| resolve-flow-collection.js | 209 | 0 | 0 | 0 | Frontend |
| resolve-flow-scalar.d.ts | 10 | 0 | 0 | 0 | Frontend |
| resolve-flow-scalar.js | 225 | 0 | 0 | 0 | Frontend |
| resolve-props.d.ts | 23 | 0 | 0 | 0 | Frontend |
| resolve-props.js | 148 | 0 | 0 | 0 | Frontend |
| util-contains-newline.d.ts | 2 | 0 | 0 | 0 | Frontend |
| util-contains-newline.js | 36 | 0 | 0 | 0 | Frontend |
| util-empty-scalar-position.d.ts | 2 | 0 | 0 | 0 | Frontend |
| util-empty-scalar-position.js | 28 | 0 | 0 | 0 | Frontend |
| util-flow-indent-check.d.ts | 3 | 0 | 0 | 0 | Frontend |
| util-flow-indent-check.js | 17 | 0 | 0 | 0 | Frontend |
| util-map-includes.d.ts | 4 | 0 | 0 | 0 | Frontend |
| util-map-includes.js | 15 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/doc`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Document.d.ts | 141 | 0 | 0 | 0 | Frontend |
| Document.js | 337 | 0 | 0 | 0 | Frontend |
| anchors.d.ts | 24 | 0 | 0 | 0 | Frontend |
| anchors.js | 76 | 0 | 0 | 0 | Frontend |
| applyReviver.d.ts | 9 | 0 | 0 | 0 | Frontend |
| applyReviver.js | 57 | 0 | 0 | 0 | Frontend |
| createNode.d.ts | 17 | 0 | 0 | 0 | Frontend |
| createNode.js | 90 | 0 | 0 | 0 | Frontend |
| directives.d.ts | 49 | 0 | 0 | 0 | Frontend |
| directives.js | 178 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/nodes`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Alias.d.ts | 29 | 0 | 0 | 0 | Frontend |
| Alias.js | 116 | 0 | 0 | 0 | Frontend |
| Collection.d.ts | 73 | 0 | 0 | 0 | Frontend |
| Collection.js | 151 | 0 | 0 | 0 | Frontend |
| Node.d.ts | 53 | 0 | 0 | 0 | Frontend |
| Node.js | 40 | 0 | 0 | 0 | Frontend |
| Pair.d.ts | 22 | 0 | 0 | 0 | Frontend |
| Pair.js | 39 | 0 | 0 | 0 | Frontend |
| Scalar.d.ts | 43 | 0 | 0 | 0 | Frontend |
| Scalar.js | 27 | 0 | 0 | 0 | Frontend |
| YAMLMap.d.ts | 53 | 0 | 0 | 0 | Frontend |
| YAMLMap.js | 147 | 0 | 0 | 0 | Frontend |
| YAMLSeq.d.ts | 60 | 0 | 0 | 0 | Frontend |
| YAMLSeq.js | 115 | 0 | 0 | 0 | Frontend |
| addPairToJSMap.d.ts | 4 | 0 | 0 | 0 | Frontend |
| addPairToJSMap.js | 65 | 0 | 0 | 0 | Frontend |
| identity.d.ts | 23 | 0 | 0 | 0 | Frontend |
| identity.js | 53 | 0 | 0 | 0 | Frontend |
| toJS.d.ts | 29 | 0 | 0 | 0 | Frontend |
| toJS.js | 39 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/parse`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cst-scalar.d.ts | 64 | 0 | 0 | 0 | Frontend |
| cst-scalar.js | 218 | 0 | 0 | 0 | Frontend |
| cst-stringify.d.ts | 8 | 0 | 0 | 0 | Frontend |
| cst-stringify.js | 63 | 0 | 0 | 0 | Frontend |
| cst-visit.d.ts | 39 | 0 | 0 | 0 | Frontend |
| cst-visit.js | 99 | 0 | 0 | 0 | Frontend |
| cst.d.ts | 109 | 0 | 0 | 0 | Frontend |
| cst.js | 112 | 0 | 0 | 0 | Frontend |
| lexer.d.ts | 87 | 0 | 0 | 0 | Frontend |
| lexer.js | 719 | 0 | 0 | 0 | Frontend |
| line-counter.d.ts | 22 | 0 | 0 | 0 | Frontend |
| line-counter.js | 41 | 0 | 0 | 0 | Frontend |
| parser.d.ts | 84 | 0 | 0 | 0 | Frontend |
| parser.js | 972 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/schema`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Schema.d.ts | 17 | 0 | 0 | 0 | Frontend |
| Schema.js | 39 | 0 | 0 | 0 | Frontend |
| json-schema.d.ts | 69 | 0 | 0 | 0 | Frontend |
| tags.d.ts | 48 | 0 | 0 | 0 | Frontend |
| tags.js | 99 | 0 | 0 | 0 | Frontend |
| types.d.ts | 92 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/schema/common`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| map.d.ts | 2 | 0 | 0 | 0 | Frontend |
| map.js | 19 | 0 | 0 | 0 | Frontend |
| null.d.ts | 4 | 0 | 0 | 0 | Frontend |
| null.js | 17 | 0 | 0 | 0 | Frontend |
| seq.d.ts | 2 | 0 | 0 | 0 | Frontend |
| seq.js | 19 | 0 | 0 | 0 | Frontend |
| string.d.ts | 2 | 0 | 0 | 0 | Frontend |
| string.js | 16 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/schema/core`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| bool.d.ts | 4 | 0 | 0 | 0 | Frontend |
| bool.js | 21 | 0 | 0 | 0 | Frontend |
| float.d.ts | 4 | 0 | 0 | 0 | Frontend |
| float.js | 47 | 0 | 0 | 0 | Frontend |
| int.d.ts | 4 | 0 | 0 | 0 | Frontend |
| int.js | 42 | 0 | 0 | 0 | Frontend |
| schema.d.ts | 1 | 0 | 0 | 0 | Frontend |
| schema.js | 25 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/schema/json`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| schema.d.ts | 2 | 0 | 0 | 0 | Frontend |
| schema.js | 64 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/schema/yaml-1.1`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| binary.d.ts | 2 | 0 | 0 | 0 | Frontend |
| binary.js | 70 | 0 | 0 | 0 | Frontend |
| bool.d.ts | 7 | 0 | 0 | 0 | Frontend |
| bool.js | 29 | 0 | 0 | 0 | Frontend |
| float.d.ts | 4 | 0 | 0 | 0 | Frontend |
| float.js | 50 | 0 | 0 | 0 | Frontend |
| int.d.ts | 5 | 0 | 0 | 0 | Frontend |
| int.js | 76 | 0 | 0 | 0 | Frontend |
| merge.d.ts | 9 | 0 | 0 | 0 | Frontend |
| merge.js | 68 | 0 | 0 | 0 | Frontend |
| omap.d.ts | 22 | 0 | 0 | 0 | Frontend |
| omap.js | 77 | 0 | 0 | 0 | Frontend |
| pairs.d.ts | 10 | 0 | 0 | 0 | Frontend |
| pairs.js | 82 | 0 | 0 | 0 | Frontend |
| schema.d.ts | 1 | 0 | 0 | 0 | Frontend |
| schema.js | 41 | 0 | 0 | 0 | Frontend |
| set.d.ts | 28 | 0 | 0 | 0 | Frontend |
| set.js | 96 | 0 | 0 | 0 | Frontend |
| timestamp.d.ts | 6 | 0 | 0 | 0 | Frontend |
| timestamp.js | 105 | 0 | 0 | 0 | Frontend |

### Directory: `client/node_modules/yaml/dist/stringify`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| foldFlowLines.d.ts | 34 | 0 | 0 | 0 | Frontend |
| foldFlowLines.js | 151 | 0 | 0 | 0 | Frontend |
| stringify.d.ts | 21 | 0 | 0 | 0 | Frontend |
| stringify.js | 131 | 0 | 0 | 0 | Frontend |
| stringifyCollection.d.ts | 17 | 0 | 0 | 0 | Frontend |
| stringifyCollection.js | 145 | 0 | 0 | 0 | Frontend |
| stringifyComment.d.ts | 10 | 0 | 0 | 0 | Frontend |
| stringifyComment.js | 24 | 0 | 0 | 0 | Frontend |
| stringifyDocument.d.ts | 4 | 0 | 0 | 0 | Frontend |
| stringifyDocument.js | 87 | 0 | 0 | 0 | Frontend |
| stringifyNumber.d.ts | 2 | 0 | 0 | 0 | Frontend |
| stringifyNumber.js | 26 | 0 | 0 | 0 | Frontend |
| stringifyPair.d.ts | 3 | 0 | 0 | 0 | Frontend |
| stringifyPair.js | 152 | 0 | 0 | 0 | Frontend |
| stringifyString.d.ts | 9 | 0 | 0 | 0 | Frontend |
| stringifyString.js | 338 | 0 | 0 | 0 | Frontend |

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

### Directory: `data/email_content`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| 1.json.gz | 2 | 0 | 0 | 0 | Data |

### Directory: `deployment`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| Dockerfile.backend | 36 | 0 | 0 | 0 | Containerization |
| Dockerfile.frontend | 31 | 0 | 0 | 0 | Containerization |
| README.md | 98 | 0 | 0 | 0 | Documentation |
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| data_migration.py | 0 | 0 | 0 | 0 | Core Logic |
| deploy.py | 43 | 4 | 2 | 0 | Core Logic |
| docker-compose.dev.yml | 16 | 0 | 0 | 0 | Configuration |
| docker-compose.prod.yml | 13 | 0 | 0 | 0 | Configuration |
| docker-compose.stag.yml | 67 | 0 | 0 | 0 | Configuration |
| docker-compose.yml | 25 | 0 | 0 | 0 | Configuration |
| setup_env.py | 185 | 7 | 7 | 0 | Core Logic |
| test_stages.py | 99 | 4 | 7 | 1 | Testing |

### Directory: `deployment/nginx`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| nginx.conf | 18 | 0 | 0 | 0 | Other |

### Directory: `docs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .GITHUB_FILES_INVENTORY.md | 228 | 0 | 0 | 0 | Documentation |
| .branch-config.json | 18 | 0 | 0 | 0 | Configuration |
| .merge-history.json | 1 | 0 | 0 | 0 | Configuration |
| .review-queue.json | 94 | 0 | 0 | 0 | Configuration |
| AGENT_INSTRUCTIONS_MANIFEST.md | 253 | 0 | 0 | 0 | Documentation |
| AGENT_INSTRUCTIONS_ORCHESTRATION_STRATEGY.md | 314 | 0 | 0 | 0 | Documentation |
| AGENT_ORCHESTRATION_CHECKLIST.md | 400 | 0 | 0 | 0 | Documentation |
| API_REFERENCE.md | 32 | 0 | 0 | 0 | Documentation |
| BRANCH_NAMING_STANDARDIZATION.md | 30 | 0 | 0 | 0 | Documentation |
| BRANCH_OWNERSHIP_GUIDE.md | 30 | 0 | 0 | 0 | Documentation |
| DASHBOARD_CONSOLIDATION_REPORT.md | 30 | 0 | 0 | 0 | Documentation |
| DEVELOPER_GUIDE.md | 30 | 0 | 0 | 0 | Documentation |
| DOCUMENTATION_WORKFLOW.md | 30 | 0 | 0 | 0 | Documentation |
| GITHUB_WORKFLOWS_ROADMAP.md | 445 | 0 | 0 | 0 | Documentation |
| LLM_DOCUMENTATION_DISCOVERY.md | 778 | 0 | 0 | 0 | Documentation |
| MULTI_TOOL_DISCOVERY.md | 677 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION.md | 181 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_APPROVAL.md | 233 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_APPROVAL_QUICK_REFERENCE.md | 72 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_GITHUB_PROTECTION_SUMMARY.md | 216 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_PUSH_STRATEGIES.md | 96 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_SYSTEM.md | 637 | 0 | 0 | 0 | Documentation |
| ORCHESTRATION_WORKFLOW.md | 179 | 0 | 0 | 0 | Documentation |
| README.md | 81 | 0 | 0 | 0 | Documentation |
| SYNC-FRAMEWORK.md | 391 | 0 | 0 | 0 | Documentation |
| TROUBLESHOOTING.md | 30 | 0 | 0 | 0 | Documentation |
| WORKFLOW_README-main.md | 229 | 0 | 0 | 0 | Documentation |
| WORKFLOW_README-scientific.md | 229 | 0 | 0 | 0 | Documentation |
| WORKFLOW_README.md | 229 | 0 | 0 | 0 | Documentation |
| WORK_IN_PROGRESS_SUMMARY.md | 338 | 0 | 0 | 0 | Documentation |
| actionable_insights.md | 111 | 0 | 0 | 0 | Documentation |
| ai_model_training_guide.md | 32 | 0 | 0 | 0 | Documentation |
| analysis_WORKFLOW_README.json | 58 | 0 | 0 | 0 | Configuration |
| analysis_test_workflow-scientific.json | 3 | 0 | 0 | 0 | Testing |
| analysis_test_workflow.json | 3 | 0 | 0 | 0 | Testing |
| architecture_overview.md | 0 | 0 | 0 | 0 | Documentation |
| backend_migration_guide.md | 30 | 0 | 0 | 0 | Documentation |
| branch_alignment_executive_summary.md | 30 | 0 | 0 | 0 | Documentation |
| branch_alignment_strategies_analysis.md | 30 | 0 | 0 | 0 | Documentation |
| changes_report.md | 0 | 0 | 0 | 0 | Documentation |
| cli_workflow_map.md | 37 | 0 | 0 | 0 | Documentation |
| command_pattern.md | 138 | 0 | 0 | 0 | Documentation |
| complete_stash_resolution_procedure.md | 172 | 0 | 0 | 0 | Documentation |
| critical_files_check.md | 164 | 0 | 0 | 0 | Documentation |
| database_configuration.md | 30 | 0 | 0 | 0 | Documentation |
| detailed_progress_report.md | 30 | 0 | 0 | 0 | Documentation |
| documenting_development_sessions.md | 30 | 0 | 0 | 0 | Documentation |
| documenting_development_sessions_summary.md | 30 | 0 | 0 | 0 | Documentation |
| env_management.md | 198 | 0 | 0 | 0 | Documentation |
| extensions_guide.md | 0 | 0 | 0 | 0 | Documentation |
| getting_started.md | 30 | 0 | 0 | 0 | Documentation |
| git_workflow_plan.md | 191 | 0 | 0 | 0 | Documentation |
| hook-version-mismatch-issue.md | 160 | 0 | 0 | 0 | Documentation |
| iflow_development_workflow.md | 30 | 0 | 0 | 0 | Documentation |
| interactive_stash_resolution.md | 113 | 0 | 0 | 0 | Documentation |
| key_accomplishments.md | 30 | 0 | 0 | 0 | Documentation |
| mfa_implementation.md | 30 | 0 | 0 | 0 | Documentation |
| multi_agent_code_review.md | 30 | 0 | 0 | 0 | Documentation |
| node_architecture.md | 0 | 0 | 0 | 0 | Documentation |
| non-orchestration-workflow.md | 286 | 0 | 0 | 0 | Documentation |
| notmuch-implementation-comparison.md | 116 | 0 | 0 | 0 | Documentation |
| notmuch-implementation-deviations.md | 118 | 0 | 0 | 0 | Documentation |
| notmuch-implementation-update.md | 69 | 0 | 0 | 0 | Documentation |
| notmuch_datasource_implementation.md | 30 | 0 | 0 | 0 | Documentation |
| orchestration-push-workflow.md | 507 | 0 | 0 | 0 | Documentation |
| orchestration-quick-reference.md | 242 | 0 | 0 | 0 | Documentation |
| orchestration-workflow.md | 222 | 0 | 0 | 0 | Documentation |
| orchestration_branch_architecture_analysis.md | 167 | 0 | 0 | 0 | Documentation |
| orchestration_branch_architecture_diagram.md | 99 | 0 | 0 | 0 | Documentation |
| orchestration_branch_maintenance_refactoring_insights.md | 160 | 0 | 0 | 0 | Documentation |
| orchestration_branch_scope.md | 135 | 0 | 0 | 0 | Documentation |
| orchestration_branch_stash_todo_manager.md | 117 | 0 | 0 | 0 | Documentation |
| orchestration_hook_management.md | 219 | 0 | 0 | 0 | Documentation |
| orchestration_summary.md | 111 | 0 | 0 | 0 | Documentation |
| orchestration_validation_tests.md | 309 | 0 | 0 | 0 | Testing |
| project_structure_comparison.md | 0 | 0 | 0 | 0 | Documentation |
| recovery_log.md | 122 | 0 | 0 | 0 | Documentation |
| server_development.md | 88 | 0 | 0 | 0 | Documentation |
| stash_management_tools.md | 151 | 0 | 0 | 0 | Documentation |
| stash_resolution_procedure.md | 164 | 0 | 0 | 0 | Documentation |
| stash_scripts_improvements.md | 61 | 0 | 0 | 0 | Documentation |
| tagging-functionality-analysis.md | 92 | 0 | 0 | 0 | Documentation |
| technical_debt_tracker.md | 50 | 0 | 0 | 0 | Documentation |
| test_workflow-scientific.md | 29 | 0 | 0 | 0 | Testing |
| test_workflow.md | 29 | 0 | 0 | 0 | Testing |
| unimplemented_code_analysis.md | 30 | 0 | 0 | 0 | Documentation |
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

### Directory: `docs/current_orchestration_docs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| workflow_implementation_plan.md | 225 | 0 | 0 | 0 | Documentation |
| workflow_system_analysis.md | 164 | 0 | 0 | 0 | Documentation |

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
| branch_switching_guide.md | 288 | 0 | 0 | 0 | Documentation |
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
| taskmaster_testing_guide.md | 466 | 0 | 0 | 0 | Testing |
| taskmaster_troubleshooting.md | 310 | 0 | 0 | 0 | Documentation |
| taskmaster_workflow_guide.md | 236 | 0 | 0 | 0 | Documentation |
| unimplemented_code_analysis.md | 123 | 0 | 0 | 0 | Documentation |
| workflow_and_review_process.md | 331 | 0 | 0 | 0 | Documentation |
| workflow_implementation_plan.md | 225 | 0 | 0 | 0 | Documentation |

### Directory: `docs/old_workflow_docs`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| CPU_ONLY_DEPLOYMENT_POLICY.md | 195 | 0 | 0 | 0 | Documentation |
| CPU_SETUP.md | 131 | 0 | 0 | 0 | Documentation |
| DOCUMENTATION_WORKFLOW.md | 196 | 0 | 0 | 0 | Documentation |
| TROUBLESHOOTING.md | 418 | 0 | 0 | 0 | Documentation |
| worktree-documentation-system.md | 251 | 0 | 0 | 0 | Documentation |

### Directory: `docs/templates`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| module_documentation_template.md | 386 | 0 | 0 | 0 | Documentation |

### Directory: `docs/troubleshooting`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| dependency_management_guide.md | 67 | 0 | 0 | 0 | Documentation |

### Directory: `guidance`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| ARCHITECTURE_ALIGNMENT_COMPLETE_AND_RECOMMENDATIONS.md | 109 | 0 | 0 | 0 | Documentation |
| ARCHITECTURE_ALIGNMENT_IMPLEMENTATION_GUIDE.md | 254 | 0 | 0 | 0 | Documentation |
| COMPREHENSIVE_CLI_ARCHITECTURE_GUIDE.md | 210 | 0 | 0 | 0 | Documentation |
| FACTORY_PATTERN_IMPLEMENTATION_GUIDE.md | 217 | 0 | 0 | 0 | Documentation |
| FINAL_MERGE_STRATEGY.md | 68 | 0 | 0 | 0 | Documentation |
| HANDLING_INCOMPLETE_MIGRATIONS.md | 96 | 0 | 0 | 0 | Documentation |
| IMPLEMENTATION_SUMMARY.md | 108 | 0 | 0 | 0 | Documentation |
| LEGACY_FEATURE_PORTING_GUIDE.md | 83 | 0 | 0 | 0 | Documentation |
| MERGE_GUIDANCE_DOCUMENTATION.md | 232 | 0 | 0 | 0 | Documentation |
| QUICK_REFERENCE_GUIDE.md | 144 | 0 | 0 | 0 | Documentation |
| README.md | 84 | 0 | 0 | 0 | Documentation |
| SCIENTIFIC_BRANCH_ENHANCEMENTS_COMPARISON.md | 252 | 0 | 0 | 0 | Documentation |
| SUMMARY.md | 38 | 0 | 0 | 0 | Documentation |
| validate_architecture_alignment.py | 172 | 16 | 6 | 0 | Core Logic |
| validate_guidance_documentation.sh | 159 | 0 | 0 | 0 | Scripting |

### Directory: `guidance/src`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| main.py | 174 | 17 | 2 | 1 | Core Logic |

### Directory: `implement`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| plan.md | 57 | 0 | 0 | 0 | Documentation |
| state.json | 22 | 0 | 0 | 0 | Configuration |

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

### Directory: `logs/branch_cleanup`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cleanup_20251216.log | 12 | 0 | 0 | 0 | Other |

### Directory: `modules/auth`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| routes.py | 283 | 10 | 0 | 6 | Core Logic |

### Directory: `modules/dashboard`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 28 | 3 | 1 | 0 | Core Logic |
| models.py | 44 | 2 | 0 | 4 | Core Logic |
| routes.py | 93 | 10 | 0 | 0 | Core Logic |

### Directory: `modules/email`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| routes.py | 92 | 10 | 0 | 0 | Core Logic |

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

### Directory: `rule-tests`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitkeep | 0 | 0 | 0 | 0 | Testing |
| README.md | 42 | 0 | 0 | 0 | Testing |

### Directory: `rules`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitkeep | 0 | 0 | 0 | 0 | Other |

### Directory: `rules/architectural`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 32 | 0 | 0 | 0 | Documentation |
| no-logic-in-scripts.yaml | 21 | 0 | 0 | 0 | Configuration |

### Directory: `rules/devpy`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 23 | 0 | 0 | 0 | Documentation |
| pydantic-models.yaml | 18 | 0 | 0 | 0 | Configuration |
| rich-output.yaml | 18 | 0 | 0 | 0 | Configuration |
| typer-commands.yaml | 18 | 0 | 0 | 0 | Configuration |

### Directory: `rules/python`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 25 | 0 | 0 | 0 | Documentation |
| docstring-required.yaml | 21 | 0 | 0 | 0 | Configuration |
| error-handling-required.yaml | 15 | 0 | 0 | 0 | Configuration |
| logging-required.yaml | 22 | 0 | 0 | 0 | Configuration |
| no-print-statements.yaml | 14 | 0 | 0 | 0 | Configuration |
| type-hints-required.yaml | 20 | 0 | 0 | 0 | Configuration |

### Directory: `rules/typescript`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 24 | 0 | 0 | 0 | Documentation |
| no-any-type.yaml | 18 | 0 | 0 | 0 | Configuration |
| no-ts-ignore.yaml | 12 | 0 | 0 | 0 | Configuration |
| strict-null-checks.yaml | 16 | 0 | 0 | 0 | Configuration |
| type-hints-preferred.yaml | 15 | 0 | 0 | 0 | Configuration |

### Directory: `scripts`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| architectural_rule_engine.py | 279 | 9 | 14 | 1 | Scripting |
| cleanup.sh | 21 | 0 | 0 | 0 | Scripting |
| cleanup_application_files.sh | 64 | 0 | 0 | 0 | Scripting |
| cleanup_orchestration.sh | 37 | 0 | 0 | 0 | Scripting |
| common.sh | 182 | 0 | 0 | 0 | Scripting |
| config_manager.py | 146 | 4 | 6 | 1 | Configuration |
| context-control | 78 | 0 | 0 | 0 | Scripting |
| disable-all-orchestration-with-branch-sync.sh | 270 | 0 | 0 | 0 | Scripting |
| disable-all-orchestration.sh | 110 | 0 | 0 | 0 | Scripting |
| disable-hooks.sh | 97 | 0 | 0 | 0 | Scripting |
| enable-all-orchestration-with-branch-sync.sh | 259 | 0 | 0 | 0 | Scripting |
| enable-all-orchestration.sh | 97 | 0 | 0 | 0 | Scripting |
| enable-hooks.sh | 92 | 0 | 0 | 0 | Scripting |
| extract-orchestration-changes.sh | 403 | 0 | 0 | 0 | Scripting |
| file_finder.py | 37 | 3 | 1 | 0 | Scripting |
| find_lost_files_in_commits.sh | 27 | 0 | 0 | 0 | Scripting |
| find_lost_source_code_commits.sh | 30 | 0 | 0 | 0 | Scripting |
| find_lost_source_files.sh | 25 | 0 | 0 | 0 | Scripting |
| handle_stashes.sh | 214 | 0 | 0 | 0 | Scripting |
| handle_stashes_optimized.sh | 403 | 0 | 0 | 0 | Scripting |
| import_audit.py | 387 | 6 | 11 | 2 | Scripting |
| install-hooks.sh | 167 | 0 | 0 | 0 | Scripting |
| install-minimal.sh | 37 | 0 | 0 | 0 | Scripting |
| install-ml.sh | 56 | 0 | 0 | 0 | Scripting |
| intelligent_merge_analyzer.py | 199 | 5 | 4 | 1 | Scripting |
| intelligent_merger.py | 207 | 4 | 5 | 0 | Scripting |
| interactive_stash_resolver.sh | 204 | 0 | 0 | 0 | Scripting |
| interactive_stash_resolver_optimized.sh | 326 | 0 | 0 | 0 | Scripting |
| master_audit.sh | 90 | 0 | 0 | 0 | Scripting |
| path_change_detector.py | 270 | 5 | 9 | 2 | Scripting |
| performance-test.py | 265 | 7 | 8 | 1 | Testing |
| restore-hooks.sh | 56 | 0 | 0 | 0 | Scripting |
| reverse_sync_orchestration.sh | 152 | 0 | 0 | 0 | Scripting |
| show_dangling_commit_diffs.sh | 23 | 0 | 0 | 0 | Scripting |
| stash_analysis.sh | 35 | 0 | 0 | 0 | Scripting |
| stash_analysis_advanced.sh | 155 | 0 | 0 | 0 | Scripting |
| stash_details.sh | 60 | 0 | 0 | 0 | Scripting |
| stash_manager.sh | 331 | 0 | 0 | 0 | Scripting |
| stash_manager_optimized.sh | 455 | 0 | 0 | 0 | Scripting |
| stash_todo_manager.sh | 496 | 0 | 0 | 0 | Scripting |
| sync_orchestration_files.sh | 534 | 0 | 0 | 0 | Scripting |
| sync_setup_worktrees.sh | 298 | 0 | 0 | 0 | Scripting |
| update-agent-context.sh | 756 | 0 | 0 | 0 | Scripting |
| update-all-branches.sh | 537 | 0 | 0 | 0 | Scripting |
| update_references.py | 146 | 4 | 2 | 0 | Scripting |
| validate-branch-propagation.sh | 290 | 0 | 0 | 0 | Scripting |
| validate-ide-agent-inclusion.sh | 179 | 0 | 0 | 0 | Scripting |
| validate-orchestration-context.sh | 83 | 0 | 0 | 0 | Scripting |
| verify-dependencies.py | 315 | 9 | 9 | 1 | Scripting |

### Directory: `scripts/bash`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create-pr-resolution-spec.sh | 366 | 0 | 0 | 0 | Scripting |
| gh-pr-ci-integration.sh | 483 | 0 | 0 | 0 | Scripting |
| pr-test-executor.sh | 416 | 0 | 0 | 0 | Testing |
| task-creation-validator.sh | 350 | 0 | 0 | 0 | Scripting |

### Directory: `scripts/branch_cleanup`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 24 | 5 | 0 | 0 | Scripting |
| cleanup_manager.py | 475 | 13 | 22 | 5 | Scripting |
| cli.py | 309 | 6 | 10 | 0 | Scripting |
| report_generator.py | 641 | 7 | 10 | 6 | Scripting |
| review_validator.py | 444 | 9 | 20 | 7 | Scripting |
| rollback_manager.py | 640 | 8 | 26 | 6 | Scripting |
| safety_checker.py | 448 | 9 | 19 | 5 | Scripting |

### Directory: `scripts/branch_cleanup/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 23 | 0 | 0 | 0 | Scripting |
| cleanup_manager.cpython-313.pyc | 625 | 0 | 0 | 0 | Scripting |
| review_validator.cpython-313.pyc | 528 | 0 | 0 | 0 | Scripting |
| rollback_manager.cpython-313.pyc | 670 | 0 | 0 | 0 | Scripting |
| safety_checker.cpython-313.pyc | 491 | 0 | 0 | 0 | Scripting |

### Directory: `scripts/hooks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| post-checkout | 70 | 0 | 0 | 0 | Scripting |
| post-commit | 131 | 0 | 0 | 0 | Scripting |
| post-commit-setup-sync | 46 | 0 | 0 | 0 | Scripting |
| pre-commit | 114 | 0 | 0 | 0 | Scripting |

### Directory: `scripts/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| common.sh | 24 | 0 | 0 | 0 | Scripting |
| error_handling.sh | 45 | 0 | 0 | 0 | Scripting |
| git_utils.sh | 50 | 0 | 0 | 0 | Scripting |
| logging.sh | 53 | 0 | 0 | 0 | Scripting |
| orchestration-approval.sh | 216 | 0 | 0 | 0 | Scripting |
| stash_common.sh | 99 | 0 | 0 | 0 | Scripting |
| validation.sh | 77 | 0 | 0 | 0 | Scripting |

### Directory: `scripts/powershell`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| create-pr-resolution-spec.ps1 | 367 | 0 | 0 | 0 | Scripting |

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
| container.py | 50 | 1 | 6 | 1 | Core Logic |
| environment.py | 418 | 0 | 0 | 0 | Core Logic |
| launch.bat | 63 | 0 | 0 | 0 | Scripting |
| launch.py | 1625 | 0 | 0 | 0 | Core Logic |
| launch.sh | 10 | 0 | 0 | 0 | Scripting |
| project_config.py | 259 | 0 | 0 | 0 | Configuration |
| pyproject.toml | 142 | 0 | 0 | 0 | Configuration |
| requirements-cpu.txt | 14 | 0 | 0 | 0 | Other |
| requirements-dev.txt | 20 | 0 | 0 | 0 | Other |
| requirements.txt | 50 | 0 | 0 | 0 | Other |
| services.py | 518 | 0 | 0 | 0 | Core Logic |
| settings.py | 74 | 5 | 1 | 2 | Core Logic |
| setup_environment_system.sh | 395 | 0 | 0 | 0 | Scripting |
| setup_environment_wsl.sh | 521 | 0 | 0 | 0 | Scripting |
| setup_python.sh | 97 | 0 | 0 | 0 | Scripting |
| test_commands.py | 86 | 6 | 3 | 0 | Testing |
| test_config.py | 62 | 3 | 1 | 0 | Testing |
| test_stages.py | 117 | 0 | 0 | 0 | Testing |
| utils.py | 340 | 0 | 0 | 0 | Core Logic |
| validation.py | 273 | 0 | 0 | 0 | Core Logic |

### Directory: `setup/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 3 | 0 | 0 | 0 | Other |
| container.cpython-313.pyc | 67 | 0 | 0 | 0 | Other |
| environment.cpython-313.pyc | 390 | 0 | 0 | 0 | Other |
| launch.cpython-313.pyc | 450 | 0 | 0 | 0 | Other |
| project_config.cpython-313.pyc | 304 | 0 | 0 | 0 | Configuration |
| services.cpython-313.pyc | 438 | 0 | 0 | 0 | Other |
| utils.cpython-313.pyc | 295 | 0 | 0 | 0 | Other |
| validation.cpython-313.pyc | 218 | 0 | 0 | 0 | Other |

### Directory: `setup/commands`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 8 | 1 | 0 | 0 | Core Logic |
| check_command.py | 86 | 4 | 4 | 1 | Core Logic |
| cleanup_command.py | 62 | 4 | 4 | 1 | Core Logic |
| command_factory.py | 99 | 8 | 5 | 1 | Core Logic |
| command_interface.py | 62 | 3 | 5 | 1 | Core Logic |
| guide_dev_command.py | 88 | 4 | 4 | 1 | Core Logic |
| guide_pr_command.py | 69 | 3 | 3 | 1 | Core Logic |
| run_command.py | 86 | 6 | 3 | 1 | Core Logic |
| setup_command.py | 244 | 18 | 10 | 1 | Core Logic |
| test_command.py | 58 | 4 | 3 | 1 | Testing |

### Directory: `setup/setup_backup_20251216_152049`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| launch.py | 1459 | 0 | 0 | 0 | Core Logic |

### Directory: `specs/004-guided-workflow`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| GAP_ANALYSIS.md | 536 | 0 | 0 | 0 | Documentation |
| data-model.md | 115 | 0 | 0 | 0 | Documentation |
| plan.md | 141 | 0 | 0 | 0 | Documentation |
| plan.md.bak | 209 | 0 | 0 | 0 | Other |
| quickstart.md | 55 | 0 | 0 | 0 | Documentation |
| research.md | 41 | 0 | 0 | 0 | Documentation |
| spec.md | 723 | 0 | 0 | 0 | Documentation |
| tasks.md | 183 | 0 | 0 | 0 | Documentation |
| tasks.md.bak | 154 | 0 | 0 | 0 | Other |
| tasks.md.pre-rewrite.bak | 168 | 0 | 0 | 0 | Other |

### Directory: `specs/004-guided-workflow/checklists`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| agentic_safety.md | 43 | 0 | 0 | 0 | Documentation |
| backend_frontend.md | 39 | 0 | 0 | 0 | Documentation |
| decomposition.md | 39 | 0 | 0 | 0 | Documentation |
| governance.md | 26 | 0 | 0 | 0 | Documentation |
| requirements.md | 35 | 0 | 0 | 0 | Documentation |
| safety.md | 27 | 0 | 0 | 0 | Documentation |
| ux.md | 36 | 0 | 0 | 0 | Documentation |

### Directory: `specs/004-guided-workflow/contracts`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cli-contract.yaml | 161 | 0 | 0 | 0 | Configuration |
| cli-guides.md | 33 | 0 | 0 | 0 | Documentation |
| cli-schema.json | 26 | 0 | 0 | 0 | Configuration |

### Directory: `specs/004-guided-workflow/research`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| cass-session-analysis.md | 132 | 0 | 0 | 0 | Documentation |
| cli-framework-implementation-guide.md | 786 | 0 | 0 | 0 | Documentation |
| research.md | 34 | 0 | 0 | 0 | Documentation |

### Directory: `specs/006-pr176-integration-fixes`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| plan.md | 67 | 0 | 0 | 0 | Documentation |
| spec.md | 133 | 0 | 0 | 0 | Documentation |
| tasks.md | 248 | 0 | 0 | 0 | Documentation |

### Directory: `specs/006-pr176-integration-fixes/checklists`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| requirements.md | 34 | 0 | 0 | 0 | Documentation |

### Directory: `specs/013-task-execution-layer`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| plan.md | 102 | 0 | 0 | 0 | Documentation |
| spec.md | 57 | 0 | 0 | 0 | Documentation |
| tasks.md | 66 | 0 | 0 | 0 | Documentation |

### Directory: `specs/013-task-execution-layer/checklists`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| requirements.md | 20 | 0 | 0 | 0 | Documentation |

### Directory: `src`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| index.js | 23 | 0 | 0 | 0 | Frontend |
| main.py | 174 | 17 | 2 | 1 | Core Logic |

### Directory: `src/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 3 | 0 | 0 | 0 | Other |

### Directory: `src/analysis`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conflict_analyzer.py | 117 | 3 | 8 | 1 | Core Logic |

### Directory: `src/analysis/constitutional`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| analyzer.py | 95 | 6 | 3 | 2 | Core Logic |
| requirement_checker.py | 180 | 3 | 5 | 5 | Core Logic |

### Directory: `src/backend`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| db.ts | 14 | 0 | 0 | 0 | Frontend |

### Directory: `src/backend/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 3 | 0 | 0 | 0 | Other |

### Directory: `src/backend/data`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| categories.json | 38 | 0 | 0 | 0 | Configuration |
| categories.json.gz | 2 | 0 | 0 | 0 | Data |
| emails.json | 5 | 0 | 0 | 0 | Configuration |
| emails.json.gz | 2 | 0 | 0 | 0 | Data |
| settings.json | 3 | 0 | 0 | 0 | Configuration |
| users.json | 5 | 0 | 0 | 0 | Configuration |
| users.json.gz | 2 | 0 | 0 | 0 | Data |

### Directory: `src/backend/extensions`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 9 | 0 | 0 | 0 | Documentation |

### Directory: `src/backend/extensions/example`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 71 | 0 | 0 | 0 | Documentation |
| example.py | 111 | 4 | 5 | 0 | Core Logic |
| metadata.json | 17 | 0 | 0 | 0 | Configuration |
| requirements.txt | 7 | 0 | 0 | 0 | Other |

### Directory: `src/backend/extensions/example/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| example.cpython-313.pyc | 115 | 0 | 0 | 0 | Other |

### Directory: `src/backend/node_engine`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| email_nodes.py | 678 | 5 | 8 | 9 | Core Logic |
| migration_utils.py | 363 | 8 | 14 | 3 | Core Logic |
| node_base.py | 353 | 6 | 28 | 7 | Core Logic |
| node_library.py | 314 | 4 | 11 | 1 | Core Logic |
| security_manager.py | 420 | 9 | 20 | 6 | Core Logic |
| smart_filter_node.py | 160 | 3 | 3 | 1 | Core Logic |
| test_integration.py | 393 | 10 | 0 | 0 | Testing |
| test_migration.py | 101 | 2 | 2 | 0 | Testing |
| test_nodes.py | 182 | 7 | 0 | 0 | Testing |
| test_sanitization.py | 72 | 4 | 1 | 0 | Testing |
| test_security.py | 253 | 8 | 0 | 0 | Testing |
| workflow_engine.py | 429 | 8 | 6 | 3 | Core Logic |
| workflow_manager.py | 324 | 7 | 9 | 1 | Core Logic |

### Directory: `src/backend/node_engine/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| email_nodes.cpython-313.pyc | 790 | 0 | 0 | 0 | Other |
| migration_utils.cpython-313.pyc | 384 | 0 | 0 | 0 | Other |
| node_base.cpython-313.pyc | 447 | 0 | 0 | 0 | Other |
| node_library.cpython-313.pyc | 248 | 0 | 0 | 0 | Other |
| security_manager.cpython-313.pyc | 497 | 0 | 0 | 0 | Other |
| smart_filter_node.cpython-313.pyc | 154 | 0 | 0 | 0 | Other |
| test_integration.cpython-313.pyc | 503 | 0 | 0 | 0 | Testing |
| test_migration.cpython-313.pyc | 125 | 0 | 0 | 0 | Testing |
| test_nodes.cpython-313.pyc | 224 | 0 | 0 | 0 | Testing |
| test_sanitization.cpython-313.pyc | 108 | 0 | 0 | 0 | Testing |
| test_security.cpython-313.pyc | 340 | 0 | 0 | 0 | Testing |
| workflow_engine.cpython-313.pyc | 509 | 0 | 0 | 0 | Other |
| workflow_manager.cpython-313.pyc | 422 | 0 | 0 | 0 | Other |

### Directory: `src/backend/plugins`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 15 | 1 | 0 | 0 | Core Logic |
| base_plugin.py | 128 | 3 | 14 | 3 | Core Logic |
| email_filter_node.py | 103 | 2 | 8 | 1 | Core Logic |
| email_visualizer_plugin.py | 73 | 3 | 9 | 1 | Core Logic |
| plugin_manager.py | 172 | 7 | 11 | 1 | Core Logic |

### Directory: `src/backend/plugins/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 17 | 0 | 0 | 0 | Other |
| base_plugin.cpython-313.pyc | 147 | 0 | 0 | 0 | Other |
| email_filter_node.cpython-313.pyc | 113 | 0 | 0 | 0 | Other |
| email_visualizer_plugin.cpython-313.pyc | 95 | 0 | 0 | 0 | Other |
| plugin_manager.cpython-313.pyc | 241 | 0 | 0 | 0 | Other |

### Directory: `src/backend/python_backend`

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
| database.py | 725 | 11 | 6 | 1 | Core Logic |
| dependencies.py | 234 | 19 | 6 | 0 | Core Logic |
| email_data_manager.py | 251 | 11 | 4 | 1 | Core Logic |
| email_routes.py | 175 | 16 | 0 | 0 | Core Logic |
| enhanced_routes.py | 199 | 10 | 0 | 4 | Core Logic |
| exceptions.py | 134 | 3 | 10 | 11 | Core Logic |
| filter_routes.py | 94 | 9 | 0 | 0 | Core Logic |
| gmail_routes.py | 240 | 12 | 0 | 0 | Core Logic |
| gradio_app.py | 231 | 12 | 5 | 0 | Core Logic |
| json_database.py | 661 | 11 | 6 | 1 | Core Logic |
| main.py | 394 | 39 | 0 | 1 | Core Logic |
| model_manager.py | 25 | 2 | 3 | 1 | Core Logic |
| model_routes.py | 64 | 6 | 0 | 0 | Core Logic |
| node_workflow_routes.py | 384 | 18 | 0 | 4 | Core Logic |
| performance_monitor.py | 360 | 10 | 19 | 3 | Core Logic |
| performance_routes.py | 37 | 4 | 0 | 0 | Core Logic |
| plugin_manager.py | 65 | 3 | 3 | 1 | Core Logic |
| run_server.py | 62 | 5 | 0 | 0 | Core Logic |
| settings.py | 74 | 5 | 1 | 2 | Core Logic |
| smart_filters.py | 2 | 0 | 0 | 1 | Core Logic |
| training_routes.py | 170 | 16 | 0 | 0 | Core Logic |
| utils.py | 63 | 3 | 1 | 0 | Core Logic |
| workflow_editor_ui.py | 328 | 8 | 6 | 0 | Core Logic |
| workflow_engine.py | 259 | 9 | 12 | 4 | Core Logic |
| workflow_manager.py | 162 | 7 | 11 | 2 | Core Logic |
| workflow_routes.py | 362 | 12 | 1 | 2 | Core Logic |

### Directory: `src/backend/python_backend/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 44 | 0 | 0 | 0 | Other |
| advanced_workflow_routes.cpython-313.pyc | 310 | 0 | 0 | 0 | Other |
| ai_engine.cpython-313.pyc | 324 | 0 | 0 | 0 | Other |
| ai_routes.cpython-313.pyc | 209 | 0 | 0 | 0 | Other |
| auth.cpython-313.pyc | 103 | 0 | 0 | 0 | Other |
| category_data_manager.cpython-313.pyc | 204 | 0 | 0 | 0 | Data |
| category_routes.cpython-313.pyc | 105 | 0 | 0 | 0 | Other |
| config.cpython-313.pyc | 47 | 0 | 0 | 0 | Configuration |
| constants.cpython-313.pyc | 21 | 0 | 0 | 0 | Other |
| dashboard_routes.cpython-313.pyc | 168 | 0 | 0 | 0 | Other |
| database.cpython-313.pyc | 1118 | 0 | 0 | 0 | Data |
| dependencies.cpython-313.pyc | 182 | 0 | 0 | 0 | Other |
| email_data_manager.cpython-313.pyc | 397 | 0 | 0 | 0 | Data |
| email_routes.cpython-313.pyc | 248 | 0 | 0 | 0 | Other |
| enhanced_routes.cpython-313.pyc | 251 | 0 | 0 | 0 | Other |
| exceptions.cpython-313.pyc | 174 | 0 | 0 | 0 | Other |
| filter_routes.cpython-313.pyc | 133 | 0 | 0 | 0 | Other |
| gmail_routes.cpython-313.pyc | 362 | 0 | 0 | 0 | Other |
| gradio_app.cpython-313.pyc | 309 | 0 | 0 | 0 | Other |
| json_database.cpython-313.pyc | 1053 | 0 | 0 | 0 | Data |
| main.cpython-313.pyc | 362 | 0 | 0 | 0 | Other |
| model_manager.cpython-313.pyc | 32 | 0 | 0 | 0 | Other |
| model_routes.cpython-313.pyc | 75 | 0 | 0 | 0 | Other |
| node_workflow_routes.cpython-313.pyc | 425 | 0 | 0 | 0 | Other |
| performance_monitor.cpython-313.pyc | 494 | 0 | 0 | 0 | Other |
| performance_routes.cpython-313.pyc | 46 | 0 | 0 | 0 | Other |
| plugin_manager.cpython-313.pyc | 93 | 0 | 0 | 0 | Other |
| run_server.cpython-313.pyc | 70 | 0 | 0 | 0 | Other |
| settings.cpython-313.pyc | 77 | 0 | 0 | 0 | Other |
| smart_filters.cpython-313.pyc | 10 | 0 | 0 | 0 | Other |
| training_routes.cpython-313.pyc | 194 | 0 | 0 | 0 | Other |
| utils.cpython-313.pyc | 82 | 0 | 0 | 0 | Other |
| workflow_editor_ui.cpython-313.pyc | 386 | 0 | 0 | 0 | Other |
| workflow_engine.cpython-313.pyc | 456 | 0 | 0 | 0 | Other |
| workflow_manager.cpython-313.pyc | 240 | 0 | 0 | 0 | Other |
| workflow_routes.cpython-313.pyc | 400 | 0 | 0 | 0 | Other |

### Directory: `src/backend/python_backend/notebooks`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| email_analysis.ipynb | 65 | 0 | 0 | 0 | Notebook |

### Directory: `src/backend/python_backend/routes/v1`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| category_routes.py | 86 | 10 | 0 | 0 | Core Logic |
| email_routes.py | 165 | 9 | 0 | 0 | Core Logic |

### Directory: `src/backend/python_backend/routes/v1/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| category_routes.cpython-313.pyc | 71 | 0 | 0 | 0 | Other |
| email_routes.cpython-313.pyc | 160 | 0 | 0 | 0 | Other |

### Directory: `src/backend/python_backend/services`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| base_service.py | 45 | 5 | 1 | 2 | Core Logic |
| category_service.py | 90 | 3 | 1 | 1 | Core Logic |
| email_service.py | 187 | 5 | 1 | 1 | Core Logic |

### Directory: `src/backend/python_backend/services/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| base_service.cpython-313.pyc | 69 | 0 | 0 | 0 | Other |
| category_service.cpython-313.pyc | 116 | 0 | 0 | 0 | Other |
| email_service.cpython-313.pyc | 277 | 0 | 0 | 0 | Other |

### Directory: `src/backend/python_backend/tests`

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

### Directory: `src/backend/python_backend/tests/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conftest.cpython-313.pyc | 159 | 0 | 0 | 0 | Testing |
| test_advanced_ai_engine.cpython-313.pyc | 181 | 0 | 0 | 0 | Testing |
| test_category_routes.cpython-313.pyc | 81 | 0 | 0 | 0 | Testing |
| test_database_optimizations.cpython-313.pyc | 307 | 0 | 0 | 0 | Testing |
| test_email_routes.cpython-313.pyc | 267 | 0 | 0 | 0 | Testing |
| test_filter_routes.cpython-313.pyc | 101 | 0 | 0 | 0 | Testing |
| test_gmail_routes.cpython-313.pyc | 197 | 0 | 0 | 0 | Testing |
| test_model_manager.cpython-313.pyc | 143 | 0 | 0 | 0 | Testing |
| test_training_routes.cpython-313.pyc | 204 | 0 | 0 | 0 | Testing |
| test_workflow_routes.cpython-313.pyc | 98 | 0 | 0 | 0 | Testing |

### Directory: `src/backend/python_nlp`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| ai_training.py | 145 | 3 | 8 | 2 | Core Logic |
| data_strategy.py | 572 | 8 | 22 | 3 | Core Logic |
| gmail_integration.py | 615 | 24 | 15 | 5 | Core Logic |
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
| smart_filters.py | 498 | 11 | 33 | 3 | Core Logic |
| smart_retrieval.py | 249 | 16 | 6 | 3 | Core Logic |
| text_utils.py | 31 | 2 | 1 | 0 | Core Logic |
| topic_model.pkl | 0 | 0 | 0 | 0 | Other |
| urgency_model.pkl | 0 | 0 | 0 | 0 | Other |

### Directory: `src/backend/python_nlp/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 3 | 0 | 0 | 0 | Other |
| ai_training.cpython-313.pyc | 192 | 0 | 0 | 0 | Other |
| data_strategy.cpython-313.pyc | 842 | 0 | 0 | 0 | Data |
| gmail_integration.cpython-313.pyc | 1002 | 0 | 0 | 0 | Other |
| gmail_metadata.cpython-313.pyc | 686 | 0 | 0 | 0 | Data |
| gmail_service.cpython-313.pyc | 686 | 0 | 0 | 0 | Other |
| gmail_service_clean.cpython-313.pyc | 575 | 0 | 0 | 0 | Other |
| nlp_engine.cpython-313.pyc | 1400 | 0 | 0 | 0 | Other |
| protocols.cpython-313.pyc | 57 | 0 | 0 | 0 | Other |
| retrieval_monitor.cpython-313.pyc | 402 | 0 | 0 | 0 | Other |
| smart_filters.cpython-313.pyc | 657 | 0 | 0 | 0 | Other |
| smart_retrieval.cpython-313.pyc | 278 | 0 | 0 | 0 | Other |
| text_utils.cpython-313.pyc | 25 | 0 | 0 | 0 | Other |

### Directory: `src/backend/python_nlp/analysis_components`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| importance_model.py | 28 | 0 | 2 | 1 | Core Logic |
| intent_model.py | 20 | 2 | 2 | 1 | Core Logic |
| sentiment_model.py | 36 | 2 | 2 | 1 | Core Logic |
| topic_model.py | 35 | 2 | 2 | 1 | Core Logic |
| urgency_model.py | 20 | 2 | 2 | 1 | Core Logic |

### Directory: `src/backend/python_nlp/analysis_components/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| importance_model.cpython-313.pyc | 40 | 0 | 0 | 0 | Other |
| intent_model.cpython-313.pyc | 25 | 0 | 0 | 0 | Other |
| sentiment_model.cpython-313.pyc | 58 | 0 | 0 | 0 | Other |
| topic_model.cpython-313.pyc | 53 | 0 | 0 | 0 | Other |
| urgency_model.cpython-313.pyc | 25 | 0 | 0 | 0 | Other |

### Directory: `src/backend/python_nlp/tests`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_nlp_engine.py | 309 | 6 | 11 | 0 | Testing |

### Directory: `src/backend/python_nlp/tests/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_nlp_engine.cpython-313.pyc | 414 | 0 | 0 | 0 | Testing |

### Directory: `src/backend/tests`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| setup.ts | 21 | 0 | 0 | 0 | Testing |

### Directory: `src/cli`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| analyze.py | 55 | 3 | 2 | 0 | Core Logic |
| ci.py | 70 | 0 | 2 | 0 | Core Logic |
| identify.py | 49 | 2 | 2 | 0 | Core Logic |
| install.py | 56 | 0 | 2 | 0 | Core Logic |
| main.py | 309 | 14 | 1 | 0 | Core Logic |
| main_old.py | 308 | 0 | 0 | 0 | Core Logic |
| main_old_backup.py | 420 | 14 | 3 | 0 | Core Logic |
| progress.py | 38 | 2 | 1 | 0 | Core Logic |
| verify.py | 54 | 3 | 2 | 0 | Core Logic |

### Directory: `src/cli/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| main.cpython-313.pyc | 454 | 0 | 0 | 0 | Other |

### Directory: `src/cli/commands`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| analyze.py | 24 | 4 | 1 | 0 | Core Logic |
| analyze_command.py | 199 | 5 | 5 | 1 | Core Logic |
| analyze_history_command.py | 126 | 3 | 5 | 1 | Core Logic |
| compare.py | 33 | 4 | 1 | 0 | Core Logic |
| factory.py | 108 | 2 | 5 | 1 | Core Logic |
| guide.py | 27 | 3 | 1 | 0 | Core Logic |
| ide.py | 28 | 4 | 1 | 1 | Core Logic |
| integration.py | 252 | 19 | 8 | 0 | Core Logic |
| interface.py | 89 | 3 | 5 | 1 | Core Logic |
| plan_rebase_command.py | 112 | 3 | 5 | 1 | Core Logic |
| rebase.py | 30 | 4 | 2 | 0 | Core Logic |
| registry.py | 158 | 3 | 9 | 1 | Core Logic |
| resolve.py | 29 | 4 | 1 | 0 | Core Logic |
| schema.py | 13 | 4 | 1 | 0 | Core Logic |
| sync.py | 84 | 8 | 2 | 0 | Core Logic |
| task.py | 13 | 3 | 1 | 0 | Core Logic |
| validate_command.py | 94 | 3 | 5 | 1 | Core Logic |

### Directory: `src/cli/commands/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| analyze.cpython-313.pyc | 31 | 0 | 0 | 0 | Other |
| guide.cpython-313.pyc | 17 | 0 | 0 | 0 | Other |
| ide.cpython-313.pyc | 39 | 0 | 0 | 0 | Other |
| rebase.cpython-313.pyc | 39 | 0 | 0 | 0 | Other |
| resolve.cpython-313.pyc | 45 | 0 | 0 | 0 | Other |
| schema.cpython-313.pyc | 13 | 0 | 0 | 0 | Other |
| sync.cpython-313.pyc | 111 | 0 | 0 | 0 | Other |
| task.cpython-313.pyc | 19 | 0 | 0 | 0 | Other |

### Directory: `src/context_control`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 35 | 6 | 0 | 0 | Core Logic |
| agent.py | 310 | 5 | 16 | 1 | Core Logic |
| config.py | 196 | 5 | 7 | 2 | Configuration |
| core.py | 275 | 14 | 11 | 1 | Core Logic |
| environment.py | 123 | 5 | 5 | 0 | Core Logic |
| exceptions.py | 47 | 1 | 1 | 7 | Core Logic |
| isolation.py | 315 | 9 | 13 | 2 | Core Logic |
| logging.py | 100 | 4 | 5 | 1 | Core Logic |
| models.py | 154 | 3 | 0 | 7 | Core Logic |
| project.py | 281 | 8 | 10 | 1 | Core Logic |
| storage.py | 162 | 6 | 7 | 1 | Core Logic |
| validation.py | 384 | 8 | 13 | 1 | Core Logic |

### Directory: `src/context_control/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 38 | 0 | 0 | 0 | Other |
| isolation.cpython-313.pyc | 347 | 0 | 0 | 0 | Other |
| storage.cpython-313.pyc | 206 | 0 | 0 | 0 | Other |

### Directory: `src/core`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 0 | 0 | 0 | 0 | Core Logic |
| advanced_workflow_engine.py | 775 | 15 | 38 | 11 | Core Logic |
| ai_engine.py | 463 | 4 | 21 | 3 | Core Logic |
| audit_logger.py | 305 | 12 | 9 | 4 | Core Logic |
| auth.py | 312 | 13 | 9 | 3 | Core Logic |
| base.py | 23 | 3 | 1 | 3 | Core Logic |
| caching.py | 399 | 9 | 7 | 8 | Core Logic |
| conflict_models.py | 57 | 3 | 1 | 4 | Core Logic |
| constants.py | 43 | 0 | 0 | 0 | Core Logic |
| data_source.py | 113 | 2 | 0 | 1 | Core Logic |
| database.py | 843 | 15 | 7 | 2 | Core Logic |
| dynamic_model_manager.py | 410 | 9 | 6 | 1 | Core Logic |
| enhanced_caching.py | 230 | 5 | 27 | 3 | Core Logic |
| enhanced_error_reporting.py | 263 | 8 | 16 | 4 | Core Logic |
| exceptions.py | 50 | 0 | 0 | 9 | Core Logic |
| factory.py | 107 | 12 | 0 | 0 | Core Logic |
| interfaces.py | 114 | 3 | 0 | 5 | Core Logic |
| job_queue.py | 151 | 9 | 8 | 2 | Core Logic |
| mfa.py | 133 | 7 | 7 | 1 | Core Logic |
| middleware.py | 246 | 9 | 6 | 2 | Core Logic |
| model_registry.py | 717 | 13 | 3 | 5 | Core Logic |
| model_routes.py | 402 | 8 | 0 | 5 | Core Logic |
| models.py | 542 | 4 | 1 | 61 | Core Logic |
| notmuch_data_source.py | 750 | 13 | 1 | 1 | Core Logic |
| performance_monitor.py | 467 | 18 | 25 | 7 | Core Logic |
| plugin_base.py | 553 | 13 | 14 | 8 | Core Logic |
| plugin_manager.py | 486 | 13 | 8 | 3 | Core Logic |
| plugin_routes.py | 351 | 6 | 0 | 5 | Core Logic |
| rate_limiter.py | 150 | 6 | 4 | 4 | Core Logic |
| security.py | 212 | 4 | 10 | 1 | Core Logic |
| security_validator.py | 315 | 6 | 5 | 4 | Core Logic |
| settings.py | 22 | 2 | 1 | 1 | Core Logic |
| smart_filter_manager.py | 864 | 16 | 18 | 3 | Core Logic |
| workflow_engine.py | 685 | 9 | 12 | 4 | Core Logic |

### Directory: `src/core/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 3 | 0 | 0 | 0 | Other |
| advanced_workflow_engine.cpython-313.pyc | 1005 | 0 | 0 | 0 | Other |
| ai_engine.cpython-313.pyc | 664 | 0 | 0 | 0 | Other |
| audit_logger.cpython-313.pyc | 437 | 0 | 0 | 0 | Other |
| auth.cpython-313.pyc | 345 | 0 | 0 | 0 | Other |
| caching.cpython-313.pyc | 636 | 0 | 0 | 0 | Other |
| conflict_models.cpython-313.pyc | 88 | 0 | 0 | 0 | Other |
| constants.cpython-313.pyc | 19 | 0 | 0 | 0 | Other |
| data_source.cpython-313.pyc | 208 | 0 | 0 | 0 | Data |
| database.cpython-313.pyc | 1316 | 0 | 0 | 0 | Data |
| dynamic_model_manager.cpython-313.pyc | 666 | 0 | 0 | 0 | Other |
| enhanced_caching.cpython-313.pyc | 313 | 0 | 0 | 0 | Other |
| enhanced_error_reporting.cpython-313.pyc | 344 | 0 | 0 | 0 | Other |
| exceptions.cpython-313.pyc | 55 | 0 | 0 | 0 | Other |
| factory.cpython-313.pyc | 131 | 0 | 0 | 0 | Other |
| interfaces.cpython-313.pyc | 177 | 0 | 0 | 0 | Other |
| job_queue.cpython-313.pyc | 178 | 0 | 0 | 0 | Other |
| mfa.cpython-313.pyc | 161 | 0 | 0 | 0 | Other |
| middleware.cpython-313.pyc | 293 | 0 | 0 | 0 | Other |
| model_registry.cpython-313.pyc | 1032 | 0 | 0 | 0 | Other |
| model_routes.cpython-313.pyc | 518 | 0 | 0 | 0 | Other |
| models.cpython-313.pyc | 716 | 0 | 0 | 0 | Other |
| notmuch_data_source.cpython-313.pyc | 1045 | 0 | 0 | 0 | Data |
| performance_monitor.cpython-313.pyc | 621 | 0 | 0 | 0 | Other |
| plugin_base.cpython-313.pyc | 745 | 0 | 0 | 0 | Other |
| plugin_manager.cpython-313.pyc | 701 | 0 | 0 | 0 | Other |
| plugin_routes.cpython-313.pyc | 450 | 0 | 0 | 0 | Other |
| rate_limiter.cpython-313.pyc | 179 | 0 | 0 | 0 | Other |
| security.cpython-313.pyc | 235 | 0 | 0 | 0 | Other |
| security_validator.cpython-313.pyc | 382 | 0 | 0 | 0 | Other |
| settings.cpython-313.pyc | 31 | 0 | 0 | 0 | Other |
| smart_filter_manager.cpython-313.pyc | 1083 | 0 | 0 | 0 | Other |
| workflow_engine.cpython-313.pyc | 893 | 0 | 0 | 0 | Other |

### Directory: `src/core/analysis`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| scanner.py | 46 | 4 | 4 | 1 | Core Logic |
| sync.py | 41 | 6 | 2 | 1 | Core Logic |

### Directory: `src/core/analysis/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| sync.cpython-313.pyc | 70 | 0 | 0 | 0 | Other |

### Directory: `src/core/commands/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| setup_command.cpython-313.pyc | 282 | 0 | 0 | 0 | Other |

### Directory: `src/core/data`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 4 | 0 | 0 | 0 | Core Logic |
| data_source.py | 121 | 2 | 0 | 1 | Core Logic |
| database_source.py | 108 | 6 | 1 | 1 | Core Logic |
| factory.py | 9 | 1 | 0 | 0 | Core Logic |
| notmuch_data_source.py | 69 | 2 | 0 | 1 | Core Logic |
| repository.py | 316 | 6 | 2 | 3 | Core Logic |

### Directory: `src/core/data/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 7 | 0 | 0 | 0 | Data |
| data_source.cpython-313.pyc | 238 | 0 | 0 | 0 | Data |
| database_source.cpython-313.pyc | 192 | 0 | 0 | 0 | Data |
| factory.cpython-313.pyc | 13 | 0 | 0 | 0 | Data |
| notmuch_data_source.cpython-313.pyc | 97 | 0 | 0 | 0 | Data |
| repository.cpython-313.pyc | 492 | 0 | 0 | 0 | Data |

### Directory: `src/core/execution`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| executor.py | 37 | 4 | 5 | 1 | Core Logic |
| session.py | 28 | 4 | 3 | 1 | Core Logic |
| task_runner.py | 27 | 3 | 1 | 1 | Core Logic |

### Directory: `src/core/execution/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| session.cpython-313.pyc | 58 | 0 | 0 | 0 | Other |
| task_runner.cpython-313.pyc | 37 | 0 | 0 | 0 | Other |

### Directory: `src/core/git`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| comparison.py | 52 | 2 | 3 | 1 | Core Logic |
| detector.py | 13 | 3 | 2 | 1 | Core Logic |
| history.py | 95 | 3 | 4 | 2 | Core Logic |
| plumbing.py | 53 | 4 | 5 | 1 | Core Logic |

### Directory: `src/core/git/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| comparison.cpython-313.pyc | 88 | 0 | 0 | 0 | Other |
| detector.cpython-313.pyc | 20 | 0 | 0 | 0 | Other |
| history.cpython-313.pyc | 149 | 0 | 0 | 0 | Other |
| plumbing.cpython-313.pyc | 70 | 0 | 0 | 0 | Other |

### Directory: `src/core/models`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| execution.py | 8 | 3 | 0 | 1 | Core Logic |
| git.py | 22 | 3 | 0 | 3 | Core Logic |
| history.py | 17 | 2 | 0 | 2 | Core Logic |
| orchestration.py | 29 | 5 | 0 | 4 | Core Logic |

### Directory: `src/core/models/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| git.cpython-313.pyc | 46 | 0 | 0 | 0 | Other |
| history.cpython-313.pyc | 30 | 0 | 0 | 0 | Other |
| orchestration.cpython-313.pyc | 66 | 0 | 0 | 0 | Other |

### Directory: `src/core/resolution`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| engine.py | 24 | 3 | 1 | 2 | Core Logic |

### Directory: `src/core/resolution/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| engine.cpython-313.pyc | 41 | 0 | 0 | 0 | Other |

### Directory: `src/core/templates`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| antigravity.json.j2 | 4 | 0 | 0 | 0 | Other |
| vscode_tasks.json.j2 | 10 | 0 | 0 | 0 | Other |
| windsurf.json.j2 | 4 | 0 | 0 | 0 | Other |

### Directory: `src/core/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| answers.py | 17 | 3 | 2 | 1 | Core Logic |
| files.py | 24 | 3 | 2 | 0 | Core Logic |
| logger.py | 18 | 3 | 2 | 0 | Core Logic |

### Directory: `src/core/utils/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| files.cpython-313.pyc | 45 | 0 | 0 | 0 | Other |
| logger.cpython-313.pyc | 24 | 0 | 0 | 0 | Other |

### Directory: `src/emailintelligence.egg-info`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| PKG-INFO | 58 | 0 | 0 | 0 | Other |
| SOURCES.txt | 194 | 0 | 0 | 0 | Other |
| dependency_links.txt | 1 | 0 | 0 | 0 | Other |
| requires.txt | 61 | 0 | 0 | 0 | Other |
| top_level.txt | 13 | 0 | 0 | 0 | Other |

### Directory: `src/git`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conflict_detector.py | 158 | 5 | 5 | 4 | Core Logic |
| repository.py | 240 | 6 | 3 | 1 | Core Logic |

### Directory: `src/lib`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| git_wrapper.py | 68 | 2 | 8 | 1 | Core Logic |
| workflow_context.py | 43 | 2 | 6 | 2 | Core Logic |

### Directory: `src/lib/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| git_wrapper.cpython-313.pyc | 78 | 0 | 0 | 0 | Other |
| workflow_context.cpython-313.pyc | 67 | 0 | 0 | 0 | Other |

### Directory: `src/models`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| analysis.py | 51 | 3 | 0 | 2 | Core Logic |
| unified_analysis.py | 70 | 2 | 6 | 3 | Core Logic |

### Directory: `src/models/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| analysis.cpython-313.pyc | 59 | 0 | 0 | 0 | Other |
| unified_analysis.cpython-313.pyc | 121 | 0 | 0 | 0 | Other |

### Directory: `src/repl_nix_workspace.egg-info`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| PKG-INFO | 39 | 0 | 0 | 0 | Other |
| SOURCES.txt | 48 | 0 | 0 | 0 | Other |
| dependency_links.txt | 1 | 0 | 0 | 0 | Other |
| requires.txt | 35 | 0 | 0 | 0 | Other |
| top_level.txt | 4 | 0 | 0 | 0 | Other |

### Directory: `src/resolution`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.py | 272 | 6 | 9 | 5 | Core Logic |
| auto_resolver.py | 346 | 8 | 9 | 1 | Core Logic |
| semantic_merger.py | 310 | 3 | 15 | 1 | Core Logic |

### Directory: `src/resolution/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 398 | 0 | 0 | 0 | Other |

### Directory: `src/services`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| analysis_service.py | 212 | 7 | 3 | 3 | Core Logic |
| installation_service.py | 401 | 9 | 13 | 1 | Core Logic |
| merge_verifier.py | 29 | 1 | 2 | 1 | Core Logic |
| rebase_analyzer.py | 43 | 3 | 2 | 1 | Core Logic |
| rebase_detector.py | 25 | 1 | 2 | 1 | Core Logic |

### Directory: `src/services/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| analysis_service.cpython-313.pyc | 262 | 0 | 0 | 0 | Other |
| merge_verifier.cpython-313.pyc | 35 | 0 | 0 | 0 | Other |
| rebase_analyzer.cpython-313.pyc | 51 | 0 | 0 | 0 | Other |
| rebase_detector.cpython-313.pyc | 25 | 0 | 0 | 0 | Other |

### Directory: `src/strategy`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| generator.py | 202 | 4 | 11 | 1 | Core Logic |
| multi_phase_generator.py | 1112 | 6 | 35 | 8 | Core Logic |
| reordering.py | 65 | 3 | 1 | 1 | Core Logic |
| risk_assessor.py | 249 | 3 | 14 | 1 | Core Logic |
| selector.py | 118 | 3 | 2 | 1 | Core Logic |

### Directory: `src/strategy/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| generator.cpython-313.pyc | 250 | 0 | 0 | 0 | Other |
| multi_phase_generator.cpython-313.pyc | 1291 | 0 | 0 | 0 | Other |
| reordering.cpython-313.pyc | 88 | 0 | 0 | 0 | Other |
| risk_assessor.cpython-313.pyc | 309 | 0 | 0 | 0 | Other |
| selector.cpython-313.pyc | 122 | 0 | 0 | 0 | Other |

### Directory: `src/utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| caching.py | 303 | 6 | 2 | 2 | Core Logic |
| logger.py | 87 | 4 | 2 | 0 | Core Logic |
| monitoring.py | 150 | 5 | 6 | 1 | Core Logic |
| rate_limit.py | 82 | 6 | 1 | 1 | Core Logic |

### Directory: `src/validation`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| comprehensive_validator.py | 1100 | 12 | 25 | 2 | Core Logic |
| quality_checker.py | 57 | 4 | 2 | 1 | Core Logic |
| quick_validator.py | 551 | 6 | 8 | 5 | Core Logic |
| reporting_engine.py | 1031 | 9 | 21 | 2 | Core Logic |
| standard_validator.py | 669 | 7 | 8 | 2 | Core Logic |
| test_runner.py | 82 | 6 | 1 | 1 | Testing |
| validator.py | 158 | 4 | 7 | 2 | Core Logic |

### Directory: `test_data`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| categories.json.gz | 3 | 0 | 0 | 0 | Testing |
| emails.json.gz | 3 | 0 | 0 | 0 | Testing |
| users.json.gz | 3 | 0 | 0 | 0 | Testing |

### Directory: `tests`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| conftest.py | 162 | 14 | 7 | 0 | Testing |
| test_api_actions.py | 70 | 3 | 5 | 0 | Testing |
| test_auth.py | 34 | 6 | 2 | 0 | Testing |
| test_basic.py | 36 | 3 | 2 | 0 | Testing |
| test_basic_validation.py | 17 | 3 | 2 | 0 | Testing |
| test_category_api.py | 89 | 3 | 2 | 0 | Testing |
| test_dashboard_api.py | 77 | 2 | 5 | 0 | Testing |
| test_database.py | 175 | 5 | 0 | 0 | Testing |
| test_email_api.py | 134 | 5 | 0 | 0 | Testing |
| test_filter_api.py | 96 | 5 | 6 | 0 | Testing |
| test_gmail_api.py | 105 | 4 | 7 | 0 | Testing |
| test_hook_recursion.py | 252 | 7 | 11 | 1 | Testing |
| test_hooks.py | 86 | 4 | 7 | 2 | Testing |
| test_launch.py | 87 | 4 | 11 | 2 | Testing |
| test_launcher.py | 192 | 7 | 12 | 4 | Testing |
| test_mfa.py | 106 | 4 | 1 | 0 | Testing |
| test_password_hashing.py | 34 | 2 | 3 | 0 | Testing |
| test_prompt_engineer.py | 28 | 2 | 3 | 1 | Testing |
| test_security_integration.py | 267 | 11 | 13 | 5 | Testing |
| test_sync.py | 147 | 8 | 13 | 4 | Testing |
| test_workflow_engine.py | 253 | 5 | 15 | 0 | Testing |

### Directory: `tests/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| __init__.cpython-313.pyc | 3 | 0 | 0 | 0 | Testing |
| conftest.cpython-313-pytest-8.4.2.pyc | 181 | 0 | 0 | 0 | Testing |
| conftest.cpython-313-pytest-9.0.2.pyc | 181 | 0 | 0 | 0 | Testing |
| test_basic_validation.cpython-313-pytest-9.0.2.pyc | 80 | 0 | 0 | 0 | Testing |
| test_hook_recursion.cpython-313-pytest-9.0.2.pyc | 854 | 0 | 0 | 0 | Testing |
| test_hooks.cpython-313-pytest-9.0.2.pyc | 381 | 0 | 0 | 0 | Testing |
| test_launch.cpython-313-pytest-9.0.2.pyc | 194 | 0 | 0 | 0 | Testing |
| test_launcher.cpython-313-pytest-9.0.2.pyc | 312 | 0 | 0 | 0 | Testing |
| test_sync.cpython-313-pytest-9.0.2.pyc | 529 | 0 | 0 | 0 | Testing |

### Directory: `tests/backend/node_engine`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_security_manager.py | 139 | 2 | 12 | 4 | Testing |

### Directory: `tests/contract`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_cli_contracts.py | 156 | 5 | 8 | 1 | Testing |

### Directory: `tests/contract/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_cli_contracts.cpython-313-pytest-9.0.2.pyc | 570 | 0 | 0 | 0 | Testing |

### Directory: `tests/core`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_advanced_workflow_engine.py | 165 | 4 | 9 | 3 | Testing |
| test_caching.py | 153 | 3 | 5 | 3 | Testing |
| test_data_source.py | 421 | 13 | 5 | 5 | Testing |
| test_email_repository.py | 69 | 4 | 2 | 0 | Testing |
| test_factory.py | 342 | 20 | 4 | 5 | Testing |
| test_notmuch_data_source.py | 563 | 8 | 14 | 6 | Testing |
| test_security.py | 200 | 12 | 15 | 3 | Testing |
| test_workflow_engine.py | 253 | 3 | 16 | 0 | Testing |

### Directory: `tests/functional`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_advanced_git.py | 84 | 5 | 3 | 0 | Testing |
| test_git_comparison.py | 57 | 4 | 1 | 0 | Testing |
| test_git_plumbing.py | 34 | 4 | 1 | 0 | Testing |
| test_json_mode.py | 29 | 4 | 2 | 0 | Testing |
| test_recovery.py | 26 | 3 | 2 | 0 | Testing |

### Directory: `tests/functional/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_advanced_git.cpython-313-pytest-9.0.2.pyc | 202 | 0 | 0 | 0 | Testing |
| test_git_comparison.cpython-313-pytest-9.0.2.pyc | 227 | 0 | 0 | 0 | Testing |
| test_git_plumbing.cpython-313-pytest-9.0.2.pyc | 64 | 0 | 0 | 0 | Testing |
| test_json_mode.cpython-313-pytest-9.0.2.pyc | 113 | 0 | 0 | 0 | Testing |
| test_recovery.cpython-313-pytest-9.0.2.pyc | 167 | 0 | 0 | 0 | Testing |

### Directory: `tests/integration`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_cli.py | 185 | 5 | 7 | 1 | Testing |
| test_cli_guides.py | 113 | 6 | 8 | 1 | Testing |

### Directory: `tests/integration/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_cli.cpython-313-pytest-9.0.2.pyc | 265 | 0 | 0 | 0 | Testing |

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

### Directory: `tests/unit`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_analysis_service.py | 171 | 4 | 7 | 7 | Testing |
| test_git_wrapper.py | 147 | 4 | 11 | 0 | Testing |
| test_merge_verifier.py | 19 | 3 | 1 | 1 | Testing |
| test_rebase_analyzer.py | 23 | 5 | 1 | 1 | Testing |
| test_rebase_detector.py | 19 | 3 | 1 | 1 | Testing |
| test_workflow_context.py | 33 | 2 | 4 | 0 | Testing |

### Directory: `tests/unit/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| test_analysis_service.cpython-313-pytest-9.0.2.pyc | 325 | 0 | 0 | 0 | Testing |
| test_git_wrapper.cpython-313-pytest-9.0.2.pyc | 490 | 0 | 0 | 0 | Testing |
| test_merge_verifier.cpython-313-pytest-9.0.2.pyc | 22 | 0 | 0 | 0 | Testing |
| test_rebase_analyzer.cpython-313-pytest-9.0.2.pyc | 37 | 0 | 0 | 0 | Testing |
| test_rebase_detector.cpython-313-pytest-9.0.2.pyc | 22 | 0 | 0 | 0 | Testing |
| test_workflow_context.cpython-313-pytest-8.4.2.pyc | 173 | 0 | 0 | 0 | Testing |
| test_workflow_context.cpython-313-pytest-9.0.2.pyc | 173 | 0 | 0 | 0 | Testing |

### Directory: `utils`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| .gitkeep | 0 | 0 | 0 | 0 | Other |

### Directory: `workspace`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| README.md | 98 | 0 | 0 | 0 | Documentation |

### Directory: `workspace/cli_architecture`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| factory.py | 108 | 2 | 5 | 1 | Core Logic |
| interface.py | 89 | 3 | 5 | 1 | Core Logic |
| registry.py | 158 | 3 | 9 | 1 | Core Logic |

### Directory: `workspace/git_analysis`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| commits.py | 107 | 4 | 3 | 1 | Core Logic |
| history.py | 79 | 5 | 0 | 2 | Core Logic |
| reordering.py | 65 | 3 | 1 | 1 | Core Logic |
| types.py | 12 | 1 | 0 | 1 | Core Logic |

### Directory: `workspace/git_analysis/__pycache__`

| File | LOC | Imports | Functions | Classes | Category |
|------|-----|---------|-----------|---------|----------|
| commits.cpython-312.pyc | 142 | 0 | 0 | 0 | Other |
| history.cpython-312.pyc | 110 | 0 | 0 | 0 | Other |
| reordering.cpython-312.pyc | 79 | 0 | 0 | 0 | Other |
| types.cpython-312.pyc | 11 | 0 | 0 | 0 | Other |

