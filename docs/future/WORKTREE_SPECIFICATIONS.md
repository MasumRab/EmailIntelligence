# Distributed Worktree Documentation System: Specifications

## 1. Overview

This document provides the technical specifications for implementing a distributed documentation system using Git worktrees. The goal is to decouple the documentation workflow from the code development workflow, allowing for parallel, independent, and more efficient content creation.

## 2. Core Concepts

*   **Git Worktrees:** The system will leverage `git worktree` to maintain a separate `docs` branch checked out in a subdirectory (`.docs/`). This allows documentation to be developed and versioned independently of the main codebase.
*   **Decoupled Branches:**
    *   `main`: Contains the primary application code.
    *   `docs`: Contains all documentation source files.
    *   Feature branches for code will be based on `main`.
    *   Feature branches for documentation will be based on `docs`.
*   **Automation:** A set of scripts and CI/CD pipelines will automate the management of the worktree, branch synchronization, and deployments.

## 3. Directory Structure

The repository will have the following structure:

```
/
|-- .git/
|-- .github/
|-- .docs/      <-- Worktree checkout of the 'docs' branch
|   |-- content/
|   |-- ...
|-- src/
|-- tests/
|-- ...
```

## 4. Workflow Specification

1.  **Initialization:** A script (`scripts/setup-docs-worktree.sh`) will initialize the worktree environment for developers.
2.  **Documentation Development:**
    *   To work on documentation, a contributor will `cd .docs/`.
    *   Create a new branch off `docs`: `git checkout -b docs-my-feature`.
    *   Make changes to documentation files within the `.docs/` directory.
    *   Commit and push the `docs-my-feature` branch.
3.  **Code Development:** Code development continues as usual in the main working directory, with feature branches based on `main`.
4.  **Pull Requests:**
    *   Documentation PRs will target the `docs` branch.
    *   Code PRs will target the `main` branch.
    *   This separation allows for distinct review processes.
5.  **Synchronization:**
    *   A nightly CI job will merge the `docs` branch into `main`. This ensures that the main branch always has the latest documentation.
    *   This merge is a one-way sync (`docs` -> `main`). Code changes are never merged into `docs`.

## 5. Automation and Tooling

*   **`scripts/setup-docs-worktree.sh`:**
    *   Checks if the `.docs/` worktree exists.
    *   If not, it runs `git worktree add -b docs .docs origin/docs`.
*   **CI/CD Pipeline (`.github/workflows/docs.yml`):**
    *   **On PR to `docs`:**
        *   Builds the documentation website for preview.
        *   Runs linting and spell-checking on the documentation.
    *   **On Merge to `docs`:**
        *   Deploys the documentation to a staging environment.
    *   **On Merge to `main`:**
        *   Deploys the documentation to the production environment.
    *   **Nightly Sync:**
        *   Runs a script to merge `docs` into `main`.
