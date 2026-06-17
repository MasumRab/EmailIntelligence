**Sweep COMPLETE (2026-06-12)** — the remaining recent docs were scanned for task-dependency/structure claims. **No new corrections to the 001–012 core graph.** Results:

| Doc / group | Result of sweep |
|-------------|-----------------|
| \`.iflow/PHASE_1_SCRIPT_REFERENCE_AUDIT.md\`, \`TRIAGE_HANDOFF_PROMPT.md\` | Script-ref / handoff content only; no task-graph claims (covered by \`TRIAGE_REPORT.md\`) |
| \`.iflow/understand/enhanced_architecture.md\` | **Corroborates** 4-layer depth + \"no circular dependencies\"; uses Gen-2 numbering (Task 079 = orchestrator = current 012) |
| \`.qwen/PROJECT_SUMMARY.md\` | **Corroborates** layered model in Gen-2 numbering: \"Tasks 74–83 … Task 79 as central orchestrator\" |
| \`docs/three_branch_architectural_comparison.md\`, \`scientific_branch_conflict_resolution_plan.md\` | Branch/code architecture only; no task-graph claims (one *code-level* circular-import warning, not a task dep) |
| \`docs/task_004_tuned_recommendations.md\` | Scope refinement only — expand 004's branch list beyond main/scientific/orchestration-tools |
| \`reports/ck_similarity_analysis.md\` | **Minor finding:** \`task_021.md\` has duplicated config blocks (lines 513≈3009, 897≈3393) — intra-file corruption in a tail task (supports the 023/024/025 malformed-block note in §5d) |
| \`reports/task75_techspec_verification.md\`, \`cli_tooling_requirements_review.md\` | No task-graph claims |
| \`scripts/*.py\` (Jun 8) | Code, not docs — out of doc-map scope |
