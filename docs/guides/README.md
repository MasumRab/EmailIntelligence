# Guides Index

Operational and how-to guides referenced across the `main` and `scientific` branches.

| Guide                     | Path                                                               | Purpose                                                                                                  |
| ------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Branch Switching          | [`branch_switching_guide.md`](branch_switching_guide.md)           | How to move between `main`, `scientific`, and the substrate branches without violating the branch model. |
| Workflow & Review Process | [`workflow_and_review_process.md`](workflow_and_review_process.md) | PR lifecycle, review gates, and CI control on product branches.                                          |

## Related

- `[docs/git_workflow_plan.md](../git_workflow_plan.md)` — project-wide git workflow.
- `[docs/orchestration_branch_scope.md](../orchestration_branch_scope.md)` — scope rules per branch.
- 📜 **Canonical branch rules** live in the `.taskmaster` ledger: [`.taskmaster/BRANCH_MANAGEMENT_MODEL.md`](../../../taskmaster/BRANCH_MANAGEMENT_MODEL.md) (submodule, gitignored on product branches — run `git submodule update --init` to read locally).
