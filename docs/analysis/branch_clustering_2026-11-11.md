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
| Silhouette (avg) | 0.5830 |
| Davies-Bouldin | 0.8458 |
| Calinski-Harabasz | 9563.96 |

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
| 25 | 89 | 0.934 | 0.412 | 0.223 / 0.583 / 0.435 | `align-feature-notmuch-tagging-1`, `backend-refactor`, `docs/cleanup`, `docs/merge-docs-cleanup`, `docs/merge-docs-cleanup-to-comprehensive`, +84 more |
| 22 | 67 | 0.950 | 0.306 | 0.248 / 0.000 / 0.730 | `bolt-database-search-optimization-10639468176484359550`, `bolt-enhanced-caching-fix-15189319414508702031`, `bolt-optimize-db-sort-cache-8569994306623649862`, `bolt-optimize-eafp-database-io-8959520943282783781-4946642088847545950`, `bolt-optimize-workflow-cleanup-4132952529411191411`, +62 more |
| 19 | 46 | 0.911 | 0.739 | 0.466 / 0.934 / 0.830 | `bolt-journal-entry-new`, `bolt-optimize-text-utils-regex-3840185141648704649`, `docs/client-e2e-runbook`, `feature/task-009-slice-1`, `fix-audit-logger-queue-exception`, +41 more |
| 17 | 45 | 0.954 | 0.704 | 0.365 / 0.946 / 0.818 | `bugfix/sentinel-command-injection-scripts-rename-8155304876034522533`, `complex-branch-analysis`, `complex-branch-analysis-3961097721601040719`, `feat/task-019-deploy-plan`, `feature-merge-validation-6547788568774529922`, +40 more |
| 1 | 43 | 0.928 | 0.544 | 0.184 / 0.868 / 0.588 | `add-comparison-files-to-scientific`, `backup/scientific-20251129-132118`, `bolt-optimize-audit-logger-3896725142875397422`, `bolt-optimize-workflow-cleanup-memory-complexity-5380313799745612066-16246116557128889789`, `bolt-optimize-workflow-cleanup-memory-complexity-5380313799745612066-5726068222511822124`, +38 more |
| 4 | 43 | 0.945 | 0.571 | 0.129 / 0.842 / 0.769 | `bolt-optimize-database-search-4540183078167904732`, `bolt-optimize-search-io-368565110711438303`, `bolt-optimize-search-io-4063477833861769953`, `bolt-optimize-smart-filter-regex-14305652007130065894`, `bolt-search-cache-optimization-17231589403034892496`, +38 more |
| 18 | 40 | 0.912 | 0.677 | 0.351 / 0.868 / 0.835 | `bolt-smart-filter-lazy-eval-12679806066699207963`, `feature-task-009-slice-1-9128899407342713793`, `feature/task-009-slice-1-8489459750423481980`, `fix/bolt-2-clean-v2`, `jules/task003-validate-no-todos`, +35 more |
| 8 | 35 | 0.909 | 0.480 | 0.173 / 0.769 / 0.499 | `bolt-optimize-memory-cache-lru-240038953332671293`, `bolt-query-result-caching-12874945111088722875`, `bolt-rate-limiter-memory-exhaustion-1632179022360231273-10723384563685907073`, `bolt-rate-limiter-memory-exhaustion-1632179022360231273-10723384563685907073-14526103937317527694`, `bolt-smart-filter-optimization-18076606322863480435`, +30 more |
| 3 | 29 | 0.946 | 0.562 | 0.164 / 0.853 / 0.687 | `bolt-caching-capacity-limit-9307877399307151176`, `bolt-optimize-ai-engine-12203455504678449603`, `bolt-perf-email-context-lazy-eval-13364391327843600411`, `bolt/optimize-email-filtering-15760458014158965700`, `bolt/react-memo-optimizations-5814112027244730925-12706650364775836825`, +24 more |
| 6 | 29 | 0.921 | 0.523 | 0.173 / 0.760 / 0.653 | `bolt-optimize-emaillist-237124919842135197`, `bolt/search-query-caching-3778809004459403554`, `cto/batch-update-pr-heads-legacy-safeguards`, `dependabot/npm_and_yarn/npm_and_yarn-4a5a8f34f1`, `feat/context-awareness-system-1765572654974843001`, +24 more |
| 7 | 29 | 0.920 | 0.429 | 0.182 / 0.679 / 0.427 | `bolt-optimize-memory-cache-lru-240038953332671293-11053728609860372163`, `bolt-workflow-memory-optimization-11867655261819744500`, `bolt-workflow-memory-optimization-11867655261819744500-12254347793198898246`, `bugfix/backend-fixes-and-test-suite-stabilization`, `docs/comprehensive-documentation`, +24 more |
| 20 | 28 | 0.888 | 0.785 | 0.602 / 0.942 / 0.817 | `dependabot-npm`, `dependabot-pip`, `dependabot/npm_and_yarn/npm_and_yarn-e4d94ae230`, `extract-cli-consolidated`, `extract/cli-consolidated`, +23 more |
| 10 | 27 | 0.921 | 0.504 | 0.413 / 0.671 / 0.417 | `fix-ci-infrastructure-2506962712549882166-12619674719022427918`, `fix-linting-src-main`, `fix-linting-src-main-16014091508439210228`, `fix/ci-infrastructure-2506962712549882166-12619674719022427918`, `pull/698/head`, +22 more |
| 13 | 22 | 0.923 | 0.590 | 0.188 / 0.742 / 0.882 | `add-comparison-files-to-orchestration-tools`, `bolt-db-optimization-4935874087585178417`, `feat-enhanced-filtering`, `feature/search-in-category`, `feature/taskmaster-protection`, +17 more |
| 14 | 14 | 0.889 | 0.635 | 0.335 / 0.738 / 0.866 | `001-implement-planning-workflow`, `002-execution-layer-tasks`, `bolt-search-debounce-14823980629961743161`, `feature/generate-tasks-md`, `perf-sidebar-react-memo-bolt-445513471566265092`, +9 more |
| 2 | 12 | 0.879 | 0.619 | 0.331 / 0.863 / 0.669 | `bolt/optimize-keyword-extraction-regex-6825852734872785736`, `fix-path-traversal-sanitize-path-7024475819244259973`, `fix/cve-2026-4800-lodash-4.18.0-15014477667741021080`, `pull/454/head`, `pull/564/head`, +7 more |
| 23 | 11 | 0.977 | 0.416 | 0.455 / 0.367 / 0.429 | `aligned-final-pr-489`, `aligned-pr-471`, `aligned-pr-474`, `aligned-pr-476`, `aligned-pr-478`, +6 more |
| 5 | 10 | 0.879 | 0.499 | 0.155 / 0.629 / 0.748 | `001-rebase-analysis`, `002-validate-orchestration-tools`, `003-execution-layer-tasks-pr`, `jules-14524679377202940941-e5686378-10680519591823246444`, `orchestration-tools-changes-4`, +5 more |
| 9 | 9 | 0.897 | 0.664 | 0.650 / 0.874 / 0.437 | `cli-tree-followup`, `extract/taskmaster`, `fix/cli-dependency-port`, `specs/W1`, `specs/W2`, +4 more |

## Content clustering (what the diffs actually contain)

Stage one ranks a branch by aggregate scores, so two branches with similar scores can touch unrelated code. This stage clusters on the branch's content: the paths it changes, the identifiers on the lines it adds, and its commit subjects. Tokens are TF-IDF weighted, branches are compared by cosine distance with average linkage, and the cut is the threshold from 0.30 to 0.90 that maximises silhouette.

| Measure | Value |
| --- | --- |
| Branch documents | 1398 |
| Excluded (no diff content) | 411 |
| Clusters | 37 |
| Silhouette (avg) | 0.2035 |
| Cut threshold | 0.9 |
| Vocabulary | 23465 terms |
| Agreement with the score view (ARI) | 0.2059 |

A low silhouette here is the honest result, not a failed run: most of the fleet edits Python under `src/`, so their vocabularies overlap and no cut separates cleanly. The low agreement with the score view says that view is not a proxy for content — branches that score alike are often about different code. This is a lexical method: it groups a merge wave, it does not prove two branches equivalent.

### Content clusters with signature terms

Signature terms are the tokens most over-represented inside a cluster relative to the rest of the fleet.

| # | Size | Cohesion | Signature terms | Sample members |
| --- | --- | --- | --- | --- |
| 20 | 627 | 0.306 | `path/scripts`, `path/speckit`, `id/task`, `path/commands`, `id/branch`, `path/files`, `path/untracked`, `path/temp` | `000-integrated-specs`, `001-agent-context-control`, `001-command-registry-integration`, `001-implement-planning-workflow`, `001-orchestration-tools-consistency`, +622 more |
| 10 | 144 | 0.358 | `id/sha256`, `id/pythonhosted`, `id/hash`, `id/org`, `id/upload`, `id/packages`, `id/manylinux`, `id/whl` | `bolt-cache-get-emails-optimization-12679619644744086809`, `bolt-enforce-query-cache-capacity-5656601079512900964`, `bolt-lazy-email-context-filter-opt-14877540009260806442`, `bolt-optimize-ai-engine-12203455504678449603`, `bolt-optimize-audit-logger-3896725142875397422`, +139 more |
| 11 | 141 | 0.182 | `id/field`, `id/sorted`, `id/emails`, `id/manager`, `id/subject`, `id/email`, `id/caching`, `id/invalidate` | `bolt-async-email-search-4693660005507209938`, `bolt-async-search-1700927354422257992`, `bolt-content-search-optimization-11752978906130889211`, `bolt-database-optimization-17548196625265189719`, `bolt-database-search-optimization-17332120797985899697`, +136 more |
| 30 | 139 | 0.282 | `path/yml`, `path/staging`, `path/github`, `path/workflows`, `path/deploy`, `path/disabled`, `path/jules`, `msg/disable` | `Sentinel-CRITICAL]-Fix-missing-authentication-on-sensitive-endpoints`, `bolt-database-search-optimization-10639468176484359550`, `bolt-debounce-search-11171452089317330802`, `bolt-debounce-search-1398074265106423797`, `bolt-enhanced-caching-fix-15189319414508702031`, +134 more |
| 32 | 99 | 0.205 | `id/npmjs`, `id/sha512`, `id/tgz`, `id/integrity`, `id/license`, `id/registry`, `id/mit`, `id/org` | `bolt-rate-limiter-memory-exhaustion-1632179022360231273`, `bolt-rate-limiter-memory-exhaustion-1632179022360231273-10723384563685907073`, `bolt-rate-limiter-memory-exhaustion-1632179022360231273-10723384563685907073-14526103937317527694`, `bolt-search-debounce-14823980629961743161`, `bolt/optimize-search-emails-with-limit-10502466804609748602`, +94 more |
| 12 | 39 | 0.241 | `id/sanitized`, `id/html`, `id/dest`, `id/plugin`, `id/scheme`, `id/sanitize`, `id/zip`, `id/mock` | `bolt-query-result-caching-12874945111088722875`, `bolt-smart-filter-optimization-18076606322863480435`, `bolt/database-query-caching-17443091033903107417`, `configurable-sanitization-policies-4397196737957899891`, `fix/plugin-ssrf-vulnerability-1968977037766676891`, +34 more |
| 25 | 25 | 0.347 | `id/hashed`, `id/password`, `id/argon2`, `id/hash`, `id/dummy`, `msg/auth`, `id/salt`, `id/mismatch` | `fix-auth-missing-deps-4150481951493984002`, `fix-auth-nameerror-13113702114495648408`, `fix-auth-verify-password-4928457512359891241`, `jules/4928457512359891241`, `pull/240/head`, +20 more |
| 8 | 22 | 0.230 | `id/props`, `id/react`, `id/badge`, `id/memo`, `msg/react`, `id/chevron`, `path/tsx`, `msg/memo` | `bolt-caching-capacity-limit-9307877399307151176`, `bolt/debounce-search-8687753454070474780`, `fix-frontend-type-errors`, `fix/bolt-2-clean-v3`, `jules-6499354896973205490-bec36d2a`, +17 more |
| 23 | 22 | 0.243 | `id/fastapi`, `id/router`, `id/depends`, `id/user`, `id/noqa`, `id/e402`, `id/active`, `path/routes` | `final-pr-fix`, `fix-auth-bypass-registration-3387248403392921971`, `fix-plugin-model-routes-auth`, `fix/auth-968c3d59`, `jules-2805886462875627129-df438669`, +17 more |
| 29 | 21 | 0.436 | `id/ordered`, `id/popitem`, `id/cache`, `id/lru`, `id/recently`, `id/move`, `id/expires`, `id/end` | `bolt-cache-optimization-18364628782752433216`, `bolt-cache-optimization-3531886922800088779`, `bolt-cache-optimization-3614840988936812013`, `bolt-cache-optimization-4658261012249161886`, `bolt-optimize-memory-cache-14147381325537256669`, +16 more |
| 27 | 16 | 0.401 | `id/bucket`, `id/echo`, `id/checks`, `id/event`, `msg/flags`, `id/dependabot`, `id/exit`, `id/blockers` | `enhance/dependabot-auto-merge`, `fix-ci-infrastructure-2506962712549882166-6236298220428978887`, `fix-dependabot-automerge`, `fix/ci-infrastructure-2506962712549882166`, `fix/dependabot-auto-merge-ci-merged`, +11 more |
| 17 | 10 | 0.294 | `id/consumer`, `id/port`, `id/node`, `id/producer`, `id/connections`, `id/ports`, `id/conn`, `id/input` | `bolt-optimize-workflow-cleanup-memory-complexity-5380313799745612066`, `bolt/optimize-workflow-cleanup-6435047672108938677-12051453820203235666`, `enhance-node-engine-validation-7832529529333690615`, `jules-9474212697917078576-final`, `optional-ports-defaults-6114338323508528670`, +5 more |
| 21 | 9 | 0.363 | `id/multipart`, `msg/deps`, `msg/bump`, `path/versions`, `id/asyncpg`, `msg/minor`, `id/psycopg2`, `path/requirements` | `dependabot/pip/python-minor-978b58b1b8`, `pull/546/head`, `pull/619/head`, `pull/686/head`, `pull/714/head`, +4 more |
| 28 | 9 | 0.367 | `id/timezone`, `id/datetime`, `id/expires`, `id/utc`, `id/now`, `id/timedelta`, `id/expire`, `id/utcnow` | `fix-security-jwt-datetime-176656685749812344-2140584468424237267`, `pull/352/head`, `pull/370/head`, `pull/583/head`, `pull/596/head`, +4 more |
| 5 | 7 | 0.339 | `id/proxies`, `id/middleware`, `id/req`, `id/trusted`, `id/origins`, `id/proxy`, `id/forwarded`, `id/hop` | `fix/xff-spoofing-final`, `jules-1565200572967051680-746e5aa9`, `port/timer-metric`, `pull/253/head`, `pull/550/head`, +2 more |
| 13 | 7 | 0.264 | `id/getenv`, `id/dir`, `id/host`, `id/reload`, `id/port`, `msg/variable`, `msg/configurable`, `id/data` | `fix/import-does-not-serve`, `jules-configurable-data-dir-7609885797913100693`, `openhands-workspace-2p6JwFywDv3glOePqVJ5UM`, `port/data-dir`, `pull/473/head`, +2 more |
| 19 | 7 | 0.220 | `id/disabled`, `id/verdict`, `id/cherry`, `id/staging`, `id/triage`, `id/yml`, `id/dead`, `id/origin` | `jules-sunset-bootstrap`, `jules/sunset-s14-docs`, `pull/835/head`, `s13-forensics-1794327866`, `scientific-triage-docs`, +2 more |
| 7 | 6 | 0.787 | `id/word`, `id/words`, `id/gratitude`, `id/deadline`, `id/urgency`, `id/positive`, `id/thank`, `id/intent` | `bolt-optimize-ai-engine-7027917884037319553`, `bolt-optimize-ai-engine-9490147800477462605`, `bolt/optimize-ai-engine-fallback-7048942524902158717`, `pull/298/head`, `pull/307/head`, +1 more |
| 26 | 6 | 0.863 | `id/separators`, `id/func`, `id/dump`, `id/compact`, `id/partial`, `id/serialization`, `msg/serialization`, `id/heavy` | `bolt-db-json-optimization-4764718789006902431`, `bolt-json-dump-optimization-7036779522200334599`, `bolt-json-optimization-4810526327792214579`, `pull/289/head`, `pull/292/head`, +1 more |
| 34 | 6 | 0.507 | `id/playwright`, `id/e2e`, `id/headed`, `id/reporter`, `id/chromium`, `id/trace`, `id/devices`, `id/probe` | `docs/client-e2e-runbook`, `jules-13546687507968793844-8d71cc7d`, `jules-15594770323986482511-8149f6e5`, `pull/974/head`, `pull/975/head`, +1 more |

> Lexical content clustering over path names, added-line identifiers and commit subjects. It captures shared vocabulary, not shared behaviour; use it to group a merge wave, not to prove equivalence.

## Integration targets

| Target | Branches | Mean confidence | Leading tags |
| --- | --- | --- | --- |
| `main` | 1564 | 0.939 | `main-ready`, `testing-required-high`, `requires-review`, `medium-risk`, `low-file-impact` |
| `scientific` | 77 | 0.881 | `scientific-branch`, `testing-required-high`, `requires-review`, `complex`, `refactoring` |
| `orchestration-tools` | 168 | 0.898 | `orchestration-branch`, `testing-required-high`, `requires-review`, `medium-risk`, `complex` |

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
| `main-ready` | 1564 |
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
