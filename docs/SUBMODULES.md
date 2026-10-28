# Git Submodules

This repository uses one git submodule:

| Submodule    | Path          | Points to                                            | Tracked branch |
| ------------ | ------------- | ---------------------------------------------------- | -------------- |
| `.taskmaster` | `.taskmaster` | `https://github.com/MasumRab/EmailIntelligence.git` | `taskmaster`   |

> **Note:** the submodule points to the **same repository** as the parent, just
> on a different branch (`taskmaster`). This keeps Task Master AI task data
> versioned independently while living in one repo. The parent branches
> (`main`, `scientific`, `orchestration-tools`) all pin the same submodule commit.

## Cloning

Clone with submodules in one step:

```bash
git clone --recursive https://github.com/MasumRab/EmailIntelligence.git
```

If you already cloned without `--recursive`, initialize the submodule:

```bash
git submodule update --init --recursive
```

## Updating the submodule

Pull the latest commit from the tracked branch (reads `branch` from `.gitmodules`):

```bash
git submodule update --remote .taskmaster
```

> Do **not** run `git -C .taskmaster pull` without a branch — the submodule's
> internal config may track a different branch and pull the wrong one. Always
> rely on `git submodule update --remote`, which uses the `branch` declared in
> `.gitmodules` (`taskmaster`).

## URL override (SSH / private / cloud sandboxes)

`.gitmodules` uses an HTTPS URL. To use SSH or a different URL without editing
the tracked `.gitmodules` file, override it in your **local** git config:

```bash
# Option A: change the submodule URL locally, then re-sync
git config submodule..taskmaster.url git@github.com:MasumRab/EmailIntelligence.git
git submodule sync
git submodule update --init --recursive

# Option B: global URL rewrite (applies to any matching remote)
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

For private access in CI/sandboxes, make sure the token/credentials used have
read scope for the repository and the `taskmaster` branch.

## CI

All CI workflows check out submodules via `submodules: recursive` on
`actions/checkout`, so `.taskmaster` is available to every CI job.

## Cloud sandboxes (Jules, Qwen-code, Codespaces, Gitpod, etc.)

These environments clone the repo their own way and may **not** initialize
submodules automatically. If `.taskmaster` is empty after the sandbox starts,
run:

```bash
git submodule update --init --recursive
```
