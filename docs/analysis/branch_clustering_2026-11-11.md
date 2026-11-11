# Branch clustering analysis (task 002)

Generated from a live run against `/home/masum/github/remote/jules/workspaces/EmailIntelligence/state/mirror/EmailIntelligence.git`.

## Method

Every branch under the remote is scored by three independent analyzers, combined at the task's fixed weights, and clustered by Ward hierarchical agglomeration cut at a fixed distance:

| Stage | Weight | Input |
| --- | --- | --- |
| Commit history | 0.35 | commits on `main..branch` only, recency, authorship, merge readiness, stability |
| Codebase structure | 0.35 | directory similarity, file additions, core-module stability, namespace isolation |
| Diff distance | 0.30 | code churn, change concentration, diff complexity, integration risk |

- Linkage: Ward, Euclidean; cut at distance `0.5`.
- Integration targets are assigned through four levels in order: name/metric heuristics, archetype cosine affinity, cluster consensus, default.

## Headline numbers

| Measure | Value |
| --- | --- |
| Branches considered | 1818 |
| Branches analyzed | 1809 |
| Branches rejected (no merge base) | 9 |
| Clusters | 26 |
| Silhouette (avg) | 0.5833 |
| Davies-Bouldin | 0.8474 |
| Calinski-Harabasz | 9572.52 |

## Clusters by size

| # | Size | Cohesion | Combined score | Mean analyzer scores (history / structure / diff) | Sample members |
| --- | --- | --- | --- | --- | --- |
| 21 | 412 | 0.999 | 0.000 | 0.001 / 0.000 / 0.000 | `bolt/optimize-keyword-regex-8919410920181695339`, `bolt/search-debounce-14823980629961743161`, `ci/dependabot-automerge-fail-closed`, `dependabot/npm_and_yarn/client/framer-motion-14.6.0`, `dependabot/npm_and_yarn/client/jsdom-31.0.0`, +407 more |
| 24 | 218 | 0.966 | 0.324 | 0.200 / 0.356 / 0.431 | `000-integrated-specs`, `001-agent-context-control`, `001-command-registry-integration`, `001-orchestration-tools-consistency`, `001-orchestration-tools-verification-review`, +213 more |
| 16 | 145 | 0.971 | 0.631 | 0.200 / 0.851 / 0.877 | `bolt-async-email-search-4693660005507209938`, `bolt-async-search-1700927354422257992`, `bolt-cache-optimization-18364628782752433216`, `bolt-cache-optimization-3531886922800088779`, `bolt-cache-optimization-3614840988936812013`, +140 more |
| 26 | 121 | 0.947 | 0.361 | 0.197 / 0.464 / 0.432 | `001-rebase-analysis-specs`, `001-toolset-additive-analysis`, `003-unified-git-analysis`, `archive/historical-implementations`, `backend-consolidation`, +116 more |
| 11 | 99 | 0.957 | 0.649 | 0.193 / 0.864 / 0.931 | `bolt-database-search-optimization-17332120797985899697`, `bolt-database-search-optimization-6748640558952412491`, `bolt-debounce-search-1398074265106423797`, `bolt-optimize-get-emails-14611747676447537157`, `bolt-optimize-memory-cache-16538005949737429926`, +94 more |
| 15 | 95 | 0.950 | 0.622 | 0.209 / 0.870 / 0.815 | `add-comparison-files-to-main`, `bolt-content-search-optimization-11752978906130889211`, `bolt-optimize-smart-filter-invalidation-12306995843349801229`, `bolt-optimize-workflow-cleanup-memory-complexity-5380313799745612066`, `bolt-smart-filter-batch-updates-10623509739610348301`, +90 more |
| 12 | 91 | 0.952 | 0.627 | 0.136 / 0.863 / 0.924 | `Sentinel-CRITICAL]-Fix-missing-authentication-on-sensitive-endpoints`, `bolt-cache-get-emails-optimization-12679619644744086809`, `bolt-debounce-search-11171452089317330802`, `bolt-enforce-query-cache-capacity-5656601079512900964`, `bolt-lazy-email-context-filter-opt-14877540009260806442`, +86 more |
| 25 | 87 | 0.938 | 0.413 | 0.225 / 0.583 / 0.434 | `align-feature-notmuch-tagging-1`, `backend-refactor`, `docs/cleanup`, `docs/merge-docs-cleanup`, `docs/merge-docs-cleanup-to-comprehensive`, +82 more |
| 22 | 67 | 0.950 | 0.306 | 0.248 / 0.000 / 0.730 | `bolt-database-search-optimization-10639468176484359550`, `bolt-enhanced-caching-fix-15189319414508702031`, `bolt-optimize-db-sort-cache-8569994306623649862`, `bolt-optimize-eafp-database-io-8959520943282783781-4946642088847545950`, `bolt-optimize-workflow-cleanup-4132952529411191411`, +62 more |
| 19 | 46 | 0.911 | 0.739 | 0.466 / 0.934 / 0.830 | `bolt-journal-entry-new`, `bolt-optimize-text-utils-regex-3840185141648704649`, `docs/client-e2e-runbook`, `feature/task-009-slice-1`, `fix-audit-logger-queue-exception`, +41 more |
| 17 | 45 | 0.954 | 0.704 | 0.364 / 0.946 / 0.818 | `bugfix/sentinel-command-injection-scripts-rename-8155304876034522533`, `complex-branch-analysis`, `complex-branch-analysis-3961097721601040719`, `feat/task-019-deploy-plan`, `feature-merge-validation-6547788568774529922`, +40 more |
| 1 | 43 | 0.928 | 0.544 | 0.184 / 0.868 / 0.588 | `add-comparison-files-to-scientific`, `backup/scientific-20251129-132118`, `bolt-optimize-audit-logger-3896725142875397422`, `bolt-optimize-workflow-cleanup-memory-complexity-5380313799745612066-16246116557128889789`, `bolt-optimize-workflow-cleanup-memory-complexity-5380313799745612066-5726068222511822124`, +38 more |
| 4 | 43 | 0.945 | 0.571 | 0.129 / 0.842 / 0.769 | `bolt-optimize-database-search-4540183078167904732`, `bolt-optimize-search-io-368565110711438303`, `bolt-optimize-search-io-4063477833861769953`, `bolt-optimize-smart-filter-regex-14305652007130065894`, `bolt-search-cache-optimization-17231589403034892496`, +38 more |
| 18 | 40 | 0.912 | 0.677 | 0.350 / 0.868 / 0.835 | `bolt-smart-filter-lazy-eval-12679806066699207963`, `feature-task-009-slice-1-9128899407342713793`, `feature/task-009-slice-1-8489459750423481980`, `fix/bolt-2-clean-v2`, `jules/task003-validate-no-todos`, +35 more |
| 8 | 35 | 0.909 | 0.480 | 0.173 / 0.769 / 0.499 | `bolt-optimize-memory-cache-lru-240038953332671293`, `bolt-query-result-caching-12874945111088722875`, `bolt-rate-limiter-memory-exhaustion-1632179022360231273-10723384563685907073`, `bolt-rate-limiter-memory-exhaustion-1632179022360231273-10723384563685907073-14526103937317527694`, `bolt-smart-filter-optimization-18076606322863480435`, +30 more |
| 7 | 31 | 0.913 | 0.426 | 0.177 / 0.673 / 0.429 | `bolt-optimize-memory-cache-lru-240038953332671293-11053728609860372163`, `bolt-workflow-memory-optimization-11867655261819744500`, `bolt-workflow-memory-optimization-11867655261819744500-12254347793198898246`, `bugfix/backend-fixes-and-test-suite-stabilization`, `docs/comprehensive-documentation`, +26 more |
| 3 | 29 | 0.946 | 0.562 | 0.164 / 0.853 / 0.687 | `bolt-caching-capacity-limit-9307877399307151176`, `bolt-optimize-ai-engine-12203455504678449603`, `bolt-perf-email-context-lazy-eval-13364391327843600411`, `bolt/optimize-email-filtering-15760458014158965700`, `bolt/react-memo-optimizations-5814112027244730925-12706650364775836825`, +24 more |
| 6 | 29 | 0.921 | 0.523 | 0.173 / 0.760 / 0.653 | `bolt-optimize-emaillist-237124919842135197`, `bolt/search-query-caching-3778809004459403554`, `cto/batch-update-pr-heads-legacy-safeguards`, `dependabot/npm_and_yarn/npm_and_yarn-4a5a8f34f1`, `feat/context-awareness-system-1765572654974843001`, +24 more |
| 20 | 28 | 0.888 | 0.785 | 0.601 / 0.942 / 0.817 | `dependabot-npm`, `dependabot-pip`, `dependabot/npm_and_yarn/npm_and_yarn-e4d94ae230`, `extract-cli-consolidated`, `extract/cli-consolidated`, +23 more |
| 10 | 27 | 0.921 | 0.504 | 0.413 / 0.671 / 0.417 | `fix-ci-infrastructure-2506962712549882166-12619674719022427918`, `fix-linting-src-main`, `fix-linting-src-main-16014091508439210228`, `fix/ci-infrastructure-2506962712549882166-12619674719022427918`, `pull/698/head`, +22 more |
| 13 | 22 | 0.923 | 0.590 | 0.188 / 0.742 / 0.882 | `add-comparison-files-to-orchestration-tools`, `bolt-db-optimization-4935874087585178417`, `feat-enhanced-filtering`, `feature/search-in-category`, `feature/taskmaster-protection`, +17 more |
| 14 | 14 | 0.889 | 0.635 | 0.335 / 0.738 / 0.866 | `001-implement-planning-workflow`, `002-execution-layer-tasks`, `bolt-search-debounce-14823980629961743161`, `feature/generate-tasks-md`, `perf-sidebar-react-memo-bolt-445513471566265092`, +9 more |
| 2 | 12 | 0.879 | 0.618 | 0.331 / 0.863 / 0.669 | `bolt/optimize-keyword-extraction-regex-6825852734872785736`, `fix-path-traversal-sanitize-path-7024475819244259973`, `fix/cve-2026-4800-lodash-4.18.0-15014477667741021080`, `pull/454/head`, `pull/564/head`, +7 more |
| 23 | 11 | 0.977 | 0.416 | 0.455 / 0.367 / 0.429 | `aligned-final-pr-489`, `aligned-pr-471`, `aligned-pr-474`, `aligned-pr-476`, `aligned-pr-478`, +6 more |
| 5 | 10 | 0.879 | 0.499 | 0.155 / 0.629 / 0.748 | `001-rebase-analysis`, `002-validate-orchestration-tools`, `003-execution-layer-tasks-pr`, `jules-14524679377202940941-e5686378-10680519591823246444`, `orchestration-tools-changes-4`, +5 more |
| 9 | 9 | 0.897 | 0.664 | 0.650 / 0.874 / 0.437 | `cli-tree-followup`, `extract/taskmaster`, `fix/cli-dependency-port`, `specs/W1`, `specs/W2`, +4 more |

## Content clustering (what the diffs actually contain)

Stage one ranks a branch by aggregate scores, so two branches with similar scores can touch unrelated code. This stage clusters on the branch's content at several detail levels. Every token is mapped to one of 65,536 buckets by `blake2b`, with the sign taken from the digest, so there is no fitted vocabulary and the same branch always yields the same vector. One average-linkage tree is cut at a grid of cosine thresholds; the cut with the best silhouette is the primary partition and every finer cluster records the coarser cluster that contains it.

| Measure | Value |
| --- | --- |
| Branch documents | 1398 |
| Excluded (no diff content) | 411 |
| Detail levels | message, path, path_pair, subword, symbol, symbol_pair |
| Clusters (primary cut) | 57 |
| Silhouette (avg) | 0.2743 |
| Cut threshold | 0.75 |
| Vocabulary | 65536 hashed buckets, no fitted vocabulary |
| Agreement with the score view (ARI) | 0.3109 |

### Detail levels and their weights

| Level | Weight | What it captures |
| --- | --- | --- |
| `path` | 1.00 | path prefixes and segments |
| `path_pair` | 0.70 | adjacent path-segment pairs |
| `symbol` | 1.20 | identifier words from added lines |
| `symbol_pair` | 0.80 | adjacent identifier pairs |
| `message` | 0.60 | commit-subject words and word pairs |
| `subword` | 0.40 | character 4-grams of identifiers |

### Hierarchy of cuts

| Cosine cut | Clusters | Silhouette | Primary |
| --- | --- | --- | --- |
| 0.75 | 57 | 0.2743 | yes |
| 0.85 | 25 | 0.1870 |  |
| 0.95 | 7 | 0.1046 |  |

### How each level agrees with the combined partition

| Level | ARI vs combined |
| --- | --- |
| `path` | 0.5241 |
| `path_pair` | 0.318 |
| `symbol` | n/a |
| `symbol_pair` | n/a |
| `message` | 0.2201 |
| `subword` | n/a |

A low silhouette here is the honest result, not a failed run: most of the fleet edits Python under `src/`, so their vocabularies overlap and no cut separates cleanly. The low agreement with the score view says that view is not a proxy for content — branches that score alike are often about different code. This is a lexical method: it groups a merge wave, it does not prove two branches equivalent.

### Content clusters with signature terms

Signature terms are the tokens most over-represented inside a cluster relative to the rest of the fleet.

| # | Size | Cohesion | Signature terms | Sample members |
| --- | --- | --- | --- | --- |
| 46 | 351 | 0.589 | `id/task`, `path/scripts`, `prefix/scripts`, `pair/path/temp+path/untracked`, `pair/path/untracked+path/files`, `pair/task+master`, `path/files`, `path/temp` | `000-integrated-specs`, `001-rebase-analysis-specs`, `004-guided-workflow`, `aligned-final-pr-489`, `aligned-pr-471`, +346 more |
| 32 | 262 | 0.392 | `path/staging`, `path/deploy`, `pair/path/deploy+path/staging`, `pair/path/staging+path/yml`, `path/yml`, `path/core`, `prefix/github/workflows/deploy/staging/yml/deploy`, `prefix/github/workflows/deploy/staging/yml` | `bolt-async-email-search-4693660005507209938`, `bolt-async-search-1700927354422257992`, `bolt-cache-optimization-18364628782752433216`, `bolt-cache-optimization-3531886922800088779`, `bolt-cache-optimization-3614840988936812013`, +257 more |
| 28 | 129 | 0.552 | `id/whl`, `id/org`, `id/sha256`, `id/https`, `id/url`, `id/hash`, `pair/hash+sha256`, `pair/url+https` | `bolt-cache-get-emails-optimization-12679619644744086809`, `bolt-enforce-query-cache-capacity-5656601079512900964`, `bolt-lazy-email-context-filter-opt-14877540009260806442`, `bolt-optimize-ai-engine-12203455504678449603`, `bolt-optimize-audit-logger-3896725142875397422`, +124 more |
| 37 | 125 | 0.360 | `path/backend`, `pair/path/src+path/backend`, `pair/path/backend+path/python`, `prefix/src`, `path/src`, `pair/path/python+path/backend`, `prefix/src/backend`, `path/python` | `001-command-registry-integration`, `001-orchestration-tools-consistency`, `001-orchestration-tools-verification-review`, `001-pr176-integration-fixes`, `001-task-execution-layer`, +120 more |
| 24 | 113 | 0.437 | `id/node`, `id/https`, `id/sha512`, `id/integrity`, `id/npmjs`, `id/tgz`, `path/json`, `id/registry` | `bolt-rate-limiter-memory-exhaustion-1632179022360231273`, `bolt-rate-limiter-memory-exhaustion-1632179022360231273-10723384563685907073`, `bolt-rate-limiter-memory-exhaustion-1632179022360231273-10723384563685907073-14526103937317527694`, `bolt/optimize-search-emails-with-limit-10502466804609748602`, `bolt/regex-optimization-5088526991375117070`, +108 more |
| 30 | 86 | 0.394 | `path/yml`, `path/jules`, `pair/path/github+path/workflows`, `prefix/github/workflows`, `prefix/github`, `path/github`, `path/workflows`, `pair/path/disabled+path/github` | `bolt-debounce-search-11171452089317330802`, `bolt-debounce-search-1398074265106423797`, `bolt-optimize-text-utils-regex-3840185141648704649`, `bolt-search-debounce-fix`, `bolt/optimize-text-utils-clean`, +81 more |
| 44 | 46 | 0.453 | `pair/path/backlog+path/tasks`, `path/backlog`, `path/task`, `path/tasks`, `pair/path/tasks+path/task`, `prefix/backlog`, `prefix/backlog/tasks`, `id/github` | `align-feature-notmuch-tagging-1`, `backend-refactor`, `backup/scientific-20251129-132118`, `branch-integration`, `diverged-scientific-20251115161324`, +41 more |
| 56 | 36 | 0.461 | `id/branch`, `id/run`, `prefix/scripts`, `path/scripts`, `id/mock`, `id/base`, `id/git`, `id/sys` | `complex-branch-analysis`, `complex-branch-analysis-3961097721601040719`, `feature-merge-validation-6547788568774529922`, `feature-task-009-slice-1-9128899407342713793`, `feature/merge-validation`, +31 more |
| 35 | 31 | 0.376 | `pair/path/backend+path/node`, `pair/path/node+path/engine`, `path/node`, `path/engine`, `path/backend`, `id/input`, `id/node`, `id/value` | `bolt-optimize-workflow-cleanup-memory-complexity-5380313799745612066`, `bolt-query-result-caching-12874945111088722875`, `bolt-smart-filter-optimization-18076606322863480435`, `bolt/database-query-caching-17443091033903107417`, `configurable-sanitization-policies-4397196737957899891`, +26 more |
| 23 | 24 | 0.439 | `pair/path/client+path/src`, `prefix/client/src`, `prefix/client`, `path/client`, `pair/path/src+path/components`, `path/tsx`, `id/react`, `prefix/client/src/components` | `bolt-caching-capacity-limit-9307877399307151176`, `bolt-optimize-workflow-cleanup-4132952529411191411`, `bolt-search-debounce-14823980629961743161`, `bolt/debounce-search-8687753454070474780`, `fix-frontend-type-errors`, +19 more |
| 27 | 21 | 0.366 | `id/command`, `id/run`, `path/setup`, `prefix/setup`, `id/result`, `id/logger`, `id/python`, `id/subprocess` | `002-validate-orchestration-tools`, `cto/batch-update-pr-heads-legacy-safeguards`, `cto/fix-download-artifact-version-8825342107962755172`, `cto/stabilize-standardize-pr-launcher-659-660-661`, `fix/ci-test-failures`, +16 more |
| 26 | 15 | 0.548 | `id/password`, `path/auth`, `id/hash`, `id/verify`, `pair/path/core+path/auth`, `id/user`, `pair/verify+password`, `path/core` | `fix-auth-missing-deps-4150481951493984002`, `fix-auth-verify-password-4928457512359891241`, `jules/4928457512359891241`, `pull/240/head`, `pull/244/head`, +10 more |
| 48 | 15 | 0.369 | `id/git`, `id/orchestration`, `id/branch`, `pair/orchestration+tools`, `id/file`, `id/tools`, `path/analysis`, `msg/feat` | `001-agent-context-control`, `001-rebase-analysis`, `001-toolset-additive-analysis`, `003-unified-git-analysis`, `archive/historical-implementations`, +10 more |
| 29 | 14 | 0.530 | `id/actions`, `id/uses`, `pair/uses+actions`, `pair/path/github+path/workflows`, `id/setup`, `prefix/github/workflows`, `prefix/github`, `path/github` | `cto/fix-download-artifact-version`, `github-script-9-fix`, `pull/536/head`, `pull/537/head`, `pull/538/head`, +9 more |
| 47 | 11 | 0.383 | `pair/path/scripts+path/hooks`, `id/branch`, `path/hooks`, `prefix/scripts/hooks`, `id/orchestration`, `pair/path/hooks+path/post`, `prefix/scripts/hooks/post`, `path/post` | `001-implement-planning-workflow`, `002-execution-layer-tasks`, `003-execution-layer-tasks-pr`, `add-comparison-files-to-main`, `add-comparison-files-to-orchestration-tools`, +6 more |
| 51 | 11 | 0.452 | `id/command`, `path/cli`, `pair/path/cli+path/commands`, `pair/path/src+path/cli`, `id/name`, `path/commands`, `pair/path/scripts+path/automation`, `msg/cli` | `cli-tree-followup`, `extract-cli-consolidated`, `extract/cli-consolidated`, `fix/cli-dependency-port`, `jules/task007-identify-command`, +6 more |
| 39 | 8 | 0.379 | `id/path`, `pair/path/src+path/core`, `cg/path`, `path/core`, `pair/path/core+path/security`, `prefix/src/core`, `id/model`, `pair/path+path` | `fix-path-traversal-sanitize-path-7024475819244259973`, `jules-8042179028824925778-118473c6`, `pr-139-head`, `pr-140-head`, `pull/134/head`, +3 more |
| 1 | 6 | 0.529 | `id/python`, `pair/path/requirements+path/versions`, `pair/path/versions+path/txt`, `path/requirements`, `path/txt`, `prefix/requirements/versions`, `prefix/requirements/versions/txt`, `path/versions` | `pull/546/head`, `pull/619/head`, `pull/686/head`, `pull/714/head`, `pull/748/head`, +1 more |
| 7 | 6 | 0.540 | `path/e2e`, `pair/path/client+path/e2e`, `id/page`, `prefix/client/e2e`, `prefix/client`, `path/client`, `id/playwright`, `id/client` | `docs/client-e2e-runbook`, `jules-15594770323986482511-8149f6e5`, `jules-15636604994837361746-9b989797`, `pull/975/head`, `pull/976/head`, +1 more |
| 10 | 6 | 0.386 | `id/disabled`, `pair/path/jules+path/sunset`, `pair/path/docs+path/jules`, `path/sunset`, `prefix/docs/jules`, `prefix/backlog/tasks/alignment/task/feature`, `prefix/docs`, `path/docs` | `jules-sunset-bootstrap`, `s11-consolidate-1794330090`, `s13-forensics-1794327866`, `scientific-triage-docs`, `sunset/lost-features-disabled`, +1 more |

> Deterministic hashed multi-level clustering over path segments and prefixes, identifier words and pairs, commit-subject words and pairs, and sub-word 4-grams. It captures shared vocabulary, not shared behaviour; use it to group a merge wave, not to prove equivalence.

## Integration targets

| Target | Branches | Mean confidence | Leading tags |
| --- | --- | --- | --- |
| `main` | 1563 | 0.940 | `main-ready`, `testing-required-high`, `requires-review`, `medium-risk`, `low-file-impact` |
| `scientific` | 77 | 0.881 | `scientific-branch`, `testing-required-high`, `requires-review`, `complex`, `refactoring` |
| `orchestration-tools` | 169 | 0.899 | `orchestration-branch`, `testing-required-high`, `requires-review`, `medium-risk`, `complex` |

### Which level decided

| Decision level | Branches | Share |
| --- | --- | --- |
| 1 · heuristic | 533 | 29.5% |
| 2 · archetype affinity | 18 | 1.0% |
| 3 · cluster consensus | 1229 | 67.9% |
| 4 · default | 29 | 1.6% |

A high default share would mean the hierarchy is not earning its keep; a high heuristic share means the name-based rules dominate and the numeric levels rarely get a chance to speak.

### Most frequent tags

| Tag | Branches |
| --- | --- |
| `main-ready` | 1563 |
| `testing-required-high` | 1365 |
| `requires-review` | 1230 |
| `medium-risk` | 1167 |
| `refactoring` | 989 |
| `complex` | 989 |
| `minor-feature` | 923 |
| `low-file-impact` | 923 |
| `has-breaking-changes` | 867 |
| `moderate` | 820 |
| `low-risk` | 642 |
| `stale` | 578 |
| `massive-impact` | 571 |
| `testing-required-medium` | 444 |
| `core-feature` | 433 |

## Rejected branches

These are reported rather than dropped. Each one shares no history with the baseline, so no meaningful diff exists and no analyzer can score it.

| Branch | Reason |
| --- | --- |
| `beads-sync` | git diff --diff-filter=A --name-only refs/remotes/origin/main...beads-sync failed: fatal: refs/remotes/origin/main...beads-sync: no merge base |
| `chore/cli-tooling-requirements-review-8803610982851555196` | git diff --diff-filter=A --name-only refs/remotes/origin/main...chore/cli-tooling-requirements-review-8803610982851555196 failed: fatal: refs/remotes/origin/main...chore/cli-tooling-requirements-review-8803610982851555196: no merge base |
| `entire/checkpoints/v1` | git diff --diff-filter=A --name-only refs/remotes/origin/main...entire/checkpoints/v1 failed: fatal: refs/remotes/origin/main...entire/checkpoints/v1: no merge base |
| `master` | git diff --diff-filter=A --name-only refs/remotes/origin/main...master failed: fatal: refs/remotes/origin/main...master: no merge base |
| `pull/679/head` | git diff --diff-filter=A --name-only refs/remotes/origin/main...pull/679/head failed: fatal: refs/remotes/origin/main...pull/679/head: no merge base |
| `pull/927/head` | git diff --diff-filter=A --name-only refs/remotes/origin/main...pull/927/head failed: fatal: refs/remotes/origin/main...pull/927/head: no merge base |
| `pull/937/head` | git diff --diff-filter=A --name-only refs/remotes/origin/main...pull/937/head failed: fatal: refs/remotes/origin/main...pull/937/head: no merge base |
| `task-022-marker-scanner` | git diff --diff-filter=A --name-only refs/remotes/origin/main...refs/remotes/origin/task-022-marker-scanner failed: fatal: refs/remotes/origin/main...refs/remotes/origin/task-022-marker-scanner: no merge base |
| `taskmaster` | git diff --diff-filter=A --name-only refs/remotes/origin/main...taskmaster failed: fatal: refs/remotes/origin/main...taskmaster: no merge base |

## How to reproduce

```bash
python -m src.analysis.clustering \
  --repo /home/masum/github/remote/jules/workspaces/EmailIntelligence/state/mirror/EmailIntelligence.git \
  --main refs/remotes/origin/main \
  --threshold 0.5 \
  --jobs 16 --out report.json
```
