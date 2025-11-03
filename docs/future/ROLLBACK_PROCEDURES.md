# Rollback Procedures: Distributed Worktree Documentation System

## 1. Introduction

This document outlines the procedures for rolling back the distributed worktree-based documentation system to the previous centralized workflow. These procedures should be followed if the risks identified in the `RISK_ASSESSMENT.md` document are realized and cannot be mitigated.

## 2. Triggering a Rollback

A rollback should be considered under the following circumstances:

*   Persistent and unresolvable merge conflicts between the `docs` and `main` branches.
*   Significant negative impact on developer productivity that cannot be addressed through training or tooling improvements.
*   Critical failure of the CI/CD automation that cannot be fixed in a timely manner.

The decision to initiate a rollback must be made by the project lead in consultation with the development team.

## 3. Rollback Steps

The rollback process is designed to be non-destructive and to preserve all documentation content.

1.  **Freeze Documentation Changes:**
    *   Communicate to the team that a rollback is in progress and that all new documentation work should be paused.
    *   Disable the automatic merge CI job that syncs the `docs` branch to `main`.

2.  **Merge `docs` into `main`:**
    *   Perform a final, manual merge of the `docs` branch into the `main` branch to ensure all documentation is up-to-date.
    *   `git checkout main`
    *   `git pull origin main`
    *   `git merge --no-ff docs -m "Final merge of docs branch before rollback"`
    *   Resolve any merge conflicts manually.
    *   `git push origin main`

3.  **Remove the Worktree:**
    *   From the root of the repository, run the following command to remove the worktree:
    *   `git worktree remove .docs`

4.  **Delete the `docs` Branch:**
    *   Delete the remote `docs` branch to prevent further commits.
    *   `git push origin --delete docs`
    *   Delete the local `docs` branch on all developer machines.
    *   `git branch -d docs`

5.  **Update CI/CD Configuration:**
    *   Remove the `docs.yml` workflow file from `.github/workflows/`.
    *   Update the main CI/CD pipeline to handle documentation builds from the `main` branch as it did previously.

6.  **Update Developer Documentation:**
    *   Archive the documentation related to the worktree system.
    *   Update the contributor guidelines to reflect the return to the centralized workflow.

## 4. Post-Rollback Verification

*   Verify that the documentation website builds and deploys correctly from the `main` branch.
*   Confirm that all documentation content is present and correctly formatted.
*   Communicate to the team that the rollback is complete and that they can resume documentation work on feature branches based on `main`.
