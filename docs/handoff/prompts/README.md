# Per-Phase AMP Prompts

One self-contained prompt per phase. Each runs in a **fresh thread** for fail-isolation, smaller context, and easier restart.

## Why split

Monolithic multi-phase prompts fail badly: huge context, no isolation, hard to restart from a mid-phase failure. Splitting gives:
- bounded context per thread
- clean restart (only re-run the failed phase)
- mode-appropriate execution (rush/deep/smart per phase)
- per-phase state-file updates

## Files

| Phase | Mode | File | Doc |
|---|---|---|---|
| 1 | rush | `phase-01-rush.txt` | phase-01-emergency-fixes.md |
| 2 | rush | `phase-02-rush.txt` | phase-02-content-fixes.md |
| 3 | rush | `phase-03-ruler-setup.txt` | phase-03-ruler-setup.md |
| 4 | rush | `phase-04-rush.txt` | phase-04-agent-rulez.md |
| 5 | deep | `phase-05-deep.txt` | phase-05-file-cleanup.md |
| 6 | deep | `phase-06-deep.txt` | phase-06-deduplication.md |
| 7 | deep | `phase-07-deep.txt` | phase-07-hierarchy.md |
| 8 | deep | `phase-08-deep.txt` | phase-08-orchestration.md |
| 9 | deep | `phase-09-deep.txt` | phase-09-verification.md |
| 10 | deep | `phase-10-deep.txt` | phase-10-rule-quality.md |
| 11 | smart | `phase-11-smart.txt` | phase-11-smart-remediation.md |
| 14 | deep | `phase-14-deep.txt` | phase-14-gitignore-unification.md |

## Usage

```bash
# Single phase, fresh thread
amp threads new --mode rush --execute "$(cat docs/handoff/prompts/phase-01-rush.txt)"

# Convenience runner
bash docs/handoff/prompts/run.sh 01    # phase 1 (auto-detects mode)
bash docs/handoff/prompts/run.sh 14
```

## Order

Run sequentially: 1 → 2 → 3 → 4 → (5,6,7,8 parallel) → 9 → 10 → 11 → 14.
Each phase ends with the agent reporting and stopping. You start the next phase as a separate thread.
